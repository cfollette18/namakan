from prisma import Prisma
from app.core.config import settings
import asyncio

# Global Prisma client instance
prisma = Prisma()

async def connect_db():
    """Connect to the database"""
    await prisma.connect()

async def disconnect_db():
    """Disconnect from the database"""
    await prisma.disconnect()

async def get_db():
    """Dependency to get database client"""
    try:
        yield prisma
    finally:
        # Prisma handles connection pooling automatically
        pass

# Synchronous wrapper for backward compatibility
def get_db_sync():
    """Synchronous database client for non-async contexts"""
    # This is a simplified wrapper - in production you'd want proper async handling
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Connect if not already connected
    if not prisma.is_connected():
        loop.run_until_complete(connect_db())

    return prisma

import redis.asyncio as redis
from app.core.config import settings

class RedisClient:
    _instance = None
    
    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
        return cls._instance
    
    @classmethod
    async def close(cls):
        if cls._instance:
            await cls._instance.close()
            cls._instance = None

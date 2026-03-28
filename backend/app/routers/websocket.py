from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import structlog
import json

logger = structlog.get_logger()

router = APIRouter()

# Connection manager for WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, project_id: str):
        await websocket.accept()
        if project_id not in self.active_connections:
            self.active_connections[project_id] = set()
        self.active_connections[project_id].add(websocket)
        logger.info("WebSocket connected", project_id=project_id)
    
    def disconnect(self, websocket: WebSocket, project_id: str):
        if project_id in self.active_connections:
            self.active_connections[project_id].discard(websocket)
            if not self.active_connections[project_id]:
                del self.active_connections[project_id]
        logger.info("WebSocket disconnected", project_id=project_id)
    
    async def send_message(self, message: dict, project_id: str):
        if project_id in self.active_connections:
            for connection in self.active_connections[project_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error("Error sending message", error=str(e))
    
    async def broadcast(self, message: dict):
        for connections in self.active_connections.values():
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error("Error broadcasting message", error=str(e))

manager = ConnectionManager()

@router.websocket("/project/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    """WebSocket endpoint for real-time project updates"""
    await manager.connect(websocket, project_id)
    
    try:
        while True:
            # Keep connection alive and receive client messages
            data = await websocket.receive_text()
            logger.debug("Received WebSocket message", data=data)
            
            # Echo back for now (in production, handle different message types)
            await websocket.send_text(f"Message received: {data}")
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, project_id)
        logger.info("Client disconnected", project_id=project_id)

from typing import Dict, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


class ConnectionManager:
    def __init__(self) -> None:
        self.active_rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_rooms.setdefault(room, []).append(websocket)

    def disconnect(self, room: str, websocket: WebSocket) -> None:
        if room in self.active_rooms:
            self.active_rooms[room].remove(websocket)
            if not self.active_rooms[room]:
                del self.active_rooms[room]

    async def broadcast(self, room: str, message: str, sender: WebSocket) -> None:
        for ws in self.active_rooms.get(room, []):
            if ws is not sender:
                await ws.send_text(message)


manager = ConnectionManager()


@router.websocket("/screen-share/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str) -> None:
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(room_id, data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)

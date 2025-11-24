from fastapi import APIRouter, WebSocket

router = APIRouter(prefix="/notify", tags=["notify"])
connections: list[WebSocket] = []

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connections.append(ws)
    try:
        while True:
            # keep connection alive; client may send ping messages
            await ws.receive_text()
    except Exception:
        connections.remove(ws)

async def broadcast_message(message: str):
    for ws in list(connections):
        try:
            await ws.send_text(message)
        except Exception:
            connections.remove(ws)

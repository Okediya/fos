from aiohttp import web, WSMsgType
import json

clients = {}

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    
    client_id = str(len(clients))
    clients[client_id] = ws
    print(f"Client {client_id} connected")
    
    try:
        
        await ws.send_json({"type": "client_id", "id": client_id})
        
        # Handle incoming messages
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                data = json.loads(msg.data)
                print(f"Received from {client_id}: {data}")
                
                # Relay signaling messages to the target client
                target_id = data.get("target")
                if target_id in clients and target_id != client_id:
                    await clients[target_id].send_json({
                        "type": data["type"],
                        "from": client_id,
                        "data": data["data"]
                    })
                else:
                    print(f"Target {target_id} not found or invalid")
            elif msg.type == WSMsgType.ERROR:
                print(f"WebSocket error: {ws.exception()}")
    
    finally:
        # Clean up on disconnect
        clients.pop(client_id, None)
        print(f"Client {client_id} disconnected")
    
    return ws

# Set up the aiohttp application
app = web.Application()
app.router.add_get('/ws', websocket_handler)

if __name__ == '__main__':
    print("Starting signaling server on http://localhost:8080")
    web.run_app(app, host='localhost', port=8080)
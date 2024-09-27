import asyncio
import websockets
import json

# Global list to keep track of connected clients
connected_clients = set()

async def handle_connection(websocket, path):
    # Register the new client
    connected_clients.add(websocket)
    try:
        while True:
            # Receive message from client
            message = await websocket.recv()
            print(f"Received: {message}")

            # Parse JSON message
            data = json.loads(message)
            print(f"Parsed JSON: {data}")

            # Check action and perform corresponding operation
            if data.get("action") == "build":
                await handle_build(data)
            elif data.get("action") == "query":
                await handle_query(data)

            # Send response back to client
            response_data = {
                'status': 'ok',
                'message': 'Action processed',
                'received_data': data
            }
            await websocket.send(json.dumps(response_data))

    except websockets.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    finally:
        # Unregister the client on disconnect
        connected_clients.remove(websocket)

async def handle_build(data):
    # Implement your build logic here
    print(f"Handling build action with data: {data}")

async def handle_query(data):
    # Implement your query logic here
    print(f"Handling query action with data: {data}")

async def send_message(message):
    # Send a message to all connected clients
    if connected_clients:  # Check if there are any connected clients
        message_data = json.dumps(message)
        await asyncio.wait([client.send(message_data) for client in connected_clients])

# Start WebSocket server
start_server = websockets.serve(handle_connection, "localhost", 12345)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server started on ws://localhost:12345")
asyncio.get_event_loop().run_forever()

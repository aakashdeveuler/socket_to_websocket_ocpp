import asyncio
import websockets

async def handle_socket_data(websocket, path):
    # Wait for data from the socket
    data = await websocket.recv()
    # Send the data to the socket
    await websocket.send(data)

# Start the WebSocket server
start_server = websockets.serve(handle_socket_data, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

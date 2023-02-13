import asyncio
import websockets
import socket

async def handle_socket_data(websocket, path):
    # Wait for data from the socket
    data = await websocket.recv()
    # Send the data to the socket
    await websocket.send(data)

# Start the WebSocket server

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
serverSocket.bind(("127.0.0.1",8765));
serverSocket.listen();

start_server = websockets.serve(handle_socket_data, '127.0.0.1', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

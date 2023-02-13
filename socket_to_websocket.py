import asyncio
import socket
import websockets

async def handle_socket_data(websocket, path):
    # Connect to the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 12345))
    # Receive data from the socket
    data = sock.recv(1024).decode()
    # Send the data to the WebSocket
    await websocket.send(data)
    # Close the socket connection
    sock.close()

# Start the WebSocket server
start_server = websockets.serve(handle_socket_data, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

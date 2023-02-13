import asyncio
import socket
import websockets
import socket

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

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

serverSocket.bind(("localhost",12345));
print("socket connected")
serverSocket.listen();
while(True):
    (clientConnected, clientAddress) = serverSocket.accept();
    print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]));
    dataFromClient = clientConnected.recv(1024)
    print(dataFromClient.decode());


start_server = websockets.serve(handle_socket_data, '127.0.0.1', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

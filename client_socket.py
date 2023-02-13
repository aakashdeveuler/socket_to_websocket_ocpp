import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

clientSocket.connect(("localhost",12345));
print("connets")

data = "Hello Server!";
clientSocket.send(data.encode());


 
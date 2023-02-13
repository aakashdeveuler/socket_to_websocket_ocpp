import socket

data_final=""
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

serverSocket.bind(("localhost",12345));
print("socket connectedcccc")
serverSocket.listen();
while(True):
    (clientConnected, clientAddress) = serverSocket.accept();
    print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]));
    dataFromClient = clientConnected.recv(1024)
    Decoded_data=dataFromClient.decode();
    data_final=Decoded_data
    print(type(Decoded_data), "               ", Decoded_data);

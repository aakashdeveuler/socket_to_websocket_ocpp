import socket

DISCONNECT_MSG = "!DISCONNECT"

clientSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

clientSocket.connect(("fe80::c166:bbb6:ecf4:24c5%14",12345))
print("connects")


connected = True
while connected:
    data = input("> ")
    clientSocket.send(data.encode())
    
    if data == DISCONNECT_MSG:
        connected = False
    else:
        dataFromServer =  clientSocket.recv(1024).decode()
        print("message from steve to tcu 2")
        print(dataFromServer)

data = '[2, "97496a9r-867k-4d28-969d-10f795ff4545", "BootNotification", {"chargePointVendor": "123", "chargePointModel": "Euler", "chargePointSerialNumber": "", "chargeBoxSerialNumber": "", "firmwareVersion": "", "iccid": "", "imsi": "", "meterSerialNumber": "", "meterType": ""}]'

# dataFromServer =  clientSocket.recv(1024)

# print("message from steve to tcu 1")
# print(dataFromServer.decode())
# clientSocket.close()
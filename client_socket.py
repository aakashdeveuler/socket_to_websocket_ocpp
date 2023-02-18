import socket

DISCONNECT_MSG = "!DISCONNECT"

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect(("10.10.10.182",12345))
print("connects")


connected = True
while connected:
    data = input("> ")
    
    clientSocket.send(data.encode())
    if data == DISCONNECT_MSG:
        connected = False
    else:
        dataFromServer =  clientSocket.recv(1024).decode()
        print("message from steve to tcu 1")
        print(dataFromServer)

data = '[2, "97495a9r-867k-4d28-769d-10f795ff4545", "BootNotification", {"chargePointVendor": "123", "chargePointModel": "Euler", "chargePointSerialNumber": "", "chargeBoxSerialNumber": "", "firmwareVersion": "", "iccid": "", "imsi": "", "meterSerialNumber": "", "meterType": ""}]'

# dataFromServer =  clientSocket.recv(1024)

# print("message from steve to tcu 1")
# print(dataFromServer.decode())
clientSocket.close()
import socket

clientSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

clientSocket.connect(("fe80::c166:bbb6:ecf4:24c5%14",12345))
print("connects")

data = '[2, "97496a9r-867k-4d29-969d-10f795ff4545", "BootNotification", {"chargePointVendor": "", "chargePointModel": "Euler", "chargePointSerialNumber": "", "chargeBoxSerialNumber": "", "firmwareVersion": "", "iccid": "", "imsi": "", "meterSerialNumber": "", "meterType": ""}]'
clientSocket.send(data.encode())

dataFromServer =  clientSocket.recv(1024)

print("message from steve to tcu 2")
print(dataFromServer.decode())
# clientSocket.close()
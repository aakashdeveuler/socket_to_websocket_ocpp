import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

clientSocket.connect(("localhost",12345));
print("connects")

data = '[2, "97416a4e-037f-4a20-945d-10f995ff4545", "BootNotification", {"chargePointVendor": "", "chargePointModel": "Euler", "chargePointSerialNumber": "", "chargeBoxSerialNumber": "", "firmwareVersion": "", "iccid": "", "imsi": "", "meterSerialNumber": "", "meterType": ""}]';
clientSocket.send(data.encode());



dataFromServer =  clientSocket.recv(1024);
import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

clientSocket.connect(("localhost",12345));
print("connets")

data = '[2, "9ba16a4e-037f-4a20-9b5d-20f975ff4545", "BootNotification", {"chargePointVendor": "", "chargePointModel": "Euler", "chargePointSerialNumber": "", "chargeBoxSerialNumber": "", "firmwareVersion": "", "iccid": "", "imsi": "", "meterSerialNumber": "", "meterType": ""}]';
clientSocket.send(data.encode());


 
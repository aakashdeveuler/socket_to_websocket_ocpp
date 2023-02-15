import asyncio
import logging
import json
import websockets
import socket
import mysql.connector

from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import RegistrationStatus

logging.basicConfig(level=logging.INFO)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="socketsteve"
)

class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
        )
          
        response = await self.call(request)
        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")


async def main():
    async with websockets.connect(
        "ws://43.205.177.121:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
    ) as ws:

        cp = ChargePoint("1234", ws)

        await asyncio.gather(cp.start(), cp.send_boot_notification())
    print("asyncio.gather ended")


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    while(True):
        serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        serverSocket.bind(("localhost",12345))
        
        print("socket connected")
        serverSocket.listen()
        while(True):
            (clientConnected, clientAddress) = serverSocket.accept()
            print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))
            dataFromClient = clientConnected.recv(1024)
            Decoded_data=dataFromClient.decode()
            list = json.loads(Decoded_data)
            data = list[3]
            
            mycursor = mydb.cursor()

            asyncio.run(main())
            mycursor.execute("SELECT * FROM bootnotificationtotcu")
            rows = mycursor.fetchall()
            print("Data sending to client")
            # print(rows[-1])
            sendtcu = str(rows[-1][1])
            clientConnected.send(sendtcu.encode())
            break
        
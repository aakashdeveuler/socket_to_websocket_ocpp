import asyncio
import logging
import json
import websockets
import socket
import mysql.connector


from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import RegistrationStatus

from _thread import *
import threading

print_lock = threading.Lock()

logging.basicConfig(level=logging.INFO)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="socketsteve"
)


# Threaded function
def threaded(client):
   while True:

       # Data is received from the client
       data = client.recv(1024)
       if not data:
           print('No connection, Bye')
          
           # Releasing lock on exit
           print_lock.release()
           break

       # Reverse the given string from the client
       data = data[::-1]

       # Send back reversed string to the client
       client.send(data)

   # Connection closed
   client.close()



class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
        )
          
        response = await self.call(request)
        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")
        # serverSocket.close()


async def main():
    async with websockets.connect(
        "ws://43.205.177.121:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
    ) as ws:

        cp = ChargePoint("1234", ws)

        await asyncio.gather(cp.start(), cp.send_boot_notification())


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    serverSocket.bind(("localhost",12345));
    
    print("socket connected")
    serverSocket.listen();
    while(True):
        (clientConnected, clientAddress) = serverSocket.accept();
        print_lock.acquire()
        print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]));
        start_new_thread(threaded, (clientConnected,))
        dataFromClient = clientConnected.recv(1024)
        Decoded_data=dataFromClient.decode();
        list = json.loads(Decoded_data)
        data = list[3]
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM socketsteve")
        myresult = mycursor.fetchone()
        mydb.commit()
        
        print("type of myresult")
        print(type(myresult))
        
        clientConnected.send()
        asyncio.run(main())
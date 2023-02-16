import asyncio
import logging
import json
import websockets
import socket
import threading
socket.getaddrinfo('fe80::c166:bbb6:ecf4:24c5%14', 12345)

from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import RegistrationStatus

logging.basicConfig(level=logging.INFO)

DISCONNECT_MESSAGE = "!DISCONNECT"

class ChargePoint(cp):
    async def send_boot_notification(self,data):
        request = call.BootNotificationPayload(
            charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
        )
          
        response = await self.call(request)
        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")


async def main(data):
    receive_data=""
    async with websockets.connect(
        "ws://43.205.177.121:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
    ) as ws:

        cp = ChargePoint("1234", ws)
        
        val = await asyncio.gather(cp.start(), cp.send_boot_notification(data))
        receive_data = val[0]
    return receive_data


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    print("[STARTING] server is starting ....")
    
    while(True):
        def handle_client(conn, addr):
            data = {}
            print(f"[NEW CONNECTION] {addr} connected.")
            connected = True
            while connected:
                print("Accepted a connection request from %s:%s"%(addr[0], addr[1]))
                dataFromClient = conn.recv(1024).decode()
                if dataFromClient == DISCONNECT_MESSAGE:
                    connected = False
                list = json.loads(dataFromClient)
                data=list[3]
                receive_data = asyncio.run(main(data))
                clientConnected.send(receive_data.encode())
                break
            conn.close()
        
        serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        serverSocket.bind(("fe80::c166:bbb6:ecf4:24c5%14", 12345))
        serverSocket.listen()
                                
            
        while(True):
            (clientConnected, clientAddress) = serverSocket.accept()
            thread = threading.Thread(target=handle_client, args=(clientConnected, clientAddress))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
            break

        
import asyncio
import logging
import json
import websockets
import socket
import threading
socket.getaddrinfo('localhost', 12345)

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
    
    # while(True):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("localhost", 12345))
    serverSocket.listen()
    
    def handle_client(conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            try: 
                print("Accepted a connection request from %s:%s"%(addr[0], addr[1]))
                dataFromClient = conn.recv(1024).decode()
                    
                if dataFromClient == DISCONNECT_MESSAGE:
                    connected = False
                    
                else:    
                    print("=--------------------")
                    print(dataFromClient)
                    print("=--------------------")
                    
                    list = json.loads(dataFromClient)
                    data=list[3]
                    receive_data = None
                    receive_data = asyncio.run(main(data))
                    # print("-==-=-=-=-=-=-=-=-=")
                    # print(receive_data)
                    if receive_data != None:
                        clientConnected.send((receive_data+str(addr[1])).encode())
                        print("sending to client port: ", addr[1])
                    else:
                        clientConnected.send("nahi aaya".encode())
                    
            except: 
                print("error occured Steve might be down")
                connected = False
                conn.close()
        
    while(True):
        (clientConnected, clientAddress) = serverSocket.accept()
        thread = threading.Thread(target=handle_client, args=(clientConnected, clientAddress))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
        # break

        
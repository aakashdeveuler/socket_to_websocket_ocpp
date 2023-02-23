import asyncio
import logging
import json
import time
import websockets
import socket
import threading

socket.getaddrinfo('localhost', 12345)

from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import RegistrationStatus
from ocpp.v16.enums import DiagnosticsStatus

logging.basicConfig(level=logging.INFO)

DISCONNECT_MESSAGE = "!DISCONNECT"

class ChargePoint(cp):
    
## .....................................................................................................
    
    async def send_boot_notification(self,data):
        request = call.BootNotificationPayload(
            charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
        )
          
        response = await self.call(request)
        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")

## .....................................................................................................

    async def send_heartbeat(self):
        request = call.HeartbeatPayload()
          
        response = await self.call(request)
        print(response)
        
        
## .....................................................................................................


    async def send_diagnostics_status_notification(self,data):
        request = call.DiagnosticsStatusNotificationPayload(
            status=data.get("status")
        )
          
        response = await self.call(request)
        if request.status == DiagnosticsStatus.uploaded:
            print("Diagnostic status uploaded.")


## .....................................................................................................
## .....................................................................................................
## .....................................................................................................


async def main_bootnotification(data):
    receive_data=""
    async with websockets.connect(
        "ws://43.205.177.121:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
    ) as ws:

        cp = ChargePoint("1234", ws)
        
        val = await asyncio.gather(cp.start_bootnotification(), cp.send_boot_notification(data))
        receive_data = val[0]
    return receive_data


## .....................................................................................................
## .....................................................................................................


async def main_heartbeat():
    receive_data=""
    async with websockets.connect(
        "ws://43.205.177.121:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
    ) as ws:

        cp = ChargePoint("1234", ws)
        
        val = await asyncio.gather(cp.start_heartbeat(), cp.send_heartbeat())
        receive_data = val[0]
    return receive_data


## .....................................................................................................
## .....................................................................................................

async def main_diagnostics(data):
    receive_data=""
    async with websockets.connect(
        "ws://43.205.177.121:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
    ) as ws:

        cp = ChargePoint("1234", ws)
        
        val = await asyncio.gather(cp.start_diagnostics(), cp.send_diagnostics_status_notification(data))
        receive_data = val[0]
    return receive_data





def handle_client(clientConnected, clientAddress):
        print(f"[NEW CONNECTION] {clientAddress} connected.")
        try:
            connected = True
            while connected:
                print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))
                dataFromClient = clientConnected.recv(1024).decode()
                
                if dataFromClient == DISCONNECT_MESSAGE:
                    print(f"Client {clientAddress} disconnected")
                    connected = False
                    break
                    
                    
                print("=--------------------")
                print(dataFromClient)
                print("=--------------------")
                
                list = json.loads(dataFromClient)
                data=list[0]
                
                receiveBoot_data = asyncio.run(main_bootnotification(data))
                print(receiveBoot_data)
                clientConnected.send(receiveBoot_data.encode())
                print("sending to client port: ", clientAddress[1])
                
                # time.sleep(2)
                
                receiveHeartbeat_data = asyncio.run(main_heartbeat())
                clientConnected.send(receiveHeartbeat_data.encode())
                
                
                # receiveDiagnostic_data = asyncio.run(main_diagnostics(data))
                # clientConnected.send(receiveDiagnostic_data.encode())
                
                
                
                
        except:
            print("Error: Steve might be down :(")
        print(f"Client {clientAddress} disconnected")            
        clientConnected.close()
                    

def run_server():
    print("[STARTING] server is starting ....")
    # Create a TCP socket and bind it to a local address and port
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("localhost", 12345))
    # Listen for incoming connections
    serverSocket.listen(5)
    
    while(True):
        # Accept a new client connection
        clientConnected, clientAddress = serverSocket.accept()
        
        # Create a new thread to handle the client connection
        thread = threading.Thread(target=handle_client, args=(clientConnected, clientAddress))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")


if __name__ == "__main__":
    run_server()
    ## HeartBeat Msg
    ## [2,"1234567890","HeartBeat",{}]
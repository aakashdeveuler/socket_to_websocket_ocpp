import asyncio
import binascii
import codecs
import logging
import json
import time
import websockets
import socket
import threading
import binascii
import re

from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import *

logging.basicConfig(level=logging.INFO)

DISCONNECT_MESSAGE = "!DISCONNECT"

def extract_between_strings(start, end, text):
    pattern = re.escape(start) + r'(.*?)' + re.escape(end)
    match = re.search(pattern, text)
    if match:
        return start + match.group(1) + end
    else:
        return None

class ChargePoint(cp):
    
## .....................................................................................................

    async def send(self, data, dataID, action):
        if action == "authorize":
            request = call.AuthorizePayload(
                id_tag=data.get("idTag")
            )
            response = await self.call(request, dataID)
            if response.id_tag_info.get("status") == AuthorizationStatus.accepted:
                print("Authorization Successfull.")
            elif response.id_tag_info.get("status") == AuthorizationStatus.invalid:
                print("Invalid Authorization.")
            elif response.id_tag_info.get("status") == AuthorizationStatus.blocked:
                print("Authorization Blocked.")
            elif response.id_tag_info.get("status") == AuthorizationStatus.expired:
                print("Authorization Expired.")
                
        elif action == "bootnotification":
            request = call.BootNotificationPayload(
                charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
            )
            
            response = await self.call(request, dataID)
            if response.status == RegistrationStatus.accepted:
                print("BootNotification Success.")
            elif response.status == RegistrationStatus.pending:
                print("BootNotification Pending.")
            elif response.status == RegistrationStatus.rejected:
                print("BootNotification Rejected.")
                
        elif action == "heartbeat":
            request = call.HeartbeatPayload()
          
            response = await self.call(request, dataID)
            print(response)
            
        elif action == "diagnosticsstatusnotification":
            request = call.DiagnosticsStatusNotificationPayload(
                status=data.get("status")
            )
            
            response = await self.call(request, dataID)
            
        elif action == "statusnotification":
            request = call.StatusNotificationPayload(
                connector_id=data.get("connectorId"), error_code=data.get("errorCode"), status=data.get("status")
            )
            
            response = await self.call(request, dataID)
            # if response.status == RegistrationStatus.accepted:
            print("Status Notification send.")
            
        elif action == "metervalues":
            request = call.MeterValuesPayload(
                connector_id=data.get("connectorId"), meter_value=data.get("meterValue"), transaction_id=data.get("transactionId")
            )
            
            response = await self.call(request, dataID)
            # if response.status == RegistrationStatus.accepted:
            print("Meter value Done")
            
            
        elif action == "firmwarestatusnotification":
            request = call.FirmwareStatusNotificationPayload(
                status=data.get("status")
            )
            
            response = await self.call(request, dataID)
            
        elif action == "datatransfer":
            request = call.DataTransferPayload(
                vendor_id=data.get("vendorId"), message_id=data.get("messageId"), data=data.get("data")
            )
            
            response = await self.call(request, dataID)
            print(response)
            
        elif action == "starttransaction":
            request = call.StartTransactionPayload(
                connector_id=data.get("connectorId"), id_tag=data.get("idTag"), meter_start=data.get("meterStart"), reservation_id=data.get("reservationId"), timestamp=data.get("timestamp")
            )
            
            response = await self.call(request, dataID)
            print("Transaction Started")
            
        elif action == "stoptransaction":
            request = call.StopTransactionPayload(
                id_tag=data.get("idTag"), meter_stop=data.get("meterStop"), transaction_id=data.get("transactionId"), timestamp=data.get("timestamp")
            )
            
            response = await self.call(request, dataID)
            print("Transaction Stopped")    
        
            
## .....................................................................................................

        
async def main(data, dataID, action):
    receive_data=""
    action = action.lower()
    async with websockets.connect(
        "ws://13.234.76.186:8080/steve/websocket/CentralSystemService/"+dataID, subprotocols=["ocpp1.6"]
    ) as ws:

        cp = ChargePoint(dataID, ws)
        # val = await asyncio.gather(cp.start(action), cp.sendFunc[action](data, dataID))
        val = await asyncio.gather(cp.start(action), cp.send(data, dataID, action))
    receive_data = val[0]
    return receive_data
        
        

# ## .....................................................................................................
# ## .....................................................................................................


def handle_client(clientConnected, clientAddress):
        print(f"[NEW CONNECTION] {clientAddress} connected.")
        try:
            connected = True
            print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))
            while connected:
                # Assuming TCU will always give data similar to "state".
                # If data is coming similar to "rsp", then don't do binascii.hexlify()
                dataFromClient = clientConnected.recv(1024)
                print(dataFromClient)
                print(type(dataFromClient))
                dataFromClient = binascii.hexlify(dataFromClient)  # comment this if no slash in message
                print("Slash(\) removed from byte")
                print(dataFromClient)
                print("oioioioioioioioioioio")
                dataFromClient = codecs.decode(dataFromClient, 'utf-8')
                print("String form of byte")
                print(dataFromClient)
                print(type(dataFromClient))
                print("oioioioioioioioioioio")

                if dataFromClient == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"Client {clientAddress} disconnected")
                    break
                
                # elif(bytearray.fromhex(dataFromClient[:2]).decode()=='['):  # Notification Messages
                #     dataFromClient = bytearray.fromhex(dataFromClient).decode()
                #     print("=--------------------")
                #     print(dataFromClient)
                #     print("=--------------------")
                    
                #     list = json.loads(dataFromClient)
                #     data=list[3]
                #     dataID = list[1]
                #     action = list[2]
                    
                #     receivedData = asyncio.run(main(data, dataID, action))
                #     clientConnected.send(receivedData.encode())
                
                elif(dataFromClient[14:16]=='7b'):  # Notification Messages
                    dataFromClient = extract_between_strings("5b", "7d5d", dataFromClient)
                    dataFromClient = bytearray.fromhex(dataFromClient).decode()
                    print("=--------------------")
                    print(dataFromClient)
                    print("=--------------------")
                    
                    list = json.loads(dataFromClient)
                    data=list[3]
                    dataID = list[1]
                    action = list[2]
                    
                    receivedData = asyncio.run(main(data, dataID, action))
                    clientConnected.send(receivedData.encode())
                
                elif(int(dataFromClient[:4],16) == 15): # IMEI Message (000f383636393037303533323933373333)
                    # imei is from imei[2:17]
                    imei = (bytearray.fromhex(dataFromClient).decode())
                    # print(len(imei))
                    # print(imei[2:17])
                    # print(type(imei))
                    imeiCheck = "01"
                    clientConnected.send(imeiCheck.encode())  # converts imeiCheck to b'01
                    print("Check sent ")
                
                elif(int(dataFromClient[:8],16) == 0 or bytearray.fromhex(dataFromClient[:2]).decode()=='/'):  # this is State message (longitude, latitude)
                # elif(int(dataFromClient[:1],16) == 0):  # this is State message (longitude, latitude)
                    stateCheck = "00000002"
                    clientConnected.send(stateCheck.encode())  # converts stateCheck to b'00000002
                    print("state response sent")
                    
                elif(int(dataFromClient[:1],16) == 0):
                    print("2nd msg")
            
        
                # elif(bytearray.fromhex(dataFromClient[:2]).decode()=='['):  # Notification Messages
                #     dataFromClient = bytearray.fromhex(dataFromClient).decode()
                #     print("=--------------------")
                #     print(dataFromClient)
                #     print("=--------------------")
                    
                #     list = json.loads(dataFromClient)
                #     data=list[3]
                #     dataID = list[1]
                #     action = list[2]
                    
                #     receivedData = asyncio.run(main(data, dataID, action))
                #     clientConnected.send(receivedData.encode())
                    
                else:
                    print("Received Message in not in our Records !!!")
                    connected = False
                    print(f"Client {clientAddress} disconnected")
                    break
            
        except Exception as e:
            print(e)
            quit()
            print("Error: Steve might be down :(")
        print(f"Client {clientAddress} disconnected")            
        clientConnected.close()
                    

def run_server():
    print("[STARTING] server is starting ....")
    # Create a TCP socket and bind it to a local address and port
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("172.31.8.31", 12345))
    # Listen for incoming connections
    serverSocket.listen(50)
    
    
    while(True):
        # Accept a new client connection
        clientConnected, clientAddress = serverSocket.accept()
        
        # Create a new thread to handle the client connection
        thread = threading.Thread(target=handle_client, args=(clientConnected, clientAddress))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")


if __name__ == "__main__":
    run_server()
    

import asyncio
import binascii
import logging
import json
import time
import websockets
import socket
import threading
import binascii

from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import *

logging.basicConfig(level=logging.INFO)

DISCONNECT_MESSAGE = "!DISCONNECT"

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
        "ws://127.0.0.1:8080/steve/websocket/CentralSystemService/"+dataID, subprotocols=["ocpp1.6"]
    ) as ws:

        cp = ChargePoint(dataID, ws)
        # val = await asyncio.gather(cp.start(action), cp.sendFunc[action](data, dataID))
        val = await asyncio.gather(cp.start(action), cp.send(data, dataID, action))
    receive_data = val[0]
    return receive_data
        
        

# ## .....................................................................................................
# ## .....................................................................................................


def handle_client(clientConnected, clientAddress):
        # lock = threading.Lock()
        print(f"[NEW CONNECTION] {clientAddress} connected.")
        try:
            connected = True
            print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))
            # lock.acquire()
            while connected:
                dataFromClient = clientConnected.recv(1024)
                # dataFromClient = clientConnected.recv(1024)
                print("data from client :",dataFromClient)
                # print("Len of client ", len(dataFromClient))

                if dataFromClient == DISCONNECT_MESSAGE:
                    print(f"Client {clientAddress} disconnected")
                    connected = False
                    break
                # elif(int(dataFromClient[:4],16) == 15):
                #     imeiCheck = "01"
                #     print("imei received .... ")
                #     if (bytes.fromhex(dataFromClient[4:],16).decode('utf-8')) == 866907053293733:
                #         print("got it")
                #     print(int(dataFromClient[4:],16))
                #     clientConnected.send(imeiCheck.encode())
                #     print("Check sent ")
                #     # time.sleep(2)
                #     # latlang = binascii.hexlify(clientConnected.recv(1024))
                #     # print("Received latlong ")
                #     # print(latlang)    
                #     # print("Len of client ", len(latlang))
                #     # clientConnected.send('00000002'.encode())
                #     # print("check 2 sent ")
                
                # elif(dataFromClient[:8]) == "00000000":
                #     stateCheck = "00000002"
                #     clientConnected.send(stateCheck.encode())
                #     print("state response sent")
            
        
                else:
                    print("=--------------------")
                    print(dataFromClient)
                    # print(dataFromClient[:4])
                    print("=--------------------")
                    
                    list = json.loads(dataFromClient)
                    data=list[3]
                    dataID = list[1]
                    action = list[2]
                    
                    receivedData = asyncio.run(main(data, dataID, action))
                    clientConnected.send(receivedData.encode())

                
                # if dataFromClient == DISCONNECT_MESSAGE:
                #     print(f"Client {clientAddress} disconnected")
                #     connected = False
                #     break
                # elif(dataFromClient[2:] == "866907053293733"):
                #     check = "01"
                #     print("imei received .... ")
                #     clientConnected.send(check.encode())
                #     print("Check sent ")
                #     # time.sleep(2)
                #     latlang = binascii.hexlify(clientConnected.recv(1024))
                #     print("Received latlong ")
                #     print(latlang)    
                #     print("Len of client ", len(latlang))
                #     clientConnected.send('00000002'.encode())
                #     print("check 2 sent ")
        
                # else:
                #     print("=--------------------")
                #     print(dataFromClient)
                #     print("=--------------------")
                    
                #     list = json.loads(dataFromClient)
                #     data=list[3]
                #     dataID = list[1]
                #     action = list[2]
                    
                #     receivedData = asyncio.run(main(data, dataID, action))
                #     clientConnected.send(receivedData.encode())
            
            
        except KeyboardInterrupt:
            quit()
            print("Error: Steve might be down :(")
        print(f"Client {clientAddress} disconnected")            
        clientConnected.close()
        # lock.release()
                    

def run_server():
    print("[STARTING] server is starting ....")
    # Create a TCP socket and bind it to a local address and port
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("10.10.11.70", 8080))
    # Listen for incoming connections
    serverSocket.listen(50)
    
    
    while(True):
        # Accept a new client connection
        clientConnected, clientAddress = serverSocket.accept()
        
        # Create a new thread to handle the client connection
        # thread = threading.Thread(target=handle_client, args=(clientConnected, clientAddress))
        # thread.start()
        # print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
        
        handle_client(clientConnected, clientAddress)


if __name__ == "__main__":
    run_server()
    
    
    
# ## .....................................................................................................
    
#     async def send_authorize(self,data,dataID):
#         request = call.AuthorizePayload(
#             id_tag=data.get("idTag")
#         )
          
#         response = await self.call(request, dataID)
#         if response.id_tag_info.get("status") == AuthorizationStatus.accepted:
#             print("Authorization Successfull.")
#         elif response.id_tag_info.get("status") == AuthorizationStatus.invalid:
#             print("Invalid Authorization.")
#         elif response.id_tag_info.get("status") == AuthorizationStatus.blocked:
#             print("Authorization Blocked.")
#         elif response.id_tag_info.get("status") == AuthorizationStatus.expired:
#             print("Authorization Expired.")
    
    
# ## .....................................................................................................
    
#     async def send_bootnotification(self,data,dataID):
#         print(data)
#         request = call.BootNotificationPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("BootNotification Success.")
#         elif response.status == RegistrationStatus.pending:
#             print("BootNotification Pending.")
#         elif response.status == RegistrationStatus.rejected:
#             print("BootNotification Rejected.")


# ## .....................................................................................................
    
#             # From Steve
    
#     # async def send_cancel_reservation(self,data,dataID):
#     #     request = call.CancelReservationPayload(
#     #         charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#     #     )
          
#     #     response = await self.call(request, dataID)
#     #     if response.status == CancelReservationStatus.accepted:
#     #         print("Reservation Cancelled.")


# ## .....................................................................................................
    
#     async def send_certificates_signed(self,data,dataID):
#         request = call.CertificateSignedPayload(
#             certificate_chain=data.get("certificateChain")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == CertificateSignedStatus.accepted:
#             print("Certificate Signed.")


# ## .....................................................................................................
    
#     async def send_change_availability(self,data,dataID):
#         request = call.ChangeAvailabilityPayload(
#             connector_id=data.get("chargePointModel")
#             # Check this from call.py file
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == AvailabilityStatus.accepted:
#             print("Availability status updated.")


# ## .....................................................................................................
    
#     async def send_change_configuration(self,data,dataID):
#         request = call.ChangeConfigurationPayload(
#             key=data.get("chargePointModel"), value=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_clear_cache(self,data,dataID):
#         request = call.ClearCachePayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_clear_charging_profile(self,data,dataID):
#         request = call.ClearChargingProfilePayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_data_transfer(self,data,dataID):
#         request = call.DataTransferPayload(
#             vendor_id=data.get("vendorId"), message_id=data.get("messageId"), data=data.get("data")
#         )
          
#         response = await self.call(request, dataID)
#         print(response)
#         # if response.status == DataTransferStatus.accepted:
#         #     print("Data Transfered Successfully.")


# ## .....................................................................................................
    
#     async def send_delete_certificate(self,data,dataID):
#         request = call.DeleteCertificatePayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_diagnostics_status_notification(self,data,dataID):
#         request = call.DiagnosticsStatusNotificationPayload(
#             status=data.get("status")
#         )
          
#         response = await self.call(request, dataID)
#         # if response.status == DiagnosticsStatus.accepted:
#         #     print("Diagnostics Accepted.")


# ## .....................................................................................................
    
#     async def send_extended_trigger_message(self,data,dataID):
#         request = call.ExtendedTriggerMessagePayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_firmware_status_notification(self,data,dataID):
#         request = call.FirmwareStatusNotificationPayload(
#             status=data.get("status")
#         )
          
#         response = await self.call(request, dataID)
#         # if response.status == FirmwareStatus.accepted:
#         #     print("Firmware Accepted Successfully.")


# ## .....................................................................................................
    
#     async def send_get_composite_schedule(self,data,dataID):
#         request = call.GetCompositeSchedulePayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_get_configuration(self,data,dataID):
#         request = call.GetConfigurationPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_get_diagnostics(self,data,dataID):
#         request = call.GetDiagnosticsPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_get_installed_certificate_ids(self,data,dataID):
#         request = call.GetInstalledCertificateIdsPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_get_local_list_version(self,data,dataID):
#         request = call.GetLocalListVersionPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_get_log(self,data,dataID):
#         request = call.GetLogPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_heartbeat(self, dataID):
#         request = call.HeartbeatPayload()
          
#         response = await self.call(request, dataID)
#         print(response)


# ## .....................................................................................................
    
#     async def send_install_certificate(self,data,dataID):
#         request = call.InstallCertificatePayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_log_status_notification(self,data,dataID):
#         request = call.LogStatusNotificationPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_meter_values(self,data,dataID):
#         request = call.MeterValuesPayload(
#             connector_id=data.get("connectorId"), meter_value=data.get("meterValue"), transaction_id=data.get("transactionId")
#         )
          
#         response = await self.call(request, dataID)
#         # if response.status == RegistrationStatus.accepted:
#         print("Meter value Done")


# ## .....................................................................................................
    
#     async def send_remote_start_transaction(self,data,dataID):
#         request = call.RemoteStartTransactionPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_remote_stop_transaction(self,data,dataID):
#         request = call.RemoteStopTransactionPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_reserve_now(self,data,dataID):
#         request = call.ReserveNowPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_reset(self,data,dataID):
#         request = call.ResetPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_security_event_notification(self,data,dataID):
#         request = call.SecurityEventNotificationPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_send_local_list(self,data,dataID):
#         request = call.SendLocalListPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_set_charging_profile(self,data,dataID):
#         request = call.SetChargingProfilePayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_sign_certificate(self,data,dataID):
#         request = call.SignCertificatePayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")



        
# ## .....................................................................................................
    
#     async def send_signed_firmware_status_notification(self,data,dataID):
#         request = call.SignedFirmwareStatusNotificationPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")



# ## .....................................................................................................
    
#     async def send_signed_update_firmware(self,data,dataID):
#         request = call.SignedUpdateFirmwarePayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


# ## .....................................................................................................
    
#     async def send_start_transaction(self,data,dataID):
#         request = call.StartTransactionPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")

# ## .....................................................................................................
    
#     async def send_status_notification(self,data,dataID):
#         request = call.StatusNotificationPayload(
#             connector_id=data.get("connectorId"), error_code=data.get("errorCode"), status=data.get("status")
#         )
          
#         response = await self.call(request, dataID)
#         # if response.status == RegistrationStatus.accepted:
#         print("Status Notification send.")

                    
# ## .....................................................................................................
    
#     async def send_trigger_message(self,data,dataID):
#         request = call.TriggerMessagePayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")

# ## .....................................................................................................
    
#     async def send_unlock_connector(self,data,dataID):
#         request = call.UnlockConnectorPayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")

# ## .....................................................................................................
    
#     async def send_update_firmware(self,data,dataID):
#         request = call.UpdateFirmwarePayload(
#             charge_point_model=data.get("chargePointModel"), charge_point_vendor=data.get("chargePointVendor")
#         )
          
#         response = await self.call(request, dataID)
#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")

        
# ## .....................................................................................................
# ## .....................................................................................................
# ## .....................................................................................................
        
#     sendFunc = {"authorize" : send_authorize,
#                 "bootnotification" : send_bootnotification,
#                 "heartbeat" : send_heartbeat,
#                 "diagnosticsstatusnotification" : send_diagnostics_status_notification,
#                 "statusnotification" : send_status_notification,
#                 "metervalues" : send_meter_values,
#                 "firmwarestatusnotification" : send_firmware_status_notification,
#                 "datatransfer" : send_data_transfer,
#                 }
        


# ## .....................................................................................................
# ## .....................................................................................................
# ## .....................................................................................................







# ## .....................................................................................................
# ## .....................................................................................................
# ## .....................................................................................................

# async def main_authorize(data, dataID, action):
#     receive_data=""
#     async with websockets.connect(
#         "ws://13.234.76.186:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
#     ) as ws:

#         cp = ChargePoint("1234", ws)
        
#         val = await asyncio.gather(cp.start(action), cp.send_authorize(data, dataID))
#         receive_data = val[0]
#     return receive_data


# ## .....................................................................................................
# ## .....................................................................................................


# async def main_bootnotification(data, dataID, action):
#     receive_data=""
#     async with websockets.connect(
#         "ws://13.234.76.186:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
#     ) as ws:

#         cp = ChargePoint("1234", ws)
        
#         val = await asyncio.gather(cp.start(action), cp.send_bootnotification(data, dataID))
#         receive_data = val[0]
#     return receive_data


# ## .....................................................................................................
# ## .....................................................................................................


# async def main_heartbeat(dataID, action):
#     receive_data=""
#     async with websockets.connect(
#         "ws://13.234.76.186:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
#     ) as ws:

#         cp = ChargePoint("1234", ws)
        
#         val = await asyncio.gather(cp.start(action), cp.send_heartbeat(dataID))
#         receive_data = val[0]
#     return receive_data


# # ## .....................................................................................................
# # ## .....................................................................................................

# # async def main_diagnostics(data):
# #     receive_data=""
# #     async with websockets.connect(
# #         "ws://43.205.177.121:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
# #     ) as ws:

# #         cp = ChargePoint("1234", ws)
        
# #         val = await asyncio.gather(cp.start_diagnostics(), cp.send_diagnostics_status_notification(data))
# #         receive_data = val[0]
# #     return receive_data


# # ## .....................................................................................................
# # ## .....................................................................................................

# async def main_diagnosticsstatusnotification(data, dataID, action):
#     receive_data=""
#     async with websockets.connect(
#         "ws://13.234.76.186:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
#     ) as ws:

#         cp = ChargePoint("1234", ws)
        
#         val = await asyncio.gather(cp.start(action), cp.send_diagnostics_status_notification(data,dataID))
#         receive_data = val[0]
#     return receive_data


# # ## .....................................................................................................
# # ## .....................................................................................................

# async def main_statusnotification(data, dataID, action):
#     receive_data=""
#     async with websockets.connect(
#         "ws://13.234.76.186:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
#     ) as ws:

#         cp = ChargePoint("1234", ws)
        
        
#         val = await asyncio.gather(cp.start(action), cp.send_status_notification(data,dataID))
#         receive_data = val[0]
#     return receive_data


# # ## .....................................................................................................
# # ## .....................................................................................................

# async def main_metervalues(data, dataID, action):
#     receive_data=""
#     async with websockets.connect(
#         "ws://13.234.76.186:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
#     ) as ws:

#         cp = ChargePoint("1234", ws)
        
#         val = await asyncio.gather(cp.start(action), cp.send_meter_values(data, dataID))
#         receive_data = val[0]
#     return receive_data


# # ## .....................................................................................................
# # ## .....................................................................................................


# async def main_firmwarestatusnotification(data, dataID, action):
#     receive_data=""
#     async with websockets.connect(
#         "ws://13.234.76.186:8080/steve/websocket/CentralSystemService/1234", subprotocols=["ocpp1.6"]
#     ) as ws:

#         cp = ChargePoint("1234", ws)
        
#         val = await asyncio.gather(cp.start(action), cp.send_firmware_status_notification(data, dataID))
#         receive_data = val[0]
#     return receive_data


# # ## .....................................................................................................
# # ## .....................................................................................................


# async def main_datatransfer(data,dataID, action):
#     receive_data=""
#     async with websockets.connect(
#         "ws://13.234.76.186:8080/steve/websocket/CentralSystemService/"+dataID, subprotocols=["ocpp1.6"]
#     ) as ws:

#         cp = ChargePoint("1234", ws)
        
#         val = await asyncio.gather(cp.start(action), cp.send_data_transfer(data, dataID))
#         receive_data = val[0]
#     return receive_data



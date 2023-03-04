import socket
import time
import threading


DISCONNECT_MSG = "!DISCONNECT"


def run_client(imei):
    lock = threading.Lock()
    # Create a TCP socket and connect to the server
    print("---------------------")
    # lock.acquire()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('13.234.76.186', 12345))
    connected = True
    count = 0
    # imei = "8643940408337"
    try:
        print('++++++++++++++++++++')
        while connected:
            # print('111')
            # lock.acquire()
            # Send a message to the server
            time.sleep(2)
            heartBeat_message = f'[2, "{imei}", "HeartBeat",{{}}]'
            boot_message = f'[2,"{imei}" , "BootNotification", {{"chargePointVendor": "123", "chargePointModel": "Euler", "chargePointSerialNumber": "", "chargeBoxSerialNumber": "", "firmwareVersion": "", "iccid": "", "imsi": "", "meterSerialNumber": "", "meterType": ""}}]'
            authorize_message = f'[2, "{imei}","Authorize", {{"idTag": "2001"}}]'
            dataTransfer_message = f'[2, "{imei}","DataTransfer",{{"vendorId": "Acme","messageId": "LogData","data": "Rmlyc3ROYW1lOjogRG9l"}}]'
            statusNotification_message = f'[2, "{imei}","StatusNotification",{{"connectorId": 98,"errorCode": "ConnectorLockFailure","status": "Available"}}]'
            diagnosticsstatusnotification_message = f'[2, "{imei}","DiagnosticsStatusNotification",{{"status": "Uploaded","uploadStatus": {{"startTime": "2022-02-22T10:00:00Z","stopTime": "2022-02-22T10:30:00Z","location": "ftp://example.com/diagnostics","retries": 3,"retryInterval": 600}}}}]'
            firmwarestatusnotification_message = f'[2, "{imei}","FirmwareStatusNotification",{{"status": "Downloaded","firmware":{{"location": "ftp://example.com/firmware","retrieveDate": "2022-02-22T10:00:00Z","installDate": "2022-02-23T10:00:00Z","signed": true,"signature": "MII...AB","signatureType": "X.509"}}}}]'
            metervalues_message = f'[2, "{imei}","MeterValues",{{"connectorId": 1001,"transactionId": 1234,"meterValue":[{{"timestamp": "2022-02-22T10:00:00Z","sampledValue":[{{"value": "0.01","context": "Interruption.Begin","unit": "Wh"}},{{"value": "2.5","context": "Sample.Periodic","unit": "A"}}]}},{{"timestamp": "2022-02-22T10:01:00Z","sampledValue":[{{"value": "0.02","context": "Interruption.End","unit": "Wh"}},{{"value": "3.0","context": "Sample.Periodic","unit": "A"}}]}}]}}]'
            starttransaction_message = f'[2,"{imei}","StartTransaction",{{"connectorId":1,"idTag":"516962","meterStart":2650,"reservationId":0,"timestamp":"2018-01-03T17:59:37Z"}}]'
            stoptransaction_message = f'[2,"{imei}","StopTransaction",{{"idTag":"3F420F","meterStop":5060,"timestamp":"2018-02-09T13:21:30Z","transactionId":554381508}}]'
        
            msg = [boot_message, heartBeat_message, authorize_message, dataTransfer_message, statusNotification_message, diagnosticsstatusnotification_message, firmwarestatusnotification_message, metervalues_message, starttransaction_message, stoptransaction_message]
            # msg = [boot_message, heartBeat_message, authorize_message, dataTransfer_message, statusNotification_message, diagnosticsstatusnotification_message, firmwarestatusnotification_message]
            # msg = [heartBeat_message]
            
            client_socket.send(msg[count].encode())
            time.sleep(2)
            if msg[count] == DISCONNECT_MSG:
                connected = False
                break
            else:
                count = count+1
                # Receive a response from the server
                response = client_socket.recv(1024)
                print(f"Received response from server: {response.decode()}")
                if count==11:
                    break
    except Exception as e:
        print('exception is:')
        print(e)
        print("All test messages passed OR Error: Steve might be down :(")
    # lock.release()            
    # Close the client socket
    client_socket.close()

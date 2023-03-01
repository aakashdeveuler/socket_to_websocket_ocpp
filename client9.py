import socket
import time

DISCONNECT_MSG = "!DISCONNECT"

def run_client():
    # Create a TCP socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('10.10.11.202', 12345))
    connected = True
    count = 0
    try:
        while connected:
            # Send a message to the server
            # time.sleep(2)
            boot_message = '[2, "864394040833709", "BootNotification", {"chargePointVendor": "123", "chargePointModel": "Euler", "chargePointSerialNumber": "", "chargeBoxSerialNumber": "", "firmwareVersion": "", "iccid": "", "imsi": "", "meterSerialNumber": "", "meterType": ""}]'
            heartBeat_message = '[2,"864394040833709","HeartBeat",{}]'
            authorize_message = '[2,"864394040833709","Authorize", {"idTag": "2001"}]'
            dataTransfer_message = '[2,"864394040833709","DataTransfer",{"vendorId": "Acme","messageId": "LogData","data": "Rmlyc3ROYW1lOjogRG9l"}]'
            statusNotification_message = '[2,"864394040833709","StatusNotification",{"connectorId": 98,"errorCode": "ConnectorLockFailure","status": "Available"}]'
            diagnosticsstatusnotification_message = '[2,"864394040833709","DiagnosticsStatusNotification",{"status": "Uploaded","uploadStatus": {"startTime": "2022-02-22T10:00:00Z","stopTime": "2022-02-22T10:30:00Z","location": "ftp://example.com/diagnostics","retries": 3,"retryInterval": 600}}]'
            firmwarestatusnotification_message = '[2,"864394040833709","FirmwareStatusNotification",{"status": "Downloaded","firmware":{"location": "ftp://example.com/firmware","retrieveDate": "2022-02-22T10:00:00Z","installDate": "2022-02-23T10:00:00Z","signed": true,"signature": "MII...AB","signatureType": "X.509"}}]'
            metervalues_message = '[2,"864394040833709","MeterValues",{"connectorId": 1001,"transactionId": 1234,"meterValue":[{"timestamp": "2022-02-22T10:00:00Z","sampledValue":[{"value": "0.01","context": "Interruption.Begin","unit": "Wh"},{"value": "2.5","context": "Sample.Periodic","unit": "A"}]},{"timestamp": "2022-02-22T10:01:00Z","sampledValue":[{"value": "0.02","context": "Interruption.End","unit": "Wh"},{"value": "3.0","context": "Sample.Periodic","unit": "A"}]}]}]'
           
            msg = [boot_message, heartBeat_message, authorize_message, dataTransfer_message, statusNotification_message, diagnosticsstatusnotification_message, firmwarestatusnotification_message, metervalues_message]
            
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
                if count==9:
                    break
    except:
        print("All test messages passed OR Error: Steve might be down :(")
                
    # Close the client socket
    client_socket.close()

if __name__ == "__main__":
    run_client()

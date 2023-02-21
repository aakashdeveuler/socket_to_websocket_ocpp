import socket
import time

DISCONNECT_MSG = "!DISCONNECT"

def run_client():
    # Create a TCP socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    connected = True
    count = 0
    while connected:
        # Send a message to the server
        time.sleep(2)
        message = '[2, "97495a9r-867k-4d28-769d-10f795ff4545", "BootNotification", {"chargePointVendor": "123", "chargePointModel": "Euler", "chargePointSerialNumber": "", "chargeBoxSerialNumber": "", "firmwareVersion": "", "iccid": "", "imsi": "", "meterSerialNumber": "", "meterType": ""}]'
        client_socket.send(message.encode())
        if message == DISCONNECT_MSG:
            connected = False
        else:
            count = count+1
            # Receive a response from the server
            response = client_socket.recv(1024)
            print(f"Received response from server: {response.decode()}")
            if count==5:
                break
    # Close the client socket
    client_socket.close()

if __name__ == "__main__":
    run_client()

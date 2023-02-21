import socket

DISCONNECT_MSG = "!DISCONNECT"

def run_client():
    # Create a TCP socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    connected = True
    while connected:
        # Send a message to the server
        message = input("Enter a message to send to the server: ")
        client_socket.send(message.encode())
        if message == DISCONNECT_MSG:
            connected = False
        else:
            # Receive a response from the server
            response = client_socket.recv(1024)
            print(f"Received response from server: {response.decode()}")
    # Close the client socket
    client_socket.close()

if __name__ == "__main__":
    run_client()

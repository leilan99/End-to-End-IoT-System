# CECS 327 - Interprocess Communication (Server)

import socket
import ipaddress
import errno

def set_port():
    # Bind socket to the IP address and server port
    while True:
        try:
            port = int(input("\nEnter port number: "))

            if port < 0 or port>65535:
                raise ValueError
            else:
                return port

        except ValueError:
            print("Port number not valid. Try again.") # Ensures user input matches declared format
        
def create_socket():
    # Create TCP socket
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def listen_tcp(ip, port):
    TCPSocket = create_socket()
    TCPSocket.bind((ip, port))
    # Listen for incoming connections
    TCPSocket.listen(5)
    print(f"Server: {ip}:{port} - Listening...")
    return TCPSocket

def connect_data() -> []:
    import MongoDBConnection as mongo
    return mongo.QueryDatabase();

def main():
    # Print a message indicating the server is starting
    print("Starting server...")
    print()

    ip = '0.0.0.0'  # Setting IP address to listen on all available interfaces

    port = set_port()
    TCPSocket = listen_tcp(ip, port)

    # Accept an incoming connection
    incomingSocket, incomingAddress = TCPSocket.accept()

    # Loop to receive and respond to messages from the client
    while True:
        # Receive a message from the client (up to 1024 bytes)
        clientMessage = incomingSocket.recv(1024)

        # If no message is received, break the loop (client has disconnected)
        if not clientMessage:
            break

        # Display the client's message
        print(f"Client message: {clientMessage.decode('utf-8')}")

        # Receive server data
        serverData = connect_data()
        
        # Send the message back to the client, converted to uppercase
        incomingSocket.sendall(str(serverData).encode())

    # Close the connection to the client
    incomingSocket.close()

if __name__ == "__main__":
    main()

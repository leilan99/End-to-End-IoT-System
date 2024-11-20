# CECS 327 - Interprocess Communication (Server)

import socket
import ipaddress

# Print a message indicating the server is starting
print("Starting server...")
print()

ip = '0.0.0.0'  # Setting IP address to listen on all available interfaces

# Create TCP socket
TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to the IP address and server port
while True:
    try:
        port = int(input("\nEnter port number: "))

        if port < 0 or port>65535:
            raise ValueError
        else:
            break

    except ValueError:
        print("Port number not valid. Try again.") # Ensures user input matches declared format

TCPSocket.bind((ip, port))


# Listen for incoming connections
TCPSocket.listen(5)
print(f"Server: {ip}:{port} - Listening...")

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
    
    # Send the message back to the client, converted to uppercase
    incomingSocket.send(clientMessage.upper())

# Close the connection to the client
incomingSocket.close()

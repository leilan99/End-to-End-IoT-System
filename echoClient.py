# CECS 327 - Interprocess Communication (Client)
# Leila Nunez, 028574375

import socket
import ipaddress

sendMessage = True # This will be the condition for the infinite loop

print("Starting client...")
print()

# Prompt user for the IP address.
while True:
    serverIP = input("Enter IP address: ")
    # Verify IP address
    try:
        ipaddress.ip_address(serverIP)
        print(f"\nThe server IP address is set to: {serverIP}") 
        break
    except ValueError:
        print(f"\n'{serverIP}' is not a valid IP address. Try again.") # If IP address is incorrect, prompt user again


# Prompt user for the port number. The port number must be the same as server.
while True:
    try:
        serverPort = int(input("\nEnter port number: "))

        if serverPort < 0 or serverPort>65535:
            raise ValueError

        else:
            try:
                # Create a TCP socket
                myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                # Attempt to connect to the server
                myTCPSocket.connect((serverIP, serverPort))
                print(f"Connected to the server at {serverIP} on port {serverPort}.")

                break  # Exit loop if connection is successful

            except ConnectionRefusedError:
                print(f"Error: Could not connect to the server at {serverIP} on port {serverPort}. Please try again.")

    except ValueError:
        print("Port number not valid. Try again.") # Ensures user input matches declared format


# Loop to send messages to the server
while sendMessage:
    # Prompt the user to enter a message
    message = input("\nEnter message: ")
    
    # Send the message to the server, encoded as UTF-8
    myTCPSocket.send(message.encode("utf-8"))

    # Receive the server's response (up to 1024 bytes)
    response = myTCPSocket.recv(1024)
    print(f"Received from server: {response.decode('utf-8')}")

    # Ask the user if they want to send another message
    addMessage = input("Send another message? (y/n): ")
    if addMessage.lower() == 'y':  # Accept both 'y' and 'Y'
        sendMessage = True
    elif addMessage.lower() == 'n':  # Accept both 'n' and 'N'
        sendMessage = False
    else:
        print("Please respond with 'y' or 'n'.") # Handles invalid input

myTCPSocket.close()
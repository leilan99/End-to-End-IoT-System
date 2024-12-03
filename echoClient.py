# CECS 327 - Interprocess Communication (Client)

import socket
import ipaddress

# List of accepted queries
VALID_QUERIES = [
    "What is the average moisture inside my kitchen fridge in the past three hours?",
    "What is the average water consumption per cycle in my smart dishwasher?",
    "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?"
]

sendMessage = True

print("Starting client...\n")

# Prompt user for the IP address.
while True:
    serverIP = input("Enter IP address: ")
    # Verify IP address
    try:
        ipaddress.ip_address(serverIP)
        print(f"\nThe server IP address is set to: {serverIP}")
        break
    except ValueError:
        print(f"\n'{serverIP}' is not a valid IP address. Try again.")  # If IP address is incorrect, prompt user again

# Prompt user for the port number. The port number must be the same as server.
while True:
    try:
        serverPort = int(input("\nEnter port number: "))

        if serverPort < 0 or serverPort > 65535:
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
        print("Port number not valid. Try again.")  # Ensures user input matches declared format

# Loop to send messages to the server
while sendMessage:
    # Prompt the user to choose a query
    print("\nAvailable queries:")
    for idx, query in enumerate(VALID_QUERIES, start=1):
        print(f"{idx}. {query}")

    choice = input("\nEnter the number corresponding to your query (1, 2, or 3): ")

    # Validate the input
    if choice.isdigit() and 1 <= int(choice) <= 3:
        query = VALID_QUERIES[int(choice) - 1] # Subtracting because of index
        # Send the query to the server
        myTCPSocket.send(query.encode("utf-8"))

        # Receive the server's response (up to 1024 bytes)
        response = myTCPSocket.recv(1024)
        print(f"Received from server: {response.decode('utf-8')}")
    else:
        print(f"Invalid choice. Please select 1, 2, or 3.")

    # Ask the user if they want to send another message
    addMessage = input("Send another query? (y/n): ")
    if addMessage.lower() == 'y':  # Accept both 'y' and 'Y'
        sendMessage = True
    elif addMessage.lower() == 'n':  # Accept both 'n' and 'N'
        sendMessage = False
    else:
        print("Please respond with 'y' or 'n'.")  # Handles invalid input

myTCPSocket.close()
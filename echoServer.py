import socket
from Mongo import query_database  # Import the updated query_database function

def set_port():
    # Bind socket to the IP address and server port
    while True:
        try:
            port = int(input("\nEnter port number: "))
            if port < 0 or port > 65535:
                raise ValueError
            return port
        except ValueError:
            print("Port number not valid. Try again.")

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

def process_query(query):
    """Process the client's query and fetch the relevant data."""
    try:
        if query == "What is the average moisture inside my kitchen fridge in the past three hours?":
            documents = query_database("Table1_virtual", topic="home_to_kitchen", field="Moisture Meter - MoistureMeter2", hours=3)
            if documents:
                average_moisture = sum(map(float, documents)) / len(documents)
                return f"The average moisture inside your kitchen fridge in the past three hours is {average_moisture:.2f}%."
            else:
                return "No moisture data available for the past three hours."

        elif query == "What is the average water consumption per cycle in my smart dishwasher?":
            documents = query_database("Table1_virtual", topic="home_to_kitchen", field="Water Consumption", hours=3)
            if documents:
                average_water_consumption = sum(map(float, documents)) / len(documents)
                return f"The average water consumption per cycle in your smart dishwasher is {average_water_consumption:.2f} liters."
            else:
                return "No water consumption data available."

        elif query == "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?":
            devices = {
                "Fridge 1": "FridgeBoard",
                "Fridge 2": "FridgeBoard2",
                "Dishwasher": "DishwasherBoard"
            }
            consumption = {}
            for device_name, board in devices.items():
                documents = query_database("Table1_virtual", topic="home_to_kitchen", field="Ammeter", hours=3)
                consumption[device_name] = sum(map(float, documents)) if documents else 0
            max_device = max(consumption, key=consumption.get)
            return f"The device that consumed the most electricity is {max_device} with {consumption[max_device]:.2f} kWh."

        else:
            return "Invalid query."

    except Exception as e:
        return f"Error: Unable to process query. Details: {e}"

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
        clientMessage = incomingSocket.recv(1024)

        # If no message is received, break the loop (client has disconnected)
        if not clientMessage:
            break

        query = clientMessage.decode('utf-8')
        print(f"Client message: {query}")

        # Process the query and get the response
        response = process_query(query)

        # Send the response back to the client
        incomingSocket.sendall(response.encode())

    # Close the connection to the client
    incomingSocket.close()

if __name__ == "__main__":
    main()
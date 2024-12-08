import socket
from Mongo import query_database_with_metadata, SENSOR_TABLE
from datetime import datetime, timedelta, timezone


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

def convert_to_rh(moisture_value):
    return moisture_value * 2.5


def get_time_range(hours):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)
    return start_time, end_time

def convert_to_gallons(liters):
    return liters * 0.264172

def listen_tcp(ip, port):
    TCPSocket = create_socket()
    TCPSocket.bind((ip, port))
    # Listen for incoming connections
    TCPSocket.listen(5)
    print(f"Server: {ip}:{port} - Listening...")
    return TCPSocket

def process_query(query):
    try:
        if query == "What is the average moisture inside my kitchen fridge in the past three hours?":
            # Fetch data for both fridges
            start_time, end_time = get_time_range(3)
            documents1 = query_database_with_metadata(
                SENSOR_TABLE,
                field="Moisture Meter - MoistureMeter",
                asset_id="awm-54c-6o6-0w7",
                start_time=start_time,
                end_time=end_time
            )
            documents2 = query_database_with_metadata(
                SENSOR_TABLE,
                field="Moisture Meter - MoistureMeter2",
                asset_id="6a8f12e8-a2d2-42c8-a21a-8b9bea3b7277",
                start_time=start_time,
                end_time=end_time
            )
            documents = documents1 + documents2
            if documents:
                average_moisture = sum(map(float, documents)) / len(documents)
                average_moisture_rh = convert_to_rh(average_moisture)
                return f"The average moisture inside your kitchen fridge in the past three hours is {average_moisture_rh:.2f}% RH."
            else:
                return "No moisture data available for the past three hours."

        elif query == "What is the average water consumption per cycle in my smart dishwasher?":
            # Fetch data for the dishwasher
            start_time, end_time = get_time_range(3)
            documents = query_database_with_metadata(
                SENSOR_TABLE, 
                field="Water Consumption", 
                asset_id="9f210964-f560-495c-a97e-2d4ef80f145f",  # Device ID for Dishwasher
                start_time=start_time,
                end_time=end_time
            )
            if documents:
                average_water_consumption = sum(map(float, documents)) / len(documents)
                average_water_gallons = convert_to_gallons(average_water_consumption)
                return f"The average water consumption per cycle in your smart dishwasher is {average_water_gallons:.2f} gallons."
            else:
                return "No water consumption data available."

        elif query == "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?":
            # Fetch data for all devices
            devices = {
                "Smart Fridge1": ("Ammeter", "awm-54c-6o6-0w7"),
                "SmartFridge2": ("Ammeter3", "6a8f12e8-a2d2-42c8-a21a-8b9bea3b7277"),
                "Smart Dishwasher": ("Ammeter2", "9f210964-f560-495c-a97e-2d4ef80f145f")
            }
            consumption = {}
            start_time, end_time = get_time_range(24)  # Calculate time range for the last 24 hours
            for device_name, (field, asset_id) in devices.items():
                documents = query_database_with_metadata(
                    SENSOR_TABLE, 
                    field=field, 
                    asset_id=asset_id, 
                    start_time=start_time, 
                    end_time=end_time
                )
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
import socket

MAX_PACKET_SIZE = 1024
DEFAULT_PORT = 12345  # Change this to your expected port
SERVER_IP = '192.168.1.1'  # Change this to your server IP

def get_tcp_port():
    """Prompt the user for a TCP port, with a fallback to the default port."""
    try:
        tcp_port = int(input("Please enter the TCP port of the host: "))
    except ValueError:
        print("Invalid input. Using the default port.")
        tcp_port = DEFAULT_PORT
    return tcp_port

def main():
    # Get the TCP port from the user
    tcp_port = get_tcp_port()
    
    # Establish a connection using a context manager
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        try:
            tcp_socket.connect((SERVER_IP, tcp_port))
            print(f"Connected to server at {SERVER_IP}:{tcp_port}")
        except socket.error as e:
            print(f"Failed to connect to the server: {e}")
            return
        
        # Communication loop
        while True:
            client_message = input("Type your message (or 'exit' to quit):\n> ")
            if client_message.lower() == "exit":
                print("Exiting the chat. Goodbye!")
                break
            
            try:
                # Send the message to the server
                tcp_socket.sendall(client_message.encode())
                
                # Receive the server's reply
                reply = tcp_socket.recv(MAX_PACKET_SIZE).decode()
                print(f"Server reply: {reply}")
            
            except socket.error as e:
                print(f"An error occurred during communication: {e}")
                break

if __name__ == "__main__":
    main()

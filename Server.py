import socket
import threading
import time
import contextlib
import errno
from dataclasses import dataclass
import sys


MAX_PACKET_SIZE = 1024
DEFAULT_PORT = 12345  # Set default port

@dataclass
class ServerConfig:
    host: str = "localhost"
    port: int = DEFAULT_PORT

def get_free_port(min_port: int = 1024, max_port: int = 65535) -> int:
    """Find an available port within a specified range."""
    for port in range(min_port, max_port):
        print(f"Testing port {port}")
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(("localhost", port))
                print(f"Port {port} is available.")
                return port
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    print(f"Port {port} is in use. Checking next...")
                else:
                    print(f"An error occurred while checking port {port}: {e}")
    raise RuntimeError("No available ports found in the specified range.")

def get_server_data() -> list:
    """Simulate querying data from a database."""
    import MongoDBConnection as mongo
    return mongo.QueryDatabase()

def handle_tcp_connection(tcp_socket: socket.socket, client_address: tuple):
    """Handle a single TCP connection."""
    print(f"New TCP connection from {client_address}")
    try:
        while True:
            data = tcp_socket.recv(MAX_PACKET_SIZE)
            if not data:
                print(f"Connection closed by {client_address}")
                break
            
            print(f"Received data: {data.decode()}")
            server_data = get_server_data()
            tcp_socket.sendall(str(server_data).encode())
    except Exception as e:
        print(f"Error handling connection from {client_address}: {e}")
    finally:
        tcp_socket.close()
        print(f"Closed connection with {client_address}")

def create_tcp_socket(config: ServerConfig) -> socket.socket:
    """Create and bind a TCP socket."""
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((config.host, config.port))
    print(f"Server listening on {config.host}:{config.port}")
    return tcp_socket

def start_tcp_server(config: ServerConfig):
    """Start a TCP server to handle multiple connections."""
    tcp_socket = create_tcp_socket(config)
    tcp_socket.listen(5)
    print("Waiting for connections...")
    try:
        while True:
            conn, addr = tcp_socket.accept()
            threading.Thread(target=handle_tcp_connection, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        tcp_socket.close()

if __name__ == "__main__":
    config = ServerConfig(port=DEFAULT_PORT)

    # Launch server in a thread
    server_thread = threading.Thread(target=start_tcp_server, args=(config,))
    server_thread.daemon = True
    server_thread.start()

    print("Server started. Press Ctrl+C to stop.")
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting program...")

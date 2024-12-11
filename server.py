import socket
import threading

clients = {}

def handle_client(client_socket, addr):
    """Handle receiving messages from the client."""
    clients[addr] = client_socket  # Store the client in the dictionary
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  # Client disconnected
            if message == "/quit":
                print(f"Client {addr} disconnected.")
                break
            print(f"Client {addr}: {message}")
            # Broadcast message to all other clients
            broadcast(message, addr)
        except (ConnectionResetError, OSError):
            print(f"Client {addr} disconnected abruptly.")
            break
    client_socket.close()
    del clients[addr]  # Remove client from the dictionary
    print(f"Connection with client {addr} closed.")

def broadcast(message, sender_addr):
    """Broadcast a message to all clients except the sender."""
    for addr, client_socket in clients.items():
        if addr != sender_addr:
            try:
                client_socket.send(f"Client {sender_addr}: {message}".encode('utf-8'))
            except (BrokenPipeError, OSError):
                print(f"Error sending message to client {addr}.")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)  # Listen for multiple clients
    print("Server is listening for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Client {addr} connected.")
        # Start a thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True)
        client_thread.start()

if __name__ == "__main__":
    start_server()

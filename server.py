#!/usr/bin/env python3

import socket
import threading

clients = {}  # Dictionary to store clients' socket and nickname

def handle_client(client_socket, addr):
    """Handle receiving messages from the client."""
    # Ask for the client's nickname
    client_socket.send("Enter your nickname: ".encode('utf-8'))
    nickname = client_socket.recv(1024).decode('utf-8').strip()
    if not nickname:  # Set a default nickname if none is provided
        nickname = f"Client_{addr[1]}"
    
    clients[addr] = {'socket': client_socket, 'nickname': nickname}  # Store the client and nickname
    print(f"{nickname} ({addr}) connected.")
    
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  # Client disconnected
            if message == "/quit":
                print(f"{nickname} ({addr}) disconnected.")
                break
            print(f"{nickname}: {message}")
            # Broadcast message to all other clients
            broadcast(message, addr, nickname)
    except (ConnectionResetError, OSError):
        print(f"{nickname} ({addr}) disconnected abruptly.")
    
    client_socket.close()
    del clients[addr]  # Remove client from the dictionary
    print(f"Connection with {nickname} ({addr}) closed.")

def broadcast(message, sender_addr, sender_nickname):
    """Broadcast a message to all clients except the sender."""
    for addr, client_info in clients.items():
        if addr != sender_addr:
            try:
                client_info['socket'].send(f"{sender_nickname}: {message}".encode('utf-8'))
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

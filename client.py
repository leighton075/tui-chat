#!/usr/bin/env python3

import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  # Server disconnected
            if message == "/quit":
                print("Server disconnected.")
                break
            print(f"{message}")  # Directly print the message without 'You:'
        except (ConnectionResetError, OSError):
            print("Connection closed by server.")
            break
    client_socket.close()
    print("Connection with server closed.")

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("Enter server IP (e.g., 209.38.83.80): ")
    server_port = 12345

    try:
        client_socket.connect((server_ip, server_port))
        print("Connected to the server!")
    except:
        print("Unable to connect to the server.")
        return

    # Ask for the nickname
    nickname = input("Enter your nickname: ")
    client_socket.send(nickname.encode('utf-8'))  # Send the nickname to the server

    # Start a thread to handle incoming messages
    client_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    client_thread.start()

    try:
        while client_thread.is_alive():
            message = input()  # User's input
            if message == "/quit":
                print("Closing connection...")
                client_socket.send(message.encode('utf-8'))
                break
            if message.strip():  # Ensure the message is not empty before sending
                client_socket.send(message.encode('utf-8'))
    finally:
        client_socket.close()
        print("Client shut down.")

if __name__ == "__main__":
    start_client()

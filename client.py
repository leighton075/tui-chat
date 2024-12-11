#!/usr/bin/env python3

import socket as sock
import threading
import sys

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  # If the server doesn't receive the message then it must have disconnected
            if message == "/quit":
                print("Server disconnected.")
                break
            print(f"{message}")
        except (ConnectionResetError, OSError):
            print("Connection closed by server.")
            break
    client_socket.close()
    print("Connection with server closed.")

def start_client():
    client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    server_ip = input("Enter server IP (e.g., 209.38.83.80): ")
    server_port = 12345

    try:
        client_socket.connect((server_ip, server_port))
        print("Connected to the server!")
    except:
        print("Unable to connect to the server.")
        return

    # Ask for the user's nickname
    nickname = input("Enter your nickname: ")
    # Send the nickname to the server
    client_socket.send(nickname.encode('utf-8'))

    # Start a thread to handle incoming messages
    client_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    client_thread.start()

    try:
        while client_thread.is_alive():
            message = input()  # User's input
            if message.strip() == "":  # Skip empty messages
                continue

            if message == "/quit":
                print("Closing connection...")
                client_socket.send(message.encode('utf-8'))
                break

            try:
                # Clear the previous "You: ..." line
                sys.stdout.write("\033[F\033[K")  # Moves cursor up and clears the line
                sys.stdout.flush()
                # Print the message with the nickname
                print(f"{nickname}: {message}")
                client_socket.send(f"{nickname}: {message}".encode('utf-8'))
            except (BrokenPipeError, OSError):
                print("Error: Connection closed by server.")
                break
    finally:
        client_socket.close()
        print("Client shut down.")

if __name__ == "__main__":
    start_client()

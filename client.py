import socket as sock # i dunno why but funny
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
            # Print server message on a new line
            print(f"Server: {message}")
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
            try:
                # Print "You: {message}" and send to server
                print(f"You: {message}")
                client_socket.send(message.encode('utf-8'))
            except (BrokenPipeError, OSError):
                print("Error: Connection closed by server.")
                break
    finally:
        client_socket.close()
        print("Client shut down.")

if __name__ == "__main__":
    start_client()

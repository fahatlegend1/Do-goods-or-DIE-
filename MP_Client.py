import socket


SERVER_IP = "127.0.0.1"
PORT = 4242

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

message = client_socket.recv(1024).decode()
print(f"[Server] ({SERVER_IP}): {message}")

client_socket.sendto("Checking for connection...".encode(), SERVER_IP)

client_socket.close()

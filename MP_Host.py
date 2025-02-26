import socket

Host = "0.0.0.0"
PORT = 4242

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((Host, PORT))
server_socket.listen(1)

print(f"[*] Listening on {Host}:{PORT}")
print("[*] Waiting for connection...")

client_socket, client_address = server_socket.accept()
print(f"[+] Player connected from {client_address[0]}")

client_socket.sendall("Welcome to the game!".encode())

message = client_socket.recv(1024).decode()
print(f"[Client] ({client_address[0]}) : {message}")

client_socket.close()
server_socket.close()

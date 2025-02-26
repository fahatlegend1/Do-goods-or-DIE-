import socket, threading

HOST = "0.0.0.0"
PORT = 4242

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
#server_socket.listen(1)

clients = {}

'''print(f"[*] Listening on {HOST}:{PORT}")
print("[*] Waiting for connection...")

client_socket, client_address = server_socket.accept()
#print(client_address)
print(f"[+] Player connected from {client_address[0]}:{client_address[1]}")

client_socket.sendall("Welcome to the game!".encode())

message = client_socket.recv(1024).decode()
print(f"[Client] ({client_address[0]}) : {message}")'''

def handle_client():
    while True:
        message, client_address = server_socket.recv(1024).decode()
        message = message.decode()

        if message == "Checking for connection..."
            print(f"[Client] ({client_address[0]}): {message}")
            server_socket.sendto("Connection established!".encode(), client_address)

        elif message.startswith("Move:"):
            player_id, x, y = message.split("5:").split(",")
            x, y = int(x), int(y)

            if player_id in clients:
                clients[player_id] = {"x": x, "y": y}
            else:
                clients[player_id]["x"] = x
                clients[player_id]["y"] = y

            print(f"Player {player_id} moved to ({x}, {y})")

        else:
            print("Receive an unknown message:\n", message)

client_socket.close()
server_socket.close()


# Server Thread for listening to client messages
client_handler_thread = threading.Thread(target=handle_client)
client_handler_thread.start()

# IBroadcast Threa for initialiing broadcasting player positions
broadcast_thread = threading.Thread(target=broadcast_positions)
broadcast_thread.start()
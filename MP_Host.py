import socket, threading

# Server Configuration
HOST = "0.0.0.0"
PORT = 4242

Players = {}
Clients = {}
# Pl



def process_message(message, client_address):
    message = message.decode().strip()


    if message.startswith("CONNECT:"):
        try:
            _, player_id = message.split(":")
            Players[player_id] = (0, 0)
            Clients[player_id] = client_address
            print(f"[+] Player {player_id} connected from {client_address[0]}:{client_address[1]}")
            server_socket.sendto("Connection established!".encode(), client_address)
        except Exception as E:
            print("Error processing CONNECT message:", E)

    elif message.startswith("MOVE:"):
        try:
            parts = message.split(",")
            prefix = parts[0]
            _, player_id = prefix.split(":")
            x, y = int(parts[1]), int(parts[2])
            Players[player_id] = (x, y)
            print(f"{player_id} moved to ({x}, {y})")
        except Exception as E:
            print("Error processing MOVE message:", E)
    else:
        print("Received an unknown meesage:\n", message)

def handle_client():
    while True:
        try:
            data, client_address = server_socket.recvfrom(1024)
            threading.Thread(target = process_message, args=(data, client_address)).start() 
        except Exception as E:
            print("Error processing message:\n", E)

def broadcast_positions():
    while True:
        if Players:
            state = str(Players).encode()
            for player_id, addr in Clients.items():
                try:
                    server_socket.sendto(state, addr)
                except Exception as E:
                    print("Error broadcasting positions to", addr, ":", E)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))

print(f"[*] Server initialized on {HOST}:{PORT}")

# Thread 1: Handle incoming messages
client_handler_thread = threading.Thread(target=handle_client)
client_handler_thread.start()

# Thread 2: Broadcast positions to all clients
broadcast_thread = threading.Thread(target=broadcast_positions)
broadcast_thread.start()
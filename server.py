import socket


server_IP = 'localhost'

MAX_RECV: int = 1024


#we are gonna get port (keep as int and use that for the rest), same as client

while True: 
    port_input: str = input("Please enter a port number")
    if port_input == "":
        port: int = 8080 #if its not a valid port, default
        print("Valid port was not entered, defaulted to 8080")
    elif port_input.isdigit() and 1024 <= int(port_input) <= 65535:
        port = int(port_input)  #if the user enters a number not in this range, reset
        break
    else: 
        print("Port is invalid. Try again, with the number between 1024 and 65535")



#gave loop a name to keep it readable, this loop will just keep trying until user enters a name
server_name_empty: bool = True

while server_name_empty:
    requested_username: str = input("Please enter a username")
    requested_username = requested_username.strip()
    if requested_username == "":
        print("Username was not entered, retry now")
    else:
        server_name_empty = False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allows port to be reused immediately if the server restarts
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server_socket.bind((server_IP, port_input))
    server_socket.listen(1)  # 1 = only expecting one client
    print(f"Server listening on {server_IP} | {port_input}")
except OSError as e:
    print("Failed, please retry.")
    server_socket.close()
    exit()

# Send server username to the other side
server_socket.send(requested_username.encode())

# Receive client username
client_username = server_socket.recv(MAX_RECV).decode()

print(f"{client_username} has joined the chat!")
print("Waiting for a client to connect...")
client_socket, client_address = server_socket.accept() #waits for a client to join 
print(f"Client connected from {client_address}") #and prints where they connected from 

while True:
    try:
        message = client_socket.recv(MAX_RECV).decode()
        if message.lower() == "end" or message == "": #if they other side sends end or an empty, break loop
            print("Client has ended the chat.")
            break
        print(f"{client_username}: {message}")

        reply = input(f"{client_username}: ").strip() #reply to client

        client_socket.send(reply.encode())
        if reply.lower() == "end":
            print("Ending chat.")
            break
    except OSError as e:
        print(f"Connection error: {e}")
        break

client_socket.close()
server_socket.close()
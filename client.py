import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("192.168.0.178", 9999)

client_socket.connect(server_address)

def send(client_socket):
    while True:
        data = input("")
            
        if data == "break":
            break

        data = data.encode()
        client_socket.send(data)

def receive(client_socket):
    while True:
        msg = client_socket.recv(1024)
        print(f"[SERVER]: {msg.decode()}")

s = threading.Thread(target=send, args=(client_socket))
r = threading.Thread(target=receive, args=(client_socket))

s.start()
r.start()

client_socket.close()

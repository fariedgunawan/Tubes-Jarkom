import socket
import os

def send_response(client_socket, response):
    client_socket.sendall(response)
    client_socket.close()

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    filename = request.split()[1]
    filename = filename[1:]

    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            response_data = file.read()
            response_header = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
            response = response_header.encode() + response_data
    else:
        if os.path.exists("404.html"):
            with open("404.html", 'rb') as file:
                response_data = file.read()
                response_header = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n"
                response = response_header.encode() + response_data
        else:
            response = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n<html><body><h1>404 Not Found</h1></body></html>".encode()

    send_response(client_socket, response)

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")
        
        handle_client(client_socket)

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 6789

    start_server(HOST, PORT)

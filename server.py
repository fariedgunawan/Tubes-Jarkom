import socket
import threading
import os

# Fungsi untuk mengirim respons HTTP
def send_response(client_socket, response):
    client_socket.sendall(response)
    client_socket.close()

# Ini buat ngurus setiap koneksi lu dari klien
def handle_client(client_socket, client_address):
    # Terus terima request HTTP dari klien
    request = client_socket.recv(1024).decode()

    # Parse request buat mendapatkan nama file yang diminta
    filename = request.split()[1]
    filename = filename[1:]  # Hapus karakter '/' di awal

    # Ngecek file ini ada atau tidak
    if os.path.exists(filename):
        # Buat response HTTP sukses
        with open(filename, 'rb') as file:
            response_data = file.read()
            response_header = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
            response = response_header.encode() + response_data
    else:
        # Buat response HTTP file yang ga ditemukan
        # Baca file 404.html jika ada
        if os.path.exists("404.html"):
            with open("404.html", 'rb') as file:
                response_data = file.read()
                response_header = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n"
                response = response_header.encode() + response_data
        else:
            # Buat respons sederhana jika file 404.html tidak ditemukan
            response = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n<html><body><h1>404 Not Found</h1></body></html>".encode()

    # Kirim response ke klien
    send_response(client_socket, response)

# Buat menjalankan server dan menerima koneksi dari klien
def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

        # Handle setiap koneksi dalam sebuah thread terpisah
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Jalankan server dalam sebuah thread utama
if __name__ == "__main__":
    HOST = '127.0.0.1'  # Ganti dengan alamat IP host Anda
    PORT = 6789  # Ganti dengan port yang Anda inginkan

    start_server(HOST, PORT)

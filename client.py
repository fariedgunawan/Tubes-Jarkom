import socket
import sys

def send_request(server_host, server_port, filename):
    try:
        # Buat koneksi TCP ke server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))

        # Kirim request HTTP
        request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
        client_socket.sendall(request.encode())

        # Terima dan tampilkan respons dari server
        response = client_socket.recv(4096).decode()
        print(response)

        # Tutup koneksi
        client_socket.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py server_host server_port filename")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    send_request(server_host, server_port, filename)

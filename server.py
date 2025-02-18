import socket

def receive_image():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(1)  # Listen for incoming connections
    print(f"Server listening on {host}:{port}")

    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    with open(r'C:\Users\Anas\Desktop\rcv/received_image.jpg', 'wb') as file:
        data = client_socket.recv(4096)
        while data:
            file.write(data)
            data = client_socket.recv(4096)

    print("Image received successfully.")
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    receive_image()

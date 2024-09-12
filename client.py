import socket

def main():
    host = '127.0.0.1'  # адрес вашего сервера (localhost)
    port = 5001  # порт, который использует ваш сервер

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.sendall(b"Hello, Server!")
    data = client_socket.recv(1024)
    message=str(input("введите сообщение: ")).encode("utf-8")

    #print("Received", repr(data))
    print('Получено от сервера:', data.decode('utf-8'))
    client_socket.close()

if __name__ == "__main__":
    main()
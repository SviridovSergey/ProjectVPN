import socket
import requests
from bs4 import BeautifulSoup
import okno

host = '0.0.0.0'
port = 5001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

proxies = {
    'http':"http://104.16.108.45:80"
}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'}

print("Выберите на какой сервер хотите подключится,есть варианты:"
      "США(ip:104.16.83.0,port:80);Франция(ip:212.83.138.245,port:50894")


print("VPN is started")


def handle_client(conn, addr):
    print(f"Подключение.. {addr}")

    german_server_address = ("104.16.108.45", 80)
    german_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        german_conn.connect(german_server_address)
        print("Подключение в Серверу Германии успешно выполнено")
    except Exception as e:
        print("Подключение к Серверу Герамании прервано:", e)
        return  # Завершаем функцию если соединение не удалось

    while True:
        try:
            data = conn.recv(1024)
            if not data: break

            print("Received data from {addr}: {data.decode()}".format(addr=addr, data=data))
            german_conn.sendall(data)  # Отправляем оригинальные данные на сервер
            response = german_conn.recv(1024)

            print("Response received from server: {response.decode('utf-8')}".format(response=response))
            conn.sendall(response)  # Отправляем ответ обратно клиенту
        except ConnectionResetError:
            break
    conn.close()
    german_conn.close()

def get_location(url):
    response = requests.get(url=url,headers=headers,proxies=proxies)
    soup = BeautifulSoup(response.text,'lxml')
    ip=soup.find('div',class_='ip').text.strip()
    print("ip:"+ip)

def main():
    while True:
        conn, addr = server_socket.accept()  # Принять новое соединение
        print(f"Connected by {addr}")
        handle_client(conn, addr)  # Передать объект соединения в функцию
        # Вызов функции из okno.py
        okno.main()


if __name__ == "__main__":
    main()

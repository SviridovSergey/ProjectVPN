import socket
import requests
from bs4 import BeautifulSoup
print("vpn is started")

host='0.0.0.0'
port=5000
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'}
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 80))
server_socket.listen()

proxies = {
    'http':"http://104.16.108.45:80"
}

def handle_client(conn, addr):
    try:
        print(f"connecting.. {addr}")
        #подкл к серверу германи
        german_server_adress=("104.16.108.45",80)
        try:
            german_conn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            german_conn.connect(german_server_adress)
            print("connected to the USA server")
        except  Exception as e:
            print("try to conection is lost")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                print("received data from {addr}: {data.decode()}".format(addr=addr, data=data))
                german_conn: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                response=german_conn.recv(1024).decode('utf-8')
                print("response received from server:{response.decode('utf-8')}".format(response=response))
                conn.sendall(data)
            except ConnectionResetError:
                break
    except Exception as t:
        print("connection is lost ")
    finally:
        print("connection close")
        conn.close()

def start_server():
    with socket.server(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host,port))
        server_socket.listen()
        print("server is started")

        while True:
            conn, addr = server_socket.accept()

def get_location(url):
    response = requests.get(url=url,headers=headers,proxies=proxies)
    soup = BeautifulSoup(response.text,'lxml')
    ip=soup.find('div',class_='ip').text.strip()
    print("ip:"+ip)


def main():
    while True:
        conn, addr = server_socket.accept()  # Принять новое соединение
        print(f"Connected by {addr}")
        handle_client(conn)  # Передать объект соединения в функцию
        get_location(url="https://2ip.ru")

if __name__=="__main__":
    main()
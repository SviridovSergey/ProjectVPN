import socket
import time
import requests
from bs4 import BeautifulSoup
import subprocess
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import threading

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

print("VPN is started")

def start_file_okno():
    subprocess.Popen(["python","okno.py"])
    print("запуск файла okno.py")

def start_file_client():
    subprocess.Popen(["python","client.py"])
    print("запуск файла client.py")

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

            print("Received data from {addr}: {data}".format(addr=addr, data=data.decode()))
            german_conn.sendall(data)  # Отправляем оригинальные данные на сервер
            response = german_conn.recv(1024)

            print("Response received from server: {}".format(response.decode('utf-8')))
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
        subprocess.Popen(["python","vpn.py"])
        #get_location(addr)

if __name__ == "__main__":
    thread_client = threading.Thread(target=start_file_okno())
    thread_vpn = threading.Thread(target=start_file_client())
    thread_client.start()
    time.sleep(0.5)
    thread_vpn.start()
    main()

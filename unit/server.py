import threading
from random import randint
from socket import *

servers = []
index = 0


def start():
    # 소켓 서버 오픈 =====================================
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(1)
    create_thread(server_socket)

    # 종료 트리 밟음
    while input() != "close":
        pass

    for server in servers:
        try:
            server.connection_socket.close()
        except:
            pass
    server_socket.close()


def game_start(index):
    # 게임 시작을 알림
    servers[index].send_data("start")
    servers[index + 1].send_data("start")

    # 시작을 정해서 알려줌
    first = randint(0, 1)
    if first == 0:
        servers[index].send_data("you_are_first")
        servers[index - 1].send_data("you_are_next")
    else:
        servers[index - 1].send_data("you_are_first")
        servers[index].send_data("you_are_next")


def create_thread(server_socket):
    global index
    servers.append(ServerThread(index, server_socket))
    servers[index].daemon = True
    servers[index].start()


class ServerThread(threading.Thread):
    def __init__(self, idx, server_socket):
        super().__init__()
        self.server_socket = server_socket
        self.idx = idx
        self.encounter_idx = idx + 1 if idx % 2 == 0 else idx - 1

    def run(self):
        global index
        self.connection_socket, addr = self.server_socket.accept()
        index = index + 1
        if index % 2 == 0:
            game_start(index - 2)

        # 새로운 연결 대기 스레드 생성
        create_thread(self.server_socket)

        # 받은 데이터는 스레드로 처리
        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.daemon = True
        receive_thread.start()

    def receive_data(self):
        while(True):
            data = self.connection_socket.recv(1024).decode("utf-8")
            servers[self.encounter_idx].send_data(data)

    def send_data(self, data):
        self.connection_socket.send(data.encode("utf-8"))

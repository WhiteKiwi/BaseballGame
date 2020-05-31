from socket import *
from game.play_game import play_game
from unit.socket_connection import receive_data


def start():
    # 연결 시작
    connection_socket = connecting()

    # 시작 기다리기
    is_my_attack_turn = waiting_encounter(connection_socket)

    # 게임 시작
    play_game(connection_socket, is_my_attack_turn)


# 연결 수립
def connecting():
    # 상대방 주소 입력
    addr = input("서버의 IP 주소를 입력하세요: ")

    connection_socket = socket(AF_INET, SOCK_STREAM)
    connection_socket.connect((addr, 8080))
    print('연결 확인 되었습니다.')
    return connection_socket


# 상대방을 기다림, 내가 선인지 반환
def waiting_encounter(connection_socket):
    print("상대방을 기다리는 중입니다...")
    if receive_data(connection_socket) == "start":
        print("상대방이 연결되었습니다.")

    # 누가 시작인지 받아서 처리
    return receive_data(connection_socket) == "you_are_first"

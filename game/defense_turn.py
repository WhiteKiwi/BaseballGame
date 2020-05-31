from unit.socket_connection import send_data, receive_data


# 수비 턴 진행
def defense_turn(connection_socket):
    send_data(connection_socket, input("수비할 숫자 세 개를 입력하세요: "))

    # 상대의 결과를 수신
    return receive_data(connection_socket) == "attack_success"

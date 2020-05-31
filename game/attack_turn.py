from unit.socket_connection import receive_data, send_data


# 공격 턴 진행
def attack_turn(connection_socket):
    defense_numbers = receive_data(connection_socket).split()
    print("받은 데이터:", defense_numbers)

    attack_numbers = input("공격할 숫자 세 개를 입력하세요: ").split()
    for defense_number in defense_numbers:
        if defense_number not in attack_numbers:
            send_data(connection_socket, "attack_failed")
            return False

    send_data(connection_socket, "attack_success")
    return True

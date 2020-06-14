from game.constants import ResultType
from unit.socket_connection import send_data, receive_data
import os


# 게임 진행
def play_game(connection_socket, is_my_attack_turn):
    my_scores = [0 for i in range(12)]
    opponent_scores = [0 for i in range(12)]
    for i in range(24):
        out_count = 0

        while out_count < 3:
            # 스트라이크 카운트
            strike_count = 0
            # 주자 수, 3명부터 공격 성공 시 1점씩 오름
            runner_count = 0
            # 볼 카운트
            ball_count = 0

            while strike_count < 3:
                if is_my_attack_turn:
                    # 내가 공격 턴 일 때
                    turn_result = attack_turn(connection_socket)
                else:
                    # 내가 수비 턴 일 때
                    turn_result = defense_turn(connection_socket)

                # 화면 초기화
                os.system('cls')

                # 안타
                if turn_result == ResultType.HITS:
                    print("Hits!")
                    if runner_count == 3:
                        # 공격 성공한 팀에 점수 + 1
                        if is_my_attack_turn:
                            print("득점 1점!")
                            my_scores[i // 2] += 1
                        else:
                            print("상대팀 득점 1점!")
                            opponent_scores[i // 2] += 1
                    else:
                        runner_count += 1
                    # 스트라이크 초기화
                    strike_count = 0
                # 홈런
                elif turn_result == ResultType.HOME_RUN:
                    print("Home Run..!!")
                    runner_count += 1
                    # 공격 성공한 팀에 점수 + 1
                    if is_my_attack_turn:
                        print(f"득점 {runner_count}점!")
                        my_scores[i // 2] += runner_count
                    else:
                        print(f"상대팀 득점 {runner_count}점!")
                        opponent_scores[i // 2] += runner_count
                    runner_count = 0
                    # 스트라이크 초기화
                    strike_count = 0
                # 파울
                elif turn_result == ResultType.FOUL:
                    print("Foul!")
                    # 파울은 2 스트라이크 이후에 카운트를 올리지 않음
                    if strike_count < 2:
                        strike_count += 1
                elif turn_result == ResultType.BALL:
                    if ball_count == 4:
                        print("4 Ball!")
                        # 스트라이크 초기화
                        strike_count = 0

                        if runner_count == 3:
                            # 공격 성공한 팀에 점수 + 1
                            if is_my_attack_turn:
                                print("득점 1점!")
                                my_scores[i // 2] += 1
                            else:
                                print("상대팀 득점 1점!")
                                opponent_scores[i // 2] += 1
                        else:
                            runner_count += 1
                    else:
                        ball_count += 1
                        print(f"{ball_count} Ball!")
                else:
                    print("Strike!")
                    # 스트라이크 +1
                    strike_count += 1

                print()
                print("내 점수: ", my_scores)
                print("상대 점수: ", opponent_scores)
                print()

            # 3 스트라이크 == 1 out
            print("1 Out!")
            out_count += 1

        # 공수교대
        is_my_attack_turn = not is_my_attack_turn


# 공격 턴
def attack_turn(connection_socket):
    defense_numbers = receive_data(connection_socket).split()
    # print("받은 데이터:", defense_numbers)

    attack_numbers = input("공격할 숫자 세 개를 입력하세요: ").split()

    result = check(attack_numbers, defense_numbers)
    send_data(connection_socket, result)
    return result


# 수비 턴
def defense_turn(connection_socket):
    send_data(connection_socket, input("수비할 숫자 세 개를 입력하세요: "))

    # 상대의 결과를 수신
    return receive_data(connection_socket)


# 한 턴 결과 검사
def check(attack_numbers, defense_numbers):
    # 스트라이크 검사
    count = 0
    for defense_number in defense_numbers:
        if defense_number in attack_numbers:
            count += 1

    if count < 2:
        return ResultType.STRIKE

    # 3개가 맞으면 홈런 검사
    i_count = 0
    for i in range(3):
        if attack_numbers[i] == defense_numbers[i]:
            i_count += 1
    
    if i_count == 3:
        # 3개가 맞으면 홈런
        return ResultType.HOME_RUN
    elif i_count == 2:
        # 홈런과 볼은 한끝차이
        return ResultType.BALL
    elif count == 2:
        # 두 개 맞추면 파울
        return ResultType.FOUL
    else:
        # 셋 중 하나라도 순서가 틀리면 안타
        return ResultType.HITS


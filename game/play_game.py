from game.attack_turn import attack_turn
from game.defense_turn import defense_turn


# 게임 진행
def play_game(connection_socket, is_my_attack_turn):
    my_scores = [0 for i in range(9)]
    opponent_scores = [0 for i in range(9)]
    for i in range(18):
        out_count = 0

        while out_count < 3:
            strike_count = 0
            # 주자 수, 3명부터 공격 성공 시 1점씩 오름
            runner_count = 0

            while strike_count < 3:
                if is_my_attack_turn:
                    # 내가 공격 턴 일 때
                    attack_success = attack_turn(connection_socket)
                else:
                    # 내가 수비 턴 일 때
                    attack_success = defense_turn(connection_socket)

                # 공격 성공
                if attack_success:
                    print("안타!")
                    runner_count += 1
                    if runner_count > 3:
                        # 공격 성공한 팀에 점수 + 1
                        if is_my_attack_turn:
                            print("득점 1점!")
                            my_scores[i // 2] += 1
                        else:
                            print("상대팀 득점 1점!")
                            opponent_scores[i // 2] += 1
                        print("내 점수: ", my_scores)
                        print("상대 점수: ", opponent_scores)
                    # 스트라이크 초기화
                    strike_count = 0
                # 공격 실패
                else:
                    print("Strike!")
                    # 스트라이크 +1
                    strike_count += 1

            # 3 스트라이크 == 1 out
            print("1 Out!")
            out_count += 1

        # 공수교대
        is_my_attack_turn = not is_my_attack_turn

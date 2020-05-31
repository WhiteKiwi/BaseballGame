from unit import server, client

if __name__ == "__main__":
    print("1. 방만들기\n2. 접속하기\n")
    choice = input("입력: ")

    if choice == "1":
        # 서버 실행
        server.start()

    else:
        # 클라이언트 실행
        client.start()




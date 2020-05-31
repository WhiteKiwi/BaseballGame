# 데이터 송신
def send_data(connection_socket, data):
    connection_socket.send(data.encode('utf-8'))


# 데이터 수신
def receive_data(connection_socket):
    return connection_socket.recv(1024).decode('utf-8')

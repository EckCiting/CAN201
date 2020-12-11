from socket import *

import FileUtil
import udp_file_client as udp


def tcp_send_file_name(file_name, hostname):
    serverName = hostname
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send(file_name.encode())
    answer = clientSocket.recv(2048)
    print(answer.decode())

    clientSocket.close()


def tcp_receive_file_name(serverSocket):
    connectionSocket, addr = serverSocket.accept()
    received_file = connectionSocket.recv(2048).decode()
    current_file_list = FileUtil.walk_subfile_list('share')
    print(received_file)
    print(current_file_list)
    if received_file in current_file_list:
        ans = "0"
    else:
        ans = "1"
        udp.udp_request_file(received_file, addr[0])
    connectionSocket.send(ans.encode())
    connectionSocket.close()


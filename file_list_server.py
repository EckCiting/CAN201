from socket import *
import json
import file_client


def file_list_server_f():
    VMA = "192.168.0.19"
    server_port = 13000
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', server_port))
    print('The server is ready to receive')
    while True:
        file_list_json, client_address = server_socket.recvfrom(2048)
        file_list = json.loads(file_list_json.decode())
        # print(file_list)
        file_client.request_file(file_list[0],VMA)

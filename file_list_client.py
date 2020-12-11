from socket import *
import json


def send_file_list(server_ip, file_list):
    server_port = 13000
    client_socket = socket(AF_INET, SOCK_DGRAM)
    file_list_json = json.dumps(file_list)
    client_socket.sendto(file_list_json.encode(), (server_ip, server_port))
    client_socket.close()

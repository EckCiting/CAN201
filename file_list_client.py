from socket import *
import json

from config import file_list_server_port


def send_file_list(server_ip, file_list):
    client_socket = socket(AF_INET, SOCK_DGRAM)
    file_list_json = json.dumps(file_list)
    client_socket.sendto(file_list_json.encode(), (server_ip, file_list_server_port))
    client_socket.close()

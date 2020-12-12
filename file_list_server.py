from socket import *
from FileUtil import *
import json
import file_client
from config import VMA, VMB, path

def file_list_server_f():
    server_port = 13000
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', server_port))
    print('The server is ready to receive')
    while True:
        # now file list is a string
        file_list_json, client_address = server_socket.recvfrom(2048)
        file_list = json.loads(file_list_json.decode())
        current_list = traverse_files(path)

        if file_list not in str(current_list):
            file_client.request_file(file_list, VMA)

        else:
            print("already have this file")

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
        has_file = 0
        for i in current_list:
            if file_list == i:
                has_file = 1
        if has_file == 0:
            # create new folder
            # only supports secondary dir
            file_list_split = file_list.split(os.sep)
            if len(file_list_split) == 3:
                new_path = file_list_split[0]+os.sep+file_list_split[1]
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
            file_client.request_file(file_list, client_address[0])
        else:
            print("already have this file")

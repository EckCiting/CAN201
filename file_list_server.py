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
        diff = []
        for i in file_list:
            if file_list not in current_list:
                diff.append(i)
        if len(diff) != 0:
            client_port = 12001
            client_socket = socket(AF_INET, SOCK_DGRAM)
            client_socket.bind(('', client_port))
            for i in diff:
                # create new folder
                # only supports secondary dir
                file_path_split = i.split(os.sep)
                if len(file_path_split) == 3:
                    new_path = file_path_split[0]+os.sep+file_path_split[1]
                    if not os.path.exists(new_path):
                        os.makedirs(new_path)
                file_client.request_file(client_socket, i, client_address[0])

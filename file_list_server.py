from socket import *
from FileUtil import *
import json
import file_client
from config import VMA, VMB, path, file_list_server_port, file_client_port
from file_list_client import send_file_list
from main import cache_file_list


def file_list_server_f():
    # server_port = 13000
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', file_list_server_port))
    print('The server is ready to receive')

    while True:
        # listening file list from other VMs
        file_list_json, client_address = server_socket.recvfrom(2048)
        file_list = json.loads(file_list_json.decode())
        diff = []
        if file_list:
            print("你是内鬼")
            for i in file_list:
                if i not in cache_file_list:
                    diff.append(i)

        if diff:
            # find difference, request for file
            if diff[0] == "allfiles":
                a = traverse_files(path)
                # a = cache_file_list
                send_file_list(client_address[0], a)

            else:
                for i in diff:
                    # create new folder
                    # only supports secondary dir
                    client_socket = socket(AF_INET, SOCK_DGRAM)
                    client_socket.bind(('', file_client_port))
                    file_path_split = i.split(os.sep)
                    if len(file_path_split) == 3:
                        new_path = file_path_split[0]+os.sep+file_path_split[1]
                        if not os.path.exists(new_path):
                            os.makedirs(new_path)
                    file_client.request_file(client_socket, i, client_address[0])


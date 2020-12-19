from socket import *
from FileUtil import *
import json
import file_client
from config import *
from file_list_client import send_file_list


def file_list_server_f():
    # server_port = 13000
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', file_list_server_port))
    print('The server is ready to receive')

    while True:
        # listening file list from other VMs
        file_list_json, client_address = server_socket.recvfrom(2048)
        file_tuple_list = json.loads(file_list_json.decode())
        diff_file_list = []
        if file_tuple_list:
            current_file_list = []
            for f_tuple in traverse_files(path):
                current_file_list.append(f_tuple[0])

            # a VM request for lists of all files
            if file_tuple_list == ["allfiles"]:
                a = current_file_list
                send_file_list(client_address[0], a)

            for f_tuple in file_tuple_list:
                if f_tuple[0] not in current_file_list:
                    diff_file_list.append(f_tuple[0])

            if diff_file_list:
                for i in diff_file_list:
                    # create new folder
                    # only supports secondary dir
                    client_socket = socket(AF_INET, SOCK_DGRAM)
                    client_socket.bind(('', file_client_port))
                    file_path_split = i.split(os.sep)
                    if len(file_path_split) == 3:
                        new_path = file_path_split[0] + os.sep + file_path_split[1]
                        if not os.path.exists(new_path):
                            os.makedirs(new_path)
                    file_client.request_file(client_socket, i, client_address[0])

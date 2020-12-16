from multiprocessing import Process
from threading import Thread
import file_server as server
from file_list_server import *
from file_list_client import *
from pathlib import Path

cache_file_list=""
current_file_list=""


def monitor_file_change_f(path):
    global current_file_list, cache_file_list
    print("start monitoring thread")
    while True:
        current_file_list = traverse_files(path)
        x = find_difference(current_file_list, cache_file_list)
        if x is not None:
            cache_file_list = current_file_list
            send_file_list(VMA, x)
            send_file_list(VMB, x)



def file_server_f():
    print('udp file server process start')
    udp_file_server_port = 12002
    udp_file_server_socket = socket(AF_INET, SOCK_DGRAM)
    udp_file_server_socket.bind(('', udp_file_server_port))
    while True:
        msg, client_address = udp_file_server_socket.recvfrom(10240)  # Set buffer size as 10kB
        return_msg = server.msg_parse(msg)
        udp_file_server_socket.sendto(return_msg, client_address)


if __name__ == '__main__':
    if not Path.exists(Path("share/")):
        Path.mkdir(Path("share"))
    cache_file_list = traverse_files(path)
    file_list_server_p = Process(target=file_list_server_f,args=())
    file_server_p = Process(target=file_server_f, args=())
    file_server_p.start()
    file_list_server_p.start()
    monitor_file_t = Thread(target=monitor_file_change_f, args=(path,))
    monitor_file_t.start()


from multiprocessing import Process
from threading import Thread
from FileUtil import *
import file_server as server
from file_list_server import *
global VMA
newest_file = ""
cache_newest_file = ""


def monitor_file_change_f(cache_list, cache_dir_list, path):
    global newest_file
    print("start monitoring thread")
    while True:
        current_list = walk_subfile_list(path)
        current_dir_list = walk_subdir(path)
        x = find_difference(current_list, current_dir_list, cache_list, cache_dir_list, path)
        if x is not None:
            newest_file = x
            print('add file:', x)
        cache_list = current_list


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
    VMA = "192.168.0.19"
    path = "share"
    cache_list = walk_subfile_list(path)
    cache_dir_list = walk_subdir(path)
    file_list_server_p = Process(target=file_list_server_f,args=())
    file_server_p = Process(target=file_server_f, args=())
    file_server_p.start()
    file_list_server_p.start()
    monitor_file_t = Thread(target=monitor_file_change_f, args=(cache_list, cache_dir_list, path,))
    monitor_file_t.start()


from multiprocessing import Process
from threading import Thread
from FileUtil import *
from tcp_file_list import *
import udp_file_server as server

global VMA
newest_file = ""
cache_newest_file = ""


def monitor_file_change_f(cache_list, cache_dir_list, path):
    global newest_file
    print("start monitoring thread")
    while(1):
        current_list = walk_subfile_list(path)
        current_dir_list = walk_subdir(path)
        x = find_difference(current_list, current_dir_list, cache_list, cache_dir_list, path)
        if x is not None:
            newest_file = x
            print('add file:', x)
        cache_list = current_list


def board_new_file_list_f():
    print('start process 2')
    global cache_newest_file
    global newest_file
    while(1):
        if newest_file != cache_newest_file:
            tcp_send_file_name(newest_file, VMA)
            cache_newest_file = newest_file


def tcp_file_list_server_f():
    print('tcp file list server process start')
    tcp_file_list_server_port = 12000
    tcp_file_list_server_socket = socket(AF_INET, SOCK_STREAM)
    tcp_file_list_server_socket.bind(('', tcp_file_list_server_port))
    tcp_file_list_server_socket.listen(1)
    while(1):
        tcp_receive_file_name(tcp_file_list_server_socket)


def udp_file_server_f():
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
    print(cache_list)
    monitor_file_t = Thread(target=monitor_file_change_f, args=(cache_list, cache_dir_list, path,))
    # send_file_list_t = Thread(target=board_new_file_list_f, args=())
    # receive_file_list_t = Thread(target=receive_new_file_list_f, args=())
    # udp_file_server_t = Thread(target=udp_file_server, args=())
    tcp_file_list_server_p = Process(target=tcp_file_list_server_f, args=())
    udp_file_server_p = Process(target=udp_file_server_f, args=())
    udp_file_server_p.start()
    tcp_file_list_server_p.start()
    monitor_file_t.start()
    # send_file_list_t.start()
    # receive_file_list_t.start()


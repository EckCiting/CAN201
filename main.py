from multiprocessing import Process
from threading import Thread
from FileUtil import *
from tcp_file_list import *
import udp_file_client as client
import udp_file_server as server
import os
import time


newest_file = ""
cache_newest_file = ""


def monitor_file_change_f(cache_list, cache_dir_list, path):
    global newest_file
    print("start process 1")
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
            tcp_send_file_name(newest_file,  '127.0.0.1')
            cache_newest_file = newest_file


def receive_new_file_list_f():
    print('start process 3')
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    while(1):
        tcp_receive_file_name(serverSocket)


def udp_file_server_f():
    print('service start')
    server_port = 12002
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', server_port))
    while True:
        msg, client_address = server_socket.recvfrom(10240)  # Set buffer size as 10kB
        return_msg = server.msg_parse(msg)
        server_socket.sendto(return_msg, client_address)


if __name__ == '__main__':
    path = "share"
    cache_list = walk_subfile_list(path)
    cache_dir_list = walk_subdir(path)
    print(cache_list)
    monitor_file_t = Thread(target=monitor_file_change_f, args=(cache_list, cache_dir_list, path,))
    send_file_list_t = Thread(target=board_new_file_list_f, args=())
    receive_file_list_t = Thread(target=receive_new_file_list_f, args=())
    # udp_file_server_t = Thread(target=udp_file_server, args=())
    udp_file_server_p = Process(target=udp_file_server_f, args=())
    udp_file_server_p.start()

    monitor_file_t.start()
    send_file_list_t.start()
    receive_file_list_t.start()


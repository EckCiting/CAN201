from multiprocessing import Process
from threading import Thread
from time import sleep
import file_server as server
from file_list_server import *
from file_list_client import *
from pathlib import Path
import FileUtil
# file list is a tuple (file_name, modified_time)
cache_file_list = []
current_file_list = []
md5_list = []


def monitor_file_change_f(path):
    global current_file_list, cache_file_list
    print("start monitoring thread")
    while True:
        current_file_list = traverse_files(path)
        new_mod_file_list = find_difference(current_file_list, cache_file_list)
        if new_mod_file_list:
            for new_mod_file in new_mod_file_list:
                new_hash = FileUtil.get_file_md5(new_mod_file[0])
                if new_hash not in md5_list: # old md5 is not removed
                    print("add new file")
                    md5_list.append(new_hash)
                    cache_file_list = current_file_list
                    send_file_list(VMA, new_mod_file)
                    send_file_list(VMB, new_mod_file)


def file_server_f():
    print('udp file server process start')

    file_server_socket = socket(AF_INET, SOCK_DGRAM)
    file_server_socket.bind(('', file_server_port))
    while True:
        msg, client_address = file_server_socket.recvfrom(262144)  # Set buffer size as 256kB
        return_msg = server.msg_parse(msg)
        file_server_socket.sendto(return_msg, client_address)


def init():
    global cache_file_list
    if not Path.exists(Path("share/")):
        Path.mkdir(Path("share"))
    if not Path.exists(Path("temp/")):
        Path.mkdir(Path("temp"))
    cache_file_list = traverse_files(path)
    for file_tuple in cache_file_list:
        md5_list.append(FileUtil.get_file_md5(file_tuple[0]))


if __name__ == '__main__':
    init()
    print(md5_list)
    file_list_server_p = Process(target=file_list_server_f,args=())
    file_server_p = Process(target=file_server_f, args=())
    file_server_p.start()
    file_list_server_p.start()
    sleep(0.2)
    send_file_list(VMA, ["allfiles"])
    send_file_list(VMB, ["allfiles"])
    monitor_file_t = Thread(target=monitor_file_change_f, args=(path,))
    monitor_file_t.start()

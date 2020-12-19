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
#md5_list = []
md5_dict = {}

def monitor_file_change_f(path):
    global current_file_list, cache_file_list
    print("start monitoring thread")
    while True:
        current_file_list = traverse_files(path)
        new_mod_file_list = find_difference(current_file_list, cache_file_list)
        if new_mod_file_list:
            for new_mod_file in new_mod_file_list:
                new_hash = FileUtil.get_file_md5(new_mod_file[0])
                if new_hash not in md5_dict:
                    md5_dict[new_mod_file[0]] = new_hash
                    f = open("md5_list.txt",'a+')
                    f.write(new_mod_file[0] + ',' + new_hash + '\n')
                    f.close()
                    cache_file_list = current_file_list
                    send_file_list(VMA, new_mod_file[0])
                    send_file_list(VMB, new_mod_file[0])


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

    f = open("md5_list.txt",'r+')
    f.seek(0,0)
    line = f.readline()
    while line != "":
        name_md5_list = line.split(',')
        md5_dict[name_md5_list[0]] = name_md5_list[1]
        line = f.readline()

    for file_tuple in cache_file_list:
        if file_tuple[0] not in md5_dict:
            file_hash = FileUtil.get_file_md5(file_tuple[0])
            md5_dict[file_tuple[0]] = file_hash
            f.write(file_tuple[0] + ','+ file_hash +'\n')
    f.close()



if __name__ == '__main__':
    init()
    file_list_server_p = Process(target=file_list_server_f,args=())
    file_server_p = Process(target=file_server_f, args=())
    file_server_p.start()
    file_list_server_p.start()
    sleep(0.2)
    send_file_list(VMA, ["allfiles"])
    send_file_list(VMB, ["allfiles"])
    monitor_file_t = Thread(target=monitor_file_change_f, args=(path,))
    monitor_file_t.start()

from FileInfo import *
from multiprocessing import Process
import os
import time


def walk_subfiles(path):
    for dir_name, subfolder, files in os.walk(path):
        yield files


def fnd_difference(cache_list,path):
    while(1):
        #time.sleep(0.2)
        current_list = walk_list(path)
        if cache_list != current_list:
            # only add files
            main_dict = {}
            main_new_file = ['']
            for file in current_list[0]:
                main_dict[file] = 1
            for file in cache_list[0]:
                main_dict[file] = main_dict[file] + 1
            for file in current_list[0]:
                if main_dict[file] == 1:
                    main_new_file = file

            if len(current_list) == 2:
                sub_dict = {}
                sub_new_file = ['']
                for file in current_list[1]:
                    sub_dict[file] = 1
                if len(cache_list) == 2:
                    for file in cache_list[1]:
                        sub_dict[file] = sub_dict[file] + 1
                for file in current_list[1]:
                    if sub_dict[file] == 1:
                        sub_new_file = file

            cache_list = current_list

            print('add in main dir: ', main_new_file)
            if len(current_list) == 2:
                print('add in sub dir: ', sub_new_file)


def walk_list(path):
    l = list()
    for i in walk_subfiles(path):
        l.append(i)
    return l


if __name__ == '__main__':
    path = "share"
    cache_list = walk_list(path)

    print(cache_list)

    monitor_process = Process(target=fnd_difference, args=(cache_list, path,))
    monitor_process.start()
    print('你是内鬼')
    monitor_process.join()
    print('你是终极内鬼')


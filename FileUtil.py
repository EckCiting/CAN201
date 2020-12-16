import os
from os.path import isfile


def traverse_files(path):
    file_list = []
    file_folder_list = os.listdir(path)
    for file_folder_name in file_folder_list:
        if isfile(path + os.sep + file_folder_name):
            file_list.append(path + os.sep + file_folder_name)
        else:
            file_list.extend(traverse_files(path + os.sep + file_folder_name))
    return file_list


def find_difference(first_file_list, second_file_list, ):
    # O(m + n) not O(n^2)
    # Find out different file between 2 list
    # Since the test process only add files, num(1_list) > num(2_list)
    file_dict = {}
    file_list = []
    for file in first_file_list:
        file_dict[file] = 1

    for file in second_file_list:
        file_dict[file] = file_dict[file] + 1

    for file in first_file_list:
        if file_dict[file] == 1:
            file_list.append(file)
    return file_list






import hashlib
import os, time


def get_file_md5(filename):
    # print(filename)
    f = open(filename, 'rb')
    md5_obj = hashlib.md5()
    while True:
        d = f.read(8192)
        if not d:
            break
        md5_obj.update(d)
    hash_code = md5_obj.hexdigest()
    f.close()
    return hash_code


def traverse_files(path):
    file_list = []
    file_folder_list = os.listdir(path)
    for file_folder_name in file_folder_list:
        sub_path = path + os.sep + file_folder_name
        if os.path.isfile(sub_path):
            modified_time = os.stat(sub_path).st_mtime
            file_list.append((sub_path, modified_time))
        else:
            file_list.extend(traverse_files(sub_path))
    return file_list


def find_difference(first_file_list, second_file_list, ):
    # O(m + n) not O(n^2)
    # Find out different file between 2 list
    # 1st f_l  is current_file_list 2nd f_l is cache_file_list
    # Since the test process only add files, num(1_list) > num(2_list)
    # ? new folder cannot be identified?
    file_dict = {}
    file_list = []
    try:
        for file in first_file_list:
            file_dict[file] = 1

        for file in second_file_list:
            if file in file_dict:
                file_dict[file] = file_dict[file] + 1

        for file in first_file_list:
            if file_dict[file] == 1:
                file_list.append(file)
    except Exception:
        print("some file was deleted")
    return file_list
    # only can pass one file when multiple file is sent into subdir
    # ! now file_list is a string. consider convert it into list !






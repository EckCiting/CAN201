import os


def walk_subfiles(path):
    for dir_name, subdir, files in os.walk(path):
        yield files


def walk_subdir(path):
    for dir_name, subdir, files in os.walk(path):
        return subdir


def walk_subfile_list(path):
    l = list()
    for i in walk_subfiles(path):
        l.append(i)
    return l


def find_difference(current_list, current_dir_list, cache_list, cache_dir_list, path):
            # O(m + n) not O(n^2)
            # current list 比 cache list 多
            file_dict = {}
            for i in range(0, len(current_list)):
                for file in current_list[i]:
                    file_dict[file] = 1
                if len(cache_list) > i:
                    for file in cache_list[i]:
                        file_dict[file] = file_dict[file] + 1
                for file in current_list[i]:
                    if file_dict[file] == 1:
                        new_file = file
                        if i > 0:
                            if len(cache_dir_list) != len(current_dir_list):
                                cache_dir_list = current_dir_list
                            new_file = cache_dir_list[i-1] + os.sep + new_file
                        #print("add in dir: ", new_file)
                        return new_file









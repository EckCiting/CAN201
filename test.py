import file_client
import file_list_client
from FileUtil import traverse_files
import sys
import config

if __name__ == '__main__':
    #a = traverse_files(config.path)
    #a = ['share\\1\\1.1.txt']
    #file_list_client.send_file_list("192.168.0.2", a)
    lst = ["1\\1","2\\2","3\\3"]
    for i in lst:
        print(i)
    print("1\1" in lst)


import file_client
import file_list_client
from FileUtil import traverse_files

if __name__ == '__main__':
    VMA="127.0.0.1"
    path = "share"
    # udp_file_client.udp_request_file("mysql.png",("192.168.0.19",12002)) # pass
    # file_list_client.send_file_list("127.0.0.1",['test1','test2']) #pass

    #with open("share/1/test.txt", "r") as file:
        #print(file.read())
    cache_file_list = traverse_files(path)
    print(cache_file_list[0])
    with open(cache_file_list[0], "r") as file:
        print(file.read())

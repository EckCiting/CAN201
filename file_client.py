import shutil
import struct
import os
import hashlib
import math
import FileUtil

from config import file_server_port

def make_get_file_information_header(filename):
    operation_code = 0
    header = struct.pack('!I', operation_code)
    header_length = len(header + filename.encode())
    return struct.pack('!I', header_length) + header + filename.encode()


def make_get_fil_block_header(filename, block_index):
    operation_code = 1
    header = struct.pack('!IQ', operation_code, block_index)
    header_length = len(header + filename.encode())
    return struct.pack('!I', header_length) + header + filename.encode()


def parse_file_information(msg):
    header_length_b = msg[:4]
    header_length = struct.unpack('!I', header_length_b)[0]
    header_b = msg[4:4 + header_length]
    client_operation_code = struct.unpack('!I', header_b[:4])[0]
    server_operation_code = struct.unpack('!I', header_b[4:8])[0]
    if server_operation_code == 0:  # get right operation code
        file_size, block_size, total_block_number = struct.unpack('!QQQ', header_b[8:32])
        md5 = header_b[32:].decode()
    else:
        file_size, block_size, total_block_number, md5 = -1, -1, -1, ''

    return file_size, block_size, total_block_number, md5


def parse_file_block(msg):
    header_length_b = msg[:4]
    header_length = struct.unpack('!I', header_length_b)[0]
    header_b = msg[4:4 + header_length]
    client_operation_code = struct.unpack('!I', header_b[:4])[0]
    server_operation_code = struct.unpack('!I', header_b[4:8])[0]

    if server_operation_code == 0:  # get right block
        block_index, block_length = struct.unpack('!QQ', header_b[8:24])
        file_block = msg[4 + header_length:]
    elif server_operation_code == 1:
        block_index, block_length, file_block = -1, -1, None
    elif server_operation_code == 2:
        block_index, block_length, file_block = -2, -2, None
    else:
        block_index, block_length, file_block = -3, -3, None

    return block_index, block_length, file_block


def request_file(client_socket, filename, server_address):
    # client_port = 12001
    # client_socket = socket(AF_INET, SOCK_DGRAM)
    # client_socket.bind(('', client_port))

    client_socket.sendto(make_get_file_information_header(filename), (server_address,file_server_port))
    msg, _ = client_socket.recvfrom(24576)
    file_size, block_size, total_block_number, md5 = parse_file_information(msg)

    if file_size >0:
        print('Filename:', filename)
        print('File size:', file_size)
        print('Block size:', block_size)
        print('Total block:', total_block_number)
        print('MD5:', md5)
        operation_code = 1
        # 0 for not download; 1 for new download or resume; 2 for update
        md5_f = open("md5_list.txt")
        line = md5_f.readline()
        while line != "":
            name_md5_list = line.split(',')
            if filename == name_md5_list[0]:
                if md5 == name_md5_list[1]:
                    operation_code = 0
                else:
                    operation_code = 2

            line = md5_f.readline()
        md5_f.close()
        print(operation_code)

        if operation_code == 1:
            # Creat a temp file
            filename_sep = filename.split(os.sep)
            filename_sep[0] = "temp"
            if len(filename_sep) == 3:
                new_path = filename_sep[0] + os.sep + filename_sep[1]
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
            tmp_file = os.sep.join(filename_sep)
            tmp_size = 0
            if os.path.exists(tmp_file):
                tmp_size = os.path.getsize(tmp_file)
                f = open(tmp_file, 'ab+')
            else:
                f = open(tmp_file, 'wb+')

            # Start to get file blocks
            block_index = math.floor(tmp_size / block_size)
            f.truncate(block_index * block_size)
            while block_index < total_block_number:
                # print(block_index)
                client_socket.sendto(make_get_fil_block_header(filename, block_index), (server_address, file_server_port))
                msg, _ = client_socket.recvfrom(block_size + 100)
                block_index_from_server, block_length, file_block = parse_file_block(msg)
                f.write(file_block)
                block_index += 1
            f.close()

            # Check the MD5
            md5_download = FileUtil.get_file_md5(tmp_file)
            if md5_download == md5:
                print('Downloaded file is completed.')
                shutil.move(tmp_file, filename)
            else:
                print('Downloaded file is broken.')
                #os.remove(tmp_file)

        elif operation_code == 2:
            print("updating: ",filename)
            f = open(filename, 'rb+')
            block_index = 0
            base = math.ceil(total_block_number * 0.0015)
            while block_index < total_block_number:
                f.seek(block_size * block_index, 0)
                client_socket.sendto(make_get_fil_block_header(filename, block_index), (server_address, file_server_port))
                msg, _ = client_socket.recvfrom(block_size + 100)
                block_index_from_server, block_length, file_block = parse_file_block(msg)
                f.write(file_block)
                # Check md5 every 0.1% of the data
                block_index += 1
                if block_index % base == 0:
                    if md5 == FileUtil.get_file_md5(filename):
                        print("Update complete")
                        break
            f.close()
        else:
            print("Already have ", filename)
    else:
        print('No such file.', filename)




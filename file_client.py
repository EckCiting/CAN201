import shutil
import struct
import os
import hashlib
from tqdm import tqdm

from config import file_server_port


def get_file_md5(filename):
    global file_dir
    f = open(filename, 'rb')
    contents = f.read()
    f.close()
    return hashlib.md5(contents).hexdigest()


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
    msg, _ = client_socket.recvfrom(102400)
    file_size, block_size, total_block_number, md5 = parse_file_information(msg)

    if file_size >0:
        print('Filename:', filename)
        print('File size:', file_size)
        print('Block size:', block_size)
        print('Total block:', total_block_number)
        print('MD5:', md5)

        # Creat a file
        filename_sep = filename.split(os.sep)
        filename_sep[0] = "temp"
        if len(filename_sep) == 3:
            new_path = filename_sep[0] + os.sep + filename_sep[1]
            if not os.path.exists(new_path):
                os.makedirs(new_path)
        tmp_file = os.sep.join(filename_sep)
        f = open(tmp_file, 'wb')

        # Start to get file blocks
        for block_index in tqdm(range(total_block_number)):
            client_socket.sendto(make_get_fil_block_header(filename, block_index), (server_address, file_server_port))
            msg, _ = client_socket.recvfrom(block_size + 100)
            block_index_from_server, block_length, file_block = parse_file_block(msg)
            f.write(file_block)
        f.close()

        # Check the MD5
        md5_download = get_file_md5(tmp_file)
        if md5_download == md5:
            print('Downloaded file is completed.')
            shutil.move(tmp_file, filename)
        else:
            print('Downloaded file is broken.')
    else:
        print('No such file.')




import os
from os.path import join
import struct
from socket import *
import hashlib, math

file_dir = 'share'
block_size = 1024  # 1kB

server_port = 12002
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', server_port))


def get_file_size(filename):
    return os.path.getsize(join(file_dir, filename))


def get_file_md5(filename):
    f = open(join(file_dir, filename), 'rb')
    contents = f.read()
    f.close()
    return hashlib.md5(contents).hexdigest()


def get_file_block(filename, block_index):
    global block_size
    f = open(join(file_dir, filename), 'rb')
    f.seek(block_index * block_size)
    file_block = f.read(block_size)
    f.close()
    return file_block


def make_return_file_information_header(filename):
    global block_size
    if os.path.exists(join(file_dir, filename)):  # find file and return information
        client_operation_code = 0
        server_operation_code = 0
        file_size = get_file_size(filename)
        total_block_number = math.ceil(file_size / block_size)
        md5 = get_file_md5(filename)
        header = struct.pack('!IIQQQ', client_operation_code, server_operation_code,
                             file_size, block_size, total_block_number)
        header_length = len(header + md5.encode())
        print(filename, file_size, total_block_number, md5)
        return struct.pack('!I', header_length) + header + md5.encode()

    else:  # no such file
        client_operation_code = 0
        server_operation_code = 1
        header = struct.pack('!II', client_operation_code, server_operation_code)
        header_length = len(header)
        return struct.pack('!I', header_length) + header


def make_file_block(filename, block_index):
    file_size = get_file_size(filename)
    total_block_number = math.ceil(file_size / block_size)

    if os.path.exists(join(file_dir, filename)) is False:  # Check the file existence
        client_operation_code = 1
        server_operation_code = 1
        header = struct.pack('!II', client_operation_code, server_operation_code)
        header_length = len(header)
        return struct.pack('!I', header_length) + header

    if block_index < total_block_number:
        file_block = get_file_block(filename, block_index)
        client_operation_code = 1
        server_operation_code = 0
        header = struct.pack('!IIQQ', client_operation_code, server_operation_code, block_index, len(file_block))
        header_length = len(header)
        print(filename, block_index, len(file_block))
        return struct.pack('!I', header_length) + header + file_block
    else:
        client_operation_code = 1
        server_operation_code = 2
        header = struct.pack('!II', client_operation_code, server_operation_code)
        header_length = len(header)
        return struct.pack('!I', header_length) + header


def msg_parse(msg):
    header_length_b = msg[:4]
    header_length = struct.unpack('!I', header_length_b)[0]
    header_b = msg[4:4 + header_length]
    client_operation_code = struct.unpack('!I', header_b[:4])[0]

    if client_operation_code == 0:  # get file information
        filename = header_b[4:].decode()
        return make_return_file_information_header(filename)

    if client_operation_code == 1:
        block_index_from_client = struct.unpack('!Q', header_b[4:12])[0]
        filename = header_b[12:].decode()
        return make_file_block(filename, block_index_from_client)

    # Error code
    server_operation_code = 400
    header = struct.pack('!II', client_operation_code, server_operation_code)
    header_length = len(header)
    return struct.pack('!I', header_length) + header


print('Service start!')

while True:
    msg, client_address = server_socket.recvfrom(10240)  # Set buffer size as 10kB
    return_msg = msg_parse(msg)
    server_socket.sendto(return_msg, client_address)
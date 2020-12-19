import sys
virtual_machines = sys.argv[2]
VMA, VMB = virtual_machines.split(',')
path = "share"
md5_path = "md5.json"
file_list_server_port = 13000
file_server_port = 12002
file_client_port = 12001
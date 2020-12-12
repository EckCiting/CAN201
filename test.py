import file_client
import file_list_client
from FileUtil import traverse_files
import sys
import config

if __name__ == '__main__':
    virtual_machines=sys.argv[2]
    #VMB=sys.argv[3]
    config.VMA, config.VMB = virtual_machines.split(',')
    print("VM1: %s VM2: %s " % (config.VMA,config.VMB))
   # print("VMB: ", VMB)

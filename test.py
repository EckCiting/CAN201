import os
import math
if __name__ == '__main__':
    block_size = 5
    tmp_size = os.path.getsize("neigui2.txt")
    delete_data = tmp_size % block_size
    block_index = math.floor(tmp_size / block_size)
    f = open("neigui2.txt","ab+")
    print("tmp_size:", tmp_size)
    print("block_index:", block_index)
    print("block_size: ", block_size)
    print("multi: ", block_index * block_size)
    f.truncate(block_index * block_size)
    #f.write(b'00')
    f.close()

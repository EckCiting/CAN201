import FileInfo as FI
import os
import math
if __name__ == '__main__':
    block_size = 5
    block_index = 0
    total_block_number = 2
    f = open("neigui.txt","rb+")
    base = math.ceil(total_block_number * 0.0015)
    print(base)
    while block_index < total_block_number:
        f.seek(block_size*block_index, 0)
        f.write(b'11111')
        block_index+=1

    f.close()

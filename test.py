import FileInfo as FI
import os
import math
import json
if __name__ == '__main__':
    f = open("test.json","r+")
    dic = json.load(f)
    if "file2" in dic:
        dic["file2"] = "00"
    dic["file4"] = "123"
    print(dic)
    f.seek(0,0)
    json.dump(dic, f)
    f.close()

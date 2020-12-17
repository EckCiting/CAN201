
if __name__ == '__main__':

    f = open("neigui.txt","rb+")
    line = f.readline()
    print(line)
    f.write(b'000000000')
    f.close()

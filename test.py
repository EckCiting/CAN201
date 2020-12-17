from threading import Thread
import test2
global list1
list1 = []
if __name__ == '__main__':
    list1 = [1,2,3]
    t1 = Thread(target=test2.neigui, args=())
    t1.start()



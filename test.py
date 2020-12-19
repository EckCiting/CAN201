import FileInfo as FI
import os
if __name__ == '__main__':
    list1= [("neigui1",21),("neigui2",51)]

    list1.append(("neigui" + os.sep + "sep",13))
    print(list1)
    list2 = []
    for i in list1:
        list2.append(i[0])

    print(list2)

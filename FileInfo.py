import os
class File:
    def __init__(self,name, size, __mTime):
        self.name = name
        self.size = size
        self.__mTime = __mTime

    def getMTime(self):
        return self.__mTime


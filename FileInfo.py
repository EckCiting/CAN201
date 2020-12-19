import os


class share_file:
    def __init__(self,name, __mTime):
        self.name = name
        self.__mTime = __mTime

    def __str__(self):
        return "filename: " + self.name + " mTime: " + self.__mTime
    __repr__ = __str__

    # def __iter__(self):


    def getMTime(self):
        return self.__mTime


#!/usr/bin/python3

from utils.singleton import Singleton


class Log:
    levels= {
        "debug":0,
        "info":1,
        "warn":2,
        "error":3,
    }
    log_level= 1

    def __init__(self,level=1):
        self.set_level(level)

    def set_level(self,s):

        if isinstance(s, str):
            for level in self.levels:
                if level == s:
                    self.log_level = self.levels[level]
        elif isinstance(s, int):
            if s in range(4):
                self.log_level = s

    def debug(self,msg):
        if self.log_level <= 0:
            print("*DEBUG*: "+str(msg))

    def info(self,msg):
        if self.log_level <= 1:
            print("*INFO*: "+str(msg))

    def warn(self,msg):
        if self.log_level <= 2:
            print("*WARN*: "+str(msg))

    def error(self,msg):
        if self.log_level <= 3:
            print("*ERROR*: "+str(msg))


class SingleLog(Log,metaclass=Singleton):
    pass
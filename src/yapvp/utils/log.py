#!/usr/bin/python3
class Log:

    levels= {
        "debug":0,
        "info":1,
        "warn":2,
        "error":3,
    }
    log_level= 1

    def set_level(self,s):
        for level in self.levels:
            if level == s:
                self.log_level = self.levels[level]

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

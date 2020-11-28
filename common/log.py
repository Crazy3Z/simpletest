# -*- coding: utf-8 -*-
# @author: crazy3z
# @project: script
# @file: log.py
# @time: 2020/10/13 5:57 下午
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import time
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class LogConfig:

    def __init__(self):
        self.logger = logging.getLogger()
        LEVEL = {
            "DEBUG" : logging.DEBUG,
            "INFO" : logging.INFO,
            "WARNING" : logging.WARNING,
            "ERROR" : logging.ERROR
        }
        timestr = time.strftime("%Y-%m-%d", time.localtime())
        self.logname = "%s-log.txt"%timestr
        self.logpath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../Log/"))
        if not os.path.exists(self.logpath):
            os.mkdir(self.logpath)
        self.logfile  = os.path.join(self.logpath, self.logname)
        # self.formatter = logging.Formatter("")
        self.formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s] : %(message)s", "%Y-%m-%d %H:%M:%S")
        self.logger.setLevel(logging.DEBUG)

        # 控制台输出的handler
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(self.formatter)
        self.logger.addHandler(console)

        #输出文件流的handler
        filehandler = logging.FileHandler(self.logfile)
        filehandler.setFormatter(self.formatter)
        filehandler.setLevel(logging.DEBUG)
        self.logger.addHandler(filehandler)

        # 回滚日志
        # handler = RotatingFileHandler(filename=self.logfile, maxBytes=1024*1024*10, backupCount=2)
        # handler.setFormatter(self.formatter)
        # handler.setLevel(logging.DEBUG)
        # self.logger.addHandler(handler)


    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    @classmethod
    def set_logger(self, name):
        self.logger = logging.getLogger(name)
        return self.logger

logconfig = LogConfig()

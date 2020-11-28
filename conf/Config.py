# -*- coding: utf-8 -*-
# @author: crazy3z
# @project: script
# @file: Config.py
# @time: 2020/10/13 4:43 下午
import os
from configparser import ConfigParser

class ConfigInfo:

    def __init__(self):
        """
        初始化配置信息
        """
        self.config = ConfigParser()
        self.ConfigPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
        if not os.path.exists(self.ConfigPath):
            raise FileNotFoundError("配置文件config.ini不存在该目录下 %s 需要手动添加" %self.ConfigPath)
        self.config.read(self.ConfigPath, encoding='utf-8')

    def setConfig(self, module, title, content):
        '''
        修改配置文件的内容
        :param module: 模块
        :param title: 标题
        :param content: 内容
        :return:
        '''

        if not self.config.has_section(module):
            self.config.add_section(module)
        self.config.set(module, title, content)
        with open(self.ConfigPath, mode='w+', encoding="utf-8") as f:
            self.config.write(f)
        return self.config.sections()


    def deleteConfig(self, module=None, title=None):
        '''
        删除配置信息
        :param module:section名称
        :param title:option名称
        :return:
        '''
        if title:
            self.config.remove_option(module, title)
        elif module:
            self.config.remove_section(module)
        with open(self.ConfigPath, mode='w+', encoding="utf-8") as f:
            return self.config.write(f)
        return self.config.sections()


if __name__ == '__main__':

    config = ConfigInfo()
    print(config.config.sections())

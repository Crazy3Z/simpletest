# -*- coding: utf-8 -*-
# @author: crazy3z
# @project: script
# @file: data.py
# @time: 2020/10/23 11:39 下午
import os
import yaml
import json
import pymysql
from configparser import ConfigParser
from common.log import logconfig

logger = logconfig.set_logger(__name__)

class DataLoad:
    """
    配置信息加载类，可读取yaml ini json 数据，后续更新excel csv
    """

    def __init__(self):
        pass

    @classmethod
    def load_yaml(self, path):
        """加载yaml文件信息"""
        logger.info("加载 {} 的yaml文件".format(path))
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        logger.debug("读取到yaml数据中的data ==>> {}".format(data))
        return data

    @classmethod
    def load_json(self, path):
        """加载json文件信息"""
        logger.info("加载 {} 的json文件".format(path))
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        logger.debug("读取到json数据中的data ==>> {}".format(data))
        return data

    @classmethod
    def load_ini(self, path):
        """加载ini数据信息"""
        logger.info("加载 {} 的ini文件".format(path))
        config = ConfigParser()
        config.read(path, encoding="utf-8")
        data = dict(config._sections)
        logger.debug("读取到ini数据中的data ==>> {}".format(data))
        return data

    @classmethod
    def load_excel(self, path):
        pass

    @classmethod
    def load_csv(self, path):
        pass

class DataBase:
    """
    mysql 数据库配置类
    """

    def __init__(self, config):
        self.config = config
        db_conf = {
            "host" : config['mysql'].get("host"),
            "port" : int(config['mysql'].get("port")),
            "user" : config['mysql'].get("user"),
            "password" : config['mysql'].get("password"),
            "db" : config['mysql'].get("database")
        }
        try:
            if config["mysql"]["status"] != 'closed':
                logger.info("准备连接mysql数据库")
                self.conn = pymysql.connect(**db_conf)
                logger.info("数据库连接成功")
                self.data_pre()
            else:
                logger.info("数据库开关关闭，不需要连接数据库，即将开始测试，如果需要配置数据库打开数据库配置开关请更新conf/config.ini下 mysql/status:open/closed")
        except Exception as e:
            logger.error("数据库连接失败，原因：%s", e)

    def get_cursor(self):
           return self.conn.cursor()

    def query_sql(self, sqlstring):
        """
        执行mysql数据库查询语句
        :param sqlstring:
        :return: 查询所有结果的列表
        """
        cursor = self.get_cursor()
        try:
            cursor.execute(sqlstring)
            results = cursor.fetchall()
            return [result for result in results]
        except Exception as e:
            logger.error("%s 执行查询失败， 原因：%s", sqlstring, e)

    def exec_sql(self, sqlstring):
        """
        数据库执行sql语句
        :param sqlstring: sql语句
        :return:None
        """
        cursor = self.get_cursor()
        try:
            cursor.execute(sqlstring)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logger.error("%s 执行失败已回滚， 原因：%s", sqlstring, e)

    def data_pre(self):
        """
        检查数据准备的sql语句，存在即执行响应的sql
        :return:
        """
        if self.config.get("pre_sql"):
            for sqlstring in self.config.get("pre_sql"):
                self.exec_sql(self.config.get("pre_sql").get(sqlstring))
            logger.info("数据准备工作完成，准备开始测试")
        else:
            logger.info("未检查到数据准备的sql, skip数据准备步骤，如果需要数据准备，请在conf文件下config.ini/pre_sql下添加sql语句")

    def data_clear(self):
        """
        数据清理执行
        :return: None
        """
        if self.config.get("mysql").get("clear_need") and self.config.get("clear_sql"):
            for sqlstring in self.config.get("clear_sql"):
                self.exec_sql(self.config.get("clear_sql").get(sqlstring))
            logger.info("数据清理开关已打开，数据清理完成")
        else:
            logger.info("数据清理开关未打开，skip数据清理，如果需要清理数据，请在conf文件下config.ini/clear_sql下添加sql语句")

    def close(self):
        """
        断开数据连接方法，检查数据清理开关，打开直接清理反之跳过数据清理
        :return: None
        """
        if self.config["mysql"]["status"] != 'closed':
            self.data_clear()
            self.get_cursor().close()
            self.conn.close()
            logger.info("数据库断开连接")
        else:
            logger.info("数据库开关未打开， 不需要处理数据库")



if __name__ == '__main__':
    x = DataLoad.load_yaml("../TestCase/case.yaml")
    for i in x.items():
        print(i)

# -*- coding: utf-8 -*-
# @author: crazy3z
# @project: script
# @file: case.py
# @time: 2020/11/3 4:45 下午
import os
import json

class Case:
    """
    case信息的抽象类，可以从解析的case详情中实例化成单个的case
    """

    def __init__(self, name, detail, conf):
        self.name = name
        self.detail = detail
        self.temp = conf.get("header")
        self.conf = conf
        self.root_url = None

    @property
    def method(self):
        return self.detail.get("method")

    @property
    def url(self):
        return self.detail.get("uri")

    @property
    def header(self):
        """
        获取请求头信息，默认取conf.ini文件中的header作为请求头，如果case信息中含有请求把case中请求头相关信息merge到公共头中
        :return:request header => dict
        """
        header = {}
        if self.detail.get("header"):
            for key, value in self.detail.get("header").items():
                header[key] = value
        header.update(self.temp)
        return header

    @property
    def excepted_result(self):
        return self.detail.get("resultcheck")

    @property
    def excepted_code(self):
        return self.detail.get("exceptcode", 200)

    def update_env(self, env):
        return self.conf.get(env)

    @property
    def data(self):
        """
        根据不同的content-type把requestdata转化成响应的格式
        :return: requestdata
        """
        if self.header.get("Content-Type") == "application/json":
            data = json.dumps(self.detail.get("requestData"), ensure_ascii=False)
        elif self.header.get("Content-Type") == "multipart/form-data":
            try:
                if os.path.exists(self.detail.get("requestData")):
                    with open(self.detail.get("requestData"), encoding="utf-8", mode="rb") as f:
                        data = f.read()
            except Exception as e:
                data = self.detail.get("requestData")
        else:
            data = self.detail.get("requestData")
        return data

    @property
    def need_cookie(self):
        """
        检查case是否需要cookie
        :return: False/True
        """
        return self.detail.get("login")

    @property
    def others(self):
        return self.detail.get("others")

    def update_data(self, key, value):
        """
        更新case的requestdata内容
        :param key:
        :param value:
        :return:
        """
        self.detail.get("requestData").update({key:value})

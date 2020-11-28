# -*- coding: utf-8 -*-
# @author: crazy3z
# @project: script
# @file: HttpResquest.py
# @time: 2020/10/21 5:44 下午
import requests
from common.log import logconfig

logger = logconfig.set_logger(__name__)

class API:
    """
    封装的request类，包括请求的分发，响应结果的校验
    """

    def __init__(self, base_url):
        self.root_url = base_url
        self.s = requests.session()
        self.timeout = 8
        self.cookie = None

    def request(self, caseinfo):
        """
        请求分发
        :param caseinfo:
        :return:
        """
        if caseinfo.need_cookie:
            self.cookie = self.get_cookie(caseinfo)

        if hasattr(self, caseinfo.method):
            logger.debug("即将测试链接：%s, 请求方式：%s, 参数：%s ,请求头：%s, cookie: %s ",
                         self.root_url + caseinfo.url, caseinfo.method, caseinfo.data, caseinfo.header, self.cookie)
            return getattr(self, caseinfo.method)(caseinfo)
        else:
            raise Exception("找不到这个请求的方法")

    def get(self, caseinfo):
        """get 请求处理"""
        try:
            res = self.s.get(self.root_url + caseinfo.url,
                             params=caseinfo.data,
                             cookies=self.cookie,
                             timeout=self.timeout,
                             verify=False,
                             headers=caseinfo.header)
            return res
        except Exception as e:
            logger.error("报错的url link是 %s", self.root_url+caseinfo.url)
            logger.error("异常错误：%s", e)
            return

    def post(self, caseinfo):
        """post请求处理"""
        try:
            if caseinfo.header.get("Content-Type") == "multipart/form-data":
                res = self.s.post(self.root_url+caseinfo.url,
                                  files=caseinfo.data,
                                  timeout=self.timeout,
                                  verify=False,
                                  cookies=self.cookie,
                                  headers=caseinfo.header)
            else:
                res = self.s.post(self.root_url+caseinfo.url,
                                  data=caseinfo.data,
                                  timeout=self.timeout,
                                  cookies=self.cookie,
                                  headers=caseinfo.header)
            return res

        except Exception as e:
            logger.error("报错的url link是 %s", self.root_url+caseinfo.url)
            logger.error("异常错误：%s", e)
            return

    def put(self, caseinfo):
        """put请求处理"""
        try:
            res = self.s.put(self.root_url+caseinfo.url,
                             data=caseinfo.data,
                             cookies=self.cookie,
                             verify=False,
                             timeout=self.timeout,
                             headers=caseinfo.header)
            return res
        except Exception as e:
            logger.error("报错的url link是 %s", self.root_url+caseinfo.url)
            logger.error("异常错误：%s", e)
            return

    def delete(self, caseinfo):
        """delete请求处理"""
        try:
            res = self.s.delete(self.root_url+caseinfo.url,
                                data=caseinfo.data,
                                cookies=self.cookie,
                                verify=False,
                                timeout=self.timeout,
                                headers=caseinfo.header)
            return res
        except Exception as e:
            logger.error("报错的url link是 %s", self.root_url+caseinfo.url)
            logger.error("异常错误：%s", e)
            return

    def get_cookie(self, case):
        """从配置信息的账号密码，网址中获取cookie"""
        data = {}
        for name, value in case.conf["cookie"]:
            if name != "url":
                data[name] = value
        logger.debug("请求URL：%s ，请求body参数 %s，请求方式post，准备获取cookie", case.conf["cookie"]["url"], data)
        res = self.s.post(case.conf["cookie"]["url"], data=data,headers=case.header)
        if not res.cookies:
            logger.error("获取的cookie值为空")
            raise Exception("没有获取到cookie")
        logger.debug("获取到的cookie ==> %s", res.cookies.get_dict())
        return res.cookies.get_dict()

    @classmethod
    def response_check(self, response, caseinfo):
        """响应结果的校验"""
        if not response:
            logger.error("response是空，请检查 test case 或者接口服务器")
            return
        response_dict = dict(code=response.status_code,
                             text = response.text)
        try:
            response_dict["json"] = response.json()
        except Exception as e:
            logger.debug("response 中不含有json数据，报错：%s", e)
            response_dict["json"] = " "
        logger.debug("返回构造的response 字典数据为：%s", response_dict)
        if not self.check_code(self, response_dict, caseinfo.excepted_code):
            logger.info("%s 测试结果 ==>> Failed ", caseinfo.name)
            return False, response_dict
        if not self.check_result(self, response_dict, caseinfo.excepted_result):
            logger.error("%s 响应结果与预期不符，响应结果是%s，预期结果是%s", caseinfo.name, response_dict, caseinfo.excepted_result)
            logger.info("%s 测试结果 ==>> Failed ", caseinfo.name)
            return False, response_dict
        logger.debug("测试结果：响应body ==>> PASS")
        logger.info("测试结果：%s ==>> PASS ", caseinfo.name)
        return True, response_dict

    def check_code(self, result, excepted):
        """校验http状态码"""
        if result.get("code") == excepted:
            logger.debug("测试结果：状态响应码 ==>> PASS")
            return True
        else:
            logger.error("响应状态码与预期不符，实际返回：%s，预期结果：%s", result, excepted)
            return False

    def check_result(self, result, excepted):
        """校验返回body"""
        if isinstance(excepted, dict):
            return result.get("json") == excepted
        else:
            return excepted in result.get("text") or excepted == result.get("text")



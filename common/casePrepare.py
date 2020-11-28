# -*- coding: utf-8 -*-
# @author: crazy3z
# @project: script
# @file: DataPrepare.py
# @time: 2020/11/21 4:18 下午
import os
from common.log import logconfig
from common.data import DataLoad
from common.case import Case
from common.commonPool import Pool


logger = logconfig.set_logger(__name__)

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class TestPrepare(Pool):
    """
    继承公共连接池类，初始化的同时，将case分类信息初始化分类
    """

    def __init__(self, confFile):
        self.confFile = confFile
        self.testInfo = self.getTestinfo()
        self.casesInfo = self.getallCaseinfo()
        super(TestPrepare, self).__init__(self.casesInfo)
        logger.debug("解析用例文件后一共发现%s个单接口测试用例，%s个关联接口测试用例", len(self.single_interface), len(self.associate_interface))

    def getoneCaseinfo(self, casefile):
        """
        解析单个yaml文件内的用例信息
        :param casefile:
        :return:
        """
        file_path = os.path.join(BASE_PATH, "testcase", casefile)
        if not os.path.exists(file_path):
            raise Exception("case 文件不存在，请在TestCase目录下创建%s文件", self.casefile)
        cases = DataLoad.load_yaml(file_path)
        logger.info("解析用例文件 %s 存在 %s 条case 分别是 %s", casefile, len(cases.keys()), cases.keys())
        case = []
        for key, value in cases.items():
            testcase = Case(key, value, self.testInfo)
            case.append((testcase.method, testcase.data, testcase))
        return case

    def getTestinfo(self):
        """
        获取默认的配置信息
        :return:
        """
        file = os.path.join(BASE_PATH, "conf", self.confFile)
        if not os.path.exists(file):
            raise Exception("配置信息文件不存在， 请在conf目录下创建%s" % self.confFile)
        testInfo = DataLoad.load_ini(file)
        logger.info("解析配置信息一共有 %s 个，分别是 %s", len(testInfo.keys()), testInfo.keys())
        return testInfo

    def getallCaseinfo(self):
        """
        获取多个yaml文件内的用例信息
        :return:
        """
        file_list = os.listdir("testcase")
        yaml_list = filter(lambda x:x.endswith(".yaml"), file_list)
        cases = []
        for yaml_file in yaml_list:
            cases.extend(self.getoneCaseinfo(yaml_file))
        logger.info("一共解析到%s个测试用例", len(cases))
        return cases

PreInfo = TestPrepare("config.ini")
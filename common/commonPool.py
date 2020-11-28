# -*- coding: utf-8 -*-
# @author: crazy3z
# @project: script
# @file: commonPool.py
# @time: 2020/11/23 9:18 下午


class Pool:
    """
    公共池，处理单接口用例，关联接口用例，用例执行结果
    """

    def __init__(self, casesInfo):
        self.single_interface = None
        self.associate_interface = None
        self.finished_interface = {}
        self.diff_interface(casesInfo)

    def diff_interface(self, cases):
        """
        把所有的case分成单接口测试集和关联接口测试用例集
        :param cases: 所有实例化的Case对象组成的列表，Preinfo里getallcaseinfo返回值
        :return:单接口测试用例集，关联接口测试用例集
        """
        case_list = set([case[2] for case in cases])
        associate_list = set(filter(lambda info:info.others, case_list))
        self.single_interface = list(case_list.difference(associate_list))
        self.associate_interface = list(associate_list)

    def extract_result(self, result, params):
        """
        提取关联参数的对应的值
        :param result:
        :param params:
        :return:
        """
        if not result["params"].get(params):
            pass
        return result["params"].get(params)

    def update_case_status(self, case, result):
        """
        接口完成测试的列表更新,把测试完成的接口从相应的接口列表中移除
        :param case: Case实例化对象
        :param result: 封装的request返回对象
        :return: {用例名称：{response：响应结果,params:关联参数字典}...}
        """
        self.finished_interface[case.name] = dict(response=result)
        self.finished_interface[case.name]["params"] = self.generate_params()(result)
        if case in self.single_interface:
            self.single_interface.remove(case)
        else:
            self.associate_interface.remove(case)

    def generate_params(self):
        """
        将可能存在的嵌套字典统一成一个字典
        :param response: 构造的响应结果
        :return:{参数名称：值.....}
        """
        params = {}
        def update(res):
            for k, v in res.items():
                params[k] = v
                if isinstance(v, dict):
                    update(v)
            return params
        return update



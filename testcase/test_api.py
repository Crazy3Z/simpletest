# -*- coding: utf-8 -*-
# @author: crazy3z
# @project: script
# @file: test_api.py
# @time: 2020/10/26 10:01 下午
import pytest
import allure
from common.log import logconfig
from common.Resquest import API
from common.casePrepare import PreInfo

logger = logconfig.set_logger(__name__)


@pytest.mark.usefixtures("init_database")
class TestApi:

    @allure.story("单接口测试用例")
    @allure.title("{detail.name}")
    @pytest.mark.parametrize("detail", PreInfo.single_interface)
    def test_yaml_single(self,  detail, init_database, cmdopt):
        """
        测试单接口用例集，后续可调用init_database进行数据库校验
        :param method: 请求方式
        :param params: 请求参数
        :param detail: case 实例化对象
        :param init_database: 数据库的cursor，可以调用校验数据库
        :return:
        """
        logger.info("正在测试单接口 %s", detail.name)
        detail.root_url = detail.update_env(cmdopt).get("host")
        res = API(detail.root_url).request(detail)
        testresult, poolstatus = API.response_check(res, detail)
        PreInfo.update_case_status(detail, poolstatus)
        assert testresult is True

    @allure.story("关联接口测试用例")
    @allure.title("{detail.name}")
    @pytest.mark.parametrize("detail", PreInfo.associate_interface)
    def test_yaml_associate(self, detail, init_database, cmdopt):
        """
        关联接口测试用例集
        :param detail:
        :return:
        """
        logger.info("正在测试关联接口 %s", detail.name)
        if detail.others.get("name") in PreInfo.finished_interface.keys():
            get_params = PreInfo.finished_interface.get(detail.others["name"])
            logger.info("公共关联池中已找到依赖的参数请求,在完成用例的结果中找到的参数集是 %s", get_params)
            extract_params = PreInfo.extract_result(get_params, detail.others["query_str"])
            logger.debug("提取到的关联参数'%s'的值是'%s',merge到requestdata的key是'%s'", detail.others["query_str"], extract_params, detail.others["rename"])
            detail.update_data(detail.others["rename"], extract_params)
        else:
            logger.error("没有在单接口用例集中找到依赖的参数接口，请按照单接口用例格式在yaml文件中添加请求信息")
            raise Exception("找不到依赖的关联参数")
        detail.root_url = detail.update_env(cmdopt).get("host")
        res = API(detail.root_url).request(detail)
        testresult, poolstatus = API.response_check(res, detail)
        PreInfo.update_case_status(detail, poolstatus)
        assert testresult is True

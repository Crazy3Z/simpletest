# -*- coding: utf-8 -*-
# @author: crazy3z
# @project: script
# @file: conftest.py
# @time: 2020/11/21 4:36 下午
import pytest
import time
from common.log import logconfig
from common.casePrepare import PreInfo
from common.data import DataBase

logger = logconfig.set_logger(__name__)

# @pytest.fixture(params=PreInfo.finished_interface)
# def finished(request):
#     return request.param

def pytest_addoption(parser):
    parser.addoption("--env",
                     action="store",
                     default="private_debug",
                     help="将选择的环境信息配置到pytest配置中")

@pytest.fixture(scope="session", autouse=True)
def cmdopt(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="class")
def init_database():
    """
    引入sql cursor，实现了数据准备和清理功能，后续可以做数据库校验
    :return:
    """
    logger.info("整体测试开始")
    sql_con = DataBase(PreInfo.testInfo)
    yield sql_con
    sql_con.close()
    logger.info("整体测试结束")

@pytest.fixture(scope="function", autouse=True)
def timerInfo(cmdopt):
    """
    计时器，但是包括一部分程序执行时间
    :return:
    """
    logger.info("============================Test START========================")
    start = time.time()
    yield
    total_time = time.time() - start
    logger.info("timer:本次测试耗时共计 %.3f 数据仅供参考", total_time)
    logger.info("============================Test END==========================")

# @pytest.fixture(scope="function")
# def find_params(request):
#     pass




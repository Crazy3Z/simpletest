# -*- coding: utf-8 -*-
# @author: crazy3z
# @project: script
# @file: run.py
# @time: 2020/11/19 11:49 下午

import pytest
import os

if __name__ == '__main__':
    pytest.main(["-sq", "--env=online_release", "--alluredir", "./report"])
    os.system("allure generate --clean report -o allure-report")
# simpletest
simple api test demo
### 项目介绍

基于python3 requests+pytest+allure+yaml的接口测试框架，可以测试基于http/http协议的get, post,put,delete请求，后续会集成Jenkins和head，patch，option的请求。

### 目录结构

```
apitest/
├── allure-report/
├──common/
│   ├── case.py
│   ├──casePrepare.py
│   ├──commonPool.py
│   ├──data.py
│   ├──log.py
│   └──Request.py
├──conf/
│		├──Config.py
│ 	└──config.ini
├──log/
├──report/
├──testcase/
│		├──conftest.py
│   └──test_api.py
└── run.py
```

- common目录封装的是通用方法：case.py 是测试用例的抽象类；casePare.py是用例初始化分类+参数公共池初始化；commonPool公共池的抽象类；data.py是封装的是文件中数据加载方法和数据库操作；log.py是封装的logging模块；request.py是封装的request请求和响应结果校验。
- Conf目录下是配置信息的配置和读取，在config.ini文件中有环境的配置信息和数据库的配置信息，还有公共header和登陆的url，账号和密码，以及测试前的数据准备和数据清理配置信息。
- testcase目录下存放测试用例，可以按照示例中的yaml格式编写测试用例，支持多个文件识别。conftest.py是测试前的setup和teardown功能以及简单的timer。可以自己扩展。test_api.py是编写的测试通用测试用例的测试类。主要分为单接口测试用例和有依赖的复杂接口测试用例。
- run.py 入口函数，执行python run.py 生成allure测试报告，如果不需要测试报告可以直接在apitest目录下执行 pytest -s。
- allure-report存放allure的html测试报告
- log存放执行产生的log文件，按日期分类
- report 存放生成allure report需要的文件

### 环境

Mac OS(Windows没试过)，python3.8，allure，mysql

### 运行

1. 首先配置conf.ini文件，可以添加多个环境配置信息，具体信息填写规范可参考代码中文件。
2. 在testcase目录下编写yaml测试用例，有固定的格式规范，可以创建多个用例文件，case中如果有请求头的相关信息会直接覆盖添加到公共请求头上。
3. 运行时通过--env来指定你所选择的环境，或者更改run.py的信

```python
pytest -s --env private_debug #private_debug是自定义的环境配置名称
```

### 附加：

如果需要数据准备和数据清理需要在conf.ini文件中设置相应的开关和数据准备的Sql语句，没有需求则可以跳过。

### 流程图

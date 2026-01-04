---
title: 多种方式获取 pytest 测试用例名称
date: 2028-06-27
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 多种方式获取 pytest 测试用例名称，并提供多重实践
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 概述

基于`pytest`写自动化测试用例，用例有的是在测试类下，有的不在测试类下，参考如下所示：

```python
class TestName():
    def test_case01(self):
        """Test case"""
        assert 1 == 1

		
def test_case02():
    """这是测试用例2"""
    assert 2 == 2


	
def test_case03():
    assert 3 == 3
```

要如何获取到测试用例名称呢？

使用了`pytest fixture`，在`pytest.ini`设置了日志格式，但是记录的日志里获取到的测试用例的名称要么显示为空，或者显示内容被截断，这说明在`conftest.py`里定义的`fixture`获取测试用例名称有`Bug`了。

要如何正确获取测试用例信息？

# 解决方案

准备好`pytest.ini`和测试用例文件，参考如下：

## pytest.ini文件

```ini
[pytest]
# 日志配置
log_cli = false
log_level = NOTSET
log_file = reports/automation.log
log_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_date_format=%Y-%m-%d %H:%M:%S
log_file_level = DEBUG
log_file_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_file_date_format=%Y-%m-%d %H:%M:%S
log_cli_level = INFO
log_cli_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_cli_date_format=%Y-%m-%d %H:%M:%S

# allure报告配置
addopts = -vrsXX -p no:warnings --show-progress --alluredir=reports/json --clean-alluredir
norecursedirs = .svn .idea .git
console_output_style = count

# 标记配置
markers =
    smoke: 冒烟测试
    regression: 回归测试
    api: API测试
    web: Web测试
    ui: UI测试

# 禁用警告
# filterwarnings = ignore::DeprecationWarning
filterwarnings =
    ignore:please use dns.resolver.Resolver.resolve() instead:DeprecationWarning
    ignore:The hookimpl ProgressTerminalReporter.pytest_report_teststatus uses old-style configuration options:pytest.PytestDeprecationWarning
    ignore:.*RLock.*greened.*:UserWarning
```

## 测试用例

`test_example.py`:

```python
class TestName():
    def test_case01(self):
        """Test case"""
        assert 1 == 1

def test_case02():
    """这是测试用例2"""
    assert 2 == 2

	
def test_case03():
    assert 3 == 3
```

又额外准备了一些其他测试用用例，放在父目录、子目录下，这里就不再逐一展示用例内容了：

```shell

```

## 方案1：使用 request.node 属性直接获取

直接使用 `request.node.nodeid` 获取完整测试路径：

```python
# conftest.py
import logging

import pytest


@pytest.fixture(scope='session', autouse=True)
def testsuite_setup_teardown():
    """记录测试集的前置和后置日志"""
    dash_count = 31
    logging.info("%s Start to run test case %s", '-' * dash_count, '-' * (dash_count + 14))
    yield
    logging.info("%s End to run test case %s\n", '-' * dash_count, '-' * (dash_count + 16))


@pytest.fixture(scope='function', autouse=True)
def testcase_setup_teardown(request):
    """测试用例的前置和后置，记录当前正在执行的测试用例名称"""
    dash_count = 31

    # 获取当前测试用例的完整名称（包括文件相对路径、类名和方法名）
    full_name = request.node.nodeid

    logging.info("%s Begin %s", '-' * dash_count, '-' * (dash_count + 5))
    logging.info("当前测试用例名称: (%s)", full_name.encode("utf-8").decode("unicode_escape"))
    yield
    logging.info("%s End %s\n", '-' * dash_count, '-' * (dash_count + 7))
```

用例运行后，查看日志：

```shell
2026-01-01 15:42:14 [conftest.py:10  ] [ INFO] ------------------------------- Start to run test case ---------------------------------------------
2026-01-01 15:42:14 [conftest.py:24  ] [ INFO] ------------------------------- Begin ------------------------------------
2026-01-01 15:42:14 [conftest.py:25  ] [ INFO] 当前测试用例名称: (test_examples.py::TestName::test_case01)
2026-01-01 15:42:14 [conftest.py:27  ] [ INFO] ------------------------------- End --------------------------------------

2026-01-01 15:42:14 [conftest.py:24  ] [ INFO] ------------------------------- Begin ------------------------------------
2026-01-01 15:42:14 [conftest.py:25  ] [ INFO] 当前测试用例名称: (test_examples.py::test_case02)
2026-01-01 15:42:14 [conftest.py:27  ] [ INFO] ------------------------------- End --------------------------------------

2026-01-01 15:42:14 [conftest.py:24  ] [ INFO] ------------------------------- Begin ------------------------------------
2026-01-01 15:42:14 [conftest.py:25  ] [ INFO] 当前测试用例名称: (test_examples.py::test_case03)
2026-01-01 15:42:14 [conftest.py:27  ] [ INFO] ------------------------------- End --------------------------------------

2026-01-01 15:42:14 [conftest.py:24  ] [ INFO] ------------------------------- Begin ------------------------------------
2026-01-01 15:42:14 [conftest.py:25  ] [ INFO] 当前测试用例名称: (testcases/feature1/test_example3.py::TestUserAPI::test_create_user)
2026-01-01 15:42:14 [conftest.py:27  ] [ INFO] ------------------------------- End --------------------------------------

2026-01-01 15:42:14 [conftest.py:24  ] [ INFO] ------------------------------- Begin ------------------------------------
2026-01-01 15:42:14 [conftest.py:25  ] [ INFO] 当前测试用例名称: (testcases/feature1/test_example3.py::TestUserAPI::test_get_user)
2026-01-01 15:42:14 [conftest.py:27  ] [ INFO] ------------------------------- End --------------------------------------

2026-01-01 15:42:14 [conftest.py:24  ] [ INFO] ------------------------------- Begin ------------------------------------
2026-01-01 15:42:14 [conftest.py:25  ] [ INFO] 当前测试用例名称: (testcases/feature1/test_example3.py::test_endpoint)
2026-01-01 15:42:14 [conftest.py:27  ] [ INFO] ------------------------------- End --------------------------------------

2026-01-01 15:42:14 [conftest.py:24  ] [ INFO] ------------------------------- Begin ------------------------------------
2026-01-01 15:42:14 [conftest.py:25  ] [ INFO] 当前测试用例名称: (testcases/test_example1.py::test_user_registration)
2026-01-01 15:42:14 [conftest.py:27  ] [ INFO] ------------------------------- End --------------------------------------

2026-01-01 15:42:14 [conftest.py:24  ] [ INFO] ------------------------------- Begin ------------------------------------
2026-01-01 15:42:14 [conftest.py:25  ] [ INFO] 当前测试用例名称: (testcases/test_example2.py::test_dynamic_marks)
2026-01-01 15:42:14 [conftest.py:27  ] [ INFO] ------------------------------- End --------------------------------------

2026-01-01 15:42:14 [conftest.py:24  ] [ INFO] ------------------------------- Begin ------------------------------------
2026-01-01 15:42:14 [conftest.py:25  ] [ INFO] 当前测试用例名称: (testcases/test_example2.py::test_mark_method)
2026-01-01 15:42:14 [conftest.py:27  ] [ INFO] ------------------------------- End --------------------------------------

2026-01-01 15:42:14 [conftest.py:12  ] [ INFO] ------------------------------- End to run test case -----------------------------------------------
```


可以看到，能够正常展示测试用例名称信息了，有文件路径，有测试类名/函数名，查找起来就方便多了。


## 方案2： 使用 request.node 的原始名称

```python
# conftest.py
import pytest
import logging

@pytest.fixture(scope='function', autouse=True)
def log_test_info(request):
    """记录测试信息 - 使用原始名称"""
    # 获取原始节点名称（不包含路径）
    original_name = request.node.originalname if hasattr(request.node, 'originalname') else request.node.name
    
    # 获取测试类名（如果有）
    class_name = None
    if hasattr(request.node, 'cls') and request.node.cls:
        class_name = request.node.cls.__name__
    
    # 构建完整名称
    if class_name:
        full_name = f"{class_name}.{original_name}"
    else:
        full_name = original_name
    
    logging.info(f"测试用例: {full_name} (文件: {request.node.nodeid})")
    
    yield
```

用例运行后，查看日志：

```shell

```


## 方案3：使用测试函数属性

```python
import pytest
import logging
import inspect

@pytest.fixture(scope='function', autouse=True)
def log_with_function_info(request):
    """通过测试函数对象获取信息"""
    # 获取测试函数对象
    test_function = getattr(request.node, 'function', None)
    
    if test_function:
        # 获取函数名
        func_name = test_function.__name__
        # 获取模块名
        module_name = test_function.__module__
        # 获取行号
        try:
            line_no = inspect.getsourcelines(test_function)[1]
        except:
            line_no = "unknown"

        logging.info(f"定义行号: {line_no},所在模块: {module_name}.py,测试函数: {func_name}")
    else:
        # 回退到节点信息
        logging.info(f"测试用例: {request.node.name}")
    
    yield
```

用例运行后，查看日志：

```shell
2026-01-01 16:13:41 [conftest.py:22  ] [ INFO] 定义行号: 2,所在模块: test_examples.py,测试函数: test_case01
2026-01-01 16:13:41 [conftest.py:22  ] [ INFO] 定义行号: 6,所在模块: test_examples.py,测试函数: test_case02
2026-01-01 16:13:41 [conftest.py:22  ] [ INFO] 定义行号: 11,所在模块: test_examples.py,测试函数: test_case03
2026-01-01 16:13:41 [conftest.py:22  ] [ INFO] 定义行号: 8,所在模块: test_example3.py,测试函数: test_create_user
2026-01-01 16:13:41 [conftest.py:22  ] [ INFO] 定义行号: 13,所在模块: test_example3.py,测试函数: test_get_user
2026-01-01 16:13:41 [conftest.py:22  ] [ INFO] 定义行号: 27,所在模块: test_example3.py,测试函数: test_endpoint
2026-01-01 16:13:41 [conftest.py:22  ] [ INFO] 定义行号: 3,所在模块: test_example1.py,测试函数: test_user_registration
2026-01-01 16:13:41 [conftest.py:22  ] [ INFO] 定义行号: 7,所在模块: test_example2.py,测试函数: test_dynamic_marks
2026-01-01 16:13:41 [conftest.py:22  ] [ INFO] 定义行号: 15,所在模块: test_example2.py,测试函数: test_mark_method
```


## 方案4：使用 pytest 钩子函数

```python
# conftest.py
import pytest
import logging

def pytest_runtest_setup(item):
    """测试用例执行前的钩子"""
    log_test_start(item)

def pytest_runtest_teardown(item, nextitem):
    """测试用例执行后的钩子"""
    log_test_end(item)

def log_test_start(item):
    """记录测试开始信息"""
    # 获取各种格式的名称
    nodeid = item.nodeid  # 完整路径
    name = item.name      # 测试名
    location = f"{item.location[0]}:{item.location[1]}" if hasattr(item, 'location') else "unknown"
    
    # 获取测试类名
    class_name = None
    if hasattr(item, 'cls') and item.cls:
        class_name = item.cls.__name__
    
    # 构建显示名称
    if class_name:
        display_name = f"{class_name}.{name}"
    else:
        display_name = name
    
    logging.info(f"[开始] {display_name}")
    logging.info(f"[位置] {nodeid}")
    logging.info(f"[源码] {location}")

def log_test_end(item):
    """记录测试结束信息"""
    logging.info(f"[结束] {item.name}")
```

用例运行后，查看日志：

```shell
2026-01-01 16:15:48 [conftest.py:30  ] [ INFO] [开始] TestName.test_case01
2026-01-01 16:15:48 [conftest.py:31  ] [ INFO] [位置] test_examples.py::TestName::test_case01
2026-01-01 16:15:48 [conftest.py:32  ] [ INFO] [源码] test_examples.py:1
2026-01-01 16:15:48 [conftest.py:36  ] [ INFO] [结束] test_case01
2026-01-01 16:15:48 [conftest.py:30  ] [ INFO] [开始] test_case02
2026-01-01 16:15:48 [conftest.py:31  ] [ INFO] [位置] test_examples.py::test_case02
2026-01-01 16:15:48 [conftest.py:32  ] [ INFO] [源码] test_examples.py:5
2026-01-01 16:15:48 [conftest.py:36  ] [ INFO] [结束] test_case02
2026-01-01 16:15:48 [conftest.py:30  ] [ INFO] [开始] test_case03
2026-01-01 16:15:48 [conftest.py:31  ] [ INFO] [位置] test_examples.py::test_case03
2026-01-01 16:15:48 [conftest.py:32  ] [ INFO] [源码] test_examples.py:10
2026-01-01 16:15:48 [conftest.py:36  ] [ INFO] [结束] test_case03
2026-01-01 16:15:48 [conftest.py:30  ] [ INFO] [开始] TestUserAPI.test_create_user
2026-01-01 16:15:48 [conftest.py:31  ] [ INFO] [位置] testcases/feature1/test_example3.py::TestUserAPI::test_create_user
2026-01-01 16:15:48 [conftest.py:32  ] [ INFO] [源码] testcases\feature1\test_example3.py:7
2026-01-01 16:15:48 [conftest.py:36  ] [ INFO] [结束] test_create_user
2026-01-01 16:15:48 [conftest.py:30  ] [ INFO] [开始] TestUserAPI.test_get_user
2026-01-01 16:15:48 [conftest.py:31  ] [ INFO] [位置] testcases/feature1/test_example3.py::TestUserAPI::test_get_user
2026-01-01 16:15:48 [conftest.py:32  ] [ INFO] [源码] testcases\feature1\test_example3.py:12
2026-01-01 16:15:48 [conftest.py:36  ] [ INFO] [结束] test_get_user
2026-01-01 16:15:48 [conftest.py:30  ] [ INFO] [开始] test_endpoint
2026-01-01 16:15:48 [conftest.py:31  ] [ INFO] [位置] testcases/feature1/test_example3.py::test_endpoint
2026-01-01 16:15:48 [conftest.py:32  ] [ INFO] [源码] testcases\feature1\test_example3.py:26
2026-01-01 16:15:48 [conftest.py:36  ] [ INFO] [结束] test_endpoint
2026-01-01 16:15:48 [conftest.py:30  ] [ INFO] [开始] test_user_registration
2026-01-01 16:15:48 [conftest.py:31  ] [ INFO] [位置] testcases/test_example1.py::test_user_registration
2026-01-01 16:15:48 [conftest.py:32  ] [ INFO] [源码] testcases\test_example1.py:2
2026-01-01 16:15:48 [conftest.py:36  ] [ INFO] [结束] test_user_registration
2026-01-01 16:15:48 [conftest.py:30  ] [ INFO] [开始] test_dynamic_marks
2026-01-01 16:15:48 [conftest.py:31  ] [ INFO] [位置] testcases/test_example2.py::test_dynamic_marks
2026-01-01 16:15:48 [conftest.py:32  ] [ INFO] [源码] testcases\test_example2.py:6
2026-01-01 16:15:48 [conftest.py:36  ] [ INFO] [结束] test_dynamic_marks
2026-01-01 16:15:48 [conftest.py:30  ] [ INFO] [开始] test_mark_method
2026-01-01 16:15:48 [conftest.py:31  ] [ INFO] [位置] testcases/test_example2.py::test_mark_method
2026-01-01 16:15:48 [conftest.py:32  ] [ INFO] [源码] testcases\test_example2.py:14
2026-01-01 16:15:48 [conftest.py:36  ] [ INFO] [结束] test_mark_method
```


## 方案5：使用上下文管理器

```python
import pytest
import logging
from contextlib import contextmanager

@contextmanager
def test_case_context(request):
    """测试用例上下文管理器"""
    # 获取测试信息
    test_info = {
        'nodeid': request.node.nodeid,
        'name': request.node.name,
        'file': request.node.location[0] if hasattr(request.node, 'location') else 'unknown'
    }
    
    # 获取类信息
    if hasattr(request.node, 'cls') and request.node.cls:
        test_info['class'] = request.node.cls.__name__
    
    # 开始日志
    logging.info("=" * 60)
    logging.info(f"测试用例开始执行")
    logging.info(f"名称: {test_info['name']}")
    if 'class' in test_info:
        logging.info(f"类名: {test_info['class']}")
    logging.info(f"文件: {test_info['file']}")
    logging.info(f"完整路径: {test_info['nodeid']}")
    # logging.info("=" * 60)
    
    try:
        yield test_info
    finally:
        # 结束日志
        # logging.info("=" * 60)
        logging.info(f"测试用例执行完成: {test_info['name']}")
        # logging.info("=" * 60)

@pytest.fixture(scope='function', autouse=True)
def test_context(request):
    """使用上下文管理器记录测试信息"""
    with test_case_context(request):
        yield
```

用例运行后，查看日志：

```shell
2026-01-01 16:18:57 [conftest.py:20  ] [ INFO] ============================================================
2026-01-01 16:18:57 [conftest.py:21  ] [ INFO] 测试用例开始执行
2026-01-01 16:18:57 [conftest.py:22  ] [ INFO] 名称: test_case01
2026-01-01 16:18:57 [conftest.py:24  ] [ INFO] 类名: TestName
2026-01-01 16:18:57 [conftest.py:25  ] [ INFO] 文件: test_examples.py
2026-01-01 16:18:57 [conftest.py:26  ] [ INFO] 完整路径: test_examples.py::TestName::test_case01
2026-01-01 16:18:57 [conftest.py:34  ] [ INFO] 测试用例执行完成: test_case01
2026-01-01 16:18:57 [conftest.py:20  ] [ INFO] ============================================================
2026-01-01 16:18:57 [conftest.py:21  ] [ INFO] 测试用例开始执行
2026-01-01 16:18:57 [conftest.py:22  ] [ INFO] 名称: test_case02
2026-01-01 16:18:57 [conftest.py:25  ] [ INFO] 文件: test_examples.py
2026-01-01 16:18:57 [conftest.py:26  ] [ INFO] 完整路径: test_examples.py::test_case02
2026-01-01 16:18:57 [conftest.py:34  ] [ INFO] 测试用例执行完成: test_case02
2026-01-01 16:18:57 [conftest.py:20  ] [ INFO] ============================================================
2026-01-01 16:18:57 [conftest.py:21  ] [ INFO] 测试用例开始执行
2026-01-01 16:18:57 [conftest.py:22  ] [ INFO] 名称: test_case03
2026-01-01 16:18:57 [conftest.py:25  ] [ INFO] 文件: test_examples.py
2026-01-01 16:18:57 [conftest.py:26  ] [ INFO] 完整路径: test_examples.py::test_case03
2026-01-01 16:18:57 [conftest.py:34  ] [ INFO] 测试用例执行完成: test_case03
2026-01-01 16:18:57 [conftest.py:20  ] [ INFO] ============================================================
2026-01-01 16:18:57 [conftest.py:21  ] [ INFO] 测试用例开始执行
2026-01-01 16:18:57 [conftest.py:22  ] [ INFO] 名称: test_create_user
2026-01-01 16:18:57 [conftest.py:24  ] [ INFO] 类名: TestUserAPI
2026-01-01 16:18:57 [conftest.py:25  ] [ INFO] 文件: testcases\feature1\test_example3.py
2026-01-01 16:18:57 [conftest.py:26  ] [ INFO] 完整路径: testcases/feature1/test_example3.py::TestUserAPI::test_create_user
2026-01-01 16:18:57 [conftest.py:34  ] [ INFO] 测试用例执行完成: test_create_user
2026-01-01 16:18:57 [conftest.py:20  ] [ INFO] ============================================================
2026-01-01 16:18:57 [conftest.py:21  ] [ INFO] 测试用例开始执行
2026-01-01 16:18:57 [conftest.py:22  ] [ INFO] 名称: test_get_user
2026-01-01 16:18:57 [conftest.py:24  ] [ INFO] 类名: TestUserAPI
2026-01-01 16:18:57 [conftest.py:25  ] [ INFO] 文件: testcases\feature1\test_example3.py
2026-01-01 16:18:57 [conftest.py:26  ] [ INFO] 完整路径: testcases/feature1/test_example3.py::TestUserAPI::test_get_user
2026-01-01 16:18:57 [conftest.py:34  ] [ INFO] 测试用例执行完成: test_get_user
2026-01-01 16:18:57 [conftest.py:20  ] [ INFO] ============================================================
2026-01-01 16:18:57 [conftest.py:21  ] [ INFO] 测试用例开始执行
2026-01-01 16:18:57 [conftest.py:22  ] [ INFO] 名称: test_endpoint
2026-01-01 16:18:57 [conftest.py:25  ] [ INFO] 文件: testcases\feature1\test_example3.py
2026-01-01 16:18:57 [conftest.py:26  ] [ INFO] 完整路径: testcases/feature1/test_example3.py::test_endpoint
2026-01-01 16:18:57 [conftest.py:34  ] [ INFO] 测试用例执行完成: test_endpoint
2026-01-01 16:18:57 [conftest.py:20  ] [ INFO] ============================================================
2026-01-01 16:18:57 [conftest.py:21  ] [ INFO] 测试用例开始执行
2026-01-01 16:18:57 [conftest.py:22  ] [ INFO] 名称: test_user_registration
2026-01-01 16:18:57 [conftest.py:25  ] [ INFO] 文件: testcases\test_example1.py
2026-01-01 16:18:57 [conftest.py:26  ] [ INFO] 完整路径: testcases/test_example1.py::test_user_registration
2026-01-01 16:18:57 [conftest.py:34  ] [ INFO] 测试用例执行完成: test_user_registration
2026-01-01 16:18:57 [conftest.py:20  ] [ INFO] ============================================================
2026-01-01 16:18:57 [conftest.py:21  ] [ INFO] 测试用例开始执行
2026-01-01 16:18:57 [conftest.py:22  ] [ INFO] 名称: test_dynamic_marks
2026-01-01 16:18:57 [conftest.py:25  ] [ INFO] 文件: testcases\test_example2.py
2026-01-01 16:18:57 [conftest.py:26  ] [ INFO] 完整路径: testcases/test_example2.py::test_dynamic_marks
2026-01-01 16:18:57 [conftest.py:34  ] [ INFO] 测试用例执行完成: test_dynamic_marks
2026-01-01 16:18:57 [conftest.py:20  ] [ INFO] ============================================================
2026-01-01 16:18:57 [conftest.py:21  ] [ INFO] 测试用例开始执行
2026-01-01 16:18:57 [conftest.py:22  ] [ INFO] 名称: test_mark_method
2026-01-01 16:18:57 [conftest.py:25  ] [ INFO] 文件: testcases\test_example2.py
2026-01-01 16:18:57 [conftest.py:26  ] [ INFO] 完整路径: testcases/test_example2.py::test_mark_method
2026-01-01 16:18:57 [conftest.py:34  ] [ INFO] 测试用例执行完成: test_mark_method
```


## 方案6：使用装饰器模式

```python
# conftest.py
# conftest.py - 修复方案6
import pytest
import logging
import functools

def log_test_execution(request=None):
    """测试执行日志装饰器 - 工厂函数"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 从不同来源获取测试信息
            test_name = None
            test_nodeid = None
            
            # 如果传入了request参数
            if request:
                test_name = request.node.name
                test_nodeid = request.node.nodeid
            # 尝试从kwargs中获取request
            elif 'request' in kwargs:
                req = kwargs['request']
                test_name = req.node.name
                test_nodeid = req.node.nodeid
            else:
                test_name = func.__name__
                test_nodeid = "unknown"
            
            logging.info(f"执行测试: {test_name}")
            logging.info(f"测试路径: {test_nodeid}")
            
            try:
                result = func(*args, **kwargs)
                logging.info(f"测试完成: {test_name}")
                return result
            except Exception as e:
                logging.error(f"测试失败: {test_name}, 错误: {str(e)}")
                raise

        return wrapper
    return decorator

@pytest.fixture(scope='function', autouse=True)
def wrapped_test_execution(request):
    """包装测试执行的fixture - 修复版本"""
    # 方法1：直接记录日志，不使用装饰器包装
    test_name = request.node.name
    test_nodeid = request.node.nodeid

    logging.info(f"🔸 开始执行测试: {test_name}")
    logging.info(f"🔸 测试路径: {test_nodeid}")

    yield

    logging.info(f"🔸 测试完成: {test_name}")
```



用例运行后，查看日志：

```shell
2026-01-01 16:48:23 [conftest.py:49  ] [ INFO] 🔸 开始执行测试: test_case01
2026-01-01 16:48:23 [conftest.py:50  ] [ INFO] 🔸 测试路径: test_examples.py::TestName::test_case01
2026-01-01 16:48:23 [conftest.py:54  ] [ INFO] 🔸 测试完成: test_case01
2026-01-01 16:48:23 [conftest.py:49  ] [ INFO] 🔸 开始执行测试: test_case02
2026-01-01 16:48:23 [conftest.py:50  ] [ INFO] 🔸 测试路径: test_examples.py::test_case02
2026-01-01 16:48:23 [conftest.py:54  ] [ INFO] 🔸 测试完成: test_case02
2026-01-01 16:48:23 [conftest.py:49  ] [ INFO] 🔸 开始执行测试: test_case03
2026-01-01 16:48:23 [conftest.py:50  ] [ INFO] 🔸 测试路径: test_examples.py::test_case03
2026-01-01 16:48:23 [conftest.py:54  ] [ INFO] 🔸 测试完成: test_case03
2026-01-01 16:48:23 [conftest.py:49  ] [ INFO] 🔸 开始执行测试: test_create_user
2026-01-01 16:48:23 [conftest.py:50  ] [ INFO] 🔸 测试路径: testcases/feature1/test_example3.py::TestUserAPI::test_create_user
2026-01-01 16:48:23 [conftest.py:54  ] [ INFO] 🔸 测试完成: test_create_user
2026-01-01 16:48:23 [conftest.py:49  ] [ INFO] 🔸 开始执行测试: test_get_user
2026-01-01 16:48:23 [conftest.py:50  ] [ INFO] 🔸 测试路径: testcases/feature1/test_example3.py::TestUserAPI::test_get_user
2026-01-01 16:48:23 [conftest.py:54  ] [ INFO] 🔸 测试完成: test_get_user
2026-01-01 16:48:23 [conftest.py:49  ] [ INFO] 🔸 开始执行测试: test_endpoint
2026-01-01 16:48:23 [conftest.py:50  ] [ INFO] 🔸 测试路径: testcases/feature1/test_example3.py::test_endpoint
2026-01-01 16:48:23 [conftest.py:54  ] [ INFO] 🔸 测试完成: test_endpoint
2026-01-01 16:48:23 [conftest.py:49  ] [ INFO] 🔸 开始执行测试: test_user_registration
2026-01-01 16:48:23 [conftest.py:50  ] [ INFO] 🔸 测试路径: testcases/test_example1.py::test_user_registration
2026-01-01 16:48:23 [conftest.py:54  ] [ INFO] 🔸 测试完成: test_user_registration
2026-01-01 16:48:23 [conftest.py:49  ] [ INFO] 🔸 开始执行测试: test_dynamic_marks
2026-01-01 16:48:23 [conftest.py:50  ] [ INFO] 🔸 测试路径: testcases/test_example2.py::test_dynamic_marks
2026-01-01 16:48:23 [conftest.py:54  ] [ INFO] 🔸 测试完成: test_dynamic_marks
2026-01-01 16:48:23 [conftest.py:49  ] [ INFO] 🔸 开始执行测试: test_mark_method
2026-01-01 16:48:23 [conftest.py:50  ] [ INFO] 🔸 测试路径: testcases/test_example2.py::test_mark_method
2026-01-01 16:48:23 [conftest.py:54  ] [ INFO] 🔸 测试完成: test_mark_method
```


或者使用更简单的装饰器版本：

```python
# conftest.py
# 方案6的简化版本
import pytest
import logging

@pytest.fixture(scope='function', autouse=True)
def simple_test_logging(request):
    """简单的测试日志记录 - 替代方案6"""
    # 获取测试信息
    test_info = {
        'name': request.node.name,
        'nodeid': request.node.nodeid,
        'class': request.node.cls.__name__ if hasattr(request.node, 'cls') and request.node.cls else None
    }
    
    # 构建显示名称
    if test_info['class']:
        display_name = f"{test_info['class']}.{test_info['name']}"
    else:
        display_name = test_info['name']
    
    # 记录开始
    logging.info("▶" * 40)
    logging.info(f"测试开始: {display_name}")
    logging.info(f"完整路径: {test_info['nodeid']}")
    
    yield
    
    # 记录结束
    logging.info(f"测试完成: {display_name}")
    logging.info("◀" * 40)
    logging.info("")  # 空行分隔
```

用例运行后，查看日志：

```shell
2026-01-01 16:47:59 [conftest.py:22  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:47:59 [conftest.py:23  ] [ INFO] 测试开始: TestName.test_case01
2026-01-01 16:47:59 [conftest.py:24  ] [ INFO] 完整路径: test_examples.py::TestName::test_case01
2026-01-01 16:47:59 [conftest.py:29  ] [ INFO] 测试完成: TestName.test_case01
2026-01-01 16:47:59 [conftest.py:30  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:47:59 [conftest.py:31  ] [ INFO] 
2026-01-01 16:47:59 [conftest.py:22  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:47:59 [conftest.py:23  ] [ INFO] 测试开始: test_case02
2026-01-01 16:47:59 [conftest.py:24  ] [ INFO] 完整路径: test_examples.py::test_case02
2026-01-01 16:47:59 [conftest.py:29  ] [ INFO] 测试完成: test_case02
2026-01-01 16:47:59 [conftest.py:30  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:47:59 [conftest.py:31  ] [ INFO] 
2026-01-01 16:47:59 [conftest.py:22  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:47:59 [conftest.py:23  ] [ INFO] 测试开始: test_case03
2026-01-01 16:47:59 [conftest.py:24  ] [ INFO] 完整路径: test_examples.py::test_case03
2026-01-01 16:47:59 [conftest.py:29  ] [ INFO] 测试完成: test_case03
2026-01-01 16:47:59 [conftest.py:30  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:47:59 [conftest.py:31  ] [ INFO] 
2026-01-01 16:47:59 [conftest.py:22  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:47:59 [conftest.py:23  ] [ INFO] 测试开始: TestUserAPI.test_create_user
2026-01-01 16:47:59 [conftest.py:24  ] [ INFO] 完整路径: testcases/feature1/test_example3.py::TestUserAPI::test_create_user
2026-01-01 16:47:59 [conftest.py:29  ] [ INFO] 测试完成: TestUserAPI.test_create_user
2026-01-01 16:47:59 [conftest.py:30  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:47:59 [conftest.py:31  ] [ INFO] 
2026-01-01 16:47:59 [conftest.py:22  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:47:59 [conftest.py:23  ] [ INFO] 测试开始: TestUserAPI.test_get_user
2026-01-01 16:47:59 [conftest.py:24  ] [ INFO] 完整路径: testcases/feature1/test_example3.py::TestUserAPI::test_get_user
2026-01-01 16:47:59 [conftest.py:29  ] [ INFO] 测试完成: TestUserAPI.test_get_user
2026-01-01 16:47:59 [conftest.py:30  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:47:59 [conftest.py:31  ] [ INFO] 
2026-01-01 16:47:59 [conftest.py:22  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:47:59 [conftest.py:23  ] [ INFO] 测试开始: test_endpoint
2026-01-01 16:47:59 [conftest.py:24  ] [ INFO] 完整路径: testcases/feature1/test_example3.py::test_endpoint
2026-01-01 16:47:59 [conftest.py:29  ] [ INFO] 测试完成: test_endpoint
2026-01-01 16:47:59 [conftest.py:30  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:47:59 [conftest.py:31  ] [ INFO] 
2026-01-01 16:47:59 [conftest.py:22  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:47:59 [conftest.py:23  ] [ INFO] 测试开始: test_user_registration
2026-01-01 16:47:59 [conftest.py:24  ] [ INFO] 完整路径: testcases/test_example1.py::test_user_registration
2026-01-01 16:47:59 [conftest.py:29  ] [ INFO] 测试完成: test_user_registration
2026-01-01 16:47:59 [conftest.py:30  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:47:59 [conftest.py:31  ] [ INFO] 
2026-01-01 16:47:59 [conftest.py:22  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:47:59 [conftest.py:23  ] [ INFO] 测试开始: test_dynamic_marks
2026-01-01 16:47:59 [conftest.py:24  ] [ INFO] 完整路径: testcases/test_example2.py::test_dynamic_marks
2026-01-01 16:47:59 [conftest.py:29  ] [ INFO] 测试完成: test_dynamic_marks
2026-01-01 16:47:59 [conftest.py:30  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:47:59 [conftest.py:31  ] [ INFO] 
2026-01-01 16:47:59 [conftest.py:22  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:47:59 [conftest.py:23  ] [ INFO] 测试开始: test_mark_method
2026-01-01 16:47:59 [conftest.py:24  ] [ INFO] 完整路径: testcases/test_example2.py::test_mark_method
2026-01-01 16:47:59 [conftest.py:29  ] [ INFO] 测试完成: test_mark_method
2026-01-01 16:47:59 [conftest.py:30  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:47:59 [conftest.py:31  ] [ INFO] 
```

## 方案7：使用配置文件的自定义格式

```python
# conftest.py
import pytest
import logging

@pytest.fixture(scope='function', autouse=True)
def configure_test_logging(request):
    """配置测试日志格式"""
    # 获取测试信息
    test_info = {
        'test_name': request.node.name,
        'test_class': request.node.cls.__name__ if hasattr(request.node, 'cls') and request.node.cls else '',
        'test_file': request.node.location[0] if hasattr(request.node, 'location') else 'unknown',
        'test_line': request.node.location[1] if hasattr(request.node, 'location') else 0,
        'test_nodeid': request.node.nodeid
    }
    
    # 创建自定义日志记录器
    logger = logging.getLogger(f"test.{test_info['test_name']}")
    
    # 添加自定义处理器
    class TestInfoFilter(logging.Filter):
        def filter(self, record):
            for key, value in test_info.items():
                setattr(record, key, value)
            return True
    
    # 为当前logger添加过滤器
    for handler in logger.handlers:
        handler.addFilter(TestInfoFilter())
    
    # 记录开始信息
    logger.info("测试开始执行： %s", test_info)
    
    yield
    
    # 记录结束信息
    logger.info("测试执行完成")
```

用例运行后，查看日志：

```shell
2026-01-01 16:29:02 [conftest.py:31  ] [ INFO] 测试开始执行： {'test_name': 'test_case01', 'test_class': 'TestName', 'test_file': 'test_examples.py', 'test_line': 1, 'test_nodeid': 'test_examples.py::TestName::test_case01'}
2026-01-01 16:29:02 [conftest.py:36  ] [ INFO] 测试执行完成
2026-01-01 16:29:02 [conftest.py:31  ] [ INFO] 测试开始执行： {'test_name': 'test_case02', 'test_class': '', 'test_file': 'test_examples.py', 'test_line': 5, 'test_nodeid': 'test_examples.py::test_case02'}
2026-01-01 16:29:02 [conftest.py:36  ] [ INFO] 测试执行完成
2026-01-01 16:29:02 [conftest.py:31  ] [ INFO] 测试开始执行： {'test_name': 'test_case03', 'test_class': '', 'test_file': 'test_examples.py', 'test_line': 10, 'test_nodeid': 'test_examples.py::test_case03'}
2026-01-01 16:29:02 [conftest.py:36  ] [ INFO] 测试执行完成
2026-01-01 16:29:02 [conftest.py:31  ] [ INFO] 测试开始执行： {'test_name': 'test_create_user', 'test_class': 'TestUserAPI', 'test_file': 'testcases\\feature1\\test_example3.py', 'test_line': 7, 'test_nodeid': 'testcases/feature1/test_example3.py::TestUserAPI::test_create_user'}
2026-01-01 16:29:02 [conftest.py:36  ] [ INFO] 测试执行完成
2026-01-01 16:29:02 [conftest.py:31  ] [ INFO] 测试开始执行： {'test_name': 'test_get_user', 'test_class': 'TestUserAPI', 'test_file': 'testcases\\feature1\\test_example3.py', 'test_line': 12, 'test_nodeid': 'testcases/feature1/test_example3.py::TestUserAPI::test_get_user'}
2026-01-01 16:29:02 [conftest.py:36  ] [ INFO] 测试执行完成
2026-01-01 16:29:02 [conftest.py:31  ] [ INFO] 测试开始执行： {'test_name': 'test_endpoint', 'test_class': '', 'test_file': 'testcases\\feature1\\test_example3.py', 'test_line': 26, 'test_nodeid': 'testcases/feature1/test_example3.py::test_endpoint'}
2026-01-01 16:29:02 [conftest.py:36  ] [ INFO] 测试执行完成
2026-01-01 16:29:02 [conftest.py:31  ] [ INFO] 测试开始执行： {'test_name': 'test_user_registration', 'test_class': '', 'test_file': 'testcases\\test_example1.py', 'test_line': 2, 'test_nodeid': 'testcases/test_example1.py::test_user_registration'}
2026-01-01 16:29:02 [conftest.py:36  ] [ INFO] 测试执行完成
2026-01-01 16:29:02 [conftest.py:31  ] [ INFO] 测试开始执行： {'test_name': 'test_dynamic_marks', 'test_class': '', 'test_file': 'testcases\\test_example2.py', 'test_line': 6, 'test_nodeid': 'testcases/test_example2.py::test_dynamic_marks'}
2026-01-01 16:29:02 [conftest.py:36  ] [ INFO] 测试执行完成
2026-01-01 16:29:02 [conftest.py:31  ] [ INFO] 测试开始执行： {'test_name': 'test_mark_method', 'test_class': '', 'test_file': 'testcases\\test_example2.py', 'test_line': 14, 'test_nodeid': 'testcases/test_example2.py::test_mark_method'}
2026-01-01 16:29:02 [conftest.py:36  ] [ INFO] 测试执行完成
```



## 优化后的推荐方案（综合多种方法）

### 使用相同宽度的字符

```python
# conftest.py
import pytest
import logging
import os

@pytest.fixture(scope='function', autouse=True)
def comprehensive_test_logging(request):
    """综合测试日志记录 - 修复对齐问题"""
    # 1. 获取基本测试信息
    test_node = request.node
    
    # 2. 构建测试标识信息
    test_info = {
        'nodeid': test_node.nodeid,
        'name': test_node.name,
        'original_name': getattr(test_node, 'originalname', test_node.name),
        'file': test_node.location[0] if hasattr(test_node, 'location') else 'unknown',
        'line': test_node.location[1] if hasattr(test_node, 'location') else 0,
        'class': test_node.cls.__name__ if hasattr(test_node, 'cls') and test_node.cls else None
    }
    
    # 3. 构建显示名称
    if test_info['class']:
        display_name = f"{test_info['class']}.{test_info['name']}"
    else:
        display_name = test_info['name']
    
    # 4. 获取相对路径
    current_dir = os.getcwd()
    if test_info['file'].startswith(current_dir):
        relative_file = os.path.relpath(test_info['file'], current_dir)
    else:
        relative_file = test_info['file']
    
    # 5. 使用等宽字符确保对齐
    separator_char = "="  # 使用等宽ASCII字符
    separator_length = 60
    half_length = (separator_length - len(" 测试开始 ")) // 2
    
    # 6. 记录开始日志
    logging.info(separator_char * half_length + " 测试开始 " + separator_char * half_length)
    logging.info(f"📋 测试用例: {display_name}")
    logging.info(f"📍 位置: {relative_file}:{test_info['line']}")
    logging.info(f"🔗 完整路径: {test_info['nodeid']}")
    
    yield
    
    # 7. 记录结束日志（使用相同的分隔符字符和长度）
    logging.info(separator_char * half_length + " 测试完成 " + separator_char * half_length)
    logging.info(f"✅ 测试完成: {display_name}\n")
```

查看运行日志：

```shell
2026-01-01 16:50:27 [conftest.py:41  ] [ INFO] =========================== 测试开始 ===========================
2026-01-01 16:50:27 [conftest.py:42  ] [ INFO] 📋 测试用例: TestName.test_case01
2026-01-01 16:50:27 [conftest.py:43  ] [ INFO] 📍 位置: test_examples.py:1
2026-01-01 16:50:27 [conftest.py:44  ] [ INFO] 🔗 完整路径: test_examples.py::TestName::test_case01
2026-01-01 16:50:27 [conftest.py:49  ] [ INFO] =========================== 测试完成 ===========================
2026-01-01 16:50:27 [conftest.py:50  ] [ INFO] ✅ 测试完成: TestName.test_case01

2026-01-01 16:50:27 [conftest.py:41  ] [ INFO] =========================== 测试开始 ===========================
2026-01-01 16:50:27 [conftest.py:42  ] [ INFO] 📋 测试用例: test_case02
2026-01-01 16:50:27 [conftest.py:43  ] [ INFO] 📍 位置: test_examples.py:5
2026-01-01 16:50:27 [conftest.py:44  ] [ INFO] 🔗 完整路径: test_examples.py::test_case02
2026-01-01 16:50:27 [conftest.py:49  ] [ INFO] =========================== 测试完成 ===========================
2026-01-01 16:50:27 [conftest.py:50  ] [ INFO] ✅ 测试完成: test_case02

2026-01-01 16:50:27 [conftest.py:41  ] [ INFO] =========================== 测试开始 ===========================
2026-01-01 16:50:27 [conftest.py:42  ] [ INFO] 📋 测试用例: test_case03
2026-01-01 16:50:27 [conftest.py:43  ] [ INFO] 📍 位置: test_examples.py:10
2026-01-01 16:50:27 [conftest.py:44  ] [ INFO] 🔗 完整路径: test_examples.py::test_case03
2026-01-01 16:50:27 [conftest.py:49  ] [ INFO] =========================== 测试完成 ===========================
2026-01-01 16:50:27 [conftest.py:50  ] [ INFO] ✅ 测试完成: test_case03

2026-01-01 16:50:27 [conftest.py:41  ] [ INFO] =========================== 测试开始 ===========================
2026-01-01 16:50:27 [conftest.py:42  ] [ INFO] 📋 测试用例: TestUserAPI.test_create_user
2026-01-01 16:50:27 [conftest.py:43  ] [ INFO] 📍 位置: testcases\feature1\test_example3.py:7
2026-01-01 16:50:27 [conftest.py:44  ] [ INFO] 🔗 完整路径: testcases/feature1/test_example3.py::TestUserAPI::test_create_user
2026-01-01 16:50:27 [conftest.py:49  ] [ INFO] =========================== 测试完成 ===========================
2026-01-01 16:50:27 [conftest.py:50  ] [ INFO] ✅ 测试完成: TestUserAPI.test_create_user

2026-01-01 16:50:27 [conftest.py:41  ] [ INFO] =========================== 测试开始 ===========================
2026-01-01 16:50:27 [conftest.py:42  ] [ INFO] 📋 测试用例: TestUserAPI.test_get_user
2026-01-01 16:50:27 [conftest.py:43  ] [ INFO] 📍 位置: testcases\feature1\test_example3.py:12
2026-01-01 16:50:27 [conftest.py:44  ] [ INFO] 🔗 完整路径: testcases/feature1/test_example3.py::TestUserAPI::test_get_user
2026-01-01 16:50:27 [conftest.py:49  ] [ INFO] =========================== 测试完成 ===========================
2026-01-01 16:50:27 [conftest.py:50  ] [ INFO] ✅ 测试完成: TestUserAPI.test_get_user

2026-01-01 16:50:27 [conftest.py:41  ] [ INFO] =========================== 测试开始 ===========================
2026-01-01 16:50:27 [conftest.py:42  ] [ INFO] 📋 测试用例: test_endpoint
2026-01-01 16:50:27 [conftest.py:43  ] [ INFO] 📍 位置: testcases\feature1\test_example3.py:26
2026-01-01 16:50:27 [conftest.py:44  ] [ INFO] 🔗 完整路径: testcases/feature1/test_example3.py::test_endpoint
2026-01-01 16:50:27 [conftest.py:49  ] [ INFO] =========================== 测试完成 ===========================
2026-01-01 16:50:27 [conftest.py:50  ] [ INFO] ✅ 测试完成: test_endpoint

2026-01-01 16:50:27 [conftest.py:41  ] [ INFO] =========================== 测试开始 ===========================
2026-01-01 16:50:27 [conftest.py:42  ] [ INFO] 📋 测试用例: test_user_registration
2026-01-01 16:50:27 [conftest.py:43  ] [ INFO] 📍 位置: testcases\test_example1.py:2
2026-01-01 16:50:27 [conftest.py:44  ] [ INFO] 🔗 完整路径: testcases/test_example1.py::test_user_registration
2026-01-01 16:50:27 [conftest.py:49  ] [ INFO] =========================== 测试完成 ===========================
2026-01-01 16:50:27 [conftest.py:50  ] [ INFO] ✅ 测试完成: test_user_registration

2026-01-01 16:50:27 [conftest.py:41  ] [ INFO] =========================== 测试开始 ===========================
2026-01-01 16:50:27 [conftest.py:42  ] [ INFO] 📋 测试用例: test_dynamic_marks
2026-01-01 16:50:27 [conftest.py:43  ] [ INFO] 📍 位置: testcases\test_example2.py:6
2026-01-01 16:50:27 [conftest.py:44  ] [ INFO] 🔗 完整路径: testcases/test_example2.py::test_dynamic_marks
2026-01-01 16:50:27 [conftest.py:49  ] [ INFO] =========================== 测试完成 ===========================
2026-01-01 16:50:27 [conftest.py:50  ] [ INFO] ✅ 测试完成: test_dynamic_marks

2026-01-01 16:50:27 [conftest.py:41  ] [ INFO] =========================== 测试开始 ===========================
2026-01-01 16:50:27 [conftest.py:42  ] [ INFO] 📋 测试用例: test_mark_method
2026-01-01 16:50:27 [conftest.py:43  ] [ INFO] 📍 位置: testcases\test_example2.py:14
2026-01-01 16:50:27 [conftest.py:44  ] [ INFO] 🔗 完整路径: testcases/test_example2.py::test_mark_method
2026-01-01 16:50:27 [conftest.py:49  ] [ INFO] =========================== 测试完成 ===========================
2026-01-01 16:50:27 [conftest.py:50  ] [ INFO] ✅ 测试完成: test_mark_method
```


### 使用计算宽度确保对齐

```python
# conftest.py
# conftest.py - 修复对齐问题版本2（智能计算）
import pytest
import logging
import os

def create_separator(text, total_width=80, char="="):
    """创建带文本的分隔线，确保居中"""
    text_with_spaces = f" {text} "
    available_width = total_width - len(text_with_spaces)
    left_width = available_width // 2
    right_width = available_width - left_width
    
    return f"{char * left_width}{text_with_spaces}{char * right_width}"

@pytest.fixture(scope='function', autouse=True)
def smart_test_logging(request):
    """智能测试日志记录 - 自动对齐"""
    # 获取测试信息
    test_node = request.node
    
    # 构建显示名称
    class_name = test_node.cls.__name__ if hasattr(test_node, 'cls') and test_node.cls else None
    if class_name:
        display_name = f"{class_name}.{test_node.name}"
    else:
        display_name = test_node.name
    
    # 获取相对文件路径
    test_file = test_node.location[0] if hasattr(test_node, 'location') else 'unknown'
    current_dir = os.getcwd()
    if test_file.startswith(current_dir):
        relative_file = os.path.relpath(test_file, current_dir)
    else:
        relative_file = test_file
    
    # 使用ASCII字符确保等宽
    separator_char = "="  # ASCII字符，等宽
    
    # 记录开始
    logging.info(create_separator("测试开始", 80, separator_char))
    logging.info(f"测试用例: {display_name}")
    logging.info(f"文件位置: {relative_file}:{test_node.location[1] if hasattr(test_node, 'location') else 0}")
    logging.info(f"节点标识: {test_node.nodeid}")
    
    yield
    
    # 记录结束
    logging.info(create_separator("测试完成", 80, separator_char))
    logging.info(f"执行状态: 完成 - {display_name}")
    logging.info("")
```

运行后查看日志：

```shell
2026-01-01 16:54:04 [conftest.py:40  ] [ INFO] ===================================== 测试开始 =====================================
2026-01-01 16:54:04 [conftest.py:41  ] [ INFO] 测试用例: TestName.test_case01
2026-01-01 16:54:04 [conftest.py:42  ] [ INFO] 文件位置: test_examples.py:1
2026-01-01 16:54:04 [conftest.py:43  ] [ INFO] 节点标识: test_examples.py::TestName::test_case01
2026-01-01 16:54:04 [conftest.py:48  ] [ INFO] ===================================== 测试完成 =====================================
2026-01-01 16:54:04 [conftest.py:49  ] [ INFO] 执行状态: 完成 - TestName.test_case01

2026-01-01 16:54:04 [conftest.py:40  ] [ INFO] ===================================== 测试开始 =====================================
2026-01-01 16:54:04 [conftest.py:41  ] [ INFO] 测试用例: test_case02
2026-01-01 16:54:04 [conftest.py:42  ] [ INFO] 文件位置: test_examples.py:5
2026-01-01 16:54:04 [conftest.py:43  ] [ INFO] 节点标识: test_examples.py::test_case02
2026-01-01 16:54:04 [conftest.py:48  ] [ INFO] ===================================== 测试完成 =====================================
2026-01-01 16:54:04 [conftest.py:49  ] [ INFO] 执行状态: 完成 - test_case02

2026-01-01 16:54:04 [conftest.py:40  ] [ INFO] ===================================== 测试开始 =====================================
2026-01-01 16:54:04 [conftest.py:41  ] [ INFO] 测试用例: test_case03
2026-01-01 16:54:04 [conftest.py:42  ] [ INFO] 文件位置: test_examples.py:10
2026-01-01 16:54:04 [conftest.py:43  ] [ INFO] 节点标识: test_examples.py::test_case03
2026-01-01 16:54:04 [conftest.py:48  ] [ INFO] ===================================== 测试完成 =====================================
2026-01-01 16:54:04 [conftest.py:49  ] [ INFO] 执行状态: 完成 - test_case03

2026-01-01 16:54:04 [conftest.py:40  ] [ INFO] ===================================== 测试开始 =====================================
2026-01-01 16:54:04 [conftest.py:41  ] [ INFO] 测试用例: TestUserAPI.test_create_user
2026-01-01 16:54:04 [conftest.py:42  ] [ INFO] 文件位置: testcases\feature1\test_example3.py:7
2026-01-01 16:54:04 [conftest.py:43  ] [ INFO] 节点标识: testcases/feature1/test_example3.py::TestUserAPI::test_create_user
2026-01-01 16:54:04 [conftest.py:48  ] [ INFO] ===================================== 测试完成 =====================================
2026-01-01 16:54:04 [conftest.py:49  ] [ INFO] 执行状态: 完成 - TestUserAPI.test_create_user

2026-01-01 16:54:04 [conftest.py:40  ] [ INFO] ===================================== 测试开始 =====================================
2026-01-01 16:54:04 [conftest.py:41  ] [ INFO] 测试用例: TestUserAPI.test_get_user
2026-01-01 16:54:04 [conftest.py:42  ] [ INFO] 文件位置: testcases\feature1\test_example3.py:12
2026-01-01 16:54:04 [conftest.py:43  ] [ INFO] 节点标识: testcases/feature1/test_example3.py::TestUserAPI::test_get_user
2026-01-01 16:54:04 [conftest.py:48  ] [ INFO] ===================================== 测试完成 =====================================
2026-01-01 16:54:04 [conftest.py:49  ] [ INFO] 执行状态: 完成 - TestUserAPI.test_get_user

2026-01-01 16:54:04 [conftest.py:40  ] [ INFO] ===================================== 测试开始 =====================================
2026-01-01 16:54:04 [conftest.py:41  ] [ INFO] 测试用例: test_endpoint
2026-01-01 16:54:04 [conftest.py:42  ] [ INFO] 文件位置: testcases\feature1\test_example3.py:26
2026-01-01 16:54:04 [conftest.py:43  ] [ INFO] 节点标识: testcases/feature1/test_example3.py::test_endpoint
2026-01-01 16:54:04 [conftest.py:48  ] [ INFO] ===================================== 测试完成 =====================================
2026-01-01 16:54:04 [conftest.py:49  ] [ INFO] 执行状态: 完成 - test_endpoint

2026-01-01 16:54:04 [conftest.py:40  ] [ INFO] ===================================== 测试开始 =====================================
2026-01-01 16:54:04 [conftest.py:41  ] [ INFO] 测试用例: test_user_registration
2026-01-01 16:54:04 [conftest.py:42  ] [ INFO] 文件位置: testcases\test_example1.py:2
2026-01-01 16:54:04 [conftest.py:43  ] [ INFO] 节点标识: testcases/test_example1.py::test_user_registration
2026-01-01 16:54:04 [conftest.py:48  ] [ INFO] ===================================== 测试完成 =====================================
2026-01-01 16:54:04 [conftest.py:49  ] [ INFO] 执行状态: 完成 - test_user_registration

2026-01-01 16:54:04 [conftest.py:40  ] [ INFO] ===================================== 测试开始 =====================================
2026-01-01 16:54:04 [conftest.py:41  ] [ INFO] 测试用例: test_dynamic_marks
2026-01-01 16:54:04 [conftest.py:42  ] [ INFO] 文件位置: testcases\test_example2.py:6
2026-01-01 16:54:04 [conftest.py:43  ] [ INFO] 节点标识: testcases/test_example2.py::test_dynamic_marks
2026-01-01 16:54:04 [conftest.py:48  ] [ INFO] ===================================== 测试完成 =====================================
2026-01-01 16:54:04 [conftest.py:49  ] [ INFO] 执行状态: 完成 - test_dynamic_marks

2026-01-01 16:54:04 [conftest.py:40  ] [ INFO] ===================================== 测试开始 =====================================
2026-01-01 16:54:04 [conftest.py:41  ] [ INFO] 测试用例: test_mark_method
2026-01-01 16:54:04 [conftest.py:42  ] [ INFO] 文件位置: testcases\test_example2.py:14
2026-01-01 16:54:04 [conftest.py:43  ] [ INFO] 节点标识: testcases/test_example2.py::test_mark_method
2026-01-01 16:54:04 [conftest.py:48  ] [ INFO] ===================================== 测试完成 =====================================
2026-01-01 16:54:04 [conftest.py:49  ] [ INFO] 执行状态: 完成 - test_mark_method
```


### 使用Unicode等宽字符

```python
# conftest.py
# conftest.py - 修复对齐问题版本3（使用等宽Unicode字符）
import pytest
import logging
import os

@pytest.fixture(scope='function', autouse=True)
def aligned_test_logging(request):
    """对齐的测试日志记录 - 使用等宽Unicode字符"""
    test_node = request.node
    
    # 显示名称
    class_name = test_node.cls.__name__ if hasattr(test_node, 'cls') and test_node.cls else None
    display_name = f"{class_name}.{test_node.name}" if class_name else test_node.name
    
    # 文件路径
    test_file = test_node.location[0] if hasattr(test_node, 'location') else 'unknown'
    current_dir = os.getcwd()
    relative_file = os.path.relpath(test_file, current_dir) if test_file.startswith(current_dir) else test_file
    
    # 使用等宽Unicode字符（这些字符在大多数终端中等宽）
    start_char = "▶"  # 或使用 "▷" 也是等宽的
    end_char = "◀"    # 或使用 "◁" 也是等宽的
    
    # 或者使用ASCII艺术字符
    # start_char = ">"  # ASCII字符，确保等宽
    # end_char = "<"    # ASCII字符，确保等宽
    
    separator_length = 60
    text_length = len(" 测试开始 ")
    side_length = (separator_length - text_length) // 2
    
    # 开始日志
    logging.info(start_char * side_length + " 测试开始 " + start_char * side_length)
    logging.info(f"📋 测试用例: {display_name}")
    logging.info(f"📍 位置: {relative_file}:{test_node.location[1] if hasattr(test_node, 'location') else 0}")
    logging.info(f"🔗 完整路径: {test_node.nodeid}")
    
    yield
    
    # 结束日志 - 使用相同数量的字符确保对齐
    logging.info(end_char * side_length + " 测试完成 " + end_char * side_length)
    logging.info(f"✅ 测试完成: {display_name}\n")
```

运行后查看日志：

```shell
2026-01-01 16:54:59 [conftest.py:33  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶ 测试开始 ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:54:59 [conftest.py:34  ] [ INFO] 📋 测试用例: TestName.test_case01
2026-01-01 16:54:59 [conftest.py:35  ] [ INFO] 📍 位置: test_examples.py:1
2026-01-01 16:54:59 [conftest.py:36  ] [ INFO] 🔗 完整路径: test_examples.py::TestName::test_case01
2026-01-01 16:54:59 [conftest.py:41  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀ 测试完成 ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:54:59 [conftest.py:42  ] [ INFO] ✅ 测试完成: TestName.test_case01

2026-01-01 16:54:59 [conftest.py:33  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶ 测试开始 ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:54:59 [conftest.py:34  ] [ INFO] 📋 测试用例: test_case02
2026-01-01 16:54:59 [conftest.py:35  ] [ INFO] 📍 位置: test_examples.py:5
2026-01-01 16:54:59 [conftest.py:36  ] [ INFO] 🔗 完整路径: test_examples.py::test_case02
2026-01-01 16:54:59 [conftest.py:41  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀ 测试完成 ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:54:59 [conftest.py:42  ] [ INFO] ✅ 测试完成: test_case02

2026-01-01 16:54:59 [conftest.py:33  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶ 测试开始 ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:54:59 [conftest.py:34  ] [ INFO] 📋 测试用例: test_case03
2026-01-01 16:54:59 [conftest.py:35  ] [ INFO] 📍 位置: test_examples.py:10
2026-01-01 16:54:59 [conftest.py:36  ] [ INFO] 🔗 完整路径: test_examples.py::test_case03
2026-01-01 16:54:59 [conftest.py:41  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀ 测试完成 ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:54:59 [conftest.py:42  ] [ INFO] ✅ 测试完成: test_case03

2026-01-01 16:54:59 [conftest.py:33  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶ 测试开始 ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:54:59 [conftest.py:34  ] [ INFO] 📋 测试用例: TestUserAPI.test_create_user
2026-01-01 16:54:59 [conftest.py:35  ] [ INFO] 📍 位置: testcases\feature1\test_example3.py:7
2026-01-01 16:54:59 [conftest.py:36  ] [ INFO] 🔗 完整路径: testcases/feature1/test_example3.py::TestUserAPI::test_create_user
2026-01-01 16:54:59 [conftest.py:41  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀ 测试完成 ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:54:59 [conftest.py:42  ] [ INFO] ✅ 测试完成: TestUserAPI.test_create_user

2026-01-01 16:54:59 [conftest.py:33  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶ 测试开始 ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:54:59 [conftest.py:34  ] [ INFO] 📋 测试用例: TestUserAPI.test_get_user
2026-01-01 16:54:59 [conftest.py:35  ] [ INFO] 📍 位置: testcases\feature1\test_example3.py:12
2026-01-01 16:54:59 [conftest.py:36  ] [ INFO] 🔗 完整路径: testcases/feature1/test_example3.py::TestUserAPI::test_get_user
2026-01-01 16:54:59 [conftest.py:41  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀ 测试完成 ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:54:59 [conftest.py:42  ] [ INFO] ✅ 测试完成: TestUserAPI.test_get_user

2026-01-01 16:54:59 [conftest.py:33  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶ 测试开始 ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:54:59 [conftest.py:34  ] [ INFO] 📋 测试用例: test_endpoint
2026-01-01 16:54:59 [conftest.py:35  ] [ INFO] 📍 位置: testcases\feature1\test_example3.py:26
2026-01-01 16:54:59 [conftest.py:36  ] [ INFO] 🔗 完整路径: testcases/feature1/test_example3.py::test_endpoint
2026-01-01 16:54:59 [conftest.py:41  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀ 测试完成 ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:54:59 [conftest.py:42  ] [ INFO] ✅ 测试完成: test_endpoint

2026-01-01 16:54:59 [conftest.py:33  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶ 测试开始 ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:54:59 [conftest.py:34  ] [ INFO] 📋 测试用例: test_user_registration
2026-01-01 16:54:59 [conftest.py:35  ] [ INFO] 📍 位置: testcases\test_example1.py:2
2026-01-01 16:54:59 [conftest.py:36  ] [ INFO] 🔗 完整路径: testcases/test_example1.py::test_user_registration
2026-01-01 16:54:59 [conftest.py:41  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀ 测试完成 ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:54:59 [conftest.py:42  ] [ INFO] ✅ 测试完成: test_user_registration

2026-01-01 16:54:59 [conftest.py:33  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶ 测试开始 ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:54:59 [conftest.py:34  ] [ INFO] 📋 测试用例: test_dynamic_marks
2026-01-01 16:54:59 [conftest.py:35  ] [ INFO] 📍 位置: testcases\test_example2.py:6
2026-01-01 16:54:59 [conftest.py:36  ] [ INFO] 🔗 完整路径: testcases/test_example2.py::test_dynamic_marks
2026-01-01 16:54:59 [conftest.py:41  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀ 测试完成 ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:54:59 [conftest.py:42  ] [ INFO] ✅ 测试完成: test_dynamic_marks

2026-01-01 16:54:59 [conftest.py:33  ] [ INFO] ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶ 测试开始 ▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶
2026-01-01 16:54:59 [conftest.py:34  ] [ INFO] 📋 测试用例: test_mark_method
2026-01-01 16:54:59 [conftest.py:35  ] [ INFO] 📍 位置: testcases\test_example2.py:14
2026-01-01 16:54:59 [conftest.py:36  ] [ INFO] 🔗 完整路径: testcases/test_example2.py::test_mark_method
2026-01-01 16:54:59 [conftest.py:41  ] [ INFO] ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀ 测试完成 ◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀◀
2026-01-01 16:54:59 [conftest.py:42  ] [ INFO] ✅ 测试完成: test_mark_method
```


### 使用格式化的最佳实践

```python
# conftest.py
# conftest.py - 最终推荐版本
import pytest
import logging
import os

@pytest.fixture(scope='function', autouse=True)
def best_practice_test_logging(request):
    """最佳实践的测试日志记录"""
    test_node = request.node
    
    # 构建测试信息
    test_info = {
        'name': test_node.name,
        'class': test_node.cls.__name__ if hasattr(test_node, 'cls') and test_node.cls else None,
        'nodeid': test_node.nodeid,
        'file': test_node.location[0] if hasattr(test_node, 'location') else 'unknown',
        'line': test_node.location[1] if hasattr(test_node, 'location') else 0,
    }
    
    # 显示名称
    if test_info['class']:
        display_name = f"{test_info['class']}.{test_info['name']}"
    else:
        display_name = test_info['name']
    
    # 相对路径
    current_dir = os.getcwd()
    if test_info['file'].startswith(current_dir):
        relative_file = os.path.relpath(test_info['file'], current_dir)
    else:
        relative_file = test_info['file']
    
    # 使用简单的分隔符（避免对齐问题）
    separator = "=" * 70
    
    # 开始执行
    logging.info(separator)
    logging.info(f"🚀 开始测试: {display_name}")
    logging.info(f"📁 文件: {relative_file}")
    logging.info(f"📍 行号: {test_info['line']}")
    logging.info(f"🔗 节点: {test_info['nodeid']}")
    logging.info("-" * 40)
    
    yield
    
    # 执行完成
    logging.info("-" * 40)
    logging.info(f"✅ 测试完成: {display_name}")
    logging.info(f"⏱️  状态: 通过")
    logging.info(separator)
    logging.info("")  # 空行分隔
```

运行后查看日志：

```shell
2026-01-01 16:55:35 [conftest.py:37  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:38  ] [ INFO] 🚀 开始测试: TestName.test_case01
2026-01-01 16:55:35 [conftest.py:39  ] [ INFO] 📁 文件: test_examples.py
2026-01-01 16:55:35 [conftest.py:40  ] [ INFO] 📍 行号: 1
2026-01-01 16:55:35 [conftest.py:41  ] [ INFO] 🔗 节点: test_examples.py::TestName::test_case01
2026-01-01 16:55:35 [conftest.py:42  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:47  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:48  ] [ INFO] ✅ 测试完成: TestName.test_case01
2026-01-01 16:55:35 [conftest.py:49  ] [ INFO] ⏱️  状态: 通过
2026-01-01 16:55:35 [conftest.py:50  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:51  ] [ INFO] 
2026-01-01 16:55:35 [conftest.py:37  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:38  ] [ INFO] 🚀 开始测试: test_case02
2026-01-01 16:55:35 [conftest.py:39  ] [ INFO] 📁 文件: test_examples.py
2026-01-01 16:55:35 [conftest.py:40  ] [ INFO] 📍 行号: 5
2026-01-01 16:55:35 [conftest.py:41  ] [ INFO] 🔗 节点: test_examples.py::test_case02
2026-01-01 16:55:35 [conftest.py:42  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:47  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:48  ] [ INFO] ✅ 测试完成: test_case02
2026-01-01 16:55:35 [conftest.py:49  ] [ INFO] ⏱️  状态: 通过
2026-01-01 16:55:35 [conftest.py:50  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:51  ] [ INFO] 
2026-01-01 16:55:35 [conftest.py:37  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:38  ] [ INFO] 🚀 开始测试: test_case03
2026-01-01 16:55:35 [conftest.py:39  ] [ INFO] 📁 文件: test_examples.py
2026-01-01 16:55:35 [conftest.py:40  ] [ INFO] 📍 行号: 10
2026-01-01 16:55:35 [conftest.py:41  ] [ INFO] 🔗 节点: test_examples.py::test_case03
2026-01-01 16:55:35 [conftest.py:42  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:47  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:48  ] [ INFO] ✅ 测试完成: test_case03
2026-01-01 16:55:35 [conftest.py:49  ] [ INFO] ⏱️  状态: 通过
2026-01-01 16:55:35 [conftest.py:50  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:51  ] [ INFO] 
2026-01-01 16:55:35 [conftest.py:37  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:38  ] [ INFO] 🚀 开始测试: TestUserAPI.test_create_user
2026-01-01 16:55:35 [conftest.py:39  ] [ INFO] 📁 文件: testcases\feature1\test_example3.py
2026-01-01 16:55:35 [conftest.py:40  ] [ INFO] 📍 行号: 7
2026-01-01 16:55:35 [conftest.py:41  ] [ INFO] 🔗 节点: testcases/feature1/test_example3.py::TestUserAPI::test_create_user
2026-01-01 16:55:35 [conftest.py:42  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:47  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:48  ] [ INFO] ✅ 测试完成: TestUserAPI.test_create_user
2026-01-01 16:55:35 [conftest.py:49  ] [ INFO] ⏱️  状态: 通过
2026-01-01 16:55:35 [conftest.py:50  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:51  ] [ INFO] 
2026-01-01 16:55:35 [conftest.py:37  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:38  ] [ INFO] 🚀 开始测试: TestUserAPI.test_get_user
2026-01-01 16:55:35 [conftest.py:39  ] [ INFO] 📁 文件: testcases\feature1\test_example3.py
2026-01-01 16:55:35 [conftest.py:40  ] [ INFO] 📍 行号: 12
2026-01-01 16:55:35 [conftest.py:41  ] [ INFO] 🔗 节点: testcases/feature1/test_example3.py::TestUserAPI::test_get_user
2026-01-01 16:55:35 [conftest.py:42  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:47  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:48  ] [ INFO] ✅ 测试完成: TestUserAPI.test_get_user
2026-01-01 16:55:35 [conftest.py:49  ] [ INFO] ⏱️  状态: 通过
2026-01-01 16:55:35 [conftest.py:50  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:51  ] [ INFO] 
2026-01-01 16:55:35 [conftest.py:37  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:38  ] [ INFO] 🚀 开始测试: test_endpoint
2026-01-01 16:55:35 [conftest.py:39  ] [ INFO] 📁 文件: testcases\feature1\test_example3.py
2026-01-01 16:55:35 [conftest.py:40  ] [ INFO] 📍 行号: 26
2026-01-01 16:55:35 [conftest.py:41  ] [ INFO] 🔗 节点: testcases/feature1/test_example3.py::test_endpoint
2026-01-01 16:55:35 [conftest.py:42  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:47  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:48  ] [ INFO] ✅ 测试完成: test_endpoint
2026-01-01 16:55:35 [conftest.py:49  ] [ INFO] ⏱️  状态: 通过
2026-01-01 16:55:35 [conftest.py:50  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:51  ] [ INFO] 
2026-01-01 16:55:35 [conftest.py:37  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:38  ] [ INFO] 🚀 开始测试: test_user_registration
2026-01-01 16:55:35 [conftest.py:39  ] [ INFO] 📁 文件: testcases\test_example1.py
2026-01-01 16:55:35 [conftest.py:40  ] [ INFO] 📍 行号: 2
2026-01-01 16:55:35 [conftest.py:41  ] [ INFO] 🔗 节点: testcases/test_example1.py::test_user_registration
2026-01-01 16:55:35 [conftest.py:42  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:47  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:48  ] [ INFO] ✅ 测试完成: test_user_registration
2026-01-01 16:55:35 [conftest.py:49  ] [ INFO] ⏱️  状态: 通过
2026-01-01 16:55:35 [conftest.py:50  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:51  ] [ INFO] 
2026-01-01 16:55:35 [conftest.py:37  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:38  ] [ INFO] 🚀 开始测试: test_dynamic_marks
2026-01-01 16:55:35 [conftest.py:39  ] [ INFO] 📁 文件: testcases\test_example2.py
2026-01-01 16:55:35 [conftest.py:40  ] [ INFO] 📍 行号: 6
2026-01-01 16:55:35 [conftest.py:41  ] [ INFO] 🔗 节点: testcases/test_example2.py::test_dynamic_marks
2026-01-01 16:55:35 [conftest.py:42  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:47  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:48  ] [ INFO] ✅ 测试完成: test_dynamic_marks
2026-01-01 16:55:35 [conftest.py:49  ] [ INFO] ⏱️  状态: 通过
2026-01-01 16:55:35 [conftest.py:50  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:51  ] [ INFO] 
2026-01-01 16:55:35 [conftest.py:37  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:38  ] [ INFO] 🚀 开始测试: test_mark_method
2026-01-01 16:55:35 [conftest.py:39  ] [ INFO] 📁 文件: testcases\test_example2.py
2026-01-01 16:55:35 [conftest.py:40  ] [ INFO] 📍 行号: 14
2026-01-01 16:55:35 [conftest.py:41  ] [ INFO] 🔗 节点: testcases/test_example2.py::test_mark_method
2026-01-01 16:55:35 [conftest.py:42  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:47  ] [ INFO] ----------------------------------------
2026-01-01 16:55:35 [conftest.py:48  ] [ INFO] ✅ 测试完成: test_mark_method
2026-01-01 16:55:35 [conftest.py:49  ] [ INFO] ⏱️  状态: 通过
2026-01-01 16:55:35 [conftest.py:50  ] [ INFO] ======================================================================
2026-01-01 16:55:35 [conftest.py:51  ] [ INFO] 
```



### 使用表格样式（推荐）

```python
# conftest.py
# conftest.py - 表格样式版本（最清晰）
import pytest
import logging
import os

@pytest.fixture(scope='function', autouse=True)
def table_style_test_logging(request):
    """表格样式的测试日志记录"""
    test_node = request.node
    
    # 获取信息
    test_name = test_node.name
    test_class = test_node.cls.__name__ if hasattr(test_node, 'cls') and test_node.cls else None
    full_name = f"{test_class}.{test_name}" if test_class else test_name
    
    # 文件路径
    test_file = test_node.location[0] if hasattr(test_node, 'location') else 'unknown'
    current_dir = os.getcwd()
    if test_file.startswith(current_dir):
        relative_file = os.path.relpath(test_file, current_dir)
    else:
        relative_file = test_file
    
    line_number = test_node.location[1] if hasattr(test_node, 'location') else 0
    
    # 固定宽度的表格样式
    header = "+" + "-" * 78 + "+"
    
    # 开始日志
    logging.info(header)
    logging.info(f"| {'🚀 测试开始':^76} |")
    logging.info(f"| {'─' * 76} |")
    logging.info(f"| {'测试用例:':<15} {full_name:<61} |")
    logging.info(f"| {'文件位置:':<15} {relative_file}:{line_number:<55} |")
    logging.info(f"| {'节点标识:':<15} {test_node.nodeid:<61} |")
    logging.info(f"| {'─' * 76} |")
    
    yield
    
    # 结束日志
    logging.info(f"| {'✅ 测试完成:':<15} {full_name:<61} |")
    logging.info(f"| {'执行状态:':<15} {'通过':<61} |")
    logging.info(header)
    logging.info("")
```

运行后查看日志：

```shell
2026-01-01 16:56:50 [conftest.py:30  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:31  ] [ INFO] |                                    🚀 测试开始                                    |
2026-01-01 16:56:50 [conftest.py:32  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:33  ] [ INFO] | 测试用例:           TestName.test_case01                                          |
2026-01-01 16:56:50 [conftest.py:34  ] [ INFO] | 文件位置:           test_examples.py:1                                                       |
2026-01-01 16:56:50 [conftest.py:35  ] [ INFO] | 节点标识:           test_examples.py::TestName::test_case01                       |
2026-01-01 16:56:50 [conftest.py:36  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:41  ] [ INFO] | ✅ 测试完成:         TestName.test_case01                                          |
2026-01-01 16:56:50 [conftest.py:42  ] [ INFO] | 执行状态:           通过                                                            |
2026-01-01 16:56:50 [conftest.py:43  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:44  ] [ INFO] 
2026-01-01 16:56:50 [conftest.py:30  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:31  ] [ INFO] |                                    🚀 测试开始                                    |
2026-01-01 16:56:50 [conftest.py:32  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:33  ] [ INFO] | 测试用例:           test_case02                                                   |
2026-01-01 16:56:50 [conftest.py:34  ] [ INFO] | 文件位置:           test_examples.py:5                                                       |
2026-01-01 16:56:50 [conftest.py:35  ] [ INFO] | 节点标识:           test_examples.py::test_case02                                 |
2026-01-01 16:56:50 [conftest.py:36  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:41  ] [ INFO] | ✅ 测试完成:         test_case02                                                   |
2026-01-01 16:56:50 [conftest.py:42  ] [ INFO] | 执行状态:           通过                                                            |
2026-01-01 16:56:50 [conftest.py:43  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:44  ] [ INFO] 
2026-01-01 16:56:50 [conftest.py:30  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:31  ] [ INFO] |                                    🚀 测试开始                                    |
2026-01-01 16:56:50 [conftest.py:32  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:33  ] [ INFO] | 测试用例:           test_case03                                                   |
2026-01-01 16:56:50 [conftest.py:34  ] [ INFO] | 文件位置:           test_examples.py:10                                                      |
2026-01-01 16:56:50 [conftest.py:35  ] [ INFO] | 节点标识:           test_examples.py::test_case03                                 |
2026-01-01 16:56:50 [conftest.py:36  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:41  ] [ INFO] | ✅ 测试完成:         test_case03                                                   |
2026-01-01 16:56:50 [conftest.py:42  ] [ INFO] | 执行状态:           通过                                                            |
2026-01-01 16:56:50 [conftest.py:43  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:44  ] [ INFO] 
2026-01-01 16:56:50 [conftest.py:30  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:31  ] [ INFO] |                                    🚀 测试开始                                    |
2026-01-01 16:56:50 [conftest.py:32  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:33  ] [ INFO] | 测试用例:           TestUserAPI.test_create_user                                  |
2026-01-01 16:56:50 [conftest.py:34  ] [ INFO] | 文件位置:           testcases\feature1\test_example3.py:7                                                       |
2026-01-01 16:56:50 [conftest.py:35  ] [ INFO] | 节点标识:           testcases/feature1/test_example3.py::TestUserAPI::test_create_user |
2026-01-01 16:56:50 [conftest.py:36  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:41  ] [ INFO] | ✅ 测试完成:         TestUserAPI.test_create_user                                  |
2026-01-01 16:56:50 [conftest.py:42  ] [ INFO] | 执行状态:           通过                                                            |
2026-01-01 16:56:50 [conftest.py:43  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:44  ] [ INFO] 
2026-01-01 16:56:50 [conftest.py:30  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:31  ] [ INFO] |                                    🚀 测试开始                                    |
2026-01-01 16:56:50 [conftest.py:32  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:33  ] [ INFO] | 测试用例:           TestUserAPI.test_get_user                                     |
2026-01-01 16:56:50 [conftest.py:34  ] [ INFO] | 文件位置:           testcases\feature1\test_example3.py:12                                                      |
2026-01-01 16:56:50 [conftest.py:35  ] [ INFO] | 节点标识:           testcases/feature1/test_example3.py::TestUserAPI::test_get_user |
2026-01-01 16:56:50 [conftest.py:36  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:41  ] [ INFO] | ✅ 测试完成:         TestUserAPI.test_get_user                                     |
2026-01-01 16:56:50 [conftest.py:42  ] [ INFO] | 执行状态:           通过                                                            |
2026-01-01 16:56:50 [conftest.py:43  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:44  ] [ INFO] 
2026-01-01 16:56:50 [conftest.py:30  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:31  ] [ INFO] |                                    🚀 测试开始                                    |
2026-01-01 16:56:50 [conftest.py:32  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:33  ] [ INFO] | 测试用例:           test_endpoint                                                 |
2026-01-01 16:56:50 [conftest.py:34  ] [ INFO] | 文件位置:           testcases\feature1\test_example3.py:26                                                      |
2026-01-01 16:56:50 [conftest.py:35  ] [ INFO] | 节点标识:           testcases/feature1/test_example3.py::test_endpoint            |
2026-01-01 16:56:50 [conftest.py:36  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:41  ] [ INFO] | ✅ 测试完成:         test_endpoint                                                 |
2026-01-01 16:56:50 [conftest.py:42  ] [ INFO] | 执行状态:           通过                                                            |
2026-01-01 16:56:50 [conftest.py:43  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:44  ] [ INFO] 
2026-01-01 16:56:50 [conftest.py:30  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:31  ] [ INFO] |                                    🚀 测试开始                                    |
2026-01-01 16:56:50 [conftest.py:32  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:33  ] [ INFO] | 测试用例:           test_user_registration                                        |
2026-01-01 16:56:50 [conftest.py:34  ] [ INFO] | 文件位置:           testcases\test_example1.py:2                                                       |
2026-01-01 16:56:50 [conftest.py:35  ] [ INFO] | 节点标识:           testcases/test_example1.py::test_user_registration            |
2026-01-01 16:56:50 [conftest.py:36  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:41  ] [ INFO] | ✅ 测试完成:         test_user_registration                                        |
2026-01-01 16:56:50 [conftest.py:42  ] [ INFO] | 执行状态:           通过                                                            |
2026-01-01 16:56:50 [conftest.py:43  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:44  ] [ INFO] 
2026-01-01 16:56:50 [conftest.py:30  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:31  ] [ INFO] |                                    🚀 测试开始                                    |
2026-01-01 16:56:50 [conftest.py:32  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:33  ] [ INFO] | 测试用例:           test_dynamic_marks                                            |
2026-01-01 16:56:50 [conftest.py:34  ] [ INFO] | 文件位置:           testcases\test_example2.py:6                                                       |
2026-01-01 16:56:50 [conftest.py:35  ] [ INFO] | 节点标识:           testcases/test_example2.py::test_dynamic_marks                |
2026-01-01 16:56:50 [conftest.py:36  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:41  ] [ INFO] | ✅ 测试完成:         test_dynamic_marks                                            |
2026-01-01 16:56:50 [conftest.py:42  ] [ INFO] | 执行状态:           通过                                                            |
2026-01-01 16:56:50 [conftest.py:43  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:44  ] [ INFO] 
2026-01-01 16:56:50 [conftest.py:30  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:31  ] [ INFO] |                                    🚀 测试开始                                    |
2026-01-01 16:56:50 [conftest.py:32  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:33  ] [ INFO] | 测试用例:           test_mark_method                                              |
2026-01-01 16:56:50 [conftest.py:34  ] [ INFO] | 文件位置:           testcases\test_example2.py:14                                                      |
2026-01-01 16:56:50 [conftest.py:35  ] [ INFO] | 节点标识:           testcases/test_example2.py::test_mark_method                  |
2026-01-01 16:56:50 [conftest.py:36  ] [ INFO] | ──────────────────────────────────────────────────────────────────────────── |
2026-01-01 16:56:50 [conftest.py:41  ] [ INFO] | ✅ 测试完成:         test_mark_method                                              |
2026-01-01 16:56:50 [conftest.py:42  ] [ INFO] | 执行状态:           通过                                                            |
2026-01-01 16:56:50 [conftest.py:43  ] [ INFO] +------------------------------------------------------------------------------+
2026-01-01 16:56:50 [conftest.py:44  ] [ INFO] 
```


## 各方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 方案1 | 简单直接，信息完整 | 显示格式固定 | 需要完整路径信息的场景 |
| 方案2 | 获取原始名称，更简洁 | 可能丢失类信息 | 需要简洁名称的场景 |
| 方案3 | 获取函数详细信息 | 依赖函数对象 | 需要函数级详细信息的场景 |
| 方案4 | 使用钩子，更底层 | 需要理解pytest钩子 | 需要全局控制的场景 |
| 方案5 | 使用上下文，结构化好 | 代码稍复杂 | 需要结构化日志的场景 |
| 方案6 | 装饰器模式，灵活 | 实现较复杂 | 需要装饰器模式的场景 |
| 方案7 | 可自定义日志格式 | 需要配置过滤器 | 需要定制化日志格式的场景 |

**推荐使用优化后的综合方案**，因为它：
1. 信息全面：包含了所有重要的测试信息
2. 格式友好：使用相对路径，显示更简洁
3. 结构清晰：开始和结束有明确的分隔
4. 兼容性好：支持类内和类外的测试用例
5. 易于阅读：使用符号和格式化提升可读性

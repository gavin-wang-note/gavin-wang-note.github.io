---
title: pytest hook系列之pytest_collection
date: 2024-09-09 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-18.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_collection
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_collection`是`pytest`框架中的一个钩子函数，它在测试用例收集的早期阶段运行。理解和应用这个钩子函数可以帮助我们在测试用例的收集和执行过程中实现更为细粒度的定制化操作。本文将详细介绍`pytest_collection`的使用场景、参数，以及通过具体案例展示其应用。

# 什么是 pytest_collection？

`pytest_collection`是`pytest`提供的一个钩子函数，它在测试框架开始收集测试用例之前被调用。这意味着你可以在测试用例收集阶段对即将被收集的项进行预处理。

# 使用场景

* 动态插入或修改测试用例：在测试用例被实际收集之前根据特定条件插入或修改测试用例。
* 预处理测试用例路径：在测试用例文件被收集之前，预处理或动态生成测试用例路径。
* 条件性启用/禁用测试模块：基于外部条件或配置，动态启用或禁用一些测试模块。


# 参数

```python
def pytest_collection(session):
    # session: 当前 pytest 会话对象
```

* session：当前`pytest`会话对象，通过这个对象可以访问所有收集到的测试项以及配置。


# 示例代码

## 案例一：动态插入测试用例

目标：根据外部条件在测试收集阶段动态插入测试用例。

步骤：

* 定义条件，决定是否插入额外的测试用例。
* 使用`pytest_collection`钩子动态插入测试用例。


示例代码：

```python
# conftest.py
import pytest

def pytest_collection(session):
    # 条件检查，比如环境变量
    if "INSERT_TEST_CASE" in session.config.option.env:
        # 创建额外的测试用例
        from _pytest.python import Function
        test_func = lambda: None  # 示例测试用例
        new_test = Function(name="test_dynamic_insert", parent=session)
        
        # 动态添加新的测试用例
        session.items.append(new_test)
```

**说明：**

* 通过检查环境变量`INSERT_TEST_CASE`决定是否动态插入测试用例。
* 使用`Function`创建新的测试函数，并将其动态添加到`session.items`列表中。


## 案例二：预处理测试用例路径

目标：在测试用例被收集之前预处理或动态生成测试路径列表。

步骤：

* 态生成测试路径列表。
* 使用 pytest_collection 钩子设置新的测试路径。


示例代码：

```python
# conftest.py
import pytest

def pytest_collection(session):
    # 生成动态测试路径列表
    test_paths = ["tests/test_file1.py", "tests/test_file2.py"]
    
    # 设置 session 配置中的测试路径
    session.config.args = test_paths
```

**说明：**

* 通过`test_paths`列表动态生成测试用例路径。
* 修改`session.config.args`来覆盖默认的测试路径设置。


## 案例三：条件性启用/禁用测试模块

目标：基于外部配置或参数，动态启用或禁用某些测试模块。

步骤：

* 读取外部配置或参数。
* 使用 pytest_collection 钩子进行条件检查，启用或禁用模块。


示例代码：

```python
# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--enable-tests", action="store", default=None, help="Enable specific test modules")

def pytest_collection(session):
    # 获取命令行参数
    enabled_tests = session.config.getoption("--enable-tests")
    if enabled_tests:
        enabled_tests_list = enabled_tests.split(",")
        
        # 筛选启用的测试模块
        def filter_tests(item):
            return any(item.nodeid.startswith(test) for test in enabled_tests_list)
        
        # 更新 session.items，保留需要启用的测试模块
        session.items = list(filter(filter_tests, session.items))
```

**说明：**

* 通过命令行参数`--enable-tests`获取要启用的测试模块列表。
* 使用`filter_tests`函数筛选并保留需要启用的测试模块。


# 完整示例

```python
# config.py
# conftest.py
import pytest
import os

def pytest_addoption(parser):
    parser.addoption("--enable-tests", action="store", default=None, help="Enable specific test modules (comma-separated)")

def pytest_collection_modifyitems(config, items):
    selected_files = ["tests/test_file1.py", "tests/test_file2.py"]

    # 预处理测试用例路径
    config.args = selected_files

    # 基于命令行参数动态启用/禁用测试模块
    enabled_tests = config.getoption("--enable-tests")
    if enabled_tests:
        enabled_tests_list = enabled_tests.split(",")
    else:
        enabled_tests_list = selected_files

    # 筛选启用的测试模块
    def filter_tests(item):
        return any(item.nodeid.startswith(test) for test in enabled_tests_list)
    
    # 更新 items，保留需要启用的测试模块
    items[:] = list(filter(filter_tests, items))

    # 动态插入测试用例
    if "INSERT_TEST_CASE" in os.environ:
        from _pytest.python import Function

        def dynamic_test_function():
            assert True, "This is a dynamically inserted test case"

        # Use Function.from_parent to create a new test function
        new_test = Function.from_parent(parent=items[0].parent, name="test_dynamic_insert", callobj=dynamic_test_function)
        items.append(new_test)
        print(f"Dynamically inserted test case: {new_test.nodeid}")
```


测试用例文件内容：

```python
# 示例测试文件 `tests/test_file1.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_file2.py`
def test_example2():
    assert 2 + 2 == 4

# 示例测试文件 `tests/test_file3.py`
def test_example3():
    assert 3 + 3 == 6
```


**详细解释:**

* 动态插入测试用例：在`pytest_collection`钩子中检查环境变量`INSERT_TEST_CASE`，如果存在则使用`_pytest.python.Function.from_parent`创建一个新的测试用例，并将其添加到`session.items`列表中。
* 预处理测试用例路径：直接修改`session.config.args`以包含指定的测试用例路径列表，从而覆盖默认的测试路径设置。
* 基于命令行参数动态启用/禁用测试模块：通过命令行选项`--enable-tests`获取要启用的测试模块列表，然后在`pytest_collection`钩子中根据此选项的值筛选并更新`session.items`中的测试用例。

# 运行说明

## 预处理测试用例路径

无需任何特殊设置，默认情况下只会收集`tests/test_file1.py`和`tests/test_file2.py`这两个文件中的测试用例。


```shell
pytest -s -v
```

这将只运行`tests/test_file1.py`和`tests/test_file2.py`中的测试用例：

```shell
root@Gavin:~/test/hook# pytest -s -v
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 3 items                                                                                                                                                                                                                                       

tests/test_file1.py::test_example1 PASSED
tests/test_file2.py::test_example2 PASSED

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
```

## 动态插入测试用例

要测试动态插入测试用例的功能，可以设置环境变量`INSERT_TEST_CASE`并运行`pytest`：


```shell
export INSERT_TEST_CASE=1
pytest -s -v
```

这将插入一个新的测试用例`test_dynamic_insert`，执行效果如下：

```shell
root@Gavin:~/test/hook# export INSERT_TEST_CASE=1
root@Gavin:~/test/hook# pytest -s -v
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collecting ... Dynamically inserted test case: tests/test_file1.py::test_dynamic_insert
collected 3 items                                                                                                                                                                                                                                       

tests/test_file1.py::test_example1 PASSED
tests/test_file2.py::test_example2 PASSED
tests/test_file1.py::test_dynamic_insert PASSED

=================================================================================================================== 3 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

## 基于命令行参数动态启用/禁用测试模块

可以通过`--enable-tests`参数指定要启用的测试模块，例如：


```shell
pytest -s -v --enable-tests=tests/test_file1.py,tests/test_file3.py
```

这将只运行`tests/test_file1.py`和`tests/test_file3.py`中的测试用例，而忽略其他文件中的测试用例(需要当前环境未设置`INSERT_TEST_CASE`，可以退出当前`ssh session`重连)：

```shell
root@Gavin:~# cd test
root@Gavin:~/test# cd hook/
root@Gavin:~/test/hook# pytest -s -v --enable-tests=tests/test_file1.py,tests/test_file3.py
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 3 items                                                                                                                                                                                                                                       

tests/test_file1.py::test_example1 PASSED
tests/test_file3.py::test_example3 PASSED

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

# 结语

`pytest_collection`是`pytest`中强大且灵活的钩子，能够在测试用例收集的早期阶段提供过渡操作。通过本文的案例，你可以针对不同需求，灵活应用`pytest_collection`来优化测试流程并增加测试的灵活性。在实际应用中，可以根据项目需求及测试场景对这些示例进行扩展和调整。


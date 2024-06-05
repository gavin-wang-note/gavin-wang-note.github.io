---
title: pytest hook系列之pytest_load_initial_conftests
date: 2024-09-08 23:00:00
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
summary: pytest hook之pytest_load_initial_conftests
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_load_initial_conftests` 是 `pytest` 提供的一个钩子函数，专门用来在测试开始之前加载最早的 `conftest.py` 文件。它在 `pytest `启动的早期阶段被调用，主要用于在加载初始 `conftest.py` 文件之前和之后进行一些定制操作。通过这个钩子，我们可以在测试运行之前进行一些前置操作，比如动态配置环境、预处理某些文件或目录等。

# 使用场景

这个钩子函数可以用在以下几个场景：

* 在测试运行之前动态添加或修改`conftest.py`文件路径。
* 在测试框架加载初始配置之前执行某些操作（例如，设置环境变量、初始化日志系统等）。
* 定制`conftest.py`文件的搜索路径，适配特定的项目结构或需求。


# 参数

* early_config: 一个`Config`对象，包含 `pytest`最早的配置和命令行选项。
* args: 命令行参数列表，可以用来决定如何加载`conftest.py`文件。


# 示例代码

以下是一个完整的示例代码及其详细注释，展示了如何使用 `pytest_load_initial_conftests` 钩子函数。

假设目录结构如下：

```shell
├── conftest.py
├── custom
│   ├── conftest.py
│   └── __init__.py
├── my_pytest_plugin.py
├── pytest.ini
└── tests
    ├── __init__.py
    └── test_example.py
```

## 创建插件模块

```python
# my_pytest_plugin.py
import os
import importlib.util

def pytest_load_initial_conftests(early_config, args):
    """
    Pytest 钩子函数：加载初始 conftest.py 文件

    参数:
        early_config: Config 对象，包含 Pytest 的早期配置和命令行选项
        args: 命令行参数列表
    """
    print("Initial command line arguments:", args)

    # 设置环境变量
    os.environ["TEST_ENV"] = "true"
    print("Environment variable TEST_ENV set to 'true'")

    # 动态加载 conftest.py
    custom_conftest_dir = "/root/test/hook/custom"
    custom_conftest_path = os.path.join(custom_conftest_dir, "conftest.py")

    if os.path.isfile(custom_conftest_path):
        spec = importlib.util.spec_from_file_location("custom_conftest", custom_conftest_path)
        custom_conftest = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(custom_conftest)
        print(f"Loaded custom conftest from {custom_conftest_path}")

# 确保模块导入时出发调试打印
print("my_pytest_plugin module imported")
```

## 配置pytest.ini文件

```shell
# pytest.ini
[pytest]
addopts = -p my_pytest_plugin
```

## 创建示例conftest.py文件

为了验证动态加载的效果，我们在自定义路径下创建一个示例`conftest.py`文件。

文件路径: `/path/to/custom/conftest/conftest.py` #  请根据实际情况修改

```python
print("Custom conftest.py loaded successfully")

def pytest_configure(config):
    print("Custom conftest.py pytest_configure called")
```

## 创建项目根目录下conftest.py文件

```python
# 文件路径: 项目根目录/conftest.py

pytest_plugins = ["my_pytest_plugin"]

def pytest_configure(config):
    print("conftest.py has been loaded.")
```

## 创建测试文件

我们创建一个测试文件，验证测试环境变量是否被正确设置。

文件路径: 项目根目录/tests/test_example.py

```python
import os

def test_env_variable():
    assert os.getenv("TEST_ENV") == "true"
```

## 运行和验证

在项目根目录运行 `pytest`:

```shell
PYTHONPATH=. pytest
```

## 输出结果

控制台应显示如下信息，表示插件成功加载，环境变量设置正确，并且自定义的`conftest.py`文件被正确加载：

```shell
root@Gavin:~/test/hook# PYTHONPATH=. pytest -s -v
my_pytest_plugin module imported
Initial command line arguments: ['-p', 'my_pytest_plugin', '-s', '-v']
Environment variable TEST_ENV set to 'true'
Custom conftest.py loaded successfully
Loaded custom conftest from /root/test/hook/custom/conftest.py
conftest.py has been loaded.
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
configfile: pytest.ini
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collecting ... Custom conftest.py loaded successfully
collected 1 item                                                                                                                                                                                                                                        

tests/test_example.py::test_env_variable PASSED

=================================================================================================================== 1 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```



# 小结

通过自定义`pytest_load_initial_conftests`钩子函数，我们可以在测试运行之前进行各种初始化操作，如修改`conftest.py`文件路径、设置环境变量等。这将有助于你更灵活且有针对性地配置和运行测试环境，满足不同的项目需求。

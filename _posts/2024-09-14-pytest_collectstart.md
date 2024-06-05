---
title: pytest hook系列之pytest_collectstart
date: 2024-09-14 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-14.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_collectstart
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_collectstart` 是`pytest`框架中的一个钩子函数，提供一个在测试用例收集开始时运行自定义逻辑的机会。利用这个钩子函数，我们可以在测试收集器开始收集测试用例前进行一些初始化操作或调试信息输出等操作。本篇文章将详细介绍 `pytest_collectstart` 的使用场景、参数，并通过具体案例展示其应用。

# 什么是pytest_collectstart？

`pytest_collectstart` 是一个`pytest`提供的钩子函数，它在收集器开始收集测试用例之前调用。通过这个钩子，我们可以在测试用例的收集阶段执行特定的初始化操作、调试输出或记录日志等。

# 使用场景

1. **收集前初始化操作**：在测试用例收集之前进行一些全局性的初始化操作。
2. **输出调试信息**：输出当前正在收集的节点信息，以便调试复杂的测试收集过程。
3. **记录日志**：在收集器开始收集前记录相关信息到日志文件，用于后续的审计和分析。

# 参数

```python
def pytest_collectstart(collector):
    # collector: pytest 收集器对象，表示即将开始收集测试用例的节点
    pass
```

- `collector`：当前`pytest`收集器对象，表示即将开始收集测试用例的节点，可以通过此对象获取相关的收集信息。

# 示例代码

## 案例一：收集前初始化操作

目标：在测试用例收集之前进行全局性的初始化操作。

步骤：
1. 定义初始化操作逻辑。
2. 使用 `pytest_collectstart` 钩子函数在收集器开始收集测试用例前执行初始化操作。

示例代码：

```python
# conftest.py
import pytest

def pytest_collectstart(collector):
    print(f"Starting to collect tests from: {collector}")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

**说明：**
- `pytest_collectstart` 钩子中，通过 `print` 函数输出当前收集器的收集信息。

运行效果如下：

```shell
root@Gavin:~/test/hook# pytest
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collecting ... Starting to collect tests from: <Session  exitstatus=<ExitCode.OK: 0> testsfailed=0 testscollected=0>
Starting to collect tests from: <Dir hook>
Starting to collect tests from: <Dir tests>
Starting to collect tests from: <Module test_example.py>
collected 2 items                                                                                                                                                                                                                                       

tests/test_example.py ..                                                                                                                                                                                                                          [100%]

=================================================================================================================== 2 passed in 0.06s ===================================================================================================================
root@Gavin:~/test/hook#
```

## 案例二：输出调试信息

目标：输出当前正在收集的节点信息，以便调试复杂的测试收集过程。

步骤：
1. 在 `pytest_collectstart` 钩子中输出当前收集器的节点信息。
2. 运行测试收集过程，查看输出的调试信息。

示例代码：

```python
# conftest.py
import pytest

def pytest_collectstart(collector):
    print(f"Collecting tests from: {collector}")

# 示例测试文件 `tests/test_example1.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_example2.py`
def test_example2():
    assert 2 + 2 == 4
```

**说明：**
- `pytest_collectstart` 钩子中，通过 `print` 函数输出当前收集器的节点信息，用于调试和分析。

运行效果如下：

```shell
root@Gavin:~/test/hook# vim conftest.py 
root@Gavin:~/test/hook# rm -rf tests/*
root@Gavin:~/test/hook# vim tests/test_example1.py
root@Gavin:~/test/hook# vim tests/test_example2.py
root@Gavin:~/test/hook# pytest
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collecting ... Collecting tests from: <Session  exitstatus=<ExitCode.OK: 0> testsfailed=0 testscollected=0>
Collecting tests from: <Dir hook>
Collecting tests from: <Dir tests>
Collecting tests from: <Module test_example1.py>
Collecting tests from: <Module test_example2.py>
collected 2 items                                                                                                                                                                                                                                       

tests/test_example1.py .                                                                                                                                                                                                                          [ 50%]
tests/test_example2.py .                                                                                                                                                                                                                          [100%]

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# 
```

## 案例三：记录日志

目标：在收集器开始收集前记录相关信息到日志文件，用于后续的审计和分析。

步骤：
1. 配置日志记录。
2. 在 `pytest_collectstart` 钩子中记录当前收集器的信息到日志文件。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='test_collection.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_sessionstart(session):
    logging.info("Test session started")

def pytest_collectstart(collector):
    # 记录当前收集器的信息到日志文件
    logging.info(f"Collecting tests from: {collector}")

# 示例测试文件 `tests/test_example1.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_example2.py`
def test_example2():
    assert 2 + 2 == 4
```

**注释**：
- `pytest_sessionstart` 钩子，用于配置日志记录，确保在测试会话开始时初始化日志配置。
- `pytest_collectstart` 钩子中，通过 `logging.info` 函数记录当前收集器的节点信息到日志文件，为后续的审计和分析提供数据。


运行 pytest 来验证新的测试设置：

```shell
pytest -s -v
```

你应该看到输出当前正在收集的测试信息（以及可以通过日志文件查看记录的信息）:

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
collected 2 items                                                                                                                                                                                                                                       

tests/test_example1.py::test_example1 PASSED
tests/test_example2.py::test_example2 PASSED

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Jun  1 09:43 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  380 Jun  1 09:42 conftest.py
drwxr-xr-x 2 root root 4096 Jun  1 09:43 __pycache__/
drwxr-xr-x 3 root root 4096 Jun  1 09:41 .pytest_cache/
-rw-r--r-- 1 root root  437 Jun  1 09:43 test_collection.log
drwxr-xr-x 3 root root 4096 Jun  1 09:41 tests/
root@Gavin:~/test/hook# cat test_collection.log 
2024-06-01 09:43:00,301 - Test session started
2024-06-01 09:43:00,323 - Collecting tests from: <Session  exitstatus=<ExitCode.OK: 0> testsfailed=0 testscollected=0>
2024-06-01 09:43:00,324 - Collecting tests from: <Dir hook>
2024-06-01 09:43:00,325 - Collecting tests from: <Dir tests>
2024-06-01 09:43:00,325 - Collecting tests from: <Module test_example1.py>
2024-06-01 09:43:00,326 - Collecting tests from: <Module test_example2.py>
root@Gavin:~/test/hook# 
```


补充说明

1. **pytest_collectstart 函数**
    - 在测试用例收集阶段，每当一个新的收集器开始收集测试用例时调用。
    - 通过 `collector` 参数，可以获取当前即将开始收集测试用例的节点信息。

2. **不同应用场景**
    - **初始化操作**：在测试收集之前，可以进行一些全局性的初始化操作，确保测试环境的准备。
    - **输出调试信息**：输出当前正在收集的节点信息，有助于调试和理解测试用例的收集过程。
    - **记录日志**：将收集器的信息记录到日志文件中，为后续的审计和分析提供数据。

# 结语

`pytest_collectstart` 是`pytest`中一个灵活和强大的钩子，允许我们在测试用例收集开始时执行自定义逻辑。通过本文的案例，你可以了解如何使用 `pytest_collectstart` 实现初始化操作、输出调试信息和记录日志。在实际应用中，可以根据项目需求及测试场景对这些示例进行扩展和调整，从而实现更灵活的测试管理和调试。希望这篇文章能够帮助你更好地理解和使用 `pytest_collectstart`。


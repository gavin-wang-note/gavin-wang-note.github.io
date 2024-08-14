---
title: pytest hook系列之pytest_runtest_call
date: 2024-09-29 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-17.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_runtest_call
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_runtest_call` 是`pytest`框架中的一个钩子函数，它在每个测试项实际调用执行时被触发，允许我们在每个测试项实际调用时插入自定义逻辑。通过这个钩子，我们可以在测试执行期间进行特定的操作或记录，如监控测试执行、处理特定的前后操作等，从而增强测试的灵活性和可调试性。

# 使用场景

1. **监控测试执行**：在测试项调用时插入监控逻辑，记录执行时间、测试结果等。
2. **前后操作**：在测试项调用时执行特定的前后操作，如统计、日志记录等。
3. **调试和分析**：在测试项调用时插入调试逻辑，帮助开发者观察测试执行过程中的状态和变化。

# 参数

```python
def pytest_runtest_call(item):
    # item: 被采集到的测试项对象，包含测试项的所有信息
    pass
```

- `item`：被采集到的测试项对象，包含测试项的所有信息。

# 示例代码

## 案例一：记录每个测试项的执行时间

目标：在每个测试项调用时记录其执行时间，并输出统计信息。

步骤：
1. 使用 `pytest_runtest_call` 钩子函数。
2. 在钩子函数中记录测试项的开始时间和结束时间，并计算执行时间。

示例代码：

```python
# conftest.py
import pytest
import time

def pytest_runtest_call(item):
    start_time = time.time()
    print(f"Starting test: {item.nodeid}")

    # 实际调用测试函数
    item.obj()

    end_time = time.time()
    duration = end_time - start_time
    print(f"Finished test: {item.nodeid} in {duration:.4f} seconds")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    time.sleep(1)
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

**注释**：
- 在 `pytest_runtest_call` 钩子函数中，记录每个测试项的开始时间和结束时间，并计算其执行时间。

## 案例二：在测试项调用时记录日志

目标：在每个测试项调用时记录相关日志信息，如测试函数名称、测试结果等。

步骤：
1. 使用 `pytest_runtest_call` 钩子函数。
2. 在钩子函数中记录日志信息。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='test_calls.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_runtest_call(item):
    log_message = f"Executing test: {item.nodeid}"
    logging.info(log_message)
    print(log_message)

    # 实际调用测试函数
    item.obj()

    log_message = f"Finished test: {item.nodeid}"
    logging.info(log_message)
    print(log_message)

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

**注释**：
- 在 `pytest_runtest_call` 钩子函数中，使用 `logging` 模块记录日志信息，并同时输出到控制台。

## 案例三：在测试项调用时插入调试逻辑

目标：在每个测试项调用时插入调试逻辑，记录关键变量的值和状态。

步骤：
1. 使用 `pytest_runtest_call` 钩子函数。
2. 在钩子函数中插入调试逻辑，记录关键变量的值和状态。

示例代码：

```python
# conftest.py
import pytest

def pytest_runtest_call(item):
    # 插入调试逻辑，记录关键变量的值和状态
    print(f"Debugging before test: {item.nodeid}, function name: {item.name}")

    # 实际调用测试函数
    item.obj()

    print(f"Debugging after test: {item.nodeid}, function name: {item.name}")

# 示例测试文件 `tests/test_example.py`
x = 10

def test_example1():
    assert x == 10

def test_example2():
    assert x < 20
```

**注释**：
- 在 `pytest_runtest_call` 钩子函数中，插入调试逻辑，记录测试项执行前后的关键变量和状态信息。

## 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree
.
├── conftest.py
└── tests
    └── test_example.py

2 directories, 2 files
root@Gavin:~/test/hook#
```

在项目根目录下运行以下命令：

```shell
pytest -s -v
```

### 验证输出信息

根据不同的案例，控制台和日志文件输出应包含自定义逻辑的结果，如每个测试项的执行时间、日志信息和调试信息。

### 控制台输出示例

**案例一：记录每个测试项的执行时间**

```plaintext
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

tests/test_example.py::test_example1 Starting test: tests/test_example.py::test_example1
Finished test: tests/test_example.py::test_example1 in 1.0007 seconds
PASSED
tests/test_example.py::test_example2 Starting test: tests/test_example.py::test_example2
Finished test: tests/test_example.py::test_example2 in 0.0000 seconds
PASSED

=================================================================================================================== 2 passed in 2.04s ===================================================================================================================
root@Gavin:~/test/hook# 
```

**案例二：在测试项调用时记录日志**

```plaintext
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

tests/test_example.py::test_example1 Executing test: tests/test_example.py::test_example1
Finished test: tests/test_example.py::test_example1
PASSED
tests/test_example.py::test_example2 Executing test: tests/test_example.py::test_example2
Finished test: tests/test_example.py::test_example2
PASSED

=================================================================================================================== 2 passed in 2.04s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Sep 29 09:30 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  441 Sep 29 09:30 conftest.py
drwxr-xr-x 2 root root 4096 Sep 29 09:30 __pycache__/
drwxr-xr-x 3 root root 4096 Sep 29 09:21 .pytest_cache/
-rw-r--r-- 1 root root  314 Sep 29 09:30 test_calls.log
drwxr-xr-x 3 root root 4096 Sep 29 09:29 tests/
root@Gavin:~/test/hook# cat test_calls.log 
2024-09-29 09:30:10,574 - Executing test: tests/test_example.py::test_example1
2024-09-29 09:30:11,575 - Finished test: tests/test_example.py::test_example1
2024-09-29 09:30:12,581 - Executing test: tests/test_example.py::test_example2
2024-09-29 09:30:12,581 - Finished test: tests/test_example.py::test_example2
root@Gavin:~/test/hook# 
```

**案例三：在测试项调用时插入调试逻辑**

```plaintext
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

tests/test_example.py::test_example1 Debugging before test: tests/test_example.py::test_example1, function name: test_example1
Debugging after test: tests/test_example.py::test_example1, function name: test_example1
PASSED
tests/test_example.py::test_example2 Debugging before test: tests/test_example.py::test_example2, function name: test_example2
Debugging after test: tests/test_example.py::test_example2, function name: test_example2
PASSED

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

### 详细解释

1. **记录测试执行时间**
   - 在 `pytest_runtest_call` 钩子函数中，通过记录测试项的开始时间和结束时间来计算其执行时间，并输出到控制台。
  
2. **日志记录**
   - 在 `pytest_runtest_call` 钩子函数中，使用 `logging` 模块记录每个测试项的日志信息，并输出到控制台。

3. **调试逻辑**
   - 在 `pytest_runtest_call` 钩子函数中，插入调试逻辑，记录测试项执行前后的关键变量和状态信息，帮助开发者观察测试执行过程中变量的变化。

### 确保钩子正确触发的步骤

1. **检查 pytest 版本**
   - 确保使用的是支持 `pytest_runtest_call` 钩子的 `pytest` 版本。

2. **正确的目录结构和文件内容**
   - 确保 `conftest.py` 文件位于项目根目录，测试文件如 `test_example.py` 放在 `tests` 目录你且符合 `pytest` 命名规则。

3. **清理 pytest 缓存**
   - 通过 `pytest --cache-clear` 清理缓存，确保使用最新代码和配置。

4. **验证输出**
   - 运行`pytest`并查看控制台和日志文件输出，确认测试项调用期间的自定义逻辑执行结果符合预期。

# 总结

通过详细介绍 `pytest_runtest_call` 钩子的使用场景、参数及应用示例，希望能帮助你更好地理解和使用这个钩子函数。无论是记录测试执行时间、记录日志信息，还是插入调试逻辑，都能为你提供强大的工具，增强测试执行期间的灵活性和可调试性。

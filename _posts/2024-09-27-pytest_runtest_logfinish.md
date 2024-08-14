---
title: pytest hook系列之pytest_runtest_logfinish
date: 2024-09-27 23:00:00
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
summary: pytest hook之pytest_runtest_logfinish
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_runtest_logfinish` 是`pytest`框架中的一个钩子函数，它在每个测试项结束执行时被调用，允许我们在测试项结束执行时插入自定义逻辑。通过这个钩子，我们可以在测试项结束时进行特定的记录或清理操作，如日志记录、清理环境变量等，从而对测试执行过程进行更细粒度的控制和监控。

# 使用场景

1. **测试项结束记录**：在每个测试项结束时记录相关信息，如结束时间、测试项结果等。
2. **清理操作**：在测试项结束时执行特定的清理操作，如清理环境变量、释放资源等。
3. **调试和分析**：在测试项结束时插入调试逻辑，帮助开发者观察测试执行后的状态和结果。

# 参数

```python
def pytest_runtest_logfinish(nodeid, location):
    # nodeid: 测试项的唯一标识符
    # location: 测试项的位置，包括文件名和行号
    pass
```

- `nodeid`：测试项的唯一标识符。
- `location`：测试项的位置，包括文件名和行号。

# 示例代码

## 案例一：记录每个测试项的结束时间

目标：在每个测试项结束时记录其结束时间，并输出到日志文件。

步骤：

1. 使用 `pytest_runtest_logfinish` 钩子函数。
2. 在钩子函数中记录测试项的结束时间，并输出到日志文件。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='test_finish.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_runtest_logfinish(nodeid, location):
    logging.info(f"Finished test: {nodeid} at location: {location}")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

**注释**：

- 在 `pytest_runtest_logfinish` 钩子函数中，通过 `logging` 记录每个测试项的结束时间和测试项位置信息。

## 案例二：在测试项结束时清理环境变量

目标：在每个测试项结束时清理特定的环境变量，并确保清理操作生效。

步骤：

1. 使用 `pytest_runtest_logfinish` 钩子函数。
2. 在钩子函数中清理环境变量。

示例代码：

```python
# conftest.py
import pytest
import os

def pytest_runtest_logfinish(nodeid, location):
    # 在测试项结束时清理环境变量
    print(f"Cleaning environment variable for test: {nodeid}")
    if "TEST_ENV" in os.environ:
        del os.environ["TEST_ENV"]

# 示例测试文件 `tests/test_example.py`
def test_example():
    os.environ["TEST_ENV"] = "1"
    assert os.getenv("TEST_ENV") == "1"
```

**注释**：

- 在 `pytest_runtest_logfinish` 钩子函数中，清理环境变量 `TEST_ENV`，并在测试项中验证其清理生效。

## 案例三：在测试项结束时插入调试逻辑

目标：在每个测试项结束时插入调试逻辑，记录测试项的最终状态和结果。

步骤：

1. 使用 `pytest_runtest_logfinish` 钩子函数。
2. 在钩子函数中插入调试逻辑，记录测试项的最终状态和结果。

示例代码：

```python
# conftest.py
import pytest

def pytest_runtest_logfinish(nodeid, location):
    # 插入调试逻辑，记录测试项的最终状态
    print(f"Debugging test finish: {nodeid} at location: {location}")

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 1 + 1 == 2
```

**注释**：

- 在 `pytest_runtest_logfinish` 钩子函数中，插入调试逻辑，记录测试项的最终状态和结果。

## 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree
.
├── conftest.py
└── tests
    └── test_example.py

2 directories, 2 files
root@Gavin:~/test/hook
```

在项目根目录下运行以下命令：

```shell
pytest -s -v
```

### 验证输出信息

根据不同的案例，控制台和日志文件输出应包含自定义逻辑的结果，如每个测试项的结束时间、环境变量清理以及调试信息。

### 控制台输出和日志文件示例

**案例一：记录每个测试项的结束时间**

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

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSED

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Sep 27 09:07 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  273 Sep 27 09:06 conftest.py
drwxr-xr-x 2 root root 4096 Sep 27 09:07 __pycache__/
drwxr-xr-x 3 root root 4096 Sep 27 09:07 .pytest_cache/
-rw-r--r-- 1 root root  274 Sep 27 09:07 test_finish.log
drwxr-xr-x 3 root root 4096 Sep 27 09:07 tests/
root@Gavin:~/test/hook# cat test_finish.log 
2024-09-27 09:07:27,053 - Finished test: tests/test_example.py::test_example1 at location: ('tests/test_example.py', 0, 'test_example1')
2024-09-27 09:07:27,054 - Finished test: tests/test_example.py::test_example2 at location: ('tests/test_example.py', 3, 'test_example2')
root@Gavin:~/test/hook# 
```

**案例二：在测试项结束时清理环境变量**

```plaintext
root@Gavin:~/test/hook# pytest -s -v --cache-clear
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                        

tests/test_example.py::test_example PASSEDCleaning environment variable for test: tests/test_example.py::test_example


=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例三：在测试项结束时插入调试逻辑**

```plaintext
root@Gavin:~/test/hook# pytest -s -v --cache-clear
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                        

tests/test_example.py::test_example PASSEDDebugging test finish: tests/test_example.py::test_example at location: ('tests/test_example.py', 0, 'test_example')


=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook#
```

### 详细解释

1. **记录每个测试项的结束时间**
   - 在 `pytest_runtest_logfinish` 钩子函数中，通过 `logging` 记录每个测试项的结束时间和位置信息，便于后续分析和调试。

2. **清理环境变量**
   - 在 `pytest_runtest_logfinish` 钩子函数中，清理特定的环境变量，确保测试项执行后的清理操作生效。

3. **调试信息**
   - 在 `pytest_runtest_logfinish` 钩子函数中，插入调试逻辑，记录测试项的最终状态和结果，帮助开发者观察测试执行后的环境和设置。

### 确保钩子正确触发的步骤

1. **检查 pytest 版本**
   - 确保使用的 pytest 版本支持 `pytest_runtest_logfinish` 钩子。

2. **正确的目录结构和文件内容**
   - 确保 `conftest.py` 文件位于项目根目录，测试文件如 `test_example.py` 放在 `tests` 目录内且符合 pytest 命名规则。

3. **清理 pytest 缓存**
   - 通过 `pytest --cache-clear` 清理缓存，确保使用最新代码和配置。

4. **验证输出**
   - 运行`pytest`并查看控制台和日志文件输出，确认自定义逻辑的结果符合预期。

# 总结

通过详细介绍 `pytest_runtest_logfinish` 钩子的使用场景、参数及应用示例，希望能帮助你更好地理解和使用这个钩子函数。无论是记录测试项的结束时间、清理环境变量，还是插入调试逻辑，都能为你提供强大的工具，增强测试的监控和调试能力。

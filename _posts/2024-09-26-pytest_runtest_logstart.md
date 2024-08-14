---
title: pytest hook系列之pytest_runtest_logstart
date: 2024-09-26 23:00:00
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
summary: pytest hook之pytest_runtest_logstart
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_runtest_logstart` 是`pytest`框架中的一个钩子函数，它在每个测试项开始执行时被调用。这个钩子允许我们在测试项开始时执行特定操作，如日志记录、环境变量设置等。通过这个钩子，我们可以在测试项开始时进行特定的记录或初始化操作，从而增强测试的监控和调试能力。

# 使用场景

1. **测试项开始记录**：在每个测试项开始时记录相关信息，如开始时间、测试项名称等。
2. **初始化操作**：在测试项开始时执行特定的初始化操作，如设置环境变量、初始化资源等。
3. **调试和分析**：在测试项开始时插入调试逻辑，帮助开发者观察测试执行前的状态和设置。

# 参数

```python
def pytest_runtest_logstart(nodeid, location):
    # nodeid: 测试项的唯一标识符
    # location: 测试项的位置，包括文件名和行号
    pass
```

- `nodeid`：测试项的唯一标识符。
- `location`：测试项的位置，包括文件名和行号。

# 示例代码

## 案例一：记录每个测试项的开始时间

目标：在每个测试项开始时记录其开始时间，并输出到日志文件。

步骤：

1. 使用 `pytest_runtest_logstart` 钩子函数。
2. 在钩子函数中记录测试项的开始时间，并输出到日志文件。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='test_start.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_runtest_logstart(nodeid, location):
    logging.info(f"Starting test: {nodeid} at location: {location}")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

**注释**：

- 在 `pytest_runtest_logstart` 钩子函数中，通过 `logging` 记录每个测试项的开始时间和测试项位置信息。

## 案例二：在测试项开始时设置环境变量

目标：在每个测试项开始时设置特定的环境变量，并确保测试项正确使用该环境变量。

步骤：

1. 使用 `pytest_runtest_logstart` 钩子函数。
2. 在钩子函数中设置环境变量。

示例代码：

```python
# conftest.py
import pytest
import os

def pytest_runtest_logstart(nodeid, location):
    # 在测试项开始时设置环境变量
    print(f"Setting environment variable for test: {nodeid}")
    os.environ["TEST_ENV"] = "1"

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert os.getenv("TEST_ENV") == "1"
```

**注释**：

- 在 `pytest_runtest_logstart` 钩子函数中，设置环境变量 `TEST_ENV`，并在测试项中验证其值。

## 案例三：在测试项开始时插入调试逻辑

目标：在每个测试项开始时插入调试逻辑，记录测试项的初始状态和配置信息。

步骤：
1. 使用 `pytest_runtest_logstart` 钩子函数。
2. 在钩子函数中插入调试逻辑，记录测试项的初始状态和配置信息。

示例代码：

```python
# conftest.py
import pytest

def pytest_runtest_logstart(nodeid, location):
    # 插入调试逻辑，记录测试项的初始状态
    print(f"Debugging test start: {nodeid} at location: {location}")

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 1 + 1 == 2
```

**注释**：
- 在 `pytest_runtest_logstart` 钩子函数中，插入调试逻辑，记录测试项的初始状态和配置信息。

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

根据不同的案例，控制台和日志文件输出应包含自定义逻辑的结果，如每个测试项的开始时间、环境变量设置以及调试信息。

### 控制台输出和日志文件示例

**案例一：记录每个测试项的开始时间**

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
drwxr-xr-x 5 root root 4096 Sep 26 08:56 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  271 Sep 26 08:56 conftest.py
drwxr-xr-x 2 root root 4096 Sep 26 08:56 __pycache__/
drwxr-xr-x 3 root root 4096 Sep 26 08:56 .pytest_cache/
drwxr-xr-x 3 root root 4096 Sep 26 08:56 tests/
-rw-r--r-- 1 root root  274 Sep 26 08:56 test_start.log
root@Gavin:~/test/hook# cat test_start.log 
2024-09-26 08:56:45,882 - Starting test: tests/test_example.py::test_example1 at location: ('tests/test_example.py', 0, 'test_example1')
2024-09-26 08:56:45,901 - Starting test: tests/test_example.py::test_example2 at location: ('tests/test_example.py', 3, 'test_example2')
root@Gavin:~/test/hook# 
```

**案例二：在测试项开始时设置环境变量**

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

tests/test_example.py::test_example Setting environment variable for test: tests/test_example.py::test_example
PASSED

=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 24
drwxr-xr-x 5 root root 4096 Sep 26 08:58 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  213 Sep 26 08:57 conftest.py
drwxr-xr-x 2 root root 4096 Sep 26 08:58 __pycache__/
drwxr-xr-x 3 root root 4096 Sep 26 08:58 .pytest_cache/
drwxr-xr-x 3 root root 4096 Sep 26 08:58 tests/
root@Gavin:~/test/hook#
```

**案例三：在测试项开始时插入调试逻辑**

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

tests/test_example.py::test_example Debugging test start: tests/test_example.py::test_example at location: ('tests/test_example.py', 0, 'test_example')
PASSED

=================================================================================================================== 1 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

### 详细解释

1. **记录每个测试项的开始时间**
   - 在 `pytest_runtest_logstart` 钩子函数中，通过 `logging` 记录每个测试项的开始时间和测试项位置信息，便于后续分析和调试。
  
2. **设置环境变量**
   - 在 `pytest_runtest_logstart` 钩子函数中，设置特定的环境变量，确保测试项能够正确使用该环境变量。

3. **插入调试逻辑**
   - 在 `pytest_runtest_logstart` 钩子函数中，插入调试逻辑，记录测试项的初始状态和配置信息，帮助开发者观察测试执行前的环境和设置。

### 确保钩子正确触发的步骤

1. **检查 pytest 版本**
   - 确保使用的是支持 `pytest_runtest_logstart` 钩子的 `pytest` 版本。

2. **正确的目录结构和文件内容**
   - 确保 `conftest.py` 文件位于项目根目录，测试文件如 `test_example.py` 放在 `tests` 目录内且符合 `pytest` 命名规则。

3. **清理 pytest 缓存**
   - 通过 `pytest --cache-clear` 清理缓存，确保使用最新代码和配置。

4. **验证输出**
   - 运行`pytest`并查看控制台和日志文件输出，确认自定义逻辑的结果符合预期。

# 总结

通过详细介绍 `pytest_runtest_logstart` 钩子的使用场景、参数及应用示例，希望能帮助你更好地理解和使用这个钩子函数。无论是记录测试项的开始时间、设置环境变量，还是插入调试逻辑，都能为你提供强大的工具，增强测试的监控和调试能力。

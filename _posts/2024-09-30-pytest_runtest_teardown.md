---
title: pytest hook系列之pytest_runtest_teardown
date: 2024-09-30 23:00:00
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
summary: pytest hook之pytest_runtest_teardown
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_runtest_teardown` 是`pytest`框架中的一个钩子函数，它在每个测试项结束执行后被调用，允许我们在每个测试项结束执行后插入自定义逻辑。通过这个钩子函数，我们可以在测试项结束后进行清理操作、资源释放、记录日志等，从而保证测试后的环境和状态的清洁、一致性和稳定性。

# 使用场景

1. **资源清理**：在测试项结束后清理特定的资源，如数据库连接、文件句柄等。
2. **环境恢复**：在测试项结束后恢复测试前的环境变量、配置等。
3. **日志记录**：在测试项结束后记录特定的日志信息，以便调试和分析。
4. **调试与分析**：在测试项结束后插入调试逻辑，帮助开发者观察测试后的状态和结果。

# 参数

```python
def pytest_runtest_teardown(item, nextitem):
    # item: 被采集到的测试项对象，包含测试项的所有信息
    # nextitem: 下一个将要运行的测试项对象（如果有）
    pass
```

- `item`：被采集到的测试项对象，包含测试项的所有信息。
- `nextitem`：下一个将要运行的测试项对象（如果有）。

# 例代码

## 案例一：在测试项结束后清理数据库连接

目标：在每个测试项结束后关闭数据库连接，并确保资源被正确释放。

步骤：
1. 使用 `pytest_runtest_teardown` 钩子函数。
2. 在钩子函数中关闭数据库连接。

示例代码：

```python
# conftest.py
import pytest
import sqlite3

def pytest_runtest_teardown(item, nextitem):
    # 在测试项结束后关闭数据库连接
    if hasattr(item, "db_connection"):
        item.db_connection.close()
        print(f"Closed database connection for test: {item.nodeid}")

def pytest_runtest_setup(item):
    # 在测试项开始前初始化数据库连接
    item.db_connection = sqlite3.connect(':memory:')
    print(f"Initialized database connection for test: {item.nodeid}")

# 示例测试文件 `tests/test_example.py`
def test_example(request):
    db_connection = request.node.db_connection
    cursor = db_connection.cursor()
    cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)')
    cursor.execute('INSERT INTO test (value) VALUES ("test_value")')
    db_connection.commit()
    
    cursor.execute('SELECT value FROM test WHERE id=1')
    result = cursor.fetchone()
    assert result[0] == "test_value"
```

**注释**：
- 在 `pytest_runtest_teardown` 钩子函数中，关闭数据库连接，并确保资源被正确释放。
- 在 `pytest_runtest_setup` 钩子函数中，初始化数据库连接，并将其附加到测试项对象。

## 案例二：在测试项结束后恢复环境变量

目标：在每个测试项结束后恢复测试前的环境变量，确保后续测试不受影响。

步骤：
1. 使用 `pytest_runtest_teardown` 钩子函数。
2. 在钩子函数中恢复环境变量。

示例代码：

```python
# conftest.py
import pytest
import os

original_env = os.environ.copy()

def pytest_runtest_teardown(item, nextitem):
    # 在测试项结束后恢复环境变量
    os.environ.clear()
    os.environ.update(original_env)
    print(f"Restored environment variables for test: {item.nodeid}")

def pytest_runtest_setup(item):
    # 在测试项开始前设置临时环境变量
    os.environ["TEST_ENV"] = "temp_value"
    print(f"Set temporary environment variable for test: {item.nodeid}")

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert os.getenv("TEST_ENV") == "temp_value"
```

**注释**：
- 在 `pytest_runtest_teardown` 钩子函数中，恢复测试前的环境变量，确保后续测试不受影响。
- 在 `pytest_runtest_setup` 钩子函数中，设置临时环境变量供测试项使用。

## 案例三：在测试项结束后记录日志信息

目标：在每个测试项结束后记录相关的日志信息，如测试结果、执行时间等，以便调试和分析。

步骤：
1. 使用 `pytest_runtest_teardown` 钩子函数。
2. 在钩子函数中记录日志信息。

示例代码：

```python
# conftest.py
import pytest
import logging
import time

# 配置日志记录
logging.basicConfig(filename='test_teardown.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_runtest_setup(item):
    # 在测试项开始前记录开始时间
    item.start_time = time.time()
    print(f"Starting test: {item.nodeid}")

def pytest_runtest_teardown(item, nextitem):
    # 在测试项结束后记录结束时间和执行时间
    end_time = time.time()
    duration = end_time - item.start_time
    log_message = f"Finished test: {item.nodeid} in {duration:.4f} seconds"
    
    logging.info(log_message)
    print(log_message)

# 示例测试文件 `tests/test_example.py`
def test_example1():
    time.sleep(1)  # 模拟长时间运行的测试
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

**注释**：
- 在 `pytest_runtest_teardown` 钩子函数中，通过 `logging` 记录测试项的结束时间和执行时间，并输出到日志文件。
- 在 `pytest_runtest_setup` 钩子函数中，记录测试项的开始时间。

## 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree
.
├── conftest.py
└── tests
    └── test_exampley.py

2 directories, 2 files
root@Gavin:~/test/hook# 
```

在项目根目录下运行以下命令：

```shell
pytest -s -v
```

### 验证输出信息

根据不同的案例，控制台和日志文件输出应包含自定义逻辑的结果，如数据库连接关闭信息、环境变量恢复信息以及测试执行时间日志信息。

### 控制台输出和日志文件示例

**案例一：在测试项结束后清理数据库连接**

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
collected 1 item                                                                                                                                                                                                                                        

tests/test_exampley.py::test_example Initialized database connection for test: tests/test_exampley.py::test_example
PASSEDClosed database connection for test: tests/test_exampley.py::test_example


=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例二：在测试项结束后恢复环境变量**

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
collected 1 item                                                                                                                                                                                                                                        

tests/test_exampley.py::test_example Set temporary environment variable for test: tests/test_exampley.py::test_example
PASSEDRestored environment variables for test: tests/test_exampley.py::test_example


=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook# 
```

**案例三：在测试项结束后记录日志信息**

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

tests/test_exampley.py::test_example1 Starting test: tests/test_exampley.py::test_example1
PASSEDFinished test: tests/test_exampley.py::test_example1 in 1.0207 seconds

tests/test_exampley.py::test_example2 Starting test: tests/test_exampley.py::test_example2
PASSEDFinished test: tests/test_exampley.py::test_example2 in 0.0005 seconds


=================================================================================================================== 2 passed in 1.04s ===================================================================================================================
root@Gavin:~/test/hook# 
root@Gavin:~/test/hook# cat test_teardown.log 
2024-06-03 09:38:37,196 - Finished test: tests/test_exampley.py::test_example1 in 1.0207 seconds
2024-06-03 09:38:37,197 - Finished test: tests/test_exampley.py::test_example2 in 0.0005 seconds
root@Gavin:~/test/hook# 
```

### 详细解释

1. **清理数据库连接**
   - 在 `pytest_runtest_teardown` 钩子函数中，通过关闭数据库连接，确保资源被正确释放。
  
2. **恢复环境变量**
   - 在 `pytest_runtest_teardown` 钩子函数中，通过恢复环境变量，确保后续测试不受影响。

3. **记录日志信息**
   - 在 `pytest_runtest_teardown` 钩子函数中，通过 `logging` 记录测试项的结束时间和执行时间，并输出到日志文件，以便调试和分析。

### 确保钩子正确触发的步骤

1. **检查 pytest 版本**
   - 确保使用的是支持 `pytest_runtest_teardown` 钩子的 pytest 版本。

2. **正确的目录结构和文件内容**
   - 确保 `conftest.py` 文件位于项目根目录，测试文件如 `test_example.py` 放在 `tests` 目录你且符合 pytest 命名规则。

3. **清理 pytest 缓存**
   - 通过 `pytest --cache-clear` 清理缓存，确保使用最新代码和配置。

4. **验证输出**
   - 运行` pytest`并查看控制台和日志文件输出，确认测试项结束后的自定义逻辑执行结果符合预期。

# 总结

通过详细介绍 `pytest_runtest_teardown` 钩子的使用场景、参数及应用示例，希望能帮助你更好地理解和使用这个钩子函数。无论是清理数据库连接、恢复环境变量，还是记录日志信息，都能为你提供强大帮助。

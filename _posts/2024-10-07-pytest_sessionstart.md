---
title: pytest hook系列之pytest_sessionstart
date: 2024-10-07 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-19.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_sessionstart
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_sessionstart` 是`pytest`框架中的一个钩子函数，用于在测试会话开始时执行特定的初始化代码。它在测试会话开始时被触发。这个钩子允许我们在所有测试用例执行之前执行一些全局的初始化操作，例如配置环境、启动服务、设置全局变量等，从而为测试的顺利进行提供保障，增强测试的准备工作和初始配置。

# 使用场景

1. **全局初始化**：在所有测试用例执行之前执行全局的初始化操作，如配置数据库连接、准备测试数据等。
2. **启动服务**：在测试会话开始时启动一些必要的服务，如 `web` 服务器、后台任务进程等。
3. **环境配置**：设置环境变量、配置文件路径等，以便测试能够在正确的环境中运行。
4. **日志记录**：记录测试会话的开始时间、版本信息、环境信息等，以便调试和分析。

# 参数

```python
def pytest_sessionstart(session):
    # session: pytest 的会话对象，包含有关当前测试会话的所有信息
    pass
```

- `session`：`pytest`的会话对象，包含有关当前测试会话的所有信息。

# 示例代码

## 案例一：全局初始化

目标：在所有测试用例执行之前执行全局的初始化操作，如配置数据库连接、准备测试数据等。

步骤：
1. 使用 `pytest_sessionstart` 钩子函数。
2. 在钩子函数中插入全局初始化代码。

示例代码：

```python
# conftest.py
import pytest
import sqlite3

def pytest_sessionstart(session):
    """在测试会话开始时创建一个全局的数据库连接"""
    session.db_connection = sqlite3.connect(':memory:')
    cursor = session.db_connection.cursor()
    cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)')
    cursor.execute('INSERT INTO test (value) VALUES ("test_value")')
    session.db_connection.commit()
    print("Global database connection initialized.")

@pytest.fixture
def db_connection(request):
    """提供一个数据库连接 fixture"""
    return request.session.db_connection

# 示例测试文件 `tests/test_example.py`
def test_example1(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT value FROM test WHERE id=1')
    result = cursor.fetchone()
    assert result[0] == "test_value"

def test_example2(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM test')
    result = cursor.fetchone()
    assert result[0] == 1
```

**注释**：
- 在 `pytest_sessionstart` 钩子函数中，创建一个全局的数据库连接，并在会话对象中存储该连接。
- 通过 `db_connection fixture` 提供该数据库连接，以便测试用例使用。

## 案例二：启动服务

目标：在测试会话开始时启动一些必要的服务，如 `web` 服务器、后台任务进程等。

步骤：
1. 使用 `pytest_sessionstart` 钩子函数。
2. 在钩子函数中插入服务启动代码。

示例代码：

```python
# conftest.py
import pytest
import subprocess
import time

def pytest_sessionstart(session):
    """在测试会话开始时启动一个 web 服务器"""
    session.web_server = subprocess.Popen(['python3', '-m', 'http.server', '8000'])
    time.sleep(2)  # 等待服务器启动
    print("Web server started.")

def pytest_sessionfinish(session, exitstatus):
    """在测试会话结束时关闭 web 服务器"""
    session.web_server.terminate()
    session.web_server.wait()
    print("Web server terminated.")

# 示例测试文件 `tests/test_example.py`
import requests

def test_web_server():
    response = requests.get('http://localhost:8000')
    assert response.status_code == 200
```

**注释**：
- 在 `pytest_sessionstart` 钩子函数中，启动一个`web`服务器，并在会话对象中存储该服务器的进程对象。
- 在 `pytest_sessionfinish` 钩子函数中，关闭该`web`服务器，确保资源正确释放。
- 使用 `requests` 库检查`web`服务器是否正常运行。

## 案例三：环境配置

目标：设置环境变量、配置文件路径等，以便测试能够在正确的环境中运行。

步骤：
1. 使用 `pytest_sessionstart` 钩子函数。
2. 在钩子函数中插入环境配置代码。

示例代码：

```python
# conftest.py
import pytest
import os

def pytest_sessionstart(session):
    """在测试会话开始时配置环境变量"""
    os.environ['TEST_ENV_VAR'] = 'test_value'
    print("Environment variable configured.")

@pytest.fixture
def env_config():
    """提供一个环境配置 fixture"""
    return os.environ['TEST_ENV_VAR']

# 示例测试文件 `tests/test_example.py`
def test_env_variable(env_config):
    assert env_config == 'test_value'
```

**注释**：
- 在 `pytest_sessionstart` 钩子函数中，设置环境变量。
- 通过 `env_config fixture`提供该环境变量，以便测试用例使用。

## 案例四：日志记录

目标：记录测试会话的开始时间、版本信息、环境信息等，以便调试和分析。

步骤：
1. 使用 `pytest_sessionstart` 钩子函数。
2. 在钩子函数中插入日志记录代码。

示例代码：

```python
# conftest.py
import pytest
import logging
import time
import sys

# 配置日志记录
logging.basicConfig(filename='session.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_sessionstart(session):
    """在测试会话开始时记录日志信息"""
    logging.info("Test session started.")
    logging.info(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"pytest version: {pytest.__version__}")
    logging.info(f"Python version: {sys.executable}")  # 获取当前解释器的路径

def pytest_sessionfinish(session, exitstatus):
    """在测试会话结束时记录日志信息"""
    logging.info("Test session finished.")
    logging.info(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Exit status: {exitstatus}")

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 1 + 1 == 2
```

**注释**：
- 在 `pytest_sessionstart` 钩子函数中，记录测试会话的开始时间、`pytest`版本信息、`Python`版本信息等。
- 在 `pytest_sessionfinish` 钩子函数中，记录测试会话的结束时间和退出状态。

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
pytest -s -v --cache-clear
```

### 验证输出信息

根据不同的案例，控制台、日志文件和环境变量应包含自定义逻辑的结果，如数据库连接的初始化日志、`web` 服务器的启动和终止日志、环境变量的设置及其值、会话开始和结束日志等。

**案例一：全局初始化**

```shell
root@Gavin:~/test/hook# pytest -s -v
Global database connection initialized.
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
root@Gavin:~/test/hook#
```

**案例二：启动服务**:

```shell
root@Gavin:~/test/hook# pytest -s -v
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
Web server started.
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

tests/test_example.py::test_web_server 127.0.0.1 - - [03/Jun/2024 22:54:55] "GET / HTTP/1.1" 200 -
PASSEDWeb server terminated.


=================================================================================================================== 1 passed in 0.09s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例三：环境配置**:

```shell
root@Gavin:~/test/hook# pytest -s -v
Environment variable configured.
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

tests/test_example.py::test_env_variable PASSED

=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook#
```

### 日志文件示例

**案例四：日志记录**

`session.log` 文件内容示例：

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

tests/test_example.py::test_example PASSED

=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Oct  7 23:00 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  779 Oct  7 23:00 conftest.py
drwxr-xr-x 2 root root 4096 Oct  7 23:00 __pycache__/
drwxr-xr-x 3 root root 4096 Oct  7 22:45 .pytest_cache/
-rw-r--r-- 1 root root  667 Oct  7 23:00 session.log
drwxr-xr-x 3 root root 4096 Oct  7 22:58 tests/
root@Gavin:~/test/hook# cat session.log 
2024-10-07 22:58:07,725 - Test session started.
2024-10-07 22:58:07,725 - Start time: 2024-10-07 22:58:07
2024-10-07 22:58:07,725 - pytest version: 8.0.2
2024-10-07 22:58:36,644 - Test session started.
2024-10-07 22:58:36,644 - Start time: 2024-10-07 22:58:36
2024-10-07 22:58:36,644 - pytest version: 8.0.2
2024-10-07 23:00:56,983 - Test session started.
2024-10-07 23:00:56,984 - Start time: 2024-10-07 23:00:56
2024-10-07 23:00:56,984 - pytest version: 8.0.2
2024-10-07 23:00:56,984 - Python version: /usr/bin/python3
2024-10-07 23:00:57,024 - Test session finished.
2024-10-07 23:00:57,024 - End time: 2024-10-07 23:00:57
2024-10-07 23:00:57,024 - Exit status: 0
root@Gavin:~/test/hook#
```

# 总结

通过 `pytest_sessionstart` 钩子，我们可以在测试会话开始时执行全局的初始化操作，如配置环境、启动服务、设置全局变量和记录日志等，从而为测试的顺利进行提供保障。

本文详细介绍了 `pytest_sessionstart` 钩子的使用场景、参数及具体案例，并提供了完整的示例代码和详细解释，帮助读者更好地理解和应用这个强大的功能。

希望这些内容对你有所帮助，使你能够更好地利用 `pytest_sessionstart` 来优化和扩展你的测试流程。

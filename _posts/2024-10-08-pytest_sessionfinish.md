---
title: pytest hook系列之pytest_sessionfinish
date: 2024-10-08 23:00:00
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
summary: pytest hook之pytest_sessionfinish
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_sessionfinish` 是`pytest`框架中的一个钩子函数，用于在测试会话结束时执行特定的最终化代码，它在测试会话结束时被触发。通过这个钩子函数，我们可以在所有测试用例执行完毕之后运行一些清理代码或收尾工作（测试用例执行完毕之后执行一些全局的最终化操作，例如关闭服务、清理资源、生成报告等），从而增强测试的清理及结果处理。

# 使用场景

1. **关闭服务**：在测试会话结束时关闭某些在会话期间启动的服务，如 `web` 服务器、后台任务进程等。
2. **清理资源**：释放在测试会话期间分配的资源，如数据库连接、文件句柄等。
3. **生成报告**：在测试会话结束时生成测试报告，汇总所有测试用例的结果。
4. **记录日志**：记录测试会话的结束时间及结果，以便调试和分析。

# 参数
```python
def pytest_sessionfinish(session, exitstatus):
    # session: pytest 的会话对象，包含有关当前测试会话的所有信息
    # exitstatus: 测试会话的退出状态，表示测试运行的结果
    pass
```

- `session`：`pytest`的会话对象，包含有关当前测试会话的所有信息。
- `exitstatus`：测试会话的退出状态，表示测试运行的结果。

# 示例代码

## 案例一：关闭服务

目标：在测试会话结束时关闭某些在会话期间启动的服务，如 `web` 服务器、后台任务进程等。

步骤：

1. 使用 `pytest_sessionfinish` 钩子函数。
2. 在钩子函数中插入服务关闭代码。

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
- 在 `pytest_sessionstart` 钩子函数中，启动一个 `web` 服务器，并在会话对象中存储该服务器的进程对象。
- 在 `pytest_sessionfinish` 钩子函数中，关闭该 `web` 服务器，确保资源正确释放。
- 使用 `requests` 库检查 `web` 服务器是否正常运行。

## 案例二：清理资源

目标：在测试会话结束时释放在会话期间分配的资源，如数据库连接、文件句柄等。

步骤：
1. 使用 `pytest_sessionfinish` 钩子函数。
2. 在钩子函数中插入资源清理代码。

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

def pytest_sessionfinish(session, exitstatus):
    """在测试会话结束时关闭数据库连接"""
    session.db_connection.close()
    print("Global database connection closed.")

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
- 在 `pytest_sessionfinish` 钩子函数中，关闭数据库连接，确保资源正确释放。
- 通过 `db_connection fixture` 提供该数据库连接，以便测试用例使用。

## 案例三：生成报告

目标：在测试会话结束时生成测试报告，汇总所有测试用例的结果。

步骤：
1. 使用 `pytest_sessionfinish` 钩子函数。
2. 在钩子函数中插入报告生成代码。

示例代码：

```python
# conftest.py
import pytest
import json

test_results = []

def pytest_runtest_makereport(item, call):
    """收集每个测试用例的结果"""
    if call.when == 'call':
        test_results.append({
            'nodeid': item.nodeid,
            'outcome': call.excinfo.typename if call.excinfo else 'passed',
            'duration': call.stop - call.start,
        })

def pytest_sessionfinish(session, exitstatus):
    """在测试会话结束时生成测试报告"""
    with open('test_report.json', 'w') as f:
        json.dump(test_results, f, indent=4)
    print(f"Test report generated with {len(test_results)} entries.")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 5  # 故意的失败用于演示
```

**注释**：
- 在 `pytest_runtest_makereport` 钩子函数中，收集每个测试用例的结果，并存储在 `test_results` 列表中。
- 在 `pytest_sessionfinish` 钩子函数中，生成包含所有测试用例结果的 `JSON` 报告，并将其保存到文件。

## 案例四：记录日志

目标：记录测试会话的结束时间及结果，以便调试和分析。

步骤：
1. 使用 `pytest_sessionfinish` 钩子函数。
2. 在钩子函数中插入日志记录代码。

示例代码：

```python
# conftest.py
import pytest
import logging
import time

# 配置日志记录
logging.basicConfig(filename='session.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_sessionstart(session):
    """在测试会话开始时记录日志信息"""
    logging.info("Test session started.")
    logging.info(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

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
- 在 `pytest_sessionstart` 钩子中记录测试会话的开始时间。
- 在 `pytest_sessionfinish` 钩子中记录测试会话的结束时间及退出状态。
- 使用 `logging` 模块记录日志信息。

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

根据不同的案例，控制台、日志文件和生成的报告文件应包含自定义逻辑的结果，如服务的启动和关闭日志、数据库连接的初始化和关闭日志、测试结果的报告以及会话开始和结束日志等。

**案例一：关闭服务**


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

tests/test_example.py::test_web_server 127.0.0.1 - - [04/Jun/2024 09:06:13] "GET / HTTP/1.1" 200 -
PASSEDWeb server terminated.


=================================================================================================================== 1 passed in 0.08s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例二：清理资源**

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
tests/test_example.py::test_example2 PASSEDGlobal database connection closed.


=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例三：生成报告**

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

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 FAILEDTest report generated with 2 entries.


======================================================================================================================= FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example2 _____________________________________________________________________________________________________________________

    def test_example2():
>       assert 2 + 2 == 5  # 故意的失败用于演示
E       assert (2 + 2) == 5

tests/test_example.py:5: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_example2 - assert (2 + 2) == 5
============================================================================================================== 1 failed, 1 passed in 0.11s ==============================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Oct  8 09:10 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  622 Oct  8 09:10 conftest.py
drwxr-xr-x 2 root root 4096 Oct  8 09:10 __pycache__/
drwxr-xr-x 3 root root 4096 Oct  8 09:06 .pytest_cache/
-rw-r--r-- 1 root root  296 Oct  8 09:10 test_report.json
drwxr-xr-x 3 root root 4096 Oct  8 09:10 tests/
root@Gavin:~/test/hook# cat test_report.json 
[
    {
        "nodeid": "tests/test_example.py::test_example1",
        "outcome": "passed",
        "duration": 0.00014448165893554688
    },
    {
        "nodeid": "tests/test_example.py::test_example2",
        "outcome": "AssertionError",
        "duration": 0.00045752525329589844
    }
]root@Gavin:~/test/hook#
```

**案例四：记录日志**

`session.log` 文件内容示例：

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

tests/test_example.py::test_example1 PASSED

=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook# cat session.log 
2024-10-08 09:11:52,038 - Test session started.
2024-10-08 09:11:52,038 - Start time: 2024-10-08 09:11:52
2024-10-08 09:11:52,081 - Test session finished.
2024-10-08 09:11:52,081 - End time: 2024-10-08 09:11:52
2024-10-08 09:11:52,081 - Exit status: 0
root@Gavin:~/test/hook#
```

### 详细解释

1. **关闭服务**（案例一）：
   - 在 `pytest_sessionstart` 钩子中，通过 `subprocess` 模块启动一个本地 `web` 服务器，并将其进程对象存储在 `session` 对象中。
   - 在 `pytest_sessionfinish` 钩子中，使用 `terminate` 方法关闭 `web` 服务器，确保资源能够正确释放。
   - 通过一个简单的测试用例验证 `web` 服务器的运行状态。

2. **清理资源**（案例二）：
   - 在 `pytest_sessionstart` 钩子中，创建一个全局的数据库连接，并在会话对象中存储该连接。
   - 在 `pytest_sessionfinish` 钩子中，关闭数据库连接，确保测试结束时资源能够正确释放。
   - 使用 `fixture` 提供数据库连接，确保测试用例能够正常使用该连接。

3. **生成报告**（案例三）：
   - 在 `pytest_runtest_makereport` 钩子函数中，收集每个测试用例的结果，包括节点 `ID`、结果和执行时间，并将数据存储在 `test_results` 列表中。
   - 在 `pytest_sessionfinish` 钩子中，将收集到的测试结果生成 `JSON` 格式的报告，并保存到文件中。
   - 通过多个测试用例演示测试结果的收集和报告的生成。

4. **记录日志**（案例四）：
   - 在 `pytest_sessionstart` 钩子中记录测试会话的开始时间，使用 `time.strftime` 获取当前时间，同时记录 `pytest` 版本和 `Python` 解释器路径。
   - 在 `pytest_sessionfinish` 钩子中记录测试会话的结束时间及退出状态，确保在会话结束时能够记录所有必要的日志信息。
   - 使用 `logging` 模块配置日志记录的格式和日志文件的路径。

### 其他考虑因素

1. **性能影响**：
   - 在使用 `pytest_sessionfinish` 钩子执行清理或报告生成操作时，应注意性能影响。特别是在处理大量测试数据或执行耗时操作时，应尽量简化清理逻辑和报告生成过程，避免对其他测试的执行产生影响。

2. **一致性和可维护性**：
   - 确保在所有需要清理的资源和生成报告的场景中使用一致的策略。这有助于保持代码的一致性和可维护性，避免因不同清理逻辑或报告生成过程不一致而导致的问题。

3. **异常处理**：
   - 在钩子函数中处理可能的异常情况，避免因清理操作失败或报告生成过程中的错误而影响后续测试的执行。使用日志记录和适当的错误处理机制，确保测试过程的稳定性。

# 总结

通过 `pytest_sessionfinish` 钩子，我们可以在测试会话结束时执行全局的最终化操作，如关闭服务、清理资源、生成报告和记录日志等，从而确保测试环境能够被正确释放，并对测试结果进行处理。这些操作有助于提高测试的稳定性和可维护性，确保所有资源在测试结束时能够被正确清理，从而避免资源泄露或其他潜在问题。

本文详细介绍了 `pytest_sessionfinish` 钩子的使用场景、参数及具体案例，并提供了完整的示例代码和详细解释，帮助读者更好地理解和应用这个强大的功能。希望这些内容使你能够更好地利用 `pytest_sessionfinish` 来优化和扩展你的测试流程。

---
title: pytest hook系列之pytest_unconfigure
date: 2024-10-09 23:00:00
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
summary: pytest hook之pytest_unconfigure
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_unconfigure` 是 `pytest` 框架中的一个钩子函数，用于在 `pytest` 配置对象将被销毁前执行特定的清理代码(在 `pytest` 配置对象将被销毁之前被触发)。通过这个钩子函数，我们可以在测试引擎完全关闭之前运行一些收尾工作（在 `pytest` 完全退出之前执行一些全局的最终化操作，例如释放全局资源、保存最后的日志等），从而增强测试的清理及结果处理，保环境能够被正确释放。

# 使用场景

1. **释放全局资源**：在 `pytest` 退出之前释放某些全局资源，如数据库连接、文件句柄等。
2. **保存日志**：在 `pytest` 退出之前保存测试日志以便调试和分析。
3. **生成最后的报告**：在 `pytest` 退出之前生成并保存最后的测试报告。
4. **清理临时文件**：删除在测试过程中生成的临时文件和文件夹，确保环境整洁。

# 参数

```python
def pytest_unconfigure(config):
    # config: `pytest` 的配置对象，包含有关当前测试会话的所有信息
    pass
```

- `config`：`pytest` 的配置对象，包含有关当前测试会话的所有信息。

# 示例代码

## 案例一：释放全局资源

目标：在 `pytest` 退出之前释放某些全局资源，如数据库连接、文件句柄等。

步骤：
1. 使用 `pytest_unconfigure` 钩子函数。
2. 在钩子函数中插入资源释放代码。

示例代码：

```python
# conftest.py
import pytest
import sqlite3

@pytest.fixture(scope='session')
def db_connection():
    """提供一个全局数据库连接"""
    connection = sqlite3.connect(':memory:')
    yield connection
    # 连接将在 pytest_unconfigure 钩子中关闭

def pytest_unconfigure(config):
    """在 pytest 退出之前关闭数据库连接"""
    db_connection = config.pluginmanager.getplugin('db_connection')
    if db_connection:
        db_connection.close()
        print("Global database connection closed.")

# 示例测试文件 `tests/test_example.py`
def test_example1(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)')
    cursor.execute('INSERT INTO test (value) VALUES ("test_value")')
    db_connection.commit()
    
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
- 在 `db_connection fixture` 中创建一个全局数据库连接，并在 `yield` 之后保留该连接。
- 在 `pytest_unconfigure` 钩子中，获取并关闭该数据库连接，确保资源正确释放。

## 案例二：保存日志

目标：在 `pytest` 退出之前保存测试日志以便调试和分析。

步骤：
1. 使用 `pytest_unconfigure` 钩子函数。
2. 在钩子函数中插入日志保存代码。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='test.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_sessionstart(session):
    """在测试会话开始时记录日志信息"""
    logging.info("Test session started.")

def pytest_sessionfinish(session, exitstatus):
    """在测试会话结束时记录日志信息"""
    logging.info("Test session finished.")
    logging.info(f"Exit status: {exitstatus}")

def pytest_unconfigure(config):
    """在 pytest 退出之前保存最终的日志条目"""
    logging.info("Pytest is about to exit.")

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 1 + 1 == 2
```

**注释**：
- 在 `pytest_sessionstart` 钩子中记录测试会话的开始信息。
- 在 `pytest_sessionfinish` 钩子中记录测试会话的结束信息和退出状态。
- 在 `pytest_unconfigure` 钩子中记录 `pytest` 即将退出的信息，确保日志的完整性。

## 案例三：生成最后的报告

目标：在 `pytest` 退出之前生成并保存最后的测试报告。

步骤：
1. 使用 `pytest_unconfigure` 钩子函数。
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

def pytest_unconfigure(config):
    """在 pytest 退出之前生成最终的测试报告"""
    with open('final_test_report.json', 'w') as f:
        json.dump(test_results, f, indent=4)
    print(f"Final test report generated with {len(test_results)} entries.")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 5  # 故意的失败用于演示
```

**注释**：
- 在 `pytest_runtest_makereport` 钩子函数中，收集每个测试用例的结果，包括节点 `ID`、结果和执行时间，并将数据存储在 `test_results` 列表中。
- 在 `pytest_unconfigure` 钩子中，将收集到的测试结果生成 `JSON` 格式的报告，并保存到 `final_test_report.json` 文件中。

## 案例四：清理临时文件

目标：删除在测试过程中生成的临时文件和文件夹，确保环境整洁。

步骤：
1. 使用 `pytest_unconfigure` 钩子函数。
2. 在钩子函数中插入清理临时文件和文件夹的代码。

示例代码：

```python
# conftest.py
import pytest
import shutil
import os

@pytest.fixture(scope='session')
def temp_dir():
    """创建一个临时目录用于测试"""
    os.makedirs('temp', exist_ok=True)
    yield 'temp'
    # 临时目录将在 pytest_unconfigure 钩子中删除

def pytest_unconfigure(config):
    """在 pytest 退出之前删除临时目录"""
    shutil.rmtree('temp', ignore_errors=True)
    print("Temporary directory deleted.")

# 示例测试文件 `tests/test_example.py`
def test_example(temp_dir):
    test_file = os.path.join(temp_dir, 'test_file.txt')
    with open(test_file, 'w') as f:
        f.write('Hello, pytest!')
    assert os.path.exists(test_file)
```

**注释**：
- 在 `temp_dir fixture` 中创建一个临时目录，用于存储测试过程中生成的文件。
- 在 `pytest_unconfigure` 钩子中，删除临时目录，确保测试环境的整洁。

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

根据不同的案例，控制台、日志文件和生成的报告文件应包含自定义逻辑的结果，如服务的关闭日志、数据库连接的关闭日志、最终报告的生成及临时文件的清理等。

### 日志文件示例

**案例二：保存日志**

`test.log` 文件内容示例：

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

=================================================================================================================== 1 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Oct  9 10:00 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  608 Oct  9 10:00 conftest.py
drwxr-xr-x 2 root root 4096 Oct  9 10:00 __pycache__/
drwxr-xr-x 3 root root 4096 Oct  9 09:34 .pytest_cache/
-rw-r--r-- 1 root root  378 Oct  9 10:00 test.log
drwxr-xr-x 3 root root 4096 Oct  9 10:00 tests/
root@Gavin:~/test/hook# cat test.log 
2024-10-09 10:00:22,603 - Test session started.
2024-10-09 10:00:22,651 - Test session finished.
2024-10-09 10:00:22,651 - Exit status: 1
2024-10-09 10:00:22,652 - Pytest is about to exit.
2024-10-09 10:00:45,640 - Test session started.
2024-10-09 10:00:45,684 - Test session finished.
2024-10-09 10:00:45,684 - Exit status: 0
2024-10-09 10:00:45,685 - Pytest is about to exit.
root@Gavin:~/test/hook#
```

**案例三：生成最后的报告**

`final_test_report.json` 文件内容示例：

```json
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
tests/test_example.py::test_example2 FAILED

======================================================================================================================= FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example2 _____________________________________________________________________________________________________________________

    def test_example2():
>       assert 2 + 2 == 5  # 故意的失败用于演示
E       assert (2 + 2) == 5

tests/test_example.py:5: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_example2 - assert (2 + 2) == 5
============================================================================================================== 1 failed, 1 passed in 0.10s ==============================================================================================================
Final test report generated with 2 entries.
root@Gavin:~/test/hook# ll
total 32
drwxr-xr-x 5 root root 4096 Oct  9 10:01 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  627 Oct  9 10:01 conftest.py
-rw-r--r-- 1 root root  291 Oct  9 10:01 final_test_report.json
drwxr-xr-x 2 root root 4096 Oct  9 10:01 __pycache__/
drwxr-xr-x 3 root root 4096 Oct  9 09:34 .pytest_cache/
-rw-r--r-- 1 root root  378 Oct  9 10:00 test.log
drwxr-xr-x 3 root root 4096 Oct  9 10:01 tests/
root@Gavin:~/test/hook# cat final_test_report.json 
[
    {
        "nodeid": "tests/test_example.py::test_example1",
        "outcome": "passed",
        "duration": 9.918212890625e-05
    },
    {
        "nodeid": "tests/test_example.py::test_example2",
        "outcome": "AssertionError",
        "duration": 0.0003113746643066406
    }
]root@Gavin:~/test/hook#
```


**案例四：清理临时文件**

```shell
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

tests/test_example.py::test_example PASSED

=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
Temporary directory deleted.
root@Gavin:~/test/hook#
```

### 总结

通过 `pytest_unconfigure` 钩子，我们可以在 `pytest` 配置对象将被销毁之前执行全局的最终化操作，如释放全局资源、保存测试日志、生成最后的测试报告和清理临时文件等，从而确保环境能够被正确释放，并对测试结果进行处理

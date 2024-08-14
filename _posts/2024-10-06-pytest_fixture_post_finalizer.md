---
title: pytest hook系列之pytest_fixture_post_finalizer
date: 2024-10-06 23:00:00
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
summary: pytest hook之pytest_fixture_post_finalizer
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_fixture_post_finalizer` 是 `pytest` 框架中的一个钩子函数，允许我们在 `fixture`的清理阶段插入自定义逻辑，它在每个 `fixture` 被清理（即 `finalization`）后被触发，如资源的清理、结果的记录等。通过这个钩子函数，我们可以在 `fixture` 被撤销后运行特定的后处理代码，从而增强测试的灵活性和可配置性。

# 使用场景

1. **自定义资源清理**：在 `fixture` 清理阶段插入特定的资源清理代码，如关闭数据库连接、释放外部资源等。
2. **增强可调试性**：在 `fixture` 清理阶段记录日志或调试信息，帮助观察和分析测试过程中的状态和变化。
3. **收集测试数据**：在 `fixture` 清理阶段收集测试数据，便于后续的分析和报告生成。

# 参数

```python
def pytest_fixture_post_finalizer(fixturedef, request):
    # fixturedef: FixtureDef 对象，包含 fixture 定义的所有信息
    # request: _pytest.fixtures.FixtureRequest 对象，包含有关当前测试请求的所有信息
    pass
```

- `fixturedef`：`fixture` 定义对象，包含 `fixture` 定义的所有信息。
- `request`：当前测试请求对象，包含有关当前测试请求的所有信息。

# 示例代码

## 案例一：自定义资源清理

目标：在 `fixture` 清理阶段执行特定的资源清理代码，如关闭数据库连接、释放外部资源等。

步骤：
1. 使用 `pytest_fixture_post_finalizer` 钩子函数。
2. 在钩子函数中插入资源清理代码。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='fixture_cleanup.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_fixture_post_finalizer(fixturedef, request):
    if fixturedef.argname == 'db_connection':
        logging.info(f"Cleaning up fixture: {fixturedef.argname} for {request.node.nodeid}")
        # 假设我们有一个 db_connection 对象需要关闭
        db_connection = request.getfixturevalue('db_connection')
        db_connection.close()
        logging.info(f"Cleaned up fixture: {fixturedef.argname} for {request.node.nodeid}")

@pytest.fixture(scope='function')
def db_connection():
    import sqlite3
    connection = sqlite3.connect(':memory:')
    yield connection
    # 这里不需要立即关闭连接，将在 post finalizer 中关闭

# 示例测试文件 `tests/test_example.py`
def test_example(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)')
    cursor.execute('INSERT INTO test (value) VALUES ("test_value")')
    db_connection.commit()
    
    cursor.execute('SELECT value FROM test WHERE id=1')
    result = cursor.fetchone()
    assert result[0] == "test_value"
```

**注释**：
- 在 `pytest_fixture_post_finalizer` 钩子函数中，检查 `fixture` 名称是否为 `db_connection`，并执行特定的资源清理代码。
- 使用 `logging` 模块记录 `fixture` 清理的开始和结束信息。
- 在 `fixture` 本体中使用 `yield` 关键字，将清理动作延迟到 `post finalizer` 中执行。

## 案例二：增强可调试性

目标：在 `fixture` 清理阶段记录日志或调试信息，帮助观察和分析测试过程中的状态和变化。

步骤：
1. 使用 `pytest_fixture_post_finalizer` 钩子函数。
2. 在钩子函数中插入日志或调试信息记录代码。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='fixture_cleanup.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_fixture_post_finalizer(fixturedef, request):
    if fixturedef.argname == 'example_fixture':
        logging.info(f"Cleaning up fixture: {fixturedef.argname} for {request.node.nodeid}")
        # 示例清理代码，可以根据需要添加其他清理或调试信息
        logging.info(f"Fixture {fixturedef.argname} value: {request.getfixturevalue('example_fixture')}")
        logging.info(f"Cleaned up fixture: {fixturedef.argname} for {request.node.nodeid}")

@pytest.fixture
def example_fixture():
    return "example_fixture_value"

# 示例测试文件 `tests/test_example.py`
def test_example1(example_fixture):
    assert example_fixture == "example_fixture_value"

def test_example2(example_fixture):
    assert example_fixture == "example_fixture_value"
```

**注释**：
- 在 `pytest_fixture_post_finalizer` 钩子函数中，检查 `fixture` 名称是否为 `example_fixture`，并记录清理的日志或调试信息。
- 使用 `logging` 模块记录 `fixture` 清理的开始和结束信息，以及 `fixture` 的值。

## 案例三：收集测试数据

目标：在 `fixture` 清理阶段收集测试数据，便于后续的分析和报告生成。

步骤：
1. 使用 `pytest_fixture_post_finalizer` 钩子函数。
2. 在钩子函数中插入测试数据收集代码。

示例代码：

```python
# conftest.py
import pytest
import json

test_data = []

def pytest_fixture_post_finalizer(fixturedef, request):
    if fixturedef.argname == 'example_fixture':
        # 收集测试数据
        test_data.append({
            'nodeid': request.node.nodeid,
            'fixture': fixturedef.argname,
            'value': request.getfixturevalue('example_fixture')
        })

def pytest_sessionfinish(session, exitstatus):
    # 在会话结束时，将测试数据保存为 JSON 文件
    with open('test_data.json', 'w') as f:
        json.dump(test_data, f, indent=4)
    print(f"Collected {len(test_data)} test data entries.")

@pytest.fixture
def example_fixture():
    return "example_fixture_value"

# 示例测试文件 `tests/test_example.py`
def test_example1(example_fixture):
    assert example_fixture == "example_fixture_value"

def test_example2(example_fixture):
    assert example_fixture == "example_fixture_value"
```

**注释**：
- 在 `pytest_fixture_post_finalizer` 钩子函数中，检查 fixture 名称是否为 `example_fixture`，并收集测试数据。
- 将收集到的测试数据追加到 `test_data` 列表中。
- 在 `pytest_sessionfinish` 钩子函数中，将收集到的测试数据保存为 `JSON` 文件。

## 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree
.
├── conftest.py
└── tests
    └── test_example.py

2 directories, 2 files
```

在项目根目录下运行以下命令：

```shell
pytest -s -v --cache-clear
```

### 验证输出信息

根据不同的案例，控制台和日志文件输出应包含自定义逻辑的结果，如清理操作的日志、收集到的测试数据等。

### 日志文件示例

**案例一：自定义资源清理**

```plaintext
root@Gavin:~/test/hook# vim tests/test_example.py
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

=================================================================================================================== 1 passed in 0.05s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Oct  6 21:48 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  823 Oct  6 21:47 conftest.py
-rw-r--r-- 1 root root  201 Oct  6 21:48 fixture_cleanup.log
drwxr-xr-x 2 root root 4096 Oct  6 21:48 __pycache__/
drwxr-xr-x 3 root root 4096 Oct  6 21:48 .pytest_cache/
drwxr-xr-x 3 root root 4096 Oct  6 21:48 tests/
root@Gavin:~/test/hook# cat fixture_cleanup.log 
2024-10-06 21:48:12,685 - Cleaning up fixture: db_connection for tests/test_example.py::test_example
2024-10-06 21:48:12,686 - Cleaned up fixture: db_connection for tests/test_example.py::test_example
root@Gavin:~/test/hook#
```

**案例二：增强可调试性**

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
drwxr-xr-x 5 root root 4096 Oct  6 21:51 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  713 Oct  6 21:51 conftest.py
-rw-r--r-- 1 root root  572 Oct  6 21:51 fixture_cleanup.log
drwxr-xr-x 2 root root 4096 Oct  6 21:51 __pycache__/
drwxr-xr-x 3 root root 4096 Oct  6 21:51 .pytest_cache/
drwxr-xr-x 3 root root 4096 Oct  6 21:51 tests/
root@Gavin:~/test/hook# cat fixture_cleanup.log 
2024-10-06 21:51:29,396 - Cleaning up fixture: example_fixture for tests/test_example.py::test_example1
2024-10-06 21:51:29,396 - Fixture example_fixture value: example_fixture_value
2024-10-06 21:51:29,396 - Cleaned up fixture: example_fixture for tests/test_example.py::test_example1
2024-10-06 21:51:29,398 - Cleaning up fixture: example_fixture for tests/test_example.py::test_example2
2024-10-06 21:51:29,398 - Fixture example_fixture value: example_fixture_value
2024-10-06 21:51:29,398 - Cleaned up fixture: example_fixture for tests/test_example.py::test_example2
root@Gavin:~/test/hook#
```

**案例三：收集测试数据**

```shell
root@Gavin:~/test/hook# cat fixture_cleanup.log 
2024-10-06 21:51:29,396 - Cleaning up fixture: example_fixture for tests/test_example.py::test_example1
2024-10-06 21:51:29,396 - Fixture example_fixture value: example_fixture_value
2024-10-06 21:51:29,396 - Cleaned up fixture: example_fixture for tests/test_example.py::test_example1
2024-10-06 21:51:29,398 - Cleaning up fixture: example_fixture for tests/test_example.py::test_example2
2024-10-06 21:51:29,398 - Fixture example_fixture value: example_fixture_value
2024-10-06 21:51:29,398 - Cleaned up fixture: example_fixture for tests/test_example.py::test_example2
root@Gavin:~/test/hook# >conftest.py 
root@Gavin:~/test/hook# vim conftest.py 
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Oct  6 21:52 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  696 Oct  6 21:52 conftest.py
-rw-r--r-- 1 root root  572 Oct  6 21:51 fixture_cleanup.log
drwxr-xr-x 2 root root 4096 Oct  6 21:51 __pycache__/
drwxr-xr-x 3 root root 4096 Oct  6 21:51 .pytest_cache/
drwxr-xr-x 3 root root 4096 Oct  6 21:51 tests/
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
collected 2 items                                                                                                                                                                                                                                       

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSEDCollected 2 test data entries.


=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 32
drwxr-xr-x 5 root root 4096 Oct  6 21:52 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  696 Oct  6 21:52 conftest.py
-rw-r--r-- 1 root root  572 Oct  6 21:51 fixture_cleanup.log
drwxr-xr-x 2 root root 4096 Oct  6 21:52 __pycache__/
drwxr-xr-x 3 root root 4096 Oct  6 21:52 .pytest_cache/
-rw-r--r-- 1 root root  302 Oct  6 21:52 test_data.json
drwxr-xr-x 3 root root 4096 Oct  6 21:51 tests/
root@Gavin:~/test/hook# cat test_data.json 
[
    {
        "nodeid": "tests/test_example.py::test_example1",
        "fixture": "example_fixture",
        "value": "example_fixture_value"
    },
    {
        "nodeid": "tests/test_example.py::test_example2",
        "fixture": "example_fixture",
        "value": "example_fixture_value"
    }
]root@Gavin:~/test/hook# 
```

### 详细解释

1. **自定义资源清理**：
   - 在 `pytest_fixture_post_finalizer` 钩子中检查和标识特定的 `fixture`（比如 `db_connection`）。
   - 使用 `logging` 记录清理操作的开始和结束时间，以便调试和监控。
   - 执行资源清理操作，例如关闭数据库连接，确保资源能够正确释放。

2. **增强可调试性**：
   - 在 `pytest_fixture_post_finalizer` 钩子中记录有关 `fixture` 的调试信息，例如 `fixture` 的名称、值及其所属的测试用例。
   - 通过记录清理阶段的信息，帮助开发者和测试人员更好地理解和分析测试过程中发生的问题和状态变化。

3. **收集测试数据**：
   - 在 `pytest_fixture_post_finalizer` 钩子中收集测试数据，例如 `fixture` 的名称、值及其所属的测试用例。
   - 将收集到的测试数据存储在一个全局列表 `test_data` 中。
   - 在测试会话结束时，通过 `pytest_sessionfinish` 钩子将收集到的测试数据保存为 `JSON` 文件，用于后续的分析和报告生成。

### 其他考虑因素

1. **性能影响**：
   - 在使用 `pytest_fixture_post_finalizer` 钩子进行日志记录或数据收集时，要考虑对测试执行性能的影响。尽量保持清理逻辑简洁高效，避免不必要的复杂操作。

2. **一致性和可维护性**：
   - 确保在所有需要清理的 `fixture` 中使用一致的清理策略。这有助于保持代码的一致性和可维护性，避免因不同 `fixture` 的清理逻辑不一致而导致的问题。

3. **异常处理**：
   - 在钩子函数中处理可能的异常情况，避免因清理操作失败而影响后续测试的执行。使用日志记录和适当的错误处理机制，确保测试过程的稳定性。

### 总结

通过 `pytest_fixture_post_finalizer` 钩子，我们可以在 `fixture` 清理阶段执行自定义的资源释放、日志记录和数据收集操作，从而增强测试的灵活性和可维护性。

本文详细介绍了钩子的使用场景、参数及具体案例，并提供了完整的示例代码和详细解释，帮助读者更好地理解和应用这个强大的功能。

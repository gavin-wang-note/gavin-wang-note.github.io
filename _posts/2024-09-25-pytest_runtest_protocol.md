---
title: pytest hook系列之pytest_runtest_protocol
date: 2024-09-25 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-15.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_runtest_protocol
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_runtest_protocol` 是`pytest`框架中的一个钩子函数，它在每个测试项运行时被调用，这个钩子允许我们在测试执行的各个阶段（如调用、设置、清理等）插入自定义逻辑。

通过这个钩子，我们可以在测试运行的不同阶段插入特定的行为，从而实现复杂的测试控制和管理。

# 使用场景

1. **自定义测试执行流程**：在测试执行过程中插入特定的行为，如日志记录、监控等。
2. **测试执行前后操作**：在测试执行前后插入一些前置或后置操作，如设置环境、清理资源等。
3. **调试和观察**：在测试执行的不同阶段插入调试逻辑，观察测试执行过程中的状态和变化。

# 参数

```python
def pytest_runtest_protocol(item, nextitem):
    # item: 被采集到的测试项对象，包含测试项的所有信息
    # nextitem: 下一个将要运行的测试项对象（如果有）
    pass
```

- `item`：被采集到的测试项对象，包含测试项的所有信息。
- `nextitem`：下一个将要运行的测试项对象（如果有）。

# 示例代码

## 案例一：记录每个测试用例的执行时间

目标：在每个测试用例执行前后记录其执行时间，并输出统计信息。

步骤：

1. 使用 `pytest_runtest_protocol` 钩子函数。
2. 在钩子函数中记录测试用例的开始和结束时间，并计算执行时间。

示例代码：

```python
# conftest.py
import pytest
import time

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    start_time = time.time()
    print(f"Starting test: {item.nodeid}")

    # 调用pytest_runtest_protocol的默认实现
    result = yield

    end_time = time.time()
    duration = end_time - start_time
    print(f"Finished test: {item.nodeid} in {duration:.4f} seconds")

    return result  # 返回默认实现的结果

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    time.sleep(1)  # 模拟长时间运行的测试
    assert 2 + 2 == 4
```

**注释**：

- 在 `pytest_runtest_protocol` 钩子函数中，记录测试用例的开始和结束时间，并输出每个测试用例的执行时间。

## 案例二：在测试执行前后执行自定义操作

目标：在每个测试用例执行前后插入自定义操作，如设置环境变量、清理资源等。

步骤：

1. 使用 `pytest_runtest_protocol` 钩子函数。
2. 在钩子函数中添加测试执行前后的自定义操作。

示例代码：

```python
# conftest.py
import pytest
import os

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    # 测试执行前操作
    print(f"Setting up environment for test: {item.nodeid}")
    os.environ["TEST_ENV"] = "1"

    # 调用pytest_runtest_protocol的默认实现
    result = yield

    # 测试执行后操作
    print(f"Tearing down environment for test: {item.nodeid}")
    del os.environ["TEST_ENV"]

    return result  # 返回默认实现的结果

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert os.getenv("TEST_ENV") == "1"
```

**注释**：

- 在 `pytest_runtest_protocol` 钩子函数中，添加测试执行前的环境设置操作和测试执行后的环境清理操作。

## 案例三：在测试执行过程中插入调试逻辑

目标：在测试执行的不同阶段插入调试逻辑，观察测试执行过程中的状态和变化。

步骤：

1. 使用 `pytest_runtest_protocol` 钩子函数。
2. 在钩子函数中添加调试逻辑，记录测试执行过程中的状态和变化。

示例代码：

```python
# conftest.py
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    old_config = item.config
    print(f"Debugging before test: {item.nodeid}, Config: {old_config}")

    # 调用pytest_runtest_protocol的默认实现
    result = yield

    new_config = item.config
    print(f"Debugging after test: {item.nodeid}, Config: {new_config}")

    return result  # 返回默认实现的结果

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 1 + 1 == 2
```

**注释**：

- 在 `pytest_runtest_protocol` 钩子函数中，添加调试逻辑，记录测试执行前后的配置状态。

# 运行和验证

确保目录结构如下：

```shell
```

在项目根目录下运行以下命令：

```shell
pytest -s -v
```

## 验证输出信息

根据不同的案例，控制台输出应显示自定义逻辑的结果，如每个测试用例的执行时间、环境设置和清理操作以及调试信息。

## 控制台输出示例

**案例一：记录每个测试用例的执行时间**

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
Starting test: tests/test_example.py::test_example1

tests/test_example.py::test_example1 PASSEDFinished test: tests/test_example.py::test_example1 in 0.0197 seconds
Starting test: tests/test_example.py::test_example2

tests/test_example.py::test_example2 PASSEDFinished test: tests/test_example.py::test_example2 in 1.0039 seconds


=================================================================================================================== 2 passed in 1.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例二：在测试执行前后执行自定义操作**

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
Setting up environment for test: tests/test_example.py::test_example

tests/test_example.py::test_example PASSEDTearing down environment for test: tests/test_example.py::test_example


=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook# 
```

**案例三：在测试执行过程中插入调试逻辑**

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
Debugging before test: tests/test_example.py::test_example, Config: <_pytest.config.Config object at 0x7342ce0d1310>

tests/test_example.py::test_example PASSEDDebugging after test: tests/test_example.py::test_example, Config: <_pytest.config.Config object at 0x7342ce0d1310>


=================================================================================================================== 1 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# 

```

## 详细解释

1. **记录测试执行时间**
   - 在 `pytest_runtest_protocol` 钩子函数中，通过记录测试开始和结束时间来计算每个测试用例的执行时间，并输出到控制台。
  
2. **前后操作**
   - 在 `pytest_runtest_protocol` 钩子函数中，添加测试执行前后的自定义操作，如设置和删除环境变量。

3. **调试信息**
   - 在 `pytest_runtest_protocol` 钩子函数中，插入调试逻辑，可以在测试执行前后记录配置状态等信息，帮助调试和观察测试执行过程中的变化。

## 确保钩子正确触发的步骤

1. **检查 pytest 版本**
   - 确保使用的`pytest`版本支持 `pytest_runtest_protocol` 钩子。

2. **正确的目录结构和文件内容**
   - 确保 `conftest.py` 文件位于项目根目录，测试文件如 `test_example.py` 放在 `tests` 目录内且符合`pytest`命名规则。

3. **清理 pytest 缓存**
   - 通过 `pytest --cache-clear` 清理缓存，确保使用最新代码和配置。

4. **验证输出**
   - 运行`pytest`并查看控制台输出，确认自定义逻辑的结果符合预期。

# 总结

通过详细介绍 `pytest_runtest_protocol` 钩子的使用场景、参数及应用示例，希望能帮助你更好地理解和使用这个钩子函数。无论是记录测试执行时间、执行前后操作，还是插入调试逻辑，都能为你提供强大的工具，满足各种复杂的测试需求。

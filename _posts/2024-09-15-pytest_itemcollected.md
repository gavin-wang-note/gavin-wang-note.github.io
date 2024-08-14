---
title: pytest hook系列之pytest_itemcollected
date: 2024-09-15 23:00:00
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
summary: pytest hook之pytest_itemcollected
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_itemcollected` 是`pytest`框架中的一个钩子函数，允许我们在每一个测试项被收集到后执行自定义逻辑。利用这个钩子函数，我们可以对收集到的测试项进行处理、记录日志信息或执行其他操作，从而更好地管理和调试测试过程。本篇文章将详细介绍 `pytest_itemcollected` 的使用场景、参数，并通过具体案例展示其应用。

# 什么是pytest_itemcollected？

`pytest_itemcollected` 是一个`pytest`提供的钩子函数，它在每一个测试项被收集到后调用。通过这个钩子，我们可以对收集到的测试项进行进一步处理，如记录日志、过滤测试用例或输出调试信息。

# 使用场景

1. **记录测试项信息**：在每个测试项被收集到后记录信息，便于调试和分析。
2. **动态处理测试项**：根据特定条件对收集到的测试项进行处理，如修改、过滤等。
3. **收集统计信息**：在测试项收集过程中统计特定类型的测试项信息，用于生成报告。

# 参数

```python
def pytest_itemcollected(item):
    # item: 收集到的测试项对象，表示一个具体的测试用例
    pass
```

- `item`：被收集到的测试项对象，表示一个具体的测试用例。可以通过这个对象访问测试用例的相关信息。

# 示例代码

## 案例一：记录测试项信息

目标：在每个测试项被收集到后记录信息，便于调试和分析。

步骤：

1. 配置日志记录。
2. 使用 `pytest_itemcollected` 钩子在每个测试项被收集到后记录其信息。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='item_collection.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_sessionstart(session):
    logging.info("Test session started")

def pytest_itemcollected(item):
    # 记录当前收集到的测试项信息
    logging.info(f"Collected test item: {item.nodeid}")

# 示例测试文件 `tests/test_example1.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_example2.py`
def test_example2():
    assert 2 + 2 == 4
```

**说明**：

- 配置基本日志记录，在 `pytest_itemcollected` 钩子中通过 `logging.info` 记录每个收集到的测试项信息。

运行效果：

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

=================================================================================================================== 2 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Sep 15 09:49 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  370 Sep 15 09:49 conftest.py
-rw-r--r-- 1 root root  217 Sep 15 09:49 item_collection.log
drwxr-xr-x 2 root root 4096 Sep 15 09:49 __pycache__/
drwxr-xr-x 3 root root 4096 Sep 15 09:41 .pytest_cache/
drwxr-xr-x 3 root root 4096 Sep 15 09:41 tests/
root@Gavin:~/test/hook# cat item_collection.log 
2024-09-15 09:49:51,431 - Test session started
2024-09-15 09:49:51,452 - Collected test item: tests/test_example1.py::test_example1
2024-09-15 09:49:51,452 - Collected test item: tests/test_example2.py::test_example2
root@Gavin:~/test/hook#
```

## 案例二：动态处理测试项

目标：根据特定条件对收集到的测试项进行处理，如修改或过滤。

步骤：

1. 在 `pytest_itemcollected` 钩子中定义处理逻辑。
2. 根据特定条件修改或过滤测试项。

示例代码：

```python
# conftest.py
import pytest

def pytest_itemcollected(item):
    # 动态修改测试项的名称
    if 'test_example1' in item.nodeid:
        original_name = item.name
        new_name = 'modified_example1'
        item.name = new_name
        item._nodeid = item._nodeid.replace(original_name, new_name)

# 示例测试文件 `tests/test_example1.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_example2.py`
def test_example2():
    assert 2 + 2 == 4
```

**说明**：

在 `pytest_itemcollected` 钩子中，通过检查 `item.nodeid` 动态修改测试项的名称。

- 检查`item.nodeid`中是否包含`test_example1`，如果匹配，将原测试项名称（`original_name`）替换为新的名称（`new_name`）。
- 直接修改`item.name`属性以更改显示的测试项名称。
- 更新`item._nodeid`的值，确保`nodeid`中也反映出新的测试项名称。


运行效果：

```shell
root@Gavin:~/test/hook# ls -l
total 12
-rw-r--r-- 1 root root  294 Sep 15 09:56 conftest.py
drwxr-xr-x 2 root root 4096 Sep 15 09:50 __pycache__
drwxr-xr-x 3 root root 4096 Sep 15 09:41 tests
root@Gavin:~/test/hook# ls -l tests/
total 12
drwxr-xr-x 2 root root 4096 Sep 15 09:41 __pycache__
-rw-r--r-- 1 root root   43 Sep 15 09:21 test_example1.py
-rw-r--r-- 1 root root   43 Sep 15 09:21 test_example2.py
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

tests/modified_example1.py::modified_example1 PASSED
tests/test_example2.py::test_example2 PASSED

=================================================================================================================== 2 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook#
```

## 案例三：收集统计信息

### 目标

在测试项收集过程中统计特定类型的测试项信息，用于生成报告。

### 步骤

1. 在 `pytest_itemcollected` 钩子中定义统计逻辑。
2. 统计过程中记录相关信息，用于后续生成报告。

### 示例代码

```python
# conftest.py
import pytest

collected_items = []

def pytest_itemcollected(item):
    # 收集统计信息
    collected_items.append(item.nodeid)

# 生成报告
def pytest_sessionfinish(session, exitstatus):
    with open('collected_items_report.txt', 'w') as f:
        f.write("\n".join(collected_items))

# 示例测试文件 `tests/test_example1.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_example2.py`
def test_example2():
    assert 2 + 2 == 4
```

**说明**：

- 使用 `pytest_itemcollected` 钩子收集每个测试项的节点 `ID` 信息。
- 在 `pytest_sessionfinish` 钩子中生成统计报告文件，将收集到的信息写入报告。

### 运行和验证

确保目录结构如下：

```shell
tests/
    ├── test_example1.py
    ├── test_example2.py
conftest.py
```

运行`pytest`来验证新的测试设置，并检查生成的报告文件：

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
drwxr-xr-x 5 root root 4096 Sep 15 09:58 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root   75 Sep 15 09:58 collected_items_report.txt
-rw-r--r-- 1 root root  296 Sep 15 09:58 conftest.py
drwxr-xr-x 2 root root 4096 Sep 15 09:58 __pycache__/
drwxr-xr-x 3 root root 4096 Sep 15 09:58 .pytest_cache/
drwxr-xr-x 3 root root 4096 Sep 15 09:41 tests/
root@Gavin:~/test/hook# cat collected_items_report.txt 
tests/test_example1.py::test_example1
tests/test_example2.py::test_example2
```

### 验证生成的文件

**报告文件 `collected_items_report.txt`**
- 查看该文件，应包含所有收集到的测试项的节点 `ID` 信息。

### 详细解释

1. **钩子函数**
    - `pytest_sessionstart`：在测试会话开始时记录日志，标识测试会话启动。
    - `pytest_itemcollected`：在每个测试项收集到后调用，记录测试项信息或进行动态处理。

2. **统计和报告**
    - 在 `pytest_itemcollected` 中统计收集到的测试项信息，在 `pytest_sessionfinish` 中生成报告文件并写入统计信息。

# 结语

`pytest_itemcollected` 是一个非常有用的钩子，允许我们在每一个测试项被收集到后执行自定义逻辑。通过本文的案例，你可以了解如何使用 `pytest_itemcollected` 实现记录测试项信息、动态处理测试项以及收集统计信息等功能。在实际应用中，可以根据项目需求及测试场景对这些示例进行扩展和调整，从而实现更灵活的测试管理和调试。希望这篇文章能够帮助你更好地理解和使用 `pytest_itemcollected`。

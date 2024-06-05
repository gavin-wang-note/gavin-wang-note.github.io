---
title: pytest hook系列之pytest_deselected
date: 2024-09-17 23:00:00
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
summary: pytest hook之pytest_deselected
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_deselected` 是`pytest`框架中的一个钩子函数，允许我们在测试用例被取消选择（`deselected`）时执行自定义逻辑。利用这个钩子函数，我们可以记录那些被取消选择而未执行的测试用例，联合调试信息以及生成报告等操作，从而更好地监控和管理测试用例的执行情况。本篇文章将详细介绍 `pytest_deselected` 的使用场景、参数，并通过具体案例展示其应用。

# 什么是pytest_deselected？

`pytest_deselected` 是一个`pytest`提供的钩子函数，它在测试用例被取消选择时调用。通过这个钩子，我们可以获取所有被取消选择的测试用例列表，并根据这些信息执行进一步的处理，如日志记录、报告生成或调试输出。

# 使用场景

1. **记录取消选择的测试用例信息**：记录那些被取消选择的测试用例，便于后续分析和跟踪。
2. **生成取消选择的测试用例报告**：生成一个包含所有被取消选择测试用例的报告，有助于可以了解哪些测试用例被忽略。
3. **调试和分析**：获取被取消选择的测试用例信息以便调试和分析测试选择策略。

# 参数

```python
def pytest_deselected(items):
    # items: 被取消选择的测试用例列表
    pass
```

- `items`：被取消选择的测试用例列表，每个元素是一个测试项对象，表示一个具体的测试用例。

# 示例代码

## 案例一：记录取消选择的测试用例信息

目标：在测试用例被取消选择时记录这些测试用例的信息，便于后续分析和跟踪。

步骤：

1. 在 `pytest_deselected` 钩子中处理取消选择的测试用例列表。
2. 将测试用例的信息记录到日志文件中。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='deselected_tests.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_collection_modifyitems(config, items):
    deselected = []
    selected = []

    for item in items:
        if "test_example2" in item.nodeid:
            deselected.append(item)
        else:
            selected.append(item)

    config.hook.pytest_deselected(items=deselected)
    items[:] = selected

def pytest_deselected(items):
    # 记录取消选择的测试用例信息
    for item in items:
        logging.info(f"Deselected test item: {item.nodeid}")

# 示例测试文件 `tests/test_example1.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_example2.py`
def test_example2():
    assert 2 + 2 == 4

# 示例测试文件 `tests/test_example3.py`
def test_example3():
    assert 3 + 3 == 6
```

**注释**：

- 配置基本日志记录，在 `pytest_deselected` 钩子中通过 `logging.info` 记录每个被取消选择的测试用例信息。


运行效果：

```shell
root@Gavin:~/test/hook# tree
.
├── conftest.py
└── tests
    ├── test_example1.py
    ├── test_example2.py
    └── test_example3.py

2 directories, 4 files
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
collected 3 items / 1 deselected / 2 selected                                                                                                                                                                                                           

tests/test_example1.py::test_example1 PASSED
tests/test_example3.py::test_example3 PASSED

============================================================================================================ 2 passed, 1 deselected in 0.04s ============================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Jun  1 10:52 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  638 Jun  1 10:51 conftest.py
-rw-r--r-- 1 root root   86 Jun  1 10:52 deselected_tests.log
drwxr-xr-x 2 root root 4096 Jun  1 10:52 __pycache__/
drwxr-xr-x 3 root root 4096 Jun  1 10:52 .pytest_cache/
drwxr-xr-x 3 root root 4096 Jun  1 10:52 tests/
root@Gavin:~/test/hook# cat deselected_tests.log 
2024-06-01 10:52:00,883 - Deselected test item: tests/test_example2.py::test_example2
root@Gavin:~/test/hook# 
root@Gavin:~/test/hook# 
```

## 案例二：生成取消选择的测试用例报告

目标：生成一个包含所有被取消选择测试用例的报告，有助于了解哪些测试用例被忽略。

步骤：

1. 在 `pytest_deselected` 钩子中处理取消选择的测试用例列表。
2. 将测试用例的信息写入报告文件中。

示例代码：

```python
# conftest.py
import pytest

deselected_items = []
selected_items = []

def pytest_collection_modifyitems(config, items):
    deselected = []
    selected = []

    for item in items:
        if "test_example2" in item.nodeid:
            deselected.append(item)
        else:
            selected.append(item)
            selected_items.append(item.nodeid)  # 记录被选择的测试用例

    config.hook.pytest_deselected(items=deselected)
    items[:] = selected

def pytest_deselected(items):
    # 收集取消选择的测试用例信息
    for item in items:
        deselected_items.append(item.nodeid)

def pytest_sessionfinish(session, exitstatus):
    # 生成报告
    with open('deselected_tests_report.txt', 'w') as f:
        f.write("Deselected test items:\n")
        for nodeid in deselected_items:
            f.write(f"{nodeid}\n")
    
    # 生成被选择用例的报告
    with open('selected_tests_report.txt', 'w') as f:
        f.write("Selected test items:\n")
        for nodeid in selected_items:
            f.write(f"{nodeid}\n")

# 示例测试文件 `tests/test_example1.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_example2.py`
def test_example2():
    assert 2 + 2 == 4

# 示例测试文件 `tests/test_example3.py`
def test_example3():
    assert 3 + 3 == 6
```

**注释**：

- 在 `pytest_deselected` 钩子中收集每个被取消选择的测试项的节点 ID 信息。
- 在 `pytest_sessionfinish` 钩子中生成报告文件 `deselected_tests_report.txt`，将所有被取消选择的测试项信息写入报告。

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
collected 3 items / 1 deselected / 2 selected                                                                                                                                                                                                           

tests/test_example1.py::test_example1 PASSED
tests/test_example3.py::test_example3 PASSED

============================================================================================================ 2 passed, 1 deselected in 0.04s ============================================================================================================
root@Gavin:~/test/hook# ll
total 32
drwxr-xr-x 5 root root 4096 Jun  1 11:03 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root 1053 Jun  1 11:03 conftest.py
-rw-r--r-- 1 root root   61 Jun  1 11:03 deselected_tests_report.txt
drwxr-xr-x 2 root root 4096 Jun  1 11:03 __pycache__/
drwxr-xr-x 3 root root 4096 Jun  1 10:52 .pytest_cache/
-rw-r--r-- 1 root root   97 Jun  1 11:03 selected_tests_report.txt
drwxr-xr-x 3 root root 4096 Jun  1 10:52 tests/
root@Gavin:~/test/hook# cat deselected_tests_report.txt 
Deselected test items:
tests/test_example2.py::test_example2
root@Gavin:~/test/hook# cat selected_tests_report.txt 
Selected test items:
tests/test_example1.py::test_example1
tests/test_example3.py::test_example3
root@Gavin:~/test/hook# 
```

## 案例三：调试和分析取消选择的测试用例

目标：获取被取消选择的测试用例信息，以便调试和分析测试选择策略。

步骤：

1. 在 `pytest_deselected` 钩子中处理取消选择的测试用例列表。
2. 输出取消选择的测试用例信息，便于调试和分析。

示例代码：

```python
# conftest.py
import pytest

def pytest_deselected(items):
    # 输出取消选择的测试用例信息
    print("Deselected test items:")
    for item in items:
        print(f"- {item.nodeid}")

# 示例测试文件 `tests/test_example1.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_example2.py`
def test_example2():
    assert 2 + 2 == 4

# 示例测试文件 `tests/test_example3.py`
def test_example3():
    assert 3 + 3 == 6
```

**注释**：

- 在 `pytest_deselected` 钩子中，通过 `print` 输出每个被取消选择的测试项的节点 ID 信息，便于在调试和分析时查看。

### 运行和验证

确保目录结构如下：
```shell
tests/
    ├── test_example1.py
    ├── test_example2.py
    ├── test_example3.py
conftest.py
```

运行pytest，并使用 `-k` 选项进行测试用例过滤：

```shell
root@Gavin:~/test/hook# pytest -s -v -k "not test_example2"
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collecting ... Deselected test items:
- tests/test_example2.py::test_example2
collected 3 items / 1 deselected / 2 selected                                                                                                                                                                                                           

tests/test_example1.py::test_example1 PASSED
tests/test_example3.py::test_example3 PASSED

============================================================================================================ 2 passed, 1 deselected in 0.04s ============================================================================================================
root@Gavin:~/test/hook# 
```

# 总结

`pytest_deselected` 是一个非常有用的钩子，允许我们在测试用例被取消选择时执行自定义逻辑。通过本文的案例，你可以看到如何使用 `pytest_deselected` 实现记录取消选择的测试用例信息、生成报告以及调试和分析测试选择策略等功能。在实际应用中，可以根据项目需求及测试场景对这些示例进行扩展和调整，从而实现更灵活的测试管理和调试。希望这篇文章能够帮助你更好地理解和使用 `pytest_deselected`。

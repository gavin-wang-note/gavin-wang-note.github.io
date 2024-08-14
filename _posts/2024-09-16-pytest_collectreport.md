---
title: pytest hook系列之pytest_collectreport
date: 2024-09-16 23:00:00
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
summary: pytest hook之pytest_collectreport
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_collectreport` 是`pytest`框架中的一个钩子函数，允许我们在测试用例收集结束后生成一个收集报告。利用这个钩子函数，我们可以获取收集过程中的详细信息，并据此生成日志、报告或执行其他操作，从而更好地监控和管理测试用例的收集过程。本篇文章将详细介绍 `pytest_collectreport` 的使用场景、参数，并通过具体案例展示其应用。

# 什么是pytest_collectreport？

`pytest_collectreport` 是一个`pytest`提供的钩子函数，它在每一个收集器（如文件、目录）产生收集报告后被调用。通过这个钩子，我们可以访问收集报告中的详细信息，并可以根据这些信息执行进一步的处理，如日志记录、报告生成或调试输出。

# 使用场景

1. **生成测试收集报表**：在测试收集阶段结束后生成详细的收集报表。
2. **记录收集过程的日志**：记录测试收集过程中出现的问题和详细信息，便于调试和分析。
3. **收集特定类型的错误信息**：在收集过程中检测和记录特定类型的错误，如收集失败的节点信息。

 参数

```python
def pytest_collectreport(report):
    # report: 收集报告对象，包含收集过程中的详细信息，如节点、结果和错误信息
    pass
```

- `report`：收集报告对象，包含收集过程中的详细信息。这些信息包括收集的测试节点、收集结果（成功、失败等）和任何收集过程中产生的错误信息。

# 示例代码

## 案例一：生成测试收集报表

目标：在测试收集阶段结束后生成一个包含所有测试收集信息的报表。

步骤：

1. 在 `pytest_collectreport` 钩子中处理收集报告对象。
2. 将收集到的信息写入报表文件中。

示例代码：

```python
# conftest.py
import pytest

def pytest_collectreport(report):
    # 打开一个文件以追加模式记录收集报告
    with open('collect_report.txt', 'a') as f:
        f.write(f"Collect report for {report.nodeid}\n")
        f.write(f"Outcome: {report.outcome}\n")

        if report.outcome != 'passed':
            f.write("Errors:\n")
            for section, content in report.sections:
                if section == 'Captured stdout call':
                    f.write(f"STDOUT: {content}\n")
                elif section == 'Captured stderr call':
                    f.write(f"STDERR: {content}\n")
        
        f.write("\n")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

**注释**：

- `pytest_collectreport` 钩子中打开一个文件 `collect_report.txt`，并将每个收集报告的信息写入文件中。
- 记录每个收集器的节点 `ID` 和收集结果。如果收集未通过，还记录错误信息。

运行效果：

```shell
root@Gavin:~/test/hook# ll
total 24
drwxr-xr-x 5 root root 4096 Sep 16 10:15 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  630 Sep 16 10:15 conftest.py
drwxr-xr-x 2 root root 4096 Sep 16 09:58 __pycache__/
drwxr-xr-x 3 root root 4096 Sep 16 09:58 .pytest_cache/
drwxr-xr-x 3 root root 4096 Sep 16 09:41 tests/
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
drwxr-xr-x 5 root root 4096 Sep 16 10:15 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  235 Sep 16 10:15 collect_report.txt
-rw-r--r-- 1 root root  630 Sep 16 10:15 conftest.py
drwxr-xr-x 2 root root 4096 Sep 16 10:15 __pycache__/
drwxr-xr-x 3 root root 4096 Sep 16 09:58 .pytest_cache/
drwxr-xr-x 3 root root 4096 Sep 16 09:41 tests/
root@Gavin:~/test/hook# cat collect_report.txt 
Collect report for 
Outcome: passed

Collect report for tests/test_example1.py
Outcome: passed

Collect report for tests/test_example2.py
Outcome: passed

Collect report for tests
Outcome: passed

Collect report for .
Outcome: passed

root@Gavin:~/test/hook#
```

## 案例二：记录收集过程的日志

目标：在测试收集过程中记录详细的日志信息，便于调试和分析。

步骤：

1. 配置日志记录。
2. 在 `pytest_collectreport` 钩子中记录收集过程的详细信息。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='collect_process.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_collectreport(report):
    # 记录收集报告的详细信息
    logging.info(f"Collect report for: {report.nodeid}")
    logging.info(f"Outcome: {report.outcome}")

    if report.outcome != 'passed':
        logging.info("Errors:")
        for section, content in report.sections:
            if section == 'Captured stdout call':
                logging.info(f"STDOUT: {content}")
            elif section == 'Captured stderr call':
                logging.info(f"STDERR: {content}")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

**注释**：

- 配置基本日志记录，在 `pytest_collectreport` 钩子中通过 `logging.info` 记录每个收集报告的详细信息。

运行日志：

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
drwxr-xr-x 5 root root 4096 Sep 16 10:17 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  495 Sep 16 10:17 collect_process.log
-rw-r--r-- 1 root root  659 Sep 16 10:17 conftest.py
drwxr-xr-x 2 root root 4096 Sep 16 10:17 __pycache__/
drwxr-xr-x 3 root root 4096 Sep 16 09:58 .pytest_cache/
drwxr-xr-x 3 root root 4096 Sep 16 09:41 tests/
root@Gavin:~/test/hook# cat collect_process.log 
2024-09-16 10:17:22,908 - Collect report for: 
2024-09-16 10:17:22,908 - Outcome: passed
2024-09-16 10:17:22,911 - Collect report for: tests/test_example1.py
2024-09-16 10:17:22,911 - Outcome: passed
2024-09-16 10:17:22,911 - Collect report for: tests/test_example2.py
2024-09-16 10:17:22,911 - Outcome: passed
2024-09-16 10:17:22,912 - Collect report for: tests
2024-09-16 10:17:22,912 - Outcome: passed
2024-09-16 10:17:22,912 - Collect report for: .
2024-09-16 10:17:22,912 - Outcome: passed
root@Gavin:~/test/hook# 
```



## 案例三：收集特定类型的错误信息

目标：在收集过程中检测和记录特定类型的错误，如收集失败的节点信息。

步骤：

1. 在 `pytest_collectreport` 钩子中检查收集结果。
2. 将失败的节点信息和错误详情记录到文件中。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='collect_process.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_sessionstart(session):
    logging.info("Test session started")

def pytest_collectreport(report):
    # 记录收集报告的详细信息
    with open('collect_report.txt', 'a') as f:
        f.write(f"Collect report for: {report.nodeid}\n")
        f.write(f"Outcome: {report.outcome}\n")
    
        if report.outcome != 'passed':
            f.write("Errors:\n")
            for section, content in report.sections:
                if section == 'Captured stdout call':
                    f.write(f"STDOUT: {content}\n")
                elif section == 'Captured stderr call':
                    f.write(f"STDERR: {content}\n")
            f.write("\n")

    logging.info(f"Collect report for: {report.nodeid}")
    logging.info(f"Outcome: {report.outcome}")

    if report.outcome != 'passed':
        logging.info("Errors:")
        with open('collect_errors.txt', 'a') as f:
            f.write(f"Failed to collect {report.nodeid}\n")
            for section, content in report.sections:
                if section == 'Captured stdout call':
                    f.write(f"STDOUT: {content}\n")
                    logging.info(f"STDOUT: {content}")
                elif section == 'Captured stderr call':
                    f.write(f"STDERR: {content}\n")
                    logging.info(f"STDERR: {content}")
            f.write("\n")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert False  # This will intentionally fail to test error collection
```

**注释**：

- `pytest_collectreport` 钩子中检查收集结果是否未通过，如果是，则将失败的节点信息和错误详情记录到文件 `collect_errors.txt` 中。

### 运行和验证

确保目录结构如下：
```shell
tests/
    ├── test_example.py
conftest.py
```

运行 `pytest` 来验证新的测试设置，并检查生成的日志文件和报告文件：

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
collected 3 items                                                                                                                                                                                                                                       

tests/test_example.py::test_example1 FAILED
tests/test_example1.py::test_example1 PASSED
tests/test_example2.py::test_example2 PASSED

======================================================================================================================= FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example1 _____________________________________________________________________________________________________________________

    def test_example1():
>       assert False  # This will intentionally fail to test error collection
E       assert False

tests/test_example.py:2: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_example1 - assert False
============================================================================================================== 1 failed, 2 passed in 0.11s ==============================================================================================================
root@Gavin:~/test/hook# ll
total 32
drwxr-xr-x 5 root root 4096 Sep 16 10:27 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  652 Sep 16 10:27 collect_process.log
-rw-r--r-- 1 root root  293 Sep 16 10:27 collect_report.txt
-rw-r--r-- 1 root root 1520 Sep 16 10:26 conftest.py
drwxr-xr-x 2 root root 4096 Sep 16 10:27 __pycache__/
drwxr-xr-x 3 root root 4096 Sep 16 10:19 .pytest_cache/
drwxr-xr-x 3 root root 4096 Sep 16 10:19 tests/
root@Gavin:~/test/hook# cat collect_process.log 
2024-09-16 10:27:01,651 - Test session started
2024-09-16 10:27:01,673 - Collect report for: 
2024-09-16 10:27:01,673 - Outcome: passed
2024-09-16 10:27:01,676 - Collect report for: tests/test_example.py
2024-09-16 10:27:01,676 - Outcome: passed
2024-09-16 10:27:01,677 - Collect report for: tests/test_example1.py
2024-09-16 10:27:01,677 - Outcome: passed
2024-09-16 10:27:01,678 - Collect report for: tests/test_example2.py
2024-09-16 10:27:01,678 - Outcome: passed
2024-09-16 10:27:01,678 - Collect report for: tests
2024-09-16 10:27:01,678 - Outcome: passed
2024-09-16 10:27:01,678 - Collect report for: .
2024-09-16 10:27:01,678 - Outcome: passed
root@Gavin:~/test/hook# cat collect_report.txt 
Collect report for: 
Outcome: passed
Collect report for: tests/test_example.py
Outcome: passed
Collect report for: tests/test_example1.py
Outcome: passed
Collect report for: tests/test_example2.py
Outcome: passed
Collect report for: tests
Outcome: passed
Collect report for: .
Outcome: passed
root@Gavin:~/test/hook#
```

### 验证生成的文件

1. **报表文件 `collect_report.txt`**
    - 查看该文件，应包含所有测试收集报告的信息。

2. **日志文件 `collect_process.log`**
    - 查看该文件，应包含测试收集过程的详细日志信息。

3. **错误文件 `collect_errors.txt`**
    - 查看该文件，应包含失败收集的节点信息和错误详情。

### 详细解释

1. **配置日志记录**
    - 使用 `logging.basicConfig` 配置日志文件名、日志级别和日志格式，确保在整个 pytest 会话中日志记录正常工作。

2. **钩子函数**
    - `pytest_collectreport`：在每一个收集器生成收集报告后调用，通过这个钩子可以获取收集过程中的详细信息并执行自定义逻辑。

3. **具体场景应用**
    - **生成测试收集报表**：收集报告生成后将信息写入文件中，便于后续查看和分析。
    - **记录收集过程的日志**：在收集过程中记录详细的日志信息，帮助调试和分析收集阶段的问题。
    - **收集特定类型的错误信息**：检测和记录收集失败的节点信息，便于排查问题。

# 结语

`pytest_collectreport` 是一个非常有用的钩子，允许我们在每一个收集器生成收集报告后执行自定义逻辑。通过本文的案例，你可以了解如何使用 `pytest_collectreport` 实现生成测试收集报表、记录收集过程的日志和检测特定类型错误等功能。在实际应用中，可以根据项目需求及测试场景对这些示例进行扩展和调整，从而实现更灵活的测试管理和调试。希望这篇文章能够帮助你更好地理解和使用 `pytest_collectreport`。

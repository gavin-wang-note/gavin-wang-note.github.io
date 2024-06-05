---
title: pytest hook系列之pytest_collection_finish
date: 2024-09-11 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-18.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_collection_finish
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_collection_finish`是`pytest`框架中的一个钩子函数，当测试用例收集过程完成时触发。通过使用这个钩子函数，我们可以在收集完成后进行一些统计、记录或报告等操作。本篇文章将详细介绍`pytest_collection_finish`的使用场景、参数，并通过具体案例展示其应用。

# 什么是 pytest_collection_finish？

`pytest_collection_finish`是一个`pytest`提供的钩子函数，它在所有测试用例收集完毕后立即调用。使用这个钩子，我们可以获取已经收集到的测试用例列表，并对其进行处理或统计。

# 使用场景

* 收集统计信息：统计收集到的测试用例的数量和分布情况。
* 生成报告：在收集完成后生成一个包含所有测试用例的信息报告。
* 自定义日志记录：记录测试用例的收集过程和结果，用于调试或审计。


参数

```python
def pytest_collection_finish(session):
    # session: 当前 pytest 会话对象，包含配置信息和收集到的测试用例
    pass


    session：当前 pytest 会话对象，包含配置信息和已经收集到的测试用例。
```

# 示例代码

## 案例一：收集统计信息

目标：统计收集到的测试用例的数量和分布情况，并在收集完成后打印统计信息。

步骤：

* 使用`pytest_collection_finish`钩子获取收集到的测试用例列表。
* 统计测试用例的数量和分布情况。
* 打印统计信息。


示例代码：

```python
# conftest.py
import pytest

def pytest_collection_finish(session):
    total_tests = len(session.items)
    print(f"Total collected tests: {total_tests}")

    # 统计每个文件的测试用例数量
    file_test_count = {}
    for item in session.items:
        file_name = item.fspath
        if file_name not in file_test_count:
            file_test_count[file_name] = 0
        file_test_count[file_name] += 1

    for file_name, count in file_test_count.items():
        print(f"File {file_name}: {count} tests")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4

def test_example3():
    assert 3 + 3 == 6
```

运行效果：

```shell
root@Gavin:~/test/hook# pytest
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 3 items                                                                                                                                                                                                                                       
Total collected tests: 3
File /root/test/hook/test_example.py: 3 tests

test_example.py ...                                                                                                                                                                                                                               [100%]

=================================================================================================================== 3 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# 
```

**说明：**

* `pytest_collection_finish`钩子中，通过`session.items`获取收集到的所有测试用例? 
* 统计每个测试文件中的测试用例数量，并打印结果。


## 案例二：生成测试用例报告

目标：在收集完成后生成一个包含所有测试用例信息的报告文件。

步骤：

* 使用`pytest_collection_finish`钩子获取收集到的测试用例列表。
* 将测试用例信息写入报告文件。


示例代码：

```python
# conftest.py
import pytest

def pytest_collection_finish(session):
    report_lines = ["Collected test cases:\n"]
    for item in session.items:
        report_lines.append(f"{item.nodeid}\n")

    report_file = "test_collection_report.txt"
    with open(report_file, "w") as f:
        f.writelines(report_lines)
    print(f"Test collection report generated: {report_file}")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4

def test_example3():
    assert 3 + 3 == 6
```


运行效果：

```shell
root@Gavin:~/test/hook# pytest
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 3 items                                                                                                                                                                                                                                       
Test collection report generated: test_collection_report.txt

test_example.py ...                                                                                                                                                                                                                               [100%]

=================================================================================================================== 3 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# 
```


**说明：**

* `pytest_collection_finish`钩子中，通过`session.items`获取所有收集到的测试用例。
* 将每个测试用例的节点`ID`写入一个报告文件`test_collection_report.txt`并生成报告。


## 案例三：自定义日志记录

目标：在收集完成后记录日志，包含测试用例的收集情况和统计信息。

步骤：

* 使用`pytest_collection_finish`钩子获取收集到的测试用例列表。
* 记录日志文件，包含测试用例的收集信息和统计数据。


示例代码：

```python
# conftest.py
import pytest
import logging

def pytest_sessionstart(session):
    logging.basicConfig(filename='test_collection.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    logging.info("Test session started")

def pytest_collection_finish(session):
    logging.info("Collected test cases:")
    total_tests = len(session.items)
    logging.info(f"Total collected tests: {total_tests}")

    for item in session.items:
        logging.info(f"Collected: {item.nodeid}")

    logging.info("Test collection finished")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4

def test_example3():
    assert 3 + 3 == 6
```



运行效果：

```shell
root@Gavin:~/test/hook# pytest
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 3 items                                                                                                                                                                                                                                       

test_example.py ...                                                                                                                                                                                                                               [100%]

=================================================================================================================== 3 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# cat test_
test_collection_report.txt  test_example.py             
root@Gavin:~/test/hook# cat test_collection_report.txt 
Collected test cases:
test_example.py::test_example1
test_example.py::test_example2
test_example.py::test_example3
root@Gavin:~/test/hook#
```


**说明：**

* `pytest_sessionstart`钩子用来配置日志文件，并记录测试会话的开始时间。
* 在`pytest_collection_finish`钩子中记录每个收集到的测试用例的节点`ID`，以及收集完成的总数和其他信息。


# 结语

`pytest_collection_finish`是一个非常有用的`pytest`钩子，能够在测试用例收集完成后提供多种操作可能。通过本文的案例，你可以了解如何使用`pytest_collection_finish`来统计信息、生成报告和记录日志。在实际应用中，可以根据项目需求及测试场景对这些示例进行扩展和调整。


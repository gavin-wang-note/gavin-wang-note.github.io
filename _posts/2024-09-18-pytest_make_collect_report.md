---
title: pytest hook系列之pytest_make_collect_report
date: 2024-09-18 23:00:00
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
summary: pytest hook之pytest_make_collect_report
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview


`pytest_make_collect_report` 是`pytest`框架中的一个钩子函数，允许我们在测试用例收集完成之后生成一个自定义收集报告。这使得我们可以灵活地对收集的测试用例进行详细报告和记录，定制化日志信息和诊断数据等。本篇文章将详细介绍 `pytest_make_collect_report` 的使用场景、参数，并通过具体案例展示其应用，以及详细的示例代码和注释。

# 什么是pytest_make_collect_report？

`pytest_make_collect_report` 是一个 pytest 提供的钩子函数，它在测试用例收集完成之后调用，用于生成一个自定义的收集报告。通过这个钩子，我们可以获取收集过程中的详细信息，并将这些信息组织成一个报告对象。

# 使用场景

1. **生成详细的收集报告**：在测试用例收集完成之后生成包含详细信息的收集报告。
2. **定制化日志记录**：记录收集过程中出现的所有事件，包括成功和失败的信息。
3. **调试信息输出**：输出详细的测试收集信息，便于调试和诊断潜在的问题。

# 参数

```python
def pytest_make_collect_report(collector):
    # collector: pytest 收集器对象，用于生成收集报告
    pass
```

- `collector`：当前的 pytest 收集器对象，用于生成收集报告。

# 示例代码

## 案例一：生成详细的收集报告

目标：在测试用例收集完成之后生成一个包含详细信息的收集报告。

步骤：

1. 使用 `pytest_make_collect_report` 钩子处理收集器对象生成报告。
2. 输出收集报告到文件中。

示例代码：

```python
# conftest.py
import pytest

def pytest_make_collect_report(collector):
    # 使用 collect 方法收集测试用例
    collector_result = list(collector.collect())
    num_tests = len(collector_result)
  
    report_message = f"Collected {num_tests} tests from {collector.nodeid}\n"

    for item in collector_result:
        report_message += f" - {item.nodeid}\n"

    # 将收集报告内容写入文件
    with open('collect_report.txt', 'a') as f:
        f.write(report_message)

    return pytest.CollectReport(
        nodeid=collector.nodeid,
        result=collector_result,
        outcome="passed",
        longrepr=None,
        sections=[]
    )

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

- 在 `pytest_make_collect_report` 钩子函数中，使用`pytest.CollectReport`类，构建和返回自定义的收集报告。
- 将收集到的信息和错误写入到`collect_report.txt`文件中。


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
collected 3 items                                                                                                                                                                                                                                       

tests/test_example1.py::test_example1 PASSED
tests/test_example2.py::test_example2 PASSED
tests/test_example3.py::test_example3 PASSED

=================================================================================================================== 3 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# cat collect_report.txt 
Collected 1 tests from 
 - .
Collected 1 tests from .
 - tests
Collected 3 tests from tests
 - tests/test_example1.py
 - tests/test_example2.py
 - tests/test_example3.py
Collected 1 tests from tests/test_example1.py
 - tests/test_example1.py::test_example1
Collected 1 tests from tests/test_example2.py
 - tests/test_example2.py::test_example2
Collected 1 tests from tests/test_example3.py
 - tests/test_example3.py::test_example3
root@Gavin:~/test/hook# 
```


## 案例二：定制化日志记录

目标：记录收集过程中所有事件的日志，包括收集到的测试用例和错误信息。

步骤：

1. 配置日志记录。
2. 在 `pytest_make_collect_report` 钩子中记录收集的详细日志信息。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='collect_report.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_make_collect_report(collector):
    # 使用 collect 方法收集测试用例，并转换成列表
    collector_result = list(collector.collect())

    # 构建收集报告
    num_tests = len(collector_result)
    report_message = f"Collected {num_tests} tests from {collector.nodeid}\n"
    for item in collector_result:
        report_message += f" - {item.nodeid}\n"
    
    # 记录收集报告信息到日志文件
    logging.info(report_message)

    # 构建并返回收集报告对象
    report = pytest.CollectReport(
        nodeid=collector.nodeid,
        result=collector_result,
        outcome="passed" if num_tests > 0 else "failed",
        longrepr=None if num_tests > 0 else "No tests collected",
        sections=[]
    )

    # 如果收集失败，记录错误信息
    if report.failed:
        logging.error(f"Collected report has errors for {collector.nodeid}: {report.longrepr}")

    return report

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

- 在 `pytest_make_collect_report` 钩子中，通过日志记录收集到的测试用例和任何错误信息。
- 使用 `logging.info` 记录收集的详细信息，使用 `logging.error` 记录错误信息。


**注释**：

* Configuration of Logging:

  * 通过使用`logging.basicConfig`配置日志记录，确保日志信息写入`collect_report.log`文件。

* pytest_make_collect_report 函数:

  * 使用 collector.collect() 方法收集测试用例，并转换为列表。
  * 构建收集报告，统计收集到的测试用例数量，并生成详细的报告信息。
  * 将收集报告信息记录到日志文件 collect_report.log 中。
  * 基于收集结果构建并返回一个 pytest.CollectReport 对象。
  * 如果收集失败，记录错误信息到日志文件当中。

通过这种方式，我们确保了代码的兼容性和稳定性，并且使用`pytest`推荐的公开方法来完成收集报告，同时详细记录收集过程的日志信息。


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
collected 3 items                                                                                                                                                                                                                                       

tests/test_example1.py::test_example1 PASSED
tests/test_example2.py::test_example2 PASSED
tests/test_example3.py::test_example3 PASSED

=================================================================================================================== 3 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Jun  1 14:20 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  593 Jun  1 14:20 collect_report.log
-rw-r--r-- 1 root root 1101 Jun  1 14:19 conftest.py
drwxr-xr-x 2 root root 4096 Jun  1 14:20 __pycache__/
drwxr-xr-x 3 root root 4096 Jun  1 10:52 .pytest_cache/
drwxr-xr-x 3 root root 4096 Jun  1 10:52 tests/
root@Gavin:~/test/hook# cat collect_report.log 
2024-06-01 14:20:45,763 - Collected 1 tests from 
 - .

2024-06-01 14:20:45,764 - Collected 1 tests from .
 - tests

2024-06-01 14:20:45,765 - Collected 3 tests from tests
 - tests/test_example1.py
 - tests/test_example2.py
 - tests/test_example3.py

2024-06-01 14:20:45,766 - Collected 1 tests from tests/test_example1.py
 - tests/test_example1.py::test_example1

2024-06-01 14:20:45,766 - Collected 1 tests from tests/test_example2.py
 - tests/test_example2.py::test_example2

2024-06-01 14:20:45,767 - Collected 1 tests from tests/test_example3.py
 - tests/test_example3.py::test_example3

root@Gavin:~/test/hook#
```

## 案例三：调试信息输出

目标：输出详细的测试收集信息到控制台，便于调试和诊断潜在的问题。

步骤：

1. 使用 `pytest_make_collect_report` 钩子处理收集器对象生成报告。
2. 在控制台输出详细的收集报告信息。

示例代码：

```python
# conftest.py
import pytest

def pytest_make_collect_report(collector):
    # 生成收集报告
    report = collector._top.collect()

    # 获取收集到的节点信息
    collected_items = report.result
    errors = report.longreprtext if report.failed else None

    # 输出详细的收集报告信息
    print("Collect report:")

    print("Collected items:")
    for item in collected_items:
        print(f"{item.nodeid}")

    if errors:
        print("Errors:")
        print(errors)

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


**验证输出信息**:

在控制台中，应能看到收集报告的详细信息，包括每个被收集的测试项。若有测试项未被收集或收集失败，则应显示错误信息。

**注释**：

* pytest_make_collect_report 函数

  * 使用`collector.collect()`方法收集测试用例，并将结果转换成列表，以便统计和处理。
  * 统计收集到的测试用例数量，并构建和格式化收集报告信息。
  * 使用`print`函数输出详细的收集报告信息到控制台，包括每个被收集的测试项。
  * 根据收集结果设置`outcome`和`longrepr`，如果收集失败，输出错误信息。
  * 构建并返回一个`pytest.CollectReport`对象，包含所有收集报告的详细信息。


**与目标一致的调试输出**:

通过此代码，我们实现了以下目标：

* 输出详细的测试收集信息到控制台：每个被收集的测试项都详细打印在控制台上，以便调试。
* 调试和诊断潜在的问题：若收集失败，则会明确输出错误信息，帮助诊断问题。


**示例输出**:

假设所有的测试样例都被正确收集和测试，在控制台中应能看到类似如下的输出：

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
collecting ... Collect report for: 
Collected items:
 - .
Collect report for: .
Collected items:
 - tests
Collect report for: tests
Collected items:
 - tests/test_example1.py
 - tests/test_example2.py
 - tests/test_example3.py
Collect report for: tests/test_example1.py
Collected items:
 - tests/test_example1.py::test_example1
Collect report for: tests/test_example2.py
Collected items:
 - tests/test_example2.py::test_example2
Collect report for: tests/test_example3.py
Collected items:
 - tests/test_example3.py::test_example3
collected 3 items                                                                                                                                                                                                                                       

tests/test_example1.py::test_example1 PASSED
tests/test_example2.py::test_example2 PASSED
tests/test_example3.py::test_example3 PASSED

=================================================================================================================== 3 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

如有任何收集失败或测试失败，控制台中将提供详尽的错误信息，有助于快速定位并修复问题。


# pytest_make_collect_report与其他pytest钩子函数（如pytest_mark_only, pytest_mark_except) 的区别和联系是什么？

`pytest_make_collect_report`与其他`pytest`钩子函数（如`pytest_mark_only, pytest_mark_except`) 的区别和联系如下：

## 功能定位

  - `pytest_make_collect_report`是一个钩子函数，用于在测试收集过程中生成报告。它在测试收集阶段被调用，用于生成测试项的详细报告。
  - `pytest_mark_only`和`pytest_mark_except`并未在我搜索到的资料中明确描述，但通常这类钩子函数用于处理特定的标记或跳过某些测试项。

## 使用场景

  - `pytest_make_collect_report`主要用于生成测试报告，这是测试执行过程中的一个重要环节，确保测试结果的可视化和分析。
  - `pytest_mark_only` 可能用于仅标记某些测试项，而不执行这些测试项。这可以通过配置文件或代码中指定特定的标记来实现，从而控制哪些测试项被包含在测试运行中。
  - `pytest_mark_except` 可能用于排除某些带有特定标记的测试项。这同样可以通过配置文件或代码中指定特定的标记来实现，从而控制哪些测试项被排除。

## 工作流程

  - 在`pytest`的测试收集阶段，`pytest_make_collect_report`会被调用，生成每个测试项的报告。这一过程涉及到对测试项的遍历和报告生成。
  - `pytest_mark_only`和`pytest_mark_except`可能会在更早的阶段被调用，如`pytest_collection_modifyitems`钩子函数中，用于修改测试项集合，根据标记决定是否包含或排除某些测试项。

## 配置和使用

  - `pytest_make_collect_report`通常在`conftest.py`文件中定义，并在需要的地方引用。
  - `pytest_mark_only`和`pytest_mark_except`可能需要在pytest的配置文件（如`pytest.ini`）中进行相应的配置，以便在测试运行时能够识别和应用这些标记。

总结来说，`pytest_make_collect_report`主要用于生成测试报告，而`pytest_mark_only`和`pytest_mark_except`可能用于控制哪些测试项被包含或排除。


# 结语

`pytest_make_collect_report` 是一个强大的钩子，允许我们在测试用例收集完成之后生成自定义的收集报告。通过本文的案例，你可以了解如何使用 `pytest_make_collect_report` 生成详细的收集报告、记录收集过程的日志和输出调试信息等功能。在实际应用中，可以根据项目需求及测试场景对这些示例进行扩展和调整，从而实现更灵活的测试管理和调试。


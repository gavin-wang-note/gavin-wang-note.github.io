---
title: 测试用例持续时间之pytest-extra-durations源码解读
date: 2026-02-28 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-26.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 测试用例持续时间之pytest-extra-durations源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest`默认自带`pytest_durations`插件，常用于统计用例运行时间，比如写完一个项目的自动化用例之后，发现有些用例运行较慢，影响整体的用例运行速度，即可使用`pytest_durations`插件的`--durations` 参数可以统计出每个用例运行的时间，对用例的时间做个排序。

今天，看到另外一个插件`pytest-extra-durations`，[官网网站](https://pypi.org/project/pytest-extra-durations/)介绍如下：

A pytest plugin to get durations on a per-function basis and per module basis.

意思是说这个插件旨在为 `pytest` 提供额外的测试时长报告功能，具体包括模块级别和函数级别的时长报告，以及所有测试的总时长报告。

但官方也说了:`Integration with line_profiler `，但是我又找到了类似此功能的另外一个插件`pytest-line-profiler/`，有兴趣的可访问[此地址](https://pypi.org/project/pytest-line-profiler/).

具体需要使用哪个插件，看使用者需求，在我看来，`pytest_durations`插件足够了，因为在实际测试用例的`function call`中，各个函数都会记录日志，再结合`Allure`报告中的时间线查找哪个用例耗时，自然就能找到对应函数哪里耗时异常。

# pytest-extra-durations和pytest-durations插件的异同点

| 特性/插件       | pytest-extra-durations                                      | pytest-durations                                                   |
|-----------------|------------------------------------------------------------|---------------------------------------------------------------------|
| **主要功能**     | 提供额外的测试持续时间报告                                 | 测量测试、`setup、teardown` 以及 `fixture` 的执行时间                 |
| **安装方式**     | 通常通过 pip 安装                                           | 通常通过 pip 安装                                                 |
| **命令行选项**   | `--modules-durations` 和 `--functions-durations`          | 具体选项根据其实现可能有所不同，但可能包括用于设置报告阈值的选项 |
| **持续时间测量** | 针对模块和测试函数的持续时间                                | 针对单个测试用例、测试用例的 `setup/teardown`、以及 `fixture` 的 `setup/teardown` |
| **报告内容**     | 显示最慢的 N 个模块和测试函数的持续时间                     | 可以报告单个测试用例的详细持续时间，以及 `fixture` 的持续时间         |
| **排序和筛选**   | 允许通过命令行选项设置显示条目的数量（N 或 0 表示所有）   | 可能提供更详细的持续时间数据，包括测试和 `fixture` 的时间              |
| **集成**         | 作为一个独立的插件工作                                     | 可能需要与 `pytest` 或其他插件集成以提供其功能                        |
| **使用场景**     | 当需要快速查看最慢的模块或测试函数时使用                   | 当需要对测试性能进行深入分析时使用                                |
| **配置**         | 通过命令行选项进行配置                                     | 可能需要在 `pytest` 配置文件中进行配置                              |

简而言之：

- 这两个插件的功能有一些重叠，但也有不同的侧重点。
- `pytest-extra-durations` 主要致力于显示执行时间最长的测试，适合那些需要关注长时间运行测试的用户。
- `pytest-durations` 则不仅显示最长的测试，还显示最短的测试，更加全面。


# 源码解读

## 源码目录结构

下载源码下来看看：

```shell
root@Gavin:~/pytest_plugin# cd pytest-extra-durations-0.1.3/
root@Gavin:~/pytest_plugin/pytest-extra-durations-0.1.3# ll
total 44
drwxr-xr-x  3 1001 rtkit 4096 Apr 21  2020 ./
drwxr-xr-x 10 root root  4096 Jul 15 11:39 ../
-rw-r--r--  1 1001 rtkit 1088 Apr 21  2020 LICENSE
-rw-r--r--  1 1001 rtkit   96 Apr 21  2020 MANIFEST.in
-rw-r--r--  1 1001 rtkit 4173 Apr 21  2020 PKG-INFO
drwxr-xr-x  2 1001 rtkit 4096 Apr 21  2020 pytest_extra_durations.egg-info/
-rw-r--r--  1 1001 rtkit 3344 Apr 21  2020 pytest_extra_durations.py
-rw-r--r--  1 1001 rtkit 2321 Apr 21  2020 README.md
-rw-r--r--  1 1001 rtkit   38 Apr 21  2020 setup.cfg
-rw-r--r--  1 1001 rtkit 1621 Apr 21  2020 setup.py
root@Gavin:~/pytest_plugin/pytest-extra-durations-0.1.3# cd pytest_extra_durations.egg-info/
root@Gavin:~/pytest_plugin/pytest-extra-durations-0.1.3/pytest_extra_durations.egg-info#
```

## 核心文件pytest_extra_durations.py

## 导入模块

```python
from collections import defaultdict
```

- **`defaultdict`**：从 `collections` 模块导入 `defaultdict`，用于自动初始化值的字典。

## 添加命令行选项

```python
def pytest_addoption(parser):
    parser.addoption(
        "--modules-durations",
        action="store",
        type=int,
        default=None,
        metavar="N",
        help="Shows the N slowest modules durations (N=0 for all). "
        "A module duration is the sum of the durations of all its tests, "
        "setups and teardowns.",
    )

    parser.addoption(
        "--functions-durations",
        action="store",
        type=int,
        default=None,
        metavar="N",
        help="Shows the N slowest test functions durations (N=0 for all). "
        "This is different from the --durations argument. --durations works on "
        "a per-test basis, but a test function can produce multiple tests. "
        "This gives the sum of all the durations of the tests generated from "
        "a given test function.",
    )
```

- **`pytest_addoption(parser)`**：添加两个命令行选项 `--modules-durations` 和 `--functions-durations`：
  - **`--modules-durations`**：显示测试时长最长的 N 个模块时长。
  - **`--functions-durations`**：显示测试时长最长的 N 个测试函数时长。

## 获取测试报告

```python
def get_test_reports(terminalreporter):
    dlist = []
    for replist in terminalreporter.stats.values():
        for rep in replist:
            if hasattr(rep, "duration"):
                dlist.append(rep)
    return dlist
```

- **`get_test_reports(terminalreporter)`**：从 `terminalreporter` 获取包含 `duration` 属性的测试报告：
  - **`terminalreporter.stats`**：获取报告统计数据。
  - **`dlist`**：包含所有带有 `duration` 属性的测试报告。

## 报告模块时长

```python
def report_modules_durations(terminalreporter):
    durations = terminalreporter.config.getoption("--modules-durations")
    if durations is None:
        return

    dlist = get_test_reports(terminalreporter)
    if not dlist:
        return

    # group by file
    durations_by_file = defaultdict(float)
    for test_report in dlist:
        durations_by_file[test_report.fspath] += test_report.duration

    dlist = list(durations_by_file.items())

    dlist.sort(key=lambda x: x[1])
    dlist.reverse()
    terminalreporter.write_sep("=", "slowest modules durations")
    if durations:
        dlist = dlist[:durations]

    for filename, test_time in dlist:
        terminalreporter.write_line("{:02.2f}s {}".format(test_time, filename))
```

- **`report_modules_durations(terminalreporter)`**：生成和打印模块级别的时长报告：
  - 获取 `--modules-durations` 选项。
  - 获取测试报告列表。
  - 按文件路径 (`fspath`) 对时长进行汇总。
  - 按时长排序并显示前 N 个时长最长的模块。

## 报告函数时长

```python
def report_funtions_durations(terminalreporter):
    durations = terminalreporter.config.getoption("--functions-durations")
    if durations is None:
        return

    dlist = get_test_reports(terminalreporter)
    if not dlist:
        return

    # group by file
    durations_by_file = defaultdict(float)
    for test_report in dlist:
        if "[" in test_report.nodeid:
            file_and_function = test_report.nodeid[: test_report.nodeid.index("[")]
        else:
            file_and_function = test_report.nodeid
        durations_by_file[file_and_function] += test_report.duration

    dlist = list(durations_by_file.items())

    dlist.sort(key=lambda x: x[1])
    dlist.reverse()
    terminalreporter.write_sep("=", "slowest test functions durations")
    if durations:
        dlist = dlist[:durations]

    for filename, test_time in dlist:
        terminalreporter.write_line("{:02.2f}s {}".format(test_time, filename))
```

- **`report_funtions_durations(terminalreporter)`**：生成和打印函数级别的时长报告：
  - 获取 `--functions-durations` 选项。
  - 获取测试报告列表。
  - 按文件和函数 (`nodeid`) 对时长进行汇总。
  - 按时长排序并显示前 N 个时长最长的测试函数。

## 报告总时长

```python
def report_sum_durations(terminalreporter):
    """Print the sum of durations of all the tests."""
    dlist = get_test_reports(terminalreporter)
    if not dlist:
        return

    terminalreporter.write_sep("=", "sum of all tests durations")
    terminalreporter.write_line("{:02.2f}s".format(sum(x.duration for x in dlist)))
```

- **`report_sum_durations(terminalreporter)`**：计算所有测试的总时长并显示。

## 终端摘要

```python
def pytest_terminal_summary(terminalreporter):
    report_modules_durations(terminalreporter)
    report_funtions_durations(terminalreporter)
    report_sum_durations(terminalreporter)
```

- **`pytest_terminal_summary(terminalreporter)`**：pytest 终端摘要阶段调用，依次生成并打印模块时长、函数时长和总时长报告。

# 结语

`pytest-extra-durations` 插件的主要功能是生成以下三个等级的测试时长报告：
- **模块级别时长（--modules-durations）**：显示时长最长的 N 个模块。
- **函数级别时长（--functions-durations）**：显示时长最长的 N 个测试函数。
- **总时长**：显示所有测试时长的总和。

这些报告可以帮助开发人员识别性能瓶颈、优化测试和提高整体测试效率。


# 测试实践

准备如下测试用例，使用`pytest-durations`和`pytest-extra-durations`这两个插件，分别执行看下效果。

```python
# Content of test_durations.py
import time

import pytest


@pytest.fixture()
def set_up_fixture():
    time.sleep(0.1)
    yield
    time.sleep(0.2)

def test_01(set_up_fixture):
    print("用例1")
    time.sleep(1.0)

def test_02(set_up_fixture):
    print("用例2")
    time.sleep(0.6)

def test_03(set_up_fixture):
    print("用例3")
    time.sleep(1.2)

def test_04(set_up_fixture):
    print("用例4")
    time.sleep(0.3)

def test_05(set_up_fixture):
    print("用例5")
    time.sleep(2.3)
```

用例运行效果展示如下：

```shell
root@Gavin:~/test# pytest -v --durations=3 test_durations.py 
Test session starts (platform: linux, Python 3.11.6, pytest 8.2.2, pytest-sugar 1.0.0)
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-44-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'order': '1.2.1', 'progress': '1.3.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'assume': '2.4.3', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'sugar': '1.0.0', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2', 'extra-durations': '0.1.3'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/test
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, twisted-1.14.1, picked-0.5.0, assume-2.4.3, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, sugar-1.0.0, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2, extra-durations-0.1.3
asyncio: mode=Mode.STRICT
collected 5 items                                                                                                                                                                                                                                        

 test_durations.py::test_01 ✓                                                                                                                                                                                                               20% ██        
 test_durations.py::test_02 ✓                                                                                                                                                                                                               40% ████      
 test_durations.py::test_03 ✓                                                                                                                                                                                                               60% ██████    
 test_durations.py::test_04 ✓                                                                                                                                                                                                               80% ████████  
 test_durations.py::test_05 ✓                                                                                                                                                                                                              100% ██████████
=============================================================================================================== sum of all tests durations ===============================================================================================================
6.99s
================================================================================================================== slowest 3 durations ===================================================================================================================
2.31s call     test_durations.py::test_05
1.20s call     test_durations.py::test_03
1.00s call     test_durations.py::test_01

Results (7.03s):
       5 passed
root@Gavin:~/test# pytest -v --functions-durations=3 test_durations.py 
Test session starts (platform: linux, Python 3.11.6, pytest 8.2.2, pytest-sugar 1.0.0)
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-44-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'order': '1.2.1', 'progress': '1.3.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'assume': '2.4.3', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'sugar': '1.0.0', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2', 'extra-durations': '0.1.3'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/test
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, twisted-1.14.1, picked-0.5.0, assume-2.4.3, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, sugar-1.0.0, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2, extra-durations-0.1.3
asyncio: mode=Mode.STRICT
collected 5 items                                                                                                                                                                                                                                        

 test_durations.py::test_01 ✓                                                                                                                                                                                                               20% ██        
 test_durations.py::test_02 ✓                                                                                                                                                                                                               40% ████      
 test_durations.py::test_03 ✓                                                                                                                                                                                                               60% ██████    
 test_durations.py::test_04 ✓                                                                                                                                                                                                               80% ████████  
 test_durations.py::test_05 ✓                                                                                                                                                                                                              100% ██████████
============================================================================================================ slowest test functions durations ============================================================================================================
2.61s test_durations.py::test_05
1.50s test_durations.py::test_03
1.33s test_durations.py::test_01
=============================================================================================================== sum of all tests durations ===============================================================================================================
6.96s

Results (6.99s):
       5 passed
root@Gavin:~/test# pytest -v --modules-durations=2 test_durations.py 
Test session starts (platform: linux, Python 3.11.6, pytest 8.2.2, pytest-sugar 1.0.0)
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-44-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'order': '1.2.1', 'progress': '1.3.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'assume': '2.4.3', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'sugar': '1.0.0', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2', 'extra-durations': '0.1.3'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/test
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, twisted-1.14.1, picked-0.5.0, assume-2.4.3, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, sugar-1.0.0, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2, extra-durations-0.1.3
asyncio: mode=Mode.STRICT
collected 5 items                                                                                                                                                                                                                                        

 test_durations.py::test_01 ✓                                                                                                                                                                                                               20% ██        
 test_durations.py::test_02 ✓                                                                                                                                                                                                               40% ████      
 test_durations.py::test_03 ✓                                                                                                                                                                                                               60% ██████    
 test_durations.py::test_04 ✓                                                                                                                                                                                                               80% ████████  
 test_durations.py::test_05 ✓                                                                                                                                                                                                              100% ██████████
=============================================================================================================== slowest modules durations ================================================================================================================
6.97s test_durations.py
=============================================================================================================== sum of all tests durations ===============================================================================================================
6.97s

Results (7.00s):
       5 passed
root@Gavin:~/test#
```

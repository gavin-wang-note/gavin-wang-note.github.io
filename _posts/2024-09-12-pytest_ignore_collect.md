---
title: pytest hook系列之pytest_ignore_collect
date: 2024-09-12 23:00:00
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
summary: pytest hook之pytest_ignore_collect
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_ignore_collect` 是`pytest`框架中的一个钩子函数，允许我们在特定条件下动态地忽略某些测试文件或目录的收集过程。通过使用这个钩子函数，我们可以根据配置、环境变量或其他条件决定是否忽略某些测试用例的收集。本篇文章将详细介绍 `pytest_ignore_collect` 的使用场景、参数，并通过具体案例展示其应用。

# 什么是pytest_ignore_collect？

`pytest_ignore_collect` 是一个`pytest`提供的钩子函数，它在测试用例收集过程中被调用。这个钩子允许我们根据一些条件忽略某些测试文件或目录的收集，从而实现灵活的测试管理。

# 使用场景

1. **基于文件名模式忽略测试文件**：根据文件名模式动态地忽略某些文件。
2. **基于环境变量忽略测试**：在特定环境下忽略某些测试，适用于复杂的测试环境配置。
3. **根据配置文件忽略测试**：通过外部配置文件控制测试收集过程，避免对代码进行硬编码修改。

# 参数

```python
def pytest_ignore_collect(path, config):
    # path: 将被收集的测试文件路径。
    # config: pytest 配置对象，包含解析后的命令行选项和 ini 配置。
    pass
```

- `path`：即将被收集的测试文件或目录路径，可以根据这个路径来决定是收集还是忽略。
- `config`：`pytest`配置对象，包含了从命令行和`pytest`配置文件中解析出来的选项。

# 示例代码

## 案例一：基于文件名模式忽略测试文件

目标：根据文件名模式忽略以 `_skip.py` 结尾的测试文件。

步骤：
1. 定义文件名模式，标识需要忽略的测试文件。
2. 使用 `pytest_ignore_collect` 钩子忽略符合模式的测试文件。

示例代码：

```python
# conftest.py
import pytest

def pytest_ignore_collect(path, config):
    if path.basename.endswith("_skip.py"):
        return True
    return False

# 示例测试文件 `tests/test_example_skip.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_example.py`
def test_example2():
    assert 2 + 2 == 4
```

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
collected 1 item                                                                                                                                                                                                                                        

tests/test_example.py::test_example2 PASSED

=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook#
```

**说明：**：
- `pytest_ignore_collect` 钩子函数中检查文件名是否以 `_skip.py` 结尾，如果是则返回 `True` 忽略该文件的收集。
- 通过这种方式，可以动态地忽略特定文件名模式的测试文件。

## 案例二：基于环境变量忽略测试

目标：在特定环境变量设置下忽略某些测试文件的收集。

步骤：
1. 检查环境变量的值。
2. 使用 `pytest_ignore_collect` 钩子在特定环境变量值下忽略测试文件。

示例代码：

```python
# conftest.py
import pytest
import os

def pytest_ignore_collect(path, config):
    if "SKIP_TESTS" in os.environ and path.basename.startswith("test_skip_"):
        return True
    return False

# 示例测试文件 `tests/test_skip_example.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_example.py`
def test_example2():
    assert 2 + 2 == 4
```

**说明：**：
- `pytest_ignore_collect` 钩子函数中检查环境变量 `SKIP_TESTS` 是否存在，并且文件名是否以 `test_skip_` 开头，如果是则返回 `True` 忽略该文件的收集。
- 设置环境变量 `SKIP_TESTS` 后，可以动态地忽略某些文件的测试。

```shell
export SKIP_TESTS=1
pytest
```

运行效果：

```shell
root@Gavin:~/test/hook# vim tests/test_skip_example.py
root@Gavin:~/test/hook# ls -l tests/
total 16
drwxr-xr-x 2 root root 4096 May 31 17:01 __pycache__
-rw-r--r-- 1 root root   43 May 31 17:00 test_example.py
-rw-r--r-- 1 root root   43 May 31 17:00 test_example_skip.py
-rw-r--r-- 1 root root   43 May 31 17:07 test_skip_example.py
root@Gavin:~/test/hook# export SKIP_TESTS=1
root@Gavin:~/test/hook# pytest
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                                       

tests/test_example.py .                                                                                                                                                                                                                           [ 50%]
tests/test_example_skip.py .                                                                                                                                                                                                                      [100%]

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

## 案例三：根据配置文件忽略测试

目标：通过外部配置文件控制忽略哪些测试文件。

步骤：
1. 在外部配置文件中定义要忽略的文件列表。
2. 在 `pytest_ignore_collect` 钩子中读取该配置文件，根据配置忽略测试文件。

示例代码：

```python
# config.json
{
    "ignore_files": [
        "test_ignore_example.py"
    ]
}

# conftest.py
import pytest
import json

def pytest_ignore_collect(path, config):
    with open("config.json") as f:
        ignore_files = json.load(f).get("ignore_files", [])
    if path.basename in ignore_files:
        return True
    return False

# 示例测试文件 `tests/test_ignore_example.py`
def test_example1():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_example.py`
def test_example2():
    assert 2 + 2 == 4
```

运行效果：

```shell
root@Gavin:~/test/hook# vim tests/test_ignore_example.py
root@Gavin:~/test/hook# ls -l tests/
total 20
drwxr-xr-x 2 root root 4096 May 31 17:01 __pycache__
-rw-r--r-- 1 root root   43 May 31 17:00 test_example.py
-rw-r--r-- 1 root root   43 May 31 17:00 test_example_skip.py
-rw-r--r-- 1 root root   43 May 31 17:08 test_ignore_example.py
-rw-r--r-- 1 root root   43 May 31 17:07 test_skip_example.py
root@Gavin:~/test/hook# pytest
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 3 items                                                                                                                                                                                                                                       

tests/test_example.py .                                                                                                                                                                                                                           [ 33%]
tests/test_example_skip.py .                                                                                                                                                                                                                      [ 66%]
tests/test_skip_example.py .                                                                                                                                                                                                                      [100%]

=================================================================================================================== 3 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

**说明**：
- 配置文件 `config.json` 中定义了需要忽略的文件列表。
- `pytest_ignore_collect` 钩子函数中读取该配置文件，并根据配置文件中定义的文件名列表决定是否忽略文件的收集。

# 总结

`pytest_ignore_collect` 是`pytest`中一个非常强大和灵活的钩子，能够在测试用例收集过程中动态决定是否忽略某些文件或目录。通过本文的案例，你可以了解如何使用 `pytest_ignore_collect` 在不同场景下灵活地管理测试用例收集过程。在实际应用中，可以根据项目需求及测试场景对这些示例进行扩展和调整，从而达到更灵活的测试管理效果。

---
title: pytest hook系列之pytest_collect_file
date: 2024-09-13 23:00:00
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
summary: pytest hook之pytest_collect_file
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_collect_file` 是`pytest`框架中的一个钩子函数，允许我们在收集测试文件时执行自定义逻辑。利用这个钩子函数，我们可以根据文件类型或其他条件自定义测试用例的收集过程。这使得我们可以扩展`pytest`来支持更多类型的测试文件或进行更细粒度的测试管理。本篇文章将详细介绍 `pytest_collect_file` 的使用场景、参数，并通过具体案例展示其应用。

# 什么是pytest_collect_file？

`pytest_collect_file` 是一个`pytest`提供的钩子函数，它在测试框架收集每个测试文件时被调用。这个钩子允许我们在文件收集阶段自定义逻辑，例如处理自定义类型的测试文件或进行条件性筛选。

# 使用场景

1. **自定义文件类型支持**：添加对新类型测试文件的支持，例如 `.txt`、`.json` 等。
2. **基于文件类型的收集策略**：根据文件类型应用不同的收集策略。
3. **条件性收集文件**：基于文件名模式、文件内容等条件进行文件收集。

# 参数

```python
def pytest_collect_file(file_path, parent):
    # file_path: 文件路径对象，表示当前需要收集的文件
    # parent: 收集这个文件的父对象
    pass
```

- `file_path`：这是一个 `py.path` 或者 `pathlib.Path` 对象，表示当前需要收集的文件。
- `parent`：当前文件的父收集器对象，通常是一个 `Directory` 或 `Package` 对象。

# 示例代码

## 案例一：支持自定义文件类型

目标：为自定义的 `.txt` 文件类型添加支持，并将其作为测试文件收集。

步骤：
1. 定义一个自定义的文件收集器。
2. 使用 `pytest_collect_file` 钩子检查文件类型，并返回自定义的文件收集器。

示例代码：

```python
# conftest.py
import pytest
import pathlib

class TxtFile(pytest.File):
    def collect(self):
        yield TxtItem.from_parent(self, name=self.path.stem)

class TxtItem(pytest.Item):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.path = pathlib.Path(parent.path) / name

    def runtest(self):
        # 自定义测试逻辑，比如验证文件内容非空
        with self.path.open() as f:
            content = f.read().strip()
            if not content:
                raise pytest.fail(f"File {self.name} is empty")

    def repr_failure(self, excinfo):
        # Customize output failure representation
        return f"File {self.name} test failed"

    def reportinfo(self):
        return self.path, 0, f"use case: {self.name}"

def pytest_collect_file(file_path, parent):
    if file_path.suffix == ".txt":
        return TxtFile.from_parent(parent, path=file_path)

# 示例测试文件 `tests/test_example.txt`
def test_example():
    assert 1 +1 == 2
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

tests/test_example.txt::test_example FAILED

======================================================================================================================= FAILURES ========================================================================================================================
________________________________________________________________________________________________________________ use case: test_example _________________________________________________________________________________________________________________
File test_example test failed
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.txt::test_example
=================================================================================================================== 1 failed in 0.02s ===================================================================================================================
root@Gavin:~/test/hook#
```

**说明：**
1. **TxtFile 类**
    - 继承自 `pytest.File`。
    - 收集过程中使用 `yield` 生成 `TxtItem` 实例，同时传递文件名作为测试用例的名字。

2. **TxtItem 类**
    - 继承自 `pytest.Item`。
    - 使用 `pathlib.Path` 进行文件路径操作，确保与`pytest 8.0`的兼容性。
    - `runtest` 方法实现了文件内容的验证逻辑，确保文件非空。
    - `repr_failure` 用于自定义失败时的输出信息。
    - `reportinfo` 提供测试报告中的相关信息。

3. **pytest_collect_file 函数**
    - 在收集阶段检查文件后缀是否为 `.txt`。
    - 返回自定义的 `TxtFile` 对象，使用 `pathlib.Path` 进行路径处理。

## 案例二：基于文件类型应用不同收集策略

目标：根据文件类型分别处理不同的测试文件类型，例如 `.py` 和 `.txt`。

步骤：
1. 定义不同文件类型的收集器。
2. 使用 `pytest_collect_file` 钩子根据文件类型返回相应的收集器。

示例代码：

```python
# conftest.py
# 其他内容不变，只修改函数pytest_collect_file
def pytest_collect_file(file_path, parent):
    if file_path.suffix == ".py":
        # return parent.session.pytest_collect_file(file_path, parent)
        return pytest.Module.from_parent(parent=parent, path=file_path)
    elif file_path.suffix == ".txt":
        return TxtFile.from_parent(parent, path=file_path)

# 示例测试文件 `tests/test_example.txt`
# (内容非空即可)

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 1 + 1 == 2
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
collected 3 items                                                                                                                                                                                                                                       

tests/test_example.py::test_example PASSED
tests/test_example.py::test_example PASSED
tests/test_example.txt::test_example FAILED

======================================================================================================================= FAILURES ========================================================================================================================
________________________________________________________________________________________________________________ use case: test_example _________________________________________________________________________________________________________________
File test_example test failed
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.txt::test_example
============================================================================================================== 1 failed, 2 passed in 0.04s ==============================================================================================================
root@Gavin:~/test/hook# 
```

**说明：**
- 通过 `pytest_collect_file` 钩子，根据文件后缀判断文件类型，并返回相应的收集器。
- `.py` 文件使用默认的 Python 收集器，而 `.txt` 文件使用自定义的 `TxtFile` 收集器。

## 案例三：基于文件名模式进行条件性收集

目标：根据文件名模式忽略以 `_ignore` 结尾的测试文件。

步骤：
1. 使用 `pytest_collect_file` 钩子检查文件名模式。
2. 根据文件名模式决定是否忽略文件。

示例代码：

```python
# conftest.py
import pytest

# 其他内容不变，只修改函数pytest_collect_file
def pytest_collect_file(file_path, parent):
    if "_ignore" in file_path.stem:
        return None  # 忽略文件
    return pytest.Module.from_parent(parent=parent, path=file_path) if file_path.suffix == ".py" else TxtFile.from_parent(parent=parent, path=file_path)


# 示例测试文件 `tests/test_example_ignore.py`
def test_example():
    assert 1 + 1 == 2

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 2 + 2 == 4
```

运行效果：

```shell
root@Gavin:~/test/hook# ls -l tests/
total 16
drwxr-xr-x 2 root root 4096 May 31 17:55 __pycache__
-rw-r--r-- 1 root root   42 May 31 17:54 test_example.py
-rw-r--r-- 1 root root   41 May 31 17:32 test_example.txt
-rw-r--r-- 1 root root   42 May 31 17:56 test_ignore.py
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
collected 4 items                                                                                                                                                                                                                                       

tests/test_example.py::test_example PASSED
tests/test_example.py::test_example PASSED
tests/test_example.txt::test_example FAILED
tests/test_ignore.py::test_example PASSED

======================================================================================================================= FAILURES ========================================================================================================================
________________________________________________________________________________________________________________ use case: test_example _________________________________________________________________________________________________________________
File test_example test failed
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.txt::test_example
============================================================================================================== 1 failed, 3 passed in 0.04s ==============================================================================================================
root@Gavin:~/test/hook#
```

**说明：**
- `pytest_collect_file` 钩子函数中检查文件名是否包含 `_ignore`，如果包含则返回 `None` 忽略该文件。
- 对于 `.py` 文件，使用默认的收集机制。

# 总结

`pytest_collect_file` 是`pytest`中一个非常灵活和强大的钩子，允许我们在文件收集阶段实现自定义逻辑。通过本文的案例，你可以了解如何使用 `pytest_collect_file` 来支持自定义文件类型、根据文件类型应用不同的收集策略以及进行条件性收集。在实际应用中，可以根据项目需求及测试场景对这些示例进行扩展和调整，从而实现更灵活的测试管理。

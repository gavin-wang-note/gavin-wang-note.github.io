---
title: pytest hook系列之pytest_assertrepr_compare
date: 2024-10-10 23:00:00
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
summary: pytest hook之pytest_assertrepr_compare
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_assertrepr_compare` 是`pytest`框架中的一个钩子函数，它在比较操作（如 `==`, `!=`, `<`, `>`, `<=`, `>=`）失败时被触发，用于在比较操作失败时提供自定义的错误报告。这个钩子允许我们提供自定义的错误报告，替换默认的错误信息，以便在断言失败时提供更丰富的调试信息，这样可以在断言失败时生成更具可读性和详细的错误信息，从而帮助调试和定位问题。

# 使用场景

1. **增强错误报告**：在断言失败时提供详细和有用的错误信息，帮助更快定位问题。
2. **自定义比较逻辑**：为特定类型或自定义对象提供定制的比较逻辑和相应的错误报告。
3. **易于调试**：通过提供更可读的错误信息，减少调试时间，提高效率。

# 参数

```python
def pytest_assertrepr_compare(config, op, left, right):
    # config: pytest 的配置对象，包含有关当前测试会话的所有信息
    # op: 比较操作符，表示比较的类型（如 '==', '!=', '<', '>', '<=', '>='）
    # left: 比较操作符左侧的值
    # right: 比较操作符右侧的值
    pass
```

- `config`：`pytest` 的配置对象，包含有关当前测试会话的所有信息。
- `op`：比较操作符，表示比较的类型（如 '==', '!=', '<', '>', '<=', '>='）。
- `left`：比较操作符左侧的值。
- `right`：比较操作符右侧的值。

# 示例代码

## 案例一：增强错误报告

目标：在断言失败时提供详细和有用的错误信息，帮助更快定位问题。

步骤：
1. 使用 `pytest_assertrepr_compare` 钩子函数。
2. 在钩子函数中插入自定义的错误报告逻辑。

示例代码：

```python
# conftest.py
import pytest

def pytest_assertrepr_compare(config, op, left, right):
    if op == "==":
        return [
            "Comparing two values:",
            f"   value 1: {left}",
            f"   value 2: {right}",
            "Equality assertion failed!",
        ]

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 2 + 2 == 5
```

**注释**：
- 在 `pytest_assertrepr_compare` 钩子函数中，提供断言失败时的自定义错误信息，包括被比较的两个值和相应的比较操作符。
- 测试用例中引入一个故意的错误，以演示自定义错误报告的效果。

## 案例二：自定义对象的比较

目标：为特定类型或自定义对象提供定制的比较逻辑和相应的错误报告。

步骤：
1. 定义一个自定义对象类型。
2. 使用 `pytest_assertrepr_compare` 钩子函数，为该类型提供定制的比较逻辑和错误报告。

示例代码：

```python
# conftest.py
import pytest

class CustomObject:
    def __init__(self, name, value):
        self.name = name
        self.value = value

def pytest_assertrepr_compare(config, op, left, right):
    if isinstance(left, CustomObject) and isinstance(right, CustomObject) and op == "==":
        return [
            "Comparing two CustomObject instances:",
            f"   object 1: {left.name} with value {left.value}",
            f"   object 2: {right.name} with value {right.value}",
            "Equality assertion failed!",
        ]

# 示例测试文件 `tests/test_example.py`
from conftest import CustomObject

def test_custom_object_comparison():
    obj1 = CustomObject("obj1", 100)
    obj2 = CustomObject("obj2", 100)
    assert obj1 == obj2
```

**注释**：
- 定义一个 `CustomObject` 类，并在 `pytest_assertrepr_compare` 钩子函数中为该类型的实例提供自定义的比较逻辑和错误报告。
- 在测试用例中比较两个 `CustomObject` 实例，并故意引发断言失败以演示自定义错误报告。

## 案例三：对列表和字典的比较

目标：在断言列表或字典相等性失败时，提供更具可读性的错误报告，显示详细的差异信息。

步骤：
1. 使用 `pytest_assertrepr_compare` 钩子函数。
2. 在钩子函数中插入列表和字典的详细比较逻辑。

示例代码：

```python
# conftest.py
import pytest

def pytest_assertrepr_compare(config, op, left, right):
    if isinstance(left, list) and isinstance(right, list) and op == "==":
        return [
            "Comparing two lists:",
            f"   list 1: {left}",
            f"   list 2: {right}",
            "List equality assertion failed!",
            "Differences:",
        ] + [f"   Index {i}: {l} != {r}" for i, (l, r) in enumerate(zip(left, right)) if l != r]

    if isinstance(left, dict) and isinstance(right, dict) and op == "==":
        return [
            "Comparing two dictionaries:",
            f"   dict 1: {left}",
            f"   dict 2: {right}",
            "Dictionary equality assertion failed!",
            "Differences:",
        ] + [f"   Key {key}: {left.get(key)} != {right.get(key)}" for key in set(left.keys()).union(right.keys()) if left.get(key) != right.get(key)]

# 示例测试文件 `tests/test_example.py`
def test_list_comparison():
    assert [1, 2, 3] == [1, 3, 2]

def test_dict_comparison():
    assert {"a": 1, "b": 2} == {"a": 2, "b": 2}
```

**注释**：
- 在 `pytest_assertrepr_compare` 钩子函数中，提供对列表和字典的详细比较逻辑和错误报告。
- 在测试用例中比较两个列表和两个字典，并故意引发断言失败以演示自定义错误报告。

## 运行和验证

确保目录结构如下：

```shell
```

在项目根目录下运行以下命令：

```shell
pytest -s -v --cache-clear
```

### 验证输出信息

根据具体的案例，控制台输出应包含自定义的错误报告，显示详细的比较信息和相应的差异。

### 控制台输出示例

**案例一：增强错误报告**

```plaintext
______________ test_example ________________
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

tests/test_example.py::test_example FAILED

======================================================================================================================= FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example ______________________________________________________________________________________________________________________

    def test_example():
>       assert 2 + 2 == 5
E       assert Comparing two values:
E            value 1: 4
E            value 2: 5
E         Equality assertion failed!

tests/test_example.py:2: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_example - assert Comparing two values:
=================================================================================================================== 1 failed in 0.10s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例二：自定义对象的比较**

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

tests/test_example.py::test_custom_object_comparison FAILED

======================================================================================================================= FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________ test_custom_object_comparison _____________________________________________________________________________________________________________

    def test_custom_object_comparison():
        obj1 = CustomObject("obj1", 100)
        obj2 = CustomObject("obj2", 100)
>       assert obj1 == obj2
E       assert Comparing two CustomObject instances:
E            object 1: obj1 with value 100
E            object 2: obj2 with value 100
E         Equality assertion failed!

tests/test_example.py:6: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_custom_object_comparison - assert Comparing two CustomObject instances:
=================================================================================================================== 1 failed in 0.10s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例三：对列表和字典的比较**

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
collected 2 items                                                                                                                                                                                                                                       

tests/test_example.py::test_list_comparison FAILED
tests/test_example.py::test_dict_comparison FAILED

======================================================================================================================= FAILURES ========================================================================================================================
_________________________________________________________________________________________________________________ test_list_comparison __________________________________________________________________________________________________________________

    def test_list_comparison():
>       assert [1, 2, 3] == [1, 3, 2]
E       assert Comparing two lists:
E            list 1: [1, 2, 3]
E            list 2: [1, 3, 2]
E         List equality assertion failed!
E         Differences:
E            Index 1: 2 != 3
E            Index 2: 3 != 2

tests/test_example.py:2: AssertionError
_________________________________________________________________________________________________________________ test_dict_comparison __________________________________________________________________________________________________________________

    def test_dict_comparison():
>       assert {"a": 1, "b": 2} == {"a": 2, "b": 2}
E       AssertionError: assert Comparing two dictionaries:
E            dict 1: {'a': 1, 'b': 2}
E            dict 2: {'a': 2, 'b': 2}
E         Dictionary equality assertion failed!
E         Differences:
E            Key a: 1 != 2

tests/test_example.py:5: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_list_comparison - assert Comparing two lists:
FAILED tests/test_example.py::test_dict_comparison - AssertionError: assert Comparing two dictionaries:
=================================================================================================================== 2 failed in 0.11s ===================================================================================================================
root@Gavin:~/test/hook# 
```

# 总结

通过 `pytest_assertrepr_compare` 钩子，我们可以在比较操作失败时提供自定义的错误报告，从而增强错误信息的可读性和可调试性。本文详细介绍了钩子的使用场景、参数及具体案例，并提供了完整的示例代码和详细解释，帮助读者更好地理解和应用这个钩子函数。

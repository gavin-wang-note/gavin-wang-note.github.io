---
title: pytest hook系列之pytest_pycollect_makeitem
date: 2024-09-20 23:00:00
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
summary: pytest hook之pytest_pycollect_makeitem
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_pycollect_makeitem` 是 pytest 框架中的一个钩子函数，允许我们在测试集合过程中创建收集项。利用这个钩子函数，我们可以自定义测试项的创建逻辑，例如根据特定条件动态生成测试项，过滤某些测试项等。这为我们提供了高度的灵活性，以适应各种复杂的测试需求。

# 什么是pytest_pycollect_makeitem？

`pytest_pycollect_makeitem` 是一个·pytest·提供的钩子函数，它在测试集合过程中被调用，用于创建自定义的测试项。通过这个钩子，我们可以根据文件、类或函数等对象来生成测试项，或对默认的测试项创建过程进行调整。

# 使用场景

1. **动态生成测试项**：根据自定义逻辑动态生成测试项，例如从配置文件或数据库中读取用例信息。
2. **过滤测试项**：在测试项创建过程中，过滤掉不需要的测试项。
3. **自定义测试用例类型**：为特定类型的测试用例创建自定义项，例如为特定装饰器的测试函数创建特定的测试项。

# 参数

```python
def pytest_pycollect_makeitem(collector, name, obj):
    # collector: 当前收集器对象，通常是一个目录、模块或类收集器
    # name: 被收集的项目的名称，通常是模块、类或函数的名称
    # obj: 被收集的对象，通常是一个模块、类或函数对象
    pass
```

- `collector`：当前收集器对象，通常是一个目录、模块或类收集器，可以通过它访问包含此测试项的父对象。
- `name`：被收集的项目的名称，通常是模块、类或函数的名称。
- `obj`：被收集的对象，通常是一个模块、类或函数对象。

# 示例代码

## 案例一：动态生成测试项

目标：根据自定义逻辑动态生成测试项，例如从配置文件中读取用例信息并生成对应的测试项。

步骤：

1. 使用 `pytest_pycollect_makeitem` 钩子函数。
2. 根据自定义逻辑动态生成测试项。

示例代码：

```python
# conftest.py
import pytest

def pytest_pycollect_makeitem(collector, name, obj):
    # 动态生成测试项
    if isinstance(obj, type) and hasattr(obj, "dynamic_tests"):
        # 如果类具有 dynamic_tests 属性，生成对应的测试项
        dynamic_tests = obj.dynamic_tests()
        items = []
        for test_name, test_func in dynamic_tests.items():
            item = pytest.Function.from_parent(collector, name=test_name, callobj=test_func)
            items.append(item)
        return items  # 返回生成的测试项列表
    return None  # 使用默认的收集行为

# 示例测试文件 `tests/test_dynamic.py`
import pytest

class TestDynamic:
    @staticmethod
    def dynamic_tests():
        # 动态生成测试用例
        return {
            "test_dynamic_1": TestDynamic.test_dynamic_1,
            "test_dynamic_2": TestDynamic.test_dynamic_2
        }
    
    @staticmethod
    def test_dynamic_1():
        assert 1 + 1 == 2

    @staticmethod
    def test_dynamic_2():
        assert 2 + 2 == 4

# 示例测试文件 `tests/test_static.py`
def test_example():
    assert 3 + 3 == 6
```

**注释**：

- 在 `pytest_pycollect_makeitem` 钩子函数中，检查类是否具有 `dynamic_tests` 属性，如果有则动态生成测试项。
- 通过 `pytest.Function.from_parent` 创建测试项并添加到收集器中。

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

tests/test_dynamic.py::test_dynamic_1 PASSED
tests/test_dynamic.py::test_dynamic_2 PASSED
tests/test_static.py::test_example PASSED

=================================================================================================================== 3 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

# 案例二：过滤测试项

目标：在测试项创建过程中，过滤掉不需要的测试项。

步骤：

1. 使用 `pytest_pycollect_makeitem` 钩子函数。
2. 根据特定条件过滤测试项。

示例代码：

```python
# conftest.py
import pytest

def pytest_pycollect_makeitem(collector, name, obj):
    # 过滤掉名字中包含 "skip" 的测试项
    if "skip" in name:
        print(f"Skipping test: {name}")
        return []
    return None  # 使用默认的收集行为

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2

def test_skip_example2():
    assert 2 + 2 == 4
```

**注释**：

- 在 `pytest_pycollect_makeitem` 钩子函数中，检查测试项的名称，如果名称中包含 "skip"，则过滤掉该测试项。

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
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2
ut-2.2.0
asyncio: mode=Mode.STRICT
collecting ... Skipping test: test_skip_example2
collected 4 items                                                                                                                                                                                                                                       

tests/test_dynamic.py::TestDynamic::test_dynamic_1 PASSED
tests/test_dynamic.py::TestDynamic::test_dynamic_2 PASSED
tests/test_example.py::test_example1 PASSED
tests/test_static.py::test_example PASSED

=================================================================================================================== 4 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

##### 案例三：自定义测试用例类型

目标：为特定类型的测试用例创建自定义项，例如为带有特定装饰器的测试函数创建特定的测试项。

步骤：

1. 使用 `pytest_pycollect_makeitem` 钩子函数。
2. 为带有特定装饰器的测试函数创建自定义测试项。

示例代码：

```python
# conftest.py
import pytest
import os
from pathlib import Path

def pytest_pycollect_makeitem(collector, name, obj):
    # 确保函数被调用
    print(f"pytest_pycollect_makeitem called for: {collector}, name: {name}, obj: {obj}")
    
    # 如果名字中包含 "config"，处理模块初始化
    if "config" in name and isinstance(collector, pytest.Module):
        print(f"Configuring module for: {name}")
        # 初始化逻辑，例如设置环境变量
        os.environ["CONFIG_PATH"] = str(collector.fspath)
        print(f"CONFIG_PATH set to: {os.environ['CONFIG_PATH']}")
    return None  # 使用默认的收集行为


# 示例测试文件 `tests/test_config_module.py`
def test_example1():
    config_path = os.getenv("CONFIG_PATH")
    assert config_path and config_path.endswith("test_config_module.py")

# 示例测试文件 `tests/test_normal_module.py`
def test_example2():
    assert 2 + 2 == 4
```

**注释**：

- 在 `pytest_pycollect_makeitem` 钩子函数中，检查测试函数是否具有 `custom_marker` 属性，如果有则创建自定义测试项。
- 通过 `pytest.Function.from_parent` 创建自定义测试项并添加到收集器中。

运行效果：

```shell
root@Gavin:~/test/hook# pytest --cache-clear -s -v
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collecting ... pytest_pycollect_makeitem called for: <Module test_config_module.py>, name: @py_builtins, obj: <module 'builtins' (built-in)>
pytest_pycollect_makeitem called for: <Module test_config_module.py>, name: @pytest_ar, obj: <module '_pytest.assertion.rewrite' from '/usr/local/lib/python3.11/dist-packages/_pytest/assertion/rewrite.py'>
pytest_pycollect_makeitem called for: <Module test_config_module.py>, name: os, obj: <module 'os' (frozen)>
pytest_pycollect_makeitem called for: <Module test_config_module.py>, name: test_example1, obj: <function test_example1 at 0x71fe7eb43380>
pytest_pycollect_makeitem called for: <Module test_config_module.py>, name: __pytest_asyncio_scoped_event_loop, obj: <function pytest_collectstart.<locals>.scoped_event_loop at 0x71fe7eb42fc0>
pytest_pycollect_makeitem called for: <Module test_dynamic.py>, name: @py_builtins, obj: <module 'builtins' (built-in)>
pytest_pycollect_makeitem called for: <Module test_dynamic.py>, name: @pytest_ar, obj: <module '_pytest.assertion.rewrite' from '/usr/local/lib/python3.11/dist-packages/_pytest/assertion/rewrite.py'>
pytest_pycollect_makeitem called for: <Module test_dynamic.py>, name: pytest, obj: <module 'pytest' from '/usr/local/lib/python3.11/dist-packages/pytest/__init__.py'>
pytest_pycollect_makeitem called for: <Module test_dynamic.py>, name: TestDynamic, obj: <class 'test_dynamic.TestDynamic'>
pytest_pycollect_makeitem called for: <Module test_dynamic.py>, name: __pytest_asyncio_scoped_event_loop, obj: <function pytest_collectstart.<locals>.scoped_event_loop at 0x71fe7eb43240>
pytest_pycollect_makeitem called for: <Class TestDynamic>, name: dynamic_tests, obj: <staticmethod(<function TestDynamic.dynamic_tests at 0x71fe7eb436a0>)>
pytest_pycollect_makeitem called for: <Class TestDynamic>, name: test_dynamic_1, obj: <staticmethod(<function TestDynamic.test_dynamic_1 at 0x71fe7eb43740>)>
pytest_pycollect_makeitem called for: <Class TestDynamic>, name: test_dynamic_2, obj: <staticmethod(<function TestDynamic.test_dynamic_2 at 0x71fe7eb437e0>)>
pytest_pycollect_makeitem called for: <Class TestDynamic>, name: __pytest_asyncio_scoped_event_loop, obj: <function pytest_collectstart.<locals>.scoped_event_loop at 0x71fe7eb43560>
pytest_pycollect_makeitem called for: <Module test_example.py>, name: @py_builtins, obj: <module 'builtins' (built-in)>
pytest_pycollect_makeitem called for: <Module test_example.py>, name: @pytest_ar, obj: <module '_pytest.assertion.rewrite' from '/usr/local/lib/python3.11/dist-packages/_pytest/assertion/rewrite.py'>
pytest_pycollect_makeitem called for: <Module test_example.py>, name: test_example1, obj: <function test_example1 at 0x71fe7eb43c40>
pytest_pycollect_makeitem called for: <Module test_example.py>, name: test_skip_example2, obj: <function test_skip_example2 at 0x71fe7eb43ce0>
pytest_pycollect_makeitem called for: <Module test_example.py>, name: __pytest_asyncio_scoped_event_loop, obj: <function pytest_collectstart.<locals>.scoped_event_loop at 0x71fe7eb43920>
pytest_pycollect_makeitem called for: <Module test_normal_module.py>, name: @py_builtins, obj: <module 'builtins' (built-in)>
pytest_pycollect_makeitem called for: <Module test_normal_module.py>, name: @pytest_ar, obj: <module '_pytest.assertion.rewrite' from '/usr/local/lib/python3.11/dist-packages/_pytest/assertion/rewrite.py'>
pytest_pycollect_makeitem called for: <Module test_normal_module.py>, name: test_example2, obj: <function test_example2 at 0x71fe7eb43f60>
pytest_pycollect_makeitem called for: <Module test_normal_module.py>, name: __pytest_asyncio_scoped_event_loop, obj: <function pytest_collectstart.<locals>.scoped_event_loop at 0x71fe7eb43d80>
pytest_pycollect_makeitem called for: <Module test_static.py>, name: @py_builtins, obj: <module 'builtins' (built-in)>
pytest_pycollect_makeitem called for: <Module test_static.py>, name: @pytest_ar, obj: <module '_pytest.assertion.rewrite' from '/usr/local/lib/python3.11/dist-packages/_pytest/assertion/rewrite.py'>
pytest_pycollect_makeitem called for: <Module test_static.py>, name: test_example, obj: <function test_example at 0x71fe7eb8c180>
pytest_pycollect_makeitem called for: <Module test_static.py>, name: __pytest_asyncio_scoped_event_loop, obj: <function pytest_collectstart.<locals>.scoped_event_loop at 0x71fe7eb43ec0>
collected 7 items                                                                                                                                                                                                                                       

tests/test_config_module.py::test_example1 FAILED
tests/test_dynamic.py::TestDynamic::test_dynamic_1 PASSED
tests/test_dynamic.py::TestDynamic::test_dynamic_2 PASSED
tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_skip_example2 PASSED
tests/test_normal_module.py::test_example2 PASSED
tests/test_static.py::test_example PASSED

======================================================================================================================= FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example1 _____________________________________________________________________________________________________________________

    def test_example1():
        config_path = os.getenv("CONFIG_PATH")
>       assert config_path and config_path.endswith("test_config_module.py")
E       assert (None)

tests/test_config_module.py:5: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_config_module.py::test_example1 - assert (None)
============================================================================================================== 1 failed, 6 passed in 0.11s ==============================================================================================================
root@Gavin:~/test/hook#
```


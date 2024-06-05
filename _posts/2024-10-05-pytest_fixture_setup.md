---
title: pytest hook系列之pytest_fixture_setup
date: 2024-10-05 23:00:00
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
summary: pytest hook之pytest_fixture_setup
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_fixture_setup` 钩子函数用于在执行 `fixture` 的设置过程时加入自定义逻辑。这个钩子函数允许你在 `fixture` 定义和请求执行期间干预设置过程。它返回第一个非 `None` 的结果，根据 `firstresult` 这个特性，其他实现会被跳过。

# 参数

```python
@hookspec(firstresult=True)
def pytest_fixture_setup(
    fixturedef: "FixtureDef[Any]", request: "SubRequest"
) -> Optional[object]:
    """Perform fixture setup execution.

    :param fixturedef:
        The fixture definition object.
    :param request:
        The fixture request object.
    :returns:
        The return value of the call to the fixture function.

    Stops at first non-None result, see :ref:`firstresult`.
    
    .. note::
        If the fixture function returns None, other implementations of
        this hook function will continue to be called, according to the
        behavior of the :ref:`firstresult` option.
    """
```

- `fixturedef`: `FixtureDef` 对象，表示 `fixture` 定义，包含有关 `fixture` 的详细信息。
- `request`: `SubRequest` 对象，表示 `fixture` 请求，包含当前测试请求的信息。

返回值: 调用 `fixture` 函数的返回值。如果返回 `None`，其他钩子函数的实现将继续被调用。

# 使用场景

1. **自定义 fixture 设置**：在执行 `fixture` 设置逻辑之前或之后添加额外的操作。
2. **调试和日志记录**：在 `fixture` 设置过程中添加调试信息和日志记录。
3. **条件性初始化**：根据不同的测试需求动态改变 `fixture` 的初始化行为。

# 示例代码

## 案例一：自定义 fixture 设置

目标：在执行 `fixture` 设置逻辑之前和之后打印调试信息。

步骤：
1. 使用 `pytest_fixture_setup` 钩子函数。
2. 在钩子函数中打印调试信息。

**示例代码**：

```python
# conftest.py
import pytest

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    """在 fixture 设置逻辑之前和之后打印调试信息"""
    print(f"Setting up fixture: {fixturedef.scope} - {fixturedef.argname}")
    # 获取实际 fixture setup 的结果
    outcome = yield
    result = outcome.get_result()
    print(f"Finished setting up fixture: {fixturedef.scope} - {fixturedef.argname}")
    return result

# tests/test_example.py
@pytest.fixture
def dynamic_fixture():
    return "default value"

def test_custom_fixture(dynamic_fixture):
    assert dynamic_fixture == "custom setup value"

def test_addition():
    assert 1 + 1 == 2

def test_division_by_zero():
    assert 1 / 0  # 这将引发一个ZeroDivisionError，触发调试模式

def test_subtraction():
    assert 2 - 1 == 1
```

**解释：**
- 使用 `print` 语句在 `fixture` 设置逻辑之前和之后打印调试信息。
- 调用 `fixturedef.execute(request)` 执行 `fixture` 的实际设置逻辑。

**运行效果:**

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
collected 4 items                                                                                                                                                                                                                                       

tests/test_example.py::test_custom_fixture Setting up fixture: session - event_loop_policy
Finished setting up fixture: session - event_loop_policy
Setting up fixture: session - twisted_greenlet
Finished setting up fixture: session - twisted_greenlet
Setting up fixture: session - _session_faker
Finished setting up fixture: session - _session_faker
Setting up fixture: session - base_url
Finished setting up fixture: session - base_url
Setting up fixture: session - _verify_url
Finished setting up fixture: session - _verify_url
Setting up fixture: session - sensitive_url
Finished setting up fixture: session - sensitive_url
Setting up fixture: function - _skip_sensitive
Finished setting up fixture: function - _skip_sensitive
Setting up fixture: function - dynamic_fixture
Finished setting up fixture: function - dynamic_fixture
FAILED
tests/test_example.py::test_addition Setting up fixture: function - _skip_sensitive
Finished setting up fixture: function - _skip_sensitive
PASSED
tests/test_example.py::test_division_by_zero Setting up fixture: function - _skip_sensitive
Finished setting up fixture: function - _skip_sensitive
FAILED
tests/test_example.py::test_subtraction Setting up fixture: function - _skip_sensitive
Finished setting up fixture: function - _skip_sensitive
PASSED

======================================================================================================================= FAILURES ========================================================================================================================
__________________________________________________________________________________________________________________ test_custom_fixture __________________________________________________________________________________________________________________

dynamic_fixture = 'default value'

    def test_custom_fixture(dynamic_fixture):
>       assert dynamic_fixture == "custom setup value"
E       AssertionError: assert 'default value' == 'custom setup value'
E         
E         - custom setup value
E         + default value

tests/test_example.py:8: AssertionError
_________________________________________________________________________________________________________________ test_division_by_zero _________________________________________________________________________________________________________________

    def test_division_by_zero():
>       assert 1 / 0  # 这将引发一个ZeroDivisionError，触发调试模式
E       ZeroDivisionError: division by zero

tests/test_example.py:14: ZeroDivisionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_custom_fixture - AssertionError: assert 'default value' == 'custom setup value'
FAILED tests/test_example.py::test_division_by_zero - ZeroDivisionError: division by zero
============================================================================================================== 2 failed, 2 passed in 0.12s ==============================================================================================================
root@Gavin:~/test/hook#
```

## 案例二：调试和日志记录

目标：在 `fixture` 设置过程中添加日志记录。

步骤：
1. 使用 `pytest_fixture_setup` 钩子函数。
2. 在钩子函数中记录日志。

**示例代码**：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='fixtures.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    """在 fixture 设置过程中记录日志"""
    logging.info(f"Setting up fixture: {fixturedef.scope} - {fixturedef.argname}")
    
    # 获取实际 fixture setup 的结果
    outcome = yield
    result = outcome.get_result()
    
    logging.info(f"Finished setting up fixture: {fixturedef.scope} - {fixturedef.argname}")
    return result
```

**解释：**
- 使用 `logging` 模块记录 `fixture` 设置过程的日志信息，包括`fixture` 的作用域和参数名。


**运行效果:**

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
collected 4 items                                                                                                                                                                                                                                       

tests/test_example.py::test_custom_fixture FAILED
tests/test_example.py::test_addition PASSED
tests/test_example.py::test_division_by_zero FAILED
tests/test_example.py::test_subtraction PASSED

======================================================================================================================= FAILURES ========================================================================================================================
__________________________________________________________________________________________________________________ test_custom_fixture __________________________________________________________________________________________________________________

dynamic_fixture = 'default value'

    def test_custom_fixture(dynamic_fixture):
>       assert dynamic_fixture == "custom setup value"
E       AssertionError: assert 'default value' == 'custom setup value'
E         
E         - custom setup value
E         + default value

tests/test_example.py:8: AssertionError
------------------------------------------------------------------------------------------------------------------ Captured log setup -------------------------------------------------------------------------------------------------------------------
INFO     root:conftest.py:11 Setting up fixture: session - event_loop_policy
INFO     root:conftest.py:17 Finished setting up fixture: session - event_loop_policy
INFO     root:conftest.py:11 Setting up fixture: session - twisted_greenlet
INFO     root:conftest.py:17 Finished setting up fixture: session - twisted_greenlet
INFO     root:conftest.py:11 Setting up fixture: session - _session_faker
INFO     root:conftest.py:17 Finished setting up fixture: session - _session_faker
INFO     root:conftest.py:11 Setting up fixture: session - base_url
INFO     root:conftest.py:17 Finished setting up fixture: session - base_url
INFO     root:conftest.py:11 Setting up fixture: session - _verify_url
INFO     root:conftest.py:17 Finished setting up fixture: session - _verify_url
INFO     root:conftest.py:11 Setting up fixture: session - sensitive_url
INFO     root:conftest.py:17 Finished setting up fixture: session - sensitive_url
INFO     root:conftest.py:11 Setting up fixture: function - _skip_sensitive
INFO     root:conftest.py:17 Finished setting up fixture: function - _skip_sensitive
INFO     root:conftest.py:11 Setting up fixture: function - dynamic_fixture
INFO     root:conftest.py:17 Finished setting up fixture: function - dynamic_fixture
_________________________________________________________________________________________________________________ test_division_by_zero _________________________________________________________________________________________________________________

    def test_division_by_zero():
>       assert 1 / 0  # 这将引发一个ZeroDivisionError，触发调试模式
E       ZeroDivisionError: division by zero

tests/test_example.py:14: ZeroDivisionError
------------------------------------------------------------------------------------------------------------------ Captured log setup -------------------------------------------------------------------------------------------------------------------
INFO     root:conftest.py:11 Setting up fixture: function - _skip_sensitive
INFO     root:conftest.py:17 Finished setting up fixture: function - _skip_sensitive
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_custom_fixture - AssertionError: assert 'default value' == 'custom setup value'
FAILED tests/test_example.py::test_division_by_zero - ZeroDivisionError: division by zero
============================================================================================================== 2 failed, 2 passed in 0.11s ==============================================================================================================
root@Gavin:~/test/hook# cat fixtures.log 
2024-06-05 18:29:44,024 - Setting up fixture: session - event_loop_policy
2024-06-05 18:29:44,024 - Finished setting up fixture: session - event_loop_policy
2024-06-05 18:29:44,024 - Setting up fixture: session - twisted_greenlet
2024-06-05 18:29:44,024 - Finished setting up fixture: session - twisted_greenlet
2024-06-05 18:29:44,025 - Setting up fixture: session - _session_faker
2024-06-05 18:29:44,042 - Finished setting up fixture: session - _session_faker
2024-06-05 18:29:44,042 - Setting up fixture: session - base_url
2024-06-05 18:29:44,042 - Finished setting up fixture: session - base_url
2024-06-05 18:29:44,042 - Setting up fixture: session - _verify_url
2024-06-05 18:29:44,042 - Finished setting up fixture: session - _verify_url
2024-06-05 18:29:44,042 - Setting up fixture: session - sensitive_url
2024-06-05 18:29:44,043 - Finished setting up fixture: session - sensitive_url
2024-06-05 18:29:44,043 - Setting up fixture: function - _skip_sensitive
2024-06-05 18:29:44,043 - Finished setting up fixture: function - _skip_sensitive
2024-06-05 18:29:44,043 - Setting up fixture: function - dynamic_fixture
2024-06-05 18:29:44,043 - Finished setting up fixture: function - dynamic_fixture
2024-06-05 18:29:44,067 - Setting up fixture: function - _skip_sensitive
2024-06-05 18:29:44,067 - Finished setting up fixture: function - _skip_sensitive
2024-06-05 18:29:44,068 - Setting up fixture: function - _skip_sensitive
2024-06-05 18:29:44,068 - Finished setting up fixture: function - _skip_sensitive
2024-06-05 18:29:44,069 - Setting up fixture: function - _skip_sensitive
2024-06-05 18:29:44,069 - Finished setting up fixture: function - _skip_sensitive
root@Gavin:~/test/hook#
```

## 案例三：条件性初始化

目标：根据参数动态改变 `fixture` 的初始化行为。

步骤：
1. 定义一个需要根据参数动态初始化的 `fixture`。
2. 使用 `pytest_fixture_setup` 钩子函数，根据需要修改初始化行为。

**示例代码**：

```python
# conftest.py
import pytest

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    """根据参数动态改变 fixture 的初始化行为"""
    if fixturedef.scope == "function" and fixturedef.argname == "dynamic_fixture":
        print("Custom setup for dynamic_fixture")
        fixturedef.cached_result = ("custom setup value", request.param_index, None)
        yield
    else:
        outcome = yield
        result = outcome.get_result()
        fixturedef.cached_result = (result, request.param_index, None)

@pytest.fixture
def dynamic_fixture():
    return "default value"

# tests/test_example.py
def test_custom_fixture(dynamic_fixture):
    assert dynamic_fixture == "custom setup value"

def test_default_fixture(dynamic_fixture):
    assert dynamic_fixture == "default value"
```

**解释：**
- 使用 `pytest_fixture_setup` 钩子根据 `fixture` 的作用域和参数名来动态修改初始化行为。
- 在 `fixture` 中使用不同的参数，实现条件性初始化。


**运行效果:**

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

tests/test_example.py::test_custom_fixture Custom setup for dynamic_fixture
FAILED
tests/test_example.py::test_default_fixture Custom setup for dynamic_fixture
PASSED

======================================================================================================================= FAILURES ========================================================================================================================
__________________________________________________________________________________________________________________ test_custom_fixture __________________________________________________________________________________________________________________

dynamic_fixture = 'default value'

    def test_custom_fixture(dynamic_fixture):
>       assert dynamic_fixture == "custom setup value"
E       AssertionError: assert 'default value' == 'custom setup value'
E         
E         - custom setup value
E         + default value

tests/test_example.py:2: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_custom_fixture - AssertionError: assert 'default value' == 'custom setup value'
============================================================================================================== 1 failed, 1 passed in 0.11s ==============================================================================================================
root@Gavin:~/test/hook# 
```


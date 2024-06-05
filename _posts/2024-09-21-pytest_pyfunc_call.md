---
title: pytest hook系列之pytest_pyfunc_call
date: 2024-09-21 23:00:00
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
summary: pytest hook之pytest_pyfunc_call
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_pyfunc_call` 是`pytest`框架中的一个钩子函数，允许我们在测试函数被调用时执行自定义逻辑。通过这个钩子，我们可以在测试函数调用前后插入特定的行为，这为我们提供了极大的灵活性，以满足各种复杂的测试需求。

# 什么是pytest_pyfunc_call？

`pytest_pyfunc_call` 是一个`pytest`提供的钩子函数，它在测试函数被调用时触发。通过这个钩子，我们可以在测试函数运行之前或之后执行自定义的操作，甚至替换测试函数的执行逻辑。

# 使用场景

1. **记录函数调用信息**：在测试函数被调用时记录详细的信息，如参数、返回值等。
2. **自定义测试函数执行逻辑**：根据特定条件，自定义或替换测试函数的执行逻辑。
3. **增加前置或后置操作**：在测试函数执行之前或之后增加前置或后置操作，如设置环境、清理资源等。

# 参数

```python
def pytest_pyfunc_call(pyfuncitem):
    # pyfuncitem: 被调用的测试函数项，包含测试函数的详细信息
    pass
```
- `pyfuncitem`：被调用的测试函数项，包含测试函数的详细信息，包括函数对象、参数等。

# 示例代码

## 案例一：记录函数调用信息

目标：在测试函数被调用时记录详细的信息，如函数名称、参数、返回值等。

步骤：

1. 使用 `pytest_pyfunc_call` 钩子函数。
2. 在测试函数调用前后记录相关信息。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='test_calls.log', level=logging.INFO, format='%(asctime)s - %(message)s')

@pytest.hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    # 记录测试函数调用信息
    func_name = pyfuncitem.name
    func_args = pyfuncitem.funcargs
    logging.info(f"Calling test function: {func_name} with arguments: {func_args}")

    # 执行实际的测试函数
    outcome = yield

    # 获取测试函数执行结果
    try:
        result = outcome.get_result()
        logging.info(f"Test function {func_name} finished with result: {result}")
    except Exception as e:
        logging.error(f"Test function {func_name} raised an exception: {e}")

# 示例测试文件 `tests/test_example.py`
import pytest

def test_example1():
    assert 1 + 1 == 2

def test_example2(a, b):
    assert a + b == 4   

# conftest.py 里面增加一个 Fixture 给 test_example2 提供参数
@pytest.fixture
def a():
    return 2

@pytest.fixture
def b():
    return 2
```

**注释**：

- 在 `pytest_pyfunc_call` 钩子中，通过 `logging` 记录测试函数名称及参数。
- 执行测试函数并记录其返回值。


运行效果：

```shell
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

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSED

=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Jun  1 16:34 ./
drwxr-xr-x 4 root root 4096 May 30 16:27 ../
-rw-r--r-- 1 root root  756 Jun  1 16:34 conftest.py
drwxr-xr-x 2 root root 4096 Jun  1 16:34 __pycache__/
drwxr-xr-x 3 root root 4096 Jun  1 16:34 .pytest_cache/
-rw-r--r-- 1 root root 1126 Jun  1 16:34 test_calls.log
drwxr-xr-x 3 root root 4096 Jun  1 16:32 tests/
root@Gavin:~/test/hook# cat test_calls.log 
2024-06-01 16:34:17,843 - Calling test function: test_example1 with arguments: {'event_loop_policy': <asyncio.unix_events._UnixDefaultEventLoopPolicy object at 0x74b03486dcd0>, 'twisted_greenlet': <greenlet.greenlet object at 0x74b034feb780 (otid=0x(nil)) pending>, '_session_faker': <faker.proxy.Faker object at 0x74b034889c10>, '_verify_url': None, 'sensitive_url': False, 'base_url': '', '_skip_sensitive': None, 'request': <FixtureRequest for <Function test_example1>>}
2024-06-01 16:34:17,843 - Test function test_example1 finished with result: True
2024-06-01 16:34:17,845 - Calling test function: test_example2 with arguments: {'event_loop_policy': <asyncio.unix_events._UnixDefaultEventLoopPolicy object at 0x74b03486dcd0>, 'twisted_greenlet': <greenlet.greenlet object at 0x74b034feb780 (otid=0x(nil)) pending>, '_session_faker': <faker.proxy.Faker object at 0x74b034889c10>, '_verify_url': None, 'sensitive_url': False, 'base_url': '', '_skip_sensitive': None, 'a': 2, 'b': 2, 'request': <FixtureRequest for <Function test_example2>>}
2024-06-01 16:34:17,845 - Test function test_example2 finished with result: True
root@Gavin:~/test/hook#
```


## 案例二：自定义测试函数执行逻辑

目标：根据特定条件，自定义或替换测试函数的执行逻辑。

步骤：

1. 使用 `pytest_pyfunc_call` 钩子函数。
2. 根据特定条件自定义或替换测试函数的执行逻辑。

示例代码：

```python
# conftest.py
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    func_name = pyfuncitem.name

    # 自定义执行逻辑，根据特定条件
    if func_name == "test_custom_logic":
        print(f"Custom logic for: {func_name}")

        # 自定义逻辑：替换实际测试函数的执行逻辑
        def custom_logic(*args, **kwargs):
            assert 2 + 2 == 5  # 这是个故意失败的例子

        # 直接运行自定义逻辑
        custom_logic()
        
        # 防止 pytest 运行原始测试逻辑
        outcome = yield pytest.CallInfo(lambda: None, when="call")
        outcome.get_result()
        return

    # 运行默认的测试逻辑
    outcome = yield
    result = outcome.get_result()

# 示例测试文件 `tests/test_example.py`
def test_custom_logic():
    assert 1 + 1 == 2  # 实际这个测试用例的逻辑会被替换

def test_normal_logic():
    assert 1 + 1 == 2
```

**注释**：

- 在 `pytest_pyfunc_call` 钩子中，根据函数名称决定是否自定义执行逻辑。
- 如果匹配特定条件，实现自定义测试函数逻辑，否则使用默认运行逻辑。


运行效果：

```shell
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

tests/test_example.py::test_custom_logic Custom logic for: test_custom_logic
FAILED
tests/test_example.py::test_normal_logic PASSED

======================================================================================================================= FAILURES ========================================================================================================================
___________________________________________________________________________________________________________________ test_custom_logic ___________________________________________________________________________________________________________________

pyfuncitem = <Function test_custom_logic>

    @pytest.hookimpl(hookwrapper=True)
    def pytest_pyfunc_call(pyfuncitem):
        func_name = pyfuncitem.name
    
        # 自定义执行逻辑，根据特定条件
        if func_name == "test_custom_logic":
            print(f"Custom logic for: {func_name}")
    
            # 自定义逻辑：替换实际测试函数的执行逻辑
            def custom_logic(*args, **kwargs):
                assert 2 + 2 == 5  # 这是个故意失败的例子
    
            # 直接运行自定义逻辑
>           custom_logic()

conftest.py:16: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

args = (), kwargs = {}, @py_assert0 = 2, @py_assert2 = 2, @py_assert4 = 4, @py_assert6 = 5, @py_assert5 = False, @py_format8 = '(2 + 2) == 5', @py_format10 = 'assert (2 + 2) == 5'

    def custom_logic(*args, **kwargs):
>       assert 2 + 2 == 5  # 这是个故意失败的例子
E       assert (2 + 2) == 5

conftest.py:13: AssertionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_custom_logic - assert (2 + 2) == 5
============================================================================================================== 1 failed, 1 passed in 0.11s ==============================================================================================================
root@Gavin:~/test/hook#
```


## 案例三：增加前置或后置操作

目标：在测试函数执行之前或之后增加前置或后置操作，如设置环境、清理资源等。

步骤：

1. 使用 `pytest_pyfunc_call` 钩子函数。
2. 在测试函数执行之前或之后实现前置或后置操作。

示例代码：

```python
# conftest.py
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    func_name = pyfuncitem.name

    # 前置操作：打印函数调用前的信息
    print(f"Before calling {func_name}")

    # 执行测试函数
    outcome = yield

    # 后置操作：打印函数调用后的信息
    print(f"After calling {func_name}")

    # 获取结果，这里是为了确保 pytest 的流程顺利
    outcome.get_result()


# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 1 + 1 == 2
```

**注释**：

- 添加前置操作，在测试函数执行前打印信息。
- 添加后置操作，在测试函数执行后打印信息。


运行效果：

```shell
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

tests/test_example.py::test_example Before calling test_example
After calling test_example
PASSED

=================================================================================================================== 1 passed in 0.03s ===================================================================================================================
root@Gavin:~/test/hook# 
```


# 总结

通过详细介绍 `pytest_pyfunc_call` 钩子的使用场景、参数及应用示例，希望能帮助你更好地理解和使用这个钩子函数。无论是记录详细的函数调用信息，自定义测试函数执行逻辑，还是增加前置或后置操作，都能为你提供强大的工具，满足各种复杂的测试需求。

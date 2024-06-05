---
title: pytest hook系列之pytest_warning_recorded
date: 2024-10-16 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-20.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_warning_recorded
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_warning_recorded` 是 `Pytest`框架中的一个钩子函数，用于记录和处理测试过程中发出的警告信息。通过这个钩子函数，我们可以在测试过程中拦截、记录和处理警告，甚至是过滤特定类型的警告，不仅提高了调试的灵活性，也增强了测试报告的准确性。

# 使用场景

1. **记录警告详情**：在测试日志或报告中记录所有发出的警告，包括警告消息、级别、触发位置等。
2. **过滤特定警告**：对特定类型的警告进行捕获和过滤，避免测试报告中充斥过多无关紧要的警告信息。
3. **调整警告级别**：根据开发需求，将某些警告的级别调整为错误或忽略，确保测试结果的准确性。
4. **调试和分析**：通过拦截和记录警告，分析程序中的潜在问题并进行调试。

# 参数

```python
def pytest_warning_recorded(warning_message, when, nodeid, location):
    # warning_message: 警告消息对象，包含警告的详细信息
    # when: 触发警告的阶段，如'runtest'、'setup'、'teardown'
    # nodeid: 触发警告的测试节点ID
    # location: 警告信息中的位置，如代码所在文件和行号等
    pass
```

- `warning_message`：警告消息对象，包含警告的详细信息。
- `when`：触发警告的阶段，包括 `'runtest', 'setup', 'teardown'` 等。
- `nodeid`：触发警告的测试节点ID。
- `location`：警告信息中的位置，如代码所在文件和行号等。

# 示例代码

## 案例一：记录警告详情

目标：在测试日志或报告中记录所有发出的警告，包括警告消息、级别、触发位置等。

步骤：
1. 使用 `pytest_warning_recorded` 钩子函数。
2. 在钩子函数中插入警告记录代码。

示例代码：

```python
# conftest.py
import pytest

def pytest_warning_recorded(warning_message, when, nodeid, location):
    """记录警告详情"""
    with open('warnings.log', 'a') as f:
        f.write(f"{when} - {nodeid} - {location}\n")
        f.write(f"Message: {warning_message.message}\n")
        f.write(f"Category: {warning_message.category.__name__}\n")
        f.write(f"File: {warning_message.filename}\n")
        f.write(f"Line: {warning_message.lineno}\n")
        f.write("="*40 + "\n")

# 示例测试文件 tests/test_warnings.py

import warnings

def test_warning():
    warnings.warn("This is a test warning", UserWarning)
    assert True
```

**注释**：
- 在 `pytest_warning_recorded` 钩子中，将警告的详细信息记录到 `warnings.log` 文件中。
- 警告详细信息包括：触发阶段、测试节点ID、位置、消息、类别、文件和行号。

**运行效果**：

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

tests/test_example.py::test_warning PASSED

=================================================================================================================== warnings summary ====================================================================================================================
tests/test_example.py::test_warning
  /root/test/hook/tests/test_example.py:4: UserWarning: This is a test warning
    warnings.warn("This is a test warning", UserWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================================================================================= 1 passed, 1 warning in 0.03s ==============================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Jun  4 19:41 ./
drwxr-xr-x 6 root root 4096 Jun  4 18:49 ../
-rw-r--r-- 1 root root  472 Jun  4 19:41 conftest.py
drwxr-xr-x 2 root root 4096 Jun  4 19:41 __pycache__/
drwxr-xr-x 3 root root 4096 Jun  4 19:41 .pytest_cache/
drwxr-xr-x 3 root root 4096 Jun  4 19:41 tests/
-rw-r--r-- 1 root root  200 Jun  4 19:41 warnings.log
root@Gavin:~/test/hook# cat warnings.log 
runtest - tests/test_example.py::test_warning - None
Message: This is a test warning
Category: UserWarning
File: /root/test/hook/tests/test_example.py
Line: 4
========================================
root@Gavin:~/test/hook#
```

## 案例二：过滤特定警告

目标：对特定类型的警告进行捕获和过滤，避免测试报告中充斥过多无关紧要的警告信息。

步骤：
1. 使用 `pytest_warning_recorded` 钩子函数。
2. 在钩子函数中插入警告过滤代码。

示例代码：

```python
# conftest.py
import pytest

def pytest_warning_recorded(warning_message, when, nodeid, location):
    """过滤特定类型的警告"""
    if warning_message.category == DeprecationWarning:
        # 忽略特定类型的警告
        return
    with open('warnings.log', 'a') as f:
        f.write(f"{when} - {nodeid} - {location}\n")
        f.write(f"Message: {warning_message.message}\n")
        f.write(f"Category: {warning_message.category.__name__}\n")
        f.write(f"File: {warning_message.filename}\n")
        f.write(f"Line: {warning_message.lineno}\n")
        f.write("="*40 + "\n")

# 示例测试文件 tests/test_warnings.py

import warnings

def test_warning():
    warnings.warn("This is a test warning", UserWarning)
    warnings.warn("This is a deprecation warning", DeprecationWarning)
    assert True
```

**注释**：
- 在 `pytest_warning_recorded` 钩子中，对 `DeprecationWarning` 类型的警告进行过滤忽略。

**运行效果**：

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

tests/test_example.py::test_warning PASSED

=================================================================================================================== warnings summary ====================================================================================================================
tests/test_example.py::test_warning
  /root/test/hook/tests/test_example.py:4: UserWarning: This is a test warning
    warnings.warn("This is a test warning", UserWarning)

tests/test_example.py::test_warning
  /root/test/hook/tests/test_example.py:5: DeprecationWarning: This is a deprecation warning
    warnings.warn("This is a deprecation warning", DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================================================================================= 1 passed, 2 warnings in 0.03s =============================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Jun  4 19:43 ./
drwxr-xr-x 6 root root 4096 Jun  4 18:49 ../
-rw-r--r-- 1 root root  589 Jun  4 19:43 conftest.py
drwxr-xr-x 2 root root 4096 Jun  4 19:43 __pycache__/
drwxr-xr-x 3 root root 4096 Jun  4 19:41 .pytest_cache/
drwxr-xr-x 3 root root 4096 Jun  4 19:43 tests/
-rw-r--r-- 1 root root  200 Jun  4 19:43 warnings.log
root@Gavin:~/test/hook# cat warnings.log 
runtest - tests/test_example.py::test_warning - None
Message: This is a test warning
Category: UserWarning
File: /root/test/hook/tests/test_example.py
Line: 4
========================================
root@Gavin:~/test/hook#
```


## 案例三：调整警告级别

目标：根据开发需求，将某些警告的级别调整为错误或忽略，确保测试结果的准确性。

步骤：
1. 使用 `pytest_warning_recorded` 钩子函数。
2. 在钩子函数中插入调整警告级别的代码。

示例代码：

```python
# conftest.py
import pytest
import warnings

def pytest_warning_recorded(warning_message, when, nodeid, location):
    """调整特定警告的级别"""
    if warning_message.category == UserWarning:
        # 提升 UserWarning 到错误级别
        raise pytest.fail(f"UserWarning as Error: {warning_message.message}")
    with open('warnings.log', 'a') as f:
        f.write(f"{when} - {nodeid} - {location}\n")
        f.write(f"Message: {warning_message.message}\n")
        f.write(f"Category: {warning_message.category.__name__}\n")
        f.write(f"File: {warning_message.filename}\n")
        f.write(f"Line: {warning_message.lineno}\n")
        f.write("="*40 + "\n")

# 示例测试文件 tests/test_warnings.py

import warnings

def test_warning():
    warnings.warn("This is a test warning", UserWarning)
    assert True
```

**注释**：
- 在 `pytest_warning_recorded` 钩子中，将 `UserWarning` 类型的警告提升到错误级别并抛出 `pytest.fail` 异常。


**运行效果**：

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

tests/test_example.py::test_warning PASSED
INTERNALERROR> Traceback (most recent call last):
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 273, in wrap_session
INTERNALERROR>     session.exitstatus = doit(config, session) or 0
INTERNALERROR>                          ^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 327, in _main
INTERNALERROR>     config.hook.pytest_runtestloop(session=session)
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_hooks.py", line 513, in __call__
INTERNALERROR>     return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_manager.py", line 120, in _hookexec
INTERNALERROR>     return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 139, in _multicall
INTERNALERROR>     raise exception.with_traceback(exception.__traceback__)
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 122, in _multicall
INTERNALERROR>     teardown.throw(exception)  # type: ignore[union-attr]
INTERNALERROR>     ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/logging.py", line 796, in pytest_runtestloop
INTERNALERROR>     return (yield)  # Run all the tests.
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
INTERNALERROR>     res = hook_impl.function(*args)
INTERNALERROR>           ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 352, in pytest_runtestloop
INTERNALERROR>     item.config.hook.pytest_runtest_protocol(item=item, nextitem=nextitem)
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_hooks.py", line 513, in __call__
INTERNALERROR>     return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_manager.py", line 120, in _hookexec
INTERNALERROR>     return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 182, in _multicall
INTERNALERROR>     return outcome.get_result()
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_result.py", line 100, in get_result
INTERNALERROR>     raise exc.with_traceback(exc.__traceback__)
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 169, in _multicall
INTERNALERROR>     teardown.send(outcome._result)
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/warnings.py", line 106, in pytest_runtest_protocol
INTERNALERROR>     with catch_warnings_for_item(
INTERNALERROR>   File "/usr/lib/python3.11/contextlib.py", line 144, in __exit__
INTERNALERROR>     next(self.gen)
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/warnings.py", line 64, in catch_warnings_for_item
INTERNALERROR>     ihook.pytest_warning_recorded.call_historic(
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_hooks.py", line 535, in call_historic
INTERNALERROR>     res = self._hookexec(self.name, self._hookimpls.copy(), kwargs, False)
INTERNALERROR>           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_manager.py", line 120, in _hookexec
INTERNALERROR>     return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 139, in _multicall
INTERNALERROR>     raise exception.with_traceback(exception.__traceback__)
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
INTERNALERROR>     res = hook_impl.function(*args)
INTERNALERROR>           ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/root/test/hook/conftest.py", line 8, in pytest_warning_recorded
INTERNALERROR>     raise pytest.fail(f"UserWarning as Error: {warning_message.message}")
INTERNALERROR>           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/outcomes.py", line 188, in fail
INTERNALERROR>     raise Failed(msg=reason, pytrace=pytrace)
INTERNALERROR> Failed: UserWarning as Error: This is a test warning

============================================================================================================= 1 passed, 1 warning in 0.04s ==============================================================================================================
root@Gavin:~/test/hook#
root@Gavin:~/test/hook# cat warnings.log 
2024-06-04 19:44:59,297 - runtest - tests/test_example.py::test_warning - None
2024-06-04 19:44:59,297 - Message: This is a test warning
2024-06-04 19:44:59,297 - Category: UserWarning
2024-06-04 19:44:59,297 - File: /root/test/hook/tests/test_example.py
2024-06-04 19:44:59,297 - Line: 4
root@Gavin:~/test/hook# 
```

## 案例四：调试和分析

目标：通过拦截和记录警告，分析程序中的潜在问题并进行调试。

步骤：
1. 使用 `pytest_warning_recorded` 钩子函数。
2. 在钩子函数中插入调试和分析的代码。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='warnings.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_warning_recorded(warning_message, when, nodeid, location):
    """记录警告详情用于调试和分析"""
    logging.info(f"{when} - {nodeid} - {location}")
    logging.info(f"Message: {warning_message.message}")
    logging.info(f"Category: {warning_message.category.__name__}")
    logging.info(f"File: {warning_message.filename}")
    logging.info(f"Line: {warning_message.lineno}")

# 示例测试文件 tests/test_warnings.py

import warnings

def test_warning():
    warnings.warn("This is a test warning", UserWarning)
    assert True
```

**注释**：
- 在 `pytest_warning_recorded` 钩子中，将警告的详细信息记录到日志文件 `warnings.log` 中。
- 使用 Python 的 `logging` 模块记录警告，适用于需要调试和分析的项目。


**运行效果**：

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

tests/test_example.py::test_warning PASSED

=================================================================================================================== warnings summary ====================================================================================================================
tests/test_example.py::test_warning
  /root/test/hook/tests/test_example.py:4: UserWarning: This is a test warning
    warnings.warn("This is a test warning", UserWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================================================================================= 1 passed, 1 warning in 0.04s ==============================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Jun  4 19:46 ./
drwxr-xr-x 6 root root 4096 Jun  4 18:49 ../
-rw-r--r-- 1 root root  554 Jun  4 19:46 conftest.py
drwxr-xr-x 2 root root 4096 Jun  4 19:46 __pycache__/
drwxr-xr-x 3 root root 4096 Jun  4 19:41 .pytest_cache/
drwxr-xr-x 3 root root 4096 Jun  4 19:46 tests/
-rw-r--r-- 1 root root  289 Jun  4 19:46 warnings.log
root@Gavin:~/test/hook# cat warnings.log 
2024-06-04 19:46:59,297 - runtest - tests/test_example.py::test_warning - None
2024-06-04 19:46:59,297 - Message: This is a test warning
2024-06-04 19:46:59,297 - Category: UserWarning
2024-06-04 19:46:59,297 - File: /root/test/hook/tests/test_example.py
2024-06-04 19:46:59,297 - Line: 4
root@Gavin:~/test/hook# 
```


# 高级用例：结合pytest_warning_recorded与其他钩子

通过结合 `pytest_warning_recorded` 与其他 `pytest` 钩子，我们可以实现更复杂和更实用的功能。例如，在测试会话结束时生成一份综合报告，包括警告详情、测试结果等。

## 扩展示例：综合报告生成

在测试会话结束时，生成包含警告详情、测试结果和覆盖率信息的综合报告，并保存为 `JSON` 文件和文本文件。

```python
# conftest.py
import pytest
import coverage
from colorama import Fore, Style, init
import json

init(autoreset=True)  # 自动重置颜色

cov = None
test_summary = {
    'total': 0,
    'passed': 0,
    'failed': 0,
    'skipped': 0,
    'by_module': {},
    'failures': [],
    'warnings': []
}

def pytest_configure(config):
    global cov
    """在 pytest 配置时，启动覆盖率插件"""
    cov = coverage.Coverage()
    cov.start()

def pytest_sessionfinish(session, exitstatus):
    global cov
    """在测试会话结束时停止覆盖率收集并保存数据"""
    if cov:
        cov.stop()
        cov.save()

def pytest_warning_recorded(warning_message, nodeid, location):
    """记录警告详情"""
    global test_summary
    warning_info = {
        'nodeid': nodeid,
        'location': location,
        'message': str(warning_message.message),
        'category': warning_message.category.__name__,
        'filename': warning_message.filename,
        'lineno': warning_message.lineno
    }
    test_summary['warnings'].append(warning_info)

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    global cov, test_summary
    """在测试结束时汇总报告统计信息、警告详情和覆盖率信息，并保存报告和结果"""
    stats = terminalreporter.stats

    test_summary['total'] = sum(len(stats.get(stat, [])) for stat in ['passed', 'failed', 'skipped'])
    test_summary['passed'] = len(stats.get('passed', []))
    test_summary['failed'] = len(stats.get('failed', []))
    test_summary['skipped'] = len(stats.get('skipped', []))
    
    for stat in ['passed', 'failed', 'skipped']:
        for report in stats.get(stat, []):
            module = report.location[0]
            if module not in test_summary['by_module']:
                test_summary['by_module'][module] = {'passed': 0, 'failed': 0, 'skipped': 0}
            test_summary['by_module'][module][stat] += 1
            
            if stat == 'failed':
                test_summary['failures'].append({
                    'name': report.nodeid,
                    'reason': str(report.longrepr)
                })

    # 输出警告详情到终端
    terminalreporter.write_sep("=", f"{Fore.MAGENTA}Warnings Summary")
    for warning in test_summary['warnings']:
        terminalreporter.write_line(f"{warning['nodeid']} - {warning['location']}")
        terminalreporter.write_line(f"Message: {warning['message']}")
        terminalreporter.write_line(f"Category: {warning['category']}")
        terminalreporter.write_line(f"File: {warning['filename']}")
        terminalreporter.write_line(f"Line: {warning['lineno']}")
        terminalreporter.write_line("="*40)

    terminalreporter.write_sep("=", f"{Fore.CYAN}Test Summary")
    terminalreporter.write_line(f"{Fore.GREEN}Passed: {test_summary['passed']}")
    terminalreporter.write_line(f"{Fore.RED}Failed: {test_summary['failed']}")
    terminalreporter.write_line(f"{Fore.YELLOW}Skipped: {test_summary['skipped']}")
    
    terminalreporter.write_sep("=", f"{Fore.RED}Failure Summary")
    for report in stats.get('failed', []):
        terminalreporter.write_line(f"{Fore.RED}{report.nodeid}: {report.longrepr}")
    
    terminalreporter.write_sep("=", f"{Fore.BLUE}Coverage Summary")
    if cov and cov.get_data().measured_files():
        cov.report(file=terminalreporter._tw)
    else:
        terminalreporter.write_line(f"{Fore.RED}No coverage data to report.")

    terminalreporter.write_sep("=", f"{Fore.MAGENTA}Module-wise Summary")
    for module, counts in test_summary['by_module'].items():
        terminalreporter.write_line(f"{module}: Passed: {counts['passed']}, Failed: {counts['failed']}, Skipped: {counts['skipped']}")

    # 保存警告、总结、覆盖率信息为 JSON 文件
    with open('test_summary_report.json', 'w') as f:
        json.dump(test_summary, f, indent=4)

    # 保存警告、总结、覆盖率信息为文本文件
    with open('test_summary_report.txt', 'w') as f:
        f.write("Test Summary\n")
        f.write(f"Passed: {test_summary['passed']}\n")
        f.write(f"Failed: {test_summary['failed']}\n")
        f.write(f"Skipped: {test_summary['skipped']}\n")
        f.write("\nFailure Summary\n")
        for report in stats.get('failed', []):
            f.write(f"{report.nodeid}: {report.longrepr}\n")
        f.write("\nWarnings Summary\n")
        for warning in test_summary['warnings']:
            f.write(f"{warning['nodeid']} - {warning['location']}\n")
            f.write(f"Message: {warning['message']}\n")
            f.write(f"Category: {warning['category']}\n")
            f.write(f"File: {warning['filename']}\n")
            f.write(f"Line: {warning['lineno']}\n")
            f.write("="*40 + "\n")
        f.write("\nCoverage Summary\n")
        if cov and cov.get_data().measured_files():
            cov.report(file=f)
        else:
            f.write("No coverage data to report.\n")
        f.write("\nModule-wise Summary\n")
        for module, counts in test_summary['by_module'].items():
            f.write(f"{module}: Passed: {counts['passed']}, Failed: {counts['failed']}, Skipped: {counts['skipped']}\n")

# 示例测试文件 tests/test_warnings.py
import pytest
import warnings

@pytest.mark.unit
def test_unit_passed():
    assert 1 + 1 == 2

@pytest.mark.integration
def test_integration_passed():
    assert 2 + 2 == 4

def test_failed():
    warnings.warn("This is a failing test warning", UserWarning)
    assert 1 + 1 == 3

def test_skipped():
    pytest.skip("Skipping this test")
```

## 运行和验证

控制台输出应包括综合报告，警告详情、测试结果、覆盖率报告，并生成 `test_summary_report.json` 和 `test_summary_report.txt` 文件。

### 控制台输出示例

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
collected 4 items                                                                                                                                                                                                                                       

tests/test_example.py::test_unit_passed PASSED
tests/test_example.py::test_integration_passed PASSED
tests/test_example.py::test_failed FAILED
tests/test_example.py::test_skipped SKIPPED (Skipping this test)

======================================================================================================================= FAILURES ========================================================================================================================
______________________________________________________________________________________________________________________ test_failed ______________________________________________________________________________________________________________________

    def test_failed():
        warnings.warn("This is a failing test warning", UserWarning)
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:14: AssertionError
=================================================================================================================== warnings summary ====================================================================================================================
tests/test_example.py:4
  /root/test/hook/tests/test_example.py:4: PytestUnknownMarkWarning: Unknown pytest.mark.unit - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.unit

tests/test_example.py:8
  /root/test/hook/tests/test_example.py:8: PytestUnknownMarkWarning: Unknown pytest.mark.integration - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.integration

tests/test_example.py::test_failed
  /root/test/hook/tests/test_example.py:13: UserWarning: This is a failing test warning
    warnings.warn("This is a failing test warning", UserWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================================================================================================= Warnings Summary =================================================================================================================
 - None
Message: Unknown pytest.mark.unit - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
Category: PytestUnknownMarkWarning
File: /root/test/hook/tests/test_example.py
Line: 4
========================================
 - None
Message: Unknown pytest.mark.integration - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
Category: PytestUnknownMarkWarning
File: /root/test/hook/tests/test_example.py
Line: 8
========================================
tests/test_example.py::test_failed - None
Message: This is a failing test warning
Category: UserWarning
File: /root/test/hook/tests/test_example.py
Line: 13
========================================
=================================================================================================================== Test Summary ===================================================================================================================
Passed: 2
Failed: 1
Skipped: 1
================================================================================================================= Failure Summary ==================================================================================================================
tests/test_example.py::test_failed: def test_failed():
        warnings.warn("This is a failing test warning", UserWarning)
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:14: AssertionError
================================================================================================================= Coverage Summary =================================================================================================================
Name                                                                                      Stmts   Miss  Cover
-------------------------------------------------------------------------------------------------------------
/usr/lib/python3/dist-packages/OpenSSL/SSL.py                                              1003    665    34%
/usr/lib/python3/dist-packages/OpenSSL/__init__.py                                            4      0   100%
/usr/lib/python3/dist-packages/OpenSSL/_util.py                                              41     18    56%
/usr/lib/python3/dist-packages/OpenSSL/crypto.py                                           1219    986    19%
/usr/lib/python3/dist-packages/OpenSSL/version.py                                            10      0   100%
/usr/lib/python3/dist-packages/_distutils_hack/__init__.py                                  100     95     5%
/usr/lib/python3/dist-packages/attr/_compat.py                                               69     60    13%
................................................
/usr/lib/python3/dist-packages/twisted/python/threadpool.py                                 119     80    33%
/usr/lib/python3/dist-packages/twisted/python/util.py                                       427    330    23%
/usr/lib/python3/dist-packages/twisted/python/win32.py                                       55     12    78%
/usr/lib/python3/dist-packages/zope/interface/_compat.py                                     65     38    42%
/usr/lib/python3/dist-packages/zope/interface/adapter.py                                    511    351    31%
/usr/lib/python3/dist-packages/zope/interface/declarations.py                               475    388    18%
/usr/lib/python3/dist-packages/zope/interface/interface.py                                  497    379    24%
/usr/lib/python3/dist-packages/zope/interface/ro.py                                         274    216    21%
conftest.py                                                                                  81     76     6%
tests/test_example.py                                                                        13      0   100%
-------------------------------------------------------------------------------------------------------------
TOTAL                                                                                     23153  14733    36%
=============================================================================================================== Module-wise Summary ================================================================================================================
tests/test_example.py: Passed: 2, Failed: 1, Skipped: 1
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_failed - assert (1 + 1) == 3
================================================================================================== 1 failed, 2 passed, 1 skipped, 3 warnings in 1.79s ===================================================================================================
root@Gavin:~/test/hook# 

```

### 详细解释和总结

1. **记录和报告警告详情**：
   - 在 `pytest_warning_recorded` 钩子中记录所有警告信息，包括触发阶段、节点ID、位置、消息、类别、文件和行号。
   - 使用 `pytest.config._test_summary['warnings']` 存储警告信息，以便在测试总结时进行输出。

2. **综合报告生成**：
   - 在 `pytest_terminal_summary` 钩子中，综合汇总测试结果、警告详情和覆盖率信息。
   - 使用 `terminalreporter.write_sep` 和 `terminalreporter.write_line` 在终端输出综合报告。

3. **覆盖率报告**：
   - 在 `pytest_sessionfinish` 钩子中停止覆盖率收集并保存数据。
   - 在 `pytest_terminal_summary` 钩子中检查是否收集到覆盖率数据，并在终端中输出覆盖率报告。

4. **保存总结为文件**：
   - 使用 Python 标准库中的 `json` 模块将总结信息保存为 JSON 文件 `test_summary_report.json`。
   - 使用标准文件操作方法将总结信息保存为文本文件 `test_summary_report.txt`。

# 高级功能示例

进一步扩展，我们可以添加更多高级功能，例如邮件通知和图形报告。

## 扩展示例：邮件通知

在测试会话结束时，自动发送测试结果和警告详情的电子邮件通知。

**扩展 `conftest.py` 以包括邮件通知功能**

```python
# conftest.py
import pytest
import coverage
from colorama import Fore, Style, init
import json
import smtplib
from email.mime.text import MIMEText
import matplotlib.pyplot as plt

init(autoreset=True)  # 自动重置颜色

cov = None
test_summary = {
    'total': 0,
    'passed': 0,
    'failed': 0,
    'skipped': 0,
    'by_module': {},
    'failures': [],
    'warnings': []
}

def send_email(summary):
    """发送测试结果和警告详情的电子邮件通知"""
    msg = MIMEText(json.dumps(summary, indent=4))
    msg['Subject'] = 'Test Summary Report'
    msg['From'] = 'sender@example.com'
    msg['To'] = 'recipient@example.com'

    with smtplib.SMTP('localhost') as server:  # 或者使用实际的 SMTP 服务器
        server.sendmail('sender@example.com', ['recipient@example.com'], msg.as_string())

def pytest_configure(config):
    global cov
    """在 pytest 配置时，启动覆盖率插件"""
    cov = coverage.Coverage()
    cov.start()

def pytest_sessionfinish(session, exitstatus):
    global cov
    """在测试会话结束时停止覆盖率收集并保存数据"""
    if cov:
        cov.stop()
        cov.save()

def pytest_warning_recorded(warning_message, nodeid, location):
    """记录警告详情"""
    global test_summary
    warning_info = {
        'nodeid': nodeid,
        'location': location,
        'message': str(warning_message.message),
        'category': warning_message.category.__name__,
        'filename': warning_message.filename,
        'lineno': warning_message.lineno
    }
    test_summary['warnings'].append(warning_info)

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    global cov, test_summary
    """在测试结束时汇总报告统计信息、警告详情和覆盖率信息，并保存报告和结果"""
    stats = terminalreporter.stats

    test_summary['total'] = sum(len(stats.get(stat, [])) for stat in ['passed', 'failed', 'skipped'])
    test_summary['passed'] = len(stats.get('passed', []))
    test_summary['failed'] = len(stats.get('failed', []))
    test_summary['skipped'] = len(stats.get('skipped', []))
    
    for stat in ['passed', 'failed', 'skipped']:
        for report in stats.get(stat, []):
            module = report.location[0]
            if module not in test_summary['by_module']:
                test_summary['by_module'][module] = {'passed': 0, 'failed': 0, 'skipped': 0}
            test_summary['by_module'][module][stat] += 1
            
            if stat == 'failed':
                test_summary['failures'].append({
                    'name': report.nodeid,
                    'reason': str(report.longrepr)
                })

    # 输出警告详情到终端
    terminalreporter.write_sep("=", f"{Fore.MAGENTA}Warnings Summary")
    for warning in test_summary['warnings']:
        terminalreporter.write_line(f"{warning['nodeid']} - {warning['location']}")
        terminalreporter.write_line(f"Message: {warning['message']}")
        terminalreporter.write_line(f"Category: {warning['category']}")
        terminalreporter.write_line(f"File: {warning['filename']}")
        terminalreporter.write_line(f"Line: {warning['lineno']}")
        terminalreporter.write_line("="*40)

    terminalreporter.write_sep("=", f"{Fore.CYAN}Test Summary")
    terminalreporter.write_line(f"{Fore.GREEN}Passed: {test_summary['passed']}")
    terminalreporter.write_line(f"{Fore.RED}Failed: {test_summary['failed']}")
    terminalreporter.write_line(f"{Fore.YELLOW}Skipped: {test_summary['skipped']}")
    
    terminalreporter.write_sep("=", f"{Fore.RED}Failure Summary")
    for report in stats.get('failed', []):
        terminalreporter.write_line(f"{Fore.RED}{report.nodeid}: {report.longrepr}")
    
    terminalreporter.write_sep("=", f"{Fore.BLUE}Coverage Summary")
    if cov and cov.get_data().measured_files():
        cov.report(file=terminalreporter._tw)
    else:
        terminalreporter.write_line(f"{Fore.RED}No coverage data to report.")

    terminalreporter.write_sep("=", f"{Fore.MAGENTA}Module-wise Summary")
    for module, counts in test_summary['by_module'].items():
        terminalreporter.write_line(f"{module}: Passed: {counts['passed']}, Failed: {counts['failed']}, Skipped: {counts['skipped']}")

    # 生成图表并保存为文件
    labels = ['Passed', 'Failed', 'Skipped']
    sizes = [test_summary['passed'], test_summary['failed'], test_summary['skipped']]
    colors = ['green', 'red', 'yellow']
    
    plt.figure(figsize=(10, 7))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Test Results Distribution')
    plt.savefig('test_results_distribution.png')
    plt.close()

    # 保存总结为 JSON 文件
    with open('test_summary_report.json', 'w') as f:
        json.dump(test_summary, f, indent=4)

    # 保存总结为文本文件
    with open('test_summary_report.txt', 'w') as f:
        f.write("Test Summary\n")
        f.write(f"Passed: {test_summary['passed']}\n")
        f.write(f"Failed: {test_summary['failed']}\n")
        f.write(f"Skipped: {test_summary['skipped']}\n")
        f.write("\nFailure Summary\n")
        for report in stats.get('failed', []):
            f.write(f"{report.nodeid}: {report.longrepr}\n")
        f.write("\nWarnings Summary\n")
        for warning in test_summary['warnings']:
            f.write(f"{warning['nodeid']} - {warning['location']}\n")
            f.write(f"Message: {warning['message']}\n")
            f.write(f"Category: {warning['category']}\n")
            f.write(f"File: {warning['filename']}\n")
            f.write(f"Line: {warning['lineno']}\n")
            f.write("="*40 + "\n")
        f.write("\nCoverage Summary\n")
        if cov and cov.get_data().measured_files():
            cov.report(file=f)
        else:
            f.write("No coverage data to report.\n")
        f.write("\nModule-wise Summary\n")
        for module, counts in test_summary['by_module'].items():
            f.write(f"{module}: Passed: {counts['passed']}, Failed: {counts['failed']}, Skipped: {counts['skipped']}\n")

    # 发送电子邮件
    send_email(test_summary)

# 示例测试文件 tests/test_warnings.py
import pytest
import warnings

@pytest.mark.unit
def test_unit_passed():
    assert 1 + 1 == 2

@pytest.mark.integration
def test_integration_passed():
    assert 2 + 2 == 4

def test_failed():
    warnings.warn("This is a failing test warning", UserWarning)
    assert 1 + 1 == 3

def test_skipped():
    pytest.skip("Skipping this test")
```


## 运行和验证

在项目根目录下运行以下命令来执行测试，并启用覆盖率报告：

```shell
pytest -s -v
```

控制台输出应包括综合报告，警告详情、测试结果、覆盖率报告，并生成 test_summary_report.json 和 test_summary_report.txt 文件，同时发送电子邮件通知。

控制台输出参考：

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
collected 4 items                                                                                                                                                                                                                                       

tests/test_example.py::test_unit_passed PASSED
tests/test_example.py::test_integration_passed PASSED
tests/test_example.py::test_failed FAILED
tests/test_example.py::test_skipped SKIPPED (Skipping this test)

======================================================================================================================= FAILURES ========================================================================================================================
______________________________________________________________________________________________________________________ test_failed ______________________________________________________________________________________________________________________

    def test_failed():
        warnings.warn("This is a failing test warning", UserWarning)
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:14: AssertionError
=================================================================================================================== warnings summary ====================================================================================================================
tests/test_example.py:4
  /root/test/hook/tests/test_example.py:4: PytestUnknownMarkWarning: Unknown pytest.mark.unit - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.unit

tests/test_example.py:8
  /root/test/hook/tests/test_example.py:8: PytestUnknownMarkWarning: Unknown pytest.mark.integration - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.integration

tests/test_example.py::test_failed
  /root/test/hook/tests/test_example.py:13: UserWarning: This is a failing test warning
    warnings.warn("This is a failing test warning", UserWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================================================================================================= Warnings Summary =================================================================================================================
 - None
Message: Unknown pytest.mark.unit - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
Category: PytestUnknownMarkWarning
File: /root/test/hook/tests/test_example.py
Line: 4
========================================
 - None
Message: Unknown pytest.mark.integration - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
Category: PytestUnknownMarkWarning
File: /root/test/hook/tests/test_example.py
Line: 8
========================================
tests/test_example.py::test_failed - None
Message: This is a failing test warning
Category: UserWarning
File: /root/test/hook/tests/test_example.py
Line: 13
========================================
=================================================================================================================== Test Summary ===================================================================================================================
Passed: 2
Failed: 1
Skipped: 1
================================================================================================================= Failure Summary ==================================================================================================================
tests/test_example.py::test_failed: def test_failed():
        warnings.warn("This is a failing test warning", UserWarning)
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:14: AssertionError
================================================================================================================= Coverage Summary =================================================================================================================
Name                                                                                      Stmts   Miss  Cover
-------------------------------------------------------------------------------------------------------------
/usr/lib/python3/dist-packages/OpenSSL/SSL.py                                              1003    665    34%
........................省略..............................
/usr/lib/python3/dist-packages/zope/interface/ro.py                                         274    216    21%
conftest.py                                                                                 101     96     5%
tests/test_example.py                                                                        13      0   100%
-------------------------------------------------------------------------------------------------------------
TOTAL                                                                                     23173  14753    36%
=============================================================================================================== Module-wise Summary ================================================================================================================
tests/test_example.py: Passed: 2, Failed: 1, Skipped: 1
........................省略..............................
root@Gavin:~/test/hook#
```


生成的文件：

JSON 文件` test_summary_report.json` 示例:

```json
root@Gavin:~/test/hook# cat test_summary_report.json 
{
    "total": 4,
    "passed": 2,
    "failed": 1,
    "skipped": 1,
    "by_module": {
        "tests/test_example.py": {
            "passed": 2,
            "failed": 1,
            "skipped": 1
        }
    },
    "failures": [
        {
            "name": "tests/test_example.py::test_failed",
            "reason": "def test_failed():\n        warnings.warn(\"This is a failing test warning\", UserWarning)\n>       assert 1 + 1 == 3\nE       assert (1 + 1) == 3\n\ntests/test_example.py:14: AssertionError"
        }
    ],
    "warnings": [
        {
            "nodeid": "",
            "location": null,
            "message": "Unknown pytest.mark.unit - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html",
            "category": "PytestUnknownMarkWarning",
            "filename": "/root/test/hook/tests/test_example.py",
            "lineno": 4
        },
        {
            "nodeid": "",
            "location": null,
            "message": "Unknown pytest.mark.integration - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html",
            "category": "PytestUnknownMarkWarning",
            "filename": "/root/test/hook/tests/test_example.py",
            "lineno": 8
        },
        {
            "nodeid": "tests/test_example.py::test_failed",
            "location": null,
            "message": "This is a failing test warning",
            "category": "UserWarning",
            "filename": "/root/test/hook/tests/test_example.py",
            "lineno": 13
        }
    ]
}root@Gavin:~/test/hook# 
```

文本文件 `test_summary_report.txt` 示例:

```plaintext
root@Gavin:~/test/hook# cat test_summary_report.txt 
Test Summary
Passed: 2
Failed: 1
Skipped: 1

Failure Summary
tests/test_example.py::test_failed: def test_failed():
        warnings.warn("This is a failing test warning", UserWarning)
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

tests/test_example.py:14: AssertionError

Warnings Summary
 - None
Message: Unknown pytest.mark.unit - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
Category: PytestUnknownMarkWarning
File: /root/test/hook/tests/test_example.py
Line: 4
========================================
 - None
Message: Unknown pytest.mark.integration - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
Category: PytestUnknownMarkWarning
File: /root/test/hook/tests/test_example.py
Line: 8
========================================
tests/test_example.py::test_failed - None
Message: This is a failing test warning
Category: UserWarning
File: /root/test/hook/tests/test_example.py
Line: 13
========================================

Coverage Summary
Name                                                                                      Stmts   Miss  Cover
-------------------------------------------------------------------------------------------------------------
/usr/lib/python3/dist-packages/OpenSSL/SSL.py                                              1003    665    34%
........................省略............................
/usr/lib/python3/dist-packages/zope/interface/ro.py                                         274    216    21%
conftest.py                                                                                 101     96     5%
tests/test_example.py                                                                        13      0   100%
-------------------------------------------------------------------------------------------------------------
TOTAL                                                                                     23173  14753    36%

Module-wise Summary
tests/test_example.py: Passed: 2, Failed: 1, Skipped: 1
root@Gavin:~/test/hook# 
```

生成的饼图示例:

<img class="shadow" src="/img/in-post/test_results_distribution2.png" width="600">

# 详细解释和总结

通过上述扩展示例，我们实现了以下功能：

* 记录和报告警告详情：
  使用 `pytest_warning_recorded` 钩子记录所有警告信息，并在测试总结时进行输出。
* 综合报告生成：
  在 `pytest_terminal_summary` 钩子中，综合汇总测试结果、警告详情和覆盖率信息，输出到终端并保存为文件。
* 覆盖率报告：
  使用 `coverage` 库进行覆盖率收集和报告，确保在测试总结中包含覆盖率信息。
* 图表生成：
  使用 `matplotlib` 生成测试结果分布的饼图，直观展示通过、失败和跳过的测试用例比例。
* 邮件通知：
  使用 `smtplib` 发送电子邮件通知，包含测试结果和警告详情，确保开发团队及时收到测试结果。


# 小结

通过这些扩展和优化，我们极大地增强了测试报告的丰富性、可读性和实用性。这些详细的测试报告和通知功能，可以帮助开发团队更好地理解测试结果，做出更好的质量决策。

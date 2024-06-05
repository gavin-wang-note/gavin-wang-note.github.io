---
title: pytest hook系列之pytest_internalerror
date: 2024-10-18 23:00:00
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
summary: pytest hook之pytest_internalerror
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_internalerror` 是 `pytest` 框架中的一个钩子函数。它用于捕获并处理 `pytest` 内部错误（`internal errors`）。

它在 `pytest` 内部发生错误时被触发。这些错误通常不是用户测试用例造成的，而是 pytest 自身的运行问题。捕获这些错误可以帮助开发者和测试人员快速定位和修正问题。

# 使用场景

1. **记录内部错误**：将内部错误记录到日志文件或外部存储中，以便后续分析。
2. **自定义错误处理**：提供自定义的错误处理逻辑，如发送错误报告邮件，或者通过其他方式通知相关人员。
3. **增强调试信息**：在测试报告中输出详细的内部错误信息，有助于调试和修复 pytest 自身的问题。

# 参数

```python
def pytest_internalerror(excrepr, excinfo):
    # excrepr: 编写的异常信息对象
    # excinfo: 异常捕获信息对象，包含异常的详细信息
    pass
```

- `excrepr`：编写的异常信息对象，包含格式化的异常信息，可以直接用于日志记录或输出。
- `excinfo`：捕获的异常信息对象，包含原始异常信息和详细的异常堆栈信息。

# 示例代码

## 案例一：记录内部错误到日志文件

目标：将内部错误记录到日志文件中，以便后续分析和处理。

步骤：
1. 使用 `pytest_internalerror` 钩子捕获内部错误。
2. 将捕获的错误信息记录到日志文件中。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='internal_errors.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def pytest_internalerror(excrepr, excinfo):
    """记录内部错误到日志文件"""
    logging.error(f"Internal Error: {excrepr}\n")

# 为了测试内部错误，我们故意在某个钩子中引发一个错误
def pytest_runtest_protocol(item, nextitem):
    if item.name == "test_trigger_internal_error":
        raise RuntimeError("This is a forced internal error for testing purposes.")
    return

# tests/test_example.py
def test_sample():
    assert 1 + 1 == 2

# 这个测试用例将强制引发一个内部错误
def test_trigger_internal_error():
    assert 1 + 1 == 2
```

**注释**：
- 使用 `logging` 模块配置日志记录，将日志输出到 `internal_errors.log` 文件中。
- 在 `pytest_internalerror` 钩子中，捕获异常并记录到日志文件中。

**运行效果**:

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

tests/test_example.py::test_sample PASSED
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
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 167, in _multicall
INTERNALERROR>     teardown.throw(outcome._exception)
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/warnings.py", line 109, in pytest_runtest_protocol
INTERNALERROR>     return (yield)
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 167, in _multicall
INTERNALERROR>     teardown.throw(outcome._exception)
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/assertion/__init__.py", line 175, in pytest_runtest_protocol
INTERNALERROR>     return (yield)
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 167, in _multicall
INTERNALERROR>     teardown.throw(outcome._exception)
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/unittest.py", line 411, in pytest_runtest_protocol
INTERNALERROR>     res = yield
INTERNALERROR>           ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 167, in _multicall
INTERNALERROR>     teardown.throw(outcome._exception)
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/faulthandler.py", line 85, in pytest_runtest_protocol
INTERNALERROR>     return (yield)
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
INTERNALERROR>     res = hook_impl.function(*args)
INTERNALERROR>           ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/root/test/hook/conftest.py", line 15, in pytest_runtest_protocol
INTERNALERROR>     raise RuntimeError("This is a forced internal error for testing purposes.")
INTERNALERROR> RuntimeError: This is a forced internal error for testing purposes.

=================================================================================================================== 1 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook# ll
total 28
drwxr-xr-x 5 root root 4096 Jun  5 09:44 ./
drwxr-xr-x 6 root root 4096 Jun  4 18:49 ../
-rw-r--r-- 1 root root  607 Jun  5 09:43 conftest.py
-rw-r--r-- 1 root root 4024 Jun  5 09:45 internal_errors.log
drwxr-xr-x 2 root root 4096 Jun  5 09:43 __pycache__/
drwxr-xr-x 3 root root 4096 Jun  4 22:42 .pytest_cache/
drwxr-xr-x 3 root root 4096 Jun  5 09:45 tests/
root@Gavin:~/test/hook# cat internal_errors.log 
2024-06-05 09:45:03,472 - ERROR - Internal Error: Traceback (most recent call last):
  File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 273, in wrap_session
    session.exitstatus = doit(config, session) or 0
                         ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 327, in _main
    config.hook.pytest_runtestloop(session=session)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_hooks.py", line 513, in __call__
    return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_manager.py", line 120, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 139, in _multicall
    raise exception.with_traceback(exception.__traceback__)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 122, in _multicall
    teardown.throw(exception)  # type: ignore[union-attr]
    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/_pytest/logging.py", line 796, in pytest_runtestloop
    return (yield)  # Run all the tests.
            ^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
    res = hook_impl.function(*args)
          ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 352, in pytest_runtestloop
    item.config.hook.pytest_runtest_protocol(item=item, nextitem=nextitem)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_hooks.py", line 513, in __call__
    return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_manager.py", line 120, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 182, in _multicall
    return outcome.get_result()
           ^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_result.py", line 100, in get_result
    raise exc.with_traceback(exc.__traceback__)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 167, in _multicall
    teardown.throw(outcome._exception)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/warnings.py", line 109, in pytest_runtest_protocol
    return (yield)
            ^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 167, in _multicall
    teardown.throw(outcome._exception)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/assertion/__init__.py", line 175, in pytest_runtest_protocol
    return (yield)
            ^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 167, in _multicall
    teardown.throw(outcome._exception)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/unittest.py", line 411, in pytest_runtest_protocol
    res = yield
          ^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 167, in _multicall
    teardown.throw(outcome._exception)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/faulthandler.py", line 85, in pytest_runtest_protocol
    return (yield)
            ^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
    res = hook_impl.function(*args)
          ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/test/hook/conftest.py", line 15, in pytest_runtest_protocol
    raise RuntimeError("This is a forced internal error for testing purposes.")
RuntimeError: This is a forced internal error for testing purposes.

root@Gavin:~/test/hook#
```

## 案例二：自定义内部错误处理

目标：提供自定义的内部错误处理逻辑，如发送错误报告邮件。

步骤：
1. 使用 `pytest_internalerror` 钩子捕获内部错误。
2. 在钩子函数中实现自定义的错误处理逻辑，比如通过 SMTP 发送错误报告邮件。

示例代码：

```python
# conftest.py
import pytest
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body):
    """发送邮件通知"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'sender@example.com'
    msg['To'] = 'recipient@example.com'

    with smtplib.SMTP('localhost', 1025) as server:  # 连接到本地伪SMTP服务器
        server.sendmail('sender@example.com', ['recipient@example.com'], msg.as_string())

def pytest_internalerror(excrepr, excinfo):
    """自定义内部错误处理，发送错误报告邮件"""
    subject = "Pytest Internal Error"
    body = f"Internal Error: {excrepr}\nException info: {excinfo}"
    send_email(subject, body)

# 故意在 pytest 集收集(test collection)阶段引发一个内部错误
def pytest_collection_modifyitems(items):
    raise RuntimeError("This is a forced internal error for testing purposes.")
```

**注释**：
- 定义 `send_email` 函数，用于通过 SMTP 发送电子邮件。
- 在 `pytest_internalerror` 钩子中，捕获异常并发送错误报告邮件。


**运行效果**:

确保有一个本地`SMTP`服务器，使用`Python`的`smtpd`模块启动一个伪`SMTP`服务器来接收测试邮件。

```shell
python3 -m smtpd -c DebuggingServer -n localhost:1025
```

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
INTERNALERROR> Traceback (most recent call last):
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 273, in wrap_session
INTERNALERROR>     session.exitstatus = doit(config, session) or 0
INTERNALERROR>                          ^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 326, in _main
INTERNALERROR>     config.hook.pytest_collection(session=session)
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
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/logging.py", line 783, in pytest_collection
INTERNALERROR>     return (yield)
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 122, in _multicall
INTERNALERROR>     teardown.throw(exception)  # type: ignore[union-attr]
INTERNALERROR>     ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/warnings.py", line 118, in pytest_collection
INTERNALERROR>     return (yield)
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 122, in _multicall
INTERNALERROR>     teardown.throw(exception)  # type: ignore[union-attr]
INTERNALERROR>     ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/config/__init__.py", line 1367, in pytest_collection
INTERNALERROR>     return (yield)
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
INTERNALERROR>     res = hook_impl.function(*args)
INTERNALERROR>           ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 337, in pytest_collection
INTERNALERROR>     session.perform_collect()
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 803, in perform_collect
INTERNALERROR>     hook.pytest_collection_modifyitems(
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
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/cacheprovider.py", line 414, in pytest_collection_modifyitems
INTERNALERROR>     res = yield
INTERNALERROR>           ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 122, in _multicall
INTERNALERROR>     teardown.throw(exception)  # type: ignore[union-attr]
INTERNALERROR>     ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/cacheprovider.py", line 342, in pytest_collection_modifyitems
INTERNALERROR>     res = yield
INTERNALERROR>           ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
INTERNALERROR>     res = hook_impl.function(*args)
INTERNALERROR>           ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/root/test/hook/conftest.py", line 24, in pytest_collection_modifyitems
INTERNALERROR>     raise RuntimeError("This is a forced internal error for testing purposes.")
INTERNALERROR> RuntimeError: This is a forced internal error for testing purposes.

================================================================================================================= no tests ran in 0.25s =================================================================================================================
root@Gavin:~/test/hook#
```

## 案例三：在测试报告中输出详细内部错误信息

目标：在测试报告中输出详细的内部错误信息，增强调试信息，帮助定位问题。

步骤：
1. 使用 `pytest_internalerror` 钩子捕捉内部错误。
2. 将捕获的错误信息格式化后输出到测试报告中。

示例代码：

```python
# conftest.py
import pytest
import sys

def pytest_internalerror(excrepr, excinfo):
    """在测试报告中输出详细的内部错误信息"""
    print("\n" + "="*40)
    print("Pytest encountered an internal error!")
    print("="*40)
    print(f"Error Description: {excrepr}", file=sys.stderr)
    print(f"Exception Info: {excinfo}", file=sys.stderr)
    print("="*40)

# 故意在 pytest 集收集(test collection)阶段引发一个内部错误
def pytest_collection_modifyitems(items):
    raise RuntimeError("This is a forced internal error for testing purposes.")
```

**注释**：
- 使用 `print` 函数将详细的错误信息输出到控制台和测试报告中。
- 格式化输出，确保错误信息清晰易读。

**输出效果**:

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
INTERNALERROR> Traceback (most recent call last):
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 273, in wrap_session
INTERNALERROR>     session.exitstatus = doit(config, session) or 0
INTERNALERROR>                          ^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 326, in _main
INTERNALERROR>     config.hook.pytest_collection(session=session)
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
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/logging.py", line 783, in pytest_collection
INTERNALERROR>     return (yield)
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 122, in _multicall
INTERNALERROR>     teardown.throw(exception)  # type: ignore[union-attr]
INTERNALERROR>     ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/warnings.py", line 118, in pytest_collection
INTERNALERROR>     return (yield)
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 122, in _multicall
INTERNALERROR>     teardown.throw(exception)  # type: ignore[union-attr]
INTERNALERROR>     ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/config/__init__.py", line 1367, in pytest_collection
INTERNALERROR>     return (yield)
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
INTERNALERROR>     res = hook_impl.function(*args)
INTERNALERROR>           ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 337, in pytest_collection
INTERNALERROR>     session.perform_collect()
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 803, in perform_collect
INTERNALERROR>     hook.pytest_collection_modifyitems(
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
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/cacheprovider.py", line 414, in pytest_collection_modifyitems
INTERNALERROR>     res = yield
INTERNALERROR>           ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 122, in _multicall
INTERNALERROR>     teardown.throw(exception)  # type: ignore[union-attr]
INTERNALERROR>     ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/_pytest/cacheprovider.py", line 342, in pytest_collection_modifyitems
INTERNALERROR>     res = yield
INTERNALERROR>           ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
INTERNALERROR>     res = hook_impl.function(*args)
INTERNALERROR>           ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/root/test/hook/conftest.py", line 16, in pytest_collection_modifyitems
INTERNALERROR>     raise RuntimeError("This is a forced internal error for testing purposes.")
INTERNALERROR> RuntimeError: This is a forced internal error for testing purposes.

========================================
Pytest encountered an internal error!
========================================
Error Description: Traceback (most recent call last):
  File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 273, in wrap_session
    session.exitstatus = doit(config, session) or 0
                         ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 326, in _main
    config.hook.pytest_collection(session=session)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_hooks.py", line 513, in __call__
    return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_manager.py", line 120, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 139, in _multicall
    raise exception.with_traceback(exception.__traceback__)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 122, in _multicall
    teardown.throw(exception)  # type: ignore[union-attr]
    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/_pytest/logging.py", line 783, in pytest_collection
    return (yield)
            ^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 122, in _multicall
    teardown.throw(exception)  # type: ignore[union-attr]
    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/_pytest/warnings.py", line 118, in pytest_collection
    return (yield)
            ^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 122, in _multicall
    teardown.throw(exception)  # type: ignore[union-attr]
    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/_pytest/config/__init__.py", line 1367, in pytest_collection
    return (yield)
            ^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
    res = hook_impl.function(*args)
          ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 337, in pytest_collection
    session.perform_collect()
  File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 803, in perform_collect
    hook.pytest_collection_modifyitems(
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_hooks.py", line 513, in __call__
    return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_manager.py", line 120, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 139, in _multicall
    raise exception.with_traceback(exception.__traceback__)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 122, in _multicall
    teardown.throw(exception)  # type: ignore[union-attr]
    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/_pytest/cacheprovider.py", line 414, in pytest_collection_modifyitems
    res = yield
          ^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 122, in _multicall
    teardown.throw(exception)  # type: ignore[union-attr]
    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/_pytest/cacheprovider.py", line 342, in pytest_collection_modifyitems
    res = yield
          ^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
    res = hook_impl.function(*args)
          ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/test/hook/conftest.py", line 16, in pytest_collection_modifyitems
    raise RuntimeError("This is a forced internal error for testing purposes.")
RuntimeError: This is a forced internal error for testing purposes.
Exception Info: <ExceptionInfo RuntimeError('This is a forced internal error for testing purposes.') tblen=23>
========================================

================================================================================================================= no tests ran in 0.02s =================================================================================================================
root@Gavin:~/test/hook#
```

### 详细解释和总结

1. **记录内部错误到日志文件**：
   - 使用 `pytest_internalerror` 钩子捕获内部错误，并使用 `logging` 模块记录错误信息到日志文件中。
   - 日志文件记录了详细的错误信息，方便后续分析和处理。

2. **自定义内部错误处理**：
   - 在 `pytest_internalerror` 钩子中，捕获内部错误，并通过自定义函数 `send_email` 发送错误报告邮件。
   - 邮件通知确保相关人员及时了解测试过程中的内部错误。

3. **在测试报告中输出详细内部错误信息**：
   - 捕获内部错误后，将详细错误信息格式化输出到测试报告中。
   - 增强的错误信息对调试和问题定位非常有帮助。

# 小结

通过 `pytest_internalerror` 钩子，我们可以在`pytest`内部发生错误时捕获并处理这些错误，实现自定义的错误记录、处理和报告机制。希望这些详细的案例和解释对你有所帮助。

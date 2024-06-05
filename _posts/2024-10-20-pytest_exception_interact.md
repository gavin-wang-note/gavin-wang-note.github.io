---
title: pytest hook系列之pytest_exception_interact
date: 2024-10-20 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-21.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_exception_interact
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_exception_interact` 是 `pytest` 框架中的一个钩子函数，该钩子函数在测试执行期间抛出异常时被触发。通过这个钩子函数，我们可以在测试过程中的异常互动时添加自定义逻辑，例如向用户提供调试信息，记录异常详情，交互式调试，发送错误报告等。

# 使用场景

1. **记录异常详情**：在测试过程中发生异常时记录异常详情，以便后续分析和调试。
2. **交互式调试**：在测试过程中发生异常时，自动进入交互式调试模式，以便及时查找和修复问题。
3. **发送错误报告**：在测试过程中发生异常时发送错误报告邮件或消息，及时告知相关人员。

# 参数

```python
def pytest_exception_interact(node, call, report):
    # node: 测试节点对象，表示发生异常的测试用例或测试函数
    # call: 测试调用对象，包含异常类型、值和详细堆栈信息
    # report: 测试报告对象，表示测试的执行结果
    pass
```

- `node`：测试节点对象，表示发生异常的测试用例或测试函数。
- `call`：测试调用对象，包含异常类型、值和详细堆栈信息。
- `report`：测试报告对象，表示测试的执行结果。

# 示例代码

## 案例一：异常详情记录

目标：在测试过程中发生异常时记录异常详情，以便后续分析和调试。

步骤：
1. 使用 `pytest_exception_interact` 钩子捕获异常。
2. 将捕获的异常详情记录到日志文件中。

示例代码：

```python
# conftest.py
# conftest.py
import pytest
import logging
import traceback

# 配置日志记录
logging.basicConfig(filename='exceptions.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def pytest_exception_interact(node, call, report):
    """记录异常详情到日志文件"""
    if call.excinfo:
        excinfo = call.excinfo
        formatted_exception = "".join(traceback.format_exception(excinfo.type, excinfo.value, excinfo.tb))
        logging.error(
            f"Exception occurred in {node.nodeid}:\n"
            f"{excinfo.value}\n"
            f"{formatted_exception}"
        )

#测试用例示例 tests/test_example.py
def test_addition():
    assert 1 + 1 == 2

def test_division_by_zero():
    assert 1 / 0  # 这将引发一个ZeroDivisionError

def test_subtraction():
    assert 2 - 1 == 1
```

**注释**：
- 使用 `logging` 模块配置日志记录，将日志输出到 `exceptions.log` 文件中。
- 在 `pytest_exception_interact` 钩子中，检查 `call.excinfo`，并记录异常详情到日志文件中。


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
collected 3 items                                                                                                                                                                                                                                       

tests/test_example.py::test_addition PASSED
tests/test_example.py::test_division_by_zero FAILED
tests/test_example.py::test_subtraction PASSED

======================================================================================================================= FAILURES ========================================================================================================================
_________________________________________________________________________________________________________________ test_division_by_zero _________________________________________________________________________________________________________________

    def test_division_by_zero():
>       assert 1 / 0  # 这将引发一个ZeroDivisionError
E       ZeroDivisionError: division by zero

tests/test_example.py:7: ZeroDivisionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_division_by_zero - ZeroDivisionError: division by zero
============================================================================================================== 1 failed, 2 passed in 0.11s ==============================================================================================================
root@Gavin:~/test/hook# ll
total 36
drwxr-xr-x 5 root root 4096 Jun  5 11:18 ./
drwxr-xr-x 6 root root 4096 Jun  4 18:49 ../
-rw-r--r-- 1 root root  496 Jun  5 11:12 clear_pyc.py
-rw-r--r-- 1 root root  622 Jun  5 11:17 conftest.py
-rw-r--r-- 1 root root 4904 Jun  5 11:18 exceptions.log
drwxr-xr-x 2 root root 4096 Jun  5 11:18 __pycache__/
drwxr-xr-x 3 root root 4096 Jun  5 11:18 .pytest_cache/
drwxr-xr-x 3 root root 4096 Jun  5 11:18 tests/
root@Gavin:~/test/hook# cat exceptions.log 
2024-06-05 11:18:02,659 - ERROR - Exception occurred in tests/test_example.py::test_division_by_zero:
division by zero
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/dist-packages/_pytest/runner.py", line 342, in from_call
    result: Optional[TResult] = func()
                                ^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/_pytest/runner.py", line 263, in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
            ^^^^^^^^^^^^^^^^^^^^^^^^
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
  File "/usr/local/lib/python3.11/dist-packages/_pytest/threadexception.py", line 87, in pytest_runtest_call
    yield from thread_exception_runtest_hook()
  File "/usr/local/lib/python3.11/dist-packages/_pytest/threadexception.py", line 63, in thread_exception_runtest_hook
    yield
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 167, in _multicall
    teardown.throw(outcome._exception)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/unraisableexception.py", line 90, in pytest_runtest_call
    yield from unraisable_exception_runtest_hook()
  File "/usr/local/lib/python3.11/dist-packages/_pytest/unraisableexception.py", line 65, in unraisable_exception_runtest_hook
    yield
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 167, in _multicall
    teardown.throw(outcome._exception)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/logging.py", line 839, in pytest_runtest_call
    yield from self._runtest_for(item, "call")
  File "/usr/local/lib/python3.11/dist-packages/_pytest/logging.py", line 822, in _runtest_for
    yield
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 167, in _multicall
    teardown.throw(outcome._exception)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/capture.py", line 882, in pytest_runtest_call
    return (yield)
            ^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 167, in _multicall
    teardown.throw(outcome._exception)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/skipping.py", line 256, in pytest_runtest_call
    return (yield)
            ^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
    res = hook_impl.function(*args)
          ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/_pytest/runner.py", line 178, in pytest_runtest_call
    raise e
  File "/usr/local/lib/python3.11/dist-packages/_pytest/runner.py", line 170, in pytest_runtest_call
    item.runtest()
  File "/usr/local/lib/python3.11/dist-packages/_pytest/python.py", line 1831, in runtest
    self.ihook.pytest_pyfunc_call(pyfuncitem=self)
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
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
    res = hook_impl.function(*args)
          ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/dist-packages/pytest_tornasync/plugin.py", line 45, in pytest_pyfunc_call
    pyfuncitem.obj(**testargs)
  File "/root/test/hook/tests/test_example.py", line 7, in test_division_by_zero
    assert 1 / 0  # 这将引发一个ZeroDivisionError
    ^^^^^^^^^^^^
ZeroDivisionError: division by zero

root@Gavin:~/test/hook#
```

## 案例二：交互式调试

目标：在测试过程中发生异常时，自动进入交互式调试模式，以便及时查找和修复问题。

步骤：
1. 使用 `pytest_exception_interact` 钩子捕获异常。
2. 在钩子函数中调用调试工具（如 `pdb`）进入交互式调试模式。

示例代码：

```python
# conftest.py
import pytest
import pdb

def pytest_exception_interact(node, call, report):
    """在异常发生时进入交互式调试模式"""
    if call.excinfo:
        excinfo = call.excinfo
        print(f"Exception occurred in {node.nodeid}:\n{excinfo.value}\n")
        pdb.post_mortem(excinfo.tb)

#测试用例示例 tests/test_example.py
def test_addition():
    assert 1 + 1 == 2

def test_division_by_zero():
    assert 1 / 0  # 这将引发一个ZeroDivisionError

def test_subtraction():
    assert 2 - 1 == 1
```

**注释**：
- 使用 `print` 函数打印异常详情。
- 调用 `pdb.post_mortem` 进入交互式调试模式。


**运行效果**:

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
collected 3 items                                                                                                                                                                                                                                       

tests/test_example.py::test_addition PASSED
tests/test_example.py::test_division_by_zero FAILEDException occurred in tests/test_example.py::test_division_by_zero:
division by zero

> /root/test/hook/tests/test_example.py(7)test_division_by_zero()
-> assert 1 / 0  # 这将引发一个ZeroDivisionError
(Pdb) next

tests/test_example.py::test_subtraction PASSED

======================================================================================================================= FAILURES ========================================================================================================================
_________________________________________________________________________________________________________________ test_division_by_zero _________________________________________________________________________________________________________________

    def test_division_by_zero():
>       assert 1 / 0  # 这将引发一个ZeroDivisionError
E       ZeroDivisionError: division by zero

tests/test_example.py:7: ZeroDivisionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_division_by_zero - ZeroDivisionError: division by zero
============================================================================================================== 1 failed, 2 passed in 3.91s ==============================================================================================================
root@Gavin:~/test/hook# 
```

## 案例三：发送错误报告

目标：在测试过程中发生异常时发送错误报告邮件或消息，及时告知相关人员。

步骤：
1. 使用 `pytest_exception_interact` 钩子捕获异常。
2. 在钩子函数中实现发送错误报告邮件或消息的逻辑。

示例代码：

```python
# conftest.py
import pytest
import smtplib
from email.mime.text import MIMEText
import traceback

def send_email(subject, body):
    """发送邮件通知"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'sender@example.com'
    msg['To'] = 'recipient@example.com'

    with smtplib.SMTP('localhost', 1025) as server:  # 或者使用实际的 SMTP 服务器
        server.sendmail('sender@example.com', ['recipient@example.com'], msg.as_string())

def pytest_exception_interact(node, call, report):
    """在异常发生时发送错误报告"""
    if call.excinfo:
        excinfo = call.excinfo
        subject = f"Exception in {node.nodeid}"
        formatted_exception = ''.join(traceback.format_exception(excinfo.type, excinfo.value, excinfo.tb))
        body = (
            f"Exception Type: {excinfo.type}\n"
            f"Exception Value: {excinfo.value}\n"
            f"Traceback:\n{formatted_exception}"
        )
        send_email(subject, body)

#测试用例示例 tests/test_example.py
def test_addition():
    assert 1 + 1 == 2

def test_division_by_zero():
    assert 1 / 0  # 这将引发一个ZeroDivisionError

def test_subtraction():
    assert 2 - 1 == 1
```

**注释**：
- 定义 `send_email` 函数，用于通过 SMTP 发送电子邮件。
- 在 `pytest_exception_interact` 钩子中，捕获异常并发送错误报告。

**运行效果**:

为了接收错误报告邮件，启动一个本地伪 SMTP 服务器：

```shell
python3 -m smtpd -c DebuggingServer -n localhost:1025
```

然后执行`pytest`命令运行用例：

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
collected 3 items                                                                                                                                                                                                                                       

tests/test_example.py::test_addition PASSED
tests/test_example.py::test_division_by_zero FAILED
tests/test_example.py::test_subtraction PASSED

======================================================================================================================= FAILURES ========================================================================================================================
_________________________________________________________________________________________________________________ test_division_by_zero _________________________________________________________________________________________________________________

    def test_division_by_zero():
>       assert 1 / 0  # 这将引发一个ZeroDivisionError
E       ZeroDivisionError: division by zero

tests/test_example.py:7: ZeroDivisionError
================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_division_by_zero - ZeroDivisionError: division by zero
============================================================================================================== 1 failed, 2 passed in 0.35s ==============================================================================================================
root@Gavin:~/test/hook# 
```

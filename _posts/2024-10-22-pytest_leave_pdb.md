---
title: pytest hook系列之pytest_leave_pdb
date: 2024-10-22 23:00:00
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
summary: pytest hook之pytest_leave_pdb
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述


`pytest_leave_pdb` 是 `pytest` 框架中的一个钩子函数，当你从基于 `pdb` 的调试模式退出时（例如，通过在调试器中执行 `continue` 命令），该钩子函数就会被触发。通过这个钩子函数，你可以在退出调试模式后执行一些自定义操作，例如清理调试环境、记录调试事件或通知团队成员等。

# 参数

```python
def pytest_leave_pdb(config: "Config", pdb: "pdb.Pdb") -> None:
    """Called when leaving pdb (e.g. with continue after pdb.set_trace()).

    Can be used by plugins to take special action just after the python
    debugger leaves interactive mode.

    :param config: The pytest config object.
    :param pdb: The Pdb instance.
    """
```

- `config`：`pytest` 配置对象，包含当前 `pytest` 会话的配置信息。
- `pdb`：`Pdb` 类实例，用于控制调试器的行为。

# 使用场景

1. **清理调试环境**：在退出调试模式后，清理调试时设置的环境变量。
2. **记录调试事件**：在退出调试模式时记录调试事件，以便后期分析调试的频率和原因。
3. **通知团队成员**：当调试完成后，通过邮件或消息通知团队成员。

# 示例代码

## 案例一：清理调试环境

目标：在退出调试模式后，清理调试环境变量。

步骤：
1. 使用 `pytest_leave_pdb` 钩子函数。
2. 在钩子函数中清理调试环境变量。

**示例代码**：

```python
# conftest.py
import pytest

def pytest_leave_pdb(config, pdb):
    """清理调试环境变量"""
    print("Leaving PDB: cleaning up debug environment variables...")
    del pdb.prompt  # 假设我们在调试时设置了一个自定义提示符

# tests/test_example.py
def test_addition():
    assert 1 + 1 == 2

def test_division_by_zero():
    assert 1 / 0  # 这将引发一个ZeroDivisionError，触发调试模式

def test_subtraction():
    assert 2 - 1 == 1
```

**解释**：
- 使用 `print` 语句打印退出调试模式的信息。
- 删除调试时设置的环境变量（如自定义提示符）。

**运行效果**:

```shell
root@Gavin:~/test/hook# pytest -s -v --pdb
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
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> traceback >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def test_division_by_zero():
>       assert 1 / 0  # 这将引发一个ZeroDivisionError，触发调试模式
E       ZeroDivisionError: division by zero

tests/test_example.py:16: ZeroDivisionError
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> entering PDB >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PDB post_mortem >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
> /root/test/hook/tests/test_example.py(16)test_division_by_zero()
-> assert 1 / 0  # 这将引发一个ZeroDivisionError，触发调试模式
(Pdb) continue

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PDB continue >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Leaving PDB: cleaning up debug environment variables...

tests/test_example.py::test_subtraction PASSED

================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_division_by_zero - ZeroDivisionError: division by zero
============================================================================================================== 1 failed, 2 passed in 4.69s ==============================================================================================================
root@Gavin:~/test/hook# 
```

## 案例二：记录调试事件

目标：在退出调试模式时记录调试事件，包括调试结束时间和触发调试的测试用例信息。

步骤：
1. 使用 `pytest_leave_pdb` 钩子函数。
2. 在钩子函数中记录调试事件到日志文件中。

**示例代码**：

```python
# conftest.py
import pytest
import logging
from datetime import datetime

# 配置日志记录
logging.basicConfig(filename='debug_events.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def pytest_leave_pdb(config, pdb):
    """记录调试事件到日志文件"""
    test_nodeid = pdb.curframe.f_globals.get('__name__', 'Unknown')
    logging.info(f"Leaving PDB for test: {test_nodeid} at {datetime.now()}")
    print("Leaving PDB and logging debug event...")
```

**解释**：
- 使用 `logging` 模块配置日志记录，将日志输出到 `debug_events.log` 文件中。
- 在 `pytest_leave_pdb` 钩子函数中，获取当前测试节点信息并记录调试事件。

**运行效果**:

```shell
root@Gavin:~/test/hook# pytest -s -v --pdb
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
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> traceback >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def test_division_by_zero():
>       assert 1 / 0  # 这将引发一个ZeroDivisionError，触发调试模式
E       ZeroDivisionError: division by zero

tests/test_example.py:16: ZeroDivisionError
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> entering PDB >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PDB post_mortem >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
> /root/test/hook/tests/test_example.py(16)test_division_by_zero()
-> assert 1 / 0  # 这将引发一个ZeroDivisionError，触发调试模式
(Pdb) continue

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PDB continue >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Leaving PDB and logging debug event...

tests/test_example.py::test_subtraction PASSED

================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_division_by_zero - ZeroDivisionError: division by zero
============================================================================================================== 1 failed, 2 passed in 4.80s ==============================================================================================================
root@Gavin:~/test/hook# ll
total 32
drwxr-xr-x 5 root root 4096 Oct  22 17:55 ./
drwxr-xr-x 6 root root 4096 Oct  21 18:49 ../
-rw-r--r-- 1 root root  496 Oct  22 11:12 clear_pyc.py
-rw-r--r-- 1 root root  500 Oct  22 17:54 conftest.py
-rw-r--r-- 1 root root   98 Oct  22 17:55 debug_events.log
drwxr-xr-x 2 root root 4096 Oct  22 17:55 __pycache__/
drwxr-xr-x 3 root root 4096 Oct  22 17:55 .pytest_cache/
drwxr-xr-x 3 root root 4096 Oct  22 17:55 tests/
root@Gavin:~/test/hook# cat debug_events.log 
2024-10-22 17:55:43,394 - INFO - Leaving PDB for test: test_example at 2024-10-22 17:55:43.394565
root@Gavin:~/test/hook# 
```

## 案例三：通知团队成员

目标：当调试完成后，通过邮件或消息通知团队成员。

步骤：
1. 使用 `pytest_leave_pdb` 钩子函数。
2. 在钩子函数中发送通知邮件或消息。

**示例代码**：

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

    with smtplib.SMTP('localhost', 1025) as server:  # 本地调试用的 SMTP 服务器
        server.sendmail('sender@example.com', ['recipient@example.com'], msg.as_string())

def pytest_leave_pdb(config, pdb):
    """调试完成后发送通知邮件"""
    test_nodeid = pdb.curframe.f_globals.get('__name__', 'Unknown')
    subject = f"Debugging finished for test: {test_nodeid}"
    body = f"Finished debugging test: {test_nodeid}"
    send_email(subject, body)
    print("Leaving PDB and sending notification email...")
```

**解释**：
- 定义 `send_email` 函数，用于通过 SMTP 发送电子邮件。
- 在 `pytest_leave_pdb` 钩子函数中，发送包含相关调试信息的通知邮件。


**运行效果**:

先确保SMTP服务运行：

```shell
python3 -m smtpd -c DebuggingServer -n localhost:1025
```

然后执行测试用例，运行效果参考如下：

```shell
root@Gavin:~/test/hook# pytest -s -v --pdb
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
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> traceback >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def test_division_by_zero():
>       assert 1 / 0  # 这将引发一个ZeroDivisionError，触发调试模式
E       ZeroDivisionError: division by zero

tests/test_example.py:16: ZeroDivisionError
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> entering PDB >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PDB post_mortem >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
> /root/test/hook/tests/test_example.py(16)test_division_by_zero()
-> assert 1 / 0  # 这将引发一个ZeroDivisionError，触发调试模式
(Pdb) continue

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PDB continue >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Leaving PDB and sending notification email...

tests/test_example.py::test_subtraction PASSED

================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_division_by_zero - ZeroDivisionError: division by zero
============================================================================================================== 1 failed, 2 passed in 2.82s ==============================================================================================================
root@Gavin:~/test/hook#
```

此时在`SMTP`端收到的消息参考如下：

```shell
root@Gavin:~# python3 -m smtpd -c DebuggingServer -n localhost:1025
/usr/lib/python3.11/smtpd.py:96: DeprecationWarning: The asyncore module is deprecated and will be removed in Python 3.12. The recommended replacement is asyncio
  import asyncore
/usr/lib/python3.11/smtpd.py:97: DeprecationWarning: The asynchat module is deprecated and will be removed in Python 3.12. The recommended replacement is asyncio
  import asynchat
---------- MESSAGE FOLLOWS ----------
b'Content-Type: text/plain; charset="us-ascii"'
b'MIME-Version: 1.0'
b'Content-Transfer-Encoding: 7bit'
b'Subject: Debugging finished for test: test_example'
b'From: sender@example.com'
b'To: recipient@example.com'
b'X-Peer: ::1'
b''
b'Finished debugging test: test_example'
------------ END MESSAGE ------------
```

# 小结

至此，`pytest`的52个`hook`全部介绍完毕。



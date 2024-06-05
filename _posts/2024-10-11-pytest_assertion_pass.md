---
title: pytest hook系列之pytest_assertion_pass
date: 2024-10-11 23:00:00
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
summary: pytest hook之pytest_assertion_pass
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_assertion_pass` 是 `pytest` 框架中的一个钩子函数，它在一个断言成功时被触发(在测试中每一个断言成功时被调用)。通过这个钩子函数，我们可以在断言通过时执行一些自定义操作，如日志记录、统计信息的收集等，从而增强测试的可视化和调试能力。

# 使用场景

1. **日志记录**：记录每个断言成功的信息，以便对测试过程进行详细记录和调试。
2. **统计信息收集**：收集断言通过的统计信息，例如通过断言的总数、每个测试用例中通过断言的数量等。
3. **监控和警报**：在特定条件下监控断言的成功，并根据需要触发警报或通知。
4. **调试**：在调试复杂测试用例时获得更多成功断言的信息，帮助定位问题并验证预期情况。

# 参数

```python
def pytest_assertion_pass(item, lineno, orig, expl):
    # item: 测试用例对象，包含当前执行的测试用例的相关信息
    # lineno: 断言所在的行号
    # orig: 原始断言代码的字符串表示
    # expl: 断言解释的字符串表示（如果有）
    pass
```

- `item`：测试用例对象，包含当前执行的测试用例的相关信息。
- `lineno`：断言所在的行号。
- `orig`：原始断言代码的字符串表示。
- `expl`：断言解释的字符串表示（如果有）。

# 示例代码

## 案例一：日志记录

目标：在每个断言成功时记录日志信息，以便对测试过程进行详细记录和调试。

步骤：
1. 使用 `pytest_assertion_pass` 钩子函数。
2. 在钩子函数中插入日志记录代码。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='assertion.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def pytest_assertion_pass(item, lineno, orig, expl):
    """在每个断言成功时记录日志信息"""
    logging.info(f"Assertion passed: {orig} at {item.location[0]}:{lineno}")

# 示例测试文件 `tests/test_example.py`
def test_example():
    assert 1 + 1 == 2
    assert "pytest" in "pytest is fun"
```

**注释**：
- 在 `pytest_assertion_pass` 钩子中记录断言成功的信息，包括断言的原始代码和所在文件及行号。
- 通过两条断言语句分别验证数学操作和字符串包含关系，确保钩子函数记录成功。

**注意**：

这里有个小知识点，看过我写的《pytest实战指南》的同学，不是是否有印象，在`pytest -h`的输出中，有这么一段内容：

```shell
enable_assertion_pass_hook (bool):
     Enables the pytest_assertion_pass hook. Make sure to delete any previously generated pyc cache files.
```
总结下来就两点：

* 需要设置`enable_assertion_pass_hook`为`true`，可在`pytest.ini`中设置
* 要求在`pytest_assertion_pass hook`中打印(print)或者日志记录(logging)内容，需要先清理掉cache，然后再执行测试代码。

`pytest.ini` 文件内容参考如下：

```shell
[pytest]
enable_assertion_pass_hook=true
```

再附带上清理`cache`代码：

```python
root@Gavin:~/test/hook# cat clear_pyc.py 
import os
import shutil


for dirs, folders, files in os.walk('.'):
    for each_file in files:
        root, end = os.path.splitext(each_file)
        if end == '.pyc':
            print(os.path.abspath(os.path.join(dirs, each_file)))
            os.remove(os.path.abspath(os.path.join(dirs, each_file)))

    if dirs.endswith(".pytest_cache") or dirs.endswith("__pycache__"):
        print(("{}".format(os.path.abspath(dirs))))
        shutil.rmtree(dirs)


if __name__ == '__main__':
    pass
```

## 案例二：统计信息收集

目标：收集断言通过的统计信息，例如通过断言的总数、每个测试用例中通过断言的数量等。

步骤：
1. 使用 `pytest_assertion_pass` 钩子函数。
2. 在钩子函数中插入统计信息收集代码。

示例代码：

```python
# conftest.py
import pytest

assertion_count = 0

def pytest_assertion_pass(item, lineno, orig, expl):
    """统计通过断言的数量"""
    global assertion_count
    assertion_count += 1

def pytest_sessionfinish(session, exitstatus):
    """在会话结束时输出统计信息"""
    print(f"Total number of passed assertions: {assertion_count}")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2
    assert "pytest" in "pytest is fun"

def test_example2():
    assert 2 * 2 == 4
    assert len("hello") == 5
```

**注释**：
- 在 `pytest_assertion_pass` 钩子中统计每个成功断言的数量。
- 在测试会话结束时，通过 `pytest_sessionfinish` 钩子输出统计信息。


## 案例三：监控和警报

目标：在特定条件下监控断言的成功，并根据需要触发警报或通知。

步骤：
1. 使用 `pytest_assertion_pass` 钩子函数。
2. 在钩子函数中插入监控逻辑，并根据需要触发警报或通知。

示例代码：

```python
# conftest.py
import pytest
import smtplib
from email.mime.text import MIMEText

alert_triggered = False
threshold = 5  # 设定一个阈值，当超过该阈值时触发警报
assertion_count = 0

def send_alert(count):
    msg = MIMEText(f"Alert: Number of passed assertions exceeded threshold: {count}")
    msg['Subject'] = 'Assertion Pass Alert'
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'recipient@example.com'

    # 假设 SMTP 服务器位于 localhost，并且没有身份验证
    with smtplib.SMTP('localhost') as server:
        server.sendmail('your_email@example.com', ['recipient@example.com'], msg.as_string())

def pytest_assertion_pass(item, lineno, orig, expl):
    """监控断言成功，并在超过阈值时触发警报"""
    global assertion_count, alert_triggered
    assertion_count += 1
    if assertion_count > threshold and not alert_triggered:
        send_alert(assertion_count)
        alert_triggered = True

def pytest_sessionfinish(session, exitstatus):
    """在会话结束时输出断言统计信息"""
    print(f"Total number of passed assertions: {assertion_count}")
    if alert_triggered:
        print("Alert: Number of passed assertions exceeded threshold and alert was sent.")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2
    assert "pytest" in "pytest is fun"

def test_example2():
    assert 2 * 2 == 4
    assert len("hello") == 5
    assert 10 / 2 == 5
    assert "world".upper() == "WORLD"
    assert isinstance(3.14, float)
```

**注释**：
- 在 `pytest_assertion_pass` 钩子中统计每个成功断言的数量，并在超过设定的阈值时通过 `send_alert` 函数发送电子邮件警报。
- `send_alert` 函数使用 `smtplib` 发送电子邮件通知警报信息。
- 在测试会话结束时，通过 `pytest_sessionfinish` 钩子输出断言统计信息，并提示是否触发了警报。

## 案例四：调试信息收集

目标：在调试复杂测试用例时记录更多成功断言的信息，帮助定位问题并验证预期情况。

步骤：
1. 使用 `pytest_assertion_pass` 钩子函数。
2. 在钩子函数中插入调试信息记录代码。

示例代码：

```python
# conftest.py
import pytest

debug_info = []

def pytest_assertion_pass(item, lineno, orig, expl):
    """记录每个成功断言的调试信息"""
    debug_info.append({
        'file': item.location[0],
        'line': lineno,
        'assertion': orig,
        'explanation': expl
    })

def pytest_sessionfinish(session, exitstatus):
    """在会话结束时输出调试信息"""
    print("\nDebug Information for Passed Assertions:")
    for info in debug_info:
        print(f"File: {info['file']}, Line: {info['line']}, Assertion: {info['assertion']}")
        if info['explanation']:
            print(f"Explanation: {info['explanation']}")
    print(f"Total number of passed assertions: {len(debug_info)}")

# 示例测试文件 `tests/test_example.py`
def test_example1():
    assert 1 + 1 == 2
    assert "pytest" in "pytest is fun"

def test_example2():
    assert 2 * 2 == 4
    assert len("hello") == 5
```

**注释**：
- 在 `pytest_assertion_pass` 钩子中记录每个成功断言的调试信息，包括文件名、行号、断言代码和解释（如果有）。
- 在测试会话结束时，通过 `pytest_sessionfinish` 钩子输出所有调试信息，帮助分析测试过程中的状态和行为。

## 运行和验证

确保目录结构如下：

```shell
root@Gavin:~/test/hook# tree
.
├── conftest.py
└── tests
    └── test_example.py

2 directories, 2 files
root@Gavin:~/test/hook#
```

在项目根目录下运行以下命令：

```shell
pytest -s -v --cache-clear
```

### 验证输出信息

根据不同的案例，控制台和日志文件输出应包含自定义逻辑的结果，如断言成功的日志信息、统计的通过断言数量、监控警报的触发信息及调试信息等。

### 控制台和日志文件示例

**案例一：日志记录**

`assertion.log` 文件内容示例：

```plaintext
root@Gavin:~/test/hook# cat assertion.log 
2024-06-04 14:07:36,832 - Assertion passed: 1 + 1 == 2 at tests/test_example.py:2
2024-06-04 14:07:36,832 - Assertion passed: "pytest" in "pytest is fun" at tests/test_example.py:3
```

**案例二：统计信息收集**

控制台输出示例：

```plaintext
root@Gavin:~/test/hook# pytest -s -v
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
configfile: pytest.ini
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                                       

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSEDTotal number of passed assertions: 4


=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

**案例三：监控和警报**

控制台输出示例：

```plaintext
collected 2 items                                                                                                                                                                                                                                       

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 FAILEDTotal number of passed assertions: 6


======================================================================================================================= FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example2 _____________________________________________________________________________________________________________________

    def test_example2():
        assert 2 * 2 == 4
        assert len("hello") == 5
        assert 10 / 2 == 5
>       assert "world".upper() == "WORLD"

tests/test_example.py:9: 
```

**案例四：调试信息收集**

控制台输出示例：

```plaintext
root@Gavin:~/test/hook# pytest -s -v
================================================================================================================== test session starts ==================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-35-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'dotenv': '0.5.2', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/test/hook
configfile: pytest.ini
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 2 items                                                                                                                                                                                                                                       

tests/test_example.py::test_example1 PASSED
tests/test_example.py::test_example2 PASSED
Debug Information for Passed Assertions:
File: tests/test_example.py, Line: 2, Assertion: 1 + 1 == 2
Explanation: (1 + 1) == 2
File: tests/test_example.py, Line: 3, Assertion: "pytest" in "pytest is fun"
Explanation: 'pytest' in 'pytest is fun'
File: tests/test_example.py, Line: 6, Assertion: 2 * 2 == 4
Explanation: (2 * 2) == 4
File: tests/test_example.py, Line: 7, Assertion: len("hello") == 5
Explanation: 5 == 5
 +  where 5 = len('hello')
Total number of passed assertions: 4


=================================================================================================================== 2 passed in 0.04s ===================================================================================================================
root@Gavin:~/test/hook#
```

# 总结

通过 `pytest_assertion_pass` 钩子，我们可以在断言成功时执行一些自定义操作，如记录日志、收集统计信息、触发监控警报和记录调试信息等，从而增强测试的可视化和调试能力。这些操作有助于提高测试的透明度和可维护性，确保测试过程中的每个断言都得到正确处理和记录。

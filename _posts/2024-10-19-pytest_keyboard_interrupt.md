---
title: pytest hook系列之pytest_keyboard_interrupt
date: 2024-10-19 23:00:00
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
summary: pytest hook之pytest_keyboard_interrupt
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述
`pytest_keyboard_interrupt` 是`pytest`框架中的一个钩子函数，用于在测试执行过程中捕获并处理 `KeyboardInterrupt` 事件。`KeyboardInterrupt` 通常由用户通过键盘输入（如 Ctrl+C）触发，用于中断测试的执行。通过这个钩子函数，我们可以自定义在测试中断时的行为，例如记录日志、清理资源、发送通知等，以便后续分析。

# 使用场景

1. **记录中断信息**：在测试中断时记录中断原因和相关信息，以便分析和排查问题。
2. **清理资源**：在测试中断时执行资源清理操作，例如释放文件句柄、关闭网络连接等。
3. **发送通知**：在测试中断时发送通知邮件或消息，告知相关人员测试被中断的情况。

# 参数

```python
def pytest_keyboard_interrupt(excinfo):
    # excinfo: 捕获的异常信息对象，包含详细的异常信息和调用栈
    pass
```

- `excinfo`：捕获的异常信息对象，包含详细的异常信息和调用栈。通过这个参数，我们可以获取 `KeyboardInterrupt` 的详细信息，并进行相应的处理。

# 示例代码

## 案例一：日志记录

目标：在测试中断时记录中断信息和调用栈，以便后续分析和处理。

步骤：
1. 使用 `pytest_keyboard_interrupt` 钩子捕获 `KeyboardInterrupt` 事件。
2. 将捕获的中断信息和调用栈记录到日志文件中。

示例代码：

```python
# conftest.py
import pytest
import logging

# 配置日志记录
logging.basicConfig(filename='keyboard_interrupt.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def pytest_keyboard_interrupt(excinfo):
    """记录中断信息到日志文件"""
    logging.error(f"Keyboard Interrupt: {excinfo}\n")
```

**注释**：
- 使用 `logging` 模块配置日志记录，将日志输出到 `keyboard_interrupt.log` 文件中。
- 在 `pytest_keyboard_interrupt` 钩子中，捕获 `KeyboardInterrupt` 事件并记录到日志文件中。

## 案例二：资源清理

目标：在测试中断时执行资源清理操作，以释放文件句柄、关闭网络连接等。

步骤：
1. 使用 `pytest_keyboard_interrupt` 钩子捕获 `KeyboardInterrupt` 事件。
2. 在钩子函数中执行资源清理操作。

示例代码：

```python
# conftest.py
import pytest
import logging

# 假设我们有一些需要清理的资源，例如文件句柄和网络连接
open_files = []
network_connections = []

# 配置日志记录
logging.basicConfig(filename='keyboard_interrupt.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def pytest_keyboard_interrupt(excinfo):
    """在中断时执行资源清理操作，并记录日志"""
    logging.error(f"Keyboard Interrupt: {excinfo}\n")
    
    # 关闭所有打开的文件
    for f in open_files:
        f.close()
    
    # 关闭所有网络连接
    for conn in network_connections:
        conn.close()

    logging.info("Resources have been cleaned up!")
```

**注释**：
- 假设我们有 `open_files` 和 `network_connections` 全局变量，表示一些需要清理的资源。
- 在 `pytest_keyboard_interrupt` 钩子中，执行资源清理操作并记录日志。

## 案例三：发送通知

目标：在测试中断时发送通知邮件或消息，告知相关人员测试被中断的情况。

步骤：
1. 使用 `pytest_keyboard_interrupt` 钩子捕获 `KeyboardInterrupt` 事件。
2. 在钩子函数中实现发送通知邮件或消息的逻辑。

示例代码：

```python
# conftest.py
import pytest
import smtplib
from email.mime.text import MIMEText
import logging

# 配置日志记录
logging.basicConfig(filename='keyboard_interrupt.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def send_email(subject, body):
    """发送邮件通知"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'sender@example.com'
    msg['To'] = 'recipient@example.com'

    with smtplib.SMTP('localhost') as server:  # 或者使用实际的 SMTP 服务器
        server.sendmail('sender@example.com', ['recipient@example.com'], msg.as_string())

def pytest_keyboard_interrupt(excinfo):
    """在中断时记录日志，并发送通知邮件"""
    logging.error(f"Keyboard Interrupt: {excinfo}\n")
    
    subject = "Pytest Keyboard Interrupt"
    body = f"Keyboard Interrupt detected: {excinfo}"
    send_email(subject, body)
```

**注释**：
- 定义 `send_email` 函数，用于通过 `SMTP` 发送电子邮件。
- 在 `pytest_keyboard_interrupt` 钩子中，捕获 `KeyboardInterrupt` 事件，记录日志并发送通知邮件。

## 运行和验证

**示例测试文件**：

```python
# tests/test_example.py
import time

def test_long_running():
    time.sleep(10)  # 模拟长时间运行的测试
    assert True
```

### 执行测试命令并模拟中断

在项目根目录下运行以下命令来执行测试，并在测试过程中按 `Ctrl+C` 中断测试：

```shell
pytest tests -v
```

### 验证输出和日志文件

根据具体的案例，你可以查看控制台输出和日志文件 `keyboard_interrupt.log`，验证 `KeyboardInterrupt` 事件被正确处理。

### 控制台输出示例

```plaintext
collected 1 item                                                                                                                                                                                                                                        

tests/test_example.py::test_long_running ^C
^C

================================================================================================================= no tests ran in 7.48s =================================================================================================================
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! KeyboardInterrupt !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
/root/test/hook/tests/test_example.py:4: KeyboardInterrupt
(to show a full traceback on KeyboardInterrupt use --full-trace)
```

### 日志文件 `keyboard_interrupt.log` 内容示例

```plaintext
root@Gavin:~/test/hook# cat keyboard_interrupt.log 
2024-10-19 10:31:58,279 - ERROR - Keyboard Interrupt: <ExceptionInfo KeyboardInterrupt() tblen=55>

root@Gavin:~/test/hook#
```

### 详细解释和总结

1. **记录中断信息**：
   - 使用 `pytest_keyboard_interrupt` 钩子捕获 `KeyboardInterrupt` 事件，并使用 `logging` 模块记录中断信息到日志文件中。

2. **资源清理**：
   - 使用 `pytest_keyboard_interrupt` 钩子捕获 `KeyboardInterrupt` 事件，在钩子函数中执行资源清理操作，如关闭文件和网络连接。

3. **发送通知**：
   - 使用 `pytest_keyboard_interrupt` 钩子捕获 `KeyboardInterrupt` 事件，在钩子函数中通过 `send_email` 函数发送通知邮件。



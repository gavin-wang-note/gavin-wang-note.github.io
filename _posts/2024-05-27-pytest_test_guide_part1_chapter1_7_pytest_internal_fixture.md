---
title: 《pytest测试指南》-- 章节1-7 pytest内置fixture
date: 2024-05-27 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-2.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 《pytest测试指南》一书 章节1-7 pytest内置fixture详细介绍与示例说明
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 第7章 pytest内置fixture

上一章节中我们介绍了`pytest fixture`，`fixture` 提供了一种优雅的方式来设置代码执行前的预置条件（如数据库连接、测试数据创建等），以及执行后的清理动作（比如断开网络连接、删除临时文件等）。最关键的是，它们让测试代码变得更简洁、可读，并大幅提高测试的可复用性。接下来介绍`pytest`内置fixture。`pytest` 之所以在开发者和测试工程师中广受欢迎，不仅在于它的易用性和强大的插件生态，更在于它的一个核心功能——内置的 fixtures 系统。`pytest` 通过一套内置的 fixtures 为开发者们带来了极致的灵活性和便捷性，无论是要为测试用例制造复杂的场景，还是要捕获和断言代码行为，抑或是要在测试周期内保持某些状态或配置——`pytest` 的内置 `fixture` 都能够帮助你轻松实现。
在本文中，我们将深入探索 `pytest` 内置 `fixture` 的强大功能，带你深入了解 `pytest` 内置 `fixture` 的世界。我们将探讨它们如何简化测试设置过程，如何让我们能够编写更模块化和可维护的测试代码，以及如何利用这些强大的工具来提高测试效率和质量。无论你是刚开始接触 `pytest`，还是已经是一个经验丰富的用户，了解这些内置 `fixture` 的细节都将对你的测试实践大有裨益。


# 7.1 pytest 内置 fixture 按功能分类

`pytest` 提供了多种内置的 fixtures 以帮助我们设置测试环境、参数化测试数据、测试执行控制以及记录测试过程等，可通过`pytest --fixtures  -v`命令查看全部的fixture，包括内置与用户自定义或安装的第三方fixture信息。

在 `pytest` 中，内置的 fixtures 按照功能划分可分为如下几个主要类别：

## 7.1.1 基础测试设置与清理

| Fixture                | 作用域           | 说明                                                         |
| ---------------------- | ---------------- | ------------------------------------------------------------ |
| **`cache`**            | session          | 提供存储和获取测试会话间数据的功能。                         |
| **`capsys`**           | function         | 捕获系统的输出和错误输出，并允许你在测试中访问它们。         |
| **`capsysbinary`**     | function         | 与 `capsys` 类似，但捕获的是二进制输出。                     |
| **`capfd`**            | function         | 与 `capfd` 类似，但捕获的是二进制输出。                      |
| **`monkeypatch`**      | function         | 临时修改类或模块、字典条目以及环境变量。                     |
| **`testdir`**          | function         | 提供一个临时的测试目录来运行接收 `pytest` 测试用例的测试，废弃中，推荐使用`tmpdir`。 |
| **`tmpdir`**           | function,session | 成一个临时目录用于测试中的文件操作。                         |
| **`tmpdir_factory`**   | function,session | 用于多个测试，跨测试函数、类、模块或整个会话创建临时目录。   |
| **`tmp_path`**         | function,session | 类似 `tmpdir`，但提供一个 `pathlib.Path` 对象。              |
| **`tmp_path_factory`** | function,session | 用于生成临时文件和目录，使用的是 `py.path.local` 对象。      |
| **`caplog`**           | function         | 用于捕获和检查日志输出。                                     |
| **`pytester`**         | function         | 用于编写对 `pytest` 本身的测试。                             |

## 7.1.2 记录测试套件属性

| Fixture                         | 作用域                           | 说明                                                         |
| ------------------------------- | -------------------------------- | ------------------------------------------------------------ |
| **`record_property`**           | function                         | 在测试报告中为测试用例添加额外的属性。                       |
| **`record_testsuite_property`** | session                          | 在测试套件级别记录额外的属性信息到报告中。                   |
| **`request`**                   | session, module, class, function | 访问请求特定的 `pytest` 固件。                               |
| **`fixture`**                   | session, module, class, function | 请求使用 fixtures 的列表。（`@pytest.fixture`是一个特殊的fixture哦） |

## 7.1.3 配置和测试功能

| Fixture            | 作用域   | 说明                       |
| ------------------ | -------- | -------------------------- |
| **`pytestconfig`** | session  | 访问 `pytest` 配置信息。   |
| **`recwarn`**      | function | 记录测试过程中出现的警告。 |

## 7.1.4 高级测试执行控制

| Fixture                 | 作用域  | 说明                                                         |
| ----------------------- | ------- | ------------------------------------------------------------ |
| **`doctest_namespace`** | session | 提供一个命名空间，使得 `doctest` 可以访问外部定义的变量和函数。 |

# 7.2 内置fixture详解

## 7.2.1 基础测试设置与清理

### 7.2.1.1 capfd/capsys

`pytest` 提供了 `capfd` 和 `capsys` 这两个内置的fixture用于捕获标准输出(`stdout`)和标准错误输出(`stderr`)，这对于测试期望输出的函数非常有用。尽管它们的功能非常相似，但它们之间存在一些关键的区别。

#### 7.2.1.1.1 capsys

`capsys` fixture 捕获由 `sys.stdout` 和 `sys.stderr` 生成的输出，主要是Python代码内部使用 `print()` 等函数产生的输出。

##### 7.2.1.1.1.1使用场景

捕获由纯Python代码生成的输出，通常用于测试标准输出和错误输出是否如预期产生：

- 测试函数是否从标准输入读取输入
- 测试函数是否通过标准输出打印输出
- 测试函数是否通过标准错误流打印错误信息

##### 7.2.1.1.1.2 代码示例

```python
# content of test_capsys.py
import sys
import pytest


def test_read_input(capsys):
    input("Enter your name: ")
    captured = capsys.readouterr()
    assert captured.out == "Enter your name: "


def test_print_output(capsys):
    print("hello world")
    captured = capsys.readouterr()
    assert captured.out == "hello world\n"


def test_print_error(capsys):
    print("An error occurred", file=sys.stderr)
    captured = capsys.readouterr()
    assert captured.err == "An error occurred\n"


def test_print_both(capsys):
    print("hello world")
    print("An error occurred", file=sys.stderr)
    captured = capsys.readouterr()
    assert captured.out == "hello world\n"
    assert captured.err == "An error occurred\n"
```

输出结果参考如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_capsys.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code/chapter1-7
plugins: check-2.2.2, metadata-3.0.0
collected 4 items

test_capsys.py::test_read_input Hello Gavin
PASSED
test_capsys.py::test_print_output PASSED
test_capsys.py::test_print_error PASSED
test_capsys.py::test_print_both PASSED

=============================== 4 passed in 3.69s =============================
root@Gavin:~/code/chapter1-7#
```

注意，这里执行`pytest`命令时，需要携带上参数'-s'，表示‘reading from stdin while output is captured’，因为测试用例中使用了input方法。

#### 7.2.1.1.2 capfd

`capfd` fixture 捕获所有到文件描述符 1（标准输出）和 2（标准错误）的输出，这包括系统级别的输出，甚至是Python代码之外的输出。

关于文件描述符(fd)，本文不做介绍，请另行查阅资料。

##### 7.2.1.1.2.1 使用场景

捕获系统调用、子进程或C语言扩展模块生成的输出。

  - 测试函数是否打印输出
  - 测试函数是否打印错误信息

##### 7.2.1.1.2.2 代码示例

```python
# content of test_capfd.py
import pytest

def test_print_output(capfd):
    print("hello world")
    out, err = capfd.readouterr()
    assert out == "hello world\n"


def test_print_error(capfd):
    print("An error occurred", file=sys.stderr)
    out, err = capfd.readouterr()
    assert err == "An error occurred\n"


def test_print_both(capfd):
    print("hello world")
    print("An error occurred", file=sys.stderr)
    out, err = capfd.readouterr()
    assert out == "hello world\n"
    assert err == "An error occurred\n"
```

上述例子中，分别校验了标准输出，标准错误，用例可全部执行通过，运行效果如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_capfd.py
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code/chapter1-7
plugins: check-2.2.2, metadata-3.0.0
collected 3 items

test_capfd.py::test_print_output PASSED
test_capfd.py::test_print_error PASSED
test_capfd.py::test_print_both PASSED

================================== 3 passed in 0.01s ===========================
root@Gavin:~/code/chapter1-7#
```

#### 7.2.1.1.3 capsys与capfd的区别

 `capsys` 和 `capfd` 的主要差异如下：

| 特性           | capsys                                                  | capfd                                  |
| -------------- | ------------------------------------------------------- | -------------------------------------- |
| 捕获层级       | Python层（例如 `sys.stdout` 和 `sys.stderr`）           | 系统层（文件描述符，包括Python层）     |
| 使用场景       | 测试纯Python打印输出                                    | 测试包含系统调用或子进程的打印输出     |
| 捕获子进程输出 | 不能捕获                                                | 能捕获                                 |
| 相互干扰可能性 | 较低                                                    | 较高，因为可能捕获到其他非测试代码输出 |
| 推荐使用       | 当你仅需要捕获由 `print()` 等Python内部函数产生的输出时 | 当你需要捕获包括子进程在内的所有输出时 |

选择使用 `capsys` 还是 `capfd` 主要取决于你的具体测试需求。如果测试的功能仅涉及Python代码产生的输出，`capsys` 是足够的，并且测试结果不太可能受到不相关输出的干扰。相反，如果测试的代码将运行子进程或其他可能直接写入文件描述符的功能，则 `capfd` 更合适。

### 7.2.1.2 capfdbinary/capsysbinary

#### 7.2.1.2.1 capfdbinary

`capfdbinary` 与 `capfd` 类似，它允许你捕获在测试过程中向文件描述符 1（标准输出）和 2（标准错误）写入的二进制输出。不同之处在于，`capfdbinary` 保留了输出的二进制形式，而不是将其解码成字符串形式。

如果你的测试需要捕获并检查二进制数据的精确内容，比如来自二进制可执行程序或产生非文本输出的系统调用，那么使用 `capfdbinary` 将非常有用。

##### 7.2.1.2.1.1 使用场景

- 检查生成图像、音频或其他非文本文件的程序的输出。
- 测试可能产生或处理二进制数据的程序，如数据压缩或加密程序。
- 捕获来自不产生标准文本输出的外部工具或子进程的输出。

##### 7.2.1.2.1.2 代码示例

假设我们有一个程序或脚本，它输出特定的二进制数据到 `stdout`，我们可以使用 `capfdbinary` 来捕获这些数据，进行测试。

```python
# test_capfdbinary.py

def test_capfdbinary(capfdbinary):
    # 假设我们有如下函数，它打印二进制内容到 stdout
    def print_header():
        print('89PNG\r\n\x1a\n', end='')

    print_header()
    # 使用 capfdbinary 捕获输出
    captured = capfdbinary.readouterr()
    
    # 断言是否捕获到了正确的二进制
    assert captured.out == b'89PNG\r\n\x1a\n'
    assert captured.err == b''  # 确认 stderr 没有数据
```

在上面的例子中，我们可以看到一个捕获二进制输出并进行断言的简单例子。需要注意的是，断言时比较的是二进制数据（如：用 `b''` 表示的字节字符串）。

#### 7.2.1.2.2 capsysbinary

在 `pytest` 中，`capsysbinary` 的作用类似于 `capfdbinary` 和 `capsys`，但专门用于捕获二进制形式的系统捕获（系统输出`stdout`和错误`stderr`）。这可以非常有用，当你需要测试的代码产生了二进制输出，比如写一个文件下载的功能测试，或者你的代码直接向 `sys.stdout.buffer` 或 `sys.stderr.buffer` 写入二进制数据。

**主要特征：**

- **二进制数据捕获**：`capsysbinary` 捕获标准输出和标准错误的二进制形式。
- **测试期间的数据检查**：允许你在测试中检查和断言在` stdout`或 `stderr` 中输出的二进制数据。
- **清理及隔离输出**：每个测试结束后，captured output/output 将会被清除，保证测试间的隔离。

##### 7.2.1.2.2.1 使用场景

为了使用 `capsysbinary`，你需要在测试函数中作为参数包含它。`pytest` 将自动处理 fixture，并且在测试结束后，处理捕获的数据。

```python
# content of test_capsysbinary.py
import sys

def test_output_binary_data(capsysbinary):
    sys.stdout.buffer.write(b'This is binary stdout data')
    sys.stderr.buffer.write(b'This is binary stderr data')
    
    # 获取捕获到的输出
    captured = capsysbinary.readouterr()

    # 现在你可以断言这两个数据
    assert captured.out == b'This is binary stdout data'
    assert captured.err == b'This is binary stderr data'
```

在上述示例中：

- `sys.stdout.buffer.write` 和 `sys.stderr.buffer.write` 用于直接写二进制数据到标准输出和标准错误。
- `capsysbinary.readouterr()` 调用返回一个包含两个属性的对象：`out` 和 `err`，其中包含了到目前为止的捕获数据。这让你可以断言这些输出是否与预期一致。

请注意，这异于 `capsys`，后者捕获的是文本（编码为字符串）数据，而 `capsysbinary` 专门处理二进制数据。

##### 7.2.1.2.2.2 代码示例

下面是如何在一个测试中使用 `capsysbinary` 的示例：

```python
# content of test_capsysbinary.py
import sys

def test_binary_output(capsysbinary):
    # 假设你有一个函数，它产生二进制数据到 stdout 和 stderr
    def output_binary_data():
        sys.stdout.buffer.write(b'\x89PNG\r\n\x1a\n')  # 比如二进制的PNG文件头
        sys.stderr.buffer.write(b'\x00\x01\x02\x03\x04')  # 随便一些二进制错误
    
    output_binary_data()
    captured = capsysbinary.readouterr()
    
    # 测试 stdout 上的二进制输出
    assert captured.out == b'\x89PNG\r\n\x1a\n'
    
    # 测试 stderr 上的二进制输出
    assert captured.err == b'\x00\x01\x02\x03\x04'
```

在这个测试中，`output_binary_data` 函数模拟了生成二进制数据的代码。`capsysbinary.readouterr()` 捕获了这些输出，允许你在断言中检查这些二进制数据。通过这种方式，你可以保证你的代码按预期产生了正确的二进制数据。

两个示例执行效果如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_capsysbinary.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code/chapter1-7
plugins: check-2.2.2, metadata-3.0.0
collected 2 items

test_capsysbinary.py::test_output_binary_data PASSED
test_capsysbinary.py::test_binary_output PASSED

================================ 2 passed in 0.00s ============================
root@Gavin:~/code/chapter1-7#
```

#### 7.2.1.2.3 capfdbinary/capsysbinary的区别

`pytest` 提供的两种捕获测试中二进制输出的方法，`capfdbinary` 和 `capsysbinary`，这两个 fixtures 主要区别在于它们捕获输出的层级：

| 功能                       | `capfdbinary`                                                | `capsysbinary`                                               |
| -------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **描述**                   | 捕获系统层面的二进制输出至文件描述符。                       | 捕获Python标准库中的 `sys.stdout` 和 `sys.stderr` 输出的二进制流。 |
| **捕获范围**               | 更底层，可以捕获到直接写入到操作系统文件描述符的输出（`stdout/stderr`），包括由子进程生成的输出。 | 仅捕获到由当前Python进程自己的代码直接写入到 `sys.stdout` 或 `sys.stderr` 的输出。 |
| **捕获对象**               | 包括由非 Python 代码（如C扩展）写入的输出。                  | 限于由 Python 代码产生的输出。                               |
| **捕获输出的形式**         | 二进制形式。                                                 | 二进制形式。                                                 |
| **适合场景**               | 当涉及底层或跨语言的输出操作时，如使用 `ctypes` 调用 C 函数时的输出。 | 当测试的对象仅为 Python 代码时，更加常用。                   |
| **测试代码示例**           | `out, err = capfdbinary.readouterr()`                        | `out, err = capsysbinary.readouterr()`                       |
| **适用输出**               | 标准输出(`stdout`)或标准错误(`stderr`)                       | 标准输出(`stdout`)或标准错误(`stderr`)                       |
| **返回值类型**             | 返回捕获到的输出和错误为二进制形式                           | 返回捕获到的输出和错误为二进制形式                           |
| **与`capfd/capsys`的关系** | `capfdbinary`是`capfd`的二进制版本，专用于捕获二进制数据的场景 | `capsysbinary`是`capsys`的二进制版本，专用于捕获二进制数据的场景 |

### 7.2.1.3 caplog

在 `pytest` 中，`caplog` 用于捕获和检查日志输出。`caplog` 在 `pytest` 中扮演着“记录器（logger）”的角色，与内置的记录器相比，`caplog` 可以轻松地存储和查询日志消息，它允许测试者验证代码中的日志调用是否按预期执行，还可以用来确保日志消息的内容、级别和其他属性是否正确。

`caplog` 最常见的使用场景是在需要临时重新配置记录器的过滤器或处理程序的情况下，因为这可以保护正在测试的代码免受其他日志消息的影响。

#### 7.2.1.3.1 主要特性

- **捕获日志记录**：`caplog` 可以捕获在测试运行期间产生的日志输出。
- **配置日志级别**：可以在测试中动态设置捕获的日志级别，例如只捕获警告以上的日志。
- **检查日志记录**：提供方便的接口来检查日志消息的内容和属性。

#### 7.2.1.3.2 使用方法/场景

要使用 `caplog` fixture，你只需要在你的测试函数中作为参数引入它，`pytest` 会自动识别并传入 `caplog` 对象。

常用方法如下：

- `caplog.clear()`： 清除所有已捕获的日志消息。
- `caplog.record_tuples()`: 返回捕获的所有日志消息的元组。每个元组包含日志记录级别、消息和日志函数名称。
- `caplog.records`：一个记录（`logging.LogRecord` 对象）的列表，提供对每个日志消息的访问。
- `caplog.set_level(level, logger=None)`: 为给定的记录器设置日志级别。
- `caplog.text()`: 返回捕获的所有日志消息的文本，一个字符串，包含测试期间所有捕获的日志输出。

`caplog` 常被用于如下场景：

- 测试日志输出是否正确。
- 测试日志记录级别是否正确。
- 测试日志记录器是否正确配置。

#### 7.2.1.3.3 代码示例

以下是如何使用 `caplog` fixture 的一个简单示例：

```python
# content of test_caplog.py
import logging

def function_that_logs():
    logging.info("Info level log message")
    logging.warning("Warning level log message")

def test_logging(caplog):
    function_that_logs()
    # 使用 caplog 来进行断言
    assert "Info level log message" in caplog.text
    assert "Warning level log message" in caplog.text
    # 检查特定级别的日志
    for record in caplog.records:
        assert record.levelname != "ERROR"  # 确保没有错误级别的日志记录
```

在上述代码中：

- `function_that_logs` 是一个简单的函数，它会产生不同级别的日志消息。
- `test_logging` 是测试函数，它使用 `caplog` fixture 来检查 `function_that_logs` 函数产生的日志消息。

上述代码执行过程报错，因为`caplog`默认只捕获和检查WARNING级别及以上的log，如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_caplog.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code/chapter1-7
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_caplog.py::test_logging FAILED

================================ FAILURES =====================================
________________________________ test_logging _________________________________

caplog = <_pytest.logging.LogCaptureFixture object at 0x7f4bd18e8150>

    def test_logging(caplog):
        # caplog.set_level(logging.INFO)
        function_that_logs()
        # 使用 caplog 来进行断言
>       assert "Info level log message" in caplog.text
E       AssertionError: assert 'Info level log message' in 'WARNING  root:test_caplog.py:5 Warning level log message\n'
E        +  where 'WARNING  root:test_caplog.py:5 Warning level log message\n' = <_pytest.logging.LogCaptureFixture object at 0x7f4bd18e8150>.text

test_caplog.py:11: AssertionError
----------------------- Captured log call ------------------------------------
WARNING  root:test_caplog.py:5 Warning level log message
======================== short test summary info ==============================
FAILED test_caplog.py::test_logging - AssertionError: assert 'Info evel log message' in 'WARNING  root:test_caplog.py:5 Warning level log message\n'
=============================== 1 failed in 0.03s ==============================
root@Gavin:~/code/chapter1-7
```

如何解决呢？我们接下来讲如何设置日志级别。

**设置日志级别：**

在测试开始前，你可以设置 `caplog` 的日志级别来决定捕获哪些级别的日志消息：

```python
def test_logging_with_specific_level(caplog):
    caplog.set_level(logging.WARNING)  # 只捕获警告和警告以上级别的日志
    function_that_logs()
    assert "Warning level log message" in caplog.text
    assert "Info level log message" not in caplog.text
```

在这个示例中，通过调用 `caplog.set_level()` 并传入 `logging.WARNING`，测试将只会捕获警告及以上级别的日志消息。这意味着 `caplog.text` 不应该包含信息级别（INFO）的日志消息。

### 7.2.1.4 config.cache

`pytest` 的 `config.cache` 是一个与 `pytest` 配置对象（通常标识为 `config`）相关联的缓存对象，它允许在连续的测试运行之间存储和读取数据。这样，你可以在一次测试中缓存某些数据，然后在后续的测试中重新使用这些数据。

缓存功能可以在多个测试运行之间保留数据，这对于保存不经常变化或计算成本高昂的结果非常有用。默认情况下缓存将保存到`.pytest_cache`目录中的一个特殊文件中，除非你指定了`config.cache`的`mkdir`参数，创建了其他目录/路径。

#### 7.2.1.4.1 使用场景

要使用缓存，需要导入 `cache` fixture 并在测试函数中使用它。例如，你可能希望在测试期间缓存一些配置参数或一个复杂计算的结果。

#### 7.2.1.4.2 代码示例

下面是如何使用 `config.cache` 的一个示例：

```python
# content of test_config_cache.py
import pytest

def costly_computation():
    print("Performing costly computation...")
    return 42

def test_expensive_computation(pytestconfig):
    # 尝试从缓存中获取先前的运算结果
    if 'expensive_result' in pytestconfig.cache:
        result = pytestconfig.cache.get('expensive_result', None)
    else:
        # 运算结果不在缓存中，执行高成本计算
        result = costly_computation()
        # 将结果存入缓存，以备未来使用
        pytestconfig.cache.set('expensive_result', result)

    assert result == 42
```

在上述代码中：

- `test_expensive_computation` 使用 `pytestconfig` fixture 来引入配置和缓存对象。
- 函数会首先尝试从缓存中读取 `'expensive_result'` 键关联的值。
- 如果缓存中不存在这个值（例如，在第一次运行时），则会执行一个"昂贵"的计算，并保存它的结果到缓存中。
- 这样，在再次运行测试时，就可以直接从缓存中读取计算结果，而避免重新进行计算。

第一次运行，你会看到打印信息`Performing costly computation...`：

```shell
root@Gavin:~/code/chapter1-7# pytest -q test_config_cache.py 
================================ test session starts ==========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, html-4.1.1, metadata-3.0.0
collected 1 item

test_config_cache.py::test_expensive_computation FAILED                 [100%]

================================= FAILURES =====================================
_________________________________ test_expensive_computation ___________________

mydata = 23

    def test_expensive_computation(mydata):
>       assert mydata == 42
E       assert 23 == 42

test_config_cache.py:21: AssertionError
------------------------------- Captured stdout setup ---------------------------
Performing costly computation...
================================== 1 failed in 0.04s ============================
root@Gavin:~/code/chapter1-7#
```

第二次运行，所有数据会从cache中读取，不再有打印信息`Performing costly computation...`：

```shell
root@Gavin:~/code/chapter1-7# pytest -q test_config_cache.py 
================================= test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, html-4.1.1, metadata-3.0.0
collected 1 item

test_config_cache.py::test_expensive_computation FAILED                  [100%]

================================== FAILURES =====================================
______________________________ test_expensive_computation _______________________

mydata = 23

    def test_expensive_computation(mydata):
>       assert mydata == 42
E       assert 23 == 42

test_config_cache.py:21: AssertionError
================================= 1 failed in 0.04s =============================
root@Gavin:~/code/chapter1-7#
```

#### 7.2.1.4.3 检查缓存内容

```shell
root@Gavin:~/code/chapter1-7# pytest --cache-show
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, html-4.1.1, metadata-3.0.0
cachedir: /root/code/.pytest_cache
----------------------------- cache values for '*' ----------------------------
cache/lastfailed contains:
  {'chapter1-7/test_config_cache.py::test_expensive_computation': True}
cache/nodeids contains:
  ['chapter1-7/test_config_cache.py::test_expensive_computation']
cache/stepwise contains:
  []
expensive_result contains:
  23

============================== no tests ran in 0.00s ===========================
root@Gavin:~/code/chapter1-7#
```

`--cache-show`包含一个可选参数，用于指定用于过滤的glob模式：

```shell
root@Gavin:~/code/chapter1-7# pytest --cache-show test_cap*
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, html-4.1.1, metadata-3.0.0
cachedir: /root/code/.pytest_cache
-------------------- cache values for 'test_capfdbinary.py' --------------------

=========================== no tests ran in 0.00s ==============================
root@Gavin:~/code/chapter1-7# 
```

#### 7.2.1.4.4 清理缓存

缓存可以在终端使用 `pytest --cache-clear` 来清除。这个命令将删除 `.pytest_cache` 目录及其内容。

在实践中，缓存不应该用于共享测试状态或者测试期间的数据，因为这将违背独立测试的原则。但是，它非常适合在连续的测试运行中保存一些不常变化的环境配置或者重用之前的计算结果等。

这里会借助`--lf`和`--ff`，从cache中读取失败用例历史记录，再次执行。

- `--lf`, `--last-failed` - to only re-run the failures.
*  --last-failed --last-failed-no-failures all      # runs the full test suite (default behavior)
  * --last-failed --last-failed-no-failures none   # runs no tests and exits successfully
  
- `--ff`, `--failed-first` - to run the failures first and then the rest of the tests.

#### 7.2.1.4.5 关于逐步执行(stepwise)

作为 `--lf -x` 的替代方案，尤其是在预计大部分测试套件都会失败的情况下，`--sw`、`--stepwise` 可以让你一次解决一个问题。测试套件将运行到第一次失败，然后停止，在下一次调用时，测试将从上一次失败的测试开始，一直运行到下一次失败的测试。你可以使用 `--stepwise-skip` 选项忽略一个失败的测试，而在第二个失败的测试中停止测试执行。如果卡在一个失败的测试上，只想稍后再忽略它，这个选项就很有用。提供 `--stepwise-skip` 也会隐式启用 `--stepwise` 选项。

### 7.2.1.5 monkeypatch

`pytest` 的 `monkeypatch` fixture 提供了一个方便的方式来动态地修改类或模块等在测试期间的行为。这通常用于“打补丁”来覆盖某些不便于测试的全局设置或行为。例如，你可以使用 `monkeypatch` 来更改环境变量、修改类或对象的属性、替换函数或方法以及操纵模块的导入。

#### 7.2.1.5.1 主要功能

- **设置、删除和恢复环境变量**。
- **修改对象、类或模块的属性**。
- **替换（patch）函数或方法为 mock 对象**。

#### 7.2.1.5.2 使用方法

在测试中使用 `monkeypatch` fixture 时，只需在测试函数的参数中包含 `monkeypatch`，`pytest` 会自动传入这个 fixture。

#### 7.2.1.5.3 代码示例

修改环境变量：

```python
# content of test_monkeypath.py
import os


def test_modify_env(monkeypatch):
    # 假设我们依赖于环境变量HOME
    monkeypatch.setenv('HOME', '/new/path')
    assert os.environ['HOME'] == '/new/path'
```

修改对象的属性：

```python
# content of test_monkeypath.py
class MyClass:
    class_var = 'original value'

def test_change_class_var(monkeypatch):
    # 使用 monkeypatch 来更改 MyClass 中的 class_var 值
    monkeypatch.setattr(MyClass, 'class_var', 'modified value')
    
    instance = MyClass()
    assert instance.class_var == 'modified value'
```

替换函数或方法：

```python
# content of test_monkeypath.py
import some_module

def fake_func(*args, **kwargs):
    return 'fake value'

def test_replace_function(monkeypatch):
    # 替换 some_module.some_function 为 fake_func
    monkeypatch.setattr(some_module, 'some_function', fake_func)

    result = some_module.some_function()
    assert result == 'fake value'
```

上面这个示例中`some_module`，在实际调试是需要替换为具体存在的模块，上文只是伪码示例，比如下面的调测：

```python
# content of test_monkeypath.py
def fake_func(*args, **kwargs):
    return 'fake value'

def test_replace_function(monkeypatch):
    # 替换 some_module.some_function 为 fake_func
    # monkeypatch.setattr(some_module, 'some_function', fake_func)
    monkeypatch.setattr(os, 'uname', fake_func)

    # result = some_module.some_function()
    result = os.uname()
    assert result == 'fake valu
```

如上用例，执行结果如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_monkeypath.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code/chapter1-7
plugins: check-2.2.2, metadata-3.0.0
collected 3 items

test_monkeypath.py::test_modify_env PASSED
test_monkeypath.py::test_change_class_var PASSED
test_monkeypath.py::test_replace_function PASSED

=============================== 3 passed in 0.01s ===============================
root@Gavin:~/code/chapter1-7#
```

monkeypatch还有许多有用的方法可以用来修改代码的行为，下面是一些常用的方法：

- `setattr(obj, attr, value)`：将obj的attr属性的值设置为value。
- `getattr(obj, attr)`：获取obj的attr属性的值。
- `delattr(obj, attr)`：删除obj的attr属性。
- `setenv(name, value)`：设置环境变量。
- `delenv(name, raising=True)`：删除环境变量
- `monkeypatch.syspath_prepend(path)`：临时把路径添加到 `sys.path`。
- `unsetenv(name)`：删除环境变量。
- `chdir(path)`：更改当前工作目录。
- `isfile(path)`：检查文件是否存在。
- `isdir(path)`：检查目录是否存在。
- `join(path, *paths)`：连接路径。
- `copy(src, dst)`：复制文件。
- `delete(path)`：删除文件或目录。
- `mkdir(path)`：创建目录。
- `makedirs(path)`：创建多级目录。
- `rmtree(path)`：删除目录及其子目录。

#### 7.2.1.5.4 最佳实践

使用 `monkeypatch` 可以帮助创建更可控的测试环境，减少测试与外部因素的依赖，从而提高测试的可靠性和独立性。`monkeypatch` 提供的所有修改，在测试方法结束时都会被恢复，这意味着对系统不会有永久性的影响，保证了测试的隔离性。因此，测试开发者可以放心地使用 `monkeypatch`，无需担心需要手动撤销他们的修改。

以下是使用`monkeypatch`的一些最佳实践：

- 尽可能使用内置的`monkeypatch`方法，而不是使用直接修改代码的方式。
- 在测试用例中只使用`monkeypatch`来修改必需的代码。
- 在测试用例的最后，使用`monkeypatch.undo()`来撤销所有修改。
- 避免使用`monkeypatch`来测试代码的实现细节。
- 使用`monkeypatch`来测试依赖外部资源的代码的集成行为。

### 7.2.1.6 pytester

`pytester` 用于编写对 `pytest` 本身的测试，这种测试称为端到端（end-to-end）测试或集成测试，通常用于确保 `pytest` 插件和功能按预期工作。它为测试提供了一个模拟的 `pytest` 测试环境，允许你运行 `pytest` 测试和检查结果。

通过 `pytester`，你可以创建文件、编写测试代码、运行子测试、并检查运行结果，这是 `pytest` 插件开发者经常使用的工具：

- `pytester` fixture是通过调用`request.getfixturevalue("testdir")`获得的，其中`testdir`是`pytest`内置的另一个fixture，用于创建临时目录，并在临时目录中运行测试代码。

- `pytester` fixture提供了许多有用的方法，例如`makefile()`, `path()`, `runpytest()`等，可以用来测试文件系统、命令行。

这些方法都是很直观的，比如：

   - `makefile("filename", "content")`函数可以创建一个指定的文件名和内容的文件
   - `path(".filename")`方法可以返回一个`pathlib.Path`对象，该对象可以用来对文件进行各种操作，如读取、写入、删除等。
   - `runpytest`方法可以运行`pytest`命令，并返回一个`Result`对象，该对象包含了命令的返回码、标准输出和标准错误等信息。

使用`pytester` fixture可以大大简化对文件系统、命令行和网络交互的测试，使测试代码更加简洁和可维护。

#### 7.2.1.6.1 主要功能

- 创建临时的测试目录
- 生成测试文件和配置文件
- 运行测试并收集结果
- 提供一个简易的方式来分析和断言测试输出和结果

#### 7.2.1.6.2 使用场景

- 插件开发：当开发新的 `pytest` 插件时，使用 `pytester` 可以帮助插件开发者编写集成测试，确保插件按预期运行。
- 高级测试场景：当需要对 `pytest` 测试过程本身进行测试或者需要复杂的测试场景时，`pytester` 提供的辅助工具非常有用。

#### 7.2.1.6.3 代码示例

要使用它，需要事先在`conftest.py`文件中添加如下记录：

```python
# content of conftest.py
pytest_plugins = "pytester"
```

下面的示例展示了如何使用 `pytester` 来写一个简单的集成测试：

```python
# content of test_pytester.py
def test_pytester_example(pytester):
    # 创建一个临时的 Python 测试文件
    pytester.makepyfile("""
        def test_pass():
            assert 1 == 1

        def test_fail():
            assert 1 == 2
    """)

    # 运行 pytest 在当前的 pytester 环境中
    result = pytester.runpytest()

    # 检查测试结果
    result.assert_outcomes(passed=1, failed=1)

    # result.ret 返回一个整数，表示测试是否通过
    # 一般来说，0 表示测试通过，1 表示测试失败
    assert result.ret == 1

    # result.stdout 和 result.stderr 可以让你访问测试的输出
    # 这里我们检查输出中是否包含特定的字符串
    assert result.stdout.str().find('100%') != -1 # 检查成功率100%
    assert 'test_fail' in result.stdout.str()    # 检查失败的测试是否出现

    # 你可以使用 'result.stdout.lines' 获取输出的行列表
    for line in result.stdout.lines:
        print(line) # 这里可以打印每一行的内容，或者进行额外的处理和断言
```

在这个示例中，我们首先使用 `pytester` 执行以下步骤：

* 创建测试文件：`makepyfile` 方法是 `pytester` 提供的，用于创建一个临时的 Python 测试文件。这个文件包含两个测试函数：一个会通过，另一个会失败。
* 运行测试：`runpytest` 方法启动 `pytest`，就像在命令行中运行一样。这将运行所有在 `pytester` 环境中创建的测试。
* 检查结果：`assert_outcomes` 方法用于验证测试结果。在这个案例中，我们预期有一个测试通过（`passed=1`）和一个测试失败（`failed=1`）。

执行效果如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_pytester.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 1 item

test_pytester.py::test_pytester_example 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /tmp/pytest-of-root/pytest-11/test_pytester_example0
plugins: html-4.1.1, metadata-3.0.0
collected 2 items

test_pytester_example.py .F                                      [100%]

=================================== FAILURES ==================================
___________________________________ test_fail _________________________________

    def test_fail():
>       assert 1 == 2
E       assert 1 == 2

test_pytester_example.py:5: AssertionError
=========================== short test summary info ===========================
FAILED test_pytester_example.py::test_fail - assert 1 == 2
=========================== 1 failed, 1 passed in 0.03s =======================
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /tmp/pytest-of-root/pytest-11/test_pytester_example0
plugins: html-4.1.1, metadata-3.0.0
collected 2 items

test_pytester_example.py .F                                       [100%]

================================= FAILURES ====================================
___________________________________ test_fail _________________________________

    def test_fail():
>       assert 1 == 2
E       assert 1 == 2

test_pytester_example.py:5: AssertionError
========================== short test summary info ============================
FAILED test_pytester_example.py::test_fail - assert 1 == 2
========================== 1 failed, 1 passed in 0.03s ========================
PASSED

=============================== 1 passed in 0.10s =============================
root@Gavin:~/code/chapter1-7#
```

`pytester` 提供了多种方法来辅助测试，如下：

```shell
['CLOSE_STDIN', 'TimeoutExpired', 'chdir', 'collect_by_name', 'copy_example', 'genitems', 'getinicfg', 'getitem', 'getitems', 'getmodulecol', 'getnode', 'getpathnode', 'inline_genitems', 'inline_run', 'inline_runsource', 'make_hook_recorder', 'makeconftest', 'makefile', 'makeini', 'makepyfile', 'makepyprojecttoml', 'maketxtfile', 'mkdir', 'mkpydir', 'parseconfig', 'parseconfigure', 'path', 'plugins', 'popen', 'run', 'runitem', 'runpytest', 'runpytest_inprocess', 'runpytest_subprocess', 'runpython', 'runpython_c', 'spawn', 'spawn_pytest', 'syspathinsert']
```

此外，`runpytest` 返回的对象提供了诸多方法和属性，用于分析测试运行结果，如 `stdout`、`stderr`、`parseoutcomes` 等。

使用 `pytester` 时需要注意，因为这些测试运行真实的 `pytest` 会话，它们通常会比单元测试运行得更慢。因此，在编写大量使用 `pytester` 的测试时，要特别考虑测试的速度和效率。

## 7.2.2 高级测试执行控制

### 7.2.2.1 doctest_namespace

`doctest_namespace` 在 `pytest` 中用于为 `doctest` 测试扩展全局命名空间。`doctest` 是一种编写简单的交互式 Python 会话的测试，通常写在文档字符串（`docstrings`）中。`pytest` 通过集成 `doctest`，能够执行包含在文档字符串中的这些交互式会话测试。

基本上，`doctest_namespace` fixture 允许你向 `doctests` 的命名空间添加条目（变量、函数等），这样就可以在 `doctest` 中使用它们而无需明确的导入。这在当你想在多个 `doctests` 中共享一些预定义的帮助函数或数据时非常有用。

以下是一个使用 `doctest_namespace` 的例子：

假设你有如下的函数：

```python
# content of test_doctest_namespace.py

def square(x):
    """Return the square of a number.

    Examples
    --------
    >>> square(4)
    16
    """
    return x * x
```

你可以在 `conftest.py` 中添加以下内容来扩展 `doctest` 的全局命名空间：

```python
import pytest

# conftest.py

@pytest.fixture(autouse=True)
def add_square_to_doctest_namespace(doctest_namespace):
    doctest_namespace['square'] = lambda x: x * x
```

在这个 `conftest.py` 中，我们使用 `@pytest.fixture` 创建了一个自动使用的 fixture （`autouse=True`）, 它会接受 `doctest_namespace` 作为参数，并向它添加了 `square` 函数。现在，任何 `doctest` 都可以直接使用 `square` 函数而无需显式的导入。其执行效果如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v --doctest-modules test_doctest_namespace.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code/chapter1-7
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_doctest_namespace1.py::test_doctest_namespace.square PASSED

=============================== 1 passed in 0.01s ==============================
root@Gavin:~/code/chapter1-7# 
```

当你运行 `pytest` 时，它会执行 `square` 函数的 `doctest` 并使用 `conftest.py` 中的 fixture 扩展的 `square` 来完成测试。

使用 `doctest_namespace` fixture 的优点是它为 `doctest` 提供了更大的灵活性和可重用性。不过，你应该谨慎使用这个特性，因为它可能使得 `doctest` 在它们自己的文档字符串之外的环境中表现不同，这可能导致一些混淆。

## 7.2.3 配置和测试功能

### 7.2.3.1 pytestconfig

`pytestconfig` 提供了对 `pytest` 配置值的访问能力，这允许测试代码获取关于当前测试运行配置的信息，包括命令行参数、选项、配置文件、插件、运行目录以及其他配置项。

`pytestconfig`是`request.config`的快捷方式，它在`pytest`文档里有时候被称为“pytest配置对象”。

#### 7.2.3.1.1 pytestconfig 源码分析

如下内容来自`pytest-main/src/_pytest/fixtures.py`，参考如下：

```python
@fixture(scope="session")
def pytestconfig(request: FixtureRequest) -> Config:
    """Session-scoped fixture that returns the session's :class:`pytest.Config`
    object. 

    Example::

        def test_foo(pytestconfig):
            if pytestconfig.getoption("verbose") > 0:
                ...

    """
    return request.config
```

从上面的源码看出，实际返回的就是 `request.config`，所以`pytestconfig` 的作用跟 `request.config` 是一样的，都是获取配置对象。`request.config` 则是 `FixtureRequest` 中的属性，返回 `_pytest.config.Config` (`pytest` 配置对象)，如下所示：

```python
class FixtureRequest(abc.ABC):
    """The type of the ``request`` fixture.
        
    A request object gives access to the requesting test context and has a
    ``param`` attribute in case the fixture is parametrized.
    """ 
    ...

    @property       
    def config(self) -> Config:
        """The pytest config object associated with this request."""
        return self._pyfuncitem.config  # type: ignore[no-any-return]
```

#### 7.2.3.1.2 主要功能

- **获取命令行参数**：可以检索传递给 `pytest` 命令行的参数值。
- **获取ini配置值**：可以访问位于 `pytest.ini`、`tox.ini` 或 `setup.cfg` 文件中指定的配置值。
- **获取插件配置**：可以访问通过插件或勾子（hook）设置的配置值。
- **获取测试根目录**：可以获取测试运行时的根目录路径（通常是项目的顶层目录）。
- **获取自定义配置项**：如果你为 `pytest` 定义了自己的命令行参数或配置，也可以通过 `pytestconfig` 获取到这些值。

#### 7.2.3.1.3 使用方法

##### 7.2.3.1.3.1 获取命令行参数

```python
# content of test_pytestconfig.py
def test_get_option_from_command(pytestconfig):
    # 访问命令行参数
    verbose = pytestconfig.getoption("verbose")
    print(f"Verbose level: {verbose}")

    # 验证和断言使用，通常在实际测试函数中
    assert verbose == 1  # 假设你期待的是 -v 选项
```

从命令行参数获取verbose，并断言是不是携带了一个'-v'选项，执行效果如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_pytestconfig.py::test_get_option_from_command
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_pytestconfig.py::test_get_option_from_command Verbose level: 1
PASSED

=============================== 1 passed in 0.00s =============================
root@Gavin:~/code/chapter1-7#
```

如果在pytest.ini文件中做例如下配置：

```shell
[pytest]
addopts =-vrs -p no:warnings
```

再次执行上述用例，执行效果如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_pytestconfig.py::test_get_option_from_command
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_pytestconfig.py::test_get_option_from_command Verbose level: 2
FAILED

============================== FAILURES ======================================
______________________________ test_get_option_from_command __________________

pytestconfig = <_pytest.config.Config object at 0x7f40a5212110>

    def test_get_option_from_command(pytestconfig):
        # 访问命令行参数
        verbose = pytestconfig.getoption("verbose")
        print(f"Verbose level: {verbose}")
    
        # 验证和断言使用，通常在实际测试函数中
>       assert verbose == 1  # 假设你期待的是 -v 选项
E       assert 2 == 1

test_pytestconfig.py:11: AssertionError
================================ 1 failed in 0.03s ============================
root@Gavin:~/code/chapter1-7#
```

这是因为`pytest.ini`中携带了一个`-v`参数，命令行也携带了一个`-v`参数，就存在两个`-v`参数了，断言处失败。

##### 7.2.3.1.3.2 从配置文件获取参数

在项目的根目录一般会放一个 `pytest.ini` 写一些配置参数：

```shell
[pytest]
log_cli = True
addopts =-vrs -p no:warnings
markers =
    slow: slow test case
    fast: fast test case
```

想读取 `pytest.ini` 里面的配置信息，可以用 `pytestconfig.getini()` 来获取，示例代码如下：

```python
# content of test_pytestconfig.py
def test_get_from_config(pytestconfig):
    # 获取测试配置
    print(pytestconfig.getini("markers"))
    
    # 访问ini配置文件中的值,需要事先配置pytest.ini文件中的addopts
    addopts = pytestconfig.getini("addopts")
    print(f"addopts option value from ini: {addopts}")
```

从`pytest.ini`文件中获取`markers` 和 `addopts` 配置信息，运行结果参考如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_pytestconfig.py::test_get_from_config
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_pytestconfig.py::test_get_from_config ['slow: slow test case', 'fast: fast test case', 'skip(reason=None): skip the given test function with an optional reason. Example: skip(reason="no way of currently testing this") skips the test.', "skipif(condition, ..., *, reason=...): skip the given test function if any of the conditions evaluate to True. Example: skipif(sys.platform == 'win32') skips the test if we are on the win32 platform. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-skipif", "xfail(condition, ..., *, reason=..., run=True, raises=None, strict=xfail_strict): mark the test function as an expected failure if any of the conditions evaluate to True. Optionally specify a reason for better reporting and run=False if you don't even want to execute the test function. If only specific exception(s) are expected, you can list them in raises, and if the test fails in other ways, it will be reported as a true failure. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-xfail", "parametrize(argnames, argvalues): call a test function multiple times passing in different arguments in turn. argvalues generally needs to be a list of values if argnames specifies only one name or a list of tuples of values if argnames specifies multiple names. Example: @parametrize('arg1', [1,2]) would lead to two calls of the decorated test function, one with arg1=1 and another with arg1=2.see https://docs.pytest.org/en/stable/how-to/parametrize.html for more info and examples.", 'usefixtures(fixturename1, fixturename2, ...): mark tests as needing all of the specified fixtures. see https://docs.pytest.org/en/stable/explanation/fixtures.html#usefixtures ', 'tryfirst: mark a hook implementation function such that the plugin machinery will try to call it first/as early as possible. DEPRECATED, use @pytest.hookimpl(tryfirst=True) instead.', 'trylast: mark a hook implementation function such that the plugin machinery will try to call it last/as late as possible. DEPRECATED, use @pytest.hookimpl(trylast=True) instead.']
addopts option value from ini: ['-vrs', '-p', 'no:warnings']
PASSED

================================ 1 passed in 0.00s ==============================
root@Gavin:~/code/chapter1-7#
```

##### 7.2.3.1.3.3 获取插件配置

在 `pytest` 中，要获取插件的配置，我们通常是在插件自身或 `conftest.py` 文件中定义一些可配置的选项，然后通过 `pytestconfig` fixture 来访问它们（通常通过 `pytest_addoption` 钩子函数实现）。下面会展示如何在一个 `pytest` 插件中定义配置项，以及如何在测试代码中使用 `pytestconfig` 获取这些配置值。主要用到两个方法：

* 使用 `pytestconfig.getoption` 来获取命令行参数。
* 使用 `pytestconfig.getini` 来获取 `ini` 文件中的配置项。

定义插件配置项

首先，你要在插件定义中使用 `pytest_addoption` 钩子函数来添加命令行参数或 `ini` 配置选项。

下面是一个示例，在 `conftest.py` 文件或独立的插件中添加配置选项：

```python
# contents of conftest.py 或者 plugin file
def pytest_addoption(parser):
    parser.addoption('--myoption', action='store', default='default', help='Custom option for my plugin')
    parser.addini('myconfig', 'My custom configuration option', type='linelist', default=[])
```

在这个例子中，我们添加了一个名为 `--myoption` 的命令行参数以及一个 `ini` 文件配置项 `myconfig`。

然后，在你的测试函数中，可以将 `pytestconfig` 作为参数，来访问你的插件配置：

```python
# test_myplugin.py
def test_plugin_option(pytestconfig):
    myoption_value = pytestconfig.getoption('myoption')
    print('The value of the command-line option --myoption:', myoption_value)

    myconfig_value = pytestconfig.getini('myconfig')
    print('The value of the ini file option myconfig:', myconfig_value)
```

通过这个测试函数，我们使用 `pytestconfig.getoption` 和 `pytestconfig.getini` 访问了我们之前定义的插件配置项。`getoption` 方法用于获取命令行参数，而 `getini` 用于获取 `ini` 配置。

运行带有插件配置选项的 `pytest`

当你执行 `pytest` 测试时，可以直接传递 `--myoption` 参数，并在 `pytest.ini` 文件中设置 `myconfig`：

```ini
# contents of pytest.ini
[pytest]
myconfig = 
    value1
    value2
    value3
```

命令行执行示例：

```bash
pytest --myoption some_value
```

在这个例子中，`test_plugin_option` 函数将输出 `some_value` 作为 `--myoption` 的值，同时从 `pytest.ini` 文件中读取 `myconfig` 配置项的值，输出应该是一个列表包含 "value1", "value2" 和 "value3"，执行效果参考如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v --myoption value1 test_myplugin.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_myplugin.py::test_plugin_option The value of the command-line option --myoption: value1
The value of the ini file option myconfig: ['value1', 'value2', 'value3']
PASSED

=============================== 1 passed in 0.00s =============================
root@Gavin:~/code/chapter1-7# pytest -s -v --myoption value2 test_myplugin.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_myplugin.py::test_plugin_option The value of the command-line option --myoption: value2
The value of the ini file option myconfig: ['value1', 'value2', 'value3']
PASSED

================================ 1 passed in 0.00s =============================
root@Gavin:~/code/chapter1-7#
```

这就是如何在 `pytest` 中定义插件配置，并使用 `pytestconfig` 在测试中获取这些配置的方法。这样做可以增加测试的灵活性，允许它们根据不同的配置和环境进行不同的逻辑处理。

接下来我们看另外两个示例，用于获取某个插件或全部插件信息，代码示例如下：

```python
# content of test_pytestconfig.py
def test_get_plugin(pytestconfig):
    myplugin = pytestconfig.pluginmanager.get_plugin('check')
    print(f"myplugin : {myplugin}")


def test_list_all_of_plugins(pytestconfig):
    # 获取pytest的插件列表
    plugins = pytestconfig.pluginmanager.list_plugin_distinfo()
    print(f"All of plugins : {plugins}")
```

两个测试用例，`test_get_plugin`获取`pytest_check`的插件信息，`test_list_all_of_plugins`则获取当前`pytest`下的所有插件信息，运行效果参考如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_pytestconfig.py::test_get_plugin test_pytestconfig.py::test_list_all_of_plugins
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, metadata-3.0.0
collected 2 items

test_pytestconfig.py::test_get_plugin myplugin : <module 'pytest_check.plugin' from '/usr/local/lib/python3.11/dist-packages/pytest_check/plugin.py'>
PASSED
test_pytestconfig.py::test_list_all_of_plugins All of plugins : [(<module 'pytest_check.plugin' from '/usr/local/lib/python3.11/dist-packages/pytest_check/plugin.py'>, <pluggy._manager.DistFacade object at 0x7f8039e79b10>), (<module 'pytest_metadata.plugin' from '/usr/local/lib/python3.11/dist-packages/pytest_metadata/plugin.py'>, <pluggy._manager.DistFacade object at 0x7f8039e94210>)]
PASSED

================================= 2 passed in 0.00s ============================
root@Gavin:~/code/chapter1-7#
```

##### 7.2.3.1.3.4 获取自定义配置项

`pytestconfig.getoption` 获取命令行参数（对应的参数值），不但可以获取`pytest`框架中自带的命令行参数值，也可以获取用户注册的自定义参数值。

要理解`pytestconfig`如何工作，可以添加一个自定义的命令行选项，然后在测试中读取该选项。

```python
# content of conftes.tpy
import pytest

def pytest_addoption(parser):
    """  Add a command line option  """
    parser.addoption(
        "--env", default="test", choices=["dev", "test", "pre"], help="enviroment parameter")

@pytest.fixture
def get_option(pytestconfig):
    return pytestconfig.getoption("--env")
```

以 `pytest_addoption` 添加的命令行选项必须通过插件来实现，或者在项目顶层目录的`conftest.py`文件中完成。它所在的`conftest.py`不能处于测试子目录下。

上述是一个传入测试环境的命令行选项，接下来可以在测试用例中使用这些选项。

```python
# content of test_pytestconfig.py

def test_option(pytestconfig):
    print('the current environment is:', pytestconfig.getoption('--env')
```

由于前面的 `pytest_addoption` 中定义的`env`的默认参数是test，所以通过 `pytestconfig.getoption` 获取到的`env`的值就是test；如果传递了其他的参数值（只能是choices=["dev", "test", "pre"]中的三选一）则获取到对应的传参。执行效果如下：

不指定'--env'参数，使用默认值：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_pytestconfig.py
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_pytestconfig.py::test_option the current environment is: test
PASSED

=============================== 1 passed in 0.00s =============================
root@Gavin:~/code/chapter1-7#
```

指定""--env"参数，携带参数值"pre"：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_pytestconfig.py --env=pre
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, metadata-3.0.0
collected 1 item

test_pytestconfig.py::test_option the current environment is: pre
PASSED

================================ 1 passed in 0.00s ============================
root@Gavin:~/code/chapter1-7#
```


##### 7.2.3.1.3.5 获取测试跟目录

获取测试根目录通常用于查找测试数据文件、配置文件或者为了根据项目结构进行相对定位。这个根目录通常是包含 `pyproject.toml`, `pytest.ini`, `tox.ini` 或者 `setup.py` 文件的目录，`pytest` 会将其视作测试的跟目录。

**用途与场景：**

- **加载测试数据文件**：在测试中可能需要加载一些数据文件，如 JSON、XML 或 CSV 文件，这些文件通常放在一个固定的目录下，通过跟目录可以构建出正确的文件路径。
- **配置文件定位**：有时候我们会在项目的根目录下放置一些配置文件，测试时需要从这些文件中读取配置信息。
- **目录结构依赖**：对于可能根据项目目录结构有依赖的测试，知道根目录的位置能够帮助测试正确地定位其他模块或文件。

**代码示例：**

获取测试跟目录的操作很简单，可以使用 `pytestconfig` fixture 的 `rootpath` 属性或者`rootdir`属性来获得项目的根目录作为一个 `pathlib.Path` 对象。

```python
# content of test_pytestconfig.py
def test_get_root_dir(pytestconfig):
    # 获取测试根目录路径
    root_dir = pytestconfig.rootdir
    print(f"Root directory of the tests: {root_dir}")


def test_root_dir(pytestconfig):
    rootdir = pytestconfig.rootpath
    print(f"The root directory is: {rootdir}")
    # 如果需要的话，可以根据这个根目录进行进一步的文件操作
    # 例如，打开一个在根目录下的文件
    filename = rootdir.joinpath("some_data_file.json")

    with open(filename, "r") as file:
        # 对文件进行相应的操作
        pass
```

其执行效果如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_pytestconfig.py::test_root_dir test_pytestconfig.py::test_get_root_dir
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, metadata-3.0.0
collected 2 items

test_pytestconfig.py::test_root_dir The root directory is: /root/code
PASSED
test_pytestconfig.py::test_get_root_dir Root directory of the tests: /root/code
PASSED

=============================== 2 passed in 0.01s =============================
root@Gavin:~/code/chapter1-7#
```



在编写 `pytest` 插件时，`pytestconfig` 尤其有用，因为插件可以通过它访问用户提供的配置、选项和其他有用的测试运行信息。

使用 `pytestconfig` 允许你编写更灵活的测试，它可以根据环境设置或者用户提供配置来适当更改其行为。然而，依赖于全局状态的过度使用可能会导致测试之间的耦合，这是需要谨慎考虑的事情。

### 7.2.3.2 recwarn

`pytest` 的内置 `recwarn` fixture 允许你在测试过程中记录和检查 python 警告，它能帮助你确保你的代码在特定条件下正常发出警告，或者如果你做出了代码更改以防止某些警告，你可以验证这些警告不再发生。

#### 7.2.3.2.1 使用场景

* **验证特定警告的发生**：确保某个函数或方法在给定条件下正确发出了预期的警告。
* **验证警告的细节**：检查警告的信息，验证它包含正确的消息文本、分类或来源。
* **测试警告的清除**：测试过程结束后没有剩余警告，确保随后的测试不会受它们的干扰。

#### 7.2.3.2.2 代码示例

```python
# content of test_recwarn.py
import pytest
import warnings

# 假设我们有一个函数，该函数将发出一个即将弃用的功能警告。
def will_warn():
    warnings.warn("deprecated", DeprecationWarning)

# 测试使用 recwarn 来捕捉发出的警告
def test_deprecation_warning(recwarn):
    # 调用可能发出警告的函数
    will_warn()

    # 验证是否有警告被捕捉
    assert len(recwarn) == 1

    # 获取警告信息，recwarn.list 包含所有被捕捉的警告
    warn = recwarn.pop(DeprecationWarning)
    
    # 验证警告信息和警告类型
    assert issubclass(warn.category, DeprecationWarning)
    assert "deprecated" in str(warn.message)

# 测试使用 recwarn 确认没有警告被发出
def test_no_warnings(recwarn):
    # 假如有一个不发出警告的函数调用
    # no_warnings()

    # 确认 recwarn 没有捕捉到警告
    assert len(recwarn) == 0
    
# 可以自定义测试来判断警告的特定行为
def test_specific_behavior_for_warning(recwarn):
    # 假设有一个特定的行为会导致警告
    # specific_behavior()

    # 循环通过捕获的警告并进行更详细的检查
    for warning in recwarn.list:
        if issubclass(warning.category, UserWarning) and "specific" in str(warning.message):
            assert "specific" in str(warning.message)
            break
    else:
        pytest.fail("UserWarning with 'specific' not found")
```

在上面的第一个测试函数 `test_deprecation_warning` 中，我们测试了函数 `will_warn()` 是否会发出 `DeprecationWarning`，我们用 `recwarn` fixture 来捕获警告，然后我们对它进行检验，以确保警告的分类和信息是正确的。

在第二个测试函数 `test_no_warnings` 中，我们验证在某个操作后没有警告发出。我们期望 `recwarn` 的长度为 0，这意味着没有警告被记录。

在第三个测试函数 `test_specific_behavior_for_warning` 中，我们演示了如何遍历所有捕获的警告，并且寻找特定类型和信息的警告。

执行效果参考如下：

```shell
root@Gavin:~/code# pytest -s -v chapter1-7/test_recwarn.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, html-4.1.1, metadata-3.0.0
collected 3 items

chapter1-7/test_recwarn.py::test_deprecation_warning PASSED
chapter1-7/test_recwarn.py::test_no_warnings PASSED
chapter1-7/test_recwarn.py::test_specific_behavior_for_warning FAILED

================================ FAILURES =====================================
______________________ test_specific_behavior_for_warning _____________________

recwarn = WarningsRecorder(record=True)

    def test_specific_behavior_for_warning(recwarn):
        # 假设有一个特定的行为会导致警告
        # specific_behavior()
    
        # 循环通过捕获的警告并进行更详细的检查
        for warning in recwarn.list:
            if issubclass(warning.category, UserWarning) and "specific" in str(warning.message):
                assert "specific" in str(warning.message)
                break
        else:
>           pytest.fail("UserWarning with 'specific' not found")
E           Failed: UserWarning with 'specific' not found

chapter1-7/test_recwarn.py:42: Failed
=========================== 1 failed, 2 passed in 0.04s ======================
root@Gavin:~/code#
```

使用这个 fixture，你可以确保代码的警告行为符合预期，这是履行良好的维护和用户沟通实践的一部分。

## 7.2.4 记录测试套件属性

### 7.2.4.1 request

当我们在 `pytest` 中编写测试代码时，经常会遇到需要获取当前测试用例的详细信息或上下文的情况。`pytest` 提供了一个强大的内置`fixture`—`request`来应对这样的需求，它为测试函数提供了一个 `FixtureRequest` 类型的对象，通过`request.config` 获取配置对象，可以访问很多关于当前测试函数、类、模块或会话的详细请求信息。在本文中，我们将深入探讨 `request` fixture 的能力，并且通过实际代码示例来展示其在不同场景下的应用。

#### 7.2.4.1.1 request提供的功能

* **获取测试函数/用例的标记/标识**：访问测试函数/用例上的自定义标记/标识，并根据这些标记/标识改变测试行为。
* **访问自定义标记**：可以检索用 `pytest.mark` 设置的标记。
* **访问参数化数据**：对于参数化的测试，可以获取当前测试用例的参数。
* **动态资源管理**：根据测试需求动态地设置和清理资源。
* **访问其他 fixture**：获取其他 fixture 的参数信息。
* **实现复杂的依赖注入逻辑**：基于测试的不同属性（如标记、参数值）条件性地设置 fixture。
* **资源清理**：注册最终化函数以在测试结束后执行资源清理。
* **访问 CLI 参数**：可从 `pytest` 命令行参数获取信息。
* **测试节点（item）和会话（session）信息**：获取更多关于测试集合和测试会话的信息。

#### 7.2.4.1.2 使用request的场景

##### 7.2.4.1.2.1 获取测试函数/用例的标记/标识

```python
# content of test_request.py
# 使用pytest.mark来定义标记
@pytest.mark.my_marker_name
def test_get_mark_info1(request):
    # 通过request访问该测试的标记
    marker = request.node.get_closest_marker("my_marker_name")
    if marker:
        # 如果标记存在，执行相应的逻辑
        pass

@pytest.mark.category("slow")
def test_get_mark_info2(request):
    if request.node.get_closest_marker("category").args[0] == "slow":
        # 对于 "slow" 类别的测试，可能需要特殊处理
        pass
```

##### 7.2.4.1.2.2 访问参数化数据

```python
# content of test_request.py
# 参数化测试函数
@pytest.mark.parametrize("value,expected", [(1, 2), (2, 3)])
def test_add_one(value, expected, request):
    # 通过request.node.callspec.params访问参数化的值，并将其赋值给param变量
    param = request.node.callspec.params
    assert value + 1 == expected

# 创建了一个参数化的fixture param_fixture，它会对每一对参数进行迭代，
# 并在每次测试中提供一对参数。然后，这些参数在test_with_fixture函数中被使用。
# 这种方法适用于需要在fixture级别处理参数化数据的场景。
@pytest.fixture(params=[("3+5", 8), ("2+4", 6), ("6*9", 54)])
def param_fixture(request):
    return request.param
    
def test_with_fixture(param_fixture):
    input, expected = param_fixture
    assert eval(input) == expected
    
@pytest.mark.parametrize("number,result", [(1, 2), (2, 4)])
def test_doubling(number, result, request):
    assert number * 2 == result
    # 对参数化的测试进行断言，同时可以访问当前的参数化数据
    print(request.node.callspec.params)  # 输出当前的测试参数，例如 (1, 2)
```

##### 7.2.4.1.2.3 动态资源管理

```python
# content of test_request.py
# 创建一个fixture，它将使用request对象来关闭文件资源
@pytest.fixture
def open_file(request):
    # 创建并打开一个临时文件
    temp_file = open('temp.txt', 'w+')
    
    # 定义一个内部函数用于关闭文件资源
    def close_file():
        temp_file.close()
        os.remove('temp.txt')

    # 添加一个finalizer，它在测试结束后被调用
    request.addfinalizer(close_file)

    # 返回打开的文件对象，供测试用例使用
    return temp_file

# 测试用例：写入内容并检查是否写入成功
def test_write_to_file(open_file):
    open_file.write('Hello pytest!')
    open_file.flush()  # 确保内容写入到文件中
    open_file.seek(0)  # 移动到文件的开头，以便读取内容
    content = open_file.read()
    assert content == 'Hello pytest!'

# 测试用例：检查当打开文件时，文件是否存在
def test_file_exists(open_file):
    assert not open_file.closed
```

##### 7.2.41.2.4 获取 fixture 的名称和参数

```python
# content of test_request.py
@pytest.fixture(scope="function")
def get_fixture_name_param(request):
    print(f"Fixture name: {request.fixturename}")
    print(f"Fixture params: {request.param}")

def test_one(get_fixture_name_param):
    pass

def test_two(get_fixture_name_param):
    pass
```

##### 7.2.4.1.2.5 访问其他 fixture

```python
# content of test_request.py
@pytest.fixture
def other_fixture():
    return "data"

# 在fixture中使用request来访问其他fixture
@pytest.fixture
def combined_fixture(request):
    other_data = request.getfixturevalue("other_fixture")
    return f"combined with {other_data}"

def test_combined(combined_fixture):
    assert combined_fixture == "combined with data"
```

##### 7.2.4.1.2.6 获取并触发其他 fixtures

```python
# content of test_request.py
@pytest.fixture
def setup_data():
    return {'data': 1}

@pytest.fixture
def more_setup(setup_data, request):
    setup_data.update({'extra': request.getfixturevalue('setup_data')['data'] + 1})
    return setup_data

def test_data(request):
    assert request.getfixturevalue('more_setup')['extra'] == 2
```

##### 7.2.4.1.2.7 实现复杂的依赖注入逻辑

```python
# content of test_request.py
@pytest.fixture(params=[".txt", ".md", ".json"])
def file_with_different_types(request):
    # 根据不同的参数创建不同类型的文件名
    filename = f"test_file{request.param}"

    # 创建并打开文件
    with open(filename, 'w') as f:
        f.write(f"This is a {request.param} file.")

    # 传递文件名给测试
    yield filename

    # 清理：测试结束后删除文件
    os.remove(filename)

# 测试用例，确保文件创建并且内容正确
def test_file_content(file_with_different_types):
    # 检查文件是否存在
    assert os.path.exists(file_with_different_types)
    # 读取文件内容
    with open(file_with_different_types, 'r') as f:
        content = f.read()
    # 检查内容是否正确
    expected_content = f"This is a {os.path.splitext(file_with_different_types)[1]} file."
    assert content == expected_content

# 测试用例，确保文件后缀名匹配
def test_file_extension(file_with_different_types):
    # 检查文件后缀名
    assert any(file_with_different_types.endswith(ext) for ext in [".txt", ".md", ".json"])
```

在这个示例中，`file_with_different_types` 是一个参数化fixture，它会运行三次，每次生成不同类型的文件（`.txt`, `.md`, `.json`）。这个fixture使用`request.param`来获取当前的参数值。

`yield`在fixture中用于提供一个对象给测试用例，同时保持上下文，以便在测试执行结束后执行后续的代码。在这种情况下，我们在测试结束后删除了创建的文件，以清理测试环境。

`test_file_content` 测试用例检查文件是否存在，并且内容是否正确。`test_file_extension` 测试用例确保文件的扩展名是预期的类型之一。

##### 7.2.4.1.2.8 获取正在运行的测试函数

```python
# content of test_request.py
def test_get_test_name(request):
    # 打印当前测试用例函数名称
    print(request.function.__name__)  # 输出 'test_get_test_name'

@pytest.fixture(scope="function")
def by_fixture_get_case_name(request):
    print(f"Running test: {request.function.__name__}")

def test_one(by_fixture_get_case_name):
    pass

def test_two(by_fixture_get_case_name):
    pass
```

##### 7.2.4.1.2.9 获取正在运行测试的测试类

```python
# content of test_request.py
@pytest.fixture(scope="function")
def by_fixture_get_cls_name(request):
    print(f"Test class: {request.cls.__name__}")

class TestCase:
    def test_one(self, by_fixture_get_cls_name):
        pass

    def test_two(self, by_fixture_get_cls_name):
        pass
```

##### 7.2.4.1.2.10 获取 fixture 的 scope

```python
# content of test_request.py
@pytest.fixture(scope="function")
def get_fixture_scope(request):
    print(f"Fixture scope: {request.scope}")

def test_one(get_fixture_scope):
    pass

def test_two(get_fixture_scope):
    pass
```

##### 7.2.4.1.2.11 注册清理函数

```python
# content of test_request.py
def file_open(request):
    """打开一个文件并返回文件对象"""
    filename = request.param  # 假设文件名通过param传递
    print(f"Opening file {filename}")
    return open(filename, 'w')  # 以写入模式打开文件
    
def release_resource(resource):
    """释放资源，这里指的是关闭文件"""
    resource.close()
    print(f"File {resource.name} closed")
    
@pytest.fixture(params=["file1.txt", "file2.txt"])
def register_clear_fixture(request):
    resource = file_open(request)
    # 注册清理函数以确保资源被释放
    request.addfinalizer(lambda: release_resource(resource))
    return resource
    
def test_my_fixture(register_clear_fixture):
    # 测试可以使用资源 register_clear_fixture
    # 这里可以进行一些写入文件的操作
    register_clear_fixture.write("Hello, World!")
    # 文件会在测试结束后自动关闭
"test_request.py" 227L, 7657B written 
```

在这个例子中，`file_open`函数使用`request.param`来确定要打开哪个文件。我们使用`pytest.fixture`装饰器的`params`参数来为fixture提供参数化输入，这意味着`test_my_fixture`会对每个参数执行一次。

注意，`file_open`函数假设文件名是通过`request.param`传递的，这就意味着在使用fixture时需要通过参数化来提供文件名。在这个例子中，我们在fixture装饰器中直接提供了两个文件名`["file1.txt", "file2.txt"]`，所以测试将会为这两个文件分别运行一次。

上述用例执行效果：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_request.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, html-4.1.1, metadata-3.0.0
collecting ... /root/code/chapter1-7/test_request.py:6: PytestUnknownMarkWarning: Unknown pytest.mark.my_marker_name - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
  @pytest.mark.my_marker_name
/root/code/chapter1-7/test_request.py:14: PytestUnknownMarkWarning: Unknown pytest.mark.category - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
  @pytest.mark.category("slow")
collected 26 items

test_request.py::test_get_mark_info1 PASSED
test_request.py::test_get_mark_info2 PASSED
test_request.py::test_add_one[1-2] PASSED
test_request.py::test_add_one[2-3] PASSED
test_request.py::test_with_fixture[param_fixture0] PASSED
test_request.py::test_with_fixture[param_fixture1] PASSED
test_request.py::test_with_fixture[param_fixture2] PASSED
test_request.py::test_doubling[1-2] {'number': 1, 'result': 2}
PASSED
test_request.py::test_doubling[2-4] {'number': 2, 'result': 4}
PASSED
test_request.py::test_write_to_file PASSED
test_request.py::test_file_exists PASSED
test_request.py::test_one Fixture scope: function
PASSED
test_request.py::test_two Fixture scope: function
PASSED
test_request.py::test_combined PASSED
test_request.py::test_data PASSED
test_request.py::test_file_content[.txt] PASSED
test_request.py::test_file_content[.md] PASSED
test_request.py::test_file_content[.json] PASSED
test_request.py::test_file_extension[.txt] PASSED
test_request.py::test_file_extension[.md] PASSED
test_request.py::test_file_extension[.json] PASSED
test_request.py::test_get_test_name test_get_test_name
PASSED
test_request.py::TestCase::test_one Test class: TestCase
PASSED
test_request.py::TestCase::test_two Test class: TestCase
PASSED
test_request.py::test_my_fixture[file1.txt] Opening file file1.txt
PASSEDFile file1.txt closed

test_request.py::test_my_fixture[file2.txt] Opening file file2.txt
PASSEDFile file2.txt closed


============================= 26 passed in 0.03s ==========================
root@Gavin:~/code/chapter1-7#
```



以上就是 `request` fixture 的一些常见使用场景和示例。通过使用 `request` fixture，你可以使你的测试更加灵活，适应各种复杂场景，并确保资源在测试结束时得到正确的管理。这是编写健壮测试的关键工具之一。

### 7.2.4.2 record_property

`record_property` 允许你在测试期间添加额外的属性到测试报告中，这些属性稍后可以用于测试报告或在某些插件中进行进一步处理。使用 `record_property` 函数，你可以捕获和记录与特定测试相关的附加信息，这对于调试、报告或者由测试生成的文档来说可能非常有用。

#### 7.2.4.2.1 使用场景

* **记录测试元数据**：当你需要为特定测试存储额外信息，比如测试数据版本、测试参数等。
* **改善测试报告**：通过添加更多的上下文来使得测试报告更加详细和有用。
* **在测试报告中包含动态数据**：有些测试可能会生成或计算出对了解测试结果有帮助的值，使用 `record_property` 可以将它们包含在测试报告中。
* **与其他插件集成**：一些 `pytest` 插件可能使用这些额外的属性，例如 `pytest-html` 可以在 HTML 报告中显示这些属性。

#### 7.2.4.2.2 代码示例

假设我们正在测试一个数学计算函数，并且我们希望记录下某些输入参数以便更好地理解测试结果。下面的代码示例说明了如何使用 `record_property`。

```python
# content of test_record_property.py
import pytest


def calculate_square(value):
    return value * value


def test_square(record_property):
    value = 4
    expected = 16
    result = calculate_square(value)

    # 记录测试属性
    record_property("input", value)
    record_property("expected_result", expected)

    assert result == expected


def test_record_description(record_property):
    # 设置一个描述属性。
    record_property("description", "A detailed description of the test case.")
    # ... 测试逻辑 ...
    assert 1 == 1


def test_record_some_properties_1(record_property):
    # 假设这是测试用例中的一些数据
    input_data = "some input"
    expected_result = "expected outcome"
    actual_result = "actual outcome"

    # 使用 record_property 记录这些数据
    record_property("input_data", input_data)
    record_property("expected_result", expected_result)
    record_property("actual_result", actual_result)

    # 断言实际结果是否符合期望结果
    assert expected_result == actual_result


def test_record_some_properties_2(record_property):
    # 假设的测试逻辑
    result = 42  # 一个假设的测试结果

    # 记录额外的属性
    record_property("example_property", "example_value")
    record_property("result", result)

    # 断言（仅示例）
    assert result == 42
```

在上述示例中，`record_property` fixture 被用来记录传入 `calculate_square` 函数的输入值和预期的结果。这些属性被添加到测试的结果中，并且可以在生成的测试报告中看到。

#### 7.2.4.2.3 在报告中显示

使用 `pytest-html` 插件来生成 HTML 测试报告（如果没安装，请执行`pip install pytest-html`命令进行安装），一旦你运行了测试并生成了 HTML 报告，`record_property` 添加的属性应该会出现在 HTML 报告的 `Properties` 部分。但是，请注意，默认情况下，`pytest-html` 并不显示这些属性。你需要添加额外的钩子（hook）到你的 `conftest.py` 文件中，以确保属性信息被添加到 HTML 报告中。

以下是包含在 `conftest.py` 中钩子和示例测试函数的完整示例。

首先，在你的测试目录中创建 `conftest.py`，如果还没有的话：

```python
# content of conftest.py
import pytest
from pytest_html import extras

# 捕获测试用例的属性并在报告中显示
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # 在测试阶段结束时捕获并处理属性
    if call.when == 'call' or call.when == 'teardown':
        if hasattr(item, 'user_properties'):
            report.extra = getattr(report, 'extra', [])
            report.user_properties = item.user_properties
            print(report.user_properties)
            # 将属性添加到报告的额外信息部分
            for name, value in item.user_properties:
                report.extra.append(extras.text(f'{name}: {value}'))
        else:
            print("has no user_properties")
    else:
        print(call.when)

# 修改 HTML 报告的表头，添加一个属性列
@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_header(cells):
    cells.insert(1, 'Properties')

# 修改 HTML 报告的每一行，显示相应的属性
@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_row(report, cells):
    properties = getattr(report, 'user_properties', [])
    properties_str = ', '.join([f'{name}: {value}' for name, value in properties])
    cells.insert(1, properties_str or 'N/A')

# 选项：如果你想要在 HTML 报告的摘要部分以单独的区块显示属性
def pytest_html_results_summary(prefix, summary, postfix):
    # 此处可以根据需要添加自定义的 HTML 代码来格式化和显示属性
    pass

```

生成`html`报告，运行效果如下：

```shell
root@Gavin:~/code# pytest -s -v chapter1-7/test_record_property.py  --html=report/record_property.html --self-contained-html
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, html-4.1.1, metadata-3.0.0
collected 4 items

chapter1-7/test_record_property.py::test_square PASSED
chapter1-7/test_record_property.py::test_record_description PASSED
chapter1-7/test_record_property.py::test_record_some_properties_1 FAILED
chapter1-7/test_record_property.py::test_record_some_properties_2 PASSED

============================== FAILURES =======================================
______________________________ test_record_some_properties_1 __________________

record_property = <function record_property.<locals>.append_property at 0x7f829dff3100>

    def test_record_some_properties_1(record_property):
        # 假设这是测试用例中的一些数据
        input_data = "some input"
        expected_result = "expected outcome"
        actual_result = "actual outcome"
    
        # 使用 record_property 记录这些数据
        record_property("input_data", input_data)
        record_property("expected_result", expected_result)
        record_property("actual_result", actual_result)
    
        # 断言实际结果是否符合期望结果
>       assert expected_result == actual_result
E       AssertionError: assert 'expected outcome' == 'actual outcome'
E         - actual outcome
E         + expected outcome

chapter1-7/test_record_property.py:39: AssertionError
------------------------------------------------------------------------------------- Generated html report: file:///root/code/report/record_property.html --------------------------------------------------------------------------------------
======================== 1 failed, 3 passed in 0.04s ========================
root@Gavin:~/code#
```

这样，当你查看测试报告时，你可以看到更多关于每个测试的上下文信息，如下图所示：

<img class="shadow" src="/img/in-post/pytest-html-record-property.png" width="800">

**请注意：**

- `record_property` 只在测试函数或者类的方法中使用，而不是在 fixture 中。
- `record_property` 适合记录简单的文本信息，而不适合大型数据，如图像或大型数据集/大数据。
- `record_property` 只能用于报告字符串值或可以被轻松转换为字符串的值。

### 7.2.4.3 record_testsuite_property

`record_testsuite_property` 用于在测试套件的层面上记录属性，这些属性可以在生成的测试报告中查看。与 `record_property` 相比，`record_testsuite_property` 记录的是跨越整个测试会话的信息，而不是单个测试用例的信息。

#### 7.2.4.3.1 使用场景

* **全局测试配置**：如果你想要记录全局的测试配置或环境设置，可以使用 `record_testsuite_property`。
* **统计信息**：在整个测试时段内统计信息，例如，测试次数、成功率或失败率、运行时间，测试套件版本等。
* **跨测试共享信息**：比如说，当测试套件中的某个条件影响整个测试过程时，可以使用这个 fixture 记录这些信息。
* **报告自定义信息**：在生产测试报告时可能需要出现的自定义信息，例如为CI/CD流程添加标签，获取构建版本号，构建号，测试环境的描述；或者测试执行中创建的资源数量，API调用次数，或者其他自定义指标等。

#### 7.2.4.3.2 代码示例

假设我们想要记录测试用例自定义的属性信息，诸如版本，环境，测试类等信息，使用 `record_testsuite_property`，可以做到这一点。以下是一个`pytest`代码示例：

```python
def test_example_one(record_testsuite_property):
    # 假设这是测试套件级别的一个属性
    record_testsuite_property("suite_name", "My Test Suite")
    assert True

def test_example_two():
    # 此测试用例不需要记录属性
    assert True
    
def test_example(record_testsuite_property):
    # 记录测试套件属性
    record_testsuite_property("version", "1.0.1")
    record_testsuite_property("environment", "staging")

    # ... 进行实际的测试操作
    assert True
```

#### 7.2.4.3.3 在报告中展示

与 `record_property` 类似，加入你使用了生成 HTML 报告的插件（如 `pytest-html`），这些记录的套装属性也会在报告中展示。这可以帮助团队成员理解测试套件的全局视角，并在有需要时进行进一步分析。

假设你使用了 `pytest-html` 这样的插件来生成 HTML 报告，那么通过 `record_testsuite_property` 记录的属性将会在 HTML 报告的 `Metadata` 部分展示出来。这提供了一种很方便的方式来传达关于整个测试执行环境和配置的信息给查看报告的利益相关者。

```python
# content of conftest.py
import pytest

# 测试套件属性存储结构，定义在全局以便其他hooks访问
testsuite_property_storage = {}

# pytest fixture 用于记录属性
@pytest.fixture(scope="session")
def record_testsuite_property(request):
    # 这个内部方法让测试用例能记录属性
    def add_property(key, value):
        testsuite_property_storage[key] = value
    return add_property

# 修改 HTML 报告的表头，添加一个属性列
@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_header(cells):
    # cells.insert(1, 'Properties')
    cells.insert(1, '<th>Custom Column</th>')

# 修改 HTML 报告的每一行，显示相应的属性
@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_row(report, cells):
    properties_cells = ', '.join([f'{key}: {value}' for key, value in testsuite_property_storage.items()])
    cells.insert(1, properties_cells or 'N/A')
```

执行效果如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_record_testsuite_property.py --html=../report/record_testsuite_property.html --self-contained-html
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: check-2.2.2, html-4.1.1, metadata-3.0.0
collected 3 items

test_record_testsuite_property.py::test_example_one PASSED
test_record_testsuite_property.py::test_example_two PASSED
test_record_testsuite_property.py::test_example PASSED

---------------------- Generated html report: file:///root/code/chapter1-7/../report/record_testsuite_property.html ------------------------
=============================== 3 passed in 0.01s ============================
root@Gavin:~/code/chapter1-7#
```

生成的HTML测试报告展示效果如下：

<img class="shadow" src="/img/in-post/pytest-html-record-testsuite-property.png" width="800">

## 7.2.5 临时目录相关

### 7.2.5.1 testdir

`testdir` 是一个用于测试的 `pytest` 内置 fixture，它使得编写针对`pytest`插件或`pytest`本身的功能的集成测试变得简单。此fixture为测试提供了一个临时的测试目录，其中包含了一些用于创建文件和运行`pytest`测试的便捷方法。`testdir` fixture 主要用在测试 `pytest` 插件时。但请注意：`testdir` fixture 已被 `pytest 6.2`版本中新引入的 `pytester` fixture 所取代（官方还保留着`testdir`代码与使用说明，但不推荐使用了），后者提供了更多的功能、改进和附加特性。建议使用新版本的 `pytest`下的 `pytester` fixture，故本文不再做赘述。

### 7.2.5.2 temp_path 和 temp_path_factory

`temp_path` 和 `temp_path_factory` 是 `pytest` 中用于文件和目录操作的内置 fixtures。这两个 fixtures 允许测试访问文件系统，并在测试结束时自动处理清理工作。

#### 7.2.5.2.1 使用场景

- **temp_path**:
  - 用于单个测试函数或类中，需要临时文件或目录时。
  - 实际测试代码不需要创建多个临时目录。

- **temp_path_factory**:
  - 用于需要在一个测试会话中创建多个独立临时目录的场景。
  - 实现测试特定的临时目录管理策略。
  - 当你需要在会话级别或模块级别控制临时目录时使用。

#### 7.2.5.2.2 代码示例

**temp_path 示例**:

```python
def test_with_temp_path(temp_path):
    # 创建一个临时文件
    temp_file = temp_path / "temp_file.txt"
    temp_file.write_text("Hello, World!")

    # 读取内容并断言
    assert temp_file.read_text() == "Hello, World!"
```

**temp_path_factory 示例**:

```python
# 使用 temp_path_factory 在会话级别创建临时目录
def test_with_temp_path_factory(request, temp_path_factory):
    # 动态创建一个新的临时目录
    temp_dir = temp_path_factory.mktemp("subdir") 

    # 在这个目录中创建文件
    temp_file = temp_dir / "temp_file.txt"
    temp_file.write_text("This is a temp file.")

    # 断言文件确实被创建
    assert temp_dir.is_dir()
    assert temp_file.is_file()
    assert temp_file.read_text() == "This is a temp file."
```

#### 7.2.5.2.3 temp_path 与 temp_path_factory 的区别

以下表格对比了 `temp_path` 和 `temp_path_factory`：

| 特性               | `temp_path`                                        | `temp_path_factory`                                          |
| ------------------ | -------------------------------------------------- | ------------------------------------------------------------ |
| 作用域             | 在每个测试函数/方法中自动生成                      | 需要显式调用来创建新的临时目录                               |
| 用法               | 作为参数传递给测试函数或类                         | 作为参数工厂传递给测试函数或类                               |
| 生命周期           | 在测试函数或类之前创建，在之后销毁                 | 在测试函数或类中显式创建，在之后显式销毁                     |
| 目录控制           | 自动控制                                           | 手动控制（通过 `mktemp` 方法）                               |
| 创建的临时目录数量 | 通常为每个测试一个临时目录                         | 可以创建任意多的临时目录                                     |
| 自动清理           | 测试完成后自动清理生成的临时文件和目录             | 测试完成后也会自动清理，但可以跨多个测试手动控制什么时候创建和清理资源 |
| 应用场景           | 简单情况，不需要多个临时文件/目录                  | 复杂情况或模块/会话级别控制，适合需要多个临时目录或精细控制临时资源生命周期的情景 |
| 返回值类型         | `pathlib.Path` 实例代表一个临时目录                | Factory，需要调用 `mktemp` 来创建目录                        |
| 优点               | 使用简单，在不需要显式创建和销毁临时目录时非常方便 | 提供了更多的灵活性，允许在测试函数或类中创建和销毁多个临时目录 |
|                    | 在不需要显式创建和销毁临时目录时可能会有性能开销   | 需要显式创建和销毁临时目录，可能会导致更复杂的测试代码       |

在实际应用中，如果你的测试函数只需要访问单个临时文件或目录，那么使用 `temp_path` 是便捷的。如果需要更复杂的控制或在一个会话中创建多个独立的临时目录，`temp_path_factory` 则是更好的选择。

### 7.2.5.3 tmpdir和tmpdir_factory

内置的`tmpdir`和`tmpdir_factory`负责在测试开始运行前创建临时文件和目录，并在测试结束后删除。这两个 fixtures 类似于 `temp_path` 和 `temp_path_factory`，但使用的是 `py.path.local` 对象而不是 `pathlib.Path`。

#### 7.2.5.3.1 tmpdir 的使用场景

* **单一测试作用域**: 当你需要在单一测试函数中创建临时文件或目录，并希望在测试结束后自动删除它们时，`tmpdir` 是一个好选择。
* **简单操作**: 对于相对简单的测试用例，不需要在多个测试中共享文件或目录，或者不需要在更大的作用域（类级别或模块级别）中处理临时文件。
* **隔离测试**: 希望确保每次测试都在干净的环境中运行，即每个测试函数都有自己的临时目录，以避免状态泄漏。

#### 7.2.5.3.2 tmpdir_factory 的使用场景

* **跨测试作用域**: 当测试需要在模块或会话级别共享临时目录时，`tmpdir_factory` 提供了更大的灵活性。
* **定制临时目录**: 如果需要对临时目录的创建有更多的控制，如指定目录名，控制创建时间或在单个测试会话中重用临时目录。
* **复杂测试需求**: 例如，在一组测试中需要对临时文件夹进行复杂的设置和清理策略，或者需要在不同的测试类和模块之间创建多个独立的临时环境。
* **大量或有特定要求的临时资源**: 在单个测试会话中创建和管理多个临时文件夹。例如，当一个测试会话涉及多个组件，且每个组件都需要其自己的临时存储空间。

#### 7.2.5.3.3 tempdir与tempdir_factory介绍

**tmpdir**

- 用于创建临时目录。
- 在测试函数开始时创建临时目录，并在测试函数结束时删除。
- 可以使用 `tmpdir` 作为参数传递给测试函数。
- 可以使用 `tmpdir.join()` 来创建临时文件和目录。
- 当测试函数抛出异常时，临时目录将不会被删除。

**tmpdir_factory**

- 用于创建临时目录工厂。
- 可以通过调用 `tmpdir_factory.mktemp()` 来创建临时目录。
- 可以使用 `tmpdir_factory.getbasetemp()` 来获取临时目录的根目录。
- 可以使用 `tmpdir_factory.listtempdirs()` 来列出所有临时目录。
- 当最后一个使用临时目录的测试函数结束时，临时目录将被删除。

简而言之：

* 如果测试代码要对文件进行读/写操作，那么可以使用`tmpdir`或`tmpdir_factory`来创建文件或目录。
* `tmpdir`适用于需要在单个测试中创建临时文件或目录，并且希望这些资源在测试结束后自动清理。
* `tmpdir_factory`适用于需要在一个测试会话中手动控制创建多个临时目录的场景。提供了在测试会话、模块、类或函数级别控制临时目录的生命周期的能力。
* `tmpdir`的作用范围是函数级别，`tmpdir_factory`的作用范围是会话级别。

#### 7.2.5.3.4 代码示例

```python
# content of test_tmpdir_factory.py
# 使用 tmpdir 创建临时目录
def test_tmpdir(tmpdir):
    # tmpdir already has a path name associated with it
    # join() extends the path to include a filename
    # the file is created when it's written to
    a_file = tmpdir.join('something.txt')

    # you can create directories
    a_sub_dir = tmpdir.mkdir('anything')

    # you can create files in directories (created when written)
    another_file = a_sub_dir.join('something_else.txt')

    # this write creates 'something.txt'
    a_file.write('contents may settle during shipping')

    # this write creates 'anything/something_else.txt'
    another_file.write('something different')

    # you can read the files as well
    assert a_file.read() == 'contents may settle during shipping'
    assert another_file.read() == 'something different'


def test_create_tmpdir(tmpdir):
    # Create a temporary Files
    tmpfile = tmpdir.join("test.txt")
    # Write date to temporary file
    tmpfile.write("Hello, world!")
    # Read from temporary file
    assert tmpfile.read() == "Hello, world!"


# 使用 tmpdir_factory 创建临时目录工厂
def test_tmpdir_factory(tmpdir_factory):
    # you should start with making a directory
    # a_dir acts like the object returned from the tmpdir fixture
    a_dir = tmpdir_factory.mktemp('mydir')

    # base_temp will be the parent dir of 'mydir'
    # you don't have to use getbasetemp()
    # using it here just to show that it's available
    base_temp = tmpdir_factory.getbasetemp()
    print('base:', base_temp)

    # the rest of this test looks the same as the 'test_tmpdir()'
    # example except I'm using a_dir instead of tmpdir

    a_file = a_dir.join('something.txt')
    a_sub_dir = a_dir.mkdir('anything')
    another_file = a_sub_dir.join('something_else.txt')

    a_file.write('contents may settle during shipping')
    another_file.write('something different')

    assert a_file.read() == 'contents may settle during shipping'
    assert another_file.read() == 'something different'


def test_create_tmpdir_factory(tmpdir_factory):
    # Create a temporary directory
    tmpdir = tmpdir_factory.mktemp("mytmp")
    # Create a temporary Files
    tmpfile = tmpdir.join("test.txt")
    # Write data to temporary file
    tmpfile.write("Hello, world!")
    # Read from the temporary file
    assert tmpfile.read() == "Hello, world!"
```

如上示例，`testdir`创建一临时目录，并在目录下创建文件，向文件中写入数据，最后读取数据并断言读取内容；`testdir_factory`创建父目录及其子目录，向目录及其子目录下文件写入内容并读取做断言，其执行效果参考如下：

```shell
root@Gavin:~/code/chapter1-7# pytest -s -v test_tmpdir_factory.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code
configfile: pytest.ini
collected 4 items

test_tmpdir_factory.py::test_tmpdir PASSED
test_tmpdir_factory.py::test_create_tmpdir PASSED
test_tmpdir_factory.py::test_tmpdir_factory base: /tmp/pytest-of-root/pytest-2
PASSED
test_tmpdir_factory.py::test_create_tmpdir_factory PASSED

============================== 4 passed in 0.02s ==============================
root@Gavin:~/code/chapter1-7#
```

执行后会在`/tmp/pytest-of-root`目录下产生临时目录，参考如下：

```shell
root@Gavin:/tmp/pytest-of-root# ll
total 20
drwx------  5 root root 4096 Dec 26 21:36 ./
drwxrwxrwt 16 root root 4096 Dec 26 21:36 ../
drwx------  5 root root 4096 Dec 26 21:35 pytest-0/
drwx------  6 root root 4096 Dec 26 21:36 pytest-1/
drwx------  6 root root 4096 Dec 26 21:36 pytest-2/
lrwxrwxrwx  1 root root   28 Dec 26 21:36 pytest-current -> /tmp/pytest-of-root/pytest-2/
root@Gavin:/tmp/pytest-of-root#
```

默认只保留3个临时目录，从会话0开始，再次执行，自动删除`pytest-0`，产生`pytest-3`目录：

```shell
root@Gavin:/tmp/pytest-of-root# ll
total 20
drwx------  5 root root 4096 Dec 26 21:43 ./
drwxrwxrwt 16 root root 4096 Dec 26 21:43 ../
drwx------  6 root root 4096 Dec 26 21:36 pytest-1/
drwx------  6 root root 4096 Dec 26 21:36 pytest-2/
drwx------  6 root root 4096 Dec 26 21:43 pytest-3/
lrwxrwxrwx  1 root root   28 Dec 26 21:43 pytest-current -> /tmp/pytest-of-root/pytest-3/
root@Gavin:/tmp/pytest-of-root#
```

#### 7.2.5.3.5 tmpdir和tmpdir_factory的区别

以下是 `tmpdir` 和 `tmpdir_factory` 特性的比较：


| 特性             | `tmpdir`                                          | `tmpdir_factory`                                             |
| ---------------- | ------------------------------------------------- | ------------------------------------------------------------ |
| **用途**         | 用于单个测试，提供独立的临时文件系统路径          | 用于多个测试，跨测试函数、类、模块或整个会话创建临时目录     |
| **创建时机**     | 每个测试函数自动创建                              | 手动调用 `mktemp` 方法创建临时目录                           |
| **创建数量**     | 默认每个测试函数一个                              | 可以创建任意数量的临时目录                                   |
| **清理机制**     | 测试结束时自动清理                                | 当最后一个使用临时目录的测试函数结束时删除，<br />但可控制临时目录的生命周期 |
| **目录控制**     | 隐藏目录控制细节                                  | 显式控制目录的创建位置和时间                                 |
| **复用目录**     | 不容易在多个测试中复用临时目录                    | 可以在多个测试中复用临时目录或跨会话复用                     |
| **API**          | 基于 `py.path.local` API，如 `join()` , `write()` | 同 `tmpdir`，基于 `py.path.local` API                        |
| **路径类型**     | 返回 `py.path.local` 对象                         | 返回 `py.path.local` 对象                                    |
| **适用场景示例** | 单个测试需要临时文件，如测试文件写入              | 需要在整个测试会话期间控制文件生命周期的复杂集成测试         |
| **测试隔离**     | 每个测试运行在隔离的临时目录                      | 多个测试可以共享相同的临时目录，如果需要                     |

`tmpdir` 和 `tmpdir_factory` 之间的主要区别在于它们创建临时目录的方式以及所返回的对象类型。`tmpdir` 直接为每个测试提供一个临时目录，而 `tmpdir_factory` 允许在测试会话中创建和管理多个临时目录。两者都使用 `py.path.local` 对象进行路径操作，这与 `temp_path` 和 `temp_path_factory` 使用的 `pathlib.Path` 对象不同。选择哪一个取决于你的具体需求和对 `py.path.local` 或 `pathlib.Path` 的偏好。



# 7.3 本章小结

在本章中，我们深入探讨了`pytest`内置`fixture`的功能和用法，并介绍了它在测试代码中的重要性。`pytest`内置`fixture`是`pytest`框架提供的一组预定义的`fixture`，它们为我们提供了方便且强大的功能，用于管理和共享资源、设置测试环境以及执行常见的测试操作。

`pytest`提供了一些常用的内置`fixture`，例如 `tmpdir`、`monkeypatch`、`caplog` 等，它们可以通过直接使用或者应用装饰器 `@pytest.mark.usefixtures` 在测试用例中使用。这些内置`fixture`为我们提供了一些常见的功能，如临时目录的创建、对全局变量的修改、日志捕获等。

同时，我们还介绍了一些常用的内置`fixture`和它们的用途。例如，`tmpdir` fixture可以创建临时目录，并在测试结束后自动清理；`monkeypatch` fixture可以在测试过程中修改全局变量和函数行为；`caplog` fixture可以捕获和分析日志输出等。这些内置fixture为我们提供了方便且可靠的方式来处理测试中的各种需求。

通过充分利用这些内置`fixture`，我们可以减少重复的代码编写，提高测试代码的可读性和可维护性。同时，还要注意`fixture`之间的依赖关系和执行顺序，以避免潜在的问题和错误。

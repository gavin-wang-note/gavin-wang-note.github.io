---
title: 测试用例多重校验之pytest_check源码解读
date: 2024-11-26 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-26.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 测试用例多重校验/检查点之pytest_check源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

上篇文章我们介绍了[pytest_assume](https://gavin-wang-note.github.io/2024/11/17/pytest_assume/)的多重校验，此次介绍另外一个功能类似的插件`pytest_check`，二者在实现上有一定的差异。

源码下载到本地解压后展示如下：

```shell
root@Gavin:~/pytest_plugin# cd pytest_check-2.3.1/
root@Gavin:~/pytest_plugin/pytest_check-2.3.1# ll
total 76
drwxr-xr-x 5 root root  4096 Jul  3 09:34 ./
drwxr-xr-x 9 root root  4096 Jul 13 14:05 ../
-rw-r--r-- 1 root root 10194 Jan 19 04:24 changelog.md
drwxr-xr-x 2 root root  4096 Jul  3 14:56 examples/
-rw-r--r-- 1 root root  1079 Jan 19 04:24 LICENSE.txt
-rw-r--r-- 1 root root 13382 Jan  1  1970 PKG-INFO
-rw-r--r-- 1 root root   693 Jan 19 04:24 pyproject.toml
-rw-r--r-- 1 root root 13007 Jan 19 04:24 README.md
drwxr-xr-x 3 root root  4096 Jul  3 09:34 src/
drwxr-xr-x 2 root root  4096 Jul  3 09:34 tests/
-rw-r--r-- 1 root root   868 Jan 19 04:24 tox.ini
root@Gavin:~/pytest_plugin/pytest_check-2.3.1# cd src
root@Gavin:~/pytest_plugin/pytest_check-2.3.1/src# ll
total 12
drwxr-xr-x 3 root root 4096 Jul  3 09:34 ./
drwxr-xr-x 5 root root 4096 Jul  3 09:34 ../
drwxr-xr-x 2 root root 4096 Jul  3 14:54 pytest_check/
root@Gavin:~/pytest_plugin/pytest_check-2.3.1/src# cd pytest_check/
root@Gavin:~/pytest_plugin/pytest_check-2.3.1/src/pytest_check# ll
total 44
drwxr-xr-x 2 root root 4096 Jul  3 14:54 ./
drwxr-xr-x 3 root root 4096 Jul  3 09:34 ../
-rw-r--r-- 1 root root 5299 Jan 19 04:24 check_functions.py
-rw-r--r-- 1 root root 1836 Jan 19 04:24 check_log.py
-rw-r--r-- 1 root root 3831 Jan 19 04:24 check_raises.py
-rw-r--r-- 1 root root 1669 Jan 19 04:24 context_manager.py
-rw-r--r-- 1 root root 1434 Jan 19 04:24 __init__.py
-rw-r--r-- 1 root root 4608 Jan 19 04:24 plugin.py
-rw-r--r-- 1 root root 3567 Jan 19 04:24 pseudo_traceback.py
root@Gavin:~/pytest_plugin/pytest_check-2.3.1/src/pytest_check# 
```

核心内容在`src`目录下：

* `check_functions.py` ： 提供一组自定义的断言函数，它们在断言失败时不会立即失败，而是提供了更灵活的错误处理方式。这些函数可以与 `pytest` 测试框架无缝集成，增强测试的可读性和灵活性。
* `check_log.py` ： 记录失败信息的核心。
* `check_raises.py` ： 检查预期的异常。
* `context_manager.py` ： 提供上下文管理器，捕获和记录测试中的断言错误。
* `__init__.py` ： 导入pytest_check使得被 `pytest` 测试框架使用。
* `plugin.py` ： 实现`pytest_check` 插件的核心功能，处理测试报告的生成。
* `pseudo_traceback.py` ： 生成更易于理解的追踪栈信息。

# 源码解读


## check_functions.py文件

它提供了额外的断言函数和功能来增强测试体验。

### 导入和初始化

```python
import functools
import pytest

from .check_log import log_failure

__all__ = [
    # 这里列出了所有将被导出的函数名称
]
```

这段代码导入了必要的模块，并定义了一个 `__all__` 列表，它包含了模块中所有要导出的函数名，使得这些函数可以在其他模块中直接使用 `from pytest_check import function_name` 的方式导入。

### check_func 装饰器

```python
def check_func(func):
    # 这个装饰器用来包装测试函数，记录测试结果和日志
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        __tracebackhide__ = True  # pytest 特性，用于隐藏内部的 traceback
        try:
            func(*args, **kwds)  # 调用原始函数
            return True
        except AssertionError as e:
            log_failure(e)  # 记录失败信息
            return False
    return wrapper
```

`check_func` 是一个装饰器工厂，它返回一个装饰器，这个装饰器会捕获在被装饰函数中抛出的 `AssertionError` 异常，并调用 `log_failure` 函数来记录日志。如果函数执行成功，返回 `True`。

### 断言函数

以下是一些自定义的断言函数示例，它们都遵循相似的模式：
- 使用 `__tracebackhide__` 来控制 traceback 的显示。
- 比较操作（例如 `a == b`）。
- 如果比较成功，返回 `True`。
- 如果比较失败，调用 `log_failure` 记录失败信息，并返回 `False`。

```python
def assert_equal(a, b, msg=""):
    assert a == b, msg  # 传统的断言

def equal(a, b, msg=""):
    if a == b:
        return True
    else:
        log_failure(f"check {a} == {b}", msg)
        return False

# 其他断言函数遵循类似的模式...
```

这些函数提供了与 `pytest` 内置断言不同的行为，尤其是在失败时不会立即抛出异常，而是记录失败信息并返回 `False`。

### 数学比较函数

`almost_equal` 和 `not_almost_equal` 函数使用了 `pytest.approx` 来比较两个浮点数是否在相对或绝对容差内近似相等。

### 范围检查函数

`between` 和 `between_equal` 函数检查一个值是否在两个其他值之间，可以指定是否包含边界。

### `fail` 函数

```python
def fail(msg):
    log_failure(msg)
```
`fail` 函数是一个简单的工具函数，用于在测试中主动记录一个失败信息。

## check_log.py文件

此文件是负责记录测试失败信息的核心组件。

### 变量定义

```python
should_use_color = False  # 决定是否在日志中使用颜色
COLOR_RED = "\x1b[31m"  # 红色的ANSI转义序列
COLOR_RESET = "\x1b[0m"  # 重置颜色的ANSI转义序列

_failures = []  # 存储失败信息的列表
_stop_on_fail = False  # 如果为True，则在第一个失败时停止测试

_default_max_fail = None  # 最大失败次数，默认无限制
_default_max_report = None  # 最大报告的失败次数，默认无限制
_default_max_tb = 1  # 最大记录的追踪栈深度，默认为1

_max_fail = _default_max_fail  # 当前最大失败次数
_max_report = _default_max_report  # 当前最大报告的失败次数
_max_tb = _default_max_tb  # 当前最大追踪栈深度
_num_failures = 0  # 当前失败次数计数
_fail_function = None  # 当记录失败时调用的函数，如果设置了的话

_showlocals = False  # 是否显示局部变量
```

这些变量控制了失败信息的记录、报告和展示方式。

### 函数定义

```python
def clear_failures():
    # 在每个测试函数开始时调用
    global 变量列表
    _failures = []  # 清空失败列表
    # 重置计数器和最大值到默认设置
```

`clear_failures` 函数在每个测试开始时被调用，用于重置失败信息记录的状态。

```python
def any_failures() -> bool:
    # 返回是否有任何失败发生
    return bool(get_failures())

def get_failures():
    # 返回失败信息列表
    return _failures
```

`any_failures` 和 `get_failures` 函数提供了查询当前失败状态的方法。

```python
def log_failure(msg="", check_str="", tb=None):
    # 记录失败信息的函数
    global _num_failures
    __tracebackhide__ = True  # pytest 特性，用于隐藏内部的 traceback
    _num_failures += 1  # 失败次数加一

    # 构造失败信息
    msg = str(msg).strip()
    if check_str:
        msg = f"{msg}: {check_str}"

    # 判断是否需要记录当前失败信息
    if (_max_report is None or _num_failures <= _max_report) and _num_failures <= _max_tb:
        pseudo_trace_str = _build_pseudo_trace_str(_showlocals, tb, should_use_color)
        msg = f"{msg}\n{pseudo_trace_str}"

    # 根据设置添加颜色和前缀
    if should_use_color:
        msg = f"{COLOR_RED}FAILURE: {COLOR_RESET}{msg}"
    else:
        msg = f"FAILURE: {msg}"
    _failures.append(msg)

    # 如果设置了回调函数，调用它
    if _fail_function:
        _fail_function(msg)

    # 检查是否达到了最大失败次数，并抛出异常
    if _max_fail and _num_failures >= _max_fail:
        assert_msg = f"pytest-check max fail of {_num_failures} reached"
        assert _num_failures < _max_fail, assert_msg

    # 如果设置在第一个失败时停止，断言失败
    if _stop_on_fail:
        assert False, "Stopping on first failure"
```

`log_failure` 函数是记录失败信息的核心，它接受一个消息 `msg`，一个可选的检查字符串 `check_str`，和一个追踪栈 `tb`。函数内部首先构造失败信息，然后根据配置决定是否记录当前失败。如果设置了最大失败次数 `_max_fail`，且已达到该次数，将抛出异常。如果设置了 `_stop_on_fail` 为 `True`，则在第一个失败时停止测试。

## check_raises.py 文件

`check_raises.py` 提供了一个 `raises` 函数和 `CheckRaisesContext` 类来检查预期的异常是否被抛出。

### 变量定义

```python
_stop_on_fail = False  # 如果为True，在第一个失败时停止测试
```

### raises 函数

```python
def raises(expected_exception, *args, **kwargs):
```

`raises` 函数可以作为上下文管理器或函数使用，用于检查给定的可调用或上下文是否抛出了指定类型的异常。函数接受以下参数：

- `expected_exception`：期望抛出的异常类型。
- `*args` 和 `**kwargs`：传递给可调用对象的参数和关键字参数。

函数的主体实现了以下逻辑：

1. 检查 `expected_exception` 是否为类型或元组，包含多个异常类型。
2. 断言所有期望的异常都是有效的类型或基类。
3. 从 `kwargs` 中提取 `msg` 并使用它作为日志消息。
4. 如果没有提供可调用对象，返回一个 `CheckRaisesContext` 实例作为上下文管理器。
5. 如果提供了可调用对象，使用 `CheckRaisesContext` 作为上下文管理器执行该函数。

### CheckRaisesContext 类

```python
class CheckRaisesContext:
```

`CheckRaisesContext` 类是一个辅助上下文管理器，用于参数化异常类型。它实现了以下方法：

- `__init__`：初始化实例，接收期望的异常类型和消息。
- `__enter__`：进入上下文管理器，返回自身。
- `__exit__`：退出上下文管理器，处理异常。

`__exit__` 方法的逻辑：

1. 如果捕获到的异常类型 `exc_type` 是期望的异常类型之一，返回 `True`，这会阻止异常向外传播。
2. 如果 `_stop_on_fail` 为 `False`，则记录失败并返回 `True`，允许测试继续执行。
3. 如果 `_stop_on_fail` 为 `True`，则不记录失败，允许异常向外传播，导致测试停止。

## context_manager.py

`context_manager.py` 定义了一个 `CheckContextManager` 类，它是 `pytest_check` 插件的核心上下文管理器，提供了灵活的错误检查和记录功能。

### 类变量

```python
_stop_on_fail = False  # 如果为True，在第一个失败时停止测试
```

### CheckContextManager 类

```python
class CheckContextManager:
```

`CheckContextManager` 类是一个上下文管理器，用于封装测试断言的逻辑。

### 初始化方法

```python
    def __init__(self):
        self.msg = None
```

`__init__` 方法初始化上下文管理器，设置一个 `msg` 属性来存储自定义消息。

### 进入上下文方法

```python
    def __enter__(self):
        return self
```

`__enter__` 方法在进入上下文时被调用，返回上下文管理器实例本身。

### 退出上下文方法

```python
    def __exit__(self, exc_type, exc_val, exc_tb):
```

`__exit__` 方法在退出上下文时被调用，接收异常类型、值和追踪栈作为参数。它实现了以下逻辑：

- 如果捕获到的异常是 `AssertionError` 的子类，并且 `_stop_on_fail` 为 `True`，则不记录消息，允许异常传播。
- 如果 `_stop_on_fail` 为 `False`，则记录异常值和消息（如果有），并返回 `True` 以阻止异常传播。

### 调用方法

```python
    def __call__(self, msg=None):
```
`__call__` 方法允许上下文管理器像函数一样被调用，设置自定义消息并返回实例本身。


### 设置方法

```python
    def set_no_tb(self):
        # 弃用的方法，使用 set_max_tb(0) 替代
        pass

    def set_max_fail(self, x):
        check_log._max_fail = x

    def set_max_report(self, x):
        check_log._max_report = x

    def set_max_tb(self, x):
        check_log._max_tb = x
```

这些方法允许用户设置最大失败次数、最大报告次数和最大追踪栈深度。`set_no_tb` 方法已被弃用。

### 失败回调方法

```python
    def call_on_fail(self, func):
```
`call_on_fail` 方法设置一个回调函数，当测试失败时调用。

### 全局实例

```python
check = CheckContextManager()
```

在文件的最后，创建了一个 `CheckContextManager` 的全局实例 `check`，它可以在测试代码中直接使用，无需实例化。

## __init__.py文件

`__init__.py` 文件是 Python 包的初始化文件，它定义了包的行为和对外提供的接口。对于 `pytest_check` 这个插件来说，`__init__.py` 做了以下几件事情：

1. **注册断言重写**：
   ```python
   import pytest
   pytest.register_assert_rewrite("pytest_check.check_functions")
   ```
   这行代码告诉 pytest 插件系统，当进行断言操作时，应该使用 `pytest_check.check_functions` 模块中定义的断言方法。

2. **导入并暴露辅助函数**：
   ```python
   from pytest_check.check_functions import *  # noqa: F401, F402, F403, E402
   ```
   这行代码从 `check_functions` 模块导入所有函数，并将它们放在包的顶层，使得用户可以直接使用这些函数，如 `pytest_check.equal(1, 1)`。

3. **导入并暴露 `any_failures` 函数**：
   ```python
   from pytest_check.check_log import any_failures  # noqa: F401, F402, F403, E402
   ```
   `any_failures` 函数被导入并放在包的顶层，允许用户检查是否有任何检查失败。

4. **导入并暴露 `raises` 函数**：
   ```python
   from pytest_check.check_raises import raises  # noqa: F401, F402, F403, E402
   ```
   `raises` 函数被导入，允许用户在测试中使用上下文管理器来检查是否抛出了预期的异常。

5. **导入并暴露 `check` 上下文管理器**：
   ```python
   from pytest_check.context_manager import check  # noqa: F401, F402, F403, E402
   ```
   `check` 上下文管理器被导入，允许用户在 `with` 语句中使用它来进行断言检查。

6. **为 `check` 添加额外的方法**：
   ```python
   setattr(check, "raises", raises)
   setattr(check, "any_failures", any_failures)
   setattr(check, "check", check)
   ```
   这些 `setattr` 调用为 `check` 上下文管理器添加了 `raises` 和 `any_failures` 方法，以及一个 `check` 方法，虽然这看起来有些冗余。

7. **将辅助函数添加到 `check` 上下文管理器**：
   ```python
   for func in check_functions.__all__:  # noqa: F405
       setattr(check, func, getattr(check_functions, func))  # noqa: F405
   ```
   这将 `check_functions` 模块中定义的所有函数添加到 `check` 上下文管理器中，使得这些函数可以在 `with check:` 语句中使用。

## plugin.py文件

`plugin.py` 文件是 `pytest_check` 插件的入口点，它定义了插件如何与 pytest 框架集成。以下是对文件中定义的函数和钩子（hooks）的详细解读：

### pytest_runtest_makereport 钩子

```python
@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_makereport(item, call):
```

这个钩子在每个测试用例执行后被调用，用于生成测试报告。它处理了以下逻辑：

- 获取 `check_log` 中记录的失败次数和失败信息。
- 如果存在失败，且当前测试已被标记为 `xfail`（预期失败），则将测试结果设置为 "skipped"。
- 如果存在失败，但测试没有被标记为 `xfail`，则将测试结果设置为 "failed"，并构建一个详细的失败报告。

### pytest_configure 函数

```python
def pytest_configure(config):
```

这个函数在 pytest 启动时被调用，用于配置插件的行为：

- 根据终端是否支持颜色输出，设置 `check_log` 的颜色使用标志。
- 根据命令行参数 `--maxfail` 的值，设置是否在第一个检查失败时停止测试。
- 设置 `context_manager`、`check_raises` 和 `check_log` 模块的 `_stop_on_fail` 变量。
- 根据命令行参数 `--tb` 的值，设置是否显示伪追踪栈。
- 获取并存储其他一些命令行选项，如 `check-max-report`、`check-max-fail` 和 `check-max-tb`。

### check_fixture 函数

```python
@pytest.fixture(name="check")
def check_fixture():
```

这个函数定义了一个 pytest fixture，允许测试用例通过 `check` fixture 访问 `context_manager.check` 实例。

### pytest_addoption 函数

```python
def pytest_addoption(parser):
```

这个函数添加了自定义命令行选项，允许用户在运行 `pytest` 时设置：

- `--check-max-report`：最大报告的失败次数。
- `--check-max-fail`：每个测试允许的最大失败次数。
- `--check-max-tb`：每个测试的最大伪追踪栈数量。

## pseudo_traceback.py文件

`pseudo_traceback.py` 文件定义了伪追踪栈（`pseudo traceback`）的功能，用于生成更友好和有用的错误信息。

### 变量定义

```python
_traceback_style = "auto"
```

定义了追踪栈的风格，默认为 "auto"，表示根据上下文自动选择。

### get_full_context 函数

```python
def get_full_context(frame):
```

这个函数从给定的栈帧中提取完整的上下文信息，包括文件名、行号、函数名、代码行的上下文、局部变量以及是否隐藏追踪栈。

### 颜色定义

```python
COLOR_RED = "\x1b[31m"
COLOR_RESET = "\x1b[0m"
```
定义了用于在终端中高亮显示文本的颜色代码。

### reformat_raw_traceback 函数

```python
def reformat_raw_traceback(lines, color):
```

这个函数重新格式化原始追踪栈信息，以提高可读性。它会跳过某些行，比如 "Traceback (most recent call last)"，并使用正则表达式解析文件路径、行号、函数名和代码上下文。如果启用了颜色显示，还会对关键部分进行颜色高亮。

### _build_pseudo_trace_str 函数

```python
def _build_pseudo_trace_str(showlocals, tb, color):
```

这个函数构建伪追踪栈字符串。它首先检查是否需要生成伪追踪栈（如果 `_traceback_style` 设置为 "no"，则不生成）。然后，它会遍历栈帧，提取用户代码的上下文信息，并在必要时显示局部变量。如果启用了颜色显示，还会对文件名等关键信息进行颜色高亮。

### 伪追踪栈构建逻辑

- `skip_own_frames`：跳过自身框架的数量，以避免在生成的追踪栈中包含插件自身的代码。
- `pseudo_trace`：用于存储构建的伪追踪栈信息。
- `func`：用于存储当前遍历到的函数名。

# 小结

-  `check_functions.py` 模块提供了一组自定义的断言函数，它们在断言失败时不会立即失败，而是提供了更灵活的错误处理方式。这些函数可以与 `pytest` 测试框架无缝集成，增强测试的可读性和灵活性。装饰器 `check_func` 允许用户定义自己的断言函数，并在这些函数失败时记录详细的日志信息。
- `check_log.py` 提供了一套机制来记录和处理测试中的失败情况。通过 `log_failure` 函数，用户可以灵活地记录失败信息，并根据需要调整失败处理的行为，例如设置最大失败次数、是否在第一个失败时停止测试，以及是否使用颜色高亮显示失败信息。此外，通过 `clear_failures` 函数，可以在每个测试开始时重置失败记录状态。
- `check_raises.py` 提供了一个灵活的方式来检查预期的异常。通过 `raises` 函数，用户可以指定一个或多个期望的异常类型，并将其应用于可调用对象或作为上下文管理器使用。`CheckRaisesContext` 类提供了上下文管理器的实现，允许在 `with` 语句中使用 `raises` 函数。这种实现方式允许用户更精确地控制异常的检查和测试流程，特别是在需要捕获和验证多个异常类型时。
- `__init__.py` 文件通过一系列导入和设置，使得 `pytest_check` 插件的功能可以很容易地被 `pytest` 测试框架使用。它提供了断言重写、辅助函数、上下文管理器和异常检查功能，并且允许用户以一种非常直观和一致的方式使用这些功能。通过这种方式，`pytest_check` 插件增强了 pytest 的功能，使得编写和维护测试变得更加方便。
- `context_manager.py` 中的 `CheckContextManager` 类提供了一个强大的上下文管理器，用于捕获和记录测试中的断言错误。通过这个类，用户可以自定义错误消息、设置最大失败次数和追踪栈深度，并在失败时调用回调函数。全局实例 `check` 的存在使得这个功能在整个测试代码中易于访问和使用。
- `plugin.py` 通过定义 pytest 钩子和函数，实现了 `pytest_check` 插件的核心功能。它处理测试报告的生成，根据用户配置调整插件行为，并提供了一个自定义的 `pytest fixture`。通过这些机制，`pytest_check` 插件增强了 `pytest` 的错误报告和检查功能，使得测试更加灵活和强大。
- `pseudo_traceback.py` 提供了一种机制，用于生成更易于理解的追踪栈信息，特别是在 `pytest` 测试失败时。它通过解析和重新格式化原始追踪栈，以及提取和显示用户代码的上下文信息，帮助用户更快地定位问题所在。此外，通过颜色高亮和条件显示局部变量，进一步增强了错误信息的可读性和有用性。


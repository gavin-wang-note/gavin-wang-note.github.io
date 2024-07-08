---
title: 测试用例中多个软断言pytest-assume源码解读
date: 2024-11-17 23:00:00
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
summary: 测试用例中多个软断言pytest-assume源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest-assume` 插件允许在单个测试中进行多个软断言，即便一个断言失败，也会继续测试其余断言。接下来将详细解读该插件的核心源码部分，包括两个主要文件：`hooks.py` 和 `plugin.py`。

# 文件 `hooks.py`

`hooks.py` 文件定义了三个钩子函数，用户可以自定义这些钩子以适应特定需求。

```python
def pytest_assume_fail(lineno, entry):
    """
    Hook to manipulate user-defined data in case of assumption failure.
    lineno: Line in the code from where assumption failed.
    entry: The assumption failure message generated from assume() call
    """
    pass

def pytest_assume_pass(lineno, entry):
    """
    Hook to manipulate user-defined data in case of assumption success.
    lineno: Line in the code from where assumption succeeded.
    entry: The assumption success message generated from assume() call
    """
    pass

def pytest_assume_summary_report(failed_assumptions):
    """
    Hook to manipulate the summary that prints at the end.
    User can print the failure summary as per desired format.
    failed_assumptions: List of all failed assume() calls

    return: String representation of the summary report.
    """
    pass
```

- **`pytest_assume_fail(lineno, entry)`**：当假设失败时调用，提供失败的行号和失败消息。
- **`pytest_assume_pass(lineno, entry)`**：当假设成功时调用，提供成功的行号和成功消息。
- **`pytest_assume_summary_report(failed_assumptions)`**：在打印总结报告时调用，提供所有失败假设的列表。

# 文件 `plugin.py`

`plugin.py` 文件定义了 `pytest-assume` 插件的主体实现，包括上下文管理器、假设处理等核心功能。

## 导入模块

```python
import inspect
import os.path
from functools import partial
import pytest
from six import reraise as raise_

try:
    from py.io import saferepr
except ImportError:
    saferepr = repr
```

- **`inspect`、`os.path`**：用于获取调用栈和文件路径。
- **`partial`**：部分函数应用。
- **`pytest`**：导入 pytest。
- **`six.reraise`**：兼容 Python 2 和 3 的重新引发异常函数。
- **`saferepr`**：安全地获取变量的字符串表示。

## 处理不同版本的 pytest

```python
try:
    from _pytest.skipping import xfailed_key as evalxfail_key
    from _pytest.skipping import evaluate_xfail_marks as mark_eval
except ImportError:
    from _pytest.mark.evaluate import MarkEvaluator
    mark_eval = partial(MarkEvaluator, name="xfail")
    try:
        from _pytest.skipping import evalxfail_key
    except ImportError:
        evalxfail_key = ""
```

- 处理不同版本的 `pytest` 中 `xfail` 标记的评估方式。

## 定义全局变量

```python
_FAILED_ASSUMPTIONS = []
```

- **`_FAILED_ASSUMPTIONS`**：用于存储所有失败的假设。

## 定义 `Assumption` 类

```python
class Assumption(object):
    __slots__ = ["entry", "tb", "locals"]

    def __init__(self, entry, tb, locals=None):
        self.entry = entry
        self.tb = tb
        self.locals = locals

    def longrepr(self):
        output = [self.entry, "Locals:"]
        output.extend(self.locals)
        return "\n".join(output)

    def repr(self):
        return self.entry
```

- **`Assumption` 类**：
  - **`__slots__`**：限定实例属性，节省内存。
  - **`__init__`**：初始化假设，包含条目、堆栈跟踪和局部变量。
  - **`longrepr`**：返回详细表示，包括局部变量。
  - **`repr`**：返回简短表示，仅包含条目。

## 定义 `FailedAssumption` 异常类

```python
class FailedAssumption(AssertionError):
    pass
```

- **`FailedAssumption`**：自定义异常类，用于表示假设失败继承自 `AssertionError`。

## 定义 `AssumeContextManager` 上下文管理器类

```python
class AssumeContextManager(object):
    def __init__(self):
        self._enter_from_call = False

    def __enter__(self):
        __tracebackhide__ = True
        self._last_status = None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        __tracebackhide__ = True
        pretty_locals = None
        entry = None
        tb = None
        stack_level = 2 if self._enter_from_call else 1
        (frame, filename, line, funcname, contextlist) = inspect.stack()[stack_level][0:5]
        try:
            filename = os.path.relpath(filename)
        except ValueError:
            pass
        context = "" if contextlist is None else contextlist[0].lstrip()

        if exc_type is None:
            entry = u"{filename}:{line}: AssumptionSuccess\n>>\t{context}".format(**locals())
            pytest._hook_assume_pass(lineno=line, entry=entry)
            self._last_status = True
            return True

        elif issubclass(exc_type, AssertionError):
            if exc_val:
                context += "{}: {}\n\n".format(exc_type.__name__, exc_val)
            entry = u"{filename}:{line}: AssumptionFailure\n>>\t{context}".format(**locals())
            pretty_locals = [
                "\t%-10s = %s" % (name, saferepr(val)) for name, val in frame.f_locals.items()
            ]
            pytest._hook_assume_fail(lineno=line, entry=entry)
            _FAILED_ASSUMPTIONS.append(Assumption(entry, exc_tb, pretty_locals))
            self._last_status = False
            return True

        else:
            return

    def __call__(self, expr, msg=""):
        __tracebackhide__ = True
        self._enter_from_call = True
        with self:
            if msg:
                assert expr, msg
            else:
                assert expr
        self._enter_from_call = False
        return self._last_status
```

- **`AssumeContextManager` 类**：
  - **`__enter__`**：进入上下文时初始化 `self._last_status`。
  - **`__exit__`**：离开上下文时检查异常类型，记录假设失败并调用相关钩子函数。
  - **`__call__`**：允许直接调用上下文管理器进行假设检查。

## 定义assume实例

```python
assume = AssumeContextManager()
```

- **`assume`**：实例化 `AssumeContextManager`，可用于执行假设。

# 注册和配置 pytest 钩子

## 添加钩子

```python
def pytest_addhooks(pluginmanager):
    from . import hooks
    pluginmanager.add_hookspecs(hooks)
```

- **`pytest_addhooks`**：注册自定义钩子函数。

## 配置 pytest

```python
def pytest_configure(config):
    pytest.assume = assume
    pytest._showlocals = config.getoption("showlocals")
    pytest._hook_assume_fail = config.pluginmanager.hook.pytest_assume_fail
    pytest._hook_assume_pass = config.pluginmanager.hook.pytest_assume_pass
    pytest._hook_assume_summary_report = config.pluginmanager.hook.pytest_assume_summary_report
```

- **`pytest_configure`**：配置 `pytest`，各个钩子函数绑定到 `pytest` 上。

# 实现 pytest 钩子函数

```python
@pytest.hookimpl(tryfirst=True)
def pytest_assume_fail(lineno, entry):
    pass

@pytest.hookimpl(tryfirst=True)
def pytest_assume_pass(lineno, entry):
    pass

@pytest.hookimpl(tryfirst=True)
def pytest_assume_summary_report(failed_assumptions):
    if getattr(pytest, "_showlocals"):
        content = "".join(x.longrepr() for x in failed_assumptions)
    else:
        content = "".join(x.repr() for x in failed_assumptions)
    return content
```

- **钩子实现**：这些钩子实际上在 `plugin.py` 内部定义被覆盖函数。

# 运行测试时的行为

```python
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_call(item):
    __tracebackhide__ = True
    outcome = None
    try:
        outcome = yield
    finally:
        failed_assumptions = _FAILED_ASSUMPTIONS
        if failed_assumptions:
            failed_count = len(failed_assumptions)
            root_msg = "\n%s Failed Assumptions:\n" % failed_count

            content = pytest._hook_assume_summary_report(failed_assumptions=failed_assumptions)

            if len(content) == 1:
                content = content[0]
            else:
                content = content[1]

            last_tb = failed_assumptions[-1].tb
            del _FAILED_ASSUMPTIONS[:]
            if outcome and outcome.excinfo:
                # Xfailed test, but with strict=True. This is done via the pytest_pyfunc_call() hook, which
                # is before our hook.
                if "[XPASS(strict)]" in str(outcome.excinfo[1]):
                    restore_xfail(item)
                    raise_(FailedAssumption, FailedAssumption("%s\n%s" % (root_msg, content)), last_tb)
                root_msg = "\nOriginal Failure:\n\n>> %s\n" % repr(outcome.excinfo[1]) + root_msg
                raise_(
                    FailedAssumption,
                    FailedAssumption(root_msg + "\n" + content),
                    outcome.excinfo[2],
                )
            else:
                exc = FailedAssumption(root_msg + "\n" + content)
                raise_(FailedAssumption, exc, last_tb)
```

- **`last_tb = failed_assumptions[-1].tb`**：获取最后一个失败假设的堆栈跟踪。
- **`del _FAILED_ASSUMPTIONS[:]`**：清空失败假设列表。
- **处理原始测试结果**：
  - 如果存在 `outcome` 并且它包含例外信息：
    - 如果存在严格的 `xfail` 情况（测试预期失败但实际上通过），恢复 `xfail` 标记，并引发 `FailedAssumption` 异常。
    - 生成原始失败消息，并引发 `FailedAssumption`，将原始失败消息与假设失败消息合并。
  - 否则：
    - 简单地引发 `FailedAssumption`，包含所有假设失败信息。

## 辅助函数restore_xfail

```python
def restore_xfail(item):
    if hasattr(item, "_store"):
        item._store[evalxfail_key] = mark_eval(item)
    else:
        item._evalxfail = mark_eval(item)
```

- **`restore_xfail`**：恢复 `xfail` 标记，用于处理严格的 `xfail` 情况（即 `strict=True` 的 `xfail`）。

# 总结

`pytest-assume` 插件的核心功能包括：
- **多个软断言**：允许在一个测试中进行多个断言检查，即使一个断言失败，测试仍会继续执行。
- **钩子机制**：通过钩子函数 `pytest_assume_fail`、`pytest_assume_pass` 和 `pytest_assume_summary_report`，用户可以自定义假设失败、成功和总结报告的行为。
- **上下文管理器**：`AssumeContextManager` 类提供了一个上下文管理器和函数调用接口，通过 `__enter__` 和 `__exit__` 方法处理假设成功和失败。
- **兼容性**：插件处理了不同版本的 `pytest`，确保在多种环境下能够正常工作。
- **报告生成**：在测试结束后，生成详细的假设失败报告。

# 操作示例

以下是如何在测试中使用 `pytest-assume` 的示例：

## 安装插件

如果您还未安装 `pytest-assume`，可以通过 pip 安装：

```shell
pip install pytest-assume
```

## 编写测试示例

创建一个测试文件 `test_example.py`：

```python
import pytest

def test_multiple_assertions():
    pytest.assume(1 == 2, "First assumption failed")
    pytest.assume(2 == 2, "Second assumption passed")
    pytest.assume(3 == 2, "Third assumption failed")
    pytest.assume(3 == 3, "Fourth assumption passed")
```

## 运行测试

在终端中运行测试：

```shell
pytest test_example.py
```

## 查看输出

查看输出报告，确保显示了所有的假设，以及每个假设的成功或失败情况。

```plaintext
root@Gavin:~/pytest_plugin/test# pytest test_example.py 
Test session starts (platform: linux, Python 3.11.6, pytest 8.2.2, pytest-sugar 1.0.0)
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/pytest_plugin/test
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, twisted-1.14.1, picked-0.5.0, assume-2.4.3, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, sugar-1.0.0, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                         


―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――― test_multiple_assertions ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――

tp = <class 'pytest_assume.plugin.FailedAssumption'>, value = None, tb = None

    def reraise(tp, value, tb=None):
        try:
            if value is None:
                value = tp()
            if value.__traceback__ is not tb:
>               raise value.with_traceback(tb)
E               pytest_assume.plugin.FailedAssumption: 
E               2 Failed Assumptions:
E               
E               test_example.py:4: AssumptionFailure
E               >>	pytest.assume(1 == 2, "First assumption failed")
E               AssertionError: First assumption failed
E               assert False
E               
E               test_example.py:6: AssumptionFailure
E               >>	pytest.assume(3 == 2, "Third assumption failed")
E               AssertionError: Third assumption failed
E               assert False

/usr/lib/python3/dist-packages/six.py:718: FailedAssumption
```

通过这种方式，您可以继续在一个测试中进行多个断言检查，并查看每个断言的失败和成功情况。

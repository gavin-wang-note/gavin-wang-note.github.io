---
title: 测试用例性能分析之pytest-line-profiler源码解读
date: 2025-01-05 23:00:00
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
summary: 测试用例性能分析之pytest-line-profiler源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest-line-profiler` 插件提供了在 `pytest` 中对指定函数进行行级别性能分析的功能。通过这个插件，可以生成详细的行级别性能分析报告，以帮助优化代码性能。

本文介绍一下此插件的核心源码`pytest_line_profiler.py`，并给出运行示例。

访问[官网](https://pypi.org/project/pytest-line-profiler)下载源码到本地，解压：

```shell
root@Gavin:~/pytest_plugin/pytest-line-profiler-0.2.1# ll
total 48
drwxr-xr-x  4 1001 saned 4096 Aug 10  2023 ./
drwxr-xr-x 11 root root  4096 Jul 15 16:20 ../
-rw-r--r--  1 1001 saned 1083 Aug 10  2023 LICENSE
-rw-r--r--  1 1001 saned   97 Aug 10  2023 MANIFEST.in
-rw-r--r--  1 1001 saned 5010 Aug 10  2023 PKG-INFO
drwxr-xr-x  2 1001 saned 4096 Aug 10  2023 pytest_line_profiler.egg-info/
-rw-r--r--  1 1001 saned 2374 Aug 10  2023 pytest_line_profiler.py
-rw-r--r--  1 1001 saned 3871 Aug 10  2023 README.md
-rw-r--r--  1 1001 saned   38 Aug 10  2023 setup.cfg
-rw-r--r--  1 1001 saned 1614 Aug 10  2023 setup.py
drwxr-xr-x  2 1001 saned 4096 Aug 10  2023 tests/
root@Gavin:~/pytest_plugin/pytest-line-profiler-0.2.1#
```

# 源码解读

## 核心文件pytest_line_profiler.py

## 插件源码解读

### 导入模块

```python
import io
import pytest
from importlib import import_module
from line_profiler import LineProfiler
```

- **`io`**：提供处理 IO 操作的工具。
- **`pytest`**：引入 pytest 框架。
- **`importlib`**：用于导入模块。
- **`line_profiler`**：提供行级性能分析功能的库。

### 获取分析统计数据

```python
def get_stats(lp: LineProfiler) -> str:
    s = io.StringIO()
    lp.print_stats(stream=s)
    return s.getvalue()
```

- **`get_stats(lp)`**：获取 `LineProfiler` 对象的统计数据，并将其转换为字符串形式。

### 导入模块中的可调用对象

```python
def import_string(dotted_path):
    if not isinstance(dotted_path, str):
        return dotted_path
    try:
        module_path, callable_name = dotted_path.rsplit('.', 1)
        module = import_module(module_path)
        callable_object = getattr(module, callable_name)
        assert callable(callable_object)
        return callable_object
    except (ModuleNotFoundError, ValueError, AttributeError, AssertionError):
        raise pytest.UsageError(f"{dotted_path} not found or is not callable")
```

- **`import_string(dotted_path)`**：导入点分模块路径并返回可调用对象。如果路径无效或对象不可调用，则抛出 `pytest.UsageError` 异常。

### 添加命令行选项

```python
def pytest_addoption(parser):
    group = parser.getgroup('line-profile')
    group.addoption(
        '--line-profile',
        action='store',
        nargs="*",
        help='Register a function to profile while executed tests.'
    )
```

- **`pytest_addoption(parser)`**：添加 `--line-profile` 命令行选项，该选项接受多个指定的函数名。

### 加载初始化配置

```python
def pytest_load_initial_conftests(early_config, parser, args):
    early_config.addinivalue_line(
        "markers",
        "line_profile: Line profile this test.",
    )
```

- **`pytest_load_initial_conftests`**：在配置文件中添加 `line_profile` 标记，用于标记需要进行性能分析的测试用例。

### 运行测试调用时进行性能分析

```python
def pytest_runtest_call(item):
    instrumented = []
    if item.get_closest_marker("line_profile"):
        instrumented += [import_string(s) for s in item.get_closest_marker("line_profile").args]
    if item.config.getvalue("line_profile"):
        instrumented += [import_string(s) for s in item.config.getvalue("line_profile")]

    if instrumented:
        lp = LineProfiler(*instrumented)
        item_runtest = item.runtest
        def runtest():
            lp.runcall(item_runtest)
            item.config._line_profile = getattr(item.config, "_line_profile", {})
            item.config._line_profile[item.nodeid] = get_stats(lp)
        item.runtest = runtest
```

- **`pytest_runtest_call(item)`**：当测试用例运行时，检查是否需要对某些函数进行行级别的性能分析。如果需要，使用 `LineProfiler` 对这些函数进行分析，并将结果存储在 `item.config._line_profile` 中。

### 生成终端概述

```python
def pytest_terminal_summary(
    terminalreporter: "TerminalReporter",
    exitstatus: "ExitCode",
    config: "Config",
) -> None:
    reports = getattr(config, "_line_profile", {})
    for k, v in reports.items():
        terminalreporter.write_sep("=", f"Line Profile result for {k}")
        terminalreporter.write(v)
```

- **`pytest_terminal_summary`**：在测试执行完成后，输出所有行级别性能分析的结果。

### 定义 `line_profiler` 夹具

```python
@pytest.fixture
def line_profiler(request):
    lp = LineProfiler()
    yield lp
    request.addfinalizer(lp.print_stats)
```

- **`line_profiler(request)`**：定义一个 `line_profiler` 夹具，提供 `LineProfiler` 对象，在 `yield` 后自动打印性能分析结果。

# 如何使用这个插件

## 1. 安装依赖

首先，安装 `pytest`, `line_profiler` 以及 `pytest-line-profiler` 插件。

```shell
pip install pytest
pip install line_profiler
pip install pytest-line-profiler
```

## 2. 示例代码

假设有一个简单的 Python 模块 `mymodule.py` 和一个测试文件 `test_mymodule.py`：

### `mymodule.py`

```python
# mymodule.py

def foo():
    for _ in range(1000):
        pass

def bar():
    for _ in range(500):
        foo()
```

### `test_mymodule.py`

```python
# test_mymodule.py

import mymodule
import pytest

@pytest.mark.line_profile("mymodule.foo", "mymodule.bar")
def test_bar():
    mymodule.bar()
```

## 3. 运行测试

使用 `pytest` 运行测试，同时启用 `--line-profile` 选项。

```shell
pytest --line-profile
```

## 4. 查看结果

运行测试后，终端会显示函数 `foo` 和 `bar` 的行级别性能分析结果：

```plaintext
root@Gavin:~/test/profile# pytest --line-profile
Test session starts (platform: linux, Python 3.11.6, pytest 8.2.2, pytest-sugar 1.0.0)
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/profile
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, profiling-1.7.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, twisted-1.14.1, picked-0.5.0, assume-2.4.3, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, sugar-1.0.0, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2, extra-durations-0.1.3, line-profiler-0.2.1
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                         

 test_mymodule.py ?                                                                                                                                                                                                                        100% ██████████
=================================================================================================== Line Profile result for test_mymodule.py::test_bar ===================================================================================================
Timer unit: 1e-09 s

Total time: 0.0803654 s
File: /root/test/profile/mymodule.py
Function: foo at line 1

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     1                                           def foo():
     2    500500   44110416.0     88.1     54.9      for _ in range(1000):
     3    500000   36254943.0     72.5     45.1          pass

Total time: 0.188115 s
File: /root/test/profile/mymodule.py
Function: bar at line 5

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     5                                           def bar():
     6       501      63555.0    126.9      0.0      for _ in range(500):
     7       500  188051776.0 376103.6    100.0          foo()

=============================================================================================================== sum of all tests durations ===============================================================================================================
0.21s

Results (0.24s):
       1 passed
root@Gavin:~/test/profile#
```

通过这种方式，使用 `pytest-line-profiler` 插件生成详细的行级别性能分析报告，以帮助你优化代码性能。

当然官方给出了一个针对特定函数，使用`@pytest.mark.line_profile`实现的对应函数性能统计分析示例。


# 结语

这个插件通过添加命令行选项和使用 `pytest` 的钩子系统，允许用户在测试过程中对指定的函数或测试用例进行行级性能分析。它提供了一种方便的方式来识别性能瓶颈，并在测试报告中直接查看性能数据。通过使用 `line_profiler fixture`，用户可以在测试函数中直接使用行级分析，而无需修改测试代码。

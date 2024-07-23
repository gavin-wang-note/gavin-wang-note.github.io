---
title: 测试用例失败重运行之pytest-rerunfailures源码解读
date: 2025-02-23 22:00:00
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
summary: 测试用例失败重运行之pytest-rerunfailures源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest` 插件 `pytest-rerunfailures`用于在测试失败时重新运行测试，以消除间歇性（`flaky`）测试失败（它们可能由于许多因素，如网络延迟、资源加载问题、并发问题等偶尔失败）。



# 主要特性

- **自动重试**：能够自动重新运行未通过的测试。
- **重试次数**：可以定义要重新运行每个失败测试的次数。
- **重试延迟**：可以在重试之间设置延迟。
- **有条件的重试**：可以根据失败原因有选择地重试测试。
- **与其他插件兼容**：可以与如 `pytest-xdist` 的并行测试执行插件共同使用。



# 使用场景

- **处理间歇性错误**：网络请求或集成测试中的间歇性错误。
- **外部资源波动**：依赖于外部服务或资源的测试可能受到这些资源的可用性或响应速度的影响。
- **并发问题**：并发环境中可能出现的竞争条件或其他并发问题。
- **加载时间差异**：例如，UI 测试中的元素加载时间可能因环境而异。



# 使用示例

如果没安装，可通过 `pip` 命令进行安装：

```shell
pip install -U pytest-rerunfailures
```

我们来看一个非常常见的示例，使用命令行选项自动重试所有失败的测试：

```shell
pytest --reruns 2 --reruns-delay 1
```

在此例中，失败的测试将被自动重新运行最多两次，并在每次重试前设置 1 秒的延迟。

对特定测试使用 `@pytest.mark.flaky` 重试：

```python
# content of test_rerunfailures.py
import random
import pytest

# 无条件地在每个错误或失败的测试后重试最多两次
@pytest.mark.flaky(reruns=2)
def test_example_fail_twice():
    """这个测试有一个随机因素，它可能会失败，我们将尝试重跑两次。"""
    assert random.choice([True, False])

# 在特定条件下重试
@pytest.mark.flaky(reruns=5, reruns_delay=1)
def test_example_with_condition():
    """这个测试在特定条件下失败，我们将重试5次，并在重试间增加延迟。"""
    value = random.randint(0, 5)
    assert value > 2

# 没有使用rerunfailures装饰器的测试
def test_always_passes():
    """这个测试总是通过，不涉及重跑逻辑。"""
    assert True
```

如果期间有测试失败，`pytest-rerunfailures` 插件会按照指定的 `reruns` 数量对失败的测试进行重试。对于带有 `@pytest.mark.flaky` 装饰器的测试，如 `test_example_fail_twice` 和 `test_example_with_condition`，将遵循装饰器中定义的重试规则。

`test_always_passes` 是一个普通的测试，不涵盖重跑逻辑，所以如果它失败了，它不会自动重试。

```shell
root@Gavin:~/pytest_plugin/test# pytest -s -v test_rerunfailures.py
Test session starts (platform: linux, Python 3.11.6, pytest 8.2.2, pytest-sugar 1.0.0)
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-44-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'profiling': '1.7.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'order': '1.2.1', 'progress': '1.3.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'assume': '2.4.3', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2', 'extra-durations': '0.1.3', 'line-profiler': '0.2.1', 'sugar': '1.0.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/pytest_plugin/test
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, profiling-1.7.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, twisted-1.14.1, picked-0.5.0, assume-2.4.3, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2, extra-durations-0.1.3, line-profiler-0.2.1, sugar-1.0.0
asyncio: mode=Mode.STRICT
collected 3 items                                                                                                                                                                                                                        

 test_rerunfailures.py::test_example_fail_twice RR✓                                                                                                                                                                         33% ███▍      
 test_rerunfailures.py::test_example_with_condition ✓                                                                                                                                                                       67% ██████▋   
 test_rerunfailures.py::test_always_passes ✓                                                                                                                                                                               100% ██████████
======================================================================================================= sum of all tests durations =======================================================================================================

0.02s

Results (0.08s):
       3 passed
       2 rerun
root@Gavin:~/pytest_plugin/test#
```

从执行结果看，用例`test_example_fail_twice`第一次和第二次失败，第三次成功。再来看一下携带参数的效果：

```shell
root@Gavin:~/pytest_plugin/test# pytest -s -v --reruns 2 --reruns-delay 1 test_rerunfailures.py
Test session starts (platform: linux, Python 3.11.6, pytest 8.2.2, pytest-sugar 1.0.0)
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-44-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'profiling': '1.7.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'order': '1.2.1', 'progress': '1.3.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'assume': '2.4.3', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2', 'extra-durations': '0.1.3', 'line-profiler': '0.2.1', 'sugar': '1.0.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/pytest_plugin/test
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, profiling-1.7.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, twisted-1.14.1, picked-0.5.0, assume-2.4.3, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2, extra-durations-0.1.3, line-profiler-0.2.1, sugar-1.0.0
asyncio: mode=Mode.STRICT
collected 3 items                                                                                                                                                                                                                        

 test_rerunfailures.py::test_example_fail_twice ✓                                                                                                                                                                           33% ███▍      
 test_rerunfailures.py::test_example_with_condition R✓                                                                                                                                                                      67% ██████▋   
 test_rerunfailures.py::test_always_passes ✓                                                                                                                                                                               100% ██████████
======================================================================================================= sum of all tests durations =======================================================================================================
0.02s

Results (1.10s):
       3 passed
       1 rerun
root@Gavin:~/pytest_plugin/test#
```

携带此参数后，用例`test_example_fail_twice`的执行次数明显变少。




# 注意事项

- **遮掩问题**：自动重试有可能掩盖根本问题，而这些问题可能需要修复。
- **增加测试时间**：重试失败的测试会增加总体的测试执行时间。
- **与CI集成**：在持续集成系统中使用时需要考虑到测试时间延长问题。
- **可能的资源清理**：在重试前可能需要清理由前一次测试运行留下的资源，避免 "脏" 环境影响后续测试。
- **并行测试**：在并行测试中使用时要特别小心，重试可能不会按预期工作。

`pytest-rerunfailures` 插件很适合用在不稳定或易受环境影响的测试上，但最好还是尽量让测试保持稳定和可预测，并且对 flaky 测试进行额外的调查和分析，以防在一个确定性的环境中隐藏问题。记住，过度依赖自动重试可能会降低持续集成反馈的价值，并使得问题难以被察觉和解决。



# 源码目录结构

从[官网](https://pypi.org/project/pytest-rerunfailures)下载源码解压后目录结构如下：

```shell
root@Gavin:~/pytest_plugin/pytest-rerunfailures-14.0# ll
total 88
drwxr-xr-x  4  502 staff  4096 Mar 13 16:21 ./
drwxr-xr-x 17 root root   4096 Jul 23 11:46 ../
-rw-r--r--  1  502 staff  9708 Mar 13 16:21 CHANGES.rst
-rw-r--r--  1  502 staff  1252 Mar 13 16:21 CONTRIBUTING.rst
-rw-r--r--  1  502 staff    14 Mar 13 16:21 HEADER.rst
-rw-r--r--  1  502 staff   198 Mar 13 16:21 LICENSE
-rw-r--r--  1  502 staff    74 Mar 13 16:21 MANIFEST.in
-rw-r--r--  1  502 staff 18948 Mar 13 16:21 PKG-INFO
-rw-r--r--  1  502 staff  2306 Mar 13 16:21 pyproject.toml
-rw-r--r--  1  502 staff  7796 Mar 13 16:21 README.rst
-rw-r--r--  1  502 staff    38 Mar 13 16:21 setup.cfg
-rwxr-xr-x  1  502 staff    60 Mar 13 16:21 setup.py*
drwxr-xr-x  3  502 staff  4096 Mar 13 16:21 src/
drwxr-xr-x  2  502 staff  4096 Mar 13 16:21 tests/
-rw-r--r--  1  502 staff   966 Mar 13 16:21 tox.ini
root@Gavin:~/pytest_plugin/pytest-rerunfailures-14.0# cd src
root@Gavin:~/pytest_plugin/pytest-rerunfailures-14.0/src# ll
total 32
drwxr-xr-x 3 502 staff  4096 Mar 13 16:21 ./
drwxr-xr-x 4 502 staff  4096 Mar 13 16:21 ../
drwxr-xr-x 2 502 staff  4096 Mar 13 16:21 pytest_rerunfailures.egg-info/
-rw-r--r-- 1 502 staff 19286 Mar 13 16:21 pytest_rerunfailures.py
root@Gavin:~/pytest_plugin/pytest-rerunfailures-14.0/src#
```

核心文件是`pytest_rerunfailures.py`，接下来我们对此文件进行一些解读。



# 源码解读



## 模块import

```python
import hashlib
import importlib.metadata
import os
import platform
import re
import socket
import sys
import threading
import time
import traceback
import warnings
from contextlib import suppress

import pytest
from _pytest.outcomes import fail
from _pytest.runner import runtestprotocol
from packaging.version import parse as parse_version

try:
    from xdist.newhooks import pytest_handlecrashitem
    HAS_PYTEST_HANDLECRASHITEM = True
    del pytest_handlecrashitem
except ImportError:
    HAS_PYTEST_HANDLECRASHITEM = False
```
这里导入了需要的模块，并检查了是否导入了 `pytest_handlecrashitem`，这是为了兼容 `pytest-xdist`。

## 

## 命令行参数支持

```python
def pytest_addoption(parser):
    group = parser.getgroup("rerunfailures", "re-run failing tests to eliminate flaky failures")
    group._addoption(
        "--only-rerun",
        action="append",
        dest="only_rerun",
        type=str,
        default=None,
        help="If passed, only rerun errors matching the regex provided. "
             "Pass this flag multiple times to accumulate a list of regexes to match",
    )
    group._addoption(
        "--reruns",
        action="store",
        dest="reruns",
        type=int,
        help="number of times to re-run failed tests. defaults to 0.",
    )
    group._addoption(
        "--reruns-delay",
        action="store",
        dest="reruns_delay",
        type=float,
        help="add time (seconds) delay between reruns.",
    )
    group._addoption(
        "--rerun-except",
        action="append",
        dest="rerun_except",
        type=str,
        default=None,
        help="If passed, only rerun errors other than matching the regex "
             "provided. Pass this flag multiple times to accumulate a list of regexes to match",
    )
    arg_type = "string"
    parser.addini("reruns", "number of times to re-run failed tests. defaults to 0.", type=arg_type)
    parser.addini("reruns_delay", "add time (seconds) delay between reruns.", type=arg_type)
```
在 `pytest_addoption` 中定义了几种命令行选项，以及在 `pytest.ini` 配置文件中的选项。



## 配置检查

```python
def check_options(config):
    val = config.getvalue
    if not val("collectonly"):
        if config.option.reruns != 0:
            if config.option.usepdb:  # a core option
                raise pytest.UsageError("--reruns incompatible with --pdb")
```
这个函数检查命令行选项的有效性。如果使用了 `--reruns` 选项，将与调试（`--pdb`）功能冲突：

- 只有当 `collectonly` 选项没有被设置（即测试将被执行）时，才进行进一步检查。
- 如果设置了 `reruns` 选项，表示用户希望对失败的测试进行重新运行。
- 如果同时设置了 `usepdb` 选项，这与 `reruns` 选项的目的冲突，因为 `usepdb` 会在测试失败时立即启动调试器，而不是让测试重新运行。
- 因此，如果同时设置了这两个选项，将抛出一个 `UsageError` 异常，指出它们是不兼容的。



## 获取标记和重新运行次数

```python
def _get_marker(item):
    return item.get_closest_marker("flaky")

def get_reruns_count(item):
    rerun_marker = _get_marker(item)
    if rerun_marker is not None:
        if "reruns" in rerun_marker.kwargs:
            return rerun_marker.kwargs["reruns"]
        elif len(rerun_marker.args) > 0:
            return rerun_marker.args[0]
        else:
            return 1

    reruns = item.session.config.getvalue("reruns")
    if reruns is not None:
        return reruns

    with suppress(TypeError, ValueError):
        reruns = int(item.session.config.getini("reruns"))

    return reruns
```
这些函数用于获取重试标记和重试次数。

- 首先尝试从测试项的 `flaky` 标记中获取重试次数。`flaky` 标记可以通过位置参数或关键字参数 `reruns` 来指定重试次数。
- 如果测试项没有 `flaky` 标记或没有指定重试次数，则尝试从 pytest 的全局配置中获取 `reruns` 值。
- 如果全局配置中也没有指定，则尝试从配置文件（如 `pytest.ini`）中获取 `reruns` 配置项，并将其转换为整数。
- 如果所有方法都失败，返回默认的重试次数 1。



## 获取重试延迟

```python
def get_reruns_delay(item):
    rerun_marker = _get_marker(item)
    if rerun_marker is not None:
        if "reruns_delay" in rerun_marker.kwargs:
            delay = rerun_marker.kwargs["reruns_delay"]
        elif len(rerun_marker.args) > 1:
            delay = rerun_marker.args[1]
        else:
            delay = 0
    else:
        delay = item.session.config.getvalue("reruns_delay")
        if delay is None:
            try:
                delay = float(item.session.config.getini("reruns_delay"))
            except (TypeError, ValueError):
                delay = 0

    if delay < 0:
        delay = 0
        warnings.warn("Delay time between re-runs cannot be < 0. Using default value: 0")

    return delay
```
这个函数用于获取重试之间的延迟时间。如果在标记中有设置，则使用标记中的设置，否则使用配置中的设置。

- 首先尝试从测试项的 `flaky` 标记中获取重试延迟时间。`flaky` 标记可以通过关键字参数 `reruns_delay` 或位置参数来指定重试延迟时间。
- 如果测试项没有 `flaky` 标记或没有指定重试延迟时间，则尝试从 pytest 的全局配置中获取 `reruns_delay` 值。
- 如果全局配置中也没有指定，则尝试从配置文件中获取 `reruns_delay` 配置项，并将其转换为浮点数。
- 如果所有方法都失败或转换失败，返回默认的重试延迟时间 0。
- 确保返回的延迟时间不小于 0，并在必要时发出警告。



## get_reruns_condition



```python
def get_reruns_condition(item):
    rerun_marker = _get_marker(item)

    condition = True
    if rerun_marker is not None and "condition" in rerun_marker.kwargs:
        condition = evaluate_condition(
            item, rerun_marker, rerun_marker.kwargs["condition"]
        )

    return condition
```



 `get_reruns_condition` 的函数，用于获取与 `pytest `测试项（`test item`）相关的重试条件：

- 首先尝试从测试项的 `flaky` 标记中获取重试条件。
- 如果 `flaky` 标记中包含 `condition` 参数，则使用 `evaluate_condition` 函数来评估这个条件表达式。
- `evaluate_condition` 函数的具体实现没有在代码片段中给出，但它应该能够根据条件表达式返回一个布尔值，指示是否满足重试条件。
- 如果没有找到 `flaky` 标记或没有指定重试条件，则默认重试条件为 `True`。



## evaluate_condition



```python
def evaluate_condition(item, mark, condition: object) -> bool:
    # copy from python3.8 _pytest.skipping.py

    result = False
    # String condition.
    if isinstance(condition, str):
        globals_ = {
            "os": os,
            "sys": sys,
            "platform": platform,
            "config": item.config,
        }
        if hasattr(item, "obj"):
            globals_.update(item.obj.__globals__)  # type: ignore[attr-defined]
        try:
            filename = f"<{mark.name} condition>"
            condition_code = compile(condition, filename, "eval")
            result = eval(condition_code, globals_)  # noqa: S307
        except SyntaxError as exc:
            msglines = [
                "Error evaluating %r condition" % mark.name,
                "    " + condition,
                "    " + " " * (exc.offset or 0) + "^",
                "SyntaxError: invalid syntax",
            ]
            fail("\n".join(msglines), pytrace=False)
        except Exception as exc:
            msglines = [
                "Error evaluating %r condition" % mark.name,
                "    " + condition,
                *traceback.format_exception_only(type(exc), exc),
            ]
            fail("\n".join(msglines), pytrace=False)

    # Boolean condition.
    else:
        try:
            result = bool(condition)
        except Exception as exc:
            msglines = [
                "Error evaluating %r condition as a boolean" % mark.name,
                *traceback.format_exception_only(type(exc), exc),
            ]
            fail("\n".join(msglines), pytrace=False)
    return result
```



 `evaluate_condition` 的函数，用于评估一个条件表达式，这个条件表达式通常与 `pytest` 的 `flaky` 标记相关联，用于决定测试是否应该被标记为 flaky（即允许失败后重试）。

- 根据条件的类型（字符串或布尔值），使用不同的方法进行评估。
- 如果条件是字符串，将其作为 `Python` 表达式进行评估。
- 如果条件不是字符串，尝试将其转换为布尔值。
- 在评估过程中，如果发生语法错误或其他异常，将构造错误消息并报告错误。



## 几个私有函数



```python
def _remove_cached_results_from_failed_fixtures(item):
    """Note: remove all cached_result attribute from every fixture."""
    cached_result = "cached_result"
    fixture_info = getattr(item, "_fixtureinfo", None)
    for fixture_def_str in getattr(fixture_info, "name2fixturedefs", ()):
        fixture_defs = fixture_info.name2fixturedefs[fixture_def_str]
        for fixture_def in fixture_defs:
            if getattr(fixture_def, cached_result, None) is not None:
                result, _, err = getattr(fixture_def, cached_result)
                if err:  # Deleting cached results for only failed fixtures
                    setattr(fixture_def, cached_result, None)


def _remove_failed_setup_state_from_session(item):
    """
    Clean up setup state.

    Note: remove all failures from every node in _setupstate stack
          and clean the stack itself
    """
    setup_state = item.session._setupstate
    setup_state.stack = {}


def _get_rerun_filter_regex(item, regex_name):
    rerun_marker = _get_marker(item)

    if rerun_marker is not None and regex_name in rerun_marker.kwargs:
        regex = rerun_marker.kwargs[regex_name]
        if isinstance(regex, str):
            regex = [regex]
    else:
        regex = getattr(item.session.config.option, regex_name)

    return regex


def _matches_any_rerun_error(rerun_errors, report):
    return _try_match_reprcrash(rerun_errors, report)


def _matches_any_rerun_except_error(rerun_except_errors, report):
    return _try_match_reprcrash(rerun_except_errors, report)


def _try_match_reprcrash(rerun_errors, report):
    for rerun_regex in rerun_errors:
        try:
            if re.search(rerun_regex, report.longrepr.reprcrash.message):
                return True
        except AttributeError:
            if re.search(rerun_regex, report.longreprtext):
                return True
    return False


def _should_hard_fail_on_error(item, report):
    if report.outcome != "failed":
        return False

    rerun_errors = _get_rerun_filter_regex(item, "only_rerun")
    rerun_except_errors = _get_rerun_filter_regex(item, "rerun_except")

    if (not rerun_errors) and (not rerun_except_errors):
        # Using neither --only-rerun nor --rerun-except
        return False

    elif rerun_errors and (not rerun_except_errors):
        # Using --only-rerun but not --rerun-except
        return not _matches_any_rerun_error(rerun_errors, report)

    elif (not rerun_errors) and rerun_except_errors:
        # Using --rerun-except but not --only-rerun
        return _matches_any_rerun_except_error(rerun_except_errors, report)

    else:
        # Using both --only-rerun and --rerun-except
        matches_rerun_only = _matches_any_rerun_error(rerun_errors, report)
        matches_rerun_except = _matches_any_rerun_except_error(
            rerun_except_errors, report
        )
        return (not matches_rerun_only) or matches_rerun_except


def _should_not_rerun(item, report, reruns):
    xfail = hasattr(report, "wasxfail")
    is_terminal_error = _should_hard_fail_on_error(item, report)
    condition = get_reruns_condition(item)
    return (
        item.execution_count > reruns
        or not report.failed
        or xfail
        or is_terminal_error
        or not condition
    )
```



这段代码包含了一系列函数，它们用于在`pytest`测试框架中处理与测试重试相关的逻辑。

1. `_remove_cached_results_from_failed_fixtures` 函数：
   - 目的：从每个 `fixture` 中移除所有 `cached_result` 属性。
   - 逻辑：遍历 `item._fixtureinfo.name2fixturedefs` 中定义的所有 fixture definitions，如果找到 `cached_result` 属性，并且该 `fixture` 失败（`err` 为真），则将其 `cached_result` 设置为 `None`。

2. `_remove_failed_setup_state_from_session` 函数：
   - 目的：清理` session` 的 `setup` 状态。
   - 逻辑：清空 `item.session._setupstate.stack`，移除所有与设置状态相关的记录。

3. `_get_rerun_filter_regex` 函数：
   - 目的：获取用于决定哪些错误应该重新运行测试的正则表达式。
   - 逻辑：检查 `rerun_marker` 是否存在以及是否包含指定的 `regex_name` 参数，如果存在则使用它；否则，使用来自 `item.session.config.option` 的值。

4. `_matches_any_rerun_error` 和 `_matches_any_rerun_except_error` 函数：
   - 这两个函数的目的是检查测试报告是否与任何重试错误或排除错误匹配。
   - 它们使用 `_try_match_reprcrash` 函数来执行实际的匹配检查。

5. `_try_match_reprcrash` 函数：
   - 目的：尝试匹配报告的 crash 信息或文本表示与提供的正则表达式。
   - 逻辑：遍历 `rerun_errors` 中的每个正则表达式，尝试匹配 `report.longrepr.reprcrash.message` 或 `report.longreprtext`。

6. `_should_hard_fail_on_error` 函数：
   - 目的：确定是否应该在错误发生时立即失败（不进行重试）。
   - 逻辑：根据 `rerun_errors` 和 `rerun_except_errors` 检查报告，如果报告的失败不匹配任何 `only_rerun` 正则表达式或匹配任何 `rerun_except` 正则表达式，则测试将立即失败。

7. `_should_not_rerun` 函数：
   - 目的：确定是否不应该对测试项进行重试。
   - 逻辑：如果测试项的执行次数超过 `reruns` 指定的次数、测试没有失败、测试被标记为 xfail、测试应该立即失败，或者测试条件不满足，则不应重试。

这些函数共同处理了测试重试的逻辑，包括条件评估、错误匹配、以及基于特定规则决定是否应该重试失败的测试。



## is_master

```pyhton
def is_master(config):
    return not (hasattr(config, "workerinput") or hasattr(config, "slaveinput"))
```

这个 `is_master` 函数用于确定当前的 `pytest` 测试执行过程是否运行在主进程中。函数的逻辑非常简单：

- 它接受一个参数 `config`，这是 `pytest` 的配置对象，包含了所有的命令行选项和配置设置。
- 函数内部使用了一个 `return` 语句，检查 `config` 对象是否具有 `workerinput` 或 `slaveinput` 属性。
- 如果 `config` 有 `workerinput` 或 `slaveinput` 属性，这通常意味着当前的执行环境是一个工作进程（`worker process`），而不是主进程。
- 因此，函数返回 `False` 表示这不是主进程。
- 如果 `config` 没有这些属性，函数返回 `True`，表示这是主进程。

简而言之，`is_master` 函数通过检查配置对象是否有特定的属性来确定是否处于主进程。这是一种常见的模式，用于在分布式测试环境中区分主进程和工作进程。在 `pytest-xdist` 等插件中，这种区分可能用于决定哪些操作应该仅在主进程中执行，例如协调测试执行、收集结果或处理最终报告。



## pytest 配置函数

```python
def pytest_configure(config):
    config.addinivalue_line("markers",
                            "flaky(reruns=1, reruns_delay=0): mark test to re-run up to 'reruns' times. "
                            "Add a delay of 'reruns_delay' seconds between re-runs.")

    if config.pluginmanager.hasplugin("xdist") and HAS_PYTEST_HANDLECRASHITEM:
        config.pluginmanager.register(XDistHooks())
        if is_master(config):
            config.failures_db = ServerStatusDB()
        else:
            config.failures_db = ClientStatusDB(config.workerinput["sock_port"])
    else:
        config.failures_db = StatusDB()
```
在 `pytest_configure` 中，注册了一个新的标记 `flaky`，并根据是否使用了 `xdist` 插件来配置不同的数据库。



## 支持分布式处理的 hooks 类

```python
class XDistHooks:
    def pytest_configure_node(self, node):
        node.workerinput["sock_port"] = node.config.failures_db.sock_port

    def pytest_handlecrashitem(self, crashitem, report, sched):
        db = sched.config.failures_db
        reruns = db.get_test_reruns(crashitem)
        if db.get_test_failures(crashitem) < reruns:
            sched.mark_test_pending(crashitem)
            report.outcome = "rerun"

        db.add_test_failure(crashitem)
```
该类实现了两个 hook 方法，用于配置分布式处理节点和处理崩溃项目：

- 向 pytest 配置中添加自定义标记 `flaky` 的说明。
- 根据是否使用 `pytest-xdist` 插件以及是否支持新钩子来注册自定义钩子，并初始化用于跟踪失败测试的数据库实例。
- 确保根据当前的测试环境（并行或非并行）使用适当的数据库实例。



## 内存数据库

```python
class StatusDB:
    def __init__(self):
        self.delim = b"\n"
        self.hmap = {}

    def _hash(self, crashitem: str) -> str:
        if crashitem not in self.hmap:
            self.hmap[crashitem] = hashlib.sha1(crashitem.encode()).hexdigest()[:10]  # noqa: S324

        return self.hmap[crashitem]

    def add_test_failure(self, crashitem):
        hash = self._hash(crashitem)
        failures = self._get(hash, "f")
        failures += 1
        self._set(hash, "f", failures)

    def get_test_failures(self, crashitem):
        hash = self._hash(crashitem)
        return self._get(hash, "f")

    def set_test_reruns(self, crashitem, reruns):
        hash = self._hash(crashitem)
        self._set(hash, "r", reruns)

    def get_test_reruns(self, crashitem):
        hash = self._hash(crashitem)
        return self._get(hash, "r")

    # i is a hash of the test name, t_f.py::test_t
    # k is f for failures or r for reruns
    # v is the number of failures or reruns (an int)
    def _set(self, i: str, k: str, v: int):
        pass

    def _get(self, i: str, k: str) -> int:
        return 0
```
这是一个存储重试信息的内存数据库类：

- 使用 `_hash` 方法为每个测试项生成一个唯一的哈希值，并缓存这些哈希值以避免重复计算。
- 使用 `_set` 和 `_get` 方法来存储和检索测试失败次数和重试次数，这些方法需要在子类中具体实现。
- 提供了 `add_test_failure`、`get_test_failures`、`set_test_reruns` 和 `get_test_reruns` 等方法来操作测试失败和重试次数。



## 套接字数据库

```python
class SocketDB(StatusDB):
    def __init__(self):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(1)

    def _sock_recv(self, conn) -> str:
        buf = b""
        while True:
            b = conn.recv(1)
            if b == self.delim:
                break
            buf += b

        return buf.decode()

    def _sock_send(self, conn, msg: str):
        conn.send(msg.encode() + self.delim)
```

这段代码假设了一个网络环境，其中测试失败和重试次数的信息需要通过网络套接字进行通信。这可用于分布式测试环境中，测试结果需要在不同的测试节点之间共享。

这个类的核心逻辑如下：

- 使用 `TCP` 套接字进行网络通信。
- `_sock_recv` 方法用于从套接字连接中接收数据，直到遇到分隔符。
- `_sock_send` 方法用于将数据发送到套接字连接，并在数据末尾添加分隔符。



## 服务器数据库

```python
class ServerStatusDB(SocketDB):
    def __init__(self):
        super().__init__()
        self.sock.bind(("localhost", 0))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.rerunfailures_db = {}
        t = threading.Thread(target=self.run_server, daemon=True)
        t.start()

    @property
    def sock_port(self):
        return self.sock.getsockname()[1]

    def run_server(self):
        self.sock.listen()
        while True:
            conn, _ = self.sock.accept()
            t = threading.Thread(target=self.run_connection, args=(conn,), daemon
```

`ServerStatusDB` 类继承自 `SocketDB` 类。`ServerStatusDB` 类是一个服务器端的数据库，用于处理测试状态信息，如测试失败和重试次数，并通过 `TCP` 套接字进行通信。

- 作为服务器端，绑定到一个随机端口并监听来自客户端的连接请求。
- 使用 `threading.Thread` 创建线程来处理每个客户端连接。
- 通过 `run_server` 方法来接受客户端连接，并在连接建立时启动 `run_connection` 方法。
- `rerunfailures_db` 字典用于存储和跟踪测试的失败和重试状态信息。



## 客户端数据库

```python
class ClientStatusDB(SocketDB):
    def __init__(self, sock_port):
        super().__init__()
        self.sock.connect(("localhost", sock_port))

    def _set(self, i: str, k: str, v: int):
        self._sock_send(self.sock, "|".join(("set", i, k, str(v))))

    def _get(self, i: str, k: str) -> int:
        self._sock_send(self.sock, "|".join(("get", i, k, "")))
        return int(self._sock_recv(self.sock))
```

`ClientStatusDB` 类继承自 `SocketDB` 类。`ClientStatusDB` 类是一个客户端数据库，用于通过网络套接字与服务器进行通信，处理测试状态信息，如测试失败和重试次数。

这个类的核心逻辑是：

- 作为客户端，连接到服务器的套接字。
- 使用 `_set` 方法通过网络发送设置测试状态的请求，并等待服务器处理。
- 使用 `_get` 方法通过网络发送获取测试状态的请求，并接收服务器返回的状态信息。

请注意，这段代码中有几个关键的部分：

- `_sock_send` 和 `_sock_recv` 方法是在 `SocketDB` 类中定义的，用于发送和接收数据。
- 数据通信是通过简单的字符串传输实现的，使用 "|" 字符作为字段分隔符。
- `connect` 和 `send` 等套接字操作可能会引发异常，因此在实际使用中可能需要添加异常处理逻辑。
- 类中的 `_set` 和 `_get` 方法假设服务器能够正确处理发送的命令，并返回相应的结果。服务器端需要实现相应的逻辑来响应这些命令。



## pytest_runtest_teardown

```python
def pytest_runtest_teardown(item, nextitem):
    reruns = get_reruns_count(item)
    if reruns is None:
        # global setting is not specified, and this test is not marked with
        # flaky
        return

    if not hasattr(item, "execution_count"):
        # pytest_runtest_protocol hook of this plugin was not executed
        # -> teardown needs to be skipped as well
        return

    _test_failed_statuses = getattr(item, "_test_failed_statuses", {})

    # Only remove non-function level actions from the stack if the test is to be re-run
    # Exceeding re-run limits, being free of failue statuses, and encountering
    # allowable exceptions indicate that the test is not to be re-ran.
    if (
        item.execution_count <= reruns
        and any(_test_failed_statuses.values())
        and not any(item._terminal_errors.values())
    ):
        # clean cashed results from any level of setups
        _remove_cached_results_from_failed_fixtures(item)

        if item in item.session._setupstate.stack:
            for key in list(item.session._setupstate.stack.keys()):
                if key != item:
                    del item.session._setupstate.stack[key]
```

这个 `pytest_runtest_teardown` 函数是 `pytest` 测试框架中的一个挂钩（`hook`）实现，用于在每个测试用例执行完毕后进行清理工作。函数的主要目的是在测试失败时，如果设置了重试（`rerun`），则清理相关的状态，以便测试可以被重新执行。下面是对这段代码的逐行解读：

1. 函数签名 `pytest_runtest_teardown(item, nextitem)`：这个函数作为 `pytest` 的钩子（`hook`），接受两个参数，`item` 是当前测试项，`nextitem` 是下一个将要执行的测试项。

2. 调用 `get_reruns_count(item)` 来获取当前测试项的重试次数。

3. 如果 `reruns` 是 `None`，则表示没有设置全局重试次数，并且当前测试项没有使用 `flaky` 标记指定重试，因此不需要执行任何操作，函数返回。

4. 检查 `item` 是否有 `execution_count` 属性。该属性在 pytest 的测试执行协议钩子（`pytest_runtest_protocol`）中设置。如果没有这个属性，说明测试执行协议钩子没有被执行，因此不需要执行清理，函数返回。

5. 使用 `getattr` 获取 `item` 的 `_test_failed_statuses` 属性，这是一个字典，存储了测试失败的状态。

6. 检查是否满足以下条件才进行清理：
   - `item.execution_count` 小于或等于 `reruns`，即测试尚未超过重试次数。
   - `_test_failed_statuses` 字典中至少有一个测试用例失败了。
   - `item._terminal_errors` 字典中没有任何测试用例遇到终止错误（`terminal error`），这些通常是不应该重试的错误，如超时或中断。

7. 如果满足清理条件，调用 `_remove_cached_results_from_failed_fixtures(item)` 来移除所有失败的 `fixture` 的 `cached_result` 属性。

8. 检查 `item` 是否在 `item.session._setupstate.stack` 中，这个栈存储了测试设置的状态。如果是，并且栈中存在非当前测试项的键，则从栈中删除这些键，以清理其他测试项的设置状态。

这段代码的逻辑是在测试失败后，如果设置了重试并且测试用例没有遇到终止错误，就清理测试项的状态，以便重新执行测试。这样做的目的是避免由于测试项的副作用或依赖关系导致重试失败。



## pytest_runtest_makereport



```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    if result.when == "setup":
        # clean failed statuses at the beginning of each test/rerun
        setattr(item, "_test_failed_statuses", {})

        # create a dict to store error-check results for each stage
        setattr(item, "_terminal_errors", {})

    _test_failed_statuses = getattr(item, "_test_failed_statuses", {})
    _test_failed_statuses[result.when] = result.failed
    item._test_failed_statuses = _test_failed_statuses

    item._terminal_errors[result.when] = _should_hard_fail_on_error(item, result)
```



这段代码使用了` pytest` 的钩子（hook）机制，定义了一个 `pytest_runtest_makereport` 函数，该函数在生成测试报告时被调用。使用了 `@pytest.hookimpl` 装饰器来注册钩子实现，并使用 `hookwrapper=True` 参数来获取 `pytest` 钩子的额外上下文信息。

1. 使用 `@pytest.hookimpl` 装饰器定义钩子实现，`hookwrapper=True` 表示这个钩子会包装其他钩子的执行，允许你在其他钩子执行前后添加逻辑。

2. 定义函数 `pytest_runtest_makereport(item, call)`，它接受两个参数：
   - `item`：当前测试项（test item）。
   - `call`：一个封装了测试调用的 `pytest.CallInfo` 对象。

3. 使用 `yield` 关键字挂起函数执行，并将结果传递给 `outcome` 变量。这是 `hookwrapper=True` 用法的一部分，允许你在其他钩子执行完成后获取结果。

4. 从 `outcome` 对象获取生成的测试结果，存储在 `result` 变量中。

5. 检查 `result.when` 是否等于 `"setup"`，如果是，则表明当前是在测试用例的设置阶段。

6. 如果在设置阶段失败，则清理之前可能存在的任何失败状态，并为当前测试用例创建一个新的失败状态字典 `_test_failed_statuses`。

7. 同样在设置阶段，创建一个字典 `_terminal_errors` 来存储每个测试阶段是否应该立即失败的状态。

8. 获取当前测试项的 `_test_failed_statuses` 属性，如果不存在则使用空字典。

9. 更新 `_test_failed_statuses` 字典，将当前测试阶段的失败状态设置为 `result.failed`。

10. 将更新后的 `_test_failed_statuses` 字典设置回测试项的属性。

11. 根据当前测试结果调用 `_should_hard_fail_on_error` 函数，判断是否应该立即失败，并更新 `item._terminal_errors` 字典。

12. 将更新后的 `_terminal_errors` 字典设置回测试项的属性。

这段代码的主要目的是在生成测试报告时，收集和更新关于测试失败状态和是否应该立即失败的信息。这些信息随后可以在其他钩子中使用，例如在 `pytest_runtest_teardown` 中，以决定是否需要清理测试状态或是否应该重新执行测试。通过在测试用例的设置阶段初始化这些属性，并在测试报告生成时更新它们，可以确保测试框架具有关于测试执行状态的准确信息。



## pytest_runtest_protocol



```python
def pytest_runtest_protocol(item, nextitem):
    """
    Run the test protocol.

    Note: when teardown fails, two reports are generated for the case, one for
    the test case and the other for the teardown error.
    """
    reruns = get_reruns_count(item)
    if reruns is None:
        # global setting is not specified, and this test is not marked with
        # flaky
        return

    # while this doesn't need to be run with every item, it will fail on the
    # first item if necessary
    check_options(item.session.config)
    delay = get_reruns_delay(item)
    parallel = not is_master(item.config)
    db = item.session.config.failures_db
    item.execution_count = db.get_test_failures(item.nodeid)
    db.set_test_reruns(item.nodeid, reruns)

    if item.execution_count > reruns:
        return True

    need_to_run = True
    while need_to_run:
        item.execution_count += 1
        item.ihook.pytest_runtest_logstart(nodeid=item.nodeid, location=item.location)
        reports = runtestprotocol(item, nextitem=nextitem, log=False)

        for report in reports:  # 3 reports: setup, call, teardown
            report.rerun = item.execution_count - 1
            if _should_not_rerun(item, report, reruns):
                # last run or no failure detected, log normally
                item.ihook.pytest_runtest_logreport(report=report)
            else:
                # failure detected and reruns not exhausted, since i < reruns
                report.outcome = "rerun"
                time.sleep(delay)

                if not parallel or works_with_current_xdist():
                    # will rerun test, log intermediate result
                    item.ihook.pytest_runtest_logreport(report=report)

                # cleanin item's cashed results from any level of setups
                _remove_cached_results_from_failed_fixtures(item)
                _remove_failed_setup_state_from_session(item)

                break  # trigger rerun
        else:
            need_to_run = False

        item.ihook.pytest_runtest_logfinish(nodeid=item.nodeid, location=item.location)

    return True
```

这段代码定义了 `pytest_runtest_protocol` 函数，它是 `pytest` 测试框架中的一个核心钩子（`hook`）实现，用于控制测试的执行流程，包括处理测试的重试逻辑。代码解读：

1. 函数签名 `pytest_runtest_protocol(item, nextitem)`：这个函数作为 pytest 的钩子，接受两个参数，`item` 是当前测试项，`nextitem` 是下一个将要执行的测试项。

2. 调用 `get_reruns_count(item)` 来获取当前测试项的重试次数。

3. 如果 `reruns` 是 `None`，则表示没有设置全局重试次数，并且当前测试项没有使用 `flaky` 标记指定重试，因此不需要执行重试逻辑，函数返回。

4. 调用 `check_options(item.session.config)` 来检查配置选项是否兼容。

5. 调用 `get_reruns_delay(item)` 来获取重试之间的延迟时间。

6. 调用 `is_master(item.config)` 来确定是否在主进程中运行，如果不是，则为 `True`，表示在并行环境中。

7. 从 `item.session.config` 获取 `failures_db`，这是用于跟踪测试失败和重试次数的数据库实例。

8. 获取当前测试项的失败次数，并设置到 `item.execution_count`。

9. 设置当前测试项的重试次数到数据库。

10. 如果 `item.execution_count` 大于 `reruns`，则不再需要重试，函数返回 `True`。

11. 初始化 `need_to_run` 为 `True`，用于控制循环是否继续执行。

12. 使用 `while` 循环来处理测试的执行和重试逻辑。

13. 每次循环开始时，增加 `item.execution_count`。

14. 使用 `item.ihook.pytest_runtest_logstart` 记录测试开始日志。

15. 调用 `runtestprotocol` 函数执行测试协议，`log=False` 表示不记录日志。

16. 遍历 `runtestprotocol` 返回的报告列表（可能包括 `setup, call, teardown` 报告）。

17. 对于每个报告，设置 `rerun` 属性为当前重试次数减一。

18. 调用 `_should_not_rerun` 函数检查是否不应该重试测试。

19. 如果不应该重试，使用 `item.ihook.pytest_runtest_logreport` 记录报告。

20. 如果应该重试并且还没有达到重试次数限制，将报告的 `outcome` 设置为 `"rerun"`。

21. 如果在并行环境中或者 `works_with_current_xdist()` 返回 `True`，则记录中间结果。

22. 调用 `_remove_cached_results_from_failed_fixtures(item)` 清理缓存结果。

23. 调用 `_remove_failed_setup_state_from_session(item)` 清理会话的设置状态。

24. `break` 语句触发重试。

25. 如果没有进入 `for` 循环的 `else` 块，说明没有检测到失败或不需要重试，设置 `need_to_run` 为 `False` 退出循环。

26. 使用 `item.ihook.pytest_runtest_logfinish` 记录测试结束日志。

27. 函数返回 `True`，表示钩子逻辑正常结束。

这个函数的逻辑是在 `pytest` 的测试执行流程中，根据测试项的重试设置来控制测试的执行和重试。通过循环和条件判断，实现了在测试失败时重试测试的功能，并在重试之间添加了延迟。此外，还处理了并行测试环境中的重试逻辑，确保测试可以在适当的条件下重新执行。



## pytest_report_teststatus



```python
def pytest_report_teststatus(report):
    # Adapted from https://pytest.org/latest/_modules/_pytest/skipping.html
    if report.outcome == "rerun":
        return "rerun", "R", ("RERUN", {"yellow": True})
```



这段代码定义了一个名为 `pytest_report_teststatus` 的函数，它是 `pytest` 测试框架中的一个钩子（`hook`）实现，用于报告测试的状态。这个特定的实现是用来处理测试重新运行（rerun）的状态报告。代码解读如下：

1. 函数签名 `pytest_report_teststatus(report)`：这个函数作为 `pytest` 的钩子，接受一个参数 `report`，它是当前测试项的报告对象，包含了测试的执行结果和状态。

2. 检查 `report` 对象的 `outcome` 属性是否等于 `"rerun"`。`outcome` 属性表示测试的最终结果，`"rerun"` 是一个自定义的结果，表示测试需要重新运行。

3. 如果 `outcome` 是 `"rerun"`，函数返回一个包含三个元素的元组：
   - 第一个元素是状态字符串 `"rerun"`，表示测试的状态是重新运行。
   - 第二个元素是状态的简短表示 `"R"`，这个简短表示可能会在测试报告中使用。
   - 第三个元素是一个元组，包含两个部分：
     - 一个字符串 `"RERUN"`，表示测试重新运行的文本描述。
     - 一个字典 `{"yellow": True}`，指定了文本描述的颜色样式，这里是黄色。

这个函数的主要作用是在 `pytest` 的测试报告中添加对 `"rerun"` 状态的支持。当测试因为失败而被标记为需要重新运行时，这个状态会通过 pytest 的报告系统传递，并在最终的测试报告中以特定的样式显示。这为用户提供了清晰的反馈，说明哪些测试因为失败而被自动重新执行。



## pytest_terminal_summary



```python
def pytest_terminal_summary(terminalreporter):
    # Adapted from https://pytest.org/latest/_modules/_pytest/skipping.html
    tr = terminalreporter
    if not tr.reportchars:
        return

    lines = []
    for char in tr.reportchars:
        if char in "rR":
            show_rerun(terminalreporter, lines)

    if lines:
        tr._tw.sep("=", "rerun test summary info")
        for line in lines:
            tr._tw.line(line)
```



`pytest_terminal_summary` 是一个 `pytest` 钩子函数，通常用于在测试运行结束时向终端报告测试的摘要信息。这个特定的实现是用来在终端报告中添加关于测试重试的摘要信息。

这段代码解读如下：

1. **函数定义**：
   - `pytest_terminal_summary(terminalreporter)`：这个函数接收一个参数 `terminalreporter`，它是 `pytest` 的终端报告器对象，负责向终端输出报告信息。

2. **检查报告字符**：
   - `if not tr.reportchars: return`：如果 `terminalreporter` 的 `reportchars` 属性为空，函数直接返回。`reportchars` 是一个字符串，包含了测试结果的单字符表示，例如 `"."` 表示通过，`"F"` 表示失败，`"r"` 或 `"R"` 可能表示重试。

3. **收集重试信息**：
   - `lines = []`：初始化一个列表 `lines`，用来收集关于重试测试的信息。
   - `for char in tr.reportchars:`：遍历 `reportchars` 中的每个字符。
   - `if char in "rR":`：如果字符是 `"r"` 或 `"R"`，表明有测试用例需要重试或已经重试。

4. **展示重试信息**：
   - `show_rerun(terminalreporter, lines)`：调用 `show_rerun` 函数（未在代码中定义，可能是自定义函数），传入 `terminalreporter` 和 `lines` 来收集需要展示的重试信息。

5. **报告重试摘要**：
   - `if lines:`：如果 `lines` 非空，说明有重试信息需要展示。
   - `tr._tw.sep("=", "rerun test summary info")`：使用 `_tw.sep` 方法输出一个分隔线，标题为 "rerun test summary info"。
   - `for line in lines:`：遍历 `lines` 中的每一行信息。
   - `tr._tw.line(line)`：使用 `_tw.line` 方法输出每一行重试信息。

这个函数的主要作用是在测试结束时，如果存在重试的测试用例，就在终端报告中添加一个重试测试的摘要部分。这为用户提供了关于哪些测试用例被重试以及可能的结果的额外信息。



## show_rerun



```python

def show_rerun(terminalreporter, lines):
    rerun = terminalreporter.stats.get("rerun")
    if rerun:
        for rep in rerun:
            pos = rep.nodeid
            lines.append(f"RERUN {pos}")
```



这段代码定义了一个名为 `show_rerun` 的函数，它的作用是收集并展示在 `pytest` 测试运行中被重试的测试用例的信息。

这段代码的解读如下所示：

1. **函数定义**：
   - `show_rerun(terminalreporter, lines)`：这个函数接收两个参数，`terminalreporter` 是 `pytest` 的终端报告器对象，用于访问测试统计信息；`lines` 是一个列表，用来收集重试测试用例的信息。

2. **获取重试测试的统计信息**：
   - `rerun = terminalreporter.stats.get("rerun")`：从 `terminalreporter` 的 `stats` 字典中获取键为 `"rerun"` 的条目，这个条目包含了所有被标记为需要重试的测试报告。

3. **检查是否有重试的测试**：
   - `if rerun:`：如果存在重试的测试（即 `rerun` 不为空），则进入循环处理这些测试。

4. **遍历重试的测试报告**：
   - `for rep in rerun:`：遍历 `rerun` 列表中的每个测试报告对象。

5. **获取测试用例的位置信息**：
   - `pos = rep.nodeid`：从测试报告对象 `rep` 中获取 `nodeid` 属性，这是一个字符串，唯一标识一个测试用例。

6. **收集重试测试的信息**：
   - `lines.append(f"RERUN {pos}")`：使用 `f` 字符串格式化，创建一个包含 "RERUN" 和测试用例位置信息的字符串，并将其添加到 `lines` 列表中。

这个函数的主要作用是将被重试的测试用例的信息收集起来，并将这些信息以列表的形式返回，供 `pytest_terminal_summary` 函数在终端报告中展示。通过这种方式，用户可以清晰地看到哪些测试用例在测试运行中失败了并且被自动重试。



# 结语

`pytest-rerunfailures` 是一个 `pytest` 插件，用于在测试失败后自动重新运行测试，直到成功或达到最大重试次数。

1. **插件初始化与配置**：
   - 插件通过钩子函数（如 `pytest_configure`）进行初始化。
   - 它检查是否与其他插件（如 `pytest-xdist`）兼容，并根据配置设置初始化数据库（`StatusDB`）来跟踪测试失败和重试状态。

2. **测试重试逻辑**：
   - 通过 `pytest_runtest_protocol` 钩子实现测试重试逻辑。
   - 根据测试项的 `flaky` 标记或全局配置获取重试次数。
   - 在测试失败时，根据设定的条件和重试次数决定是否重新执行测试。

3. **数据库操作**：
   - 使用 `StatusDB` 类及其子类（如 `ServerStatusDB` 和 `ClientStatusDB`）来存储和检索测试的失败次数和重试设置。
   - 数据库操作包括设置和获取测试的失败次数及重试次数。

4. **条件评估**：
   - 通过 `evaluate_condition` 函数评估 `flaky` 标记中的条件表达式，决定是否应该对测试进行重试。

5. **错误处理与匹配**：
   - 使用正则表达式匹配测试错误，确定哪些错误应该触发重试，哪些不应该。

6. **测试设置与清理**：
   - 在测试重试之前，清理测试项的缓存结果和会话状态，确保测试环境的一致性。

7. **测试报告**：
   - 通过 `pytest_report_teststatus` 钩子自定义测试报告的状态，例如添加 `"rerun"` 状态。

8. **并行测试支持**：
   - 当与 `pytest-xdist` 插件一起使用时，`pytest-rerunfailures` 插件支持在并行测试环境中运行。

9. **兼容性检查**：
   - 插件会检查当前环境和依赖项的兼容性，确保重试逻辑正确执行。

10. **用户配置**：
    - 用户可以通过 pytest 命令行选项或配置文件设置重试次数、延迟等参数。

`pytest-rerunfailures` 插件的源码实现了一套完整的机制，用于处理测试的自动重试，包括条件评估、错误匹配、数据库跟踪、报告自定义等。它提供了一种强大的方式，以自动化测试流程，提高测试的可靠性和效率。

---
title: pytest hook系列之pytest_enter_pdb
date: 2024-10-21 23:00:00
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
summary: pytest hook之pytest_enter_pdb
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest_enter_pdb` 是 `pytest` 框架中的一个钩子函数，当你在测试过程中调用 `pdb.set_trace()` 进入 `Python` 调试器 (`pdb`) 的交互模式时，它会被触发。通过这个钩子函数，你可以在进入调试模式之前执行一些自定义操作，例如设置调试环境、记录调试事件，或者打印调试信息，设置断点之前的一些预处理等。

# 参数

```python
def pytest_enter_pdb(config: "Config", pdb: "pdb.Pdb") -> None:
    """当调用 pdb.set_trace() 时被调用。

    由插件使用来在进入 python 调试器交互模式之前采取特殊行动。

    :param config: pytest 配置对象
    :param pdb: Pdb 类实例
    """
```

- `config`：`pytest` 配置对象，包含当前 `pytest` 会话的配置信息。
- `pdb`：`Pdb` 类实例，用于控制调试器的行为。

# 使用场景

1. **预设调试环境**：在进入调试模式之前，预设一些调试环境变量，提高调试效率。
2. **记录调试事件**：在进入调试模式时记录调试事件，以便后期分析调试的频率和原因。
3. **打印调试信息**：在进入调试模式时打印额外的信息，如当前变量状态、函数调用栈等，有助于对问题定位。

# 示例代码

## 案例一：预设调试环境

目标：在进入调试模式前，预设一些调试环境变量。

步骤：
1. 使用 `pytest_enter_pdb` 钩子函数。
2. 在钩子函数中设置调试环境变量。

**示例代码**：

```python
# conftest.py
import pytest

def pytest_enter_pdb(config, pdb):
    """预设调试环境变量"""
    print("Entering PDB: setting up debug environment variables...")
    pdb.set_trace()

# tests/test_example.py 测试示例
def test_addition():
    assert 1 + 1 == 2  # 这个测试用例应该通过

def test_division_by_zero():
    assert 1 / 0  # 这将引发一个ZeroDivisionError，触发调试模式

def test_subtraction():
    assert 2 - 1 == 1  # 这个测试用例应该通过
```

**解释：**

- 使用 `print` 语句打印进入调试模式的信息。
- 使用 `pdb.set_trace()` 设置断点。


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
Entering PDB: setting up debug environment variables...
--Return--
> /root/test/hook/conftest.py(6)pytest_enter_pdb()->None
-> pdb.set_trace()
(Pdb) 
```

上文中，显示了`(Pdb)`，如果想自定义这里的显示，可参考如下代码示例：

```python
import pytest

def pytest_enter_pdb(config, pdb):
    """预设调试环境变量"""
    print("Entering PDB: setting up debug environment variables...")
    # 设置一些调试环境变量
    pdb.prompt = '(MyCustomPdb) '
    print("Environment Ready")
    pdb.set_trace()
```

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
Entering PDB: setting up debug environment variables...
Environment Ready
--Return--
> /root/test/hook/conftest.py(15)pytest_enter_pdb()->None
-> pdb.set_trace()
(MyCustomPdb)
```

## 案例二：记录调试事件

目标：在进入调试模式时记录调试事件，包括调试开始时间、触发调试的测试用例等。

步骤：
1. 使用 `pytest_enter_pdb` 钩子函数。
2. 在钩子函数中记录调试事件到日志文件中。

**示例代码**：

```python
# conftest.py
import pytest
import logging
from datetime import datetime
import inspect

# 配置日志记录
logging.basicConfig(filename='debug_events.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def pytest_enter_pdb(config, pdb):
    """记录调试事件到日志文件"""
    # 获取当前帧
    current_frame = inspect.currentframe().f_back
    test_nodeid = current_frame.f_globals.get('__name__', 'Unknown')
    logging.info(f"Entering PDB for test: {test_nodeid} at {datetime.now()}")
    print("Entering PDB and logging debug event...")
```

**解释**：

- 使用 `logging` 模块配置日志记录，将日志输出到 `debug_events.log` 文件中。
- 在 `pytest_enter_pdb` 钩子函数中，获取当前测试节点信息并记录调试事件。

**运行效果**：

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
Entering PDB and logging debug event...
> /root/test/hook/tests/test_example.py(16)test_division_by_zero()
-> assert 1 / 0  # 这将引发一个ZeroDivisionError，触发调试模式
(Pdb) exit()


================================================================================================================ short test summary info ================================================================================================================
FAILED tests/test_example.py::test_division_by_zero - ZeroDivisionError: division by zero
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! _pytest.outcomes.Exit: Quitting debugger !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
============================================================================================================== 1 failed, 1 passed in 4.57s ==============================================================================================================
root@Gavin:~/test/hook# 
```

日志文件内容：

```shell
root@Gavin:~/test/hook# cat debug_events.log 
2024-10-21 17:27:54,054 - INFO - Entering PDB for test: pluggy._callers at 2024-10-21 17:27:54.054009
root@Gavin:~/test/hook#
```


## 案例三：打印调试信息

目标：在进入调试模式时打印当前的变量状态或函数调用栈，有利于快速定位问题。

步骤：
1. 使用 `pytest_enter_pdb` 钩子函数。
2. 在钩子函数中获取并打印当前变量值或函数调用栈。

**示例代码**：

```python
# conftest.py
import pytest
import traceback
import inspect

def pytest_enter_pdb(config, pdb):
    """打印额外的调试信息"""
    current_frame = inspect.currentframe().f_back
    print("\nEntering PDB: printing extra debug information...")

    # 打印当前变量状态
    local_vars = current_frame.f_locals
    print("Local Variables:")
    for var, value in local_vars.items():
        print(f"{var}: {value}")

    # 打印函数调用栈
    stack_trace = ''.join(traceback.format_stack(current_frame))
    print("\nStack Trace:")
    print(stack_trace)
    
    pdb.set_trace()
```

**解释**：
- 使用 `pdb.curframe` 获取当前堆栈帧。
- 打印当前局部变量和函数调用栈，以帮助调试。

**运行效果:**

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

Entering PDB: printing extra debug information...
Local Variables:
hook_name: pytest_enter_pdb
hook_impls: [<HookImpl plugin_name='timeout', plugin=<module 'pytest_timeout' from '/usr/local/lib/python3.11/dist-packages/pytest_timeout.py'>>, <HookImpl plugin_name='/root/test/hook/conftest.py', plugin=<module 'conftest' from '/root/test/hook/conftest.py'>>, <HookImpl plugin_name='faulthandler', plugin=<module '_pytest.faulthandler' from '/usr/local/lib/python3.11/dist-packages/_pytest/faulthandler.py'>>]
caller_kwargs: {'config': <_pytest.config.Config object at 0x765296c154d0>, 'pdb': <_pytest.debugging.pytestPDB._get_pdb_wrapper_class.<locals>.PytestPdbWrapper object at 0x765294024cd0>}
firstresult: False
__tracebackhide__: True
results: []
exception: None
only_new_style_wrappers: True
teardowns: []
hook_impl: <HookImpl plugin_name='/root/test/hook/conftest.py', plugin=<module 'conftest' from '/root/test/hook/conftest.py'>>
args: [<_pytest.config.Config object at 0x765296c154d0>, <_pytest.debugging.pytestPDB._get_pdb_wrapper_class.<locals>.PytestPdbWrapper object at 0x765294024cd0>]
res: None

Stack Trace:
  File "/usr/local/bin/pytest", line 8, in <module>
    sys.exit(console_main())
  File "/usr/local/lib/python3.11/dist-packages/_pytest/config/__init__.py", line 198, in console_main
    code = main()
  File "/usr/local/lib/python3.11/dist-packages/_pytest/config/__init__.py", line 175, in main
    ret: Union[ExitCode, int] = config.hook.pytest_cmdline_main(
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_hooks.py", line 513, in __call__
    return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_manager.py", line 120, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
    res = hook_impl.function(*args)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 320, in pytest_cmdline_main
    return wrap_session(config, _main)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 273, in wrap_session
    session.exitstatus = doit(config, session) or 0
  File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 327, in _main
    config.hook.pytest_runtestloop(session=session)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_hooks.py", line 513, in __call__
    return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_manager.py", line 120, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
    res = hook_impl.function(*args)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/main.py", line 352, in pytest_runtestloop
    item.config.hook.pytest_runtest_protocol(item=item, nextitem=nextitem)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_hooks.py", line 513, in __call__
    return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_manager.py", line 120, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
    res = hook_impl.function(*args)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/runner.py", line 115, in pytest_runtest_protocol
    runtestprotocol(item, nextitem=nextitem)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/runner.py", line 134, in runtestprotocol
    reports.append(call_and_report(item, "call", log))
  File "/usr/local/lib/python3.11/dist-packages/_pytest/runner.py", line 229, in call_and_report
    hook.pytest_exception_interact(node=item, call=call, report=report)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_hooks.py", line 513, in __call__
    return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_manager.py", line 120, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
    res = hook_impl.function(*args)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/debugging.py", line 300, in pytest_exception_interact
    _enter_pdb(node, call.excinfo, report)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/debugging.py", line 367, in _enter_pdb
    post_mortem(tb)
  File "/usr/local/lib/python3.11/dist-packages/_pytest/debugging.py", line 388, in post_mortem
    p = pytestPDB._init_pdb("post_mortem")
  File "/usr/local/lib/python3.11/dist-packages/_pytest/debugging.py", line 276, in _init_pdb
    cls._pluginmanager.hook.pytest_enter_pdb(config=cls._config, pdb=_pdb)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_hooks.py", line 513, in __call__
    return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_manager.py", line 120, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
  File "/usr/local/lib/python3.11/dist-packages/pluggy/_callers.py", line 103, in _multicall
    res = hook_impl.function(*args)

--Return--
> /root/test/hook/conftest.py(21)pytest_enter_pdb()->None
-> pdb.set_trace()
(Pdb)
```


### 详细解释和总结

1. **预设调试环境**：
   - 使用 `pytest_enter_pdb` 钩子，在进入 `pdb` 调试模式前设置环境变量或执行特定命令。

2. **记录调试事件**：
   - 使用 `pytest_enter_pdb` 钩子，在进入 `pdb` 调试模式时记录调试事件到日志文件中，包括测试节点信息和时间戳。

3. **打印调试信息**：
   - 使用 `pytest_enter_pdb` 钩子，在进入 `pdb` 调试模式时，打印当前局部变量和函数调用栈，有助于快速定位问题。



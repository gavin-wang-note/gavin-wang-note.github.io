---
title: pytest hook系列之pytest_cmdline_parse
date: 2024-09-05 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-18.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_cmdline_parse
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation

---

# Overview

`pytest_cmdline_parse` 是一个钩子函数，用于在解析命令行选项之前调用。这个钩子函数主要用于在解析命令行前进行一些预处理，如修改或添加命令行参数，或者根据初步解析的参数进行一些额外的配置。


# 使用场景

* 修改命令行参数：在正式解析命令行参数之前修改或增加参数。
* 预处理输入：在命令行参数被解析成配置之前进行一些预处理工作。
* 添加动态选项：根据检测到的环境或者其他初步信息，动态添加或者更改选项。


# 参数

* pluginmanager: pytest 的插件管理器实例，用于管理插件、钩子和命令行选项
* args: 命令行传递的参数列表


# 注意点

官方源码中有做使用说明，如下：

```shell
@hookspec(firstresult=True)
def pytest_cmdline_parse(
    pluginmanager: "PytestPluginManager", args: List[str]
) -> Optional["Config"]:
    """Return an initialized :class:`~pytest.Config`, parsing the specified args.

    Stops at first non-None result, see :ref:`firstresult`.

    .. note::
        This hook will only be called for plugin classes passed to the
        ``plugins`` arg when using `pytest.main`_ to perform an in-process
        test run.

    :param pluginmanager: The pytest plugin manager.
    :param args: List of arguments passed on the command line.
    :returns: A pytest config object.
    """
```

意思是说：这个钩子只会在使用 `pytest.main` 执行测试时，并且 `plugins` 参数中明确传递了插件类的情况下才会被调用。

# 示例代码

假设你有一个插件，你希望只在通过 `pytest.main` 调用 `pytest` 时，利用 `pytest_cmdline_parse` 修改命令行参数。以下是实现该需求的详细步骤：

## 定义插件类


首先，定义一个插件类，并在其中实现 `pytest_cmdline_parse` 钩子方法。

```python
# my_plugin.py
import pytest
from typing import List
from _pytest.config import PytestPluginManager, Config
from _pytest.config.argparsing import Parser

class MyPlugin:
    
    @pytest.hookimpl
    def pytest_addoption(self, parser: Parser):
        parser.addoption(
            "--custom-option", action="store", default="default_value",
            help="A custom command line option for pytest"
        )

    @pytest.hookimpl
    def pytest_cmdline_preparse(self, config: Config, args: List[str]):
        # 在命令行选项被解析前修改参数
        if "--custom-option" not in [arg.split('=')[0] for arg in args]:
            args.append("--custom-option=auto_inserted_value")
        print("Modified arguments:", args)

    @pytest.hookimpl
    def pytest_configure(self, config: Config):
        custom_option = config.getoption("--custom-option")
        print(f"Custom option value: {custom_option}")
```


## 编写测试用例 test_example.py


编写一个简单的测试用例，访问并验证自定义选项。

```python
# test_example.py
def test_custom_option(pytestconfig):
    custom_option = pytestconfig.getoption("--custom-option")
    assert custom_option == "auto_inserted_value"
```

## 运行示例


通过调用 `pytest.main` 函数并传递插件来运行测试。

```python
# run_tests.py
import pytest
from my_plugin import MyPlugin

if __name__ == "__main__":
    pytest.main(["-s", "test_example.py"], plugins=[MyPlugin()])
```

## 详细说明

### my_plugin.py：

在这里，我们定义了一个插件类 `MyPlugin`，并在其中实现了 `pytest_cmdline_parse` 钩子。该方法在命令行选项被解析前将自动添加自定义选项（如果不存在），并打印修改后的命令行参数。我们还定义了 pytest_addoption 方法来添加自定义命令行选项，以及 `pytest_configure` 方法来读取和打印该选项的值。

### test_example.py：

编写一个简单的测试用例 `test_custom_option`，通过 `pytestconfig` 对象获取并验证自定义选项的值。

## run_tests.py：

通过调用 `pytest.main` 函数并传递 `MyPlugin` 插件来运行测试。运行此脚本将触发 `pytest` 流程，并按预期修改和验证命令行参数。


# 运行示例

可以通过运行 `run_tests.py `来验证：

```shell
python3 run_tests.py
```

控制台输出将会显示最终的命令行参数和选项值，并运行测试：

```plaintext
root@Gavin:~/test/hook# python3 run_tests.py 
Modified arguments: ['-s', 'test_example.py', '--custom-option=auto_inserted_value']
Custom option value: auto_inserted_value
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                         

test_example.py .

=================================================================================================================== 1 passed in 0.03s ====================================================================================================================
root@Gavin:~/test/hook#
```

# 小结

通过使用 `pytest.main` 并传递 `plugins` 参数，可以在特定插件类中实现 `pytest_cmdline_parse` 钩子，并确保该钩子在命令行解析之前按预期修改参数。这种方法适用于通过程序控制执行 `pytest`，而不是直接使用命令行运行 `pytest`。

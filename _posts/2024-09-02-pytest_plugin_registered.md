---
title: pytest hook系列之pytest_plugin_registered
date: 2024-09-02 23:00:00
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
summary: pytest hook之pytest_plugin_registered
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation

---

# Overview

`pytest_plugin_registered` 是一个钩子函数，用于在插件被注册后立即调用。它可以用于在插件注册后执行一些初始化操作，例如设置某些配置或验证插件的状态。了解这个钩子对于编写复杂的 `pytest` 插件系统或调试插件行为是非常有用的。

# 使用场景

* 插件初始化：在插件注册后立即进行一些初始化操作
* 插件依赖检查：在插件注册后检查它的依赖是否满足
* 插件配置：在插件注册后为其配置某些特定参数或状态
* 调试和日志记录：注册日志记录插件，记录安装了哪些插件以及何时安装


# 参数

* `plugin`: 被注册的插件实例(`The plugin module or instance.`)
* `manager`: 管理所有插件注册和调用的插件管理器实例(`pytest.PytestPluginManager manager: pytest plugin manager.`)

**note::**

`This hook is incompatible with hookwrapper=True`.


# 示例代码

以下是一个使用 `pytest_plugin_registered` 的示例，展示如何在插件注册后立即进行某些操作：

## 定义和注册插件

```python
# my_plugin.py
def pytest_configure(config):
    print("my_plugin: Configured!")

# conftest.py
def pytest_addoption(parser):
    parser.addoption("--my-option", action="store", default="default_value", help="Some option for my plugin")

def pytest_plugin_registered(plugin, manager):
    print(f"Plugin {plugin} has been registered with manager {manager}")
    if hasattr(plugin, 'pytest_configure'):
        print(f"Plugin {plugin} has 'pytest_configure' method")
    else:
        print(f"Plugin {plugin} does not have 'pytest_configure' method")

# 注册插件
pytest_plugins = ["my_plugin"]
```

## 测试插件


```python
# test_plugin.py
import pytest

def test_example():
    assert True
```

**说明:**

* `my_plugin.py`: 定义了一个插件，包含`pytest_configure`钩子，用于在`pytest`配置完成后执行一些操作。
* `conftest.py`: 在`conftest.py`中，定义了`pytest_addoption`钩子和`pytest_plugin_registered`钩子。在插件注册后，将会调用`pytest_plugin_registered`钩子，并检查插件是否具有`pytest_configure`方法。
* `test_plugin.py`: 一个简单的测试用例文件，用于触发`pytest`的运行，通过它来验证插件是否正确注册和初始化。



# 运行效果

使用以下命令运行测试并观察输出：

```shell
pytest -s
```

你会在控制台中看到类似以下的输出：

```plaintext
Plugin <_pytest.terminal.TerminalReporter object at 0x71875e3d40d0> has been registered with manager <_pytest.config.PytestPluginManager object at 0x718761df6310>
Plugin <_pytest.terminal.TerminalReporter object at 0x71875e3d40d0> does not have 'pytest_configure' method
Plugin <_pytest.logging.LoggingPlugin object at 0x71875e3d4fd0> has been registered with manager <_pytest.config.PytestPluginManager object at 0x718761df6310>
Plugin <_pytest.logging.LoggingPlugin object at 0x71875e3d4fd0> does not have 'pytest_configure' method
Plugin <_pytest.fixtures.FixtureManager object at 0x71875e3c7d50> has been registered with manager <_pytest.config.PytestPluginManager object at 0x718761df6310>
Plugin <_pytest.fixtures.FixtureManager object at 0x71875e3c7d50> does not have 'pytest_configure' method
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                         

test_plugin.py .

=================================================================================================================== 1 passed in 0.04s ====================================================================================================================
root@Gavin:~/test/hook#
```


# 小结

`pytest_plugin_registered` 钩子在插件被注册后立即调用，可以用于执行初始化操作、检查依赖、配置插件或者记录日志。通过这个钩子，可以更好地管理和调试 `pytest` 插件的行为，确保测试环境按预期工作。

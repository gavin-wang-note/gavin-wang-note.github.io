---
title: pytest hook系列之pytest_addhooks
date: 2024-09-01 23:00:00
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
summary: pytest hook之pytest_addhooks
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation

---


# Overview

`pytest_addhooks`是一个用来在`pytest`插件管理器中注册新的钩子的钩子函数。它允许用户或插件开发者定义自己的钩子接口，以便其他插件可以在测试运行过程中调用这些钩子。

# 使用场景

`pytest_addhooks`主要作用是注册新的钩子规范（`hook specifications`），这些钩子规范可以在后续的测试生命周期中被调用或实现，主要用于以下场景：

* 测试环境的准备和清理：在测试开始前设置环境，测试结束后清理环境
* 测试配置：根据测试需求动态调整 `pytest` 的配置
* 测试数据的准备：为测试函数提供必要的测试数据
* 测试结果的收集和处理：在测试执行后收集和处理测试结果
* 错误和异常的处理：自定义错误和异常的处理逻辑


参数：

`pytest_addhooks` 函数接受一个参数：

* `pluginmanager`：这是`pytest`的插件管理器对象，通过这个对象，你可以注册自定义的钩子函数(这个参数是一个对象，负责管理所有已注册的插件及其钩子函数)。



# 示例代码与注释

以下是一个如何使用`pytest_addhooks`注册自定义钩子的示例：

## 创建一个钩子规范文件 my_hookspec.py


```python
# my_hookspec.py
import pytest

# 定义一个钩子规范
@pytest.mark.tryfirst
def pytest_my_custom_hook(arg1, arg2):
    """This is my custom hook. It will receive two arguments."""
    pass
```

## 在conftest.py中使用 pytest_addhooks 注册这个钩子


```python
# conftest.py
def pytest_addhooks(pluginmanager):
    # Register the hook specification from my_hookspec.py
    import my_hookspec
    pluginmanager.add_hookspecs(my_hookspec)
```

## 创建一个插件或直接在conftest.py中实现这个钩子


```python
# my_plugin.py or conftest.py if you are not using a separate plugin file
def pytest_my_custom_hook(arg1, arg2):
    print(f"Custom hook called with arguments: {arg1}, {arg2}")
```

## 在测试或运行代码中调用这个钩子

```python
# test_custom_hook.py
def test_example(request):
    # 调用自定义的钩子并传递参数
    request.config.hook.pytest_my_custom_hook(arg1='Hello', arg2='World')
```

# 综合示例

以下是一个完整的代码示例，展示如何定义、注册和调用自定义钩子：

## 定义钩子规范

```python
# my_hookspec.py
import pytest

# 定义一个钩子规范
@pytest.mark.tryfirst
def pytest_my_custom_hook(arg1, arg2):
    """This is my custom hook. It will receive two arguments."""
    pass
```

## 注册钩子规范

```python
# conftest.py
def pytest_addhooks(pluginmanager):
    # Register the hook specification from my_hookspec
    import my_hookspec
    pluginmanager.add_hookspecs(my_hookspec)

def pytest_my_custom_hook(arg1, arg2):
    print(f"Custom hook called with arguments: {arg1}, {arg2}")
```

## 调用自定义钩子

```python
# test_custom_hook.py
def test_example(request):
    # 调用自定义的钩子并传递参数
    request.config.hook.pytest_my_custom_hook(arg1='Hello', arg2='World')
    assert True
```

执行效果参考如下：

```shell
test_custom_hook.py::test_example Custom hook called with arguments: Hello, World
PASSED
```

# 小结

使用`pytest_addhooks`可以让你定义和注册自定义钩子，这些钩子可以在测试生命周期的不同阶段被调用，以提供额外的功能和扩展性。通过正确地设置和调用这些钩子，你可以让`pytest`框架适应你的具体需求。

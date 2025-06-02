---
title: pytest fixture应用：显式传递参数与使用 request 对象 
date: 2026-10-11 23:00:00
author: Gavin Wang
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 显式传递参数与使用 request 对象
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest` 中使用 `Fixture` 的两种方法：显式传递参数与使用 `request` 对象。

在使用 `pytest` 编写测试用例时，`fixture` 是一个非常强大的功能，用于提供测试数据、设置测试环境等。本文将详细介绍两种常见的使用 `fixture` 的方法：显式传递参数 和 使用 `request` 对象。我们将通过完整的示例代码和详细的解释，帮助你理解这两种方法的应用场景和实现方式。

# 显式传递参数

## 1. 方法介绍

显式传递参数是最直接的方式。在这种方法中，我们将 `fixture` 作为参数直接传递给测试用例。这种方式简单直观，适合大多数场景。

## 2. 示例代码

```python
import pytest

# 定义一个 fixture，返回多个值
@pytest.fixture(scope="class")
def my_fixture():
    print("Setting up fixture")
    yield "param1", "param2", "param3"
    print("Tearing down fixture")

# 测试类
class TestMyClass:
    def test_case1(self, my_fixture):
        """测试用例1：显式传递 fixture"""
        param1, param2, param3 = my_fixture
        print(f"Test case 1: param1={param1}, param2={param2}, param3={param3}")
        assert param1 == "param1"
        assert param2 == "param2"
        assert param3 == "param3"

    def test_case2(self, my_fixture):
        """测试用例2：显式传递 fixture"""
        param1, param2, param3 = my_fixture
        print(f"Test case 2: param1={param1}, param2={param2}, param3={param3}")
        assert param1 == "param1"
        assert param2 == "param2"
        assert param3 == "param3"
```

## 3. 代码解释

`fixture` 定义：

`my_fixture` 是一个 `fixture`，其 `scope` 设置为 `class`，表示这个 `fixture` 的生命周期是整个测试类。

使用 `yield` 返回多个值："param1", "param2", "param3"。

测试用例：

在每个测试用例中，`my_fixture` 被显式地作为参数传递。
通过解包的方式，将 `fixture` 返回的值赋给测试用例中的变量。

输出：

```shell
Setting up fixture
Test case 1: param1=param1, param2=param2, param3=param3
Test case 2: param1=param1, param2=param2, param3=param3
Tearing down fixture
```

## 4. 适用场景

适用于需要在测试用例中直接使用 `fixture` 返回值的场景。
适合简单的测试场景，代码清晰易读。

# 使用 request 对象

## 1. 方法介绍

在某些情况下，我们希望将 `fixture` 的返回值绑定到测试类的属性中，这样可以在测试用例中通过类的属性访问这些值。这时可以使用 `request` 对象，通过 `request.cls` 将返回值存储为类的属性。

## 2. 示例代码

```python
import pytest

# 定义一个 fixture，返回多个值，并将其绑定到类的属性
@pytest.fixture(scope="class", autouse=True)
def my_fixture(request):
    print("Setting up fixture")
    # 将返回值绑定到类的属性
    request.cls.param1 = "param1"
    request.cls.param2 = "param2"
    request.cls.param3 = "param3"
    yield
    print("Tearing down fixture")

# 测试类
class TestMyClass:
    def setup_method(self):
        """在每个测试用例执行前调用"""
        # 从类的属性中获取 fixture 的返回值
        self.param1 = self.__class__.param1
        self.param2 = self.__class__.param2
        self.param3 = self.__class__.param3
        print(f"Setup method: param1={self.param1}, param2={self.param2}, param3={self.param3}")

    def test_case1(self):
        """测试用例1：通过类的属性访问 fixture 的返回值"""
        print(f"Test case 1: param1={self.param1}, param2={self.param2}, param3={self.param3}")
        assert self.param1 == "param1"
        assert self.param2 == "param2"
        assert self.param3 == "param3"
    
    def test_case2(self):
        """测试用例2：通过类的属性访问 fixture 的返回值"""
        print(f"Test case 2: param1={self.param1}, param2={self.param2}, param3={self.param3}")
        assert self.param1 == "param1"
        assert self.param2 == "param2"
        assert self.param3 == "param3"
```

## 3. 代码解释

`fixture` 定义：

`my_fixture` 是一个 `fixture`，其 `scope` 设置为 "class"，并且 `autouse=True`，表示这个 `fixture` 会自动应用于类中的所有测试用例。

使用 `request.cls` 将返回值绑定到类的属性：`request.cls.param1、request.cls.param2、request.cls.param3`

`setup_method` 方法：

在每个测试用例执行前，`setup_method` 会被调用。
通过 `self.__class__.param1、self.__class__.param2` 和 `self.__class__.param3` 获取类的属性值，并将其赋给实例变量。

测试用例：

在测试用例中，通过实例变量 `self.param1、self.param2` 和 `self.param3` 访问 `fixture` 的返回值。

输出：

```shell
Setting up fixture
Setup method: param1=param1, param2=param2, param3=param3
Test case 1: param1=param1, param2=param2, param3=param3
Test case 2: param1=param1, param2=param2, param3=param3
Tearing down fixture
```

## 4. 适用场景

适用于需要将 `fixture` 的返回值绑定到类的属性的场景。

适合需要在多个测试用例中共享某些资源的场景。

# 小结

## 1. 显式传递参数

优点：
- 代码简单直观，易于理解和维护。
- 适合大多数测试场景。

缺点：
- 如果需要在多个测试用例中共享 `fixture` 的返回值，可能会导致代码重复。

## 2. 使用 request 对象

优点：
- 可以将 `fixture` 的返回值绑定到类的属性，方便在多个测试用例中共享。
- 适合复杂的测试场景，代码更加灵活。

缺点：
- 需要使用 `request` 对象，代码稍微复杂一些。
- 需要手动在 `setup_method` 中获取类的属性值。

## 3. 选择建议

- 如果测试用例比较简单，推荐使用 显式传递参数 的方法，代码更加清晰易读。
- 如果需要在多个测试用例中共享 `fixture` 的返回值，或者测试场景比较复杂，推荐使用 `request` 对象 的方法，代码更加灵活。


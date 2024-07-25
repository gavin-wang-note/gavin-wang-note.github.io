---
title: pytest的yield和addfinalizer的区别 
date: 2026-03-20 22:00:00
author: Gavin Wang
img: "/img/pytest/pytest-24.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest的yield和addfinalizer的区别，以及如何规避addfinalizer使用上的一些坑
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

在`pytest`中，`yield`和`addfinalizer`两者都可以用于管理测试资源的初始化和清理，但它们有不同的用法和语法。

# yield 方式

`yield` 方式通常用于 `pytest fixture` 中，它的作用类似于传统的`setup` 和 `teardown` 方法。`yield` 语句会将控制权交还给测试用例，并且在测试用例运行结束后继续执行 `yield` 后面的清理代码。

## 示例代码

```python
import pytest

@pytest.fixture
def resource():
    # 初始化资源
    resource = "resource"
    print("Setup")

    # 把资源传给测试用例
    yield resource

    # 清理资源
    print("Teardown")
```

在测试用例中使用这个`fixture`：

```python
def test_example(resource):
    # 使用资源
    print("Test")
    assert resource == "resource"
```

## 执行顺序

1. 运行初始化代码（`print("Setup")`）。
2. 执行`yield`，并把`resource`返回给测试用例。
3. 测试用例运行（`print("Test")`）。
4. 测试用例结束后，执行`yield`后的清理代码（`print("Teardown")`）。

# addfinalizer 方式

`addfinalizer` 方法是通过在 `fixture` 中添加一个函数来实现清理代码的执行。这个方法通常用于需要多次清理或在不同的地方添加清理任务时。

## 示例代码

```python
import pytest

@pytest.fixture
def resource(request):
    # 初始化资源
    resource = "resource"
    print("Setup")

    # 定义清理函数
    def teardown():
        print("Teardown")

    # 将清理函数添加到 `request` 的finalizer
    request.addfinalizer(teardown)

    # 把资源传给测试用例
    return resource
```

在测试用例中使用这个`fixture`：

```python
def test_example(resource):
    # 使用资源
    print("Test")
    assert resource == "resource"
```

## 执行顺序

1. 运行初始化代码（`print("Setup")`）。
2. 将清理函数`teardown`注册到`request`的finalizer。
3. 返回`resource`给测试用例。
4. 测试用例运行（`print("Test")`）。
5. 测试用例结束后，调用`request` 的 `finalizer` 运行清理函数（`print("Teardown")`）。


# addfinalizer使用上有哪些坑？

尽管 `addfinalizer` 功能强大，但一些常见场景中的误用可能会导致问题，以下是对常见坑点的介绍及避免方法。

## 1. addfinalizer 中函数的闭包问题

闭包问题指的是在 `addfinalizer` 中注册的清理函数引用了外部变量，而外部变量在注册时之后发生了变化，这会导致清理函数的行为不正确。

### 示例代码

```python
import pytest

@pytest.fixture
def make_resource(request):
    resources = []

    def _make_resource(name):
        resource = f"resource {name}"
        resources.append(resource)

        def teardown():
            resources.remove(resource)
            print(f"Teardown resource {resource}")

        request.addfinalizer(teardown)
        return resource

    return _make_resource

def test_example(make_resource):
    res1 = make_resource("A")
    res2 = make_resource("B")

    assert res1 == "resource A"
    assert res2 == "resource B"
```

### 问题解析

这里我们定义了一个动态创建资源的 `fixture make_resource`，并使用 `addfinalizer` 注册了清理函数。由于闭包问题，可能会发生 `teardown` 使用错误的资源。

## 避坑方法：为每个资源单独定义清理函数，以避免闭包问题。

### 正确示例

```python
import pytest

@pytest.fixture
def make_resource(request):
    resources = []

    def _make_resource(name):
        resource = f"resource {name}"
        resources.append(resource)

        # 定义一个独立的清理函数，避免闭包问题
        def make_teardown(resource):
            def teardown():
                resources.remove(resource)
                print(f"Teardown resource {resource}")
            return teardown

        request.addfinalizer(make_teardown(resource))
        return resource

    return _make_resource

def test_example(make_resource):
    res1 = make_resource("A")
    res2 = make_resource("B")

    assert res1 == "resource A"
    assert res2 == "resource B"
```

## 2. 与多次调用 request.addfinalizer 相关的问题

多次调用 `addfinalizer` 不会按预期的顺序执行清理，且可能遗漏未正确注册的清理操作。

### 示例代码

```python
import pytest

@pytest.fixture
def resource(request):
    resource = "resource"

    def teardown1():
        print("Teardown step 1")
    request.addfinalizer(teardown1)

    def teardown2():
        print("Teardown step 2")
    request.addfinalizer(teardown2)

    return resource

def test_example(resource):
    assert resource == "resource"
```

### 问题解析

虽然多次调用 `addfinalizer` 是允许的，但在某些情况下，顺序执行的需求可能导致清理不一致或意外的清理顺序。

### 避坑方法：使用单个清理函数，并在其中按预期顺序调用清理步骤

#### 正确示例

```python
import pytest

@pytest.fixture
def resource(request):
    resource = "resource"

    def teardown():
        print("Teardown step 2")
        print("Teardown step 1")

    # 单个清理函数
    request.addfinalizer(teardown)

    return resource

def test_example(resource):
    assert resource == "resource"
```

## 3. 不立即执行 addfinalizer 清理

如果不立即调用 `addfinalizer` 注册的清理函数，可能会导致资源未正常清理。

### 示例代码

```python
import pytest

@pytest.fixture
def resource(request):
    resource = "resource"
    return resource

def test_example(request, resource):
    def teardown():
        print("Teardown resource")

    # 错误示例：未正确注册清理
    request.addfinalizer(teardown)

    assert resource == "resource"
```

### 避坑方法：确保在 fixture 中立即调用 addfinalizer

#### 正确示例

```python
import pytest

@pytest.fixture
def resource(request):
    resource = "resource"
    
    def teardown():
        print("Teardown resource")

    # 立即注册清理函数
    request.addfinalizer(teardown)

    return resource

def test_example(resource):
    assert resource == "resource"
```

## 4. 与 addfinalizer 进行的多线程并行操作

在多线程环境下，`addfinalizer` 的使用需要额外注意，多线程可能在清理过程中出现竞争条件。

### 示例代码

```python
import pytest
import threading

@pytest.fixture
def resource(request):
    resource = "resource"

    def teardown():
        print("Teardown resource")

    request.addfinalizer(teardown)
    return resource

def test_multithreading(request, resource):
    def worker():
        assert resource == "resource"

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
```

### 问题解析

由于 `teardown` 注册到主线程，可能导致多线程竞态条件。

## 综述

- **闭包问题**：在 `addfinalizer` 中添加的清理函数避免引用外部可变状态。
- **多次 `addfinalizer`**：在单个清理函数中操作所有清理步骤。
- **立即注册清理**：确保在 `fixture` 内立即调用 `addfinalizer` 注册清理。
- **多线程注意事项**：多线程可能导致竞态情况，需要仔细管理共享资源。

这些问题和坑点，在实际开发和测试中较为常见，理解和掌握这些避坑技巧，有助于提高测试代码的健壮性和可靠性。


# 小结

- `yield` 方式通过 `yield` 语句传递`fixture`，并在 `yield` 后执行清理代码。它的语法简单直观，适用于单一次资源清理。
- `addfinalizer` 方式通过 `request.addfinalizer` 方法注册一个清理函数，并在测试用例执行完毕后自动调用该函数。适用于需要在不同阶段添加多个清理任务的场景。

# 选择使用哪种方式

- **单次清理**：若资源的清理操作是单一的，可以使用 `yield` 语法，它更为简洁。
- **多次清理或动态绑定**：如果你有多个阶段或多次清理操作，或者在`fixture`的不同部分添加清理任务，可以使用 `addfinalizer` 方法。

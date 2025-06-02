---
title: 测试用例多重校验之pytest_check避坑
date: 2026-08-17 23:00:00
author: Gavin Wang
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest_check使用避坑
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 概述

目前自动化测试用例整体上是使用`python`内置的`assert`进行断言，由于产品会有迭代，下一个迭代产生的版本有一些功能点发生变化，伴随着一些`API`也会发生变化，从而引发用例`assert`失败，此时需要维护用例，适配版本。为了要弄清楚某个/些测试用例在执行过程中有哪些`assert`错误，单纯靠`assert`在效率上会慢一些（因为`assert`失败就终止了，修复了此次的`assert`接下来还有其他的`assert`），此时`pytest_check`插件提供的用例多种校验就派上用场了。

本文介绍在使用`pytest_check`装饰器`@check.check_func`上碰到的坑。


# 现象

测试类中使用`pytest_check`装饰器`@check.check_func`，作用在某个功能点的检查函数上，而此检查函数中有`return`动作，比如return一个`resourceId`，此`resourceId`供其他函数使用,伪代码参考如下：

测试用例:

```python
from testcasebase.resource_manage import ResourceManage


class TestResource(ResourceManage):
    """Test case of Resource"""
    def test_add_doc(self):
        """Add doc resource"""
        resource_id = self.add_doc(doc_name="Bigtera")
        self.delete_doc(resource_id)
 
```


测试用例基类：

```python
from pytest_check import check


class ResourceManage():
    """Test case base for Resource"""
    def add_cod(self, doc_name):
        """Add doc"""
        # Some code here
        self.check_doc_add_result(doc_name)


    def delete_doc(self, doc_name):
        pass

    @check.check_func
    def check_doc_add_result(self):
        """Check doc added result"""
        # Some code here
        # assert one
        # assert two
        # Other assert
        return doc_id
```

在执行测试用例的时候，发现返回的`doc_id`是一个`bool`类型的，预期它应该是一个字符串。

# 分析

在 `pytest_check` 插件中，使用 `@check.check_func` 装饰器时，如果被装饰的函数有 `return` 操作，其返回值会是 `True` 或 `False`，原因如下：

## 1. 装饰器的作用

`@check.check_func` 是一个装饰器，它会包装被装饰的函数。装饰器的主要作用是捕获函数执行过程中可能抛出的 `AssertionError` 异常，并记录失败信息。

## 2. 返回值逻辑

- 如果被装饰的函数执行成功，没有抛出 `AssertionError` 异常，装饰器会返回 `True`。
- 如果被装饰的函数抛出了 `AssertionError` 异常，装饰器会记录失败信息，并返回 `False`。

## 3. 非阻塞断言

`@check.check_func` 的设计允许测试继续执行，即使某些检查失败。这与传统的 `pytest` 断言不同，传统的断言在失败时会立即停止测试执行，而 `pytest_check` 的非阻塞断言允许在一次测试中执行多个检查，并记录所有失败。

## 4. 忽略函数的原始返回值

即使被装饰的函数有 `return` 操作，装饰器会忽略函数的原始返回值，而是根据是否发生了 `AssertionError` 来决定返回 `True` 或 `False`。

### 示例代码

```python
import pytest
import check

@check.check_func
def test_example():
    assert 1 == 1  # 断言成功
    return "success"

@check.check_func
def test_example_fail():
    assert 1 == 2  # 断言失败
    return "failure"

# 执行测试
result1 = test_example()
result2 = test_example_fail()

print(result1)  # 输出: True
print(result2)  # 输出: False
```

## 5. 灵活性

通过返回 `True` 或 `False`，用户可以在测试中根据返回值进行进一步的逻辑处理，例如：
- 在测试中进行条件判断。
- 在测试结束后统计失败的检查次数。
- 根据返回值决定后续的测试步骤。

这种机制使得 `pytest_check` 插件在处理复杂的测试场景时更加灵活和强大。


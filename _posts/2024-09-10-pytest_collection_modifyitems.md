---
title: pytest hook系列之pytest_collection_modifyitems
date: 2024-09-10 23:00:00
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
summary: pytest hook之pytest_collection_modifyitems
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_collection_modifyitems`是`pytest`框架中的一个钩子函数，允许我们在测试用例已经被收集到之后对其进行修改或过滤。通过使用这个钩子函数，我们可以实现复杂的测试用例管理和动态处理。本篇文章将详细介绍`pytest_collection_modifyitems`的使用场景、参数，以及通过具体案例展示其应用。

# 什么是 pytest_collection_modifyitems？

`pytest_collection_modifyitems`是`pytest`提供的一个钩子函数，在所有的测试用例被收集之后调用。我们可以在这个钩子中处理或修改收集到的测试用例列表。这使得我们可以动态地启用或禁用测试用例、依据特定条件排序测试用例等。

# 使用场景

* 动态过滤测试用例：根据特定的条件启用或禁用某些测试用例。
* 调整测试用例顺序：根据需求对测试用例进行排序，确保特定顺序的执行。
* 自动分类测试用例：基于文件名、路径或标记对测试用例进行自动分类和管理。


# 参数

```python
def pytest_collection_modifyitems(
    session: "Session", config: "Config", items: List["Item"]
) -> None:
    """Called after collection has been performed. May filter or re-order
    the items in-place.

    :param session: The pytest session object.
    :param config: The pytest config object.
    :param items: List of item objects.
    """
```

* `session`: 当前`pytest`会话对象，通过这个对象可以访问所有收集到的测试项以及配置。
* `config`：`pytest`配置对象，包含了从命令行和`pytest`配置文件中解析出来的选项。
* `items`：已经收集到的测试用例列表，每一个元素都是一个`pytest`测试项对象，表示一个具体的测试用例。


# 示例代码

## 案例一：动态过滤测试用例

目标：根据命令行参数只运行特定标记的测试用例。

步骤：

* 添加命令行参数用于指定要运行的特定标记。
* 使用`pytest_collection_modifyitems`钩子过滤收集到的测试用例，仅保留带有指定标记的测试用例。


示例代码：

```python
# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--run-marked", action="store", default=None, help="Run tests with specific mark")

def pytest_collection_modifyitems(config, items):
    run_marked = config.getoption("--run-marked")
    if run_marked:
        marked_items = []
        deselected_items = []
        for item in items:
            if run_marked in item.keywords:
                marked_items.append(item)
            else:
                deselected_items.append(item)
        items[:] = marked_items
        # 报告被 deselected 的测试用例
        config.hook.pytest_deselected(items=deselected_items)
```

```python
# 示例测试用例 test_case.py
import pytest

@pytest.mark.my_mark
def test_example_marked():
    assert 1 + 1 == 2

def test_example_unmarked():
    assert 2 + 2 == 4
```

输出效果：

```shell
collected 2 items                                                                                                                                                                                                                                       

test_case.py::test_example_marked PASSED
test_case.py::test_example_unmarked PASSED
```

**说明：**

* `pytest_addoption`添加了一个命令行选项`--run-marked`用于指定运行带有特定标记的测试用例。
* `pytest_collection_modifyitems`钩子中，通过检查`item.keywords`找出带有指定标记的测试用例，并将其保留在`items`列表中。


## 案例二：调整测试用例顺序

目标：通过命令行选项指定测试用例的执行顺序（升序或降序）。

步骤：

* 添加命令行参数用于指定测试用例的执行顺序。
* 使用`pytest_collection_modifyitems`钩子调整收集到的测试用例的顺序。


示例代码：

```python
# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--order", action="store", default="asc", choices=["asc", "desc"], help="Order of test execution")

def pytest_collection_modifyitems(config, items):
    order = config.getoption("--order")
    if order == "desc":
        items.sort(key=lambda x: x.nodeid, reverse=True)
    else:
        items.sort(key=lambda x: x.nodeid)
```

```pytest
# 示例测试用例 test_case2.py
def test_example1():
    assert 1 + 1 == 2

def test_example3():
    assert 3 + 3 == 6

def test_example2():
    assert 2 + 2 == 4
```

输出效果：

```shell
test_case2.py::test_example1 PASSED
test_case2.py::test_example2 PASSED
test_case2.py::test_example3 PASSED
```

**说明：**

* `pytest_addoption`添加命令行选项`--order`用于指定测试用例执行顺序（升序或降序）。
* `pytest_collection_modifyitems`钩子中，通过检查`order`选项对`items`列表中的测试用例排序。


## 案例三：自动分组和分类测试用例

目标：根据测试用例的文件路径自动分组，在报告中展示每组内的运行结果。

步骤：

* 在收集阶段解析测试用例路径并进行分组。
* 在运行阶段生成分组报告。


示例代码：

```python
# conftest.py
import pytest

def pytest_collection_modifyitems(config, items):
    group_map = {}
    for item in items:
        dirname = item.fspath.dirname
        if dirname not in group_map:
            group_map[dirname] = []
        group_map[dirname].append(item)

    # 添加组信息
    config.group_report = group_map

def pytest_report_collectionfinish(config, items):
    group_map = config.group_report
    for group, tests in group_map.items():
        print(f"Group: {group}")
        for test in tests:
            print(f"  Test: {test.nodeid}")
```

```python
# 示例测试用例 test_case3.py
def test_example1():
    assert 1 + 1 == 2

def test_example2():
    assert 2 + 2 == 4
```

输出效果：

```shell
collected 2 items                                                                                                                                                                                                                                       
Group: /root/test/hook
  Test: test_case3.py::test_example1
  Test: test_case3.py::test_example2

test_case3.py .. 
```

**说明：**

* `pytest_collection_modifyitems`钩子中，根据测试项的文件路径将测试用例进行分组，并将分组信息保存到`config`对象中。
* `pytest_report_collectionfinish`钩子中，通过读取`config`对象中的分组信息，在报告阶段输出每个分组的测试用例。


# 结语

`pytest_collection_modifyitems`是`pytest`中一个非常强大和灵活的钩子，能够在测试用例收集之后进行各种定制化操作。通过本文的案例，你可以深刻理解和灵活应用`pytest_collection_modifyitems`来优化你的测试管理和执行流程。在实际应用中，可以根据项目需求及测试场景对这些示例进行扩展和调整。

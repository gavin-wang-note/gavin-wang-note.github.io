---
title: 自定义Allure报告中测试用例级别与展示
date: 2024-07-14 23:41:00
author: Gavin Wang
img: "/img/pytest/pytest-1.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 自定义Allure报告中测试用例级别与展示，实际项目中可能是P0，P1, P2, P3, P4这样的级别，`P0`对应`Blocker`级别，`P1`对应`Critical`级别，如此类推，并能够指定运行对应Px级别的测试用例
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

我们知道，只用`pytest`结合`Allure`生成可视化报告过程中， `Allure`对严重级别的定义分为 5 个级别：

* `Blocker` 级别：中断缺陷（客户端程序无响应，无法执行下一步操作）
* `Critical` 级别：临界缺陷（ 功能点缺失）
* `Normal` 级别：普通缺陷（数值计算错误）（默认）
* `Minor` 级别：次要缺陷（界面错误与 UI 需求不符）
* `Trivial` 级别：轻微缺陷（必输项无提示，或者提示不规范）

但是，但是，用户的测试用例仓库中定义的用例级别往往不是上述信息，而是`P0，P1, P2, P3, P4`这样的级别（`P0`对应`Blocker`级别，`P1`对应`Critical`级别，如此类推）。

问题来了：

要如何做，能够让`Allure HTML`可视化报告中看到用户自定义的级别？

答案是在不修改`Allure`源码的情况下，是不可能在`Allure HTML`可视化报告中看到非`Allure`定义分为 5 个级别的，原因请查阅我之前的一篇[博文](https://gavin-wang-note.github.io/2023/11/28/allure_severity_level/)。

既然修改不了，那能否将`P0`与`Blocker`级别匹配上？来个"曲线救国"，比如在测试用例中传递的用例级别是P0，在`Allure HTML`可视化报告中现实为`Blocker`?

答案是肯定的，且看下文。

# 方案一：自定义严重性映射

## 思路

* 定义自定义严重性映射：将 `P0` 至 `P4` 映射到 `Allure` 支持的严重性级别（`BLOCKER、CRITICAL、NORMAL、MINOR、TRIVIAL`）。
* 使用自定义装饰器：创建自定义装饰器，用于将测试用例标记为特定的严重性。

## 自定义装饰器

```python
# Content of custom_severity.py
import allure

def custom_severity(level):
    severity_mapping = {
        'P0': allure.severity_level.BLOCKER,
        'P1': allure.severity_level.CRITICAL,
        'P2': allure.severity_level.NORMAL,
        'P3': allure.severity_level.MINOR,
        'P4': allure.severity_level.TRIVIAL,
    }

    def decorator(test_func):
        @allure.severity(severity_mapping.get(level, allure.severity_level.NORMAL))
        def wrapper(*args, **kwargs):
            return test_func(*args, **kwargs)
        return wrapper
    return decorator
```

## 测试文件


```python
# Content of test_example1.py
import pytest
from custom_severity import custom_severity
import allure

@custom_severity('P0')
def test_case_p0():
    assert 1 + 1 == 2

@custom_severity('P1')
def test_case_p1():
    assert 1 + 2 == 3

@custom_severity('P2')
def test_case_p2():
    assert 1 + 3 == 4

@custom_severity('P3')
def test_case_p3():
    assert 1 + 4 == 5

@custom_severity('P4')
def test_case_p4():
    assert 1 + 5 == 6
```


## 测试报告展示效果

如下图所示：

<img class="shadow" src="/img/in-post/allure/Allure_severity.png" width="1200">

## 继续调整

展示效果一般般，继续调整，希望增加一下描述信息，表明用例P0~P4与`BLOCKER、CRITICAL、NORMAL、MINOR、TRIVIAL`之间的关系。

修改`allure json`文件内容，扩展测试用例描述信息，比如如下的测试用例：


```python
# Content of test_example2.py
import pytest
import allure

@allure.severity(allure.severity_level.BLOCKER)
def test_case_p0():
    """
    Test case for P0 severity level.
    """
    assert 1 + 1 == 2

@allure.severity(allure.severity_level.CRITICAL)
def test_case_p1():
    """
    Test case for P1 severity level.
    """
    assert 1 + 2 == 3

@allure.severity(allure.severity_level.NORMAL)
def test_case_p2():
    """
    Test case for P2 severity level.
    """
    assert 1 + 3 == 4

@allure.severity(allure.severity_level.MINOR)
def test_case_p3():
    """
    Test case for P3 severity level.
    """
    assert 1 + 4 == 5

@allure.severity(allure.severity_level.TRIVIAL)
def test_case_p4():
    """
    Test case for P4 severity level.
    """
    assert 1 + 5 == 6
```

增加对`json`文件处理脚本，在生成`allure json`文件后执行：


```python
# Content of process_allure_results.py
import os
import json

def update_description(allure_results_dir):
    severity_mapping = {
        'blocker': 'P0 - Blocker',
        'critical': 'P1 - Critical',
        'normal': 'P2 - Normal',
        'minor': 'P3 - Minor',
        'trivial': 'P4 - Trivial'
    }

    for filename in os.listdir(allure_results_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(allure_results_dir, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)

            # 更新描述字段中的严重级别
            if 'labels' in data:
                for label in data['labels']:
                    if label['name'] == 'severity':
                        severity = severity_mapping.get(label['value'], '')
                        if severity:
                            # 保留现有描述信息并附加严重级别映射关系
                            description = data.get('description', '')
                            if description:
                                description += "\n\n"
                            description += f"Severity Mapping: {severity}"
                            data['description'] = description

            with open(filepath, 'w') as file:
                json.dump(data, file, indent=2)

if __name__ == '__main__':
    update_description('allure-results')
```

`allure html`展示效果如下：

<img class="shadow" src="/img/in-post/allure/Allure_severity_desc.png" width="1200">


# 方案二：使用allure tag

* 在测试代码中，自定义一个函数来将用户的级别 `P0、P1` 等映射到 `Allure` 对应的级别
* 在测试用例中，使用这个自定义函数来设置级别，并通过 `Allure` 的接口将级别信息传递给报告

当然，除了`tag`外，还可以使用`allure label`，和直接使用`pytest mark`，方法大差不差吧，读者可自行拓展。

```python
# Content of conftest.py
import pytest
import allure

from allure import severity_level

# 自定义的级别映射函数
def map_user_level(user_level):
    if user_level == 'P0':
        return severity_level.BLOCKER
    elif user_level == 'P1':
        return severity_level.CRITICAL
    elif user_level == 'P2':
        return severity_level.NORMAL
    elif user_level == 'P3':
        return severity_level.MINOR
    elif user_level == 'P4':
        return severity_level.TRIVIAL

@pytest.fixture(autouse=True)
def set_custom_severity_level(request):
    user_level = request.node.get_closest_marker("severity_level")
    if user_level:
        user_level = user_level.args[0]
        with allure.step(f"Setting severity level to {user_level}"):
            allure.severity(map_user_level(user_level))
```

测试用例：

```python
# Content of test_example.py
import pytest

@pytest.mark.severity_level("P1")
def test_custom_level():
    # 测试逻辑
    assert True
```

<img class="shadow" src="/img/in-post/allure/Allure_severity_tuning.png" width="1200">


# 方案三：扩展参数，并能够支持制定Px级别测试用例的执行

直接上`code`：

```python
# Content of conftest.py
import pytest
import allure

# 定义 severity 级别
SEVERITY_LEVELS = {
    'P0': allure.severity_level.BLOCKER,
    'P1': allure.severity_level.CRITICAL,
    'P2': allure.severity_level.NORMAL,
    'P3': allure.severity_level.MINOR,
    'P4': allure.severity_level.TRIVIAL
}

def pytest_addoption(parser):
    """添加命令行选项来指定 severity 级别"""
    parser.addoption("--severity", action="store", default=None,
                     help="Specify the severity level(s) (e.g., P0,P1,P2)")

def pytest_collection_modifyitems(config, items):
    """根据命令行选项过滤测试用例"""
    severity_levels = config.getoption("--severity")
    if severity_levels:
        selected_levels = severity_levels.split(',')
        items[:] = [item for item in items if has_severity(item, selected_levels)]

def has_severity(item, selected_levels):
    """检查测试用例是否具有指定的 severity 标记"""
    marker = item.get_closest_marker("severity")
    if marker:
        marker_level = marker.args[0]
        return marker_level in selected_levels
    return False
```


```python
# Content of test_example.py
import pytest

@pytest.mark.severity('P0')
def test_case_p0():
    """This is P0 test case"""
    assert 1 + 1 == 2

@pytest.mark.severity('P1')
def test_case_p1():
    """This is P1 test case"""
    assert 1 + 2 == 3

@pytest.mark.severity('P2')
def test_case_p2():
    """This is P2 test case"""
    assert 1 + 3 == 4

@pytest.mark.severity('P3')
def test_case_p3():
    """This is P3 test case"""
    assert 1 + 4 == 5

@pytest.mark.severity('P4')
def test_case_p4():
    """This is P4 test case"""
    assert 1 + 5 == 6
```


运行指定级别的测试用例：

指定单个级别的：

```shell
pytest  --severity=P0 --alluredir=allure-results
```

或者指定多个级别的：

```shell
pytest  --severity=P0,P2 --alluredir=allure-results
```

运行后测试用例报告展示效果如下：

<img class="shadow" src="/img/in-post/allure/Allure_sepcial_severity.png" width="1200">


# 小结

黔驴技穷了，写里整整一个周末（两天）外加两个深夜...

以后项目实践想到更好的solution再更新吧...


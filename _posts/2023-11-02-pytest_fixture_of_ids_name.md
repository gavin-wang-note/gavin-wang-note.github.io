---
layout:     post
title:      "pytest fixture of ids/name"
subtitle:   "pytest fixture of ids/name"
date:       2023-11-02
author:     "Gavin Wang"
img: "/img/pytest/pytest-3.png"
catalog:    true
summary: pytest fixture的ids和name参数详解
categories:
    - [Automation]
    - [pytest]
tags:
    - pytest
    - Automation
---


# 概述



pytest fixture 的ids，需要结合fixture的param使用，其作用是给测试用例名字增加标识，语法格式如下：



```shell
@pytest.fixture(scope="", params="", autouse="", ids="", name="")
```



本文重点讲述一下ids，顺带介绍下name的用途。



# 示例


未使用ids情况下

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


@pytest.fixture(params=['Parameter1', 'Parameter2'])
def my_fixture(request):
    return request.param


def test_fixtures_01(my_fixture):
    print('\n Run test_fixtures_01')
    print(my_fixture)


def test_fixtures_02(my_fixture):
    print('\n Run test_fixtures_02')
    print(my_fixture)

```



运行效果如下：



<img class="shadow" src="/img/in-post/ids_no_ids.png" width="1200">


带上ids



```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


@pytest.fixture(params=['Parameter1', 'Parameter2'], ids=["id-01", "id-02"])
def my_fixture(request):
    return request.param


def test_fixtures_03(my_fixture):
    print('\n Run test_fixtures_03')
    print(my_fixture)


```



输出结果：


<img class="shadow" src="/img/in-post/ids_with_ids.png" width="1200">



从输出结果来看，"PASSED"前的中括号里的内容，如第一张图的```[Parameter1]``` ，未携带ids情况下；而携带了ids后，会被ids对应值替换掉。







# 利用ids实现测试需求



## 场景描述

购买AI智能体，支付状态有三种：

* 下单未支付
* 成功支付
* 支付失败/放弃支付



这三种状态对应数据库中三种值，分别为0，1，2。 利用ids方式，来简化测试用例。





## 代码示例



```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


def init_data(fixture_value):
    if fixture_value == 0:
        return "NoPay"
    elif fixture_value == 1:
        return "PaySuccess"
    elif fixture_value == 2:
        return "DropPay"


@pytest.fixture(params=[0, 1, 2], ids=init_data)
def my_AI_fixture(request):
    req_param = request.param
    print("\nParameter : [{}], status is : [{}]".format(req_param, req_param))
    yield req_param
    print("\n----------------------------------------")


def test_case_01(my_AI_fixture):
    print("\nRun [{}] test case".format(my_AI_fixture))
```



运行结果：


<img class="shadow" src="/img/in-post/without_-k_parameter.png" width="1200">


利用 -k 参数，指定要指定的测试用例：



<img class="shadow" src="/img/in-post/with_-k_parameter.png" width="1200">

{% note warning %}
注意:
{% endnote %}

  -k 后面，字符串一定要使用双引号，单引号不可以。

-k的意思如下：

```shell
  -k EXPRESSION    Only run tests which match the given substring expression. An expression is a Python evaluatable expression where all names are substring-matched against test names and their parent classes.
Example: -k 'test_method or test_other' matches all test functions and classes whose name contains 'test_method' or 'test_other', while -k 'not test_method' matches those that don't contain 'test_method' in their names. -k 'not test_method and not test_other' will eliminate the matches. Additionally keywords are matched to classes and functions containing extra names in their 'extra_keyword_matches' set, as well as functions which have names assigned directly to them. The matching is case-insensitive.
```





# 说一下 name 参数



name参数实用性不大，用于给fixture设置别名，或者描述一下这个fixture的用途，示例如下：



```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


@pytest.fixture(params=['Parameter1', 'Parameter2'], ids=["id-01", "id-02"], name="Test_Fixture_Name_Daemon")
def my_fixture(request):
    return request.param


def test_fixtures_03(Test_Fixture_Name_Daemon):
    print('\n Run test_fixtures_03')
    print(my_fixture)

```



如上图所示，函数传递的fixture，变更成了name。



## 问题：如果fixture中使用了name参数，测试函数中是否可以传递fixture 函数名而非name对应值？



答案是否定的，测试如下：



```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


@pytest.fixture(params=['Parameter1', 'Parameter2'], ids=["id-01", "id-02"], name="Test_Fixture_Name_Daemon")
def my_fixture(request):
    return request.param


def test_fixtures_03(my_fixture):
    print('\n Run test_fixtures_03')
    print(my_fixture)
```



如上，代码执行时报如下错误信息：

```shell
C:\Users\Wang>pytest -vrs C:\Users\Wang\Desktop\test_0.py
================================================= test session starts =================================================
platform win32 -- Python 3.11.4, pytest-7.4.2, pluggy-1.3.0 -- C:\Users\Wang\AppData\Local\Programs\Python\Python311\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Wang
plugins: allure-pytest-2.13.2, order-1.1.0, progress-1.2.5, repeat-0.9.1, timeout-2.1.0
collected 1 item

Desktop/test_0.py::test_fixtures_03 ERROR                                                                        [100%]

======================================================= ERRORS ========================================================
_________________________________________ ERROR at setup of test_fixtures_03 __________________________________________
file C:\Users\Wang\Desktop\test_0.py, line 39
  def test_fixtures_03(my_fixture):
E       fixture 'my_fixture' not found
>       available fixtures: Test_Fixture_Name_Daemon, __pytest_repeat_step_number, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, doctest_namespace, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

C:\Users\Wang\Desktop\test_0.py:39
================================================== 1 error in 0.02s ===================================================

C:\Users\Wang>
```

---
title: 《pytest测试指南》-- 章节1-8 pytest参数化
date: 2024-05-28 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-2.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 《pytest测试指南》一书 章节1-8 patest参数化详解
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---



# 第8章 pytest参数化

`pytest` 一个突出的功能是参数化测试，这使得重复使用相同的测试逻辑来测试不同的数据变得容易。`pytest` 通过 `pytest.mark.parameterize` 装饰器提供了参数化的能力，让测试者能够定义多组参数和值，然后 `pytest` 会自动为每组参数创建一个测试用例。

# 8.1 参数化的概念

参数化测试是一种通过代码复用来提高测试效率和覆盖率的策略，它让你可以用不同的参数多次运行同一个测试。这意味着你可以编写一个测试函数，并用不同的数据多次调用它，而每组参数实质上生成一个独立的测试用例。这有助于发现那些仅在特定条件下才出现的错误，并且使测试代码更加简洁。

# 8.2 使用 `parameterize` 的优势

使用参数化的主要优势是：

- 减少重复代码
- 增加测试的灵活性和可维护性
- 提高测试覆盖率
- 易于对测试用例进行扩展

# 8.3 `pytest.mark.parameterize` 的用法

<font color='red'>```@pytest.mark.parametrize```</font> 装饰器接受两个参数：一个字符串（代表测试函数的参数名）和一个值列表。你可以为每个参数指定一个或多个值。`pytest` 会为每组值自动创建一个测试用例实例，类似DDT。

pytest在如下几个级别上支持测试参数化：

* pytest.fixture()允许对fixture函数进行参数化
* @pytest.mark.parametrize允许在测试函数或类中定义多组参数和fixture
* pytest_generate_tests允许自定义参数化方案或扩展

其语法格式如下：

```python
@pytest.mark.parametrize('参数名',list) 
```

- 第一个参数是字符串，多个参数中间用逗号隔开

- 第二个参数是list多组数据用元组类型;传三个或更多参数也是这样传。list的每个元素都是一个元组，元组里的每个元素和按参数顺序 一 一 对应

示例：

- 传一个参数 @pytest.mark.parametrize('参数名'，list) 进行参数化

- 传两个参数@pytest.mark.parametrize('参数名1，参数名2'，[(参数1_data1, 参数2_data1),(参数1_data2, 参数2_data2)]) 进行参数化

# 8.4 常见的参数化示例

我们先来介绍一下常规测试中使用到的参数化示例应用，之后再根据parametrize源码逐一讲解各个参数的使用。

## 8.4.1 只传递一个参数

###  8.4.1.1 一个参数一个值

示例代码如下：

```python
# content of test_one_parameter_one_value.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


@pytest.mark.parametrize("name", ["Gavin"])
def test_case1(name):
    print("\n" + name)
    assert name.lower() == "gavin"
```

如上示例，只传递了一个“name”参数，其值为“Gavin”，执行结果：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_one_parameter_one_value.py 
============================== test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 1 item

test_one_parameter_one_value.py::test_case1[Gavin] 
Gavin
PASSED

=============================== 1 passed in 0.02s ===============================
root@Gavin:~/code/chapter1-8#
```

###  8.4.1.2 一个参数多个值

这种比较常见，示例代码如下：

```python
# content of test_one_parameter_many_value.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


@pytest.mark.parametrize("name", ["Gavin","Jason","Big","Andy","Bean","Chandler"])
def test_case1(name):
    print("\n" + name)
    assert name.lower() == "gavin"
```

如上示例，只传递了一个“name”参数，其值为一个含有5个元素的List，生成5个测试用例，执行结果如下：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_one_parameter_many_value.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 6 items

test_one_parameter_many_value.py::test_case1[Gavin] 
Gavin
PASSED
test_one_parameter_many_value.py::test_case1[Jason] 
Jason
FAILED
test_one_parameter_many_value.py::test_case1[Big] 
Big
FAILED
test_one_parameter_many_value.py::test_case1[Andy] 
Andy
FAILED
test_one_parameter_many_value.py::test_case1[Bean] 
Bean
FAILED
test_one_parameter_many_value.py::test_case1[Chandler] 
Chandler
FAILED

================================= FAILURES =====================================
_________________________________ test_case1[Jason] ____________________________

name = 'Jason'

    @pytest.mark.parametrize("name", ["Gavin","Jason","Big","Andy","Bean","Chandler"])
    def test_case1(name):
        print("\n" + name)
>       assert name.lower() == "gavin"
E       AssertionError: assert 'jason' == 'gavin'
E         - gavin
E         + jason

test_one_parameter_many_value.py:10: AssertionError
___________________________________ test_case1[Big] _____________________________

name = 'Big'

    @pytest.mark.parametrize("name", ["Gavin","Jason","Big","Andy","Bean","Chandler"])
    def test_case1(name):
        print("\n" + name)
>       assert name.lower() == "gavin"
E       AssertionError: assert 'big' == 'gavin'
E         - gavin
E         + big

test_one_parameter_many_value.py:10: AssertionError
___________________________________ test_case1[Andy] ____________________________

name = 'Andy'

    @pytest.mark.parametrize("name", ["Gavin","Jason","Big","Andy","Bean","Chandler"])
    def test_case1(name):
        print("\n" + name)
>       assert name.lower() == "gavin"
E       AssertionError: assert 'andy' == 'gavin'
E         - gavin
E         + andy

test_one_parameter_many_value.py:10: AssertionError
___________________________________ test_case1[Bean] _____________________________

name = 'Bean'

    @pytest.mark.parametrize("name", ["Gavin","Jason","Big","Andy","Bean","Chandler"])
    def test_case1(name):
        print("\n" + name)
>       assert name.lower() == "gavin"
E       AssertionError: assert 'bean' == 'gavin'
E         - gavin
E         + bean

test_one_parameter_many_value.py:10: AssertionError
__________________________________ test_case1[Chandler] __________________________

name = 'Chandler'

    @pytest.mark.parametrize("name", ["Gavin","Jason","Big","Andy","Bean","Chandler"])
    def test_case1(name):
        print("\n" + name)
>       assert name.lower() == "gavin"
E       AssertionError: assert 'chandler' == 'gavin'
E         - gavin
E         + chandler

test_one_parameter_many_value.py:10: AssertionError
=============================== short test summary info ===========================
FAILED test_one_parameter_many_value.py::test_case1[Jason] - AssertionError: assert 'jason' == 'gavin'
FAILED test_one_parameter_many_value.py::test_case1[Big] - AssertionError: assert 'big' == 'gavin'
FAILED test_one_parameter_many_value.py::test_case1[Andy] - AssertionError: assert 'andy' == 'gavin'
FAILED test_one_parameter_many_value.py::test_case1[Bean] - AssertionError: assert 'bean' == 'gavin'
FAILED test_one_parameter_many_value.py::test_case1[Chandler] - AssertionError: assert 'chandler' == 'gavin'
================================ 5 failed, 1 passed in 0.13s =======================
root@Gavin:~/code/chapter1-8#
```

## 8.4.2 多个参数

### 8.4.2.1 多个参数多个值

下面是官网的示例：

```python
# content of test_multiple_values_for_multiple_parameters_v1.py
import pytest


@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

此示例，参考官网给出的另外一个方案：

```https://docs.pytest.org/en/stable/how-to/parametrize.html ``` 下 “To parametrize all tests in a module, you can assign to the [`pytestmark`](https://docs.pytest.org/en/stable/reference/reference.html#globalvar-pytestmark) global variable:”

```python
# content of test_multiple_values_for_multiple_parameters_v2.py
import pytest

pytestmark = pytest.mark.parametrize("test_input, expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])


def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

v1版本是常规方式，使用`pytest.mark.parameterize`装饰器；v2版本使用`pytestmark` ，`pytestmark`是 `pytest` 中一个特殊的内置变量，它允许在模块级别设置标记。

两个版本的测试用例运行结果相同：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_multiple_values_for_multiple_parameters_v1.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 3 items

test_multiple_values_for_multiple_parameters_v1.py::test_eval[3+5-8] PASSED
test_multiple_values_for_multiple_parameters_v1.py::test_eval[2+4-6] PASSED
test_multiple_values_for_multiple_parameters_v1.py::test_eval[6*9-42] FAILED

================================ FAILURES =====================================
_______________________________ test_eval[6*9-42] _____________________________

test_input = '6*9', expected = 42

    def test_eval(test_input, expected):
>       assert eval(test_input) == expected
E       AssertionError: assert 54 == 42
E        +  where 54 = eval('6*9')

test_multiple_values_for_multiple_parameters_v1.py:15: AssertionError
========================= short test summary info =============================
FAILED test_multiple_values_for_multiple_parameters_v1.py::test_eval[6*9-42] - AssertionError: assert 54 == 42
========================== 1 failed, 2 passed in 0.09s ========================
root@Gavin:~/code/chapter1-8# pytest -s -v test_multiple_values_for_multiple_parameters_v2.py 
========================== test session starts ================================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 3 items

test_multiple_values_for_multiple_parameters_v2.py::test_eval[3+5-8] PASSED
test_multiple_values_for_multiple_parameters_v2.py::test_eval[2+4-6] PASSED
test_multiple_values_for_multiple_parameters_v2.py::test_eval[6*9-42] FAILED

=============================== FAILURES =====================================
_______________________________ test_eval[6*9-42] ____________________________

test_input = '6*9', expected = 42

    def test_eval(test_input, expected):
>       assert eval(test_input) == expected
E       AssertionError: assert 54 == 42
E        +  where 54 = eval('6*9')

test_multiple_values_for_multiple_parameters_v2.py:15: AssertionError
=========================== short test summary info ==========================
FAILED test_multiple_values_for_multiple_parameters_v2.py::test_eval[6*9-42] - AssertionError: assert 54 == 42
=========================== 1 failed, 2 passed in 0.09s ======================
root@Gavin:~/code/chapter1-8#
```

**请注意：**

通过在测试文件的顶层（模块级别）设置 `pytestmark` 变量，你可以将某个 `pytest.mark` 应用于整个模块中的所有测试用例。这是一种便捷的方式来批量应用装饰器，而不需要重复在每个单独的测试函数上使用。

当你使用 `pytestmark = pytest.mark.parametrize` ，这意味着你希望将参数化应用到整个模块的所有测试函数上。不过，需要注意的是，并不是所有的 `pytest.mark` 装饰器都能用 `pytestmark` 变量来设置。例如，`pytest.mark.parametrize` 通常不会这样使用，因为参数化通常涉及为不同的测试函数提供**不同的参数和值**。

以下是 `pytestmark` 的一个例子，其中使用了 `pytest.mark.skip` 跳过一个模块中的所有测试：

```python
# content of test_pytestmark_skip.py
import pytest

# 使用 pytest.mark.skip 标记在这个模块中跳过所有的测试
pytestmark = pytest.mark.skip("all tests still WIP")

def test_func1():
    assert True

def test_func2():
    assert True
```

在上面的例子中，模块 `test_pytestmark_skip.py` 中所有的测试函数 `test_func1()` 和 `test_func2()` 都将被跳过，因为它们被 `pytest.mark.skip` 标记所覆盖，其运行结果如下：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_pytestmark_skip.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 2 items

test_pytestmark_skip.py::test_func1 SKIPPED (all tests still WIP)
test_pytestmark_skip.py::test_func2 SKIPPED (all tests still WIP)

=============================== 2 skipped in 0.01s =============================
root@Gavin:~/code/chapter1-8#
```

如果你确实想在模块级别应用参数化，你应该以不同的方式来做，例如，定义一个通用的 `fixture` 进行参数化，然后在模块内部的测试函数中引用这个 `fixture`，如下所示：

```python
# content of test_mark_parameterize.py
import pytest

# 创建一个参数化的 fixture
@pytest.fixture(params=[1, 2, 3])
def num(request):
    return request.param

# 在模块内的测试函数中使用参数化的 fixture
def test_func1(num):
    assert num > 0

def test_func2(num):
    assert num < 4
```

在这个例子中，模块 `test_mark_parameterize.py` 中的每个测试函数 `test_func1()` 和 `test_func2()` 都会使用从 `fixture` `num` 参数化获取的值 `1`，`2` 和 `3` 分别运行三次。这样，实现了参数化而不是使用 `pytestmark` 来设置 `pytest.mark.parametrize`。

### 8.4.2.2 多个参数的混合使用

示例代码如下（在官方示例代码上做了调整）：

```python
# content of test_mixed_use_of_multiple_parameters.py
import pytest


@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_foo(x, y):
    print("Generate new combinations : {},{}".format(x, y))
```

上面示例会产生4个测试用例，输出结果参考如下：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_mixed_use_of_multiple_parameters.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 4 items

test_mixed_use_of_multiple_parameters.py::test_foo[2-0] Generate new combinations : 0,2
PASSED
test_mixed_use_of_multiple_parameters.py::test_foo[2-1] Generate new combinations : 1,2
PASSED
test_mixed_use_of_multiple_parameters.py::test_foo[3-0] Generate new combinations : 0,3
PASSED
test_mixed_use_of_multiple_parameters.py::test_foo[3-1] Generate new combinations : 1,3
PASSED

================================ 4 passed in 0.02s =============================
root@Gavin:~/code/chapter1-8#
```

再看个示例：

```python
# content of test_mixed_use_of_multiple_parameters_v2.py
import pytest

data1 = [1, 2]
data2 = ["python", "Shell"]
data3 = ["Software", "Test", "Engineer", "from", "Gavin"]


@pytest.mark.parametrize("a", data1)
@pytest.mark.parametrize("b", data2)
@pytest.mark.parametrize("c", data3)
def test_case3(a, b, c):
    print(f"[{a} {b} {c}]")
```

如上示例，会产生20个测试用例：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_mixed_use_of_multiple_parameters_v2.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 20 items

test_mixed_use_of_multiple_parameters_v2.py::test_case3[Software-python-1] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Software-python-2] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Software-Shell-1] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Software-Shell-2] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Test-python-1] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Test-python-2] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Test-Shell-1] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Test-Shell-2] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Engineer-python-1] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Engineer-python-2] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Engineer-Shell-1] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Engineer-Shell-2] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[from-python-1] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[from-python-2] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[from-Shell-1] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[from-Shell-2] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Gavin-python-1] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Gavin-python-2] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Gavin-Shell-1] [{a} {b} {c}]
PASSED
test_mixed_use_of_multiple_parameters_v2.py::test_case3[Gavin-Shell-2] [{a} {b} {c}]
PASSED

============================== 20 passed in 0.05s =============================
root@Gavin:~/code/chapter1-8#
```

## 8.4.3 参数化

### 8.4.3.1 传入字典数据

通过传入字典数据，你可以为测试用例提供键值对，其中键通常代表输入参数的名称，而值则代表实际的测试数据。这样，你可以在一个测试用例中测试多个不同的输入组合，而不必为每个组合编写单独的测试函数。

下面示例展示了如何使用 pytest 的参数化功能来传入字典数据：

```python
# content of test_passing_in_dictionary_data.py
import pytest


json=({"username":"Jason","password":"Python@123!"},{"username":"Alex","password":"226699"},{"username":"Rita","password":"123456"})

@pytest.mark.parametrize('json', json)
def test_pytest_parametrize(json):
    print(f'dit : \n{json}')
    print(f'username : {json["username"]}, password : {json["password"]}')
```

输出结果：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_passing_in_dictionary_data.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 3 items

test_passing_in_dictionary_data.py::test_pytest_parametrize[json0] dit : 
{'username': 'Jason', 'password': 'Python@123!'}
username : Json, password : Python@123!
PASSED
test_passing_in_dictionary_data.py::test_pytest_parametrize[json1] dit : 
{'username': 'Alex', 'password': '226699'}
username : Alex, password : 226699
PASSED
test_passing_in_dictionary_data.py::test_pytest_parametrize[json2] dit : 
{'username': 'Rita', 'password': '123456'}
username : Rita, password : 123456
PASSED

============================== 3 passed in 0.02s ============================
root@Gavin:~/code/chapter1-8#
```

### 8.4.3.2 集合标记

集合标记（Collection Markers）允许你根据特定的条件对测试用例进行分组，这样，你可以根据需要选择性地运行某些标记的测试用例，而不是执行全部测试。集合标记可以基于文件、类、函数等多种方式进行分组。

下面示例展示了如何使用集合标记来组织和运行特定的测试用例：

```python
# content of test_set_tag.py
import pytest


@pytest.mark.parametrize("username,password",
                         [("Jason", "123456"), ("Jack", "654321"),
                          pytest.param("Bruce", "123456", marks=pytest.mark.xfail),
                          pytest.param("Alex", "123456", marks=pytest.mark.skip)])
def test_login(username, password):
    print(username + " : " + password)
    assert username == "Jack"
```

输出结果：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_set_tag.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 4 items

test_set_tag.py::test_login[Jason-123456] Jason : 123456
FAILED
test_set_tag.py::test_login[Jack-654321] Jack : 654321
PASSED
test_set_tag.py::test_login[Bruce-123456] Bruce : 123456
XFAIL
test_set_tag.py::test_login[Alex-123456] SKIPPED (unconditional skip)

================================ FAILURES =====================================
________________________________ test_login[Jason-12___________________________

username = 'Jason', password = '123456'

    @pytest.mark.parametrize("username,password",
                             [("Jason", "123456"), ("Jack", "654321"),
                              pytest.param("Bruce", "123456", marks=pytest.mark.xfail),
                              pytest.param("Alex", "123456", marks=pytest.mark.skip)])
    def test_login(username, password):
        print(username + " : " + password)
>       assert username == "Jack"
E       AssertionError: assert 'Jason' == 'Jack'
E         - Jack
E         + Jason

test_set_tag.py:10: AssertionError
============================= short test summary info ==========================
FAILED test_set_tag.py::test_login[Jason-123456] - AssertionError: assert 'Jason' == 'Jack'
=============== 1 failed, 1 passed, 1 skipped, 1 xfailed in 0.09s ==============
root@Gavin:~/code/chapter1-8#
```

# 8.5 parametrize源码详解

源码在`src/_pytest/python.py`文件中，如下：

```python
    def parametrize(
        self,
        argnames: Union[str, Sequence[str]],
        argvalues: Iterable[Union[ParameterSet, Sequence[object], object]],
        indirect: Union[bool, Sequence[str]] = False,
        ids: Optional[
            Union[Iterable[Optional[object]], Callable[[Any], Optional[object]]]
        ] = None,
        scope: Optional[_ScopeName] = None,
        *,
        _param_mark: Optional[Mark] = None,
    ) -> None:
        """Add new invocations to the underlying test function using the list
        of argvalues for the given argnames. Parametrization is performed
        during the collection phase. If you need to setup expensive resources
        see about setting indirect to do it rather than at test setup time.

        Can be called multiple times per test function (but only on different
        argument names), in which case each call parametrizes all previous
        parametrizations, e.g. 

        ::

            unparametrized:         t
            parametrize ["x", "y"]: t[x], t[y]
            parametrize [1, 2]:     t[x-1], t[x-2], t[y-1], t[y-2]

        :param argnames:
            A comma-separated string denoting one or more argument names, or
            a list/tuple of argument strings.

        :param argvalues:
            The list of argvalues determines how often a test is invoked with
            different argument values.

            If only one argname was specified argvalues is a list of values.
            If N argnames were specified, argvalues must be a list of
            N-tuples, where each tuple-element specifies a value for its
            respective argname.

        :param indirect:
            A list of arguments' names (subset of argnames) or a boolean.
            If True the list contains all names from the argnames. Each
            argvalue corresponding to an argname in this list will
            be passed as request.param to its respective argname fixture
            function so that it can perform more expensive setups during the
            setup phase of a test rather than at collection time.

        :param ids:
            Sequence of (or generator for) ids for ``argvalues``,
            or a callable to return part of the id for each argvalue.

            With sequences (and generators like ``itertools.count()``) the
            returned ids should be of type ``string``, ``int``, ``float``,
            ``bool``, or ``None``.
            They are mapped to the corresponding index in ``argvalues``.
            ``None`` means to use the auto-generated id.

            If it is a callable it will be called for each entry in
            ``argvalues``, and the return value is used as part of the
            auto-generated id for the whole set (where parts are joined with
            dashes ("-")).
            This is useful to provide more specific ids for certain items, e.g.
            dates.  Returning ``None`` will use an auto-generated id.

            If no ids are provided they will be generated automatically from
            the argvalues.

        :param scope:
            If specified it denotes the scope of the parameters.
            The scope is used for grouping tests by parameter instances.
            It will also override any fixture-function defined scope, allowing
            to set a dynamic scope using test context or configuration.
        """
        argnames, parametersets = ParameterSet._for_parametrize(
            argnames,
            argvalues,
            self.function,
            self.config,
            nodeid=self.definition.nodeid,
        )
        del argvalues

        if "request" in argnames:
            fail(
                "'request' is a reserved name and cannot be used in @pytest.mark.parametrize",
                pytrace=False,
            )

        if scope is not None:
            scope_ = Scope.from_user(
                scope, descr=f"parametrize() call in {self.function.__name__}"
            )
        else:
            scope_ = _find_parametrized_scope(argnames, self._arg2fixturedefs, indirect)

        self._validate_if_using_arg_names(argnames, indirect)

        # Use any already (possibly) generated ids with parametrize Marks.
        if _param_mark and _param_mark._param_ids_from:
            generated_ids = _param_mark._param_ids_from._param_ids_generated
            if generated_ids is not None:
                ids = generated_ids

        ids = self._resolve_parameter_set_ids(
            argnames, ids, parametersets, nodeid=self.definition.nodeid
        )

        # Store used (possibly generated) ids with parametrize Marks.
        if _param_mark and _param_mark._param_ids_from and generated_ids is None:
            object.__setattr__(_param_mark._param_ids_from, "_param_ids_generated", ids)

        # Add funcargs as fixturedefs to fixtureinfo.arg2fixturedefs by registering
        # artificial "pseudo" FixtureDef's so that later at test execution time we can
        # rely on a proper FixtureDef to exist for fixture setup.
        arg2fixturedefs = self._arg2fixturedefs
        node = None
        # If we have a scope that is higher than function, we need
        # to make sure we only ever create an according fixturedef on
        # a per-scope basis. We thus store and cache the fixturedef on the
        # node related to the scope.
        if scope_ is not Scope.Function:
            collector = self.definition.parent
            assert collector is not None
            node = get_scope_node(collector, scope_)
            if node is None:
                # If used class scope and there is no class, use module-level
                # collector (for now).
                if scope_ is Scope.Class:
                    assert isinstance(collector, _pytest.python.Module)
                    node = collector
                # If used package scope and there is no package, use session
                # (for now).
                elif scope_ is Scope.Package:
                    node = collector.session
                else:
                    assert False, f"Unhandled missing scope: {scope}"
        if node is None:
            name2pseudofixturedef = None
        else:
            default: Dict[str, FixtureDef[Any]] = {}
            name2pseudofixturedef = node.stash.setdefault(
                name2pseudofixturedef_key, default
            )
        arg_directness = self._resolve_args_directness(argnames, indirect)
        for argname in argnames:
            if arg_directness[argname] == "indirect":
                continue
            if name2pseudofixturedef is not None and argname in name2pseudofixturedef:
                fixturedef = name2pseudofixturedef[argname]
            else:
                fixturedef = FixtureDef(
                    fixturemanager=self.definition.session._fixturemanager,
                    baseid="",
                    argname=argname,
                    func=get_direct_param_fixture_func,
                    scope=scope_,
                    params=None,
                    unittest=False,
                    ids=None,
                    _ispytest=True,
                )
                if name2pseudofixturedef is not None:
                    name2pseudofixturedef[argname] = fixturedef
            arg2fixturedefs[argname] = [fixturedef]

        # Create the new calls: if we are parametrize() multiple times (by applying the decorator
        # more than once) then we accumulate those calls generating the cartesian product
        # of all calls.
        newcalls = []
        for callspec in self._calls or [CallSpec2()]:
            for param_index, (param_id, param_set) in enumerate(
                zip(ids, parametersets)
            ):
                newcallspec = callspec.setmulti(
                    argnames=argnames,
                    valset=param_set.values,
                    id=param_id,
                    marks=param_set.marks,
                    scope=scope_,
                    param_index=param_index,
                )
                newcalls.append(newcallspec)
        self._calls = newcalls
```

下面是 `pytest.mark.parametrize` 函数的部分参数解析：

- `argnames`: 这是告诉 `parametrize` 要参数化的参数名称。它可以是一个字符串（如果你只参数化一个参数），或者是一个逗号分隔的字符串（如果你要同时参数化多个参数），或者是一个列表或元组，每个元素是一个要参数化的参数名称。
- `argvalues`: 这是一个包含参数值的迭代器。对于每个 `argnames` 中指定的参数，`argvalues` 提供了实际使用的值。如果 `argnames` 有多个名称，那么 `argvalues` 应该是一个序列的序列，例如，它可以是一个列表的列表或元组的列表。
- `indirect`: 当设置为 `False`（默认值）时，`argvalues` 直接应用到测试函数的参数。如果设置为 `True`，则每个参数值都会作为参数传递给对应的 `fixture function`，这个 `fixture function` 然后负责提供实际的测试值。
- `ids`: 可用于为每个参数集生成自定义的 ID 字符串，它们出现在测试输出中。如果 `ids` 是一个序列，那么它应该与 `argvalues` 的长度相同，提供每个参数集合的 ID。如果 `ids` 是一个可调用对象，那么对于每个 `argvalues` 条目会调用此函数以生成 ID。如果 `ids` 为 `None`（默认值），`pytest` 会自动生成 IDs。
- `scope`: 参数化的 `fixture` 的作用范围（可选项 `function`, `class`, `module` 或 `session`），这影响了 `fixture` 的新实例化频率。

- `_param_mark`: 内部使用参数，它被 `_pytest.mark.structures.ParameterSet` 使用，用于追踪额外的标记信息（如 `pytest.mark.xfail`），和参数化测试相关联。

这个 `parametrize` 方法的实现很大一部分在收集阶段发生，当测试用例被收集时，传递给 `argnames` 和 `argvalues` 的参数和值被用来生成多个测试用例实例。

接下来我们将逐一介绍各个参数的使用方法。

# 8.6 `argnames`参数

`pytest.mark.parametrize` 中的 `argnames` 参数主要用于指定测试函数中那些需要进行参数化的参数。这意味着，你可以为这些参数提供不同的值组合，`pytest` 会为每组值生成一个测试用例实例。这在以下场景中非常有用：

* **数据驱动测试**：需要测试函数针对不同输入数据给出的结果是否符合预期。
* **边界值分析**：检测函数对边界值和异常值的处理是否正确。
* **兼容性测试**：需要验证功能在不同环境或配置下的行为。
* **等价类划分**：根据输入数据的等价类来减少测试用例数量，但仍覆盖全部状况。
* **异常和特殊条件测试**： 当函数应对特定输入抛出异常时，可以用参数化提供这些特殊情境及其预期的异常。

## 8.6.1 测试一般函数行为

假设你有一个简单的 `add` 函数，你想要验证它对一系列输入的正确性。

```python
# content of add_function.py
def add(a, b):
    return a + b

# content of test_add_function.py
import pytest
from add_function import add

@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2),  # 普通值
    (0, 0, 0),  # 零值
    (-1, 1, 0), # 负值
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

在这个例子中，我们参数化了 `test_add` 测试函数，`argnames` 为 "a, b, expected"，表示该测试函数将接受三个参数。`pytest` 将分别对列表中的每组值运行 `test_add` 函数。

运行效果：

```shell
root@Gavin:~/code/chapter1-8# pytest test_add_function.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 3 items

test_add_function.py ...                                                [100%]

============================ 3 passed in 0.02s ================================
root@Gavin:~/code/chapter1-8#
```

## 8.6.2 边界值和错误情况

设置 `argnames` 进行参数化也使得测试边界值和错误情况变得简单：

```python
# content of division_function.py
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# content of test_division_function.py
import pytest
from division_function import divide

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (3, 1, 3),
    pytest.param(10, 0, 0, marks=pytest.mark.xfail(raises=ValueError)),
])
def test_divide(a, b, expected):
    assert divide(a, b) == expected
```

在此代码中，除了普通的测试情况，我们使用 `pytest.param` 并标记了一个测试用例，期望它会失败（`xfail`），因为除数为0时 `divide` 函数应该抛出一个 `ValueError`。

运行效果：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_division_function.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 3 items

test_division_function.py::test_divide[10-2-5] PASSED
test_division_function.py::test_divide[3-1-3] PASSED
test_division_function.py::test_divide[10-0-0] XFAIL

=========================== 2 passed, 1 xfailed in 0.03s ======================
root@Gavin:~/code/chapter1-8#
```

## 8.6.3 参数化多重模块或类

在更复杂的测试中，我们可以参数化多个模块或类的实例化参数：

```python
# content of some_module.py
class SomeClass:
    def __init__(self, value):
        self.value = value

# content of test_other_module.py
import pytest
from some_module import SomeClass

@pytest.mark.parametrize("class_instance", [SomeClass(10), SomeClass(20)])
def test_class_value(class_instance):
    assert class_instance.value in (10, 20)
```

在这个示例中，我们创建了两个 `SomeClass` 的实例并将它们用于参数化测试。对于每个实例，`pytest` 将验证实例属性 `value` 是否与预期匹配。其运行效果如下：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_other_module.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 2 items

test_other_module.py::test_class_value[class_instance0] PASSED
test_other_module.py::test_class_value[class_instance1] PASSED

================================ 2 passed in 0.02s ============================
root@Gavin:~/code/chapter1-8# 
```

再比如你有多个用户角色，每个用户角色有不同的权限，并且你想要测试每个角色是否能正确访问其应有的资源。

定义用户角色类：

```python
# content of user_roles.py
class User:
    def __init__(self, role):
        self.role = role
        self.permissions = self.set_permissions()

    def set_permissions(self):
        if self.role == 'admin':
            return ['add', 'delete', 'modify', 'view']
        elif self.role == 'moderator':
            return ['modify', 'view']
        elif self.role == 'viewer':
            return ['view']
```

创建测试文件并编写参数化测试函数：

```python
# content of test_user_roles.py
import pytest
from user_roles import User

roles = ['admin', 'moderator', 'viewer']

# 参数化测试验证不同角色用户的权限
@pytest.mark.parametrize('role', roles)
def test_user_role_permissions(role):
    user = User(role)
    if role == 'admin':
        assert 'add' in user.permissions
    elif role == 'moderator':
        assert 'modify' in user.permissions and 'add' not in user.permissions
    elif role == 'viewer':
        assert user.permissions == ['view']

    # 确认每个用户都有'view'权限
    assert 'view' in user.permissions
```

在这个例子中：

- `user_roles.py` 文件定义了 `User` 类，它有不同的权限设置，这些权限取决于用户的角色。
- `test_user_roles.py` 文件定义了使用 `pytest.mark.parametrize` 装饰器的 `test_user_role_permissions` 测试函数。这个函数参数化了 `role` 参数，为每个角色验证对应的权限。
- 根据角色的不同，测试验证用户具有正确的权限集，例如，管理员（admin）应该有添加（add）权限，而普通观察者（viewer）只有查看（view）权限。每个角色至少应该有查看（view）权限。

运行 `pytest` 命令后，`pytest` 将为所有的角色运行 `test_user_role_permissions`，确保每个用户角色的权限设置符合预期，其运行效果：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_user_roles.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 3 items

test_user_roles.py::test_user_role_permissions[admin] PASSED
test_user_roles.py::test_user_role_permissions[moderator] PASSED
test_user_roles.py::test_user_role_permissions[viewer] PASSED

============================== 3 passed in 0.02s ==============================
root@Gavin:~/code/chapter1-8#
```

## 8.6.4 兼容性测试

假设我们想要测试一个 Web 应用的几个浏览器版本之间的兼容性。我们可以用 `pytest.mark.parametrize` 来针对不同的浏览器类型和版本运行相同的一组测试，确保应用的行为一致。

```python
# content of test_compatibility_test.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

# 假设我们有一个函数返回特定浏览器的 WebDriver 实例
def get_browser_driver(browser_name, browser_version):
    if browser_name.lower() == 'firefox':
        # 需要 FirefoxDriver 和 version 匹配，此处略过实际细节
        return webdriver.Firefox()
    elif browser_name.lower() == 'chrome':
        # 需要 ChromeDriver 和 version 匹配，同上
        return webdriver.Chrome()
    # 添加更多的浏览器配置实现
    # ...

# 使用参数化测试不同的浏览器和版本
@pytest.mark.parametrize("browser_name, browser_version", [
    ('Firefox', '80'),
    ('Chrome', '85'),
    # 您可以添加更多的浏览器与版本作为组合
    # ('Safari', '13'),
    # ('Edge', '85'),
])
def test_browser_compatibility(browser_name, browser_version):
    # 获取对应的 WebDriver 实例
    driver = get_browser_driver(browser_name, browser_version)
    try:
        # 测试你的 Web 应用
        driver.get("https://your.web.application")
        element = driver.find_element(By.ID, "someElementId")
        # 添加你的断言，例如检查一个元素是否存在
        assert element is not None
        # 添加更多的操作和断言来验证浏览器兼容性
    finally:
        # 测试完成后，关闭浏览器
        driver.quit()
```

在这个示例中：

- 使用 `browser_name` 和 `browser_version` 这两个参数来标识不同的浏览器和版本组合。
- `get_browser_driver` 函数负责根据提供的参数返回一个相应的 `WebDriver` 对象实例。在现实场景下，这会涉及到匹配指定版本的浏览器驱动。
- `test_browser_compatibility` 是一个使用 `pytest.mark.parametrize` 参数化的测试函数，它遍历不同的浏览器参数组合来执行测试。
- 实际的测试将通过 `WebDriver` 实例访问 Web 应用，并进行检查，如检测特定元素是否出现在页面上。
- 使用 `try...finally` 语句确保在测试结束后关闭浏览器窗口，以便合理地管理资源。

## 8.6.5 等价类划分

在软件测试中，等价类划分是一种测试技术，它将输入数据划分为有效或无效的等价类，然后从每个等价类中选择代表性的值进行测试。这种方法可以减少测试用例的数量，同时保持较高的测试覆盖率。

`pytest.mark.parametrize` 能极大地简化等价类测试的实施。你可以定义不同的测试参数并赋予代表不同等价类的值，`pytest` 会为你的测试函数逐一以这些参数运行。这样做可以有效地将各种等价类的测试用例融合进单个测试函数中。

**使用场景**

假设我们测试一个密码验证函数 `is_valid_password`，它接受一个字符串并确定它是否为有效密码。有效密码需满足如下规则：

- 至少8个字符长
- 包含字母和数字
- 不能包含特殊字符

我们可以基于以上规则划分等价类，其中每个等价类都由一些具有相同特性的密码组成。等价类可能包括：少于8个字符的密码、只包含字母的密码、只包含数字的密码、既包含字母也包含数字但包含特殊字符的密码等。

**代码示例与注解：**

下面是一个 `is_valid_password` 函数的等价类划分的测试用例示例：

```python
# content of password.py
def is_valid_password(password: str) -> bool:
    # 简化的密码验证逻辑
    has_letters = any(c.isalpha() for c in password)
    has_digits = any(c.isdigit() for c in password)
    has_special_chars = any(not c.isalnum() for c in password)
    
    # 模拟密码验证规则
    return len(password) >= 8 and has_letters and has_digits and not has_special_chars

# content of test_password.py
import pytest
from password import is_valid_password

@pytest.mark.parametrize("password, valid", [
    ("StrongPass123", True),  # 有效等价类：满足所有规则
    ("short7", False),        # 无效等价类：少于8个字符
    ("allletters", False),    # 无效等价类：只包含字母
    ("12345678", False),      # 无效等价类：只包含数字
    ("Valid123$", False),     # 无效等价类：包含特殊字符
    ("_Pytest123", False),    # 无效等价类：不能以_字符开头
    ("123Python123", True),   # 有效等价类：满足所有规则
    # 可以继续添加更多的测试参数代表不同的等价类
])
def test_password_validation(password, valid):
    assert is_valid_password(password) == valid
```

在这个示例中：

- 每组参数化数据 `(password, valid)` 表示一组测试用例，`password` 是要测试的密码字符串，`valid` 标志着密码是否应该被视为有效。
- 该测试验证 `is_valid_password` 方法是否正确地接受或拒绝等价类中的密码。
- `pytest.mark.parametrize` 按给定的参数集合针对 `test_password_validation` 测试函数进行参数化。每个测试用例对应一个特定等价类的密码，通过期望的布尔值 `valid` 来验证密码验证逻辑。

运行效果：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_password.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 7 items

test_password.py::test_password_validation[StrongPass123-True] PASSED
test_password.py::test_password_validation[short7-False] PASSED
test_password.py::test_password_validation[allletters-False] PASSED
test_password.py::test_password_validation[12345678-False] PASSED
test_password.py::test_password_validation[Valid123$-False] PASSED
test_password.py::test_password_validation[_Pytest123-False] PASSED
test_password.py::test_password_validation[123Python123-True] PASSED

================================ 7 passed in 0.02s ============================
root@Gavin:~/code/chapter1-8#
```

等价类测试配合使用 `pytest.mark.parametrize` 使测试写作更为简洁，并允许在最小的用例中测试尽可能广泛的输入范围。这种方法有助于快速地发现可能影响软件功能的错误。

## 8.6.6 异常和特殊条件测试

在软件测试中，处理异常和特殊条件是非常重要的。`pytest.mark.parametrize` 允许我们以申明的方式编写测试用例，以验证代码在特定条件下是否抛出预期的异常或者表现出特定的行为。

**使用场景：**

假设我们有一个应用程序，需要处理来自用户输入的数据。我们知道特定的输入可能会导致函数抛出异常，或者需要特殊的处理逻辑。使用 `pytest.mark.parametrize` ，我们可以为这些有问题的输入创建一系列的测试用例，来确认应用程序按期望进行处理。

**代码示例与注解：**

下面是一个参数化测试异常和特殊条件的例子：

```python
# content of test_exception.py
import pytest

# 模拟一个可能会抛出异常的函数
def process_input(value):
    if value == "special_condition":
        return "special_handling"
    elif value == "raise_exception":
        raise ValueError("Invalid value provided")
    return "normal_handling"

# 用例参数化测试 process_input 函数
@pytest.mark.parametrize("test_input,expected_exception,expected_result", [
    ("normal_value", None, "normal_handling"),                  # 正常情况
    ("special_condition", None, "special_handling"),            # 特殊处理情况
    pytest.param("raise_exception", ValueError, None,           # 预期抛出异常
                 marks=pytest.mark.xfail),                      # 使用 xfail 标记预期失败的测试
])
def test_process_input(test_input, expected_exception, expected_result):
    if expected_exception:
        with pytest.raises(expected_exception):                 # 验证异常抛出
            process_input(test_input)
    else:
        assert process_input(test_input) == expected_result     # 验证期望的结果
```

运行结果如下：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_exception.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 3 items

test_exception.py::test_process_input[normal_value-None-normal_handling] PASSED
test_exception.py::test_process_input[special_condition-None-special_handling] PASSED
test_exception.py::test_process_input[raise_exception-ValueError-None] XPASS

========================= 2 passed, 1 xpassed in 0.02s =========================
root@Gavin:~/code/chapter1-8#
```

在这个测试中：

- `test_input` 是我们函数 `process_input` 将要处理的输入值。

- `expected_exception` 是我们期望的异常（如果我们预期会有异常抛出）。

- `expected_result` 是期望的处理结果（如果没有异常）。

- `pytest.mark.parametrize`创建了三个测试用例，每个对应于不同的输入条件：
- 首先是一个正常的输入，不期望任何异常。
  - 接着是一个“特殊条件”的输入，我们期待它返回一个特殊的处理结果。
- 最后，我们预期一个应该抛出 `ValueError` 异常的输入。在这里，我们使用了 `pytest.param` 来单独为这个测试用例标记一个预期失败（`xfail`）。

- 测试函数 `test_process_input` 使用 `pytest.raises` 上下文管理器来验证异常抛出。如果没有期望异常，它将验证函数返回的处理结果。

**异常和特殊条件测试的价值：**

参数化测试不仅用于普通的输入和输出验证，它也是处理复杂场景（如异常、特殊值、边界条件）的有力工具。它能够有效地验证不同的输入如何影响应用程序的行为，并确保程序能够正确处理预期之外的情况。通过参数化测试，可以确保我们的代码在面对错误的、意外的或恶意的输入时也能够以安全和合理的方式失败。此外，利用 `pytest` 的简单的 API 和强大的功能，可以提高测试代码的清晰性和维护程度。

## 8.6.7 常见的argnames语法异常

`pytest.mark.parametrize` 通过参数 `argnames` 为测试函数提供了参数化的输入值。然而，在使用 `argnames` 时，如果不规范或者不注意，便容易犯错。以下是超过10种使用 `pytest.mark.parametrize` 中 `argnames` 可能出现错误的场景，请读者避坑：

### 8.6.7.1 错误的参数名

```python
# 错误：测试函数中没有定义 'input' 参数
@pytest.mark.parametrize("input, expected", [(1, True), (0, False)])
def test_is_positive(number):
    assert (number > 0) == expected
```

### 8.6.7.2 参数名与测试函数参数顺序不匹配

```python
# 错误：参数名的顺序与测试函数中参数的顺序不一致
@pytest.mark.parametrize("expected, number", [(True, 1), (False, 0)])
def test_is_positive(number, expected):
    assert (number > 0) == expected
```

### 8.6.7.3 参数名未用逗号分隔

```python
# 错误：参数名应使用逗号分隔
@pytest.mark.parametrize("number expected", [(1, True), (0, False)])
def test_is_positive(number, expected):
    assert (number > 0) == expected
```

### 8.6.7.4 参数名使用了python关键字

```python
# 错误：'def' 是一个 Python 关键字
@pytest.mark.parametrize("def, expected", [(1, True), (0, False)])
def test_is_positive(message_def, expected):
    assert (message_def > 0) == expected
```

### 8.6.7.5 使用了不存在的参数名

```python
# 错误：'nonexistent_param' 在测试函数中不存在
@pytest.mark.parametrize("number, nonexistent_param", [(1, True), (0, False)])
def test_is_positive(number, expected):
    assert (number > 0) == expected
```

### 8.6.7.6 参数名包含空格

```python
# 错误：参数名不应包含空格
@pytest.mark.parametrize("number , expected", [(1, True), (0, False)])
def test_is_positive(number, expected):
    assert (number > 0) == expected
```

### 8.6.7.7 使用了特殊字符作为参数名

```python
# 错误：'$invalid_name' 包含非法字符
@pytest.mark.parametrize("number, $invalid_name", [(1, True), (0, False)])
def test_is_positive(number, expected):
    assert (number > 0) == expected
```

### 8.6.7.8 忘记将参数名包含在字符串中

```python
# 错误：应将参数名放置在字符串中
@pytest.mark.parametrize(number, expected, [(1, True), (0, False)])
def test_is_positive(number, expected):
    assert (number > 0) == expected
```

### 8.6.7.9 参数名字符串中的参数间存在额外的字符

```python
# 错误：参数名字符串中的参数间出现额外字符（例如分号）
@pytest.mark.parametrize("number; expected", [(1, True), (0, False)])
def test_is_positive(number, expected):
    assert (number > 0) == expected
```

### 8.6.7.10 将一个参数名字符串错误地写为多个参数

```python
# 错误：将一个意图的参数 'number_and_expected' 写成了两个参数名
@pytest.mark.parametrize("number_and_expected", [(1, True), (0, False)])
def test_is_positive(number, expected):
    assert (number > 0) == expected
```

### 8.6.7.11 参数名类型不正确

```python
# 错误：参数名应该是一个字符串或字符串序列
@pytest.mark.parametrize(123, [(1, True), (0, False)])
def test_is_positive(number, expected):
    assert (number > 0) == expected
```

### 8.6.7.12 使用了非法的变量名称

```python
# 错误：'-invalid-name' 不是一个有效的 Python 变量名
@pytest.mark.parametrize("number, -invalid-name", [(1, True), (0, False)])
def test_is_positive(number, expected):
    assert (number > 0) == expected
```

### 8.6.7.13 使用了 Python 保留的属性名

```python
# 错误： '__class__' 是 Python 的保留属性名
@pytest.mark.parametrize("number, __class__", [(1, True), (0, False)])
def test_is_positive(number, expected):
    assert (number > 0) == expected
```

在编写参数化测试时，确保避免这些常见错误，参数名称必须与测试函数中的参数匹配，用逗号分隔且无额外空格，同时是有效的Python变量名称。保持代码的整洁和语法的正确是编写成功的参数化测试的基础。

# 8.7 argvalues参数

`pytest.mark.parametrize` 中的 `argvalues` 参数用来定义测试用例的参数值集合，这个参数值集合将会与 `argnames` 参数中定义的参数名相对应。 `argvalues` 是一个可迭代对象，通常是一个列表或元组，其中包含一系列用于测试的参数值。

- 当 `argnames` 参数只有一个参数名时，`argvalues` 是一个单层序列，比如：`[1, 2, 3]`。
- 当 `argnames` 有多个参数时，`argvalues` 就是一个序列的序列（例如：列表的列表或元组的列表），其中每个内部序列或元组都包含了 `argnames` 参数中每个名字对应的值。

这些值将被 `pytest` 处理并转化为每一次测试函数调用的参数。

## 8.7.1 正常情况下为argvalues赋值

**单参数的情况**：

假设我们有一个测试函数测试数字是否为正数，我们可以为这个参数化测试提供不同的数字值。

```python
# content of test_normal_case_single_parameter.py
import pytest

@pytest.mark.parametrize("num", [1, 2, 3, -1, -2, 0])
def test_is_positive(num):
    assert (num > 0) == (num == 1 or num == 2 or num == 3)
```

在这个例子中，每一个 `num` 值都将单独传递给 `test_is_positive` 测试函数。

**多参数的情况**：

如果我们想测试一个函数是否能正确处理用户名和密码的组合，则可以同时为用户名和密码参数化测试。

```python
# content of test_normal_case_multiple_parameter.py
def validate(username, password):
    # 假设有效的用户名和密码分别是"user1"和"s3cret"
    return username == "user1" and password == "s3cret"

import pytest

# 装饰器将参数化 test_validate_login 函数
@pytest.mark.parametrize(
    "username, password, expected",
    [   
        ("user1", "s3cret", True),     # 正确的用户名和密码
        ("user1", "", False),          # 密码为空
        ("", "password", False),       # 用户名为空
        ("", "", False)                # 用户名和密码都为空
    ]
)
def test_validate_login(username, password, expected):
    # 调用 validate 函数并检测结果是否符合预期
    result = validate(username, password)
    assert result == expected
```

这个 `validate` 函数假设只有一个特定的用户名/密码组合是有效的，即用户名为 `"user1"` 且密码为 `"s3cret"`。测试用例包括一组有效的登录凭证和三组无效的凭证。基于这些输入，函数的期望返回值（`expected`）被设置为 `True` 或 `False`。在这个例子中，每一组 `(username, password, expected)` 被作为一组参数传递给 `test_validate_login` 测试函数。

## 8.7.2 特殊情况 - 参数化特定值导致的异常

参数化不仅可以用来处理常规的值，还可以用来测试特定输入应当触发异常的情况。

```python
# content of test_exceptions_caused_by_parameterizing_specific_values.py
import pytest

@pytest.mark.parametrize(
    "input, exception",
    [(0, ZeroDivisionError), ("string", TypeError), (1, None)]
)
def test_divide_exception(input, exception):
    if exception:
        with pytest.raises(exception):
            result = 10 / input
    else:
        result = 10 / input
        assert result == 10
```

在这个例子中，我们为 `test_divide_exception` 提供了几种不同的 `input` 值，期望的是在输入为 0 或 "string" 时触发异常。我们使用 `pytest.raises` 来断言当输入值导致异常时，该异常确实被抛出了。

## 8.7.3 argvalues来自pytest.param

`pytest.param`可以用作 `pytest.mark.parametrize` 的 `argvalues` 参数的一部分，进一步提升参数化的灵活性、用例的可读性和可管理性。下面通过一个具体的例子来展示如何使用 `pytest.param`为`argvalues`赋值。

假设我们有一个数学计算库，我们想要对 `sqrt` 函数进行测试。其中，对于负数输入，我们预先知道函数应该抛出 `ValueError`。

```python
# content of mymathlib.py 
import math

def sqrt(value):
    """Calculate the square root of a number."""
    if value < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return math.sqrt(value)


# content of test_with_pytest_param_for_argvalues.py
import pytest
import math
from mymathlib import sqrt

# 对 sqrt 函数进行参数化测试
@pytest.mark.parametrize(
    "test_input, expected, marks",
    [
        pytest.param(4, 2, None, id="正数"),
        pytest.param(0, 0, None, id="零值"),
        pytest.param(-1, None, pytest.mark.xfail(raises=ValueError), id="负数-应抛出异常")
    ]
)
def test_sqrt(test_input, expected, marks):
    if marks:
        with pytest.raises(ValueError):
            assert sqrt(test_input) == expected
    else:
        assert sqrt(test_input) == expected
```

在这里：

- 我们传递了一个 `pytest.param` 对象列表给 `pytest.mark.parametrize` 装饰器。
- 每个 `pytest.param` 对象接受 `test_input`（测试输入值），`expected`（预期结果）和一个 `marks` 参数，使用这个参数可以传递 `pytest.mark`。
- 针对预期抛出异常的测试用例（负数输入），我们使用 `pytest.mark.xfail` 并指定 `raises=ValueError`，这表明测试结果预期会失败并且会抛出 `ValueError` 异常。
- 我们为每个测试用例设置了可读性强的 ID（如 `"正数"`、`"零值"` 和 `"负数-应抛出异常"`），这将在测试报告中显示，使得理解测试结果变得更容易。
- 在 `test_sqrt` 函数体内，我们首先根据 `marks` 检查是否有异常的预期。如果有，我们使用了 `pytest.raises` 来断定函数是否像期望的那样抛出异常。如果没有标记，我们则直接校验结果。


## 8.7.4 argvalues来自外部

在 `pytest` 中，你可以将 `argvalues` 参数来源于外部文件或外部数据源，比如 JSON、CSV 文件或数据库。这种做法用于将测试数据与测试逻辑分离，便于管理测试数据，也便于数据的重用和共享。

### 8.7.4.1 从 JSON 文件加载测试数据

假设你有一个 `test_data.json` 文件，包含了一系列的测试用例数据：

```json
# content of test_data.json
[
    {"input": 1, "expected": 2},
    {"input": 2, "expected": 4},
    {"input": 3, "expected": 6}
]
```

使用以下方法可以将这个 JSON 文件加载为 `argvalues`：

```python
# content of test_argvalues_from_external_json_file.py
import pytest
import json

# 加载 JSON 文件中的测试数据作为参数值
def load_test_data_from_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
        return [(case["input"], case["expected"]) for case in data]

# 参数化测试，使用来自 JSON 文件的数据
@pytest.mark.parametrize("test_input, expected", load_test_data_from_json("test_data.json"))
def test_function(test_input, expected):
    assert test_input * 2 == expected
```

在这个例子中，`load_test_data_from_json` 函数用于读取 JSON 文件并返回一个包含测试数据的列表。该列表直接用作 `pytest.mark.parametrize` 的 `argvalues` 参数。执行结果如下：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_argvalues_from_external_json_file.py
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 3 items

test_argvalues_from_external_json_file.py::test_function[1-2] PASSED
test_argvalues_from_external_json_file.py::test_function[2-4] PASSED
test_argvalues_from_external_json_file.py::test_function[3-6] PASSED

================================ 3 passed in 0.02s ============================
root@Gavin:~/code/chapter1-8#
```

### 8.7.4.2 从 CSV 文件加载测试数据

假设你有一个 `test_data.csv` 文件：

```shell
# content of test_data.csv
input,expected
1,2
2,4
3,6
```

可以使用 `csv` 模块加载测试数据：

```python
# content of test_argvalues_from_external_csv_file.py
import pytest
import csv

# 从 CSV 文件加载测试数据
def load_test_data_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [tuple(row.values()) for row in reader]

# 参数化测试，使用来自 CSV 文件的数据
@pytest.mark.parametrize("test_input, expected", load_test_data_from_csv("test_data.csv"))
def test_function(test_input, expected):
    assert int(test_input) * 2 == int(expected)
```

在这里，`load_test_data_from_csv` 函数用于读取 CSV 文件并解析出测试数据。注意，由于从 CSV 读取的所有值都是字符串类型，可能需要在测试函数中进行类型转换。运行效果如下：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_argvalues_from_external_csv_file.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 3 items

test_argvalues_from_external_csv_file.py::test_function[1-2] PASSED
test_argvalues_from_external_csv_file.py::test_function[2-4] PASSED
test_argvalues_from_external_csv_file.py::test_function[3-6] PASSED

=============================== 3 passed in 0.02s =============================
root@Gavin:~/code/chapter1-8#
```

### 8.7.4.3 外部数据源的好处

- **易于维护**：使用外部文件管理测试数据更易于数据的更新和维护。
- **解耦**：这种方式有助于将测试逻辑与测试数据解耦，测试函数专注于逻辑，而数据管理可以独立进行。
- **可扩展性**：当测试用例的数据集成长时，存储在外部文件的数据易于扩展。

### 8.7.4.4 注意事项和进一步说明

- 确保数据文件格式正确，并且 Python 脚本有足够的权限去读取这个数据文件。
- 在 CI/CD 管道中，数据文件应该与测试用例一起维护，以确保测试环境的一致性。
- 处理外部数据时，要注意对异常情况进行检查，例如数据文件不存在、数据格式错误等。

综上所述，将 `argvalues` 参数化数据来源于外部文件是对测试环境的一种优化，提供了同时保持测试逻辑简洁性和增强测试数据管理能力的解决方案。

## 8.7.5 使用 `pytest.mark.parametrize` 的 `argvalues` 参数注意事项

- `argvalues` 的长度应与 `argnames` 中定义的参数数量一致。每个内部序列或元组的长度应该与 `argnames` 中的参数名数量相匹配。
- `pytest` 会根据你提供的 `argvalues` 运行对应数量的测试。传入错误的 `argvalues` 会导致测试错误或不如预期运行。
- 在实际使用时，你很可能需要处理普通用例、边界条件、异常输入甚至错误用例的组合。通过使用 `argvalues` ，你可以简洁地管理所有这些测试条件。

使用 `pytest.mark.parametrize` 中的 `argvalues` 参数能够显著提高你的测试效率和覆盖率，帮助你更好地验证软件在各种条件下的行为。通过明智地选择 `argvalues` ，你可以确保你的测试尽可能全面地覆盖了所有重要的测试场景。

# 8.8 indirect参数

`indirect` 参数在 `pytest.mark.parametrize` 装饰器中用来指示某些测试参数应该通过 `fixture` 间接传递给测试函数。当设置 `indirect` 为 `True`，将会调用与参数名对应的 `fixture` 函数，该 `fixture` 函数接收 `param` 参数来决定它的返回值。`inditect`参数常用于如下场景：

- **复杂的参数初始化** - 当测试参数需要通过复杂的设置步骤进行初始化时，使用 `fixture` 可以使代码更加整洁。
- **共享资源配置** - 当你需要对参数化的测试使用不同的配置时，`indirect` 参数可以确保每个测试能够使用配置后的资源。
- **上下文管理** - 当需要在测试前后执行清理或其他上下文管理时，通过 `fixture` 管理这一逻辑可以让测试函数保持简洁。

## 8.8.1 示例一：基本使用场景

假设我们正在测试一个需要数据库连接的函数，而我们希望对每个参数使用的是不同的数据库配置。

```python
import pytest

# 假设有一个 fixture 用来设置数据库连接
@pytest.fixture
def db_conn(request):
    db_name = request.param  # 获取参数化传递的数据库名称
    return setup_db_connection(db_name)

# 参数化测试，indirect 指示 db_name 通过 db_conn fixture 传递
@pytest.mark.parametrize("db_name, expected_result", [
    ("db_test1", True),
    ("db_test2", False),
], indirect=["db_name"])
def test_query(db_conn, expected_result):
    result = run_some_db_query(db_conn)  # 假设这是我们要测试的函数
    assert result == expected_result
```

在这个例子中：

- `db_name` 和 `expected_result` 为参数化的参数，我们通过 `indirect=["db_name"]` 指示 `db_name` 参数应当通过 `db_conn` fixture 传递。
- `db_conn` fixture 接收 `db_name` 作为输入，并设置数据库连接。它利用 `request.param` 来获取参数化的值。
- `test_query` 测试函数接收通过 `db_conn` fixture 设置好的数据库连接 `db_conn` 和 `expected_result`，然后对数据库查询结果进行断言。

## 8.8.2 示例二：测试不同用户权限

如果我们想要测试不同用户角色的权限，可能需要先以不同用户登录然后执行操作，此时 `indirect` 参数也很有用。

```python
import pytest

# 一个 fixture 来处理登陆逻辑
@pytest.fixture
def login_user(request):
    return login_as_user(request.param)  # 假设这个函数执行登录操作

# 参数化测试不同的用户角色
@pytest.mark.parametrize("user_role, can_create_project", [
    ("admin", True),
    ("guest", False),
], indirect=["user_role"])
def test_create_project(login_user, can_create_project):
    user = login_user
    assert user.can_create_project() == can_create_project
```

在这个例子中：

- 我们想要测试不同角色用户创建项目的能力。
- `user_role` 和 `can_create_project` 是测试参数。通过 `indirect=["user_role"]` 我们告诉 `pytest`，要通过一个名为 `login_user` 的 fixture 间接获取 `user_role` 参数。
- `login_user` fixture 接收 `user_role` 作为输入，执行登录操作。
- `test_create_project` 测试函数使用登录后的用户对象进行测试，并根据用户角色断言是否可以创建项目。

## 8.8.3 小结

使用 `indirect` 参数使我们能够将复杂的或重复的参数设置逻辑抽离到 `fixture` 中，从而使测试函数本身保持语义清晰，逻辑简单。这在复杂环境配置或参数设置较繁琐时尤其有效。

# 8.9 ids参数

`pytest.mark.parametrize` 的 `ids` 参数用于为每一组参数化的测试用例生成一个唯一的识别 ID。这些 ID 可以帮助我们更容易地识别测试用例，尤其在触发错误或异常时。`ids`参数有如下常见使用场景：

* **增加易读性** - 自定义 ID 提供关于测试的更多信息，比自动生成的数字更有意义。
* **国际化测试** - 使用中文或其他非英文字符作为 ID 来满足特定地区的测试报告需求。
* **区分相同参数值的不同用例** - 使用自定义 ID 来区分在不同上下文下具有相同参数值的测试用例。
* **动态生成 ID** - 通过函数根据测试数据动态生成 ID，尤其适用于在运行时可能已知测试数据的场景。
* **ID 覆盖** - `pytest.mark.parametrize` 装饰器如果被重复应用，ID 列表将被覆盖。
* **特殊格式化**：当参数是对象或者复杂的数据结构时，格式化更友好的 ID 字符串。

## 8.9.1 ids 长度

如果给`ids`传递的是列表/元祖，那么ids的长度需要与argvalues的长度保持一致，否则会报错，如下示例:

```python
# content of test_ids_length.py
import pytest


# 如果 `ids` 的长度不匹配，将会导致错误
@pytest.mark.parametrize(
    "input, expected", 
    [("a", 1), ("b", 2), ("c", 3)],
    ids=["first", "second"]  # 这里的 `ids` 数量要匹配 `argvalues`参数数量
)
def test_length_mismatch(input, expected):
    assert ord(input) - ord('a') + 1 == expected
```

执行结果：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_ids_length.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 0 items / 1 error

==================================== ERRORS ===================================
_______________ ERROR collecting chapter1-8/test_ids_length.py ________________
In test_length_mismatch: 3 parameter sets specified, with different number of ids: 2
============================ short test summary info ===========================
ERROR test_ids_length.py - Failed: In test_length_mismatch: 3 parameter sets specified, with different number of ids: 2
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
================================ 1 error in 0.14s ==============================
root@Gavin:~/code/chapter1-8#
```

正确代码示例如下：

```python
import pytest


# 如果 `ids` 的长度不匹配，将会导致错误
@pytest.mark.parametrize(
    "input, expected", 
    [("a", 1), ("b", 2), ("c", 3)],
    # ids=["first", "second"]  # 这里会报错，因为 `ids` 数量 `argvalues`参数数量不匹配
    ids=["first", "second", "third"]  # 这里是正确的
)
def test_length_mismatch(input, expected):
    assert ord(input) - ord('a') + 1 == expected
```

## 8.9.2 ids 相同

如果`ids`相同，则会自动在原`ids`值后面添加索引，示例代码如下：

```python
# content of test_same_ids.py
import pytest

# 如果提供了相同的 ID，它会在报告中显示出相同的名称，但测试仍将独立运行
@pytest.mark.parametrize(
    "input, expected",
    [("a", 1), ("b", 2)],
    ids=["same_id", "same_id"]  # 相同 ID，测试仍分开执行
)
def test_same_ids(input, expected):
    assert ord(input) - ord('a') + 1 == expected
```

执行结果：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_same_ids.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 2 items

test_same_ids.py::test_same_ids[same_id0] PASSED
test_same_ids.py::test_same_ids[same_id1] PASSED

================================ 2 passed in 0.01s =============================
root@Gavin:~/code/chapter1-8
```

## 8.9.3 使用中文作为ids

ids是支持非 ASCII 字符的，如中文，但使用中文默认情况下输入字节序列，示例代码如下：

```python
# content of test_chinese_ids.py
import pytest

@pytest.mark.parametrize(
    "input, expected",
    [("a", 1), ("b", 2)],
    ids=["第一", "第二"]
)
def test_chinese_ids(input, expected):
    assert ord(input) - ord('a') + 1 == expected
```

执行结果：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_chinese_ids.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 2 items

test_chinese_ids.py::test_chinese_ids[\u7b2c\u4e00] PASSED
test_chinese_ids.py::test_chinese_ids[\u7b2c\u4e8c] PASSED

=============================== 2 passed in 0.01s =============================
root@Gavin:~/code/chapter1-8#
```

如何更友好的展示出中文？是否还记得第三章节《pytest参数详解》的“[pytest] ini-options 相关参数”中介绍到的一个参数`disable_test_id_escaping_and_forfeit_all_rights_to_community_support`？这个参数的设置可以禁用 `pytest` 中用于测试ID的特殊字符转义。

在`pytest.ini`文件中增加此参数，并设置为True，再执行上述测试用例：

```ini
[pytest]
disable_test_id_escaping_and_forfeit_all_rights_to_community_support = True
```

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_chinese_ids.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 2 items

test_chinese_ids.py::test_chinese_ids[第一] PASSED
test_chinese_ids.py::test_chinese_ids[第二] PASSED

================================= 2 passed in 0.01s ===========================
root@Gavin:~/code/chapter1-8#
```

## 8.9.4 通过函数生成ids

`ids` 也可以是一个函数，它将对每一组参数调用：

```python
# content of test_ids_function.py
import pytest

def id_func(params):
    return f"{params}"

@pytest.mark.parametrize(
    "input, expected",
    [("a", 1), ("b", 2)],
    ids=id_func
)
def test_ids_func(input, expected):
    assert ord(input) - ord('a') + 1 == expected
```

执行效果如下：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_ids_function.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 2 items

test_ids_function.py::test_ids_func[a-1] PASSED
test_ids_function.py::test_ids_func[b-2] PASSED

================================ 2 passed in 0.02s ============================
root@Gavin:~/code/chapter1-8#
```

## 8.9.5 ids 覆盖

在讲述`ids`覆盖之前，我们先来看一个示例，同一测试函数使用多个 parametrize 装饰器，且都携带了`ids`参数：

```python
# content of test_multiple_parametrize_with_ids.py
import pytest

@pytest.mark.parametrize("input", ["a", "b"], ids=["input_a", "input_b"])
@pytest.mark.parametrize("expected", [1, 2], ids=["output_1", "output_2"])
def test_ids_override(input, expected):
    assert ord(input) - ord('a') + 1 == expected
```

这里的`@pytest.mark.parametrize("expected", [1, 2], ids=["output_1", "output_2"])`会覆盖`@pytest.mark.parametrize("input", ["a", "b"], ids=["input_a", "input_b"])`么？答案是否定的，其执行效果是：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_multiple_parametrize_with_ids.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 4 items

test_multiple_parametrize_with_ids.py::test_ids_override[output_1-input_a] PASSED
test_multiple_parametrize_with_ids.py::test_ids_override[output_1-input_b] FAILED
test_multiple_parametrize_with_ids.py::test_ids_override[output_2-input_a] FAILED
test_multiple_parametrize_with_ids.py::test_ids_override[output_2-input_b] PASSED

=================================== FAILURES ====================================
_____________________ test_ids_override[output_1-input_b] _______________________

input = 'b', expected = 1

    @pytest.mark.parametrize("input", ["a", "b"], ids=["input_a", "input_b"])
    @pytest.mark.parametrize("expected", [1, 2], ids=["output_1", "output_2"])
    def test_ids_override(input, expected):
>       assert ord(input) - ord('a') + 1 == expected
E       AssertionError: assert ((98 - 97) + 1) == 1
E        +  where 98 = ord('b')
E        +  and   97 = ord('a')

test_multiple_parametrize_with_ids.py:6: AssertionError
_____________________ test_ids_override[output_2-input_a] ______________________

input = 'a', expected = 2

    @pytest.mark.parametrize("input", ["a", "b"], ids=["input_a", "input_b"])
    @pytest.mark.parametrize("expected", [1, 2], ids=["output_1", "output_2"])
    def test_ids_override(input, expected):
>       assert ord(input) - ord('a') + 1 == expected
E       AssertionError: assert ((97 - 97) + 1) == 2
E        +  where 97 = ord('a')
E        +  and   97 = ord('a')

test_multiple_parametrize_with_ids.py:6: AssertionError
============================ short test summary info =============================
FAILED test_multiple_parametrize_with_ids.py::test_ids_override[output_1-input_b] - AssertionError: assert ((98 - 97) + 1) == 1
FAILED test_multiple_parametrize_with_ids.py::test_ids_override[output_2-input_a] - AssertionError: assert ((97 - 97) + 1) == 2
============================ 2 failed, 2 passed in 0.10s =========================
root@Gavin:~/code/chapter1-8#
```

为什么输出结果中的ids信息不是：

```shell
test_multiple_parametrize_with_ids.py::test_ids_override[input_a-output_1] PASSED
test_multiple_parametrize_with_ids.py::test_ids_override[input_a-output_2] FAILED
test_multiple_parametrize_with_ids.py::test_ids_override[input_b-output_1] FAILED
test_multiple_parametrize_with_ids.py::test_ids_override[input_b-output_2] PASSED
```

而是：

```shell
test_multiple_parametrize_with_ids.py::test_ids_override[output_1-input_a] PASSED
test_multiple_parametrize_with_ids.py::test_ids_override[output_1-input_b] FAILED
test_multiple_parametrize_with_ids.py::test_ids_override[output_2-input_a] FAILED
test_multiple_parametrize_with_ids.py::test_ids_override[output_2-input_b] PASSED
```

现在，让我们看一下代码的注解：

```python
import pytest

# 应用两次 parametrize 装饰器，创建参数的笛卡尔积
@pytest.mark.parametrize("input", ["a", "b"], ids=["input_a", "input_b"])
@pytest.mark.parametrize("expected", [1, 2], ids=["output_1", "output_2"])
def test_ids_override(input, expected):
    # 测试用例由 parametrize 装饰器决定的参数组合执行
    # 参数组合的 ID 会按照 parametrize 装饰器在函数上的顺序反向串联，
    # 所以最终的 ID 会是：output_1-input_a, output_1-input_b, output_2-input_a, output_2-input_b
    # 这些 ID 将在测试输出和报告中用来标识测试用例
    assert ord(input) - ord('a') + 1 == expected
```

在 `pytest` 的执行过程中，测试函数 `test_ids_override` 会根据参数化装饰器的定义顺序进行四次独立的调用。因此，如果我们有例子中的两个 `pytest.mark.parametrize` 装饰器，装饰器靠近函数定义的 `ids` 将优先被连接到参数 ID 中。

通过上面的例子，我们看到：同一测试函数使用多个 parametrize 装饰器，且都携带了`ids`参数，不会发生`ids`覆盖问题。

那什么情况下会发生`ids`覆盖呢？

在 `pytest.mark.parametrize` 中使用 `pytest.param` 可以让我们为每个具体的参数集（Parameter Set）设置额外的元信息——比如测试 ID、标记（marks）或者预期失败（xfail）等。如果我们对同一个参数使用多次 `pytest.mark.parametrize` 装饰器时，`ids` 很可能会相互覆盖。

当多个 `pytest.mark.parametrize` 修饰符被应用于同一个测试函数，并且每个修饰符都指定了 `ids`，`pytest` 将为生成的参数笛卡尔积创建一个合成的 ID，该 ID 是通过把每个修饰符生成的单独 ID 按照它们被应用的顺序进行连接组合而成的。

如果在这些装饰器中使用 `pytest.param` 指定了 `ids`，而且装饰器被按照不同的顺序应用，那么最终每个测试用例的 ID 将取决于最里侧的装饰器（离函数定义最近的那个）为每个参数集提供的 `ids` 值，先前的 `ids` 将被覆盖。

以下是一个详细的代码示例和对应的注解，说明如何使用带有 `pytest.param` 的 `pytest.mark.parametrize` 并展示了 `ids` 覆盖的情况：

```python
# content of test_ids_override_v1.py
import pytest


# 参数化的同时使用ids列表和pytest.param单独为某个参数对指定ID
@pytest.mark.parametrize(
    "base, exponent, expected", 
    [
        (2, 3, 8),  # 这个用例将会自动分配一个从ids列表中的ID
        pytest.param(2, 4, 16, id="id_explicitly_set")  # 对于这个用例，我们显式指定了id
    ],
    ids=["first_exp", None]  # ids列表为第一个测试用例指定ID，第二个用 `pytest.param` 中指定的ID
)
def test_power(base, exponent, expected):
    # 测试函数是否得到了预期的平方值（指数运算）
    assert base ** exponent == expected
```

在上面的代码中：

- 测试函数 `test_power` 的参数 `base`、`exponent` 和 `expected` 被 `pytest.mark.parametrize` 参数化。
- 第一组参数 `(2, 3, 8)` 将自动从 `ids` 列表中获取ID，因为对应的 `ids` 列表项是 `["first_exp", None]`。也就是说，第一个测试用例的ID为 "first_exp"；`None` 指定为第二个参数对的ID，但不会起作用，因为明确以 `pytest.param` 设置了ID "id_explicitly_set"。
- `pytest.param` 用于第二组参数 `(2, 4, 16)`，并显式指定了 ID 为 `"id_explicitly_set"`。因为 `pytest.param` 提供了一个显式的ID，所以 `ids` 列表中的 `None` 将被忽略。

在测试运行时，生成的ID将如下：

- 第一组参数 `(2, 3, 8)` 的测试用例将会使用从 `ids` 列表中的 `"first_exp"` 作为其ID。
- 第二组参数 `(2, 4, 16)` 的测试用例将会使用 `"id_explicitly_set"` 作为其ID，即使 `ids` 列表为该位置指定了 `None`，因为通过 `pytest.param` 显式指定的ID将优先于通过 `ids` 列表隐式指定的那些。

运行结果是：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_ids_override_v1.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 2 items

test_ids_override_v1.py::test_power[first_exp] PASSED
test_ids_override_v1.py::test_power[id_explicitly_set] PASSED

================================= 2 passed in 0.02s ===========================
root@Gavin:~/code/chapter1-8# 
```

我们可以在测试结果中清楚地看到，每个测试用例都具有一个明确且易于辨识的ID，其中第二个测试用例的ID是我们使用 `pytest.param` 明确为这个参数对指定的。这在测试运行结果需要明确定义的ID，以帮助更好地理解测试行为的时候非常有用。

接下来再来看上述两个示例代码的综合体：

```python
# content of test_ids_override_v2.py
import pytest

# 通过 pytest.mark.parametrize 应用第一层参数化
@pytest.mark.parametrize(
    "n", 
    [
        pytest.param(1, id="one"), 
        pytest.param(2, id="two")
    ]
)
# 应用第二层参数化，这里的 id="first" 将覆盖上面的参数化中定义的 id
@pytest.mark.parametrize("letter", [pytest.param("a", id="first"), pytest.param("b", id="second")])
def test_combine(n, letter):
    assert n in (1, 2)
    assert letter in ("a", "b")
```

在上面的代码中：

- 首先，我们对 `n` 进行了参数化，并使用 `pytest.param` 为每个值指定了一个 `id`（"one" 和 "two"）。
- 然后，对 `letter` 进行了另一轮参数化。同样使用 `pytest.param` 指定 `ids`，但这一次的 `ids` 是 "first" 和 "second"。
- 但由于 `letter` 参数化装饰器更靠近 `test_combine` 函数，所以最终的测试用例 ID 将优先基于 `letter` 参数的 `ids`，然后才是 `n` 参数中的 `pytest.param` 所指定的 `ids`。

我们预期的是：

最终生成的测试用例 IDs 被设置为第二个 `pytest.mark.parametrize` 装饰器对 `letter` 参数提供的值，也就是 "first" 和 "second"。即使 `n` 参数化提供了它自己的 IDs，也会因为被第二个装饰器的设置所覆盖。

可实际效果却是：

最终生成的测试用例 IDs 被设置为第二个 `pytest.mark.parametrize` 装饰器对 `letter` 参数提供的值和第一个 `pytest.mark.parametrize` 装饰器对`n`参数提供的值的组合体。

为什么？

当使用多个`pytest.mark.parametrize` 装饰器提供`ids`时，因为 `pytest` 在构建测试用例时合并了每一层 `parametrize` 提供的 `ids`。每一层的 `parametrize` 都独立对其参数集合进行标记，而这些标记会被合并到最终的测试用例ID中。

上述示例`test_ids_override_v2.py`代码中，“第一层参数化”和“第二层参数化”被视为两个独立的操作。这意味着，对于每一组参数（由一层内部的所有参数化装饰器定义），都会有一个与之对应的 ID。

`pytest` 对于使用多个 `parametrize` 装饰器的情况，会按照装饰器的顺序，从外到内，把装饰器所提供的参数 `ids` 组合起来，形成最后运行的测试用例的ID。这些 `ids` 是连接在一起的，按照在测试函数上定义的逆序来连接，即最接近测试函数的 `parametrize` 定义的 `ids` 最先被连接。每个测试用例的最终 `ids` 将会是第二段 `parametrize` 的 `ids` 与第一段 `parametrize` 的 `ids` 的组合，而不会发生覆盖。按照定义的顺序，最终的测试用例 ID 由 `pytest` 自动生成，将是：

- `first-one`：結合 `letter` 的 `"a"`（id="first"）和 `n` 的 `1`（id="one"）
- `first-two`：結合 `letter` 的 `"a"`（id="first"）和 `n` 的 `2`（id="two"）
- `second-one`：結合 `letter` 的 `"b"`（id="second"）和 `n` 的 `1`（id="one"）
- `second-two`：結合 `letter` 的 `"b"`（id="second"）和 `n` 的 `2`（id="two"）

正是由于这种组合方式，测试用例 `ids` 实际上是每层 `parametrize` 定义的 `ids` 的连接，并没有发生覆盖。其运行结果如下：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v test_ids_override_v2.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 4 items

test_ids_override_v2.py::test_combine[first-one] PASSED
test_ids_override_v2.py::test_combine[first-two] PASSED
test_ids_override_v2.py::test_combine[second-one] PASSED
test_ids_override_v2.py::test_combine[second-two] PASSED

================================ 4 passed in 0.02s ============================
root@Gavin:~/code/chapter1-8#
```

## 8.9.6 ids 的作用

`ids` 主要是为了使得测试报告清晰易懂，尤其是在 CI/CD 环境中，能够迅速地定位和理解失败的测试用例。除此之外，它还可以针对性的执行指定`ids`的测试用例。

比如下面的测试代码：

```python
# content of test_specifying_ids_test_case.py
import pytest

@pytest.mark.parametrize("num", [1, 2, 3], ids=["one", "two", "three"])
def test_number(num):
    assert num < 4

@pytest.mark.parametrize("letter", ["a", "b", "c"], ids=["alpha", "beta", "gamma"])
def test_letter(letter):
    assert letter in "abc"
```

上述示例代码产生6个测试用例，如果只运行所有 `id` 为 `"two"` 或 `"beta"` 的测试用例，你可以这样做：

```shell
pytest -k "two or beta" test_specifying_ids_test_case.py
```

运行结果如下：

```shell
root@Gavin:~/code/chapter1-8# pytest -s -v -k "two or beta" test_specifying_ids_test_case.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
plugins: html-4.1.1, metadata-3.0.0
collected 6 items / 4 deselected / 2 selected

test_specifying_ids_test_case.py::test_number[two] PASSED
test_specifying_ids_test_case.py::test_letter[beta] PASSED

========================= 2 passed, 4 deselected in 0.01s ======================
root@Gavin:~/code/chapter1-8#
```

使用 `-k` 参数时，确保提供的表达式适当地匹配你希望运行的测试用例 `id`。当 `ids` 参数是自动生成的，在使用 `-k` 参数时，需要考虑到生成的 `ids` 模式，以便正确匹配到测试用例。

如果你有命名冲突或不希望通过函数名匹配测试， `-k` 参数也可以与逻辑运算符 `and`、`or` 和 `not` 一起使用来进一步精确控制你需要运行的测试。例如，如果你想排除 `id` 为 `"one"` 的测试，可以使用：

```shell
pytest -k "not one"
```

请明确 `-k` 参数是基于测试函数名和 `ids`（如果被指定的话）进行匹配的，它不能直接用来指定测试函数的参数值。


## 8.9.7 注意事项和进一步说明

- **长度问题**：`ids` 的长度应该与 `argvalues` 中值的组数匹配。否则，会引发错误。如果太少，`pytest` 会无法为所有值对分配 ID。
- **相同的 ID**：虽然通常不推荐，但是技术上可以有两个具有相同 ID 的测试，这在测试报告中可能会造成混淆。
- **非 ASCII 字符**：`ids` 完全支持非 ASCII 字符，包括中文等字符，这对于国际化/本地化测试非常有用。
- **函数自动生成 `ids`**：函数应该返回一个能唯一标识参数集的字符串。当使用 `ids` 函数时，`pytest` 会将每个参数集作为元组传递给这个函数。
- **ID 覆盖**：当多个 `pytest.mark.parametrize` 装饰器应用于同一测试函数时，`pytest` 会为参数生成笛卡尔乘积，并依据最接近函数定义的 `ids` 设置 ID。如果没有显式指定，`pytest` 将生成默认 ID。

在实际应用中考虑到这些细节，将有助于编写更精确、更有信息量的测试。

# 8.10 scope参数

`scope` 参数定义了通过 `pytest.mark.parametrize` 装饰器指定的 `argnames` 参数的作用域。这不仅影响参数如何在测试函数或模块中共享，也决定了测试用例的收集和执行的顺序。每个 `scope` 对应不同的作用域级别，如 `function`（默认）、`class`、`module` 或 `session`。

当你为 `pytest.mark.parametrize` 指定 `argvalues`，你实际上是为每个 `argname` 创建了一组测试用例。`pytest` 会根据这些值的组合生成测试用例的列表，并按照特定的顺序执行它们。

`scope` 参数影响这个过程的两个方面：

* **参数共享**: 指定的 `scope` 决定了参数化的变量在哪个级别上是共享的。例如，如果 `scope` 被设置为 `module`，那么在同一模块中的所有测试用例都将使用同一组参数值，直到所有测试用例执行完毕后才会更改参数值。

* **测试用例的收集和执行顺序**: 测试用例的收集过程取决于 `scope` 的设置。对于 `function` 级别的 `scope`，每个测试函数都会对每组参数值创建一个独立的测试用例。这将导致每个测试函数都在其自己的参数上独立运行。相比之下，更高级别的 `scope`（如 `module` 或 `session`）将导致在所有测试用例中按顺序使用相同的一组参数值，从而改变测试的执行顺序。

## 8.10.1 module级别

如果没有指定 `scope` 参数时，参数化仅适用于装饰的测试函数本身，对于每组参数，测试函数都会被调用一次。如果你指定 `scope` 为 `module`，参数化将适用于整个模块级别，这意味着所有的测试函数只会接收到相同的一组参数值，直到下一个测试模块被调用。

```python
# content of test_parameterize_module_scope_v1.py
import pytest


@pytest.mark.parametrize("input, expected", [("3+5", 8), ("2+4", 6)], scope="module")
def test_eval_eval_first(input, expected):
    assert eval(input) == expected

@pytest.mark.parametrize("input, expected", [("3+5", 8), ("2+4", 6)], scope="module")
def test_eval_second(input, expected):
    assert eval(input) == expected
```

上述示例代码，运行效果如下：

```shell
collected 4 items

test_parameterize_module_scope_v1.py::test_eval_eval_first[3+5-8] PASSED
test_parameterize_module_scope_v1.py::test_eval_second[3+5-8] PASSED
test_parameterize_module_scope_v1.py::test_eval_eval_first[2+4-6] PASSED
test_parameterize_module_scope_v1.py::test_eval_second[2+4-6] PASSED
```

上述代码与下面代码效果一样：

```python
# content of test_parameterize_module_scope_v2.py
import pytest


# 指定 scope 为 module
@pytest.fixture(scope="module", params=[("3+5", 8), ("2+4", 6)])
def param_module(request):
    return request.param

def test_eval_eval_first(param_module):
    input, expected = param_module
    # 这里，同一组参数将应用到本模块的所有测试用例上，直到所有用例执行完毕才会更换另一组参数。
    assert eval(input) == expected

def test_eval_second(param_module):
    input, expected = param_module
    assert eval(input) == expected
```

喜欢哪种写法，可根据自己喜好选择。

## 8.10.2 未指定scope

我们再来看一个上述用例的一个变体：

```python
# content of test_parameterize_module_scope_v3.py
import pytest

@pytest.fixture(scope='module')
def input(request):
    return request.param


@pytest.fixture(scope='module')
def expected(request):
    return request.param

@pytest.mark.parametrize("input, expected", [("3+5", 8), ("2+4", 6)], indirect=True)
def test_eval_eval_first(input, expected):
    assert eval(input) == expected

@pytest.mark.parametrize("input, expected", [("3+5", 8), ("2+4", 6)], indirect=True)
def test_eval_second(input, expected):
    assert eval(input) == expected
```

虽然`@pytest.mark.parametrize`未显示指定`scope`参数，但通过`indirect=True`调用与参数名对应的 `fixture` 函数，对应的 `fixture` 函数有指定`scope='module'`，故而`@pytest.mark.parametrize`的`scope='module'`。上述用例的执行效果等同于`test_parameterize_module_scope_v1.py`的结果。

# 8.11 pytest_generate_tests hook方法

## 8.11.1 pytest 参数化方式

pytest实现参数化有三种方式：

* pytest.fixture() 使用fixture传递params参数实现参数化
* @pytest.mark.parametrize在测试函数或类中定义多组参数实现参数化
* pytest_generate_tests hook方法自定义参数化方法，方便扩展

## 8.11.2 pytest_generate_tests hook方法介绍

`pytest_generate_tests` 是一个功能强大的钩子（hook）函数，在 `pytest` 测试框架中用于动态地生成测试用例。与静态地使用 `@pytest.mark.parametrize` 装饰器不同，`pytest_generate_tests` 提供了更多灵活性，允许你根据复杂的逻辑或条件来定制参数化测试。这对于需要从外部数据源读取测试数据或根据某些条件生成测试用例的场景特别有用。

### 8.11.2.1 pytest_generate_tests 的主要特点

- **灵活性**：允许基于复杂逻辑和条件动态生成测试用例。
- **可访问性**：可以访问 `metafunc` 对象，提供了关于测试函数的信息，包括函数名、所属类、模块等。
- **适用性**：特别适用于需要从外部数据源（如文件、数据库）读取测试数据的场景。

### 8.11.2.2 使用场景和示例

#### 8.11.2.1 动态参数化

如果你需要根据动态条件或外部数据源来生成测试用例，`pytest_generate_tests` 就非常有用。例如，你可以从文件中读取测试数据，然后生成测试用例。

 `data.json` 文件包含了一些测试数据，比如整数列表和键值对的列表。你可以根据你的测试用例需求来修改这些数据。

```shell
# content of data.json
{
    "integers": [1, 2, 3, 4, 5],
    "key_value_pairs": [
        {"key": "A", "value": "Alpha"},
        {"key": "B", "value": "Beta"},
        {"key": "C", "value": "Gamma"}
    ]
}
```

在 `pytest_generate_tests` 钩子中，你可以读取这个文件来动态生成参数化测试。假设你想要使用这个 JSON 文件中的 `integers` 部分来参数化测试，你可以这样做：

```python
# content of conftest.py
import pytest
import json

def pytest_generate_tests(metafunc):
    if "integer" in metafunc.fixturenames:
        # 从 JSON 文件中读取 "integers" 部分的数据
        with open("data.json", "r") as f:
            data = json.load(f)
            integers = data["integers"]
        # 参数化名为 "integer" 的fixture，提供从文件中读取的整数列表
        metafunc.parametrize("integer", integers)
```

现在，`pytest` 将使用 `data.json` 文件中的整数列表为名为 "integer" 的 fixture 动态生成测试用例。每个整数将作为单独的测试用例执行。如果你的测试函数接收一个名为 "integer" 的参数，那么它将被调用多次，每次都会传入一个不同的整数。

接下来我们需要一个测试用例函数，它将接收从 `data.json` 文件中读取的参数。我们假设测试用例将检查传入的整数是否为正数。

```python
# content of test_case_param_from_json.py
def test_is_positive(integer):
    assert integer > 0, f"Value {integer} is not positive"
```

在这个示例中，`test_is_positive` 函数是我们的测试用例。它接收一个名为 `integer` 的参数，并断言这个参数是一个正数。其运行结果参考如下：

```shell
root@Gavin:~/code/chapter1-8/pytest_generate_tests# pytest -s -v test_case_param_from_json.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'base-url': '2.0.0', 'Faker': '22.0.0', 'allure-pytest': '2.13.2', 'lazy-fixture': '0.6.3', 'freezegun': '0.4.2', 'mock-resources': '2.9.2', 'html': '4.1.1', 'faker': '2.0.0', 'progress': '1.2.5', 'metadata': '3.0.0', 'assume': '2.4.3', 'check': '2.2.3', 'factoryboy': '2.6.0', 'mock': '3.12.0'}, 'JAVA_HOME': '/usr/lib/jre1.8.0_171'}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, base-url-2.0.0, Faker-22.0.0, allure-pytest-2.13.2, lazy-fixture-0.6.3, freezegun-0.4.2, mock-resources-2.9.2, html-4.1.1, faker-2.0.0, progress-1.2.5, metadata-3.0.0, assume-2.4.3, check-2.2.3, factoryboy-2.6.0, mock-3.12.0
collected 5 items

test_case_param_from_json.py::test_is_positive[1] PASSED
test_case_param_from_json.py::test_is_positive[2] PASSED
test_case_param_from_json.py::test_is_positive[3] PASSED
test_case_param_from_json.py::test_is_positive[4] PASSED
test_case_param_from_json.py::test_is_positive[5] PASSED

=============================== 5 passed in 0.07s =============================
root@Gavin:~/code/chapter1-8/pytest_generate_tests#
```

#### 8.11.2.2 根据测试函数定制参数

你还可以根据测试函数的不同来定制参数集，这在不同的测试函数需要不同测试数据时非常有用：

```python
# content of conftest.py
import pytest

def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ == "test_function_1":
        metafunc.parametrize("param", [1, 2, 3])
    elif metafunc.function.__name__ == "test_function_2":
        metafunc.parametrize("param", ["a", "b", "c"])
```

```python
# content of test_customize_param_by_function.py
def test_function_1(param):
    # 对于 test_function_1，param 将是整数 1，2，或 3
    assert isinstance(param, int)
    assert param > 0  # 这里我们简单地测试参数是否是正整数

def test_function_2(param):
    # 对于 test_function_2，param 将是字符串 "a"，"b"，或 "c"
    assert isinstance(param, str)
    assert param in ["a", "b", "c"]  # 测试参数是否是预期的字符串之一
```

在这个例子中，`test_function_1` 测试用例将会遍历整数 1,2,3，每个整数都会进行一次测试，检查它是否为正整数。类似地，`test_function_2` 测试用例将会遍历字符串 "a","b","c"，每个字符串都会进行一次测试，检查它是否在预期的字符串列表中。其运行结果如下：

```shell
root@Gavin:~/code/chapter1-8/pytest_generate_tests# pytest -s -v test_customize_param_by_function.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'cov': '4.1.0', 'base-url': '2.0.0', 'Faker': '22.0.0', 'allure-pytest': '2.13.2', 'lazy-fixture': '0.6.3', 'freezegun': '0.4.2', 'mock-resources': '2.9.2', 'html': '4.1.1', 'faker': '2.0.0', 'progress': '1.2.5', 'metadata': '3.0.0', 'assume': '2.4.3', 'check': '2.2.3', 'factoryboy': '2.6.0', 'mock': '3.12.0'}, 'JAVA_HOME': '/usr/lib/jre1.8.0_171'}
rootdir: /root/code
configfile: pytest.ini
plugins: cov-4.1.0, base-url-2.0.0, Faker-22.0.0, allure-pytest-2.13.2, lazy-fixture-0.6.3, freezegun-0.4.2, mock-resources-2.9.2, html-4.1.1, faker-2.0.0, progress-1.2.5, metadata-3.0.0, assume-2.4.3, check-2.2.3, factoryboy-2.6.0, mock-3.12.0
collected 6 items

test_customize_param_by_function.py::test_function_1[1] PASSED
test_customize_param_by_function.py::test_function_1[2] PASSED
test_customize_param_by_function.py::test_function_1[3] PASSED
test_customize_param_by_function.py::test_function_2[a] PASSED
test_customize_param_by_function.py::test_function_2[b] PASSED
test_customize_param_by_function.py::test_function_2[c] PASSED

=========================== 6 passed in 0.06s ===============================
root@Gavin:~/code/chapter1-8/pytest_generate_tests#
```

#### 8.11.2.3 复杂的逻辑

对于更复杂的参数化逻辑，比如基于一组条件生成不同的参数，`pytest_generate_tests` 也能胜任：

```python
# content of conftest.py
import pytest

# 假设 some_condition 是一个简单的布尔值，可以根据你的测试需求进行修改
some_condition = True  # 或者 some_condition = False

def pytest_generate_tests(metafunc):
    if "param" in metafunc.fixturenames:
        if some_condition:
            values = range(5)
        else:
            values = ["x", "y", "z"]
        metafunc.parametrize("param", values)
```

```python
# content of test_some_condition.py
def test_with_integer(param):
    # 这个测试用例预期 param 为整数
    assert isinstance(param, int)

def test_with_string(param):
    # 这个测试用例预期 param 为字符串
    assert isinstance(param, str)
```

在这个例子中，我们定义了两个测试函数，每个函数都接收 `param` 作为参数。`pytest` 会运行 `pytest_generate_tests` 钩子函数，并根据 `some_condition` 的值为 `param` 参数提供相应的值。如果 `some_condition` 为 `True`，则会执行 `test_with_integer` 五次，每次传入一个不同的整数。如果 `some_condition` 为 `False`，则会执行 `test_with_string` 三次，每次传入一个不同的字符串。其运行效果参考如下：

```shell
collected 10 items

test_some_condition.py::test_with_integer[0] PASSED
test_some_condition.py::test_with_integer[1] PASSED
test_some_condition.py::test_with_integer[2] PASSED
test_some_condition.py::test_with_integer[3] PASSED
test_some_condition.py::test_with_integer[4] PASSED
test_some_condition.py::test_with_string[0] FAILED
test_some_condition.py::test_with_string[1] FAILED
test_some_condition.py::test_with_string[2] FAILED
test_some_condition.py::test_with_string[3] FAILED
test_some_condition.py::test_with_string[4] FAILED
```

# 8.12 优化范本

针对本章节所学知识，我们举个例子加深一下印象，比如有如下一份比较接近实际项目的示例代码，基于webdriver实现web页面的点击功能，示例代码内容如下：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "www.google.com"

def test_click_1():
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.find_element(
        By.XPATH,
        "div[contains(@class, 'item1')]"
    ).click()
    driver.close()


def test_click_2():
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.find_element(
        By.XPATH,
        "div[contains(@class, 'item2')]"
    ).click()
    driver.close()


def test_click_3():
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.find_element(
        By.XPATH,
        "div[contains(@class, 'item3')]"
    ).click()
    driver.close()
```

上述用例，如何借助本章节的知识进行优化？我们先来分析一下这段代码：

从示例用例来看，每个用例中，都有driver的初始化和URL的get动作，以及close()动作；另外就是find_elements要做的事情，除了传递的XPATH元素不一样外，其他动作都一样，所以优化的点有：

- 封装driver初始化与URL的get动作
- 封装close动作
- 优化find_elements，借助`pytest.mark.parametrize`实现参数化

接下来，我们来看一下优化后的效果：

```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "www.google.com"


@pytest.fixture()
def fixture_driver():
    driver = webdriver.Chrome()
    driver.get(URL)
    yield driver
    driver.close()


@pytest.mark.parametrize('item', ['item'+str(x) for x in range(1,4)])
def test_case(fixture_driver, item):
    driver.find_elements(By.XPATH, item).click()
```

借助`fixture`和`@pytest.mark.parametrize`参数化优化后，测试用例更简洁、更契合`pytest`要求。



# 8.13 参数化最佳实践

参数化是`pytest`框架中非常强大和灵活的功能，可以帮助我们简化测试用例的编写和执行。下面是一些`pytest`参数化的最佳实践：

* **明确参数和参数值的含义**：在使用参数化时，确保参数和参数值的命名具有清晰的含义，以便于理解和维护。使用有意义的变量名和注释来描述每个参数和参数值的作用。

* **选择合适的数据结构**：根据测试场景的复杂性，选择合适的数据结构来组织参数和参数值。对于简单的参数，可以使用单个值、列表或元组。对于复杂的参数组合，可以使用嵌套的数据结构，如字典或对象。

* **考虑边界条件**：确保参数化测试覆盖各种可能的边界条件。包括边界值、边界情况和异常情况。这有助于发现潜在的问题和错误，并提高测试的准确性和可靠性。

* **分离测试数据**：将测试数据从测试逻辑中分离出来，可以提高测试的可读性和可维护性。可以将测试数据存储在独立的数据文件中，如CSV文件或Excel表格，并在测试用例中引用这些数据。

* **使用fixture参数化**：可以将fixture和参数化结合使用，以便在测试用例中动态生成和使用参数化数据。这样可以进一步提高测试代码的可重用性和灵活性。

* **使用表格格式的参数化**：对于复杂的参数组合，可以使用表格格式的参数化来定义参数和参数值。这种方式可以更清晰地展示参数组合，方便管理和维护。

* **结合测试标记**：可以结合使用pytest的测试标记功能和参数化来对测试用例进行分类和分组。这样可以更好地组织和管理测试，提高测试代码的可读性和可维护性。

* **慎用过多参数化**：尽量避免过多的参数化，以免造成测试用例的复杂性和混乱。在确定参数化的时候，要权衡测试需求和代码可维护性。

总之，合理使用参数化可以提高测试代码的效率和质量。通过遵循上述最佳实践，我们可以更好地利用参数化功能，使测试用例更易于理解、维护和扩展。



# 8.14 本章小结

在本章中，我们详细介绍了`pytest中`的参数化功能，并展示了如何使用参数化来简化测试用例的编写和执行。参数化是`pytest`框架中一个强大且灵活的功能，它允许我们通过在测试用例中定义参数和参数值的方式，轻松地执行多组相似的测试。

首先，我们了解了参数化的基本概念和用法。通过使用装饰器 `@pytest.mark.parametrize`，我们可以将测试用例标记为参数化，并为测试用例定义一组输入参数和对应的参数值。这样，`pytest`会自动按照参数组合的方式执行测试用例，生成多个独立的测试实例。

其次，我们介绍了参数化的多种用法和特性。我们可以在参数化中使用不同类型的参数，如单个值、列表、元组等。我们还可以使用参数化来组合多个参数，以覆盖更多的测试场景。此外，参数化还支持使用表格或CSV文件来定义参数和参数值，使得我们可以更方便地管理和维护大量的测试数据。

我们还讨论了参数化的最佳实践。我们建议在使用参数化时，根据测试用例的需求和数据的复杂性，合理地组织参数和参数值，以提高测试代码的可读性和可维护性。我们还强调了参数化的边界条件测试的重要性，以确保我们的测试覆盖了各种可能的情况。

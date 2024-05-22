---
title: 《pytest测试指南》-- 章节1-5 pytest断言
date: 2024-05-25 17:00:00
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
summary: 《pytest测试指南》一书 章节1-5 pytest断言，以及pytest-assume和pytest-check插件的一个避坑问题
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 第5章 pytest断言

本章节介绍pytest的断言，以及pytest-assume与pytest-check这两个插件的基本使用与对比，顺带提及了下另外一个测试框架`nose`的断言。

# 5.1 什么是断言

在Python中，断言（Assertion）是一种检查语句，用于验证代码的某个条件一定为真/假。如果条件为真，则程序继续执行；如果条件为假，则抛出一个`AssertionError`异常。断言主要用于调试目的，帮助开发者发现问题和错误。

断言使用`assert`语句，在其后跟上一个条件表达式和可选的错误信息。基本的语法结构如下：

```shell
assert 条件表达式, 错误信息
```

- **条件表达式**：这是你希望在程序的这个点上为真的表达式。如果表达式为假，则会触发异常。
- **错误信息**：可选参数，如果提供，当条件表达式为假时，错误信息将被包含在抛出的`AssertionError`中。

断言经常用于以下场景：

* 检查函数的输入参数是否满足特定条件。
* 确认函数的输出结果符合预期。
* 验证程序运行过程中的某些状态。
* 在运行测试用例时，确认某些条件一定成立。

这里有一个简单的示例演示了断言的使用：

```python
root@Gavin:~/code/chapter1-6# cat test_assert_example.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-


def divide(a, b):
    assert b != 0, "除数不能为0"
    return a / b

# 正常情况
result = divide(10, 2)
print(result)  # 输出 5.0

# 将触发断言错误，因为除数为0
result = divide(10, 0)
root@Gavin:~/code/chapter1-6#
```

当执行第二个`divide`函数调用时，由于除数 `b` 的值为0，违反了断言条件。因此，将引发`AssertionError`，并附带消息"除数不能为0"。



# 5.2 断言的时机

在Python中，断言的使用时机通常是当你需要确认代码在执行特定操作前或后处于预期的状态时。

合理使用断言可以帮助捕捉程序中的逻辑错误，提升代码的可靠性。以下是一些合适使用断言的场景：

* 参数检查：在函数开始处，用来验证输入参数是否满足预期的条件，比如类型检查，值范围检查等。
* 验证函数结果：在函数结束处验证返回值是否合法或处于合理的范围。
* 检查不可能发生的情况：在代码的某个点，你可以确认某条件一定不会发生，使用断言来作为双重检查。
* 测试前提条件：在执行某段关键代码之前，确保所有必须的条件都已经满足。
* 在运行测试用例时：用来确认在测试中某些条件一定为真/假。
* 保证代码不到达某个错误的状态：例如，在循环之后验证某个条件，以确保循环没有以错误的方式终止。
* 对象状态的检查：在类方法中，断言对象属性或状态的有效性。

一个演示示例，参考如下：

```python
root@Gavin:~/code/chapter1-6# cat test_assert_example2.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-


# 参数验证
def sqrt(x):
    assert x >= 0, "x 必须非负"
    return x ** 0.5


# 函数返回值验证
def divide(a, b):
    result = a / b
    assert result * b == a, "结果验证失败"
    return result


def test_sqrt():
    sqrt(10)


def test_divide():
    divide(12, 3)


def test_search_animal():
    # 验证不可能发生的情况
    animals_list = ["狼", "老虎", "熊", "独角兽"]
    zoo = ["大象", "老虎","斑马", "长颈鹿", "熊", "猴子", "大熊猫", "袋鼠", "蛇",
                  "鹦鹉", "鳄鱼", "企鹅", "鸵鸟", "河马", "狮子", "狼"]
    for animal in animals_list:
            assert animal in zoo, "发现了不可能存在的动物"

root@Gavin:~/code/chapter1-6# 
```

使用断言时应考虑以下要点：

- 如果条件失败，`assert`会引发一个`AssertionError`，这表示存在bug或不恰当的数据。
- 不要过度依赖断言来处理程序中可能发生的所有错误情况。当存在可恢复的错误，或需要为用户显示错误信息时，应使用异常处理。
- 别用断言进行常规的数据验证，断言应用于捕捉程序员的错误，而不是用户输入或外部组件错误。



# 5.3 断言分类

在 `pytest` 中，大部分的断言都是用普通的 `assert` 语句完成的。这与标准的 Python 断言用法一致。`pytest` 的一个主要优势是它会在断言失败时提供非常详细的错误信息，这是通过高级的内省机制实现的。分类上来说，断言主要分为以下几类：

## 5.3.1 真值断言

真值断言是用来验证表达式结果是否为真。若结果不为真，则测试会失败。

```python
def test_truth():
    assert True  # 将通过测试
    my_value = 5
    assert my_value  # 由于my_value非零数值，测试将通过
```

如果尝试断言一个明显为假的值，测试会失败：

```python
def test_falsehood():
    assert False  # 将失败
```

## 5.3.2 等值断言
等值断言用来检查两个值是否相等。如果不相等，`pytest`将给出详细的对比结果。

```python
def test_equality():
    number = 10
    assert number == 10  # 通过测试

    text = "pytest"
    assert text == "pytest"  # 通过测试
```

## 5.3.3 不等断言
与等值断言相反，用来检查两个值是否不等。

```python
def test_inequality():
    number = 10
    assert number != 5  # 通过测试
```

## 5.3.4 大于/小于断言
这些断言检查数字之间的大于或小于关系。

```python
def test_greater_less():
    number = 10
    assert number > 5   # 通过测试
    assert number < 15  # 通过测试
```

## 5.3.5 成员断言
成员断言用来检查一个元素是否存在于一个迭代器或集合中。

```python
def test_membership():
    my_list = [1, 2, 3, 4, 5]
    assert 3 in my_list      # 通过测试
    assert 6 not in my_list  # 通过测试
```

## 5.3.6 身份断言
身份断言用来检查两个变量是否指向同一个对象。

```python
def test_identity():
    my_list = [1, 2, 3]
    same_list = my_list
    different_list = my_list.copy()
    assert my_list is same_list           # 通过测试
    assert my_list is not different_list  # 通过测试
```

## 5.3.7 近似值断言
因为浮点数计算可能涉及精度问题而不完全相等，所以近似值断言用来检查两个浮点数是否足够接近。

```python
def test_approx():
    from pytest import approx
    assert 0.1 + 0.2 == approx(0.3)  # 通过测试
```

## 5.3.8 组合断言
在同一个断言语句中，你可以组合多个断言条件。

```python
def test_combined_assertion():
    a = 1
    b = 2
    c = 3
    assert a < b < c  # 通过测试
```

## 5.3.9 异常断言

异常断言用来确保代码块抛出了一种特定类型的异常。

```python
import pytest

def raises_value_error():
    raise ValueError("A value error occurred")

def test_exception():
    with pytest.raises(ValueError) as exc_info:
        raises_value_error()
    assert "value error" in str(exc_info.value).lower()  # 用来检查异常的具体消息
```

在这个测试用例中：

1. 使用 `with pytest.raises(ValueError) as exc_info` 上下文管理器来声明期望的异常类型 (`ValueError`)，以及一个可以存储异常详细信息的变量 (`exc_info`)。
2. 在上下文管理器的代码块内部调用 `raises_value_error` 函数，传入会引发异常的参数。
3. 使用 `assert` 语句来确保 `ValueError` 被抛出，并且异常信息包含了正确的描述。

当运行这个测试用例时，如果 `raises_value_error` 函数按照预期抛出 `ValueError` 异常且异常信息正确，则此测试会通过。如果函数没有抛出异常或者抛出了错误类型的异常，或者异常信息不符合预期，则测试会失败。

## 5.3.10 警示断言

在 `pytest` 中，你可以使用 `pytest.warns` 来测试警告信息。如果你的代码应该触发一个特定的警告，你可以使用这个功能来断言该警告确实被发出了。

例如，让我们考虑这样一个函数，该函数在输入值小于某个阈值时生成警告：

```python
import warnings

def function_with_warning(x):
    if x < 10:
        warnings.warn("x 的值太小，应当大于等于 10", UserWarning)
    return x
```

为了测试这个函数是否在 x 小于 10 时发出警告，可以编写一个如下的测试：

```python
import pytest
from test_assert_warnings_v1 import function_with_warning

def test_function_with_warning():
    with pytest.warns(UserWarning) as record:
        function_with_warning(5)
    
    # 检查是否确实发出了警告
    assert "x 的值太小，应当大于等于 10" in str(record.list[0].message)
```

在这段测试代码中：

1. 使用了 `pytest.warns` 上下文管理器来捕获 `UserWarning` 类型的警告。

2. 在 `with` 块内部调用了 `function_with_warning` 函数，并向其传递了一个小于 10 的值（5）。

3. 使用 `record` 变量，它是一个由所有激活的警告信息组成的列表，通过 `record.list[0].message` 访问第一个警告的信息，并断言它包含了预期的文本。

当这个用例运行时，如果警告正确地被发出并包含了正确的信息，那么测试将会通过。如果函数没有发出警告，或者警告类型不是 `UserWarning`，或者警告消息不符合预期，那么测试将会失败。

## 5.3.11 自定义断言消息

虽然`pytest`在断言失败时提供了详细的信息，但有时你可能想为断言失败提供额外的消息。

```python
def test_custom_message():
    value = "pytest"
    assert value == "python", "value should be 'pytest' but got 'python'"  # 将失败，并显示自定义消息
```



**小结：**

每当一个`assert`语句失败时，`pytest`执行其断言内省机制，展示表达式和相关变量的详细值。这要归功于`pytest`的高级插件系统和重写机制，它允许`assert`语句超越Python内置的断言能力，提供更为人性化的错误报告。



# 5.4 借鉴nose framework断言


一直很喜欢 nose 的 assert（因为编者当初是从nose framework转pytest framework的，使用了nose多年），方法多样，接下来我们看一下 nose 的 assert是如何使用的，以及借鉴过来给 pytest 用。

看了下 nose 的 assert，来自 nose.tools，扫了下 tools 目录下的源码，继承自 unittest，直接porting。

## 5.4.1 nose assert信息

将这部分 code 放在自动化用例公共目录，验证一下效果如何：

```shell
root@Gavin:~/code# pwd
/root/book
root@Gavin:~/code# cd tools/
root@Gavin:~/code/tools# ls -l
total 8
-rw-r--r-- 1 root root  305 Dec  2 02:25 __init__.py
-rw-r--r-- 1 root root 1221 Dec  2 02:25 trivial.py
root@Gavin:~/code/tools#
```

查看一下是否有这些 assert 属性了：

```python
root@Gavin:~/code# python3
Python 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import tools
>>> dir(tools)
['__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'assert_almost_equal', 'assert_almost_equals', 'assert_count_equal', 'assert_dict_contains_subset', 'assert_dict_equal', 'assert_equal', 'assert_equals', 'assert_false', 'assert_greater', 'assert_greater_equal', 'assert_in', 'assert_is', 'assert_is_instance', 'assert_is_none', 'assert_is_not', 'assert_is_not_none', 'assert_less', 'assert_less_equal', 'assert_list_equal', 'assert_logs', 'assert_multi_line_equal', 'assert_no_logs', 'assert_not_almost_equal', 'assert_not_almost_equals', 'assert_not_equal', 'assert_not_equals', 'assert_not_in', 'assert_not_is_instance', 'assert_not_regex', 'assert_not_regexp_matches', 'assert_raises', 'assert_raises_regex', 'assert_raises_regexp', 'assert_regex', 'assert_regexp_matches', 'assert_sequence_equal', 'assert_set_equal', 'assert_true', 'assert_tuple_equal', 'assert_warns', 'assert_warns_regex', 'eq_', 'ok_', 'trivial', 'trivial_all']
>>> 
```

可以看出nose提供的assert更加的丰富，这里简单介绍几个常用的assert示例作参考。

## 5.4.2 nose assert示例

```python
root@Gavin:~/code/chapter1-6# cat test_nose_assert.py 
#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import random

from tools import eq_, assert_greater, assert_greater_equal, assert_less, \
        assert_less_equal, assert_list_equal, assert_in, assert_not_in, \
        assert_true, assert_false, assert_not_equal, assert_sequence_equal, \
        assert_set_equal, ok_


def test_assert_eq():
    "Test case of assert equal, eq_ same as assert_equal"
    str_a = "Test Equal"
    str_b = "Test Equal"
    eq_(str_a, str_b, f"[ERROR] {str_a} is not equal as {str_b}")


def test_assert_not_equal():
    "Test of assert not equal"
    str_a = "This is string a"
    str_b = "This is string b"
    assert_not_equal(str_a, str_b,
                     f"[ERROR]  str_a : {str_a} is not equal as str_b : {str_b}")


def test_assert_greater():
    "Test case of assert greater"
    int_a = 10086
    int_b = 10010
    assert_greater(int_a, int_b, f"[ERROR] {int_a} is not greater than {int_b}")


def test_assert_greater_equal():
    "Test case of assert greater equal"
    random_value = random.randint(30, 100)
    input_value = 30
    error_msg = f"[ERROR]  Input value : ({input_value}) is not larger than " \
                "the random value : ({random_value})"
    assert_greater_equal(random_value, input_value)


def test_assert_less():
    "Test case of assert less"
    random_value1 = random.randint(60, 100)
    random_value2 = random.randint(10, 59)
    error_msg = f"[ERROR]  Input value2 : ({random_value2}) is larger than " \
                "the random value1 : ({random_value1})"
    assert_less(random_value2, random_value1, error_msg)


def test_assert_less_equal():
    "Test case of assert less equal"
    random_value1 = random.randint(29, 100)
    random_value2 = random.randint(10, 30)
    err_msg = f"[ERROR]  Random value2 : ({random_value2}) is >= " \
              "random value1 : ({random_value2})"
    assert_less_equal(random_value2, random_value1)


def test_assert_list_equal():
    "Test case of assert list equal"
    list_a = list(range(10)) 
    list_b = list(range(0, 10))
    assert_list_equal(list_b, list_a,
                      f"[ERROR]  list_b : ({list_b}) is not equal as list_a : ({list_a})")


def test_assert_in():
    "Test case of assert in"
    list_a = list(range(10))
    element_a = 6
    assert_in(element_a, list_a,
              f"[ERROR]  element_a : ({element_a}) is not in list_a : ({list_a})")


def test_assert_not_in():
    "Test case of assert not in"
    list_a = list(range(5, 10))
    element_a = 11
    assert_not_in(element_a, list_a,
                  f"[ERROR]  element_a : ({element_a}) is in list_a : ({list_a})")


def test_assert_true():
    "Test assert true"
    myset = {"apple", "banana", "cherry", False, True, 0}
    assert_true(isinstance(myset, set),
                f"[ERROR]  myset : ({myset}) is not a set")


def test_assert_false():
    "Test case of assert false"
    myset = ("apple", "banana", "cherry", False, True, 0)
    assert_false(isinstance(myset, list),
                 f"[ERROR]  myset : ({myset}) is not a list, but a set")


def test_assert_sequence_equal():
    "Test case of assert sequence equal" 
    list_a = list(range(10))
    list_b = list(range(10))
    assert_sequence_equal(list_a, list_b,
                          f"[ERROR]  list_a : (list_a) is not sequence equal " \
                          f"as list_b : ({list_b})")


def test_assert_set_equal():
    "Test case of assert set equal"
    set_a = set(list(range(10, 0, -1)))
    set_b = set(list(range(10, 0, -1)))
    assert_set_equal(set_a, set_b,
                     f"[ERROR]  set_a : ({set_a}) is not equal as set_b : ({set_b})")

def test_ok():
    "Test case of ok_"
    str_a = "123"
    str_b = "1234567890"
    str_c = "1234554321"
    ok_(str_a in str_b, f"[ERROR]  str_a : ({str_a}) is not in str_b : ({str_c})")
    ok_(str_b not in str_c, f"[ERROR]  str_b : ({str_a}) is not in str_c : ({str_c})")
root@Gavin:~/code/chapter1-6#
```

执行效果如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -sv -p no:warnings test_nose_assert.py
================================ test session starts ==========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'assume': '2.4.3'}}
rootdir: /root/code/chapter1-6
plugins: check-2.2.2, metadata-3.0.0, assume-2.4.3
collected 14 items

test_nose_assert.py::test_assert_eq PASSED
test_nose_assert.py::test_assert_not_equal PASSED
test_nose_assert.py::test_assert_greater PASSED
test_nose_assert.py::test_assert_greater_equal PASSED
test_nose_assert.py::test_assert_less PASSED
test_nose_assert.py::test_assert_less_equal PASSED
test_nose_assert.py::test_assert_list_equal PASSED
test_nose_assert.py::test_assert_in PASSED
test_nose_assert.py::test_assert_not_in PASSED
test_nose_assert.py::test_assert_true PASSED
test_nose_assert.py::test_assert_false PASSED
test_nose_assert.py::test_assert_sequence_equal PASSED
test_nose_assert.py::test_assert_set_equal PASSED
test_nose_assert.py::test_ok PASSED

================================ 14 passed in 0.01s ===========================
root@Gavin:~/code/chapter1-6#
```



# 5.5 多重校验插件之pytest-assume

在写`pytest`用例的时候，可以在用例检查点中增加断言，也可以写多个断言，但任意一个失败，后续的断言将不再执行，如下文示例所示：

```python
root@Gavin:~/code/chapter1-6# cat test_multi_assert.py 
#!/usr/bin/env python3
# -*- coding:UTF-8 -*-


list_a = list(range(10))

def test_assert_feature():
    assert len(list_a) == 10, f"[ERROR]  list_a has no ten elements"
    assert '7' in list_a, f"[ERROR]  String of '7' is not in list_a : ({list_a})"
    assert isinstance(list_a, list), f"[ERROR]  list_a : ({list_a}) is not a list"
root@Gavin:~/code/chapter1-6#
```

执行结果：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v test_multi_assert.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'metadata': '3.0.0'}}
rootdir: /root/code
configfile: pytest.ini
collected 1 item

test_multi_assert.py::test_assert_feature FAILED

============================== FAILURES ======================================
______________________________ test_assert_feature ___________________________

    def test_assert_feature():
        assert len(list_a) == 10, f"[ERROR]  list_a has no ten elements"
>       assert '7' in list_a, f"[ERROR]  String of '7' is not in list_a : ({list_a})"
E       AssertionError: [ERROR]  String of '7' is not in list_a : ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
E       assert '7' in [0, 1, 2, 3, 4, 5, ...]

test_multi_assert.py:9: AssertionError

1 assertions tested.
============================= short test summary info =========================
FAILED test_multi_assert.py::test_assert_feature - AssertionError: [ERROR]  String of '7' is not in list_a : ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
============================= 1 failed in 0.04s ===============================
root@Gavin:~/code/chapter1-6#
```

这里，第一个断言通过后，第二个断言失败了，后面的第三个断言没有被执行到。

接下来我们介绍一个多重校验插件 -- `pytest-assume`，其特点是如果运行断言失败，不会停止运行，会继续执行这个断言下的其他语句或断言，不会影响后续代码的运行。

说明：

pytest-assume 源码链接为: ``` https://github.com/astraw38/pytest-assume ```，透过此链接，可以查阅官网上提供的测试示例。



## 5.5.1 安装pytest-assume

透过pip install安装时，报错：

```shell
root@Gavin:~# pip install pytest-assume
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.
    
    See /usr/share/doc/python3.11/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

将 ``` /usr/lib/python3.11/EXTERNALLY-MANAGED```文件删除后，重新使用pip进行安装：

```shell
root@Gavin:~# ls -l /usr/lib/python3.11/EXTERNALLY-MANAGED
-rw-r--r-- 1 root root 645 Oct  8 05:06 /usr/lib/python3.11/EXTERNALLY-MANAGED
root@Gavin:~# cd /usr/lib/python3.11/
root@Gavin:/usr/lib/python3.11# mv EXTERNALLY-MANAGED /root/
root@Gavin:/usr/lib/python3.11# cd
root@Gavin:~# pip install pytest-assume
Collecting pytest-assume
  Downloading pytest_assume-2.4.3-py3-none-any.whl (6.0 kB)
Requirement already satisfied: pytest>=2.7 in /usr/lib/python3/dist-packages (from pytest-assume) (7.4.0)
Requirement already satisfied: six in /usr/lib/python3/dist-packages (from pytest-assume) (1.16.0)
Requirement already satisfied: iniconfig in /usr/lib/python3/dist-packages (from pytest>=2.7->pytest-assume) (1.1.1)
Requirement already satisfied: packaging in /usr/lib/python3/dist-packages (from pytest>=2.7->pytest-assume) (23.1)
Requirement already satisfied: pluggy<2.0,>=0.12 in /usr/lib/python3/dist-packages (from pytest>=2.7->pytest-assume) (1.2.0)
Installing collected packages: pytest-assume
Successfully installed pytest-assume-2.4.3
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
root@Gavin:~#
```

透过pip list 或者 pip freeze，检查assume安装是否成功：

```shell
root@Gavin:~# pip list | grep assume
pytest-assume          2.4.3
root@Gavin:~# pip freeze | grep assume
pytest-assume==2.4.3
root@Gavin:~# 
```



## 5.5.2 解决无法import assume问题

在引入assume时，碰到如下错误：

```shell
root@Gavin:~# python3
Python 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pytest import assume
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: cannot import name 'assume' from 'pytest' (/usr/lib/python3/dist-packages/pytest/__init__.py)
>>> 
```

解决方法：

排查过程中发现，assume存放在pytest_assume的plugin.py中：

```shell
root@Gavin:/usr/local/lib/python3.11/dist-packages/pytest_assume# ll
total 28
drwxr-xr-x 3 root root 4096 Dec  2 08:15 ./
drwxr-xr-x 4 root root 4096 Dec  2 08:15 ../
-rw-r--r-- 1 root root  853 Dec  2 08:15 hooks.py
-rw-r--r-- 1 root root   18 Dec  2 08:15 __init__.py
-rw-r--r-- 1 root root 8080 Dec  2 08:15 plugin.py
drwxr-xr-x 2 root root 4096 Dec  2 08:15 __pycache__/
root@Gavin:/usr/local/lib/python3.11/dist-packages/pytest_assume# vim plugin.py 
root@Gavin:/usr/local/lib/python3.11/dist-packages/pytest_assume# 
```

如下 import 是OK的：

```python
from pytest_assume.plugin import assume
```

修改```/usr/lib/python3/dist-packages/pytest/__init__.py```文件，有一处需要调整，如下：

在文件顶部`import`地方，增加``` from pytest_assume.plugin import assume```， 参考如下：

```python
from _pytest.warning_types import PytestWarning  # 旧有的
from pytest_assume.plugin import assume          # 本次新增的
```

验证下修改效果：

```python
root@Gavin:~# python3
Python 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pytest import assume
>>> 
```



## 5.5.3 使用pytest-assume

###  5.5.3.1 `assume()` 函数

示例：

```python
# content of ~/code/chapter1-6/test_assume.py
#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

from pytest import assume


list_a = list(range(10))

def test_assert_feature():
    assume(len(list_a) == 10)
    assume('7' in list_a)
    assume(isinstance(list_a, list))
    print("End of test.")
root@Gavin:~/code# 
```

执行效果：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v -p no:warnings test_assume.py 
============================ test session starts ==============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'metadata': '3.0.0', 'assume': '2.4.3'}}
rootdir: /root/code
configfile: pytest.ini
plugins: assume-2.4.3
collected 1 item

test_assume.py::test_assert_feature End of test.
FAILED
============================= FAILURES ========================================
_____________________________ test_assert_feature _____________________________

tp = <class 'pytest_assume.plugin.FailedAssumption'>, value = None, tb = None

    def reraise(tp, value, tb=None):
        try:
            if value is None:
                value = tp()
            if value.__traceback__ is not tb:
>               raise value.with_traceback(tb)
E               pytest_assume.plugin.FailedAssumption: 
E               1 Failed Assumptions:
E               
E               test_assume.py:12: AssumptionFailure
E               >>	assume('7' in list_a)
E               AssertionError:

/usr/lib/python3/dist-packages/six.py:718: FailedAssumption
============================= short test summary info =========================
FAILED test_assume.py::test_assert_feature - pytest_assume.plugin.FailedAssumption: 
============================= 1 failed, 1 warning in 0.05s ====================
root@Gavin:~/code/chapter1-6#
```

从上述内容可以看出，最终打印了内容"End of test."，说明中间断言失败后，后续代码有被执行到。



### 5.5.3.2 上下文管理器

pytest.assume 也可以用于普通断言的上下文管理器。

```python
root@Gavin:~/code/chapter1-6# cat test_with_assume_v1.py 
#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import pytest
from pytest import assume


@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0)])
def test_simple_assume(x, y):
    with assume: assert x == y
    with assume: assert True
    with assume: assert False
    print("End of test_simple_assume.")
root@Gavin:~/code/chapter1-6#
```

执行效果如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -rsv -p no:warnings test_with_assume_v1.py 
============================ test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
configfile: pytest.ini
plugins: metadata-3.0.0, assume-2.4.3
collected 2 items

test_with_assume_v1.py FF                                               [100%]

============================= FAILURES =======================================
_____________________________ test_simple_assume[1-1] ________________________

x = 1, y = 1

    @pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0)])
    def test_simple_assume(x, y):
        with assume: assert x == y
        with assume: assert True
>       with assume: assert False
E       pytest_assume.plugin.FailedAssumption: 
E       1 Failed Assumptions:
E       
E       test_with_assume_v1.py:12: AssumptionFailure
E       >>	with assume: assert False
E       AssertionError: assert False

test_with_assume_v1.py:12: FailedAssumption
---------------------------- Captured stdout call ----------------------------
End of test_simple_assume.
____________________________ test_simple_assume[1-0] _________________________

x = 1, y = 0

    @pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0)])
    def test_simple_assume(x, y):
        with assume: assert x == y
        with assume: assert True
>       with assume: assert False
E       pytest_assume.plugin.FailedAssumption: 
E       2 Failed Assumptions:
E       
E       test_with_assume_v1.py:10: AssumptionFailure
E       >>	with assume: assert x == y
E       AssertionError: assert 1 == 0
E       
E       test_with_assume_v1.py:12: AssumptionFailure
E       >>	with assume: assert False
E       AssertionError: assert False

test_with_assume_v1.py:12: FailedAssumption
--------------------------- Captured stdout call -----------------------------
End of test_simple_assume.
============================ 2 failed, 1 warning in 0.04s ====================
root@Gavin:~/code/chapter1-6#
```

上述示例代码``` test_with_assume_v1.py``` 能否将所有断言写在一个上下文管理器中呢？我们试一下：

```python
root@Gavin:~/code/chapter1-6# cat test_with_assume_v2.py 
#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import pytest
from pytest import assume


@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0)])
def test_simple_assume(x, y):
    with assume:
        assert x == y
        print("End of assert x == y")
        assert True
        print("End of assert True")
        assert False
        print("End of assert False")

    print("End of test_simple_assume")
root@Gavin:~/code#
```

执行效果如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -rsv -p no:warnings test_with_assume_v2.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
configfile: pytest.ini
plugins: metadata-3.0.0, assume-2.4.3
collected 2 items

test_with_assume_v2.py FF                                                [100%]

============================ FAILURES ========================================
____________________________ test_simple_assume[1-1] _________________________

x = 1, y = 1

    @pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0)])
    def test_simple_assume(x, y):
        with assume:
            assert x == y
            print("End of assert x == y")
            assert True
            print("End of assert True")
>           assert False
E           pytest_assume.plugin.FailedAssumption: 
E           1 Failed Assumptions:
E           
E           test_with_assume_v2.py:10: AssumptionFailure
E           >>	with assume:
E           AssertionError: assert False

test_with_assume_v2.py:15: FailedAssumption
---------------------------- Captured stdout call ----------------------------
End of assert x == y
End of assert True
End of test_simple_assume
____________________________ test_simple_assume[1-0] _________________________

x = 1, y = 0

    @pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0)])
    def test_simple_assume(x, y):
        with assume:
>           assert x == y
E           pytest_assume.plugin.FailedAssumption: 
E           1 Failed Assumptions:
E           
E           test_with_assume_v2.py:10: AssumptionFailure
E           >>	with assume:
E           AssertionError: assert 1 == 0

test_with_assume_v2.py:11: FailedAssumption
--------------------------- Captured stdout call -----------------------------
End of test_simple_assume
============================ 2 failed, 1 warning in 0.04s ====================
root@Gavin:~/code/chapter1-6#
```

执行过程显示，当参数化传递x，y为(1,1)时，assert x == y 成功，后续的assert True 和 assert False也顺利被执行到了；但当参数化传递x，y为(1,0)时，assert x == y 失败了，后续的assert True 和 assert False并没有被执行到。所以，**每个```with assume```块只能有一个断言，如果第一个断言失败，就不能完全验证余下断言了**。这点请注意！



## 5.5.4 pytest-assume teardown的坑

希望在teardown阶段能够产生最终失败的结果，但是不要影响teardown中所有步骤的执行，于是想到了pytest-assume，然而验证的结果出乎意料。

```python
# content of test_pytest_assume_teardown.py
import pytest


class Test_Example():
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    def test_case(self):
        pass
```

执行结果是通过，与预期相符:

```shell
root@Gavin:~/code/chapter1-6# pytest -s -p no:warnings test_pytest_assume_teardown.py
================================ test session starts ==========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
plugins: assume-2.4.3
collected 1 item

test_pytest_assume_teardown.py .

================================= 1 passed in 0.00s ============================
root@Gavin:~/code/chapter1-6#
```

### 5.5.4.1 在setup使用assume

修改测试代码，在setup中加入assume：

```python
import pytest


class Test_Example():
    def setup_method(self):
        print("Setup method with pytest.assume, assert false.")
        pytest.assume(False)

    def teardown_method(self):
        pass

    def test_case(self):
        pass

```

执行结果应该失败，与预期相符：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -p no:warnings test_pytest_assume_teardown.py
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
plugins: assume-2.4.3
collected 1 item

test_pytest_assume_teardown.py Setup method with pytest.assume, assert false.
F

============================== FAILURES ======================================
______________________________ Test_Example.test_case ________________________

tp = <class 'pytest_assume.plugin.FailedAssumption'>, value = None, tb = None

    def reraise(tp, value, tb=None):
        try:
            if value is None:
                value = tp()
            if value.__traceback__ is not tb:
>               raise value.with_traceback(tb)
E               pytest_assume.plugin.FailedAssumption: 
E               1 Failed Assumptions:
E               
E               test_pytest_assume_teardown.py:22: AssumptionFailure
E               >>	pytest.assume(False)
E               AssertionError:

/usr/lib/python3/dist-packages/six.py:718: FailedAssumption
============================== short test summary info ========================
FAILED test_pytest_assume_teardown.py::Test_Example::test_case - pytest_assume.plugin.FailedAssumption: 
============================== 1 failed in 0.04s ==============================
root@Gavin:~/code/chapter1-6#
```

### 5.5.4.2 在teardown使用assune

修改测试代码，在`teardown`中加入`assume`：

```python
class Test_Example():
    def setup_method(self):
        pass

    def teardown_method(self):
        print("Use pytest.assume(False) in teardown")
        pytest.assume(False)

    def test_case(self):
        pass
```

预期执行结果是失败，实际执行结果是成功：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -v -p no:warnings test_pytest_assume_teardown.py
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'assume': '2.4.3'}}
rootdir: /root/code
plugins: assume-2.4.3
collected 1 item

test_pytest_assume_teardown.py::Test_Example::test_case PASSEDUse pytest.assume(False) in teardown

=============================== 1 passed in 0.01s =============================
root@Gavin:~/code/chapter1-6#
```

### 5.5.4.3 改用pytest.fail

再次修改测试代码，使用`pytest.fail`代替`pytest.assume`：

```python
class Test_Example():
    def setup_method(self):
        pass

    def teardown_method(self):
        print("Use pytest.fail in teardown")
        pytest.fail()

    def test_case(self):
        pass
```

执行结果是失败，与预期相符：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -p no:warnings test_pytest_assume_teardown.py
============================== test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-6
plugins: metadata-3.0.0, assume-2.4.3
collected 1 item

test_pytest_assume_teardown.py .Use pytest.fail in teardown
E

============================== ERRORS =========================================
______________________ ERROR at teardown of Test_Example.test_case ____________

self = <test_pytest_assume_teardown.Test_Example object at 0x7efcc395b710>

    def teardown_method(self):
        print("Use pytest.fail in teardown")
>       pytest.fail()
E       Failed

test_pytest_assume_teardown.py:49: Failed
============================== short test summary info =========================
ERROR test_pytest_assume_teardown.py::Test_Example::test_case - Failed
============================== 1 passed, 1 error in 0.03s ======================
root@Gavin:~/code/chapter1-6#
```

**小结：**

对于`pytest.assume`，放在teardown里面是不会触发最后显示测试用例结果为失败状态的，这点请牢记！



对于此次碰到的状况，有没有解决方法？答案是肯定的，改用`pytest-check`这个插件。接下来，我们讲解一下`pytest-check`这个插件。



# 5.6 多重校验插件之pytest-check

`pytest-check` 插件通过增加新的命令而不是原生的 `assert`，它允许在同一个测试函数中执行多个断言，即使其中一些断言失败了，测试也会继续执行直到结束，最后一起报告所有的失败。这使得它非常适合于执行和报告多个步骤或条件的测试，而不是在第一个失败的地方就停止。这点和`pytest-assume`插件的功能非常相似。

这是`pytest`原生`assert`和`pytest-check`之间的一个主要区别，在原生`assert`中，如果断言失败，测试立即停止，后续的断言不会被执行。

## 5.6.1 安装pytest-check

`pytest-check`可以通过`pip`安装：

```shell
pip install pytest-check
```

## 5.6.2 使用pytest-check

一旦安装了`pytest-check`，你可以在测试代码中导入`pytest_check`模块，并使用它提供的多个检查（check）函数来代替普通的`assert`语句。下面是`pytest-check`支持的一些检查函数：

- `check.equal(a, b)` - 检查`a`是否等于`b`
- `check.not_equal(a, b)` - 检查`a`是否不等于`b`
- `check.is_true(x)` - 检查`x`是否为真
- `check.is_false(x)` - 检查`x`是否为假
- `check.is_in(a, b)` - 检查`a`是否在`b`中
- `check.is_not_in(a, b)` - 检查`a`是否不在`b`中
- `check.is_none(x)` - 检查`x`是否为`None`
- `check.is_not_none(x)` - 检查`x`是否不是`None`
- `check.greater(a, b)` - 检查`a`是否大于`b`
- `check.less(a, b)` - 检查`a`是否小于`b`
- ...还有更多，不再一一举例。

完整的函数名称参考如下：

```shell
root@Gavin:~/code# python3
Python 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pytest_check as check 
>>> dir(check)
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'almost_equal', 'any_failures', 'assert_equal', 'between', 'check', 'check_func', 'check_functions', 'check_log', 'check_raises', 'context_manager', 'equal', 'func', 'greater', 'greater_equal', 'is_', 'is_false', 'is_in', 'is_instance', 'is_none', 'is_not', 'is_not_in', 'is_not_instance', 'is_not_none', 'is_true', 'less', 'less_equal', 'not_almost_equal', 'not_equal', 'pseudo_traceback', 'pytest', 'raises']
```

## 5.6.3 示例

下面是一个使用`pytest-check`插件的简单示例，它包括了几种不同类型的检查（checks）：

```python
import pytest_check as check


def fake_add(a, b):
# 这个函数故意写错，为了使测试失败
    return a * b


def test_with_check():
    # 等值检查
    result = fake_add(2, 5)

    # 检查结果是否为预期的10
    check.equal(result, 10, "The result should be addition but got multiplication")

    # 大于检查
    check.greater(result, 7, f"The result should be greater than 7 but was {result}")

    # 真值检查
    check.is_true(result == 10, "Result should be true when comparing result to 10")

    # 成员检查
    fruits = ['apple', 'banana', 'cherry']
    check.is_in('banana', fruits, "Fruits list should contain 'banana'")

    # 浮点检查
    # 因为浮点数计算可能有精度问题所以比较时使用check.almost_equal
    check.almost_equal(0.1 + 0.2, 0.3, rel=None, abs=1e-9, msg="Check if two floats are almost equal")
```

现在，尽管 `fake_add` 函数返回的结果不是两个数字的加和，导致第一个检查失败，但是后面的检查还会继续执行。这意味着，测试最后将报告第一个检查失败的情况，而不是像使用`assert`语句那样立即停止。

执行上述测试代码后，`pytest`还会输出失败的检查信息。这可以帮助你更快地定位和理解测试失败的原因，特别是在测试包含很多检查的情况下，这个特性非常有帮助。

```python
import pytest_check as check

def test_multiple_checks():
    check.equal(1, 1)  # 成功
    check.greater(5, 1)  # 成功
    check.less(2, 1)  # 失败
    check.is_in(3, [1, 2, 3])  # 成功
    check.is_not_in(4, [1, 2, 3])  # 成功
    check.is_none(None)  # 成功
    check.is_not_none(1)  # 成功
```

在上面这个示例中，即使`check.less(2, 1)`会失败，其他的检查也会执行，并且所有失败的检查会在测试结束后一起被报告。输出结果参考如下：

```shell
root@Gavin:~/code/chapter1-6# pytest -sv -p no:warnings test_pytest_check_sample.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-14-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '7.4.0', 'pluggy': '1.2.0'}, 'Plugins': {'check': '2.2.2', 'metadata': '3.0.0', 'assume': '2.4.3'}}
rootdir: /root/code/chapter1-6
plugins: check-2.2.2, metadata-3.0.0, assume-2.4.3
collected 2 items

test_pytest_check_sample.py::test_with_check PASSED
test_pytest_check_sample.py::test_multiple_checks FAILED

============================== FAILURES =======================================
______________________________ test_multiple_checks ___________________________
FAILURE: check 2 < 1
test_pytest_check_sample.py:37 in test_multiple_checks() -> check.less(2, 1)

------------------------------------------------------------
Failed Checks: 1
============================== short test summary info ========================
FAILED test_pytest_check_sample.py::test_multiple_checks
============================== 1 failed, 1 passed in 0.01s ====================
root@Gavin:~/code/chapter1-6#
```

## 5.6.4 小结

使用`pytest-check`能提高测试效率，尤其是在测试需验证多个数据点或当你希望一次性收集所有相关测试失败信息而不是一次只能看到一个异常时。这对于测试具有大量验证点的复杂系统尤其有用，可以确保你获取尽可能多的错误反馈，从而进行更有效的调试。它有如下特点：

- 支持"软断言"或"非阻塞断言"，这些断言不会在失败时停止测试函数。
- 输出明确的错误消息，指出哪一个检查（check）失败，以及为何失败。
- 当没有断言异常时，与平常的`pytest`断言相比没有额外的运行时间开销。
- 兼容`pytest`的丰富插件生态系统。



# 5.7 pytest-check解决pytest-assume teardown的坑

回到本文中介绍`pytest-assume`时碰到的在`pytest-assume teardown的坑`，这里借助`pytest-check`解决之，代码示例如下:

```python
# content of test_pytest_check_teardown.py
import pytest_check as check


class Test_Example():
    def setup_method(self):
        pass

    def teardown_method(self):
        print("Use check.is_true in teardown")
        check.is_true(False)

    def test_case(self):
        pass
```

执行结果失败，符合预期：

```shell
root@Gavin:~/code/chapter1-6# pytest -s -p no:warnings test_pytest_check_teardown.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-6
plugins: check-2.2.2, assume-2.4.3
collected 1 item

test_pytest_check_teardown.py .Use check.is_true in teardown
E

============================== ERRORS ========================================
________________________ ERROR at teardown of Test_Example.test_case _________
FAILURE: check bool(False)
runner.py:182 in pytest_runtest_teardown() -> item.session._setupstate.teardown_exact(nextitem)
runner.py:526 in teardown_exact() -> fin()
fixtures.py:701 in <lambda>() -> subrequest.node.addfinalizer(lambda: fixturedef.finish(request=subrequest))
fixtures.py:1024 in finish() -> func()
fixtures.py:911 in _teardown_yield_fixture() -> next(it)
python.py:907 in xunit_setup_method_fixture() -> _call_with_optional_argument(func, method)
python.py:776 in _call_with_optional_argument() -> func()
test_pytest_check_teardown.py:14 in teardown_method() -> check.is_true(False)

------------------------------------------------------------
Failed Checks: 1
============================== short test summary info =======================
ERROR test_pytest_check_teardown.py::Test_Example::test_case
============================== 1 passed, 1 error in 0.01s ====================
root@Gavin:~/code/chapter1-6#
```

可见`pytest-check`对比`pytest-assume`的一个优势为：

- 可以克服在`teardown`阶段调用无法触发`case fail`的缺陷




# 5.8 pytest-assume与pytest-check区别

`pytest-assume` 和 `pytest-check` 都是 `pytest` 插件，旨在改善在单个测试中进行多个断言的体验。它们都允许测试在一个断言失败后继续执行，但是在实现方式和一些细节上有所不同。

以下是 `pytest-assume` 和 `pytest-check` 在使用方式和功能上的主要区别：

## 5.8.1 使用方式

- `pytest-assume` 提供了一个 `assume()` 函数和一个上下文管理器，都可以用来包装断言。如果断言失败，测试不会停止；在上下文管理器的块末尾或在测试函数的末尾，所有失败的断言都会被报告。
- `pytest-check` 提供了一系列函数来代替标准 `assert` 断言，例如 `check.equal()`, `check.is_true()`, `check.is_in()` 等，它们在失败时不会停止测试。这些函数可以在测试中随处使用，无需上下文管理器。

## 5.8.2 语法风格

- `pytest-assume` 使得你可以继续使用标准的 `assert` 语句，因为它们被包裹在 `with pytest.assume:` 块或 `pytest.assume()` 函数调用中。这种方式对于习惯了 `assert` 语法的 `pytest` 用户来说是很自然的。
- `pytest-check` 则需要你使用特定的函数调用，这意味着你必须将常规的 `assert` 断言变更为对应的 `check` 函数调用，这可能需要一些时间适应这种新的语法。

## 5.8.3 错误报告

- `pytest-assume` 在测试的末尾会汇总所有失败的断言，并且可以直接指示哪个断言失败了，因为它使用的是普通的 `assert` 语句。
- `pytest-check` 同样在测试的末尾会汇总所有失败的断言。由于它使用的是特殊的检查函数，因此失败报告可能在格式上略有差异，但同样会提供详细的失败信息。

## 5.8.4 内部实现

- `pytest-assume` 使用了 pytest 钩子和一个内部列表来跟踪每个测试中的失败断言。
- `pytest-check` 利用其自定义的检查函数来捕获并记录失败信息。

## 5.8.5 选择如何使用

选择哪个插件主要取决于个人偏好和具体需求。如果你喜欢使用标准的 `assert` 语句和希望在失败时继续，`pytest-assume` 是一个好的选择。如果你更倾向于有一个专用的断言库，并且不介意改变你的断言风格，`pytest-check` 或者nose framework的断言方式可能更适合你。

另外，还有可能是具体项目的需求或团队内部的偏好，这些因素都可能影响你选择哪个插件。在某些情况下，你甚至可以在同一个项目中同时使用这两个插件，根据不同的测试场景选择不同的工具。



# 5.9 assert优劣对比

让我们来看一下Python的`assert`语句以及`pytest`插件`pytest-assume`和`pytest-check`的优劣势比较：

| 断言方式      | 优势                                                         | 劣势                                                         |
| ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| assert        | **内置语法**：不需要安装额外库，是Python语言的一部分。 <br />**简单直观**：语法简单，直接用于断言测试条件。 <br />**立即反馈**：一旦断言失败，立即停止当前测试，可以快速发现问题所在。 | **断言失败即停止**：一个断言失败，后面的代码不会执行，可能会遗漏其他潜在的错误。 <br />**测试覆盖不全**：由于断言失败导致测试停止，无法完整覆盖测试案例。 <br />**不利于批量检查**：不能在单个测试用例中进行多项断言检查。 |
| pytest-assume | **允许多重断言**：测试不会因为一个断言失败而停止，所有的断言都会被执行。 <br />**详尽的错误报告**：提供执行所有断言后统一的错误报告，便于一次性查看所有问题 | **需要安装插件**：需要额外安装扩展包。 <br />**语法变化**：与内置的`assert`语法略有不同，需要学习和适应。 <br />**可能的依赖问题**：作为第三方插件，可能会存在版本依赖和兼容性问题。 |
| pytest-check  | **灵活的检查（check）机制**：可进行多个断言而不会停止测试，所有的断言都会被执行。<br />**聚合的错误报告**：在测试完成后提供所有失败检查的报告。 <br />**与pytest兼容**：无缝集成到现有的`pytest`框架中。 | **需要安装插件**：与`pytest-assume`类似，也需要安装额外的插件。 <br />**语法学习**：需要学习新的检查方法，如`check.equal()`, `check.greater()`等。 <br />**潜在的过度使用**：如果滥用，可能导致单个测试函数尝试测试太多的情况，而减低测试的可读性和可维护性。 |

以上总结了`assert`，`pytest-assume`和`pytest-check`的各自优劣，但具体使用哪个工具或方法，取决于测试场景和开发者的个人偏好。常见的做法是根据需要来选择适合的工具，如在简单的测试中使用`assert`，在需要多重验证时使用`pytest-assume`或`pytest-check`。至于nose framework中的断言，和`pytest-check`断言功能类似，但缺少断言出错继续后续断言执行功能。



# 5.10 本章小结

本章节主要介绍了`pytest`测试框架中的断言功能，包括借鉴`nose`断言、插件`pytest-assume`和插件`pytest-check`。我们详细介绍了这些断言库的安装、使用方法以及相关示例。

通过本章节的学习，我们了解到`pytest`断言库是进行测试过程中重要的工具，它可以用于测试结果的验证，提高测试过程的准确性和效率。`nose`断言库提供了一种基本的断言成功和失败返回信息，通过特定的参数或消息提示进行错误解决和问题跟踪。`pytest-assume`库可以在`pytest`测试框架中使用，帮助我们进行多重前提和断言，以便更好地控制测试过程和结果。`pytest-check`库则是一个实用的`pytest`插件，可以帮助我们进行多重前提和断言的组合和管理。

需要注意的是，对于不同的测试需求和场景，我们需要根据实际情况灵活使用不同的断言库。我们还需要了解断言的基本语法和任务，并对特定断言库的参数和底层逻辑进行深入学习。

此外，我们还需要不断学习掌握更多的断言技巧和方法，以便更好地优化测试过程和测试结果，最终提高代码的质量和可靠性。

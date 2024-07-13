---
title: pytest-assume teardown的坑
date: 2024-12-15 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-26.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest-assume teardown的坑，使用pytest-check规避
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

本文介绍`pytest-assume`使用过程中碰到的坑，并借助`pytest-check`进行规避。


# pytest-assume teardown的坑

希望在`teardown`阶段能够产生最终失败的结果，但是不要影响`teardown`中所有步骤的执行，于是想到了`pytest-assume`，然而验证的结果出乎意料。

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

## 在setup使用assume

修改测试代码，在`setup`中加入`assume`：

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

## 在teardown使用assune

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

## 改用pytest.fail

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

**注意：**

对于`pytest.assume`，放在`teardown`里面是不会触发最后显示测试用例结果为失败状态的，这点请牢记！


# pytest-check解决pytest-assume teardown的坑

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




# pytest-assume与pytest-check区别

`pytest-assume` 和 `pytest-check` 都是 `pytest` 插件，旨在改善在单个测试中进行多个断言的体验。它们都允许测试在一个断言失败后继续执行，但是在实现方式和一些细节上有所不同。

以下是 `pytest-assume` 和 `pytest-check` 在使用方式和功能上的主要区别：

## 使用方式

- `pytest-assume` 提供了一个 `assume()` 函数和一个上下文管理器，都可以用来包装断言。如果断言失败，测试不会停止；在上下文管理器的块末尾或在测试函数的末尾，所有失败的断言都会被报告。
- `pytest-check` 提供了一系列函数来代替标准 `assert` 断言，例如 `check.equal()`, `check.is_true()`, `check.is_in()` 等，它们在失败时不会停止测试。这些函数可以在测试中随处使用，无需上下文管理器。

## 语法风格

- `pytest-assume` 使得你可以继续使用标准的 `assert` 语句，因为它们被包裹在 `with pytest.assume:` 块或 `pytest.assume()` 函数调用中。这种方式对于习惯了 `assert` 语法的 `pytest` 用户来说是很自然的。
- `pytest-check` 则需要你使用特定的函数调用，这意味着你必须将常规的 `assert` 断言变更为对应的 `check` 函数调用，这可能需要一些时间适应这种新的语法。

## 错误报告

- `pytest-assume` 在测试的末尾会汇总所有失败的断言，并且可以直接指示哪个断言失败了，因为它使用的是普通的 `assert` 语句。
- `pytest-check` 同样在测试的末尾会汇总所有失败的断言。由于它使用的是特殊的检查函数，因此失败报告可能在格式上略有差异，但同样会提供详细的失败信息。

## 内部实现

- `pytest-assume` 使用了 `pytest` 钩子和一个内部列表来跟踪每个测试中的失败断言。
- `pytest-check` 利用其自定义的检查函数来捕获并记录失败信息。

## 选择如何使用

选择哪个插件主要取决于个人偏好和具体需求。如果你喜欢使用标准的 `assert` 语句和希望在失败时继续，`pytest-assume` 是一个好的选择。如果你更倾向于有一个专用的断言库，并且不介意改变你的断言风格，`pytest-check` 或者 `nose framework` 的断言方式可能更适合你。

另外，还有可能是具体项目的需求或团队内部的偏好，这些因素都可能影响你选择哪个插件。在某些情况下，你甚至可以在同一个项目中同时使用这两个插件，根据不同的测试场景选择不同的工具。

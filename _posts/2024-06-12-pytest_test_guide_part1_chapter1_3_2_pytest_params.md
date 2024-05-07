---
title: 《pytest测试指南》-- 章节1-3 pytest参数详解PART2
date: 2024-06-12 21:09:15
author: Gavin Wang
img: "/img/pytest/pytest-5.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 《pytest测试指南》一书 章节1-3 pytest参数详解PART2
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

## 3.2.3 Reporting 相关参数

### 3.2.3.1 参数  `--durations=N`

`pytest` 的 `--durations=N` 选项用来显示测试集中耗时最长的 `N` 个测试步骤。这可以帮助你识别测试中的性能瓶颈并优化那些耗时较多的测试。这个选项对于提高大型测试套件的效率尤其有用。

**使用方法：**

显示耗时最长的 `N` 个测试步骤的执行时间：

```shell
pytest --durations=N
```

其中 `N` 是一个整数，代表你想显示的慢速测试的数量。

**详细说明：**

- 当你执行 `pytest --durations=N` 时，测试完成后，`pytest` 会列出耗时最长的 `N` 个测试步骤，包括测试函数、测试设置（如 fixture）和测试清理的耗时。

- 列表将按照耗时排序，最耗时的测试排在最前面。

- 此功能有助于调试和性能分析，因为它提供了哪些测试或测试步骤导致整体测试时间增长的直接视图。

- `--durations` 后面的值 `N` 必须是一个非负整数。如果设置为 `0`，将报告所有测试步骤的持续时间；如果设置为正数，比如 `--durations=10`，将报告耗时最长的前 10 个测试步骤。

- 报告中显示的时间通常以秒为单位，并且显示测试设置（如 fixture）、测试模块与函数等信息。

- 这个选项特别有利于在持续集成（CI）流程中识别哪些测试可能需要优化以减少整个测试周期所需的时间。




使用 `--durations` 选项是提高测试套件效率和性能的一种实用方式。通过识别最耗时的测试，你可以决定是否有可能通过优化代码、减少冗余操作、采用并行测试等措施来减少这些测试的执行时间。




### 3.2.3.2 参数  `--durations-min=N`

`pytest` 的 `--durations-min=N` 选项用来显示测试集中耗时超过`N`秒的用例、前后置函数（setup、teardown、fixture），识别测试中哪些函数比较耗时。此参数需要结合`--durations`配合使用，单独使用无法展示出效果，借助此两个选项，优化用例执行时间，提升测试用例/测试套件效率非常有用。

**使用方法：**

显示耗时超过 `N` 秒的测试用例、前后置条件：

```shell
pytest --durations=0 --durations-min=N
```

其中 `N` 可以是整数，也可以是浮点数，单位是秒，代表你想显示的用例、前后置条件超过给定秒数的用例。此参数与`--durations`相似，此处不多额外说明。

**示例：**

```python
root@Gavin:~/code/chapter1-3# ll
total 16
drwxr-xr-x 2 root root 4096 Dec 11 17:01 ./
drwxr-xr-x 7 root root 4096 Dec 11 16:05 ../
-rw-r--r-- 1 root root  476 Dec 11 15:32 test_setup_teardown.py
-rw-r--r-- 1 root root  555 Dec 11 16:13 test_show_fixtures.py
root@Gavin:~/code/chapter1-3# cat test_setup_teardown.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
This is an example of setup and teardown 
"""

import time
import pytest


def setup(autouse=True):
    print("This is a setup")
    time.sleep(2)


def teardown(autouse=True):
    print("This is a teardown")
    time.sleep(5)


def test_case_1():
    """  Test case 1  """
    print("case 1")

def test_case_2():
    """  Test case 2  """
    print("case 2")

def test_case_3():
    """  Test case 3  """
    print("case 3")
root@Gavin:~/code/chapter1-3# cat test_show_fixtures.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
This is an example pytest fixture
"""

import time
import pytest


@pytest.fixture()
def run_function():
    """  This is a function doc info  """
    print("Run before function...")
    yield
    print("Run after function...")


def test_case_1(run_function):
    """  Test case 1  """
    print("case 1")
    time.sleep(3)

def test_case_2():
    """  Test case 2  """
    print("case 2")
    time.sleep(2)

def test_case_3(run_function):
    """  Test case 3  """
    print("case 3")
    time.sleep(4)
root@Gavin:~/code/chapter1-3#
```

执行效果：

只携带上`--durations`参数：

```python
root@Gavin:~/code/chapter1-3# pytest --durations=3 test_show_fixtures.py test_setup_teardown.py 
============================== test session starts ==========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-3
collected 6 items
test_show_fixtures.py ...                                               [ 50%]
test_setup_teardown.py ...                                              [100%]

============================== slowest 3 durations ===========================
5.01s teardown test_setup_teardown.py::test_case_3
4.00s call     test_show_fixtures.py::test_case_3
3.01s call     test_show_fixtures.py::test_case_1
============================== 6 passed in 16.07s ============================
root@Gavin:~/code/chapter1-3# 
```

携带上`--durations`  和 `--durations-min`参数：

```python
root@Gavin:~/code/chapter1-3# pytest --durations=0 --durations-min=3 test_show_fixtures.py test_setup_teardown.py 
============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-3
collected 6 items
test_show_fixtures.py ...                                               [ 50%]
test_setup_teardown.py ...                                              [100%]

=============================== slowest durations ============================
5.00s teardown test_setup_teardown.py::test_case_3
4.01s call     test_show_fixtures.py::test_case_3
3.01s call     test_show_fixtures.py::test_case_1

(15 durations < 3s hidden.  Use -vv to show these durations.)
=============================== 6 passed in 16.05s ===========================
root@Gavin:~/code/chapter1-3# 
```

携带上`--durations-min`参数：

```python
root@Gavin:~/code/chapter1-3# pytest --durations-min=3 test_show_fixtures.py test_setup_teardown.py 
=============================== test session starts ==========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code/chapter1-3
collected 6 items 
test_show_fixtures.py ...                                               [ 50%]
test_setup_teardown.py ...                                              [100%]

================================ 6 passed in 16.05s ==========================
root@Gavin:~/code/chapter1-3# 
```



三种情况综合对比图：

<img class="shadow" src="/img/in-post/chatp1-3_durations相关参数.png" width="800">



### 3.2.3.3 参数 -v --verbose

`pytest` 的 `-v` 或 `--verbose` 选项用于让测试运行时输出更详细的信息。通常，`pytest` 在执行测试时默认会输出一个比较简洁的结果，例如哪些测试通过了，哪些失败了。使用 `-v` 或 `--verbose` 选项可以让 `pytest` 提供更多的细节，比如每个测试函数的名称以及它们的结果。

**使用方法：**

```shell
pytest -v
```

或者

```shell
pytest --verbose
```

**输出对比：**

- **没有 `-v`**: 默认情况下，当运行 `pytest` 时，你会看到每个测试文件中通过和失败的测试数量，通常标记为`.` (通过) 和 `F` (失败)。
- **使用 `-v`**: 运行 `pytest -v` 时，在每个测试之前，你将看到它的完整路径和名称，以及它是通过 (`PASSED`) 还是失败 (`FAILED`)。

示例：

```python
root@Gavin:~/code/chapter1-3# cat test_time1.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-


def test_day_of_week():
    from datetime import datetime
    """  Determine what day of the week it is  """
    today = datetime.now().weekday()
    """  0: 周一; 1: 周二; 2:周三; ......,6:周日  """
    assert today == 1


def test_days_in_year():
    """ Determine if the current year is 365 days long  """
    import datetime
    current_year = datetime.date.today().year
    start_date = datetime.date(current_year, 1, 1)
    end_date = datetime.date(current_year, 12, 31)
    days_count = (end_date - start_date).days + 1
    assert days_count == 365
root@Gavin:~/code/chapter1-3# cat test_time2.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import time

def test_AM_or_PM():
    """  Determine current time is AM or PM  """
    AM = PM = False
    current_time = time.localtime()
    if current_time.tm_hour < 12:
        AM = True
    else:
        PM = True

    assert AM is True
    assert PM is False


def test_day_or_night():
    """ Determine whether the current time is day or night  """
    # 0 - 5, 19 - 23 -> night, 6 - 18 -> day
    night_time = day_time = False
    current_time = time.localtime()

    if current_time.tm_hour < 6 or current_time.tm_hour > 18:
        night_time = True
    else:
        day_time = True

    # assert night_time
    assert day_time
root@Gavin:~/code/chapter1-3#
```



- **没有 `-v`**:

```python
root@Gavin:~/code# pytest chapter1-3/test_time1.py chapter1-3/test_time2.py 
============================= test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
collected 4 items                                                                         
chapter1-3/test_time1.py ..                                             [ 50%]
chapter1-3/test_time2.py F.                                             [100%]
============================== FAILURES  =====================================
______________________________ test_AM_or_PM _________________________________

    def test_AM_or_PM():
        """  Determine current time is AM or PM  """
        AM = PM = False
        current_time = time.localtime()
        if current_time.tm_hour < 12:
            AM = True
        else:
            PM = True
    
>       assert AM is True
E       assert False is True

chapter1-3/test_time2.py:15: AssertionError
============================== short test summary info =======================
FAILED chapter1-3/test_time2.py::test_AM_or_PM - assert False is True
============================== 1 failed, 3 passed in 0.03s ===================
root@Gavin:~/code#
```

- **使用 `-v`**:

```python
root@Gavin:~/code# pytest -v chapter1-3/test_time1.py chapter1-3/test_time2.py 
=============================== test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code
collected 4 items                                                       [ 25%]
chapter1-3/test_time1.py::test_days_in_year PASSED                      [ 50%]
chapter1-3/test_time2.py::test_AM_or_PM FAILED                          [ 75%]
chapter1-3/test_time2.py::test_day_or_night PASSED                      [100%]

================================  FAILURES ====================================
________________________________ test_AM_or_PM ________________________________

    def test_AM_or_PM():
        """  Determine current time is AM or PM  """
        AM = PM = False
        current_time = time.localtime()
        if current_time.tm_hour < 12:
            AM = True
        else:
            PM = True
    
>       assert AM is True
E       assert False is True

chapter1-3/test_time2.py:15: AssertionError
===============================  short test summary info =======================
FAILED chapter1-3/test_time2.py::test_AM_or_PM - assert False is True
===============================  1 failed, 3 passed in 0.03s ===================
root@Gavin:~/code#
```

在上面的例子中，`test_time2.py` 中的 `test_AM_or_PM` 测试失败了，而其他测试都通过了。使用 `-v` 选项可以让你更清晰地看到每个测试的结果，并有助于在出现问题时进行调试。

该选项对于调试、跟踪运行的特定测试，以及在构建系统和持续集成工具中查看详细的测试执行记录尤其有用。如果你在测试套件中有大量的测试，而其中一些失败了，使用 `-v` 选项可以帮助你快速定位失败的测试，因此这个选项在测试开发过程中是一个非常有价值的工具。



### 3.2.3.4 参数 --no-header

`pytest` 的 `--no-header` 选项是用来在测试运行输出中去掉头部信息的。通常，`pytest` 在开始运行测试时会打印一些环境和配置的相关信息，这些信息构成了"头部"。使用 `--no-header` 选项，你可以告知 `pytest` 省略这些信息，只输出测试结果。

**使用方法：**

```shell
pytest --no-header
```

默认的 `pytest` 头部信息：

当你运行 `pytest` 时，它会输出一些诊断信息，如平台信息、Python 版本、`pytest` 版本、`plugins` 以及其他相关的配置信息。这些信息通常出现在测试结果的顶部。

示例（带头部信息）：

```python
root@Gavin:~/code# pytest chapter1-3/test_time1.py
================================ test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
collected 2 items
chapter1-3/test_time1.py ..                                               [100%]

================================= 2 passed in 0.00s ============================
root@Gavin:~/code#
```

**示例（没有头部信息，使用 `--no-header`）：**

```python
root@Gavin:~/code# pytest --no-header chapter1-3/test_time1.py
================================ test session starts ===========================
collected 2 items
chapter1-3/test_time1.py ..                                               [100%]

================================ 2 passed in 0.00s =============================
root@Gavin:~/code#
```

可以看到，使用 `--no-header` 后，关于平台、Python 版本、pytest 版本及插件的信息都被省略了。只有测试收集和执行的信息被打印出来。这可以让输出看起来更简洁，尤其是在自动化环境中，可能你并不需要这些额外的信息。

这个选项在合并测试结果输出到其他工具或当你只关注测试执行结果时非常有用。如果要了解测试环境的详细信息，运行时则不应该使用 `--no-header` 选项。



### 3.2.3.5 参数 --no-summary

`pytest` 的 `--no-summary` 选项最初在`pytest 7.0`中引入，用于在测试运行的输出中省略最后的总结信息，提供一个简短的总结(`short test summary info`)，指出有多少测试通过、失败、跳过等。

**使用方法：**

```shell
pytest --no-summary
```

默认的 `pytest` 总结信息：

默认情况下，当测试运行完成后，`pytest` 会在控制台的运行阶段输出错误点的相关详细信息，以及在控制台的最后输出用例错误状态总结（注意下文中的`short test summary info`）。

**示例（带总结信息）：**

```python
root@Gavin:~/code# pytest chapter1-3/
============================== test session starts ========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
collected 14 items
chapter1-3/test_example.py .x.F                                       [ 28%]
chapter1-3/test_setup_teardown.py ...                                 [ 50%]
chapter1-3/test_show_fixtures.py ...                                  [ 71%]
chapter1-3/test_time1.py ..                                           [ 85%]
chapter1-3/test_time2.py F.                                           [100%]

============================== FAILURES ====================================
______________________________ test_assert_failed __________________________

    def test_assert_failed():
>       assert all([elem == 1 for elem in list(range(5))])
E       assert False
E        +  where False = all([False, True, False, False, False])

chapter1-3/test_example.py:21: AssertionError
______________________________ test_AM_or_PM _______________________________

    def test_AM_or_PM():
        """  Determine current time is AM or PM  """
        AM = PM = False
        current_time = time.localtime()
        if current_time.tm_hour < 12:
            AM = True
        else:
            PM = True
    
>       assert AM is True
E       assert False is True

chapter1-3/test_time2.py:15: AssertionError
============================= short test summary info =====================
FAILED chapter1-3/test_example.py::test_assert_failed - assert False
FAILED chapter1-3/test_time2.py::test_AM_or_PM - assert False is True
======================== 2 failed, 11 passed, 1 xfailed in 7.06s ==========
root@Gavin:~/code#
```

**示例（没有总结信息，使用 `--no-summary`）：**

```python
root@Gavin:~/code# pytest --no-summary  chapter1-3/
============================= test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
collected 14 items
chapter1-3/test_example.py .x.F                                        [ 28%]
chapter1-3/test_setup_teardown.py ...                                  [ 50%]
chapter1-3/test_show_fixtures.py ...                                   [ 71%]
chapter1-3/test_time1.py ..                                            [ 85%]
chapter1-3/test_time2.py F.                                            [100%]

============================ 2 failed, 11 passed, 1 xfailed in 7.05s =========
root@Gavin:~/code#
```

在上面的示例中，使用 `--no-summary` 选项后，输出中省略了最后的总结行，这样可以使输出更加简洁。



如果用例执行都是成功的，带不带`--no-summary`并没有什么区别，如下图所示：

<img class="shadow" src="/img/in-post/chatp1-3_no-summary.png" width="800">

这个选项对于想减少输出中的干扰，将测试结果传递给其他工具或者在自动化脚本中处理测试结果时非常有用。如果你只关心测试是否全部通过，而不太在意具体的错误信息，那么 `--no-summary` 可以帮助清理控制台输出。但如果你需要了解详细的测试报错，比如在调试失败的测试时，那么就不应该使用 `--no-summary` 选项。



### 3.2.3.6 参数 -q, --quiet

`pytest` 的 `-q` 或 `--quiet` 选项是用来减少测试运行输出的冗余信息的，使输出更加简洁。在 `pytest` 中使用 `-q` 或 `--quiet` 时，会减少控制台上打印的日志量，这对于你要快速检查测试是否通过而不需要查看详细的失败信息时很有用。

**使用方法：**

```shell
pytest -q
```

或

```shell
pytest --quiet
```

这两种方式都会实现同样的效果。

默认 `pytest` 输出：

在默认设置下，`pytest` 会显示每个测试文件的每个测试函数的详细结果，以及全面的状态总结。

**示例（默认详细度）：**

```python
root@Gavin:~/code# pytest chapter1-3/test_time1.py chapter1-3/test_time2.py 
============================= test session starts ===========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
collected 4 items
chapter1-3/test_time1.py ..                                             [ 50%]
chapter1-3/test_time2.py F.                                             [100%]
```

**示例（使用 `-q` 或 `--quiet`）：**

```python
root@Gavin:~/code# pytest -q chapter1-3/test_time1.py chapter1-3/test_time2.py 
..F.                                                                             [100%]
```

在使用 `--quiet` 后，测试的输出变得更加简洁，只显示每个测试点的结果 (`.` 代表通过, `F` 代表失败)，并在最后提供失败的测试的简短摘要。如果所有测试都通过，则输出将仅包含测试点的结果。

如果你需要进一步减少输出信息，还可以结合使用 `--no-header` 和 `--no-summary` 选项来分别移除头部环境信息和尾部的测试总结，只保留结果指示。这在某些快速检查或大型自动化测试环境中非常有用。



### 3.2.3.7 参数 --verbosity=VERBOSE

`pytest` 的 `--verbosity` 选项是用来控制测试运行时输出的详细程度的。`VERBOSE` 是一个整数值，用于指定你希望看到的信息量。当你增加 `VERBOSE` 的值时，你将会看到更多的信息；当你减少该值时，输出的信息会更少。

**使用方法：**

```shell
pytest --verbosity=N
```

这里 `N` 是可选的整数值，代表不同的详细级别：

- `0` (或者不使用 `--verbosity` 选项)：默认的详细程度，提供中等量的信息，包含每个测试函数的结果和一个简短的总结。
- `1`：更详细的输出，类似于不使用任何详细度选项的默认行为，通常显示测试名称和结果。
- `2`：更高的详细程度，显示测试的额外信息，如测试的设置和拆解步骤（setup和teardown）。
- `-1`：减少输出的详细程度，等同于使用 `-q` 或 `--quiet`，会提供更简洁的输出。

说明：

```shell
"-vv" === "--verbose --verbose" === "--verbosity=2"
```



**示例：**

假设有如下几个测试：

```python
root@Gavin:~/code/chapter1-3# cat test_verbosity.py
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest

def test_pass():
    assert 1 == 1

def test_fail():
    assert 1 == 2

def test_skip():
    pytest.skip('skipping this test case')

@pytest.mark.xfail
def test_xfail():
    assert 1 == 2
```

减少输出的详细程度（-1）：

```python
root@Gavin:~/code# pytest --verbosity=-1 chapter1-3/test_verbosity.py 
.Fsx                                                                [100%]
=============================== FAILURES =================================
_______________________________ test_fail ________________________________
    def test_fail():
>       assert 1 == 2
E       assert 1 == 2

chapter1-3/test_verbosity.py:16: AssertionError
============================== short test summary info ====================
FAILED chapter1-3/test_verbosity.py::test_fail - assert 1 == 2
1 failed, 1 passed, 1 skipped, 1 xfailed in 0.03s
root@Gavin:~/code#
```

默认详细度 (`0` 或没有 `--verbosity`)：

```python
root@Gavin:~/code# pytest --verbosity=0 chapter1-3/test_verbosity.py 
============================== test session starts =========================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
collected 4 items
chapter1-3/test_verbosity.py .Fsx                                     [100%]

============================== FAILURES =====================================
______________________________ test_fail ____________________________________
    def test_fail():
>       assert 1 == 2
E       assert 1 == 2

chapter1-3/test_verbosity.py:16: AssertionError
========================== short test summary info ==========================
FAILED chapter1-3/test_verbosity.py::test_fail - assert 1 == 2
==================1 failed, 1 passed, 1 skipped, 1 xfailed in 0.03s =========
root@Gavin:~/code#
```

轻微详细 (`1`)：

```python
root@Gavin:~/code# pytest --verbosity=1 chapter1-3/test_verbosity.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code
collected 4 items
chapter1-3/test_verbosity.py::test_pass PASSED                            [ 25%]
chapter1-3/test_verbosity.py::test_fail FAILED                            [ 50%]
chapter1-3/test_verbosity.py::test_skip SKIPPED (skipping this test case) [ 75%]
chapter1-3/test_verbosity.py::test_xfail XFAIL                            [100%]

============================= FAILURES ========================================
_____________________________ test_fail _______________________________________
    def test_fail():
>       assert 1 == 2
E       assert 1 == 2

chapter1-3/test_verbosity.py:16: AssertionError
============================ short test summary info ==========================
FAILED chapter1-3/test_verbosity.py::test_fail - assert 1 == 2
=============== 1 failed, 1 passed, 1 skipped, 1 xfailed in 0.03s =============
root@Gavin:~/code#
```

高详细度 (`2`):

```python
root@Gavin:~/code# pytest --verbosity=2 chapter1-3/test_verbosity.py 
=========================== test session starts ===============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/code
collected 4 items
chapter1-3/test_verbosity.py::test_pass PASSED                                 [ 25%]
chapter1-3/test_verbosity.py::test_fail FAILED                                 [ 50%]
chapter1-3/test_verbosity.py::test_skip SKIPPED (skipping this test case)      [ 75%]
chapter1-3/test_verbosity.py::test_xfail XFAIL                                 [100%]

============================== FAILURES ========================================
______________________________ test_fail _______________________________________
    def test_fail():
>       assert 1 == 2
E       assert 1 == 2

chapter1-3/test_verbosity.py:16: AssertionError
============================== short test summary info =========================
FAILED chapter1-3/test_verbosity.py::test_fail - assert 1 == 2
================ 1 failed, 1 passed, 1 skipped, 1 xfailed in 0.03s =============
root@Gavin:~/code# 
```

从结果上看，`-v`  和  `-vv`的输出结果非常接近，甚至某些情况下内容一致。



每个测试的执行状态都会以不同程度的详细信息显示出来。在命令行中找到适合你当前需求的详细程度可以帮你更快地理解测试结果。高详细度非常有用，例如，当你需要调试测试问题或者理解测试执行的流程时。而在自动化环境或持续集成系统中，你可能会想要减少输出的详细程度。



### 3.2.3.8 参数 -r chars

`pytest` 的 `-r` 选项用于自定义结果输出的详细程度(默认: 'fE')。它允许你通过使用不同的字符选择要显示的测试结果类型。

**使用方法：**

```shell
pytest -r chars
```

其中，`chars` 是一组字符，每个字符代表一种特定的测试结果。字符可以组合使用，每种字符的含义如下：

- `F`：显示失败的测试 (FAILURES).
- `E`：显示错误的测试 (ERRORS).
- `S`：显示跳过的测试 (SKIPPED).
- `X`：显示预期失败但通过的测试 (XFAIL)，即意外的成功测试。
- `x`：显示预期失败的测试（即本来就预期会失败，但失败了并不影响测试结果）。
- `P`：显示通过的测试 (PASSED).
- `p`：显示通过的测试（部分，如果有使用 `-k` 提供表达式仅部分测试通过）。
- `a`：显示所有测试（all）。
- `A`：自动分页显示测试结果，这有助于防止在跑大量测试时屏幕滚动过快过多。

**示例：**

假设我们有以下测试用例，有的通过了，有的失败了，有的被跳过：

```python
root@Gavin:~/code/chapter1-3# cat test_parameter_r.py 
#!/usr/bin/env python
# -*- coding:utf-8 -*-


import pytest


def test_pass():
    assert 1 == 1


def test_fail():
    assert 0 == 1


def test_skip():
    pytest.skip('skipping this test case.')


@pytest.mark.xfail
def test_xfail():
     assert 1 == 2


@pytest.mark.xfail
def test_xpass():
    assert 2 == 2
root@Gavin:~/code/chapter1-3#
```

我们可以使用不同的 `-r` 选项来自定义我们想要显示哪些类型的结果。

只显示失败 (`F`) 和 错误 (`E`):

```shell
pytest -rFE
```



```python
root@Gavin:~/code# pytest -rFE chapter1-3/test_parameter_r.py 
============================ test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
collected 5 items
chapter1-3/test_parameter_r.py .FsxX                                    [100%]

================================= FAILURES ===================================
_________________________________ test_fail __________________________________
    def test_fail():
>       assert 0 == 1
E       assert 0 == 1

chapter1-3/test_parameter_r.py:13: AssertionError
========================== short test summary info ===========================
FAILED chapter1-3/test_parameter_r.py::test_fail - assert 0 == 1
======= 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 xpassed in 0.03s =========
root@Gavin:~/code#
```

显示失败 (`F`), 跳过 (`S`), 预期失败但通过 (`x`), 和 预期失败 (`X`):

```shell
pytest -rFSxX
```

```python
root@Gavin:~/code# pytest -rFSxX chapter1-3/test_parameter_r.py 
============================  test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
collected 5 items
chapter1-3/test_parameter_r.py .FsxX                                    [100%]

=============================  FAILURES ======================================
_____________________________ test_fail ______________________________________
    def test_fail():
>       assert 0 == 1
E       assert 0 == 1

chapter1-3/test_parameter_r.py:13: AssertionError
==========================  short test summary info ==========================
FAILED chapter1-3/test_parameter_r.py::test_fail - assert 0 == 1
SKIPPED [1] chapter1-3/test_parameter_r.py:17: skipping this test case.
XFAIL chapter1-3/test_parameter_r.py::test_xfail
XPASS chapter1-3/test_parameter_r.py::test_xpass 
======== 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 xpassed in 0.03s ========
root@Gavin:~/code#
```



使用 `-r` 选项可以帮助你创建更易于阅读和理解的测试输出。你可以根据你的需要和测试的上下文环境，选择合适的组合。在一些持续集成环境中，通常只关心失败的测试结果，那么只需包含 `-rF` 选项即可。而在日常开发中，了解哪些测试被跳过可能也很重要，那么 `-rFS` 就会有所帮助。



### 3.2.3.9 参数 --disable-warnings, --disable-pytest-warnings

`pytest` 是一个非常流行的 Python 测试框架，它有很多可以控制测试行为和输出的命令行选项。在执行测试时，你可能会遇到警告信息，这些警告可能来自于测试代码本身或者使用的第三方库。虽然警告信息可以提供有用的信息，但有时候你可能想要在测试输出中隐藏这些警告信息，以便专注于测试结果。

**使用方法：**

`pytest` 提供了两个选项来禁用警告信息：

* `--disable-warnings`

该选项将会禁用所有测试运行中的警告信息，包括来自 Python 内部函数和第三方库的警告。这可以让你的测试结果输出更加清晰，只包含测试执行的结果信息。

```shell
pytest --disable-warnings
```

加入此参数后，任何使用 Python 标准库 `warnings` 发出的警告，以及第三方库生成的警告都不会在测试输出中显示。

* `--disable-pytest-warnings` 

```shell
pytest --disable-pytest-warnings
```

该选项用于禁用由 `pytest` 产生的警告，但从实际使用效果看， 与`--disable-warnings`效果相同。

**示例：**

```python
root@Gavin:~/code# cat chapter1-3/test_warnings.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-


import warnings


def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1


def test_one():
    assert api_v1() == 1
root@Gavin:~/code#
```

不携带`--disable-warnings`或者`--disable-pytest-warnings`的效果:

```python
root@Gavin:~/code# pytest chapter1-3/test_warnings.py 
============================== test session starts ============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
collected 1 item
chapter1-3/test_warnings.py .                                            [100%]

============================ warnings summary =================================
chapter1-3/test_warnings.py::test_one
  /root/code/chapter1-3/test_warnings.py:9: UserWarning: api v1, should use functions from v2
    warnings.warn(UserWarning("api v1, should use functions from v2"))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
========================== 1 passed, 1 warning in 0.00s =======================
root@Gavin:~/code#
```

携带`--disable-warnings`的效果:

```python
root@Gavin:~/code# pytest --disable-warnings chapter1-3/test_warnings.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
collected 1 item
chapter1-3/test_warnings.py .                                           [100%]

========================== 1 passed, 1 warning in 0.00s =======================
root@Gavin:~/code#
```

携带`--disable-pytest-warnings`的效果:

```python
root@Gavin:~/code# pytest --disable-pytest-warnings chapter1-3/test_warnings.py 
============================= test session starts =============================
platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /root/code
collected 1 item
chapter1-3/test_warnings.py .                                           [100%]

==========================  1 passed, 1 warning in 0.00s ======================
root@Gavin:~/code# 
```



**请注意：**

**不显示警告并不意味着问题已经解决。** 通常，警告信息是有其存在的目的，它们可能指出了代码潜在的问题，例如过时的函数使用、不建议的做法、未来可能出现的问题等。因此，在禁用警告输出时，请确保你理解为什么要这么做，并且已经考虑到了可能的影响。在开发过程中解决这些警告通常是一个更好的做法。



### 3.2.3.10 参数 --showlocals

`pytest` 中的 `-l` 或 `--showlocals` 选项是用来在测试失败的报告信息中显示局部变量的值。这对于调试失败的测试特别有用，因为它允许开发者看到当测试失败时，在测试函数以及涉及的其他相关代码中的局部变量的精确值。

这个选项可以让你更快地理解为什么测试失败了，尤其是在复杂的测试场景中，其中可能需要理解不同函数和对象的状态。

**使用方法：**

在运行 `pytest` 命令时，加上 `-l` 或 `--showlocals` 选项：

```shell
pytest -l
# 或者
pytest --showlocals
```

**示例：**

假如我们在`chapter1-3/test_example.py`文件中有以下的测试函数：

```python
def test_assert_example():
    a = 5
    b = 10
    assert a + b == 20
```

不加 `-l` 或 `--showlocals` 选项，当测试失败时，默认的输出可能只告诉你 `assert` 语句失败了，但不会告诉你 `a` 和 `b` 的值是多少。

如果使用了 `-l` 或 `--showlocals` 选项，当测试失败了，`pytest` 会在报告信息中包括 `a` 和 `b` 的值，输出类似下面这样：

```python
============================== FAILURES ====================================
______________________________ test_assert_example _________________________

    def test_assert_example():
        a = 5
        b = 10
>       assert a + b == 20
E       assert (5 + 10) == 20

a          = 5
b          = 10

chapter1-3/test_example.py:27: AssertionError
```

在这里，你可以清楚地看到 `a` 和 `b` 的值，并且能够推断出为什么 `assert` 断言失败了。

**说明：**

虽然 `--showlocals` 选项在定位问题时非常有用，但它可能会导致报告输出变得非常长，尤其是当测试用例涉及的局部变量很多时。所以，建议仅在需要调试特定失败的测试时使用这个选项，或者结合其他命令行选项使用，如 `-k` 选项，以只针对某些特定的测试输出局部变量。



### 3.2.3.11 参数 --no-showlocals

在 `pytest` 中，`--no-showlocals` 选项用于禁止在测试失败的报告信息中显示局部变量的值。通常，`pytest` 会自动显示测试失败时的局部变量和它们的值，这有助于调试和快速地识别问题所在。然而，有时你可能会想要一个更简洁的失败报告，不包括局部变量的详细信息，尤其是当局部变量太多或它们的输出太长、过于冗余的时候。

**使用方法：**

当你运行 `pytest` 并希望隐藏失败测试中的局部变量，在命令行中加入 `--no-showlocals` 选项：

```shell
pytest --no-showlocals
```

使用这个选项后，即使测试失败，`pytest` 也不会显示局部变量和它们的值。这会给你一个更简洁的失败输出，可能仅包含失败的 `assert` 语句和一些基本的错误信息。

**请注意：**

- 当命令行中同时存在 `--showlocals`（或 `-l`）和 `--no-showlocals` 选项时，后出现的选项会覆盖前面的。
- 由于 `pytest` 默认不显示局部变量，所以在许多情况下不需要显式地使用 `--no-showlocals` 选项，除非你想要覆盖配置文件中的设置（例如在 `pytest.ini` 或 `pyproject.toml` 中配置了显示局部变量）。

**示例：**

假设你在配置文件中设置了默认显示局部变量的值，如下：

```ini
# content of pytest.ini
[pytest]
showlocals = true
```

当你想要在特定的测试运行中去除这个行为，可以在命令行中使用 `--no-showlocals` 来覆盖配置文件中的设置：

```shell
pytest --no-showlocals
```

在这种情况下，即使 `pytest.ini` 配置是显示局部变量，使用了 `--no-showlocals` 选项的测试运行将不展示失败测试的局部变量。



### 3.2.3.12 参数 --tb=style

`pytest` 的 `--tb=style` 选项用于指定当测试失败时，堆栈跟踪（traceback）的输出格式。`style` 是一个参数，它可以取不同的值来更改堆栈跟踪的显示方式。这允许开发者根据个人喜好或特定调试需求选择不同的堆栈跟踪显示风格。

下面是 `--tb` 选项可以接受的几个不同的值：

- `auto`：默认的选项，会智能地缩短跟踪输出，通常只显示最后几行。
- `long`：最详细的跟踪格式，它会展示所有的相关调用，不进行任何裁剪，这对于理解复杂错误非常有帮助。
- `short`：这将产生一个较短的跟踪，其中只包含引发错误的行数，而不包含整个堆栈跟踪。
- `line`：这个选项只显示导致异常的那一行代码，省去所有额外的跟踪信息。
- `no`：没有跟踪输出。
- `native`：使用 Python 标准库的跟踪打印。

**使用方法：**

在运行 `pytest` 命令时，加上 `--tb` 选项和相应的参数值：

```shell
pytest --tb=short # 使用短格式的跟踪
pytest --tb=long  # 使用长格式的跟踪
pytest --tb=line  # 只显示导致测试失败的代码行
pytest --tb=no    # 完全不显示跟踪
```

**示例：**

假如我们在`chapter1-3/test_example.py`文件中有以下的测试函数会抛出一个异常：

```python
def test_divide():
    num = 10
    denom = 0
    assert num / denom == 0
```

在这里，测试失败不仅因为断言错误，还因为有一个除以零的错误。

运行 `pytest` 带有不同的 `--tb` 选项会产生不同的输出：

- `--tb=short` 只会显示异常的相关代码行和一个简短的错误提示。
- `--tb=long` 会展示更多有关调用堆栈的信息，有时这可以包括你的测试函数之外的代码。
- `--tb=no` 不显示任何跟踪信息，只告诉你哪些测试失败了。

如下图所示：

<img class="shadow" src="/img/in-post/chatp1-3_tb.png" width="800">

选择适合你当前调试任务的 `--tb` 风格可以帮助你更快地定位问题。




### 3.2.3.13 参数 --show-capture={no,stdout,stderr,log,all}

`pytest` 提供了 `--show-capture` 选项，允许用户控制在测试失败或测试执行过程中产生的标准输出(`stdout`)、标准错误(`stderr`)和日志输出的显示行为。根据选项后面的参数，`pytest` 将会决定在测试报告中展现哪些类型的捕获输出。

参数选项如下：

- `no`：完全不显示任何捕获的输出。
- `stdout`：只显示测试中捕获的标准输出(`stdout`)。
- `stderr`：只显示测试中捕获的标准错误(`stderr`)。
- `log`：只显示测试中捕获的日志输出。
- `all`：显示所有类型的捕获输出，包括`stdout、stderr`和`log`。

**使用方法：**

在运行 `pytest` 命令时，可以加上 `--show-capture` 选项和所需的参数值：

```shell
pytest --show-capture=no     # 不展示任何捕获的输出
pytest --show-capture=stdout # 只展示标准输出
pytest --show-capture=stderr # 只展示标准错误
pytest --show-capture=log    # 只展示日志输出
pytest --show-capture=all    # 展示所有捕获的输出
```

**示例：**

假设在`chapter1-3/test_example.py`文件中有这样的一个测试函数，它打印了一些信息到标准输出，并记录了一个日志消息：

```python
import logging

def test_output_example():
    print("Hello, this is stdout!")
    logging.warning("This is a warning log message.")
    assert 0 
```

根据你使用的 `--show-capture` 选项，输出结果会有所不同：

- 运行 `pytest --show-capture=no` 不会在失败报告中包含任何`Hello, this is stdout!`或日志消息。
- 运行 `pytest --show-capture=stdout` 仅会包含`Hello, this is stdout!`。
- 运行 `pytest --show-capture=log` 仅会包含`This is a warning log message.`。
- 运行 `pytest --show-capture=all` 会包含`Hello, this is stdout!`和`This is a warning log message.`。

根据你的需求，可以选择适当的设置来帮助你专注于特定类型的输出，是调试更简洁、更有效。




### 3.2.3.14 参数 --full-trace

`pytest` 的 `--full-trace` 选项提供了在测试失败时显示完整的堆栈跟踪信息，而不是仅显示直接与测试用例相关的部分。它通常用于调试复杂的问题，当需要了解事件是如何从调用堆栈的更深层次传播出来的时候特别有用。

在没有任何堆栈跟踪参数的默认情况下，`pytest` 可能会截断部分跟踪信息来提供更简洁的输出。然而，当事情变得复杂，你可能会需要看到详尽的调用信息来诊断问题。这时，`--full-trace` 就显得非常有用，因为它可以提供最全面的跟踪信息，包括库函数和内部调用在内的所有调用栈信息。

**使用方法：**

当执行 `pytest` 命令时，如果想要启用完整的堆栈跟踪，可以添加 `--full-trace` 选项：

```shell
pytest --full-trace
```

**示例：**

假设在`chapter1-3/test_example.py`文件中有一个测试函数，它调用了几层函数，并且在内部某处发生了异常：

```python
def helper_function():
    raise ValueError("An error occurred.")

def another_function():
    helper_function()

def test_another_example():
    another_function()
```

在运行 `pytest` 而不带 `--full-trace` 时，输出可能只会显示与 `test_another_example` 直接相关的异常信息。而使用了 `--full-trace` 的命令，将会输出完整的堆栈跟踪，包括 `helper_function` 和 `another_function` 的调用信息，这在理解异常的来源时非常有帮助。

**请注意：**

这个选项可能会导致非常长的输出，特别是当测试调用了许多层次的外部库或框架代码时。在寻找复杂问题的解决方案时，详细的堆栈信息才是最有用的；在其他时候，可能更倾向于较为简洁的输出。




### 3.2.3.15 参数 --color=color

`pytest` 的 `--color` 选项用于控制 `pytest `输出到控制台时使用的颜色。终端的颜色输出有助于区分测试的不同状态，比如成功、失败或跳过的测试。

`--color` 选项接受以下参数：

- `auto`：`pytest` 会自动检测终端是否支持颜色输出，并相应地启用或禁用颜色。这是默认行为。
- `yes` 或 `true`：在 `pytest`输出中强制使用颜色，即使检测到终端不支持颜色输出。
- `no` 或 `false`：在 `pytest` 输出中禁用颜色，即使终端支持颜色。

使用这个选项可以强制启用或禁用颜色输出，方便在不同的环境或情况下定制化 `pytest `的表现。这对于在不支持颜色的环境（例如某些持续集成系统的日志）查看输出或者创建无颜色的日志文件时非常有用。

**使用方法：**

在运行 `pytest` 命令时，可以加上 `--color` 选项和对应的值：

```shell
pytest --color=yes  # 强制使用颜色输出
pytest --color=no   # 禁用颜色输出
pytest --color=auto # 自动检测（默认）
```

根据你的终端和个人喜好，你可以选择使用这个选项来定制化 `pytest` 的输出。在某些情况下，如果终端不支持颜色而你又想要有色输出，或者你想在不同的显示背景（比如白色和黑色背景的终端中）都有良好的可读性，这个选项就特别有用。



### 3.2.3.16 参数 --code-highlight={yes,no}

`pytest` 的 `--code-highlight` 选项用于控制在测试失败时是否显示语法高亮的代码。这个特性旨在提升输出的可读性，让用户更容易地理解代码中的错误和测试结果。

**可选参数说明：**

- `yes` 或 `true`：启用语法高亮。当测试失败时，`pytest` 将显示语法高亮的代码段，以帮助用户快速识别代码结构和重要部分。
- `no` 或 `false`：禁用语法高亮。测试失败时，`pytest` 将显示没有高亮的代码段。

**示例：**

如果你想运行 `pytest` 并启用代码高亮，可以这样使用命令：

```shell
pytest --code-highlight=yes
```

反之，如果你希望禁用代码高亮，使用以下命令：

```shell
pytest --code-highlight=no
```

默认情况下，`pytest` 通常会根据输出环境自动决定是否使用代码高亮。例如，在大多数现代终端中，`pytest` 会自动启用代码高亮，因为它可以帮助开发者更好地阅读和理解输出结果。然而，在某些环境中，比如纯文本日志文件或不支持高亮的输出设备中，你可能会想禁用这个特性。

禁用代码高亮可能会在将测试结果导出到不支持颜色和格式化的系统时有所帮助，因为高亮代码可能包括特殊字符序列，这些在没有正确解释它们的情况下会干扰文本的阅读。



### 3.2.3.17 参数 --pastebin=mode 

`pytest` 的 `--pastebin` 选项允许你将测试失败的完整报告上传到一个公共的 `pastebin` 服务中，这样可以非常方便地与他人分享测试报告。上传后，`pytest` 会提供一个 URL，你可以将这个 URL 发送给其他人，以便他们可以查看测试报告的内容。

这个选项接受以下参数（即 `mode`）：

- `failed`：只上传失败的测试报告。
- `all`：上传所有测试的报告，无论是成功还是失败。

**使用方法：**

例如，如果你只想上传那些失败的测试报告，你应该在运行 `pytest` 时这样使用命令：

```shell
pytest --pastebin=failed
```

如果想上传所有的测试报告，也就是包括成功和失败的测试，你可以这样使用：

```shell
pytest --pastebin=all
```

使用这个功能时，需要注意的是，任何上传到 `pastebin` 的内容实际上是公开的，它可能会被搜索引擎索引，或者被任何知道该 URL 的人访问。因此，在上传敏感测试报告之前，请考虑测试报告中可能包含的数据和信息。另外，请注意，这个功能依赖于公共的 `pastebin` 服务是否可用，以及 `pytest` 是否能够支持当前可用的 `pastebin API`。上传服务可能因维护、`API` 更改或其他原因而不可用。




### 3.2.3.18 参数 --junit-xml=path

`pytest` 的 `--junit-xml` 选项允许用户生成一个 `JUnit` 格式的 XML 文件，通常这种类型的文件用来与持续集成 (CI) 系统一起使用，如` Jenkins、TeamCity` 或者任何其他支持 `JUnit` 格式的系统。`JUnit XML` 报告提供了一种标准化的测试结果报告格式，使得不同的工具和系统能够解读和展示测试结果。

**使用方法：**

你需要指定一个文件路径来保存 XML 报告。如果指定路径的目录尚未存在，`pytest` 会尝试创建它。

例如，如果你想保存测试结果到当前目录下的 `report.xml` 文件，可以这样使用该命令：

```shell
pytest --junit-xml=report.xml
```

如果你想保存到一个具体的目录（假设目录已经存在），可以这样做：

```shell
pytest --junit-xml=path/to/report/directory/report.xml
```

使用这个参数后，`pytest` 将在测试完成后生成一个 XML 文件，其中包含了测试套件的详细结果，如测试用例的名称、测试状态（成功、失败、错误、跳过等）、以及其他可能的错误信息和日志。

持续集成工具可以配置为在构建过程结束时读取这个文件，以收集和展示测试结果，有助于开发和测试团队快速定位和解决问题。

`--junit-xml` 选项是一个重要的功能，尤其是在自动化测试和CI/CD流程中，因为它有助于跨不同环境和工具共享和分析测试结果。




### 3.2.3.19 参数 --junit-prefix=str

`pytest` 的 `--junit-prefix` 选项用来为生成的 `JUnit XML` 报告中的测试用例名称添加一个前缀。这在当你要将多个测试报告合并起来时非常有用，或者当你在不同的环境（例如：不同的操作系统或不同的环境配置下）运行了多次测试，并希望在报告中更容易区分这些测试。

**使用方法：**

当运行 `pytest` 并且生成 `JUnit XML` 报告文件时，使用 `--junit-prefix` 选项可以为每个测试用例的名称前加上指定的字符串。

例如，假设你的项目在 Python 3.9 和 Python 3.11 两个版本的环境下测试，并且你想在`JUnit`报告中区分这两个环境的测试结果。你可以分别为每个环境指定不同的前缀：

```shell
pytest --junit-xml=report39.xml --junit-prefix=py39
```

和

```shell
pytest --junit-xml=report311.xml --junit-prefix=py311
```

在上述例子中，`py39` 和 `py311` 就是添加到对应环境测试用例名称前的前缀字符串。在最终生成的 `report39.xml` 和 `report311.xml` 文件中，测试用例的名称将包含这些指定的前缀，这有助于在后续的测试报告分析或者在持续集成的测试结果展示中清晰地区分不同环境的测试结果。

在 CI 系统中合并多个报告时，这样的前缀可以防止测试用例的名称冲突，并提供一个更清晰的报告结构。


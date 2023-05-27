---
layout:     post
title:      "pytest skip"
subtitle:   "pytest skip"
date:       2020-04-06
author:     "Gavin"
catalog:    true
tags:
    - pytest
    - Automation
---

# 概述

pytest.mark.skip  可以标记无法在某些平台上运行的测试功能，或者您希望失败的测试功能，或者硬件不满足用例执行条件的功能。
希望满足某些条件才执行某些测试用例，否则pytest会跳过运行该测试用例
实际常见场景：跳过非Windows平台上的仅Windows测试，或者跳过依赖于当前不可用的外部资源（例如数据库）的测试，或者跳过VM上执行用例而用例实际需要硬件支撑的测试。

本文只是概述一下skip的简易用法。

# 实战

## skip

@pytest.mark.skip

跳过执行测试用例，有可选参数reason：跳过的原因，会在执行结果中打印

{% raw %}```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(autouse=True)
def login():
    print("====登录====")


def test_case01():
    print("我是测试用例11111")


@pytest.mark.skip(reason="不执行该用例！！因为没写好！！")
def test_case02():
    print("我是测试用例22222")


class Test1:

    def test_1(self):
        print("%% 我是类测试用例1111 %%")

    @pytest.mark.skip(reason="不想执行")
    def test_2(self):
        print("%% 我是类测试用例2222 %%")


@pytest.mark.skip(reason="类也可以跳过不执行")
class TestSkip:
    def test_1(self):
        print("%% 不会执行 %%")
``` {% endraw %}

执行结果：


{% raw %}```
root@FC-2:~/pytest_framework/src# PYTHONPATH=. pytest --alluredir=../report/test test.py 
============================================================================================================================ test session starts =============================================================================================================================
platform linux2 -- Python 2.7.12, pytest-4.6.11, py-1.8.1, pluggy-0.13.1 -- /usr/bin/python2.7
cachedir: .pytest_cache
rootdir: /root/pytest_framework/src, inifile: pytest.ini
plugins: cov-2.10.0, progress-1.2.1, allure-pytest-2.8.11, repeat-0.8.0, timeout-1.3.4, ordering-0.6
collected 5 items                                                                                                                                                                                                                                                            

test.py::test_case01 PASSED                                                                                                                                                                                                                                             [1/5]
________________________________________________________________________________________________ 1 of 5 completed, 1 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun ________________________________________________________________________________________________

test.py::test_case02 SKIPPED                                                                                                                                                                                                                                            [2/5]
________________________________________________________________________________________________ 2 of 5 completed, 1 Pass, 0 Fail, 1 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun ________________________________________________________________________________________________

test.py::Test1::test_1 PASSED                                                                                                                                                                                                                                           [3/5]
________________________________________________________________________________________________ 3 of 5 completed, 2 Pass, 0 Fail, 1 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun ________________________________________________________________________________________________

test.py::Test1::test_2 SKIPPED                                                                                                                                                                                                                                          [4/5]
________________________________________________________________________________________________ 4 of 5 completed, 2 Pass, 0 Fail, 2 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun ________________________________________________________________________________________________

test.py::TestSkip::test_1 SKIPPED                                                                                                                                                                                                                                       [5/5]
________________________________________________________________________________________________ 5 of 5 completed, 2 Pass, 0 Fail, 3 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun ________________________________________________________________________________________________

========================================================================================================================== short test summary info ===========================================================================================================================
SKIPPED [1] test.py:16: 不执行该用例！！因为没写好！！
SKIPPED [1] test.py:26: 不想执行
SKIPPED [1] test.py: 类也可以跳过不执行
==================================================================================================================== 2 passed, 3 skipped in 0.14 seconds =====================================================================================================================
``` {% endraw %}


知识点：

* @pytest.mark.skip 可以加在函数上，类上，类方法上
* 如果加在类上面，类里面的所有测试用例都不会执行

以上小案例都是针对：整个测试用例方法跳过执行，如果想在测试用例执行期间跳过不继续往下执行呢？


## pytest.skip()函数基础使用

作用：在测试用例执行期间强制跳过不再执行剩余内容

类似：在Python的循环里面，满足某些条件则break 跳出循环

示例：

{% raw %}```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

def test_function():
    n = 1
    while True:
        print("这是我第{n}条用例")
        n += 1
        if n == 5:
            pytest.skip("我跑五次了不跑了")
```


执行结果：

```
root@FC-2:~/pytest_framework/src# PYTHONPATH=. pytest --alluredir=../report/test test2.py 
============================================================================================================================ test session starts =============================================================================================================================
platform linux2 -- Python 2.7.12, pytest-4.6.11, py-1.8.1, pluggy-0.13.1 -- /usr/bin/python2.7
cachedir: .pytest_cache
rootdir: /root/pytest_framework/src, inifile: pytest.ini
plugins: cov-2.10.0, progress-1.2.1, allure-pytest-2.8.11, repeat-0.8.0, timeout-1.3.4, ordering-0.6
collected 1 item                                                                                                                                                                                                                                                             

test2.py::test_function SKIPPED                                                                                                                                                                                                                                         [1/1]
________________________________________________________________________________________________ 1 of 1 completed, 0 Pass, 0 Fail, 1 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun ________________________________________________________________________________________________

========================================================================================================================== short test summary info ===========================================================================================================================
SKIPPED [1] /root/pytest_framework/src/test2.py:13: 我跑五次了不跑了
========================================================================================================================= 1 skipped in 0.04 seconds ==========================================================================================================================
root@FC-2:~/pytest_framework/src# 
``` {% endraw %}



## allow_module_level

pytest.skip(msg="", allow_module_level=False)

当 allow_module_level=True 时，可以设置在模块级别跳过整个模块

示例：

{% raw %}```
root@FC-2:~/pytest_framework/src# cat test3.py 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pytest

if sys.platform.startswith("win"):
    pytest.skip("skipping windows-only tests", allow_module_level=True)


@pytest.fixture(autouse=True)
def login():
    print("====登录====")


def test_case01():
    print("我是测试用例11111")
```

执行结果：

```
root@FC-2:~/pytest_framework/src# PYTHONPATH=. pytest --alluredir=../report/test test3.py 
============================================================================================================================ test session starts =============================================================================================================================
platform linux2 -- Python 2.7.12, pytest-4.6.11, py-1.8.1, pluggy-0.13.1 -- /usr/bin/python2.7
cachedir: .pytest_cache
rootdir: /root/pytest_framework/src, inifile: pytest.ini
plugins: cov-2.10.0, progress-1.2.1, allure-pytest-2.8.11, repeat-0.8.0, timeout-1.3.4, ordering-0.6
collected 1 item                                                                                                                                                                                                                                                             

test3.py::test_case01 PASSED                                                                                                                                                                                                                                            [1/1]
________________________________________________________________________________________________ 1 of 1 completed, 1 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun ________________________________________________________________________________________________

========================================================================================================================== 1 passed in 0.06 seconds ==========================================================================================================================
root@FC-2:~/pytest_framework/src# 
``` {% endraw %}


## skipif

@pytest.mark.skipif(condition, reason="")

作用：希望有条件地跳过某些测试用例

注意：condition需要返回True才会跳过


示例：

{% raw %}```
root@FC-2:~/pytest_framework/src# cat test4.py 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pytest

@pytest.mark.skipif(sys.platform == 'win32', reason="does not run on windows")
class TestSkipIf(object):
    def test_function(self):
        print("不能在window上运行")

``` {% endraw %}

执行结果：

{% raw %}```
root@FC-2:~/pytest_framework/src# PYTHONPATH=. pytest --alluredir=../report/test test4.py 
============================================================================================================================ test session starts =============================================================================================================================
platform linux2 -- Python 2.7.12, pytest-4.6.11, py-1.8.1, pluggy-0.13.1 -- /usr/bin/python2.7
cachedir: .pytest_cache
rootdir: /root/pytest_framework/src, inifile: pytest.ini
plugins: cov-2.10.0, progress-1.2.1, allure-pytest-2.8.11, repeat-0.8.0, timeout-1.3.4, ordering-0.6
collected 1 item                                                                                                                                                                                                                                                             

test4.py::TestSkipIf::test_function PASSED                                                                                                                                                                                                                              [1/1]
________________________________________________________________________________________________ 1 of 1 completed, 1 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun ________________________________________________________________________________________________

========================================================================================================================== 1 passed in 0.05 seconds ==========================================================================================================================

``` {% endraw %}


## 跳过标记

可以将 pytest.mark.skip 和 pytest.mark.skipif 赋值给一个标记变量
在不同模块之间共享这个标记变量
若有多个模块的测试用例需要用到相同的 skip 或 skipif ，可以用一个单独的文件去管理这些通用标记，然后适用于整个测试用例集



示例：

{% raw %}```
root@FC-2:~/pytest_framework/src# cat test5.py 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pytest

# 标记
skipmark = pytest.mark.skip(reason="不能在window上运行=====")
skipifmark = pytest.mark.skipif(sys.platform == 'win32', reason="不能在window上运行啦啦啦=====")


@skipmark
class TestSkip_Mark(object):

    @skipifmark
    def test_function(self):
        print("测试标记")

    def test_def(self):
        print("测试标记")


@skipmark
def test_skip():
    print("测试标记")

``` {% endraw %}

执行结果：

{% raw %}```
root@FC-2:~/pytest_framework/src# PYTHONPATH=. pytest --alluredir=../report/test test5.py 
============================================================================================================================ test session starts =============================================================================================================================
platform linux2 -- Python 2.7.12, pytest-4.6.11, py-1.8.1, pluggy-0.13.1 -- /usr/bin/python2.7
cachedir: .pytest_cache
rootdir: /root/pytest_framework/src, inifile: pytest.ini
plugins: cov-2.10.0, progress-1.2.1, allure-pytest-2.8.11, repeat-0.8.0, timeout-1.3.4, ordering-0.6
collected 3 items                                                                                                                                                                                                                                                            

test5.py::TestSkip_Mark::test_function SKIPPED                                                                                                                                                                                                                          [1/3]
________________________________________________________________________________________________ 1 of 3 completed, 0 Pass, 0 Fail, 1 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun ________________________________________________________________________________________________

test5.py::TestSkip_Mark::test_def SKIPPED                                                                                                                                                                                                                               [2/3]
________________________________________________________________________________________________ 2 of 3 completed, 0 Pass, 0 Fail, 2 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun ________________________________________________________________________________________________

test5.py::test_skip SKIPPED                                                                                                                                                                                                                                             [3/3]
________________________________________________________________________________________________ 3 of 3 completed, 0 Pass, 0 Fail, 3 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun ________________________________________________________________________________________________

========================================================================================================================== short test summary info ===========================================================================================================================
SKIPPED [1] test5.py:15: 不能在window上运行=====
SKIPPED [1] test5.py:23: 不能在window上运行=====
SKIPPED [1] test5.py: 不能在window上运行=====
========================================================================================================================= 3 skipped in 0.06 seconds ==========================================================================================================================

``` {% endraw %}


## pytest.importorskip

pytest.importorskip( modname: str, minversion: Optional[str] = None, reason: Optional[str] = None )

作用：如果缺少某些导入，则跳过模块中的所有测试

参数列表

modname：模块名
minversion：版本号
reason：跳过原因，默认不给也行


示例：

{% raw %}```
pexpect = pytest.importorskip("pexpect", minversion="0.3")


@pexpect
def test_import():
    print("test")

``` {% endraw %}

执行结果：

如本版本匹配不是:

{% raw %}```
Skipped: could not import 'pexpect': No module named 'pexpect'
collected 0 items / 1 skipped
``` {% endraw %}


如果版本对应上：

{% raw %}```
如果版本对应不上
Skipped: module 'sys' has __version__ None, required is: '0.3'
collected 0 items / 1 skipped
``` {% endraw %}

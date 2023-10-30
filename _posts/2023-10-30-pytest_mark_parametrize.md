---
layout:     post
title:      "pytest fixture.mark.parametrize"
subtitle:   "pytest fixture.mark.parametrize"
date:       2023-10-30
author:     "Gavin"
catalog:    true
tags:
    - Automation
    - pytest
---






# 概述



pytest中装饰器 <font color='red'>```@pytest.mark.parametrize```</font> 可以实现测试用例参数化，类似DDT。



pytest在几个级别上支持测试参数化：

* pytest.fixture()允许对fixture函数进行参数化
* @pytest.mark.parametrize允许在测试函数或类中定义多组参数和fixture
* pytest_generate_tests允许自定义参数化方案或扩展



语法格式如下：



```
@pytest.mark.parametrize('参数名',list) 
```



- 第一个参数是字符串，多个参数中间用逗号隔开

- 第二个参数是list多组数据用元组类型;传三个或更多参数也是这样传。list的每个元素都是一个元组，元组里的每个元素和按参数顺序 一 一 对应



示例：

- 传一个参数 @pytest.mark.parametrize('参数名'，list) 进行参数化

- 传两个参数@pytest.mark.parametrize('参数名1，参数名2'，[(参数1_data1, 参数2_data1),(参数1_data2, 参数2_data2)]) 进行参数化




详细信息，请继续阅读下文。




# 使用示例





## 只传递一个参数



###  一个参数一个值



示例代码如下：

```text
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


@pytest.mark.parametrize("name", ["Gavin"])
def test_case1(name):
    print("\n" + name)
    assert name.lower() == "gavin"
```



输出结果：

```
C:\Users\Wang>pytest -vrs --show-progress --cache-clear --full-trace C:\Users\Wang\Desktop\test_4.py
================================================= test session starts =================================================
platform win32 -- Python 3.11.4, pytest-7.4.2, pluggy-1.3.0 -- C:\Users\Wang\AppData\Local\Programs\Python\Python311\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Wang
plugins: allure-pytest-2.13.2, order-1.1.0, progress-1.2.5, repeat-0.9.1, timeout-2.1.0
collected 1 item

Desktop/test_4.py::test_case1[Gavin] PASSED                                                                      [100%]
____________________ 1 of 1 completed, 1 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _____________________

================================================== 1 passed in 0.02s ==================================================

C:\Users\Wang>
```





###  一个参数多个值



这种比较常见，示例代码如下：

```text
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import pytest


@pytest.mark.parametrize("name", ["Gavin","Json","Bruce","Andy"])
def test_case1(name):
    print("\n" + name)
    assert name.lower() == "gavin"
```



输出结果：



```
C:\Users\Wang>pytest -vrs --show-progress --cache-clear C:\Users\Wang\Desktop\test_4.py
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.11.4, pytest-7.4.2, pluggy-1.3.0 -- C:\Users\Wang\AppData\Local\Programs\Python\Python311\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Wang
plugins: allure-pytest-2.13.2, order-1.1.0, progress-1.2.5, repeat-0.9.1, timeout-2.1.0
collected 4 items

Desktop/test_4.py::test_case1[Gavin] PASSED                                                                                                                                                               [ 25%]
_________________________________________________________________ 1 of 4 completed, 1 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

Desktop/test_4.py::test_case1[Json] FAILED                                                                                                                                                                [ 50%]
_______________________________________________________________________________________________ test_case1[Json] _______________________________________________________________________________________________

name = 'Json'

    @pytest.mark.parametrize("name", ["Gavin","Json","Bruce","Andy"])
    def test_case1(name):
        print("\n" + name)
>       assert name.lower() == "gavin"
E       AssertionError: assert 'json' == 'gavin'
E         - gavin
E         + json

Desktop\test_4.py:10: AssertionError
--------------------------------------------------------------------------------------------- Captured stdout call ---------------------------------------------------------------------------------------------

Json
_________________________________________________________________ 2 of 4 completed, 1 Pass, 1 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

Desktop/test_4.py::test_case1[Bruce] FAILED                                                                                                                                                               [ 75%]
______________________________________________________________________________________________ test_case1[Bruce] _______________________________________________________________________________________________

name = 'Bruce'

    @pytest.mark.parametrize("name", ["Gavin","Json","Bruce","Andy"])
    def test_case1(name):
        print("\n" + name)
>       assert name.lower() == "gavin"
E       AssertionError: assert 'bruce' == 'gavin'
E         - gavin
E         + bruce

Desktop\test_4.py:10: AssertionError
--------------------------------------------------------------------------------------------- Captured stdout call ---------------------------------------------------------------------------------------------

Bruce
_________________________________________________________________ 3 of 4 completed, 1 Pass, 2 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

Desktop/test_4.py::test_case1[Andy] FAILED                                                                                                                                                                [100%]
_______________________________________________________________________________________________ test_case1[Andy] _______________________________________________________________________________________________

name = 'Andy'

    @pytest.mark.parametrize("name", ["Gavin","Json","Bruce","Andy"])
    def test_case1(name):
        print("\n" + name)
>       assert name.lower() == "gavin"
E       AssertionError: assert 'andy' == 'gavin'
E         - gavin
E         + andy

Desktop\test_4.py:10: AssertionError
--------------------------------------------------------------------------------------------- Captured stdout call ---------------------------------------------------------------------------------------------

Andy
_________________________________________________________________ 4 of 4 completed, 1 Pass, 3 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

========================================================================================= 3 failed, 1 passed in 0.06s ==========================================================================================

C:\Users\Wang>
```







## 多个参数



### 多个参数多个值



下面是官网的示例：



```
# content of test_expectation.py
import pytest


@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```



此示例，参考官网给出的另外一个方案：

```https://docs.pytest.org/en/stable/how-to/parametrize.html ``` 下 “To parametrize all tests in a module, you can assign to the [`pytestmark`](https://docs.pytest.org/en/stable/reference/reference.html#globalvar-pytestmark) global variable:”

```
import pytest

pytestmark = pytest.mark.parametrize("test_input, expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])


def test_eval(test_input, expected):
    assert eval(test_input) == expected
```




输出结果：



```
C:\Users\Wang>pytest -vrs --show-progress --cache-clear C:\Users\Wang\Desktop\test_expectation.py
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.11.4, pytest-7.4.2, pluggy-1.3.0 -- C:\Users\Wang\AppData\Local\Programs\Python\Python311\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Wang
plugins: allure-pytest-2.13.2, order-1.1.0, progress-1.2.5, repeat-0.9.1, timeout-2.1.0
collected 3 items

Desktop/test_expectation.py::test_eval[3+5-8] PASSED                                                                                                                                                      [ 33%]
_________________________________________________________________ 1 of 3 completed, 1 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

Desktop/test_expectation.py::test_eval[2+4-6] PASSED                                                                                                                                                      [ 66%]
_________________________________________________________________ 2 of 3 completed, 2 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

Desktop/test_expectation.py::test_eval[6*9-42] FAILED                                                                                                                                                     [100%]
______________________________________________________________________________________________ test_eval[6*9-42] _______________________________________________________________________________________________

test_input = '6*9', expected = 42

    @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
    def test_eval(test_input, expected):
>       assert eval(test_input) == expected
E       AssertionError: assert 54 == 42
E        +  where 54 = eval('6*9')

Desktop\test_expectation.py:7: AssertionError
_________________________________________________________________ 3 of 3 completed, 2 Pass, 1 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

========================================================================================= 1 failed, 2 passed in 0.03s ==========================================================================================

C:\Users\Wang>
```





### 多个参数的混合使用

示例代码如下（在官方示例代码上做了调整）：



```text
import pytest


@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_foo(x, y):
    print("Generate new combinations : {},{}".format(x, y))
```



上面示例会产生4个测试用例，输出结果参考如下：



```
C:\Users\Wang>pytest -vrs --show-progress --cache-clear C:\Users\Wang\Desktop\test_5.py
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.11.4, pytest-7.4.2, pluggy-1.3.0 -- C:\Users\Wang\AppData\Local\Programs\Python\Python311\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Wang
plugins: allure-pytest-2.13.2, order-1.1.0, progress-1.2.5, repeat-0.9.1, timeout-2.1.0
collected 4 items

Desktop/test_5.py::test_foo[2-0] PASSED                                                                                                                                                                   [ 25%]
_________________________________________________________________ 1 of 4 completed, 1 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

Desktop/test_5.py::test_foo[2-1] PASSED                                                                                                                                                                   [ 50%]
_________________________________________________________________ 2 of 4 completed, 2 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

Desktop/test_5.py::test_foo[3-0] PASSED                                                                                                                                                                   [ 75%]
_________________________________________________________________ 3 of 4 completed, 3 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

Desktop/test_5.py::test_foo[3-1] PASSED                                                                                                                                                                   [100%]
_________________________________________________________________ 4 of 4 completed, 4 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

============================================================================================== 4 passed in 0.02s ===============================================================================================

C:\Users\Wang>
```



再看个示例：



```
data1 = [1, 2]
data2 = ["python", "Shell"]
data3 = ["Software", "Test", Engineer", "from", "Gavin"]


@pytest.mark.parametrize("a", data1)
@pytest.mark.parametrize("b", data2)
@pytest.mark.parametrize("c", data3)
def test_case3(a, b, c):
    print("[{a} {b} {c}]")
```



如上示例，会产生20个测试用例。





## 参数化





### 传入字典数据



示例代码：



```
import pytest


json=({"username":"Json","password":"Python@123!"},{"username":"Alex","password":"226699"},{"username":"Rita","password":"123456"})

@pytest.mark.parametrize('json', json)
def test_pytest_parametrize(json):
    print(f'dit : \n{json}')
    print(f'username : {json["username"]}, password : {json["password"]}')
```



输出结果：



```
C:\Users\Wang>pytest -vs --show-progress --cache-clear C:\Users\Wang\Desktop\test_pytest_parameter.py
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.11.4, pytest-7.4.2, pluggy-1.3.0 -- C:\Users\Wang\AppData\Local\Programs\Python\Python311\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Wang
plugins: allure-pytest-2.13.2, order-1.1.0, progress-1.2.5, repeat-0.9.1, timeout-2.1.0
collected 3 items

Desktop/test_pytest_parameter.py::test_pytest_parametrize[json0] dit :
{'username': 'Json', 'password': 'Python@123!'}
username : Json, password : Python@123!
PASSED
_________________________________________________________________ 1 of 3 completed, 1 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

Desktop/test_pytest_parameter.py::test_pytest_parametrize[json1] dit :
{'username': 'Alex', 'password': '226699'}
username : Alex, password : 226699
PASSED
_________________________________________________________________ 2 of 3 completed, 2 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

Desktop/test_pytest_parameter.py::test_pytest_parametrize[json2] dit :
{'username': 'Rita', 'password': '123456'}
username : Rita, password : 123456
PASSED
_________________________________________________________________ 3 of 3 completed, 3 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

============================================================================================== 3 passed in 0.02s ===============================================================================================

C:\Users\Wang>
```





### 集合标记



示例代码：



```
import pytest


@pytest.mark.parametrize("username,password",
                         [("Json", "123456"), ("Jack", "654321"),
                          pytest.param("Bruce", "123456", marks=pytest.mark.xfail),
                          pytest.param("Alex", "123456", marks=pytest.mark.skip)])
def test_login(username, password):
    print(username + " : " + password)
    assert username == "Jack"
```





输出结果：



```
C:\Users\Wang>pytest -vs --show-progress --cache-clear C:\Users\Wang\Desktop\test_multi_parameter.py
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.11.4, pytest-7.4.2, pluggy-1.3.0 -- C:\Users\Wang\AppData\Local\Programs\Python\Python311\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Wang
plugins: allure-pytest-2.13.2, order-1.1.0, progress-1.2.5, repeat-0.9.1, timeout-2.1.0
collected 4 items

Desktop/test_multi_parameter.py::test_login[Json-123456] Json : 123456
FAILED
___________________________________________________________________________________________ test_login[Json-123456] ____________________________________________________________________________________________

username = 'Json', password = '123456'

    @pytest.mark.parametrize("username,password",
                             [("Json", "123456"), ("Jack", "654321"),
                              pytest.param("Bruce", "123456", marks=pytest.mark.xfail),
                              pytest.param("Alex", "123456", marks=pytest.mark.skip)])
    def test_login(username, password):
        print(username + " : " + password)
>       assert username == "Jack"
E       AssertionError: assert 'Json' == 'Jack'
E         - Jack
E         + Json

Desktop\test_multi_parameter.py:10: AssertionError
_________________________________________________________________ 1 of 4 completed, 0 Pass, 1 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

Desktop/test_multi_parameter.py::test_login[Jack-654321] Jack : 654321
PASSED
_________________________________________________________________ 2 of 4 completed, 1 Pass, 1 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _________________________________________________________________

Desktop/test_multi_parameter.py::test_login[Bruce-123456] Bruce : 123456
XFAIL
_________________________________________________________________ 3 of 4 completed, 1 Pass, 1 Fail, 0 Skip, 0 XPass, 1 XFail, 0 Error, 0 ReRun _________________________________________________________________

Desktop/test_multi_parameter.py::test_login[Alex-123456] SKIPPED (unconditional skip)
_________________________________________________________________ 4 of 4 completed, 1 Pass, 1 Fail, 1 Skip, 0 XPass, 1 XFail, 0 Error, 0 ReRun _________________________________________________________________

=========================================================================================== short test summary info ============================================================================================
FAILED Desktop/test_multi_parameter.py::test_login[Json-123456] - AssertionError: assert 'Json' == 'Jack'
============================================================================== 1 failed, 1 passed, 1 skipped, 1 xfailed in 0.05s ===============================================================================

C:\Users\Wang>
```





# 项目实践





如下为在产品测试中使用到的 parameter 实战示例：



```
    @pytest.mark.parametrize('object_quota',
                             [-1, 0, 1, 1000, 1000000, 1000000000, 1000000000000, 1000000000000000, 1000000000000000000,
                              7168000000000000000])
    @pytest.mark.parametrize('size_quota',
                             [-1,0, 1024, 1048576, 1073741824, 1099511627776, 1125899906842624, 8070450532247928832])
    #@pytest.mark.parametrize('object_quota', [-1, 1])
    #@pytest.mark.parametrize('size_quota',[-1])
    def test_8_0_10647(self, object_quota, size_quota):
        logger.info("8_0-10647:Set value on User Max Size, User Max Objects, Bucket Max Size, Bucket Max Objects fielAccount Quota")
        TestClass.AccountCount = TestClass.AccountCount + 1
        account = "test_8_0_10604_" + str(self.rand_num) + "_" + str(TestClass.AccountCount)
        logger.info("Account: %s", account)
        self.cluster_api.Create_Account(account)
        self.radows.Set_Account_Quota(account, object_quota, size_quota)
        self.radows.Set_Account_Bucket_Quota(account, object_quota, size_quota)
        self.check_cluster_api.Check_Account_Quota(account, object_quota, size_quota)
```



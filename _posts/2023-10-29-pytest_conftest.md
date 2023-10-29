---
layout:     post
title:      "pytest 之 conftest.py"
subtitle:   "pytest of conftest.py"
date:       2023-10-29
author:     "Gavin"
catalog:    true
tags:
    - Automation
    - pytest
---


# 概述



`conftest.py`文件是pytest框架里面一个很重要的东西，它可以在这个文件里面编写fixture函数，这个fixture函数的作用，就相当于Unittest框架里面的`setup()`前置函数和`teardown()`后置函数，虽然pytest框架也有`setup()`前置函数和`teardown()`后置函数，但是在实际工作中没必要写在测试用例文件中，直接写在`conftests.py`里面就好了，pytest框架会自动去找`conftest.py`文件里面的东西，这样更灵活。



可以看出 conftest.py是 fixture函数的一个集合， 提取公共部分放在这个文件里，然后供其它模块调用。不同于普通被调用的模块，conftest.py使用时不需要导入，pytest会自动查找。



在实际工作中，通常`conftest.py`和`@pytest.fixture()`结合使用，实现全局的前后置应用。



# conftest.py使用场景



* 每个接口用例需共用到的token/session/cookie
* 每个接口用例需共用到的测试用例数据
* 每个接口用例需共用到的配置信息

​    ....

简而言之：

​    多个py文件使用同一个前/后置函数，一个fixture函数，在很多case模块中都要用到。



# conftest.py中fixture的作用域

 fixture的scope参数也适用`conftest.py`文件中fixture的特性，即有如下范围：



| 取值     | 范围     | 说明                                                         |
| -------- | -------- | ------------------------------------------------------------ |
| function | 函数级   | 每个函数或方法都会调用                                       |
| class    | 类级别   | 每个测试类只运行一次                                         |
| module   | 模块级别 | 每一个.py文件只调用一次                                      |
| package  | 包级     | 每一个python包只调用一次                                     |
| session  | 会话级   | 每次会话只需要运行一次，会话内所有方法及类、模块都共享这个方法 |



## 不同位置conftest.py文件的优先级

**其作用范围是当前目录包括子目录里的测试模块。**

- 比如在测试框架的根目录创建`conftest.py`文件，文件中的fixture的作用范围是所有测试模块
-  比如在某个单独的测试文件夹里创建`conftest.py`文件，文件中fixture的作用范围，就仅局限于该测试文件夹里的测试模块；该测试文件夹外的测试模块，或者该测试文件夹外的测试文件夹，是无法调用到这个`conftest.py`文件中的fixture。
- 如果测试框架的根目录和子包中都有`conftest.py`文件，并且这两个`conftest.py`文件中都有一个同名的fixture，实际生效的是测试框架中子包目录下的`conftest.py`文件中配置的fixture（即此场景下子目录下的conftest.py会覆盖父目录的conftest.py）



# 示例



代码目录结构：



```
root@Gavin:~/src# tree
.
├── clear_pyc.py
├── conftest.py
├── __init__.py
├── pytest.ini
└── testcase
    ├── account
    │   ├── conftest.py
    │   ├── __init__.py
    │   └── test_account.py
    ├── __init__.py
    └── ldap
        ├── __init__.py
        └── test_ldap.py

3 directories, 10 files
root@Gavin:~/src# 
```



两个conftest.py内容参考如下：



```
root@Gavin:~/src# cat conftest.py 
import os
import pytest
import logging


@pytest.fixture(scope='package', autouse=True)
def testsuite_setup_teardown():
    logging.info('------------------------------------- Start to run test case ---------------------------------\n')
    yield
    logging.info('------------------------------------- End to run test case -----------------------------------')


@pytest.fixture(scope='function', autouse=True)
def testcase_setup_teardown():
    case_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]

    logging.info('----------------------------------- Begin ----------------------------------------')
    logging.info('Current test case name : (%s)', case_name)
    yield
    logging.info('----------------------------------- End ------------------------------------------\n')
root@Gavin:~/src# cat testcase/account/conftest.py 
import pytest
import logging


@pytest.fixture(scope='function', autouse="true")
def testsuit_env_check():
    logging.info('----------- [testsuit_env_check] Begin ------------')

    logging.info('--------------- [testsuit_env_check] End ----------------\n')

root@Gavin:~/src# 
```





执行用例记录的日志：



```
root@Gavin:~/src# cat ../report/pytest_autotest.log 
2023-10-30 06:50:48 [conftest.py:8   ] [ INFO] ------------------------------------- Start to run test case ---------------------------------

2023-10-30 06:50:48 [conftest.py:17  ] [ INFO] ----------------------------------- Begin ----------------------------------------
2023-10-30 06:50:48 [conftest.py:18  ] [ INFO] Current test case name : (test_account_01)
2023-10-30 06:50:48 [conftest.py:7   ] [ INFO] ----------- [testsuit_env_check] Begin ------------
2023-10-30 06:50:48 [conftest.py:9   ] [ INFO] --------------- [testsuit_env_check] End ----------------

2023-10-30 06:50:48 [conftest.py:20  ] [ INFO] ----------------------------------- End ------------------------------------------

2023-10-30 06:50:48 [conftest.py:17  ] [ INFO] ----------------------------------- Begin ----------------------------------------
2023-10-30 06:50:48 [conftest.py:18  ] [ INFO] Current test case name : (test_account_02)
2023-10-30 06:50:48 [conftest.py:7   ] [ INFO] ----------- [testsuit_env_check] Begin ------------
2023-10-30 06:50:48 [conftest.py:9   ] [ INFO] --------------- [testsuit_env_check] End ----------------

2023-10-30 06:50:48 [conftest.py:20  ] [ INFO] ----------------------------------- End ------------------------------------------

2023-10-30 06:50:48 [conftest.py:17  ] [ INFO] ----------------------------------- Begin ----------------------------------------
2023-10-30 06:50:48 [conftest.py:18  ] [ INFO] Current test case name : (test_ldap_01)
2023-10-30 06:50:48 [conftest.py:20  ] [ INFO] ----------------------------------- End ------------------------------------------

2023-10-30 06:50:48 [conftest.py:17  ] [ INFO] ----------------------------------- Begin ----------------------------------------
2023-10-30 06:50:48 [conftest.py:18  ] [ INFO] Current test case name : (test_ldap_02)
2023-10-30 06:50:48 [conftest.py:20  ] [ INFO] ----------------------------------- End ------------------------------------------

2023-10-30 06:50:48 [conftest.py:10  ] [ INFO] ------------------------------------- End to run test case -----------------------------------
root@Gavin:~/src#
```



从测试log看：

<img class="shadow" src="/img/in-post/conftest_scope.png" width="400" />


# 结语


* conftest.py文件名字是固定的，不能做任何修改，把hook或者fixture写在这个文件里，就会自动去调用
* 文件和用例文件在同一个目录下，那么conftest.py作用于整个目录，即所有同目录测试文件运行前都会执行conftest.py文件
* conftest.py文件不能被其他文件导入
* pytest框架中的`setup()/teardown()`函数，`setup_class()/teardown_class()`函数，他们是作用于所有用例或者所有类的
* `@pytest.fixtrue()`的作用域是既可以部分用例，也可以全部用例的前后置
* `conftest.py`文件和`@pytest.fxtrue()`装饰器结合使用，作用于全局用例的前后置



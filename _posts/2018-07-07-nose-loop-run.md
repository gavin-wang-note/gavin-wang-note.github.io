---
layout:     post
title:      "nose测试用例可指定循环次数"
subtitle:   "loop run nose test case"
date:       2018-07-09
author:     "Gavin Wang"
catalog:    true
categories:
    - [Automation]
    - [nose]
tags:
    - nose
    - Automation
---


# 前言

编写nose 自动化测试用例时，有些场景需要重复循环运行，才有可能踩到Bug，为了让nose 用例能够支持循环运行，特意写了一个装饰器，能够指定nose测试用例的循环次数。



# 代码

```python
def loop_run():
    """  
    loop run a test case
    """
    from testconfig import config as cf

    def wrap(func):
        """
        :param func, string, a function name
        """
        @wraps(func)
        def wrapper(object):
            """
            :param object, object, a object name
            """
            for num in xrange(int(cf.get('runs', 1))):
                logging.info("[loop run] The current number of loop operations is: (%s), "
                             "test case name is : (%s)", num+1, func.func_name)
                func(object)

        return wrapper
    return wrap
```

# 测试用例示例

```python
    @loop_run()
    def test_435_create_enable_folder(self):
        """  Sc-435:Enable share folder  """
        folder_name = 'nose-' + rand_low_ascii(6)
        self.create_share_folder(folder_name, nfs='true', smb='true', op_type='add')
        self.disable_folder(folder_name, nfs='true', smb='true', op_type='disable')
        self.enable_folder(folder_name, nfs='true', smb='true', op_type='enable')
        self.delete_folder(folder_name, op_type='del')
```

# 用例执行示例

```shell
root@nose-70-97:/home/nose_framework/src# nosetests -v --with-progressive --with-html --html-report=../report/nas.html testcase/Function_Test/case_4_Virtual_Storages/NAS/ --tc=runs:10
```

说明：

* 这里的loop_run就是执行10次，即```testcase/Function_Test/case_4_Virtual_Storages/NAS/ ```目录下的所有测试用例，都会被执行10次
* loop_run 函数，需要配合nose的nose-testconfig使用

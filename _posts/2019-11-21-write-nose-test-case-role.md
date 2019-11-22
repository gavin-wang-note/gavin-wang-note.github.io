---
layout:     post
title:      "Nose测试用例编写规则基本要求"
subtitle:   "nose wirte test case rule"
date:       2019-11-21
author:     "Gavin"
catalog:    true
tags:
    - Automation
    - nose
---

## **用例编写基本规则要求**

### 1、test_xxxx.py尽量避免逻辑操作，纯粹是function的调用

 

### 2、测试用例的名称，携带上TestLink对应测试用例的编号

例如：

​       ![image-20191121102705635](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20191121102705635.png)

test_9143_same_daemon_different_signal， 对应TestLink的用例为：

Sc-9143:Same daemon, different signal core file，详见本章节4)

 

### 3、测试用例的__doc__，不得含有中文字符

例如：

​    """ Sc-9143:Same daemon，different signal core file """

这里的逗号，是中文符号，会导致用例报错：

  ![image-20191121102713516](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20191121102713516.png)

 

### 4、避免测试用例之间存在依赖关系

（1）每个测试suite中的测试用例互相不依赖；

（2）测试suite中的用例，尽可能避免依赖关系

如TestLink中上一个用例是创建，下一个用例是删除，则合并这两个用例为一个自动化测试用例。

 

### 5、日志记录对齐要求

日志记录，执行动作的记录，开头增加[Action]；检查动作的记录，开头增加[Check];

断言记录的log，开头增加[ERROR]； 操作成功的log，开头增加[SUCCESS]； 不需要检查点的，开头增加[Skip]；

具体要求如下：

**[Prepare]** **后面跟2****个空格；**

**[Action]** **后面跟3****个空格**

**[Start]** **后面跟4****个空格**

**[Check]** **后面跟4****个空格**

**[Success]** **后面跟2****个空格**

**[Skip]** **后面跟5****个空格**

**debug****级别的log****，内容前面跟2****个-****，之后** **再加2****个空格**

**assert****中，[ERROR]** **后面跟2****个空格**

 

### 6、用例的执行顺序

 执行 nosetests -s 可看到调用顺序，用例执行顺序，根据ASSII进行排序，在用例有关联情况下，需要对用例名称增加数字编号，人为的干预用例执行顺序，比如test_1_xxx, test_2_yyy。

 

### 7、代码规范要求

执行pylint，确保检查结果分值=10

```
pylint -r y testcasebase/Virtual_Storage/vs_user.py --rcfile=./pylintrc
```

 

MESSAGE_TYPE 有如下几种：

* (C) 惯例。违反了编码风格标准
* (R) 重构。写得非常糟糕的代码。
* (W) 警告。某些 Python 特定的问题。
* (E) 错误。很可能是代码中的错误。
* (F) 致命错误。阻止 Pylint 进一步运行的错误

 

### 8、用例文件权限

**统一使用644****权限**，否则默认情况下无法被nosetests search到，自然就不会被执行到，因为nosetesst默认只查找644权限的文件。

 

### 9、避免在class与setup_class之间做比较重的动作

比如下文中的RRS用例 test_remote_replication_tasks.py（下文代码是一个不可取的代码，这里仅做示例用）

  ![image-20191121102829783](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20191121102829783.png)

 在class TestReplicationTask 与setup_class之间，启用了RRS服务、创建了S3账号并创建bucket，最后上传了一些object到bucket中。正常情况下，这部分动作应该是在用例被执行之前要做的，然后会立刻执行setup_class中的动作，接着执行用例，最后teardown。实际上，在run.py 去执行所有测试用例的时候， 在init完所有的class之后（即创建完session后），会先执行所有test_xx.py中定义在class 与 setup_class之间的所有动作， 这也无可厚非，但是，由于约束了用例的执行顺序，case_2_Accounts 会优先于 case_5_Remote_DR被执行，而case_2_Accounts里将其他pool设置为S3 pool的动作，这势必会清理掉在执行run.py init结束后所创建的所有bucket与bucket下的object，到case_5_Remote_DR被执行时，曾经创建的bucket与bucket下的object早已不复存在，自然case_5_Remote_DR下面的相关用例就会失败。

故而，建议：

  避免在class与setup_class之间做比较重的动作。对于较重的动作，放在setup_class中，好处有2：

（1）避免被其他class import时做更多、更重的动作

（2）避免用例suite间前后有依赖关系，给用例排查带来难度

 

### 10、用例文件名称、用例中定义变量名称全局唯一

  对于测试用例中定义的变量，诸如文件夹名称、子目录名称、名称、名称、名称、名称、用例执行过程中产生的文件的名称等等，要保持全局唯一，即所有用例中不出现同名的文件名、目录名、名等。当有用例出错时，可以根据这个名称，定位到是哪个用例产生了问题，因为具有唯一性，可以排除其他用例带来的干扰。

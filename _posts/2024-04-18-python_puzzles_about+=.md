---
layout:     post
title:      "关于+=的谜题"
subtitle:   "关于+=的谜题"
date:       2024-04-18
author:     "Gavin Wang"
catalog:    true
img: "/medias/featureimages/172.jpg"
summary: 关于+=的谜题
categories:
    - [python]
tags:
    - python
---


# 关于+=的谜题

代码示例如下：

```python
>>> t = (1,2, [30, 40])
>>> t[2] += [40, 50]
```


到底会发生下面 4 种情况中的哪一种？
* A. t 变成 (1, 2, [30, 40, 50, 60])。
* B. 因为 tuple 不支持对它的元素赋值，所以会抛出 TypeError 异常。
* C. 以上两个都不是。
* D. A 和 B 都是对的。


先不要在控制台运行上面的代码，思考一下，答案会是哪个？

--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------

答案是D，是不是有些出乎意料？

我们来看一下控制台运行效果：

```shell
>>> t = (1,2, [30, 40])
>>> t[2]
[30, 40]
>>> t[2] += [40, 50]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> t
(1, 2, [30, 40, 40, 50])
>>> 
```

查看字节码信息：

```python
>>> t = (1,2, [30, 40])
>>> import dis
>>> dis.dis('t')
  0           0 RESUME                   0

  1           2 LOAD_NAME                0 (t)
              4 RETURN_VALUE
>>> t[2] += [40, 50]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> dis.dis('t[2] += [40, 50]')
  0           0 RESUME                   0

  1           2 LOAD_NAME                0 (t)
              4 LOAD_CONST               0 (2)
              6 COPY                     2
              8 COPY                     2
             10 BINARY_SUBSCR
             20 LOAD_CONST               1 (40)
             22 LOAD_CONST               2 (50)
             24 BUILD_LIST               2
             26 BINARY_OP               13 (+=)
             30 SWAP                     3
             32 SWAP                     2
             34 STORE_SUBSCR
             38 LOAD_CONST               3 (None)
             40 RETURN_VALUE
>>>
```

`https://pythontutor.com/`展示上述代码效果：

<img class="shadow" src="/img/in-post/谜题-1.png" width="600">
<img class="shadow" src="/img/in-post/谜题-2.png" width="600">

至此得到的教训：
* 不要把可变对象放在元组里面
* 增量赋值不是一个原子操作，上述示例虽然抛出了异常，但还是完成了操作
* 查看 Python 的字节码并不难，而且它对我们了解代码背后的运行机制很有帮助。
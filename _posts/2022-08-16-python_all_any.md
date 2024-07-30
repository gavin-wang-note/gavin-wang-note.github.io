---
layout:     post
title:      "python any() 与 all() 函数介绍"
subtitle:   "python any() & all()"
date:       2022-08-16
author:     "Gavin Wang"
catalog:    true
categories:
    - [python]
tags:
    - python
---




# 概述


最近碰到python的一个知识点盲区（any 与 all 函数相关），基础知识没有扎实，这里记录一下python的any 与 all 函数，填补一下部分盲区。





# 简单理解



all() 函数： 全部为真，一假为假

any() 函数：一真为真，全假为假


# for循环的any()函数

使用生成器表达式动态地创建一个迭代，并将其传递到 any() 函数中。这可以称为 “带有for循环的any()函数”。


```python
>>> print(any(x**2 == 16 for x in range(10)))
True
>>>
```

上面举例代码使用的条件是x**2==16，它只对x=4有效。

当通过使用range()函数将这个表达式应用于从0到9（包括）的所有x值时，它大多返回False。由于短路，any()函数在评估第五个元素x=4后返回True。


# all() 函数



## 描述



all() 函数用于判断给定的可迭代参数iterable中的所有元素是否都为True，如果是则返回True，否则返回False。

元素除了0，空，None，False外，都算True。



## 语法



```python
all(iterable)
```





## 返回值



如果iterable的所有元素不为 0,, '', False或者iterable为空，all(iterable) 返回True，否则返回False。



**注意：**

​    空元组，空列表返回True，这里需要特别注意。



## 示例



```python
>>> all(['a', 'b', 'c'])   # 列表list，元素都不为空或0
True
>>> all(['a', 'b', ''])    # 列表list，存在一个为空的元素
False
>>> all([0,1,2,3])         # 列表list，存在一个为0的元素
False
>>> all(('a', 'b', ''))    # 元组tuple，存在一个为空的元素
False
>>> all(('a', 'b', 'c'))   # 元组tuple，元素不存在为空或0的元素
True
>>> all((0,1,2,3))         # 元组tuple，元素存在一个为0的元素
False
>>> all([])                # 空列表list
True
>>> all(())                # 空元组tuple
True
>>>
```







# any() 函数



## 描述



any() 函数用于判断给定的可迭代参数iterable是否全部为false，则返回False；如果有一个为True，则返回True。





## 语法



```python
any(iterable)
```





## 返回值



如果都为空，0， false，则返回False；如果不都为空，0，False，则返回True。





## 示例



```python
>>> any((['a', 'b', 'c']))     # 列表list，元素都不为空或0
True
>>> any((['a', 'b', '']))      # 列表list，存在一个为空的元素
True
>>> any([0, '', False])        # 列表list，全部为0， ''， False
False
>>> any((('a', 'b', 'c')))     # 元组tuple，元素都不为空或0
True
>>> any((('a', 'b', '')))      # 元组tuple，存在一个为空的元素
True
>>> any((0, '', False))        # 元组tuple，全部为0， ''， False
False
>>> any([])                    # 空列表list 
False
>>> any(())                    # 空元组tuple
False
>>>
```



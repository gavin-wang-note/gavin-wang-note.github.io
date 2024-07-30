---
layout:     post
title:      "python max 函数介绍"
subtitle:   "python max function"
date:       2022-08-22
author:     "Gavin Wang"
catalog:    true
categories:
    - [python]
tags:
    - python
---


# Overview


max()函数用于获得给定的可迭代对象中的最大值。

key是max()函数的一个参数，它辅助max函数找到最大元素。当max() 函数中有 key 参数时，求的是 value 的最大值，当没有 key 参数时，求的是 key 的最大值。

key可以对要比较的对象进行一些处理，以达到对对象进行特定规则的比较。

要在比较之前修改对象，或基于特定的属性/索引进行比较，必须使用key参数。

语法如下：

```shell
root@scaler80:~# python
Python 2.7.12 (default, Mar  1 2021, 11:38:31) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> help(max)
Help on built-in function max in module __builtin__:

max(...)
    max(iterable[, key=func]) -> value
    max(a, b, c, ...[, key=func]) -> value
    
    With a single iterable argument, return its largest item.
    With two or more arguments, return the largest argument.
(END)
```

# Common example

获取list中最大值(元祖类似)

```python
>>> max([1,2,3,6,10,60])
60
```

获取字典中key的最大值

```python
dict1 = {'a': '11', 'c': '22', 'b': '33'}
print(max(dict1))
print(max(dict1.keys()))
```


获取字典中最大value对应的key值

```python
dict1 = {'a': '11', 'c': '22', 'b': '33'}
print(max(dict1, key=dict1.get))
print(max(dict1, key=lambda x: dict1[x]))
```


获取字典中最大value的值

```python
dict1 = {'a': '11', 'c': '22', 'b': '33'}
print(max(dict1.values()))
```


获取句子中的最长单词

```python
str3 = "Life is short , I use python"
print(str3.split())
print(max(str3.split(), key=len))
```


获取list中的最大值

```python
list1 = ['11', 'zzz', '22', 'eee']
print(max(list1))
```


获取list中的最大数值

```python
list2 = ['11', '3', '222', '67']
print(max(list2, key=lambda x: int(x)))
```


获取list中的绝对值最大的值

```python
list3 = ['11', '-399', '222', '67']
print(max(list2, key=lambda x: abs(int(x))))
```


获取元组list中指定索引的最大值

```python
list4 = [(1, 'a'), (3, 'c'), (4, 'e'), (-1, 'z')]
print(max(list4, key=lambda x: x[1]))
```


# Other Code example

```python
#!/usr/bin/env python
#-*-coding:UTF-8 -*-

import os
import sys
import glob


def check_path_exist_or_not(path):
    """
    Check the path exist or not, if not exist, exit
    :param path, string, a folder path
    """
    if not os.path.exists(path):
        print('[ERROR]  Has no path : ({}), exit!!!'.format(path))
        sys.exit(1)


def get_latest_file(path, file_prefix_suffix):
    """
    Get the latest file from mtime
    If match, return a list of file full path; else return []
    :param path, string, which folde's file to get the latest file
    :param file_prefix_suffix string, file's name or prefix or suffix, such as *.iso, or 20230819*
    """
    check_path_exist_or_not(path)

    search_path = path + os.sep + file_prefix_suffix
    list_of_files = glob.glob(search_path)

    return max(list_of_files, key=os.path.getmtime)


def get_latest_folder(path):
    """
        Get the latest file from mtime
        If match, return a list of file full path; else return []
        args:
            - path  Which folde's file to get the latest file
    """
    check_path_exist_or_not(path)

    all_subdirs = [path + os.sep + d for d in os.listdir(path) if os.path.isdir(path + os.sep + d)]
    if len(all_subdirs):
        latest_subdir = max(all_subdirs, key=os.path.getmtime)
        return latest_subdir

if __name_ == '__main__':
    path = "/home/btadmin/image"
    print get_latest_folder(path)
```

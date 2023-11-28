---
layout:     post
title:      "python debug with pysnooper/snoop"
subtitle:   "python debug with pysnooper/snoop"
date:       2021-05-02
author:     "Gavin"
catalog:    true
tags:
    - python
---


# 概述

python代码调测，早期的时候更多的是使用print加日志的方式，后期使用pdb，今天发现了个更好的调试工具 pysnooper 和 snoop.


# 实践

## 安装 pysnooper

``` pip install pysnooper ```

## 利用pysnooper调试


示例代码


```
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pysnooper


@pysnooper.snoop()
def remove_dup_element(a_list):
    return {}.fromkeys(a_list).keys()


if __name__ == '__main__':
    a_list = [10, 9, 1, 2, 2, 3, 3, 5, 6, 6, 7, 7, 8, 9]
    remove_dup_element(a_list)
```


输出结果：

```
root@wyz-node1:~# python test_pysnooper.py
Source path:... test_pysnooper.py
Starting var:.. a_list = [10, 9, 1, 2, 2, 3, 3, 5, 6, 6, 7, 7, 8, 9]
14:30:22.540068 call         8 def remove_dup_element(a_list):
14:30:22.540068 line         9     return {}.fromkeys(a_list).keys()
14:30:22.540068 return       9     return {}.fromkeys(a_list).keys()
Return value:.. dict_keys([10, 9, 1, 2, 3, 5, 6, 7, 8])
Elapsed time: 00:00:00.000000
```

它将每一行变量的值都输出到屏幕上，仅仅需要写一行代码（使用装饰器）就可以实现这个方便的调试功能，比起一行行写print，方便了很多。



如果代码执行过程比较长，输出到屏蔽不方便的话，可以输出到log文件中，在装饰器那行加上log文件路径即可：

```
@pysnooper.snoop('/log/output.log')
def remove_dup_element(a_list):
    return {}.fromkeys(a_list).keys()
```

## 安装 snoop

``` pip install snoop ```

## 利用snoop调试


示例代码：

```
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import snoop


@snoop
def remove_dup_element(a_list):
    return {}.fromkeys(a_list).keys()


if __name__ == '__main__':
    a_list = [10, 9, 1, 2, 2, 3, 3, 5, 6, 6, 7, 7, 8, 9]
    remove_dup_element(a_list)
```


输出结果：


```
root@wyz-node1:~# python test_snoop.py
14:35:52.40 >>> Call to remove_dup_element in File "test_snoop.py", line 8
14:35:52.40 ...... a_list = [10, 9, 1, 2, 2, 3, 3, 5, 6, 6, 7, 7, 8, 9]
14:35:52.40 ...... len(a_list) = 14
14:35:52.40    8 | def remove_dup_element(a_list):
14:35:52.40    9 |     return {}.fromkeys(a_list).keys()
14:35:52.40 <<< Return value from remove_dup_element: dict_keys([10, 9, 1, 2, 3, 5, 6, 7, 8])

root@wyz-node1:~# 
```


更高级的使用方法，参考：

``` https://www.pypi.com.cn/project/snoop ```
``` https://github.com/cool-RR/PySnooper/blob/master/ADVANCED_USAGE.md ```

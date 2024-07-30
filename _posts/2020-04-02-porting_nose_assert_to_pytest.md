---
layout:     post
title:      "移植nose assert到pytest，丰富pytest断言"
subtitle:   "Porting nose assert to pytest"
date:       2020-04-02
author:     "Gavin Wang"
catalog:    true
categories:
    - [Automation]
    - [pytest]
    - [nose]
tags:
    - Automation
    - pytest
---


# 概述


一直很喜欢 nose 的 assert，方法多样，后来打算把所有的用例全部转换成 pytest，而 pytest 的 assert，相较于 nose，感觉太单调了，再者如果要是直接修改用例这部分的 assert，改动有点多，比较懒，直接抄袭 nose 的 assert 过来给 pytest 用。

看了下 nose 的 assert，来自 nose.tools，扫了下 tools 目录下的源码，继承自 unittest，直接照抄就是了。


# 效果


将这部分 code 放在自动化用例公共目录，验证一下效果如何：

```shell
root@pytest-70-97:/home/pytest_storage/src/common/tools# ll
total 16
drwxr-xr-x 2 root root 4096 Apr  2 18:01 ./
drwxr-xr-x 3 root root 4096 Apr  2 17:47 ../
-rw-r--r-- 1 root root  305 Apr  2 15:05 __init__.py
-rw-r--r-- 1 root root 1184 Apr  2 15:05 trivial.py
```

查看一下是否有这些 assert 属性了：

```shell
>>> from common import tools
>>> dir(tools)
['__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__', 'assert_almost_equal', 'assert_almost_equals', 'assert_dict_contains_subset', 'assert_dict_equal', 'assert_equal', 'assert_equals', 'assert_false', 'assert_greater', 'assert_greater_equal', 'assert_in', 'assert_is', 'assert_is_instance', 'assert_is_none', 'assert_is_not', 'assert_is_not_none', 'assert_items_equal', 'assert_less', 'assert_less_equal', 'assert_list_equal', 'assert_multi_line_equal', 'assert_not_almost_equal', 'assert_not_almost_equals', 'assert_not_equal', 'assert_not_equals', 'assert_not_in', 'assert_not_is_instance', 'assert_not_regexp_matches', 'assert_raises', 'assert_raises_regexp', 'assert_regexp_matches', 'assert_sequence_equal', 'assert_set_equal', 'assert_true', 'assert_tuple_equal', 'eq_', 'ok_', 'trivial', 'trivial_all']
>>> 
```



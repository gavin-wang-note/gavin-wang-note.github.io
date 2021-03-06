---
layout:     post
title:      "消除pylint warn/error"
subtitle:   "Fix pylint warn/error"
date:       2019-08-23
author:     "Gavin"
catalog:    true
tags:
    - pylint
    - Automation
---


# 概述

在写pytest用例期间，使用pylint检查代码质量，出现了一些这样或者那样的pylint warn/error，如何消灭这些warn/error，本文介绍一个unexpected-keyword-arg warn的消除方法。

# 现象

以下文代码为示例：

<img class="shadow" src="/img/in-post/code_example.png" width="1200">


这里有一行 ```md_dev = md.get_md_dev(md_info, _host=src_gw) ```

由于传递的参数 _host，这个参数是remote call（@callable）使用的，即可以在本机执行其他机器的指令，所以_host就是其他机器的IP地址，这里一旦带上 _host参数，执行pylint就会出现unexpected-keyword-arg，如何解决呢？


# 解决方法

在对应出现error/warn的代码行后面，增加disable具体的error/warn即可：

```
md_dev = md.get_md_dev(md_info, _host=src_gw) # pylint: disable=unexpected-keyword-arg
```



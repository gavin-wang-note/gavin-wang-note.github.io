---
layout:     post
title:      "nose-html-reporting plugin 抛lstrip_blocks异常"
subtitle:   "nose html report raise lstrip_blocks exception"
date:       2018-05-20
author:     "Gavin"
catalog:    true
tags:
    - nose
---


# 概述

在Ubuntu 14.04.5 LTS系统使用nose-html-reporting(nose-html-reporting-0.2.3)这个插件生成nose测试用例HTML测试报告，但在生成报告时，出现一个异常，导致报告无法正常生成，解决之。

异常信息如下图所示：

<img class="shadow" src="/img/in-post/nose_report_lstrip_blocks.png" width="800">


# 解决方法

修改

```/usr/local/lib/python2.7/dist-packages/nose_html_reporting-0.2.3-py2.7.egg/nose_html_reporting ``` 目录下 ```__init__.py ```文件

将203行 lstrip_blocks=True 注释掉，并删除掉产生的pyc文件。

```
root@44:/home/nose_test/src# cd /usr/local/lib/python2.7/dist-packages/nose_html_reporting/
root@44:/usr/local/lib/python2.7/dist-packages/nose_html_reporting# rm __init__.pyc
```

最后重新执行用例，并生成html报告。


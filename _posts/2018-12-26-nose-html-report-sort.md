---
layout:     post
title:      "nose-html-reporting plugin HTML报告排序"
subtitle:   "nose html report sort"
date:       2018-12-26
author:     "Gavin Wang"
catalog:    true
categories:
    - [Automation]
    - [nose]
tags:
    - nose
    - Automation
---


# 参考资料

```https://pypi.org/project/nose-html-reporting/ ```

# 概述

在Ubuntu 14.04.5 LTS系统使用nose生成测试报告时，使用了nose-html-reporting这个插件,但这个插件，对产生的测试报告是不排序的，比较乱，鉴于此，调整一下源码，使得测试结果能够排序。

为什么要排序？

排序后，能够方便QA排查失败用例是最初哪一个用例失败导致的，解耦用例间关系，尽可能的确保每个测试用例的独立性。


安装命令：

```pip install nose-html-reporting ```

在apt archive目录（/var/cache/apt/archives/）看到，使用的是 nose-html-reporting-0.2.3.tar.gz


# 实践

默认HTML report用例未排序：

<img class="shadow" src="/img/in-post/nose_report_not_sort.png" width="800">

如上图所示，HTML report展示的用例文件名称，并没有顺序排序，现修改了report2.jinja2内容，将下列内容：

<img class="shadow" src="/img/in-post/nose_html_before.png" width="800">

调整成:

<img class="shadow" src="/img/in-post/nose_html_after.png" width="800">


展示的HTML效果如下图所示：

<img class="shadow" src="/img/in-post/nose_html_report_sort.png" width="800">

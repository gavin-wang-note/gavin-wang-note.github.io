---
title: 一道有趣的python练习
date: 2024-05-19 19:23:00
author: Gavin Wang
img: "/img/Linux/vim1.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 有趣的一道python list练习题
categories:
    - [python]
tags:
    - python
---

# Overview

今天碰到这么一个小题目，interesting，mark一下

```python
list = [1,2,3,4,5]
for i in list:
    list.remove(i)
    list.append(i)
print(list)
```

选项：

```shell
A:for循环不能终止，无输出
B:语法错误，程序不能正常运行
C:[5,4,3,2,1]
D:[2,4,1,5,3]
```

# 分析过程

在开始迭代之前，列表list的内容是[1, 2, 3, 4, 5]。接下来，让我们逐步分析代码的执行过程：

* 第一次迭代中，i=1。list.remove(i)会移除列表中的第一个元素1，此时列表变为[2, 3, 4, 5]。接着执行list.append(i)，将1加到列表末尾，列表更新为[2, 3, 4, 5, 1]。
* 第二次迭代中，因为列表中的元素已经被修改，迭代器现在指向了新列表的第二个元素，也就是3。重复之前的过程后，列表变成[2, 4, 5, 1, 3]。
* 第三次迭代后，如此类推，迭代器现在指向了新列表的第三个元素5，列表变为[2, 4, 1, 3, 5]。
* 第四次迭代后，列表变为[2, 4, 1, 5, 3]。
* 到了第五次迭代，i=3，从列表中移除3再追加3到list，循环结束。最终，列表变成了[2, 4, 1, 5, 3]。

如下图所示：

<img class="shadow" src="/img/in-post/过程示例图.png" width="800">

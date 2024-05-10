---
title: Linux下解决vim内容黏贴缩进异常问题
date: 2024-05-27 23:11:37
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 设置vim永久生效内容黏贴缩进异常问题
categories:
    - [Linux]
    - [vim]
tags:
    - Linux
    - vim
---

# Overview

最近用 vim 写代码的时候，发现复制整段代码再粘贴的时候，缩进就全乱了，如下图所示：


<img class="shadow" src="/img/in-post/vim代码缩进异常.png" width="800">


# 解决方法

## 方法1： set paste

每次vim时，执行`:set paste`，然后再进行内容黏贴。

缺点比较明显，就是每次vim都要进行上述操作，当然，养成习惯也无所谓（习惯成自然）。

## 方法2：快捷键

有一个切换 `paste` 开关的选项叫 `pastetoggle`,可以通过用它来绑定一个快捷键，即可实现单键控制 激活/退出 `paste`模式：

```shell
:set pastetoggle=<F5>
```

PS:
  比方法1高阶了那么'亿'点点...

## 方法3：修改.vimrc增加set paste，永久生效

在当前登录用户HOME目录下，新增`.vimrc`文件，写入如下内容：

```shell
set paste
```

下次执行`vim`命令再次黏贴代码，缩进正常了。


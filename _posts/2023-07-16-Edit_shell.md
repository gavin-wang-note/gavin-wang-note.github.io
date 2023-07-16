---
layout:     post
title:      "修改默认shell"
subtitle:   "Change shell for Ubuntu/kali"
date:       2023-07-16
author:     "Gavin"
catalog:    true
tags:
    - shell
---



# 概述


今天在Ubuntu22环境下安装LANMP，执行`sh lanmp.sh`命令运行LANMP，如果出现如下错误：

```
root@ubuntu22:~# sh lanmp.sh 
lanmp.sh: 49: lib/common.conf: function: not found
lanmp.sh: 76: lib/common.conf: Syntax error: "}" unexpected
root@ubuntu22:~# 
```

这是因为在Kali或Ubuntu系统中，对dash的兼容性不好，而编译常用的是bash（Ubuntu默认shell是dash,  但是从bash环境拿过来的shell脚本执行就会遇到一些问题）。

这里涉及到更改系统的编辑器(shell)操作，本文介绍之。



# 实践



## 方法1： 交互式修改

输入命令dpkg-reconfigure dash ，然后选择\<NO\>选项：

```js
dpkg-reconfigure dash 
```

<img class="shadow" src="/img/in-post/reconfig-shell.png" width="1200">


## 方法2：非交互式修改

方法1是交互式的, 但是实际情况用脚本的更多, 所以我们还是用命令修改吧



```
[[ -L /bin/sh ]] && mv /bin/sh /tmp/.sh$(date +%s)
[[ -f /bin/sh ]] || ln -s /bin/bash /bin/sh
[[ -L /usr/share/man/man1/sh.1.gz ]] && mv /usr/share/man/man1/sh.1.gz /tmp/.sh.1.gz$(date +%s)
[[ -f /usr/share/man/man1/sh.1.gz ]] || ln -s /usr/share/man/man1/bash.1.gz /usr/share/man/man1/sh.1.gz
```

这些命令就是根据dpkg-reconfigure dash的结果来修改的。

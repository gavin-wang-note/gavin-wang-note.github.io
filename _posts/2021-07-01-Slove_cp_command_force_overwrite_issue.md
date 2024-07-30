---
layout:     post
title:      "CentOS中cp -f copy强制覆盖命令无效"
subtitle:   "Solve 'cp' copy force overwrite issue"
date:       2021-07-01
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - Linux
---



# 概述

今天分几次执行了automation用例，产生不不用的allure需要的json文件，由于部分case执行失败，再次执行了这部分用例，对新产生的json文件覆盖掉旧的，
结果在cp时提示是否要overwrite，由于文件数量很多，不可能每个交互信息都要输入y来确认覆盖，于是就要靠强制覆盖来解决，执行cp -rf时并没有起到预期效果。

本文记录解决Linux CentOS中cp -f 复制强制覆盖的命令无效的方法。

# 环境

```shell
[root@node179 ~]# cat /etc/redhat-release 
Red Hat Enterprise Linux Server release 7.2 (Maipo)
[root@node179 ~]# 
```


# 现象

```shell
[root@node179 06_30]# cp -i json/* /root/pytest_framework/report/json/
cp: overwrite ‘/root/pytest_framework/report/json/0002c684-9976-416e-8149-ed85c5e38aa8-container.json’? y
cp: overwrite ‘/root/pytest_framework/report/json/001824e6-1cde-4d7d-ae45-02acf4f2d33f-container.json’? y
```

换 -rf，效果一样

```shell
[root@node179 06_30]# cp -rf json/* /root/pytest_framework/report/json/
cp: overwrite ‘/root/pytest_framework/report/json/0002c684-9976-416e-8149-ed85c5e38aa8-container.json’? y
cp: overwrite ‘/root/pytest_framework/report/json/001824e6-1cde-4d7d-ae45-02acf4f2d33f-container.json’? y
```



# 处理过程

网上搜索了一下，看到这么个解释： Linux下默认cp命令是有别名的(alias cp='cp -i')，无法在复制时强制覆盖，即使你用 -f 参数也无法强制覆盖文件

在CentOS里执行alias，信息如下:

```shell
[root@node179 ~]# alias
alias cp='cp -i'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias grep='grep --color=auto'
alias l.='ls -d .* --color=auto'
alias ll='ls -l --color=auto'
alias ls='ls --color=auto'
alias mv='mv -i'
alias rm='rm -i'
alias vi='vim'
alias which='alias | /usr/bin/which --tty-only --read-alias --show-dot --show-tilde'
```

果然，cp是被alias过了。


# 推荐的解决方法

下面提供几个从网上找的Linux下cp命令覆盖的方法。

1)取消cp的alias（放心这不是永久生效）：

```shell
# unalias cp
# cp -rf /test/test_other
```

2)加反斜杠 \cp 执行cp命令时不走alias：（注：推荐这个方法！）

```shell
# \cp -rf /test/test_other
```

3）另外一个有意思的方法：

```shell
# yes|cp -rf /test/test_other
```


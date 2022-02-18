---
layout:     post
title:      "Linux下显示文件隶属于哪个包"
subtitle:   "Show which package the file belongs to"
date:       2022-02-08
author:     "Gavin"
catalog:    true
tags:
    - Linux 
---


# 概述

RD在定位问题的时候，需要QA告知当前文件隶属于哪个包，方便到对应包下查询源码来定位问题，故本文介绍一下Ubuntu和CentOS两种OS下查看文件隶属于哪个包。


# 查看当前文件隶属于哪个package

* CentOS

```
[root@83fc1 bin]# rpm -qf zerocopy_setup.py 
ezgateway-8.3-211.git09ae02f.x86_64
```

* Ubuntu
```
root@CVM01:/usr/local/bin# dpkg -S ezcopy
ezgateway: /usr/local/bin/ezcopy
```


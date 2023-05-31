---
layout:     post
title:      "显示ctdb VIP与物理IP映射关系"
subtitle:   "Show the relationship between VIP and physical IP mapping"
date:       2016-11-14
author:     "Gavin"
catalog:    true
tags:
    - shell
---



# 概述

产品UI支持存储网关上设置VIP，UI上并不会展示出这个/些VIP与物理IP之间的mapping关系。

故而先提供一个脚本，展示客户想知道当前VIP与物理IP间的映射关系。

# 脚本内容

```
#!/usr/bash

ctdb_status=`ctdb status  |grep pnn |tr -d pnn:  |awk '{print $1,$2}'|sort -nk 1  > /tmp/ctdb_status.out 2>&1`
ctdb_ip=`ctdb ip |grep -v IP |sort -nk 2  > /tmp/ctdb_ip.out 2>&1`

ctdb_ip_map=`join -1 1 -2 2 /tmp/ctdb_status.out /tmp/ctdb_ip.out 2>&1`

echo "pnn   storage ip  virtual ip"
echo "${ctdb_ip_map}\n"

```

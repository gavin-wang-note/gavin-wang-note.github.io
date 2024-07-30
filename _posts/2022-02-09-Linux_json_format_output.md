---
layout:     post
title:      "Linux 输出格式化成Json"
subtitle:   "Linux output format to Json"
date:       2022-02-09
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - Linux
---

# 概述

工作中经常会将Linux输出进行格式化，方便阅读。本文罗列几个常用的将输出转换为Json格式的方法。


# 实践

## 方法1 `python -mjson.tool`

此适用于多种OS


`ceph config-key get gateway_groups | python -mjson.tool`


## 方法2 `json_pp` or `jq`


适用于Debin系OS

`ceph config-key get gateway_groups | json_pp`


适用于RedHat系OS，带颜色

`ceph config-key get gateway_groups | jq`

e.g:

```shell
root@CVM01:~# ceph config-key get gateway_groups | json_pp
obtained 'gateway_groups'
{
   "groups" : {
      "Default" : {
         "member" : [
            "10.10.101.102",
            "10.10.101.103",
            "10.10.101.101",
            "10.10.101.104"
         ],
         "type" : "standard",
         "zerocopy" : false
      },
      "!!!not used!!!" : {
         "type" : "standard",
         "member" : []
      }
   },
   "virtual_gateways" : {},
   "_ver" : "5.2"
}
```


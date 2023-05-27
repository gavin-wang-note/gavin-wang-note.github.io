---
layout:     post
title:      "Disable core dump"
subtitle:   "Disable core dump"
date:       2017-02-17
author:     "Gavin"
catalog:    true
tags:
    - Linux
---

# 概述

有时候测试环境比较弱，资源开销比较大，一旦产生core dump file，期间会消耗CPU、memory和disk空间。为了暂时规避此问题，需要禁止产生core dump。

# 操作步骤

## To disable core dumps for all users

open /etc/security/limits.conf, enter:

```
# vi /etc/security/limits.conf
```

## Make sure the following config directive exists

```
* soft core 0
* hard core 0
```

## Save and close the file

Once a hard limit is set in /etc/security/limits.conf, the user cannot increase that limit within his own session. Add fs.suid_dumpable = 0 to /etc/sysctl.conf file:

```
# echo 'fs.suid_dumpable = 0' >> /etc/sysctl.conf
# sysctl -p
```

This will make sure that core dumps can never be made by setuid programs. 


## Set soft limit

Finally, add the following to /etc/profile to set a soft limit to stop the creation of core dump files for all users (which is default and must be disabled):

```
# echo 'ulimit -S -c 0 > /dev/null 2>&1' >> /etc/profile
```

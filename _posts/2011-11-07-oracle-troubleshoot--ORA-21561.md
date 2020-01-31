---
layout:     post
title:      "Oracle案例--错误码之ORA-21561"
subtitle:   "Oracle error code troubleshoot--ORA-21561"
date:       2011-11-07
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# ORA-21561  OID generation failed 案例

## 问题

AIX平台，创建oracle数据库实例时，报ORA-21561 OID创建失败

## 解决

修改/etc/hosts文件，添加本机IP与机器名。

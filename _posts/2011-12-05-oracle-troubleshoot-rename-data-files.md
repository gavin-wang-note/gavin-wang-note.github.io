---
layout:     post
title:      "Oracle案例--重命名表空间"
subtitle:   "Oracle troubleshoot--rename files name"
date:       2011-12-05
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# 重命名表空间

## 适用条件

一般使用于创建表空间时命名随意，后期想使得表空间命名规范化、具有实际意义（读其名而知其意）。

```alter tablespace old_taplespace_name rename to new_tablespace_name; ```


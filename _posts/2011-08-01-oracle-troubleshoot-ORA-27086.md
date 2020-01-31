---
layout:     post
title:      "Oracle案例--错误码之ORA-27086"
subtitle:   "Oracle error code troubleshoot--ORA-27086"
date:       2011-08-01
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# ORA-27086  unable to lock file - already in use  案例

## 表象

静默式安装oracle11g数据库并创建实例，database安装在raw上，启动数据库时，alert日志给出如下信息：

```
kcidr_process_controlfile_error:
IO Check was called but no error was found
ORA-00227: corrupt block detected in control file: (block 1, # blocks 1)
ORA-00202: control file: '/dev/raw/raw34'
ORA-00210: cannot open the specified control file
ORA-00202: control file: '/dev/raw/raw33'
ORA-27086: unable to lock file - already in use
Linux-x86_64 Error: 11: Resource temporarily unavailable
Additional information: 8
Additional information: 29924
ORA-00210: cannot open the specified control file
ORA-00202: control file: '/dev/raw/raw32'
ORA-27086: unable to lock file - already in use
Linux-x86_64 Error: 11: Resource temporarily unavailable
Additional information: 8
Additional information: 29924
kcidr_process_controlfile_error:
 IO Check was called but no error was found
ORA-00227: corrupt block detected in control file: (block 1, # blocks 1)
ORA-00202: control file: '/dev/raw/raw34'
ORA-00210: cannot open the specified control file
ORA-00202: control file: '/dev/raw/raw33'
ORA-27086: unable to lock file - already in use
Linux-x86_64 Error: 11: Resource temporarily unavailable
Additional information: 8
Additional information: 29924
ORA-00210: cannot open the specified control file
ORA-00202: control file: '/dev/raw/raw32'
ORA-27086: unable to lock file - already in use
Linux-x86_64 Error: 11: Resource temporarily unavailable
Additional information: 8
Additional information: 29924
```

## 原因

```
oracle@mmsg:~> oerr ora 27086
27086, 00000, "unable to lock file - already in use"
// *Cause:  the file is locked by another process, indicating that it is
//          currently in use by a database instance.
// *Action: determine which database instance legitimately owns this file.
```

## 解决方法

修改静默安装数据库使用的raw文件名称与map关系，避免这些raw占用现有环境上的其他raw文件.


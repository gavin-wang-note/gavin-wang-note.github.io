---
layout:     post
title:      "Oracle案例--因USER表空间无法扩展配额，导致imp导入数据失败(IMP-00003,ORA-01536,IMP-00017)"
subtitle:   "Oracle troubleshoot--import error by space quota exceeded(IMP-00003,ORA-01536,IMP-00017)"
date:       2010-06-02
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

因USER表空间无法扩展配额，导致imp导入数据失败

# 表象

```shell
IMP-00003: ORACLE error 1536 encountered
ORA-01536: space quota exceeded for tablespace 'USERS'
IMP-00017: following statement failed with ORACLE error 1536:
 "CREATE TABLE "VIRTUALCARRIERINFO" ("VIRTUALCARRIERID" NUMBER(*,0) NOT NULL "
 "ENABLE, "VCARRIERLEVELID" NUMBER(*,0), "VIRTUALCARRIERNAME" VARCHAR2(64) NO"
 "T NULL ENABLE, "DESCRIPTION" VARCHAR2(1024))  PCTFREE 10 PCTUSED 40 INITRAN"
 "S 1 MAXTRANS 255 STORAGE(INITIAL 65536 FREELISTS 1 FREELIST GROUPS 1)      "
 "              LOGGING NOCOMPRESS"
IMP-00003: ORACLE error 1536 encountered
ORA-01536: space quota exceeded for tablespace 'USERS'
IMP-00017: following statement failed with ORACLE error 1536:
 "CREATE TABLE "VIRTUALCARRIERLEVEL" ("VCARRIERLEVELID" NUMBER(*,0) NOT NULL "
 "ENABLE, "FLUXLIMIT" NUMBER(*,0) NOT NULL ENABLE, "MESSAGESIZELIMIT" NUMBER("
 "*,0) NOT NULL ENABLE, "RECIPIENTSNUMBER" NUMBER(*,0) NOT NULL ENABLE)  PCTF"
 "REE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 STORAGE(INITIAL 65536 FREELISTS 1"
 " FREELIST GROUPS 1)                    LOGGING NOCOMPRESS"
IMP-00003: ORACLE error 1536 encountered
ORA-01536: space quota exceeded for tablespace 'USERS'
Import terminated successfully with warnings.
```

# 原因

USER表空间扩展配置受限制

```shell
% oerr ora 01536
01536, 00000, "space quota exceeded for tablespace '%s'"
// *Cause:  The space quota for the segment owner in the tablespace has
//          been exhausted and the operation attempted the creation of a
//          new segment extent in the tablespace.
// *Action: Either drop unnecessary objects in the tablespace to reclaim
//          space or have a privileged user increase the quota on this
//          tablespace for the segment owner.
```

# 解决方法

dba用户修改表空间属性信息：

```shell
GRANT UNLIMITED TABLESPACE TO <username>;
```
---
layout:     post
title:      "Oracle SQL篇之其他"
subtitle:   "Oracle SQL -- Other KB"
date:       2010-09-09
author:     "Gavin"
catalog:    true
tags:
    - oracle
---


# 随机数函数

```
dbms_random.value(100,200)
```

# 查看错误码

oracle错误码包括ORA、TNS、EXP、IMP/RMAN等，查看这里错误码含义，命令格式如下：

```
oerr ora 错误码；
oerr tns 错误码
oerr exp错误码
oerr imp错误码
oerr rman 错误码
```

# 暂停函数

```
dbms_lock.sleep(5);
```

功能描述：

保存预定信息，比如说订票，但是超过一定时间（比如说15分钟），还没付费这个预定就失效了，也就是说把订单信息从表里删除
普通数据库用户是没有这个权限的，需要dba赋予权限后才能调用dbms_lock包，如下：

```
grant execute on dbms_lock to username;
```

# oracle注释

oracle注释支持两种，如下：

1、/\*\*\*test\*\*\*/

2、--

其中，对于/\*\*/这个注释对中，在SQL中仅有的注释对并不被忽略，如下：

```
SQL> /*commit*/
DBA_2PC_NEIGHBORS
information about incoming and outgoing connections for pending transactions

DBA_2PC_PENDING
info about distributed transactions awaiting recovery

DBA_ADDM_FDG_BREAKDOWN


DBA_ADDM_FINDINGS


DBA_ADDM_INSTANCES


DBA_ADDM_SYSTEM_DIRECTIVES


DBA_ADDM_TASKS


DBA_ADDM_TASK_DIRECTIVES


DBA_ADVISOR_ACTIONS



已选择9行。
```

所以，在sql命令中，尽可能避免使用/\*\*/纯粹注释对，可在该注释对中增加一些其他信息，则可避免命令被解析，如下：

```
SQL> /****commit***/
SQL>
```

即：/\*test\*/  被SQL解析，而/\*\*test\*\*/不会被解析。  

```
SQL> /*test*/ 
DBA_2PC_NEIGHBORS
information about incoming and outgoing connections for pending transactions

DBA_2PC_PENDING
info about distributed transactions awaiting recovery

DBA_ADDM_FDG_BREAKDOWN


DBA_ADDM_FINDINGS


DBA_ADDM_INSTANCES


DBA_ADDM_SYSTEM_DIRECTIVES


DBA_ADDM_TASKS


DBA_ADDM_TASK_DIRECTIVES


DBA_ADVISOR_ACTIONS



已选择9行。
SQL> /**test**/
SQL>
```


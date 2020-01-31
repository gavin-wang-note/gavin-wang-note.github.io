---
layout:     post
title:      "Oracle SQL篇之监控"
subtitle:   "Oracle SQL -- Monitor"
date:       2010-08-20
author:     "Gavin"
catalog:    true
tags:
    - oracle
---


# 监控事例的等待

```
select event,sum(decode(wait_Time,0,0,1)) "Prev", sum(decode(wait_Time,0,1,0)) "Curr",count(*) "Tot" from v$session_Wait    group by event order by 4;
```

# 回滚段的争用情况

```
select name, waits, gets, waits/gets "Ratio"	from v$rollstat C, v$rollname D   where C.usn = D.usn;
```

# 监控表空间的 I/O 比例

```
select B.tablespace_name nam, 
        A.phyblkrd pbr,
        A.phywrts pyw, 
        B.file_name "file", 
        A.phyrds pyr, 
        A.PHYBLKWRT pbw 
from v$filestat A, dba_data_files B   
where A.file# = B.file_id   order by B.tablespace_name;     
```


# 监控文件系统的 I/O 比例 

```
select substr(C.file#,1,2) "#",substr(C.name,1,30) "Name", C.bytes, D.phyrds, D.PHYWRTS, C.status from v$datafile C, v$filestat D           
where C.file# = D.file#;
```

# 监控 SGA 的命中率

```
select a.value +	b.value "logical_reads", c.	value "phys_reads", round(100 * ((a.value+b.value)-c.value) / (a.value+b.value)) "BUFFER HIT RATIO" 
from v$sysstat a, v$sysstat 	b, v$sysstat c 
where a.statistic# = 38 and 	b.statistic# = 39 and c.statistic# = 40;
```


# 监控 SGA 中字典缓冲区的命中率

```
select parameter, gets,Getmisses , getmisses/(gets+getmisses)*100 "miss ratio",
(1-(sum(getmisses)/ (sum(getmisses)+sum(getmisses))))*100 "Hit ratio" 
from v$rowcache 
where gets+getmisses <>0 
group by parameter, gets, getmisses;
```

# 监控 SGA 中共享缓存区的命中率，应该小于1%

```
select sum(pins)	"Total Pins", sum(reloads)  "Total Reloads", 
sum(reloads)/sum(pins) *100 libcache 
from v$librarycache;                     

select sum(pinhits-reloads)/sum(pins) "hit radio",sum(reloads)/sum(pins) "reload percent" from v$librarycache;
```

# 监控 SGA 中重做日志缓存区的命中率，应该小于1% 

```
SELECT name, gets, misses, immediate_gets, immediate_misses, Decode(gets,0,0,	misses/gets*100) ratio1, 
Decode(immediate_gets+immediate_misses,0,0, immediate_misses/(immediate_gets+immediate_misses)*100) ratio2 
FROM v$latch WHERE name IN ('redo allocation	', 'redo copy');
```

# 数据库表空间使用情况监控(字典管理表空间) 

数据库运行了一段时间后，由于不断的在表空间上创建和删除对象，会在表空间上产生大量的碎片，DBA应该及时了解表空间的碎片和可用空间情况，以决定是否要对碎片进行整理或为表空间增加数据文件。以下为引用的内容：

```
select tablespace_name, 
count(*) chunks , 
max(bytes/1024/1024) max_chunk 
from dba_free_space 
group by tablespace_name; 
```

上面的SQL列出了数据库中每个表空间的空闲块情况,如下所示: 
以下为引用的内容：

```
TABLESPACE_NAME         CHUNKS      MAX_CHUNK 
--------------------  ----------   ---------- 
INDX                 1           57.9921875 
RBS                  3           490.992188 
RMAN_TS             1            16.515625 
SYSTEM               1           207.296875 
TEMP                 20          70.8046875 
TOOLS                1           11.8359375 
USERS                67          71.3671875
```

其中，CHUNKS列表示表空间中有多少可用的空闲块(每个空闲块是由一些连续的Oracle数据块组成)，如果这样的空闲块过多，比如平均到每个数据文件上超过了100个，那么该表空间的碎片状况就比较严重了，可以尝试用以下的SQL命令进行表空间相邻碎片的接合: 

```
alter tablespace 表空间名 coalesce;
```

然后再执行查看表空间碎片的SQL语句，看表空间的碎片有没有减少。如果没有效果，并且表空间的碎片已经严重影响到了数据库的运行，则考虑对该表空间进行重建。
MAX_CHUNK列的结果是表空间上最大的可用块大小，如果该表空间上的对象所需分配的空间(NEXT值)大于可用块的大小的话，就会提示ORA-1652、ORA-1653、ORA-1654的错误信息，DBA应该及时对表空间的空间进行扩充，以避免这些错误发生。

# 查看数据库的连接情况

DBA要定时对数据库的连接情况进行检查，看与数据库建立的会话数目是不是正常，如果建立了过多的连接，会消耗数据库的资源。同时，对一些“挂死”的连接，可能会需要DBA手工进行清理。
以下的SQL语句列出当前数据库建立的会话情况: 以下为引用的内容：

```
select sid,serial#,username,program,machine,status 
from v$session; 
```

输出结果为: 以下为引用的内容：

```
SID   SERIAL#    USERNAME    PROGRAM    MACHINE    STATUS 
----  -------  ---------- ----------- ---------------  -------- 
1       1                    ORACLE.EXE   WORK3      ACTIVE 
2       1                    ORACLE.EXE   WORK3      ACTIVE 
3       1                    ORACLE.EXE   WORK3      ACTIVE 
4       1                    ORACLE.EXE   WORK3      ACTIVE 
5       3                    ORACLE.EXE   WORK3      ACTIVE 
6       1                    ORACLE.EXE   WORK3      ACTIVE 
7       1                    ORACLE.EXE   WORK3      ACTIVE 
8       27        SYS        SQLPLUS.EXE  WORKGROUP\WORK3  ACTIVE 
11      5        DBSNMP    dbsnmp.exe   WORKGROUP\WORK3   INACTIVE
```
注：
* SID 会话(session)的ID号；
* SERIAL# 会话的序列号，和SID一起用来唯一标识一个会话；
* USERNAME 建立该会话的用户名；
* PROGRAM 这个会话是用什么工具连接到数据库的；
* STATUS 当前这个会话的状态，ACTIVE表示会话正在执行某些任务，INACTIVE表示当前会话没有执行任何操作。
* 如果DBA要手工断开某个会话，则执行: 
```
alter system kill session 'SID,SERIAL#'; 
```

注意，上例中SID为1到7(USERNAME列为空)的会话，是Oracle的后台进程，不要对这些会话进行任何操作。

# 查看undo回滚率

```
SELECT NAME, VALUE FROM v$sysstat WHERE NAME IN ('user commits', 'transaction rollbacks');
```

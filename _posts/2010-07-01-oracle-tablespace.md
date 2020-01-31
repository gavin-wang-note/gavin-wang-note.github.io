---
layout:     post
title:      "Oracle SQL篇之表空间"
subtitle:   "Oracle SQL -- Tablespace"
date:       2010-07-01
author:     "Gavin"
catalog:    true
tags:
    - oracle
---

# 查看表大小

有两种含义的表大小：一种是分配给一个表的物理空间数量，而不管空间是否被使用。可以这样查询获得字节数：

```
select segment_name, bytes 
from user_segments 
where segment_type = 'TABLE'; 
```

或者

```
Select Segment_Name,Sum(bytes)/1024/1024 From User_Extents Group By Segment_Name
```

另一种表实际使用的空间。这样查询：

```
analyze table AREAINFO compute statistics; 

select   TABLE_NAME,TABLESPACE_NAME, NUM_ROWS ,AVG_ROW_LEN,  NUM_ROWS*AVG_ROW_LEN   
from user_tables 
where table_name = 'AREAINFO';
```

说明：

* 表名称要大写，红色加粗部分。

# 查看每个表空间的大小

```
Select Tablespace_Name,Sum(bytes)/1024/1024 From Dba_Segments Group By Tablespace_Name
```

# 看数据库有多少个tablespace

```
oracle@mmsg:~> sqlplus / as sysdba

SQL*Plus: Release 11.1.0.7.0 - Production on 星期四 7月 1 17:37:14 2010

Copyright (c) 1982, 2008, Oracle.  All rights reserved.


连接到: 
Oracle Database 11g Enterprise Edition Release 11.1.0.7.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> set wrap on
SQL> set linesize 700
SQL> select * from dba_tablespaces;

TABLESPACE_NAME                                              BLOCK_SIZE INITIAL_EXTENT NEXT_EXTENT MIN_EXTENTS MAX_EXTENTS   MAX_SIZE PCT_INCREASE MIN_EXTLEN STATUS                 CONTENTS           LOGGING            FORCE_ EXTENT_MANAGEMENT    ALLOCATION_TYPE    PLUGGE SEGMENT_SPAC DEF_TAB_COMPRESS RETENTION                  BIGFIL PREDICATE_EVAL ENCRYP COMPRESS_FOR
------------------------------------------------------------ ---------- -------------- ----------- ----------- ----------- ---------- ------------ ---------- ------------------ ------------------ ------------------ ------ -------------------- ------------------ ------ ------------ ---------------- ---------------------- ------ -------------- ------ ------------------------------------
SYSTEM                                                             8192          65536                       1  2147483645 2147483645                       65536 ONLINE             PERMANENT          LOGGING            NO     LOCAL                SYSTEM             NO     MANUAL   DISABLED         NOT APPLY              NO     HOST           NO
SYSAUX                                                             8192          65536                       1  2147483645 2147483645                       65536 ONLINE             PERMANENT          LOGGING            NO     LOCAL                SYSTEM             NO     AUTO     DISABLED         NOT APPLY              NO     HOST           NO
UNDOTBS1                                                           8192          65536                       1  2147483645 2147483645                       65536 ONLINE             UNDO               LOGGING            NO     LOCAL                SYSTEM             NO     MANUAL   DISABLED         NOGUARANTEE            NO     HOST           NO
TEMP                                                               8192        1048576     1048576           1             2147483645                0    1048576 ONLINE             TEMPORARY          NOLOGGING          NO     LOCAL                UNIFORM            NO     MANUAL   DISABLED         NOT APPLY              NO     HOST           NO
USERS                                                              8192          65536                       1  2147483645 2147483645                       65536 ONLINE             PERMANENT          LOGGING            NO     LOCAL                SYSTEM             NO     AUTO     DISABLED         NOT APPLY              NO     HOST           NO
MMSG                                                               8192          65536                       1  2147483645 2147483645                       65536 ONLINE             PERMANENT          LOGGING            NO     LOCAL                SYSTEM             NO     AUTO     DISABLED         NOT APPLY              NO     HOST           NO
MMSG_TMP                                                           8192        1048576     1048576           1             2147483645                0    1048576 ONLINE             TEMPORARY          NOLOGGING          NO     LOCAL                UNIFORM            NO     MANUAL   DISABLED         NOT APPLY              NO     HOST           NO

已选择7行。

SQL>
```


# 如何查有多少个数据库实例

```
SQL> select instance_number,instance_name,status from v$instance;

INSTANCE_NUMBER INSTANCE_NAME    STATUS
--------------- ---------------- ------------
              1 mmsgdb           OPEN

SQL>
```

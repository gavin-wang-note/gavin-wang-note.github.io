---
layout:     post
title:      "Oracle数据导入之SQL Load"
subtitle:   "Oracle SQL Load"
date:       2010-09-24
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---


# SQL*Loader帮助

命令行输入sqlldr，显示sqlloader帮助信息：

```shell
oracle@mmsg37:~> sqlldr 
SQL*Loader: Release 11.1.0.7.0 - Production on 星期四 9月 30 23:55:39 2010
Copyright (c) 1982, 2007, Oracle.  All rights reserved.
用法: SQLLDR keyword=value [,keyword=value,...]
有效的关键字: 
    userid -- ORACLE 用户名/口令        
   control -- 控制文件名                
       log -- 日志文件名                    
       bad -- 错误文件名                   
      data -- 数据文件名                  
   discard -- 废弃文件名
discardmax -- 允许废弃的文件的数目         (全部默认)
      skip -- 要跳过的逻辑记录的数目  (默认 0)
      load -- 要加载的逻辑记录的数目  (全部默认)
    errors -- 允许的错误的数目         (默认 50)
      rows -- 常规路径绑定数组中或直接路径保存数据间的行数
               (默认: 常规路径 64, 所有直接路径)
  bindsize -- 常规路径绑定数组的大小 (以字节计)  (默认 256000)
    silent -- 运行过程中隐藏消息 (标题,反馈,错误,废弃,分区)
    direct -- 使用直接路径                     (默认 FALSE)
   parfile -- 参数文件: 包含参数说明的文件的名称
  parallel -- 执行并行加载                    (默认 FALSE)
      file -- 要从以下对象中分配区的文件     
skip_unusable_indexes -- 不允许/允许使用无用的索引或索引分区  (默认 FALSE)
skip_index_maintenance -- 没有维护索引, 将受到影响的索引标记为无用  (默认 FALSE)
commit_discontinued -- 提交加载中断时已加载的行  (默认 FALSE)
  readsize -- 读取缓冲区的大小               (默认 1048576)
external_table -- 使用外部表进行加载; NOT_USED, GENERATE_ONLY, EXECUTE  (默认 NOT_USED)
columnarrayrows -- 直接路径列数组的行数  (默认 5000)
streamsize -- 直接路径流缓冲区的大小 (以字节计)  (默认 256000)
multithreading -- 在直接路径中使用多线程
 resumable -- 启用或禁用当前的可恢复会话  (默认 FALSE)
resumable_name -- 有助于标识可恢复语句的文本字符串
resumable_timeout -- RESUMABLE 的等待时间 (以秒计)  (默认 7200)
date_cache -- 日期转换高速缓存的大小 (以条目计)  (默认 1000)
PLEASE NOTE: 命令行参数可以由位置或关键字指定
。前者的例子是 'sqlload 
scott/tiger foo'; 后一种情况的一个示例是 'sqlldr control=foo 
userid=scott/tiger'.位置指定参数的时间必须早于
但不可迟于由关键字指定的参数。例如,
允许 'sqlldr scott/tiger control=foo logfile=log', 但是
不允许 'sqlldr scott/tiger control=foo log', 即使
参数 'log' 的位置正确。
```

# SQL*Loader组成元素

## 控制文件

控制文件是用一种语言写的文本文件，这个文本文件能被SQL*LOADER识别。SQL*LOADER根据控制文件可以找到需要加载的数据。并且分析和解释这些数据。控制文件由三个部分组成：

* 1、全局选件，行，跳过的记录数等；
* 2、INFILE子句指定的输入数据；
* 3、数据特性说明。

## 输入文件

对于 SQL*Loader, 除控制文件外就是输入数据。SQL*Loader可从一个或多个指定的文件中读出数据。如果数据是在控制文件中指定，就要在控制文件中写成 INFILE * 格式。

# 控制文件的格式

```shell
OPTIONS （ { [SKIP=integer] [ LOAD = integer ]
[ERRORS = integer] [ROWS=integer]
[BINDSIZE=integer] [SILENT=(ALL|FEEDBACK|ERROR|DISCARD) ] )
LOAD[DATA]
[ { INFILE | INDDN } {file | * }
[STREAM | RECORD | FIXED length [BLOCKSIZE size]|
VARIABLE [length] ]
[ { BADFILE | BADDN } file ]
{DISCARDS | DISCARDMAX} integr ]
[ {INDDN | INFILE} . . . ]
[ APPEND | REPLACE | INSERT ]
[RECLENT integer]
[ { CONCATENATE integer |
CONTINUEIF { [THIS | NEXT] (start[: end])LAST }
Operator { 'string' | X 'hex' } } ]
INTO TABLE [user.]table
[APPEND | REPLACE|INSERT]
[WHEN condition [AND condition]...]
[FIELDS [delimiter] ]
(
column {
RECNUM | CONSTANT value |
SEQUENCE ( { integer | MAX |COUNT} [, increment] ) |
[POSITION ( { start [end] | * [ + integer] }
) ]
datatype
[TERMINATED [ BY ] {WHITESPACE| [X] 'character' } ]
[ [OPTIONALLY] ENCLOSE[BY] [X]'charcter']
[NULLIF condition ]
[DEFAULTIF condotion]
}
[ ,...]
)
[INTO TABLE...]
[BEGINDATA]
```

# SQL*Loader示例

详见博文：[Excel数据导入到oracle数据库中](https://gavin-wang-note.github.io/2010/06/03/import_excel_data_to_oracle/)一文中提供的方法一：SQL*Loader 中描述信息。


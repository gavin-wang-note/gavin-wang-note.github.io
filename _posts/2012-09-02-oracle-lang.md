---
layout:     post
title:      "Oracle字符集"
subtitle:   "Oracle LANG"
date:       2012-09-02
author:     "Gavin"
catalog:    true
tags:
    - oracle
---


# Oracle数据库字符集

在不同数据库做数据迁移、同其它系统交换数据等，常常因为字符集不同而导致迁移失败或数据库内数据变成乱码。现在将oracle字符集相关的知识做个简单总结。

# 什么是oracle字符集

Oracle字符集是一个字节数据的解释的符号集合,有大小之分,有相互的包容关系。ORACLE 支持国家语言的体系结构允许你使用本地化语言来存储，处理，检索数据。它使数据库工具，错误消息，排序次序，日期，时间，货币，数字，和日历自动适应本地化语言和平台。

影响oracle数据库字符集最重要的参数是NLS_LANG参数。它的格式如下:

```NLS_LANG = language_territory.charset```

它有三个组成部分(语言、地域和字符集)，每个成分控制了NLS子集的特性。其中:

(1)Language 指定服务器消息的语言;

(2)territory 指定服务器的日期和数字格式;

(3)charset 指定字符集。如:AMERICAN _ AMERICA. ZHS16GBK

从NLS_LANG的组成我们可以看出，真正影响数据库字符集的其实是第三部分。所以两个数据库之间的字符集只要第三部分一样就可以相互导入导出数据，前面影响的只是提示信息是中文还是英文。

# 如何查询Oracle的字符集

很多人都碰到过因为字符集不同而使数据导入失败的情况。这涉及三方面的字符集，一是oracel server端的字符集，二是oracle client端的字符集;三是dmp文件的字符集。在做数据导入的时候，需要这三个字符集都一致才能正确导入。

(1)查询oracle server端的字符集

有很多种方法可以查出oracle server端的字符集，比较直观的查询方法是以下这种:

```
SQL> select userenv('language') from dual;
AMERICAN _ AMERICA. ZHS16GBK
```

(2)查询dmp文件的字符集

用oracle的exp工具导出的dmp文件也包含了字符集信息，dmp文件的第2和第3个字节记录了dmp文件的字符集。如果dmp文件不大，比如只有几M或几十M，可以用UltraEdit打开(16进制方式)，看第2第3个字节的内容，如0354，然后用以下SQL查出它对应的字符集:

```
SQL> select nls_charset_name(to_number('0354','xxxx')) from dual;
ZHS16GBK
```

如果dmp文件很大，比如有2G以上(这也是最常见的情况)，用文本编辑器打开很慢或者完全打不开，可以用以下命令(在unix主机上)：

```cat exp.dmp |od -x|head -1|awk '{print $2 $3}'|cut -c 3-6 ```

修改为：

```cat exp.dmp | od -h | head -1 | awk '{print substr($2,3,4) substr($3,3,4)}' ```

然后用上述SQL也可以得到它对应的字符集。

(3)查询oracle client端的字符集

在windows平台下，就是注册表里面相应OracleHome的NLS_LANG。还可以在dos窗口里面自己设置，比如：

```set nls_lang=AMERICAN_AMERICA.ZHS16GBK ```, 这样就只影响这个窗口里面的环境变量。

在unix平台下，就是环境变量NLS_LANG。

```
$echo $NLS_LANG
AMERICAN_AMERICA.ZHS16GBK
```

如果检查的结果发现server端与client端字符集不一致，请统一修改为同server端相同的字符集。

# 修改oracle的字符集

oracle的字符集有互相的包容关系。如us7ascii就是zhs16gbk的子集,从us7ascii到zhs16gbk不会有数据解释上的问题,不会有数据丢失。在所有的字符集中UTF-8是最大,因为它基于unicode,双字节保存字符(也因此在存储空间上占用更多)。

一旦数据库创建后，数据库的字符集理论上讲是不能改变的。因此，在设计和安装之初考虑使用哪一种字符集十分重要。如下图所示：

<img class="shadow" src="/img/in-post/oracle_lang.png" width="1200">
 
根据Oracle的官方说明，字符集的转换是从子集到超集受支持,反之不行。如果两种字符集之间根本没有子集和超集的关系，那么字符集的转换是不受oracle支持的。对数据库server而言，错误的修改字符集将会导致很多不可测的后果，可能会严重影响数据库的正常运行，所以在修改之前一定要确认两种字符集是否存在子集和超集的关系。一般来说，除非万不得已，我们不建议修改oracle数据库server端的字符集。特别说明，我们最常用的两种字符集ZHS16GBK和ZHS16CGB231280之间不存在子集和超集关系，因此理论上讲这两种字符集之间的相互转换不受支持。

(1)修改server端字符集(不建议使用)

在oracle 8之前，可以用直接修改数据字典表props$来改变数据库的字符集。但oracle8之后，至少有三张系统表记录了数据库字符集的信息，只改props$表并不完全，可能引起严重的后果。正确的修改方法如下:

```
　　$sqlplus /nolog
　　SQL>conn / as sysdba;
　　若此时数据库服务器已启动，则先执行SHUTDOWN IMMEDIATE命令关闭数据库服务器，然后执行以下命令:
　　SQL>STARTUP MOUNT;
　　SQL>ALTER SYSTEM ENABLE RESTRICTED SESSION;
　　SQL>ALTER SYSTEM SET JOB_QUEUE_PROCESSES=0;
　　SQL>ALTER SYSTEM SET AQ_TM_PROCESSES=0;
　　SQL>ALTER DATABASE OPEN;
　　SQL>ALTER DATABASE CHARACTER SET ZHS16GBK;
　　SQL>ALTER DATABASE national CHARACTER SET ZHS16GBK;
　　SQL>SHUTDOWN IMMEDIATE;
　　SQL>STARTUP
```

(2)修改dmp文件字符集

上文说过，dmp文件的第2第3字节记录了字符集信息，因此直接修改dmp文件的第2第3字节的内容就可以‘骗’过oracle的检查。这样做理论上也仅是从子集到超集可以修改，但很多情况下在没有子集和超集关系的情况下也可以修改，我们常用的一些字符集，如US7ASCII，WE8ISO8859P1，ZHS16CGB231280，ZHS16GBK基本都可以改。因为改的只是dmp文件，所以影响不大。

具体的修改方法比较多，最简单的就是直接用UltraEdit修改dmp文件的第2和第3个字节。比如想将dmp文件的字符集改为ZHS16GBK，可以用以下SQL查出该种字符集对应的16进制代码:

```
SQL> select to_char(nls_charset_id('ZHS16GBK'), 'xxxx') from dual;

TO_CH
-----
  354

SQL>
```

然后将dmp文件的2、3字节修改为0354即可。

如果dmp文件很大，用ue无法打开，就需要用程序的方法了，这里不做叙述。

# 小结

## 字符集

将特定的符号集编码为计算机能够处理的数值。

## 字符集间的转换

对于在源字符集与目标字符集都存在的符号，理论上转换将不会产生信息丢失；而对于在源字符集中存在而在目标字符集中不存在的符号，理论上转换将会产生信息丢失。

## 数据库字符集

选择能够包含所有将要存储的信息符号的字符集。

## 客户端字符集设置

指明客户端操作系统缺省使用的字符集。


---
layout:     post
title:      "修改oracle字符集(汉字显示为乱码)"
subtitle:   "Change oracle NLS_LANGUAGE"
date:       2011-11-20
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---


# 表象

数据库中汉字显示为乱码

# 原因

安装数据库时，如果字符集选择错误，会导致汉字显示为乱码。

```shell
SQL> select value$ from props$ where  name='NLS_LANGUAGE' or     name='NLS_TERRITORY' or     name='NLS_CHARACTERSET';

VALUE$
--------------------------------------------------------------------------------
SIMPLIFIED CHINESE
CHINA
WE8MSWIN1252
```

# 解决方法

在dbca中以现成的模板General Purpose（一般都是选这个模板）创建的databae，其字符集默认是 WE8ISO8859P1 ，并且在dbca中没有找到修改字符集设置的地方。WE8ISO8859P1是无法显示和处理中文的。

操作如下：

```shell
以sqlplus "/as sysdba"登录，执行如下更新：

update sys.props$ set VALUE$='ZHS16GBK' where name='NLS_CHARACTERSET';
```

查看更新后的值：

```shell
select * from sys.props$ where NAME='NLS_CHARACTERSET';
```

此属性重启数据库后生效，如果已经执行了应用脚本，请重新执行应用脚本，这样才不会出现乱码。


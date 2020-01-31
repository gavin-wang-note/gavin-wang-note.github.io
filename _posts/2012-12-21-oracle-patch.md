---
layout:     post
title:      "Oracle补丁"
subtitle:   "Oracle Patch"
date:       2012-12-21
author:     "Gavin"
catalog:    true
tags:
    - oracle
---


# 关于补丁

金无足赤，人无完人，oralce也一样，补丁天天出，打补丁就成了日常工作中常做的事。对于给数据库打补丁，个人建议如下：

1、大补丁（跨版本的补丁）---尽可能在安装oralce软件后，安装database前进行版本升级，实在不可避免，在有database的数据库上进行大补丁的升级操作，往往会破坏数据库的数据字典，详见博主的《Oracle升级碰到的问题》之ORA-01092。

2、小补丁—这个没影响，一般是在也只能在安装有database的数据库上进行升级操作，需要注意一点是：补丁的卸载，由于补丁与补丁之间有相互依赖关系，下载某补丁时，可能顺带卸载了其他的补丁。

# 补丁安装

%vi .cshrc

修改PATH行在该行添加如下内容：

```
:$ORACLE_HOME/Opatch:
%cd 6650132
%opatch apply
```

# 查看opatch版本

```
oracle@GW_8:~> opatch version
Invoking OPatch 11.1.0.6.2

OPatch Version: 11.1.0.6.2

OPatch succeeded.
```

# 查看系统中已经打上的one-off补丁

```
oracle@GW_8:~> opatch lsinventory
Invoking OPatch 11.1.0.6.2

Oracle Interim Patch Installer version 11.1.0.6.2
Copyright (c) 2007, Oracle Corporation.  All rights reserved.


Oracle Home       : /opt/oracle/product/11g
Central Inventory : /opt/oracle/oraInventory
   from           : /etc/oraInst.loc
OPatch version    : 11.1.0.6.2
OUI version       : 11.1.0.7.0
OUI location      : /opt/oracle/product/11g/oui
Log file location : /opt/oracle/product/11g/cfgtoollogs/opatch/opatch2012-12-05_08-47-10AM.log

Lsinventory Output file location : /opt/oracle/product/11g/cfgtoollogs/opatch/lsinv/lsinventory2012-12-05_08-47-10AM.txt

--------------------------------------------------------------------------------
Installed Top-level Products (2): 

Oracle Database 11g                                                  11.1.0.6.0
Oracle Database 11g Patch Set 1                                      11.1.0.7.0
There are 2 products installed in this Oracle Home.


There are no Interim patches installed in this Oracle Home.


--------------------------------------------------------------------------------

OPatch succeeded.
```

执行该命令，如果报错

```
oracle@GW_8:~> opatch lsinventory
-bash: opatcher: command not found
```

请oracle操作系统用户环境中做如下配置

```
export PATH=$ORACLE_HOME/OPatch:$PATH
```

source生效后重新执行opatch lsinventory命令。


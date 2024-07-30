---
layout:     post
title:      "Oracle案例--机器重启后数据库启动失败（ora-00205）"
subtitle:   "Oracle troubleshoot of oracle startup failed after reboot machine"
date:       2009-03-03
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# 单板重启后数据库启动失败

## 表象

逻辑卷以及raw创建并绑定，且创建实例后数据库正常使用，单板重启后，启动数据库出错，报00205错误。

起先手动激活逻辑卷组，并将裸设备与逻辑卷绑定，然后启动数据库，数据库依然启动失败。

查看一下00205是何种错误：

```shell
oerr ora 00205
00205, 00000, "error in identifying control file, check alert log for more info"
// *Cause:  The system could not find a control file of the specified name and
//         size.
// *Action: Check that ALL control files are online and that they are the same
//         files that the system created at cold start time.
```

去查看alert日志信息

```shell
<msg time='2009-03-03T13:53:07.240+08:00' org_id='oracle' comp_id='rdbms'
 client_id='' type='UNKNOWN' level='16'
 module='' pid='6789'>
 <txt>ORA-00210: ???????????
ORA-00202: ????: &apos;&apos;/dev/raw/raw15&apos;&apos;
ORA-27041: ??????
Linux-x86_64 Error: 13: Permission denied
Additional information: 2
ORA-00210: ???????????
ORA-00202: ????: &apos;&apos;/dev/raw/raw14&apos;&apos;
ORA-27041: ??????
Linux-x86_64 Error: 13: Permission denied
Additional information: 2
ORA-00210: ???????????
ORA-00202: ????: &apos;&apos;/dev/raw/raw13&apos;&apos;
ORA-27041: ??????
Linux-x86_64 Error: 13: Permission denied
Additional information: 2
 </txt>
</msg>
```

根据日志，发现raw13、raw14和raw15三个裸设备出现权限限制。

## 解决方法

（1）更改逻辑卷组激活方式，修改/etc/init.d/boot.lvm文件。

```shell
#vi /etc/init.d/boot.lvm
/sbin/vgchange -a y $LVM_VGS_ACTIVATED_ON_BOOT
```

（2）单板重启后，检测裸设备是否与逻辑卷自动绑定；

（3）如果绑定，oracle用户启动数据库便可成功。


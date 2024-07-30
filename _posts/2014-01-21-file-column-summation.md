---
layout:     post
title:      "根据文件列求和"
subtitle:   "file column summation"
date:       2014-01-21
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - awk
    - sum 
---


# 概述

工作中，常常会用到对某个测试结果进行数据汇总，就需要求和，比如求IOPS，或者带宽值，总不能拷贝出来，贴到excel中去求和、求平均值吧。。。

# 对文件中某一列进行数值求和

示例:

```shell
198 MMSGSUSE11 [wyz] :/home/wyz/perl/testcase>more tmp.txt
testAddCountryCode.AddCountryCode 5 0 0 796.28
testChcekSAGipNormal.ChcekSAGIPNormalTest 3 0 0 418.28
testCheckInfoNormal.CheckInfoNormalTest 3 0 0 748.26
testCheckSAGIPNormal.StageInteractiveNormalTest 3 0 0 804.79
testCheckSPinfo.CheckSPinfoTest 12 0 0 1736.24
testConsumModify.ConsumModify 8 0 0 2628.19
testCountryCodeAbnormalCase.CountryCodeAbnormalTest 3 0 0 899.41
testDelCountryCode.DelCountryCodeTest 5 0 0 1512.43
testEmigratedInteractive.EmigratedInteractiveTest 1 0 0 401.68
testGeneralOndemand.OndemandTest 10 0 0 2835.79
testGeneralOndemandAbnormal.OnDemandAbnormal 4 0 0 1029.27
testGiveOndemandAbnormal.GiveOndemandAbnormal 2 0 0 115.75
```

求和操作：

```shell
200 MMSGSUSE11 [wyz] :/home/wyz/perl/testcase>awk '{m+=$2} END{print m}' tmp.txt
59
```

# 对多列求和

示例：

```shell
201 MMSGSUSE11 [wyz] :/home/wyz/perl/testcase>more t.txt
00|M00a|0A|a00|0.00|15.00
00|M00a|0A|a00|0.00|15.00
00|M0Z1|0B|my|10.00|0.00
00|M0Z1|0A|a00|10.00|0.00
00|M005|0A|a00|0.00|1.48
00|M005|0A|a00|2.96|0.00
00|M005|0A|a00|2.96|0.00
```

求和操作：

```shell
202 MMSGSUSE11 [wyz] :/home/wyz/perl/testcase>awk -F '|' '{m+=$5;n+=$6} END {print m,n}' t.txt
25.92 31.48
```


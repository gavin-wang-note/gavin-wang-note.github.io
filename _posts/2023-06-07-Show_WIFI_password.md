---
layout:     post
title:      "获取WIFI密码"
subtitle:   "Get WIFI Password"
date:       2023-06-07
author:     "Gavin"
catalog:    true
tags:
    - WIFI
---



# 概述

已经连上过WIFI，忘记了密码，有新的电脑设备要加入，如何快速获取WIFI密码，本文介绍wlan命令，通过wlan命令获取WIFI密码。


# 实践

```
Microsoft Windows [版本 10.0.19045.2965]
(c) Microsoft Corporation。保留所有权利。

C:\Users\Gavin>netsh
netsh>wlan show profile

接口 WLAN 上的配置文件:


组策略配置文件(只读)
---------------------------------
    <无>

用户配置文件
-------------
    所有用户配置文件 : wifiYang_5G
    所有用户配置文件 : strayeagle_5G

netsh>
```

		
```
netsh>wlan show profile name="strayeagle_5G" key=clear

接口 WLAN 上的配置文件 strayeagle_5G:
=======================================================================

已应用: 所有用户配置文件

配置文件信息
-------------------
    版本                   : 1
    类型                   : 无线局域网
    名称                   : strayeagle_5G
    控制选项               :
        连接模式           : 自动连接
        网络广播           : 只在网络广播时连接
        AutoSwitch         : 请勿切换到其他网络
        MAC 随机化: 禁用

连接设置
---------------------
    SSID 数目              : 1
    SSID 名称              :“strayeagle_5G”
    网络类型               : 结构
    无线电类型             : [ 任何无线电类型 ]
    供应商扩展名           : 不存在

安全设置
-----------------
    身份验证         : WPA2 - 个人
    密码                 : CCMP
    身份验证         : WPA2 - 个人
    密码                 : GCMP
    安全密钥               : 存在
    关键内容            : HelloPasswordTest123!

费用设置
-------------
    费用                : 无限制
    阻塞                : 否
    接近数据限制        : 否
    过量数据限制        : 否
    漫游                : 否
    费用来源            : 默认

netsh>
```


**说明：**

* 此处的 "关键内容            : HelloPasswordTest123!"，即为wifi的密码.



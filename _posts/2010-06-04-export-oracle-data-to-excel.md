---
layout:     post
title:      "Oracle数据库中数据导入到Excel中"
subtitle:   "Export oracle data into Excel"
date:       2010-06-04
author:     "Gavin Wang"
catalog:    true
categories:
    - [oracle]
tags:
    - oracle
---

# 方法一：使用windows系统的ODBC

ODBC是Open Database Connectivity 的缩写，就是开放式数据库互连。利用ODBC实现动态数据交换的前提条件很简单，只需先在本机安装微软OFFICE中的EXCEL,然后根据需要运行编写的SQL文件。

步骤如下：

## 1、首先配置ODBC数据源

在控制面板中，选ODBC数据源，添加选安装ODBC FOR ORACLE。在给定数据源名称和描述时，用户可自定义，用户名称和服务器则需根据在ORACLE 数据库中设置好的数据库名来设置。如：

```shell
　　数据源名称：mmsgdb_114
　　描述：114oracle
　　用户名称：mmsg
　　服务器：10.137.49.114
 
```

<img class="shadow" src="/img/in-post/oracle-odbc-1.png" width="400">
<img class="shadow" src="/img/in-post/oracle-odbc-2.png" width="300">

## 2、excel与oracle数据库建立连接

打开EXCLE，在数据(D)菜单下，选择 导入外部数据(D) 导入数据(D) ，如下图所示：

<img class="shadow" src="/img/in-post/oracle-excel-1.png" width="400">

弹出“选择数据源”，如下图所示：

<img class="shadow" src="/img/in-post/oracle-excel-2.png" width="400"> 

选择“连接到新数据源”，弹出如下界面：

<img class="shadow" src="/img/in-post/oracle-guide-1.png" width="400">

在上图中选择 “Oracle”，点击“下一步(N)”，弹出如下界面：

<img class="shadow" src="/img/in-post/oracle-guide-2.png" width="400">

正确输入服务器名称和登录数据

<img class="shadow" src="/img/in-post/oracle-guide-3.png" width="400"> 

点击“下一步(N)”,弹出如下界面：

<img class="shadow" src="/img/in-post/oracle-guide-4.png" width="400">

选择数据库中表，点击“完成(F)”，弹出如下界面：

<img class="shadow" src="/img/in-post/oracle-guide-5.png" width="400">

点击“确定”按钮后，弹出如下界面：

<img class="shadow" src="/img/in-post/oracle-guide-6.png" width="400">

在上述界面中输入连接应用数据库的密码，点击“确定”按钮，查询出数据：

<img class="shadow" src="/img/in-post/oracle-guide-7.png" width="400">

如果选择“边界查询(Q)”按钮，弹出如下界面：

<img class="shadow" src="/img/in-post/oracle-guide-8.png" width="400">

在 命令文本(E) 中可编辑查询条件

<img class="shadow" src="/img/in-post/oracle-guide-9.png" width="400">

点击“确定”按钮后弹出“导入输出”界面，点击“确定”后，弹出 输入密码 界面，点击“确定”，得出相关数据信息。

## 3、保存文件

将该文件保存起来就可以了，至此，数据导出成功。

要是重新执行该文件，只需在MICRSOFT QUERY窗口中选择打开该查询并执行，即可得到实时的数据；然后可利用ＥＸＣＥＬ强大的编辑功能，对这些数据进行分析修改，相当方便。

# 方法二 使用PLSQL Developer工具辅助

使用PLSQL Developer工具，简单而快捷。

<img class="shadow" src="/img/in-post/oracle-sql-view.png" height="700" width="500">

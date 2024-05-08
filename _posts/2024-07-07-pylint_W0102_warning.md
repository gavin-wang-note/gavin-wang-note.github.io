---
layout:     post
title:      "消除pylint W0102 警告"
subtitle:   "Fix pylint W0102 警告"
date:       2024-07-07
author:     "Gavin Wang"
catalog:    true
categories:
    - [pylint]
tags:
    - pylint
---


# Overview

最近在搭建自动化基础测试框架，访问MySQL DB，封装了相关动作，碰到pylint W0102 警告，学习一下如何原理和消除操作。

# Code

原始代码参考如下：

```python
import logging

import pymysql

from .utils import paths, load_config

config_file_path = f"{paths['config']}/config.yml"
conf_data = load_config(config_file_path)["mysql"]

DB_CONF = {
    "host": conf_data["mysql_host"],
    "port": int(conf_data["mysql_port"]),
    "user": conf_data["mysql_user"],
    "password": conf_data["mysql_passwd"],
    "db": conf_data["mysql_db"]
}



class MySQLDB():
    """MySQL 数据库操作封装"""
    def __init__(self, db_conf=DB_CONF):
        """DB建联与创建游标对象"""
        # 通过字典拆包传递配置信息，建立数据库连接
        self.conn = pymysql.connect(**db_conf, autocommit=True)
        # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        """对象资源被释放时触发，在对象即将被删除时的最后操作"""
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def select_db(self, sql):
        """查询"""
        # 检查连接是否断开，如果断开就进行重连
        self.conn.ping(reconnect=True)
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        data = self.cur.fetchall()
        return data

    def execute_db(self, sql):
        """更新/新增/删除"""
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            # 使用 execute() 执行sql
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
        except Exception as err: # pylint: disable=W0718
            logging.info("操作MySQL出现错误，错误原因：(%s)", str(err))
            # 回滚所有更改
            self.conn.rollback()


db = MySQLDB(DB_CONF)
```

pylint warn信息如下：

```shell
W0102: Dangerous default value DB_CONF (builtins.dict) as argument (dangerous-default-value)
```

# 分析

pylint 分析这段代码时发出了一个警告 (W0102)，提醒这个默认值可能是危险的，因为它是一个可变类型的字典。

假如有一个名为 db_func 的函数，像这样：

```python
def db_func(default_db=DB_CONF):
    # 函数实现...

```

pylint 的感受就像这样：

* 如果你在函数定义时，或者在函数的上下文中更改了 `DB_CONF`（比如添加或删除字段），那么同样的更改会对所有后续使用此 `default_db` 参数的调用产生影响。
* 更危险的情况可能是，如果 `default_db` 代表的是一个数据库配置，而且函数修改了这个字典，比如添加或删除键值对。这样的修改会被保留并影响到下一个调用。


# 修复

解决这个问题的方法是：

方法1：立即初始化字典：不要依赖默认参数的缓存行为，而是在函数内部创建一个新的字典实例：

```python
def db_func():
    default_db = {
        "host": conf_data["mysql_host"],
        "port": int(conf_data["mysql_port"]),
        "user": conf_data["mysql_user"],
        "password": conf_data["mysql_passwd"],
        "db": conf_data["mysql_db"]
    }
    # 函数实现...
```

方法2：使用不可变类型：如果可能，使用不可变类型作为默认值。不过，在你的例子中，应用程序需要一个完整的配置字典。

方法3：显式指定：如果你希望提供字典的默认值，请确保它在每次函数调用中复核为新的，避免共享状态的潜在问题：

```python
def db_func(default_db=None):
    if default_db is None:
        default_db = {
            "host": conf_data["mysql_host"],
            "port": int(conf_data["mysql_port"]),
            "user": conf_data["mysql_user"],
            "password": conf_data["mysql_passwd"],
            "db": conf_data["mysql_db"]
        }
    # 函数实现...
```

这种方法在 `default_db` 被传递为 `None` 时，会立即创建一个新的字典，避免使用函数外部的 `DB_CONF` 变量。

最终效果：

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""MySQL操作封装"""

import logging

import pymysql

from .utils import paths, load_config

config_file_path = f"{paths['config']}/config.yml"
conf_data = load_config(config_file_path)["mysql"]


class MySQLDB():
    """MySQL 数据库操作封装"""
    def __init__(self, db_conf=None):
        """DB建联与创建游标对象"""
        if db_conf is None:
            db_conf = {
                "host": conf_data["mysql_host"],
                "port": int(conf_data["mysql_port"]),
                "user": conf_data["mysql_user"],
                "password": conf_data["mysql_passwd"],
                "db": conf_data["mysql_db"]
            }
        # 通过字典拆包传递配置信息，建立数据库连接
        self.conn = pymysql.connect(**db_conf, autocommit=True)
        # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        """对象资源被释放时触发，在对象即将被删除时的最后操作"""
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def select_db(self, sql):
        """查询"""
        # 检查连接是否断开，如果断开就进行重连
        self.conn.ping(reconnect=True)
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        data = self.cur.fetchall()
        return data

    def execute_db(self, sql):
        """更新/新增/删除"""
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            # 使用 execute() 执行sql
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
        except Exception as err: # pylint: disable=W0718
            logging.info("操作MySQL出现错误，错误原因：(%s)", str(err))
            # 回滚所有更改
            self.conn.rollback()


db = MySQLDB()
```

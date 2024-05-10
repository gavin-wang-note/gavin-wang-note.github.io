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

最近在搭建自动化基础测试框架，访问MySQL DB，封装了相关动作，碰到pylint W0102 警告，学习一下原理和消除操作。

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

# 拓展

上文示例的重点是：不要使用可变类型作为参数的默认值。

可选参数可以有默认值，这是Python函数定义的一个很棒的特性，这样我们的API在演进的同时能够保证向后兼容。然而，应该避免使用可变的对象作为参数的默认值。

《流畅的python》第二版中给出了解释说明，我摘录一下(拍的书，上册的第六章接，展示比较丑，建议买本书看看，第二版蛮值得品鉴)：

下 面 在 示 例 6-12 中 说 明 这 个 问 题。 我 们 以 示 例 6-8 中 的 Bus 类 为 基 础 定 义 一 个 新 类, HauntedBus ,然后修改` __init__` 方法。这一次, passengers 的默认值不是 None ,而是 [] ,

这样就不用像之前那样使用 if 判断了。这个“聪明的举动”会让我们陷入麻烦。

示例 6-12 一个简单的类,说明可变默认值的危险

```python
class HauntedBus:
"""备受幽灵乘客折磨的校车"""
   def __init__(self, passengers=[]): #
        self.passengers = passengers #
   def pick(self, name):
        self.passengers.append(name)
   def drop(self, name):
        self.passengers.remove(name)
```

如果没传入 passengers 参数,使用默认绑定的列表对象,一开始是空列表。

这个赋值语句把 self.passengers 变成 passengers 的别名,而没有传入 passengers 参数时,后者又是默认列表的别名。

在 self.passengers 上调用 .remove() 和 .append() 方法时,修改的其实是默认列表,它是函数对象的一个属性。

HauntedBus 的诡异行为如示例 6-13 所示。

示例 6-13 备受幽灵乘客折磨的校车

```python
    >>> bus1 = HauntedBus(['Alice', 'Bill'])
    >>> bus1.passengers
    ['Alice', 'Bill']
    >>> bus1.pick('Charlie')
    >>> bus1.drop('Alice')
    >>> bus1.passengers 
    ['Bill', 'Charlie']
    >>> bus2 = HauntedBus() 
    >>> bus2.pick('Carrie')
    >>> bus2.passengers
    ['Carrie']
    >>> bus3 = HauntedBus() 
    >>> bus3.passengers 
    ['Carrie']
    >>> bus3.pick('Dave')
    >>> bus2.passengers 
    ['Carrie', 'Dave']
    >>> bus2.passengers is bus3.passengers 
    True
    >>> bus1.passengers 
    ['Bill', 'Charlie']
```

目前没什么问题, bus1 没有出现异常。

一开始, bus2 是空的,因此把默认的空列表赋值给self.passengers 。

bus3 一开始也是空的,因此还是赋值默认的列表。

但是默认列表不为空!

登上 bus3 的 Dave 出现在 bus2 中。

问题是, bus2.passengers 和 bus3.passengers 指代同一个列表。

但 bus1.passengers 是不同的列表。

问题在于,没有指定初始乘客的 HauntedBus 实例会共享同一个乘客列表。

这种问题很难发现。如示例6-13所示,实例化HauntedBus时,如果传入乘客,会按预期运作。但是不为HauntedBus指定乘客的话,奇怪的事就发生了,这是因为self.passengers变成了passengers参数默认值的别名。出现这个问题的根源是,默认值在定义

函数时计算(通常在加载模块时),因此默认值变成了函数对象的属性。因此,如果默认值是可变对象,而且修改了它的值,那么后续的函数调用都会受到影响。

运行示例6-13中的代码之后,可以审查`HauntedBus.__init__`对象,看看它的`__defaults__` 属性中的那些幽灵学生:

```python
    >>> dir(HauntedBus.__init__) # doctest: +ELLIPSIS
    ['__annotations__', '__call__', ..., '__defaults__', ...]
    >>> HauntedBus.__init__.__defaults__
    (['Carrie', 'Dave'],)
```

最后,我们可以验证bus2.passengers是一个别名,它绑定到`HauntedBus.__init__.__defaults__` 属性的第一个元素上:

```python
    >>> HauntedBus.__init__.__defaults__[0] is bus2.passengers
    True
```

可变默认值导致的这个问题说明了为什么通常使用 None 作为接收可变值的参数的默认值。

在示例 6-8 中, `__init__` 方法检查 passengers 参数的值是不是 None ,如果是就把一个新的空列表赋值给 self.passengers；如果 passengers 不是 None ,正确的实现会把 passengers 的副本赋值给 self.passengers。


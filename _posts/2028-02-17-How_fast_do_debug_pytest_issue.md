---
title: 如何不在用例中增加debug，也能快速定位是哪个用例触发了某个操作？
date: 2028-02-17 23:00:00
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 如何不在每个用例中增加debug log，来快速定位是哪个用例触发了某个操作（改变了数据库中某个表字段值）？
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---



# 概述

今天有个同事调试`pytest`用例，她给可能引发此问题的每个用例增加`debug`信息（查询某个表中字段值，因为有个表字段值发生了错误），想知道是哪个用例造成问题的。
这种方法不太妥当原因如下：
改动量大，且目标不明确（只知道是哪个大功能引发的错误，但不知道是哪个具体功能，自然就不知道是哪个函数引发的问题，需要把可能引发问题的用例都修改）

如果想实现问题定位（定位到是哪个用例触发了数据库的错误修改），如何最小化修改？

本文将介绍一种在`pytest`中记录测试用例执行的方法信息，这种方法比简单地在每个用例中添加`debug`信息更为高效和系统化。

# 方法介绍

我们可以使用`pytest`的`fixture`功能来实现这一目标。`fixture`允许我们在测试用例执行前后执行一些代码，从而在不修改测试用例本身的情况下添加额外的功能。

## 代码示例

以下是一个示例代码，展示了如何在`pytest`中使用`fixture`来记录测试用例的执行信息：

```python
import logging
import os
import pytest
from mysql.connector import connect

# 创建数据库连接
class MySQLDB:
    def __init__(self):
        self.conn = connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="your_database"
        )
        self.cursor = self.conn.cursor()

    def execute_sql(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

# 记录数据库信息的函数
def record_db_info():
    my_db = MySQLDB()
    fg_sql = "select c9004 from hw2_0003 where c2='南京市发改委'"
    fg_res = my_db.execute_sql(fg_sql)
    logging.info("南京市发改委的状态是: %s", fg_res[0][0])
    my_db.close()

# 使用pytest fixture记录测试用例的执行信息
@pytest.fixture(scope='function', autouse=True)
def testcase_setup_teardown():
    """测试用例的前置和后置，记录当前正在执行的测试用例名称"""
    case_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    logging.info('Test case name: %s', case_name.encode("utf-8").decode("unicode_escape"))
    logging.debug("Before Run")
    record_db_info()
    
    yield
    
    logging.debug("After Run")
    record_db_info()
```

## 代码解释

1. **MySQLDB类**：用于创建和管理数据库连接。
2. **record_db_info函数**：用于记录数据库中的特定信息，这里以南京市发改委的状态为例。
3. **testcase_setup_teardown fixture**：
   - 使用`@pytest.fixture`装饰器定义一个fixture，其作用域为函数（即每个测试用例）。
   - `autouse=True`表示自动使用此fixture，无需在测试用例中显式调用。
   - 在测试用例执行前后记录日志信息，包括测试用例名称和数据库状态。

## 优势

- **自动化**：无需在每个测试用例中手动添加`debug`信息。
- **集中管理**：所有日志信息集中记录，便于管理和分析。
- **可扩展性**：可以轻松添加更多的日志记录功能，而无需修改测试用例本身。

# 结语

通过使用`pytest`的`fixture`功能，我们可以有效地记录测试用例的执行信息，从而在出现问题时快速定位。这种方法不仅提高了测试的效率，还增强了测试的可维护性和可扩展性。



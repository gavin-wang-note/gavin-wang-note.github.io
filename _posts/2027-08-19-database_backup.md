---
title: MySQL/Oracle数据库备份
date: 2027-08-19 23:00:00
author: Gavin Wang
img: ""
top: true
hide: false
cover: true
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: Shell/Python开发一套数据库备份系统，支持MySQL和Oracle，并生成HTML可视化报告
categories:
    - [python]
    - [shell]
tags:
    - python
    - shell
---

# 数据库备份工具设计文档

## 概述

由于数据库没有高可用性，为了防止不可抗力（机器硬盘损坏、数据库故障、人工误操作数据库等）造成的影响，需要对数据库进行备份操作，于是有了此工具的设计。

该数据库备份工具是一个全面的解决方案，用于自动化管理`MySQL`和`Oracle`数据库的备份、验证、报告生成和远程同步。工具由多个模块组成，提供端到端的备份管理功能，确保数据安全性和可恢复性。

## 系统架构

<img class="shadow" src="/img/in-post/db_backup_system/系统架构.png" width="1200" />

## 代码结构

```shell
root@Gavin:/home/gavin/db_backup_system# tree
.
├── backup_manager.sh
├── db_backup.conf
├── db_backup_lib.sh
├── generate_report.py
├── LICENSE
├── mysql_backup.sh
├── oracle_backup.sh
├── README.md
├── templates
│   └── report.html
└── verify_backup.sh
```

## 功能模块

###  功能模块图

<img class="shadow" src="/img/in-post/db_backup_system/功能模块图.png" width="1200" />


## 工作流程

###  备份工作流程

<img class="shadow" src="/img/in-post/db_backup_system/备份工作流.png" width="1200" />

### 验证工作流程

<img class="shadow" src="/img/in-post/db_backup_system/验证工作流.png" width="1200" />

### 数据备份数据流
<img class="shadow" src="/img/in-post/db_backup_system/数据库备份流程.png" width="1200" />

### 报告生成数据流
<img class="shadow" src="/img/in-post/db_backup_system/报告生成流程.png" width="1200" />


### 备份验证流程
<img class="shadow" src="/img/in-post/db_backup_system/备份验证流程.png" width="1200" />

## 模块交互图
<img class="shadow" src="/img/in-post/db_backup_system/模块交互图.png" width="1200" />

## 配置与接口设计

### 配置管理架构
<img class="shadow" src="/img/in-post/db_backup_system/配置管理架构.png" width="1200" />

### 模块接口设计
<img class="shadow" src="/img/in-post/db_backup_system/模块接口设计.png" width="1200" />

## 关键功能实现

### 1. 配置文件信息

```shell

t@Gavin:/home/gavin/db_backup_system# cat db_backup.conf 
#!/bin/bash
# 公共配置
BACKUP_ROOT="/backup"
LOG_DIR="/var/log/db_backup"
RSYNC_OPTIONS="-az --partial --delete"
REMOTE_SERVERS=("192.168.0.102" "192.168.0.102")
REMOTE_PATH="/data/backups"
MAX_LOG_DAYS=30
SSH_KEY="/root/.ssh/backup_key"
REMOTE_USER="root"
REMOTE_PASSWORD="p@ssw0rd"

# MySQL配置
MYSQL_USER="resume_admin"
MYSQL_PASSWORD="SecurePass123!"
MYSQL_SOCKET="/var/run/mysqld/mysqld.sock"
MYSQL_BACKUP_TYPE="xtrabackup"    # 可选: xtrabackup, mysqldump

# Oracle配置
ORACLE_USER="backup_user"
ORACLE_PASSWORD="secure_password"
ORACLE_SID="ORCL"
ORACLE_HOME="/u01/app/oracle/product/19c/dbhome_1"
ORACLE_DUMP_DIR="DATA_PUMP_DIR"

# 备份策略
FULL_BACKUP_DAY=7                 # 周日(1-7, 7=周日)
FULL_BACKUP_TIME="02:00"
INCR_BACKUP_TIME="02:00"
RETENTION_FULL=28                 # 保留28天
RETENTION_INCR=14                 # 保留14天
RETENTION_DATAPUMP=7              # 保留7天
```

### 2. 备份类型检测

```python
def get_backup_type():
    day_of_week = datetime.now().isoweekday()  # 1=周一,7=周日
    if day_of_week == config['FULL_BACKUP_DAY']:
        return "full"
    return "incr"
```

### 3. 备份点状态检测

```python
def check_backup_status(day_date, report_data):
    # 检查MySQL备份
    for backup in report_data['mysql']['full'] + report_data['mysql']['incr']:
        if backup['date'].date() == day_date:
            return "success" if backup['status'] == 'Success' else "failed"
    
    # 检查Oracle备份
    for backup in report_data['oracle']['full'] + report_data['oracle']['incr'] + report_data['oracle']['datapump']:
        if backup['date'].date() == day_date:
            return "success" if backup['status'] == 'Success' else "failed"
    
    return "missing"
```

### 4. 备份策略图表生成

```python
def generate_backup_strategy_chart(config, report_data):
    # 初始化SVG
    svg = f'<svg width="{width}" height="{height}">...'
    
    # 绘制每一天
    for i in range(max_retention + 1):
        day_date = today - timedelta(days=(max_retention - i))
        x = padding + 100 + (i * day_width)
        
        # 背景着色
        if is_full_backup_day:
            svg += f'<rect fill="#e6f7ff" ...>'
        elif is_weekend:
            svg += f'<rect fill="#f8f8f8" ...>'
        
        # 备份点
        backup_status = check_backup_status(day_date, report_data)
        if backup_status == "success":
            svg += f'<circle class="backup-success" ...>'
        elif backup_status == "failed":
            svg += f'<circle class="backup-failed" ...>'
        elif is_full_backup_day and day_date <= today:
            svg += f'<circle class="backup-missing" ...>'
    
    return svg + "</svg>"
```


## 可视化HTML报告

参考如下图所示:

<img class="shadow" src="/img/in-post/db_backup_system/DB_backup_report1.png" width="1200" />
<img class="shadow" src="/img/in-post/db_backup_system/DB_backup_report2.png" width="1200" />

**说明**:

- 鼠标浮动到'Failed'文案上，展示任务失败信息。


## 定时任务

可设置`cron jobs`，在 [02:00~04:00] 期间，执行定时任务。

## 总结

该数据库备份工具提供了一套完整的解决方案，具有以下特点：

1. **多数据库支持**：全面支持MySQL和Oracle数据库
2. **灵活策略**：可配置的备份策略和保留策略
3. **全面验证**：备份完整性、保留策略和远程同步验证
4. **可视化报告**：丰富的HTML报告和SVG图表
5. **安全可靠**：SSH加密传输和访问控制
6. **扩展性强**：模块化设计便于添加新功能

通过合理的架构设计和详细的功能实现，该工具能够满足企业级数据库备份的需求，确保数据安全性和业务连续性。


---
title: pytest实时测试报告与监控系统
date: 3000-01-03 23:00:00
author: Gavin Wang
img: 
top: true
hide: false
cover: true
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 实时监控&可视化展示pytest运行信息（进度、并发数、实时日志等）
categories:
    - [python]
    - [pytest]
tags:
    - python
    - pytest
---


# Pytest 实时测试报告与监控系统

## 🎯 项目概述

Pytest 实时测试报告与监控系统是一个基于 Flask + SocketIO 构建的高性能测试报告平台，提供实时的测试进度监控、详细的测试报告生成和跨环境配置管理功能。

可视化HTML报告预览如下图所示：

<p><img class="shadow" src="/img/pytest/测试结果分类联动.png" width="1200" /></p>
<p><img class="shadow" src="/img/pytest/测试结果详情.png" width="1200" /></p>
<p><img class="shadow" src="/img/pytest/进度百分百时查看报告.png" width="1200" /></p>
<p><img class="shadow" src="/img/pytest/进度与实时日志.png" width="1200" /></p>
<p><img class="shadow" src="/img/pytest/配置详情查看.png" width="1200" /></p>
<p><img class="shadow" src="/img/pytest/实时测试进度.png" width="1200" /></p>
<p><img class="shadow" src="/img/pytest/实时日志级别可过滤.png" width="1200" /></p>
<p><img class="shadow" src="/img/pytest/用例执行日志详情查看.png" width="1200" /></p>
<p><img class="shadow" src="/img/pytest/最终报告概览.png" width="1200" /></p>

### 设计理念

<p><img class="shadow" src="/img/report_monitor/设计理念.png" width="600" /></p>

## ✨ 核心特性

### 1. 实时进度监控

- 实时显示测试执行进度
- 动态更新通过/失败统计
- 实时日志流式输出

### 2. 多环境配置支持

- 基于 YAML 的配置管理
- 动态环境切换 (`--env` 参数)
- 自动环境检测与回退

### 3. 详细的测试报告

- HTML 格式测试报告
- 测试用例详细日志
- 执行时间统计
- 失败原因分析

### 4. 高性能架构

- 异步事件处理
- 多线程/进程支持
- 资源优化管理

## 🏗️ 系统架构

### 整体架构图

<p><img class="shadow" src="/img/report_monitor/整体架构图.png" width="600" /></p>

### 核心类关系图

<p><img class="shadow" src="/img/report_monitor/核心类关系图.png" width="600" /></p>

### 数据流图

<p><img class="shadow" src="/img/report_monitor/数据流图.png" width="600" /></p>

## 🔧 快速开始

### 环境要求

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Pytest](https://img.shields.io/badge/Pytest-8.0%2B-green)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)
![SocketIO](https://img.shields.io/badge/SocketIO-Real--time-orange)
![Eventlet 或 Gevent](https://img.shields.io/badge/Eventlet%20%E6%88%96%20Gevent-brightgreen)
![flask_socketio](https://img.shields.io/badge/flask_socketio-5.5.1%2B-blue)

### 安装依赖

```bash
pip install -r requirements.txt
```

### 依赖架构图

<p><img class="shadow" src="/img/report_monitor/依赖架构图.png" width="600" /></p>

### 基础使用

```bash
# 启动实时监控服务器
python run_server.py

# 运行测试并生成报告
pytest --live-report --env=dev

# 保持服务器运行
pytest --live-report --keep-server --env=qa
```

### 项目结构

```shell
project/
├── utils/
│   ├── custom_reporter.py    # 核心报告生成器
│   ├── report_server.py      # Web服务器
│   ├── get_server_ip.py      # 获取服务器当前IP V4地址
│   └── config_loader.py      # 配置加载器
├── templates/
│   ├── progress.html         # 实时监控页面
│   └── template.html         # 报告模板
├── config/
│   └── environment.yaml      # 环境配置文件
├── reports/
│   ├── automation.log        # 日志文件
│   ├── json                  # Allure报告原始数据
│   ├── final_state.json      # 用例执行结束后的最终上报UI数据
│   └── final_report.html     # 生成的报告
├── conftest.py               # Pytest配置
└── run_server.py             # 服务器启动脚本
```

## 📊 功能详解

### 1. 实时监控系统

#### 监控界面组件

<p><img class="shadow" src="/img/report_monitor/监控界面组件.png" width="600" /></p>

### 2. 配置管理系统

#### 环境配置加载流程

<p><img class="shadow" src="/img/report_monitor/环境配置加载流程.png" width="600" /></p>

### 3. 测试报告生成

#### 报告生成流程

<p><img class="shadow" src="/img/report_monitor/报告生成流程.png" width="600" /></p>

## 🎯 高级配置

### 环境配置文件示例

```yaml
# config/environment.yaml
dev:
  base_url: "http://dev.api.example.com"
  api:
    endpoint: "http://dev.api.example.com/v1"
    timeout: 30
  database:
    host: "dev-db.example.com"
    port: 3306
    name: "app_dev"
  auth:
    token_url: "http://dev.api.example.com/auth"
    client_id: "dev_client"

qa:
  base_url: "http://qa.api.example.com"
  api:
    endpoint: "http://qa.api.example.com/v1" 
    timeout: 30
  database:
    host: "qa-db.example.com"
    port: 3306
    name: "app_qa"

prod:
  base_url: "https://api.example.com"
  api:
    endpoint: "https://api.example.com/v1"
    timeout: 60
  database:
    host: "prod-db.example.com"
    port: 3306
    name: "app_prod"
```

### 自定义报告模板

系统支持自定义 HTML 报告模板，主要模板变量：

```html
<!-- 在 template.html 中 -->
<div class="environment-info">
    <h3>测试环境信息</h3>
    <table>
        <tr>
            <td>测试环境</td>
            <td>{{ base_config.current_env }}</td>
        </tr>
        <tr>
            <td>BaseURL</td>
            <td>{{ base_config.base_url }}</td>
        </tr>
        <tr>
            <td>测试账号</td>
            <td>{{ base_config.account }}</td>
        </tr>
        <tr>
            <td>执行人员</td>
            <td>{{ base_config.tester }}</td>
        </tr>
    </table>
</div>
```

## 🔍 技术深度

### 1. 事件驱动架构

#### 事件处理机制

<p><img class="shadow" src="/img/report_monitor/事件驱动架构系统.png" width="600" /></p>

### 2. 并发处理模型

系统采用多线程 + 异步IO的混合并发模型：

```python
# 并发架构示例
class HybridConcurrency:
    def __init__(self):
        # 主线程：Flask + SocketIO
        self.main_thread = threading.Thread(target=self.start_server)
        
        # 工作线程：进度广播
        self.broadcast_thread = threading.Thread(target=self.broadcast_worker)
        
        # 异步任务：日志推送
        self.async_tasks = []
    
    def start_server(self):
        # 使用 eventlet 实现异步IO
        eventlet.monkey_patch()
        self.socketio.run(self.app, async_mode='eventlet')
```

### 3. 内存管理优化

<p><img class="shadow" src="/img/report_monitor/内存管理策略.png" width="600" /></p>

## 🚀 性能优化

### 1. WebSocket 连接管理

<p><img class="shadow" src="/img/report_monitor/websocket连接管理.png" width="600" /></p>

### 2. 数据序列化优化

系统采用高效的数据序列化策略：

```python
class OptimizedSerializer:
    def serialize_progress(self, progress_data):
        """优化进度数据序列化"""
        return {
            't': progress_data.get('target', ''),
            'c': progress_data.get('completed', 0),
            'tt': progress_data.get('total', 0),
            'p': progress_data.get('percent', 0)
        }
    
    def serialize_log(self, log_entry):
        """优化日志序列化"""
        return f"{log_entry.timestamp}|{log_entry.level}|{log_entry.message}"
```

---

**Pytest 实时测试报告与监控系统** - 让测试监控变得简单而强大！ 🚀

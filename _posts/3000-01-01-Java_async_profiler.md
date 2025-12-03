---
title: Java async-profiler性能分析工具
date: 3000-01-01 23:00:00
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
summary: 基于async-profiler，针对Java程序进行性能数据收集
categories:
    - [python]
    - [Performance]
tags:
    - python
    - Performance
---


# Java性能分析工具

## 概述

这是一个基于`Python`的`Java`性能分析工具，集成了`async-profiler`和火焰图生成功能，可以方便地对`Java`应用程序进行性能分析和优化。

## 功能特性

- 🔍 自动发现Java进程
- ⚡ 支持并发性能分析
- 📊 生成交互式HTML火焰图
- 📝 自动生成性能分析报告
- 🔧 权限自动检测与修复
- 🎯 支持多种PID输入格式
- ⏱️ 可配置分析时长

## 安装与部署

### 1. 安装async-profiler

```bash
# 下载最新版async-profiler
wget https://github.com/async-profiler/async-profiler/releases/download/v4.1/async-profiler-4.1-linux-x64.tar.gz

# 解压并安装
sudo tar -zxvf async-profiler-4.1-linux-x64.tar.gz -C /opt/
sudo mv async-profiler-4.1-linux-x64/ /usr/local/bin/
sudo ln -s /usr/local/bin/async-profiler-4.1-linux-x64/bin/asprof /usr/local/bin/asprof
sudo ln -s /usr/local/bin/async-profiler-4.1-linux-x64/bin/jfrconv /usr/local/bin/jfrconv

# 验证安装
asprof --version
```

### 2. 配置系统权限

```bash
# 调整内核参数以允许性能分析
sudo sh -c 'echo 1 >/proc/sys/kernel/perf_event_paranoid'
sudo sh -c 'echo 0 >/proc/sys/kernel/kptr_restrict'

# 使配置永久生效
echo 'kernel.perf_event_paranoid=1' | sudo tee -a /etc/sysctl.conf
echo 'kernel.kptr_restrict=0' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### 3. 项目结构

```shell
java_profiler/
├── main.py               # 主程序入口
├── utils.py              # 工具函数库
├── templates/
│   └── report.html      # HTML报告模板
└── README.md             # 项目说明文档
```

## 使用方法

### 基本使用

```bash
# 运行性能分析工具
python main.py

# 指定分析时长和PID
python main.py --duration 30 --pid 12345
```

### 交互式使用

1. 运行程序后，会显示所有Java进程
2. 选择是否启用并发分析模式
3. 输入要分析的PID（支持多种格式）
4. 设置分析时长
5. 查看生成的报告

### PID输入格式示例

- 分析所有Java进程：直接回车
- 分析单个进程：`112497`
- 分析多个进程（逗号分隔）：`112497,123676`
- 分析多个进程（空格分隔）：`112497 123676`
- 分析PID范围：`112490-112500`

## 设计架构

### 系统架构图

<p><img class="shadow" src="/img/java_profiler/系统架构图.png" width="600" /></p>

### 类图设计

<p><img class="shadow" src="/img/java_profiler/类图设计.png" width="600" /></p>

### 序列图示例

<p><img class="shadow" src="/img/java_profiler/序列图.png" width="600" /></p>

## 火焰图解读指南


### 理解火焰图

火焰图是一种可视化性能分析工具，显示代码执行路径和资源消耗情况：

1. **X轴**：表示采样数量，宽度越宽表示消耗资源越多
2. **Y轴**：表示调用栈深度，从上到下表示调用关系
3. **颜色**：通常没有特定含义，可用于区分不同模块

### 常见性能问题模式

| 模式 | 症状 | 解决方案 |
|------|------|----------|
| **平顶山峰** | 某个函数占用大量CPU时间 | 优化该函数算法，减少计算复杂度 |
| **深调用栈** | 调用层次过深 | 检查是否有不必要的嵌套调用 |
| **频繁分配** | 大量内存分配操作 | 使用对象池，减少临时对象创建 |
| **锁竞争** | 同步操作频繁 | 减小锁粒度，使用并发数据结构 |
| **I/O等待** | 大量I/O操作 | 使用异步I/O或批量处理 |

### 性能优化建议

1. **CPU密集型优化**：
   - 优化热点函数算法
   - 使用更高效的数据结构
   - 减少不必要的计算

2. **内存优化**：
   - 减少对象创建
   - 使用对象池
   - 优化数据结构大小

3. **I/O优化**：
   - 使用异步I/O
   - 批量处理数据
   - 增加缓存层

4. **并发优化**：
   - 减小锁范围
   - 使用无锁数据结构
   - 合理设置线程池大小

## 示例输出

### 核心命令

```shell
执行JFR数据收集命令: asprof -d 120 -f profile_3410/profile_3410.jfr -o jfr -e cpu -e alloc -e lock 3410
生成 cpu 火焰图命令: jfrconv profile_3410/profile_3410.jfr --cpu profile_3410/flamegraph_cpu_3410.html
生成 alloc 火焰图命令: jfrconv profile_3410/profile_3410.jfr --alloc profile_3410/flamegraph_alloc_3410.html
生成 lock 火焰图命令: jfrconv profile_3410/profile_3410.jfr --lock profile_3410/flamegraph_lock_3410.html
```

### 使用帮助

```shell
[gavin@Gavin java_profiler]$ python3 main.py -h
============================================================
🐛 Java性能分析工具 - Async Profiler集成
============================================================
usage: main.py [-h] [--pid PID] [--duration DURATION] [--concurrent] [--max-workers MAX_WORKERS] [--fix-permissions]

Java性能分析工具

optional arguments:
  -h, --help            show this help message and exit
  --pid PID             要分析的Java进程PID，支持逗号分隔或范围格式
  --duration DURATION   分析持续时间（秒）
  --concurrent          启用并发分析模式
  --max-workers MAX_WORKERS
                        最大并发线程数
  --fix-permissions     自动修复权限问题
[gavin@Gavin java_profiler]$
```

### 基本用法，指定了持续时间和单个java进程

```shell
[gavin@Gavin java_profiler]$ python main.py --pid 3410 --duration 30
============================================================
🐛 Java性能分析工具 - Async Profiler集成
============================================================
找到 async-profiler: Async-profiler 4.1 built on Jul 21 2025
📋 找到Java进程: 23601, 3410, 3950
🔍 使用命令行参数: PID=3410, 时长=30秒
🐢 使用顺序分析模式
🔍 将要分析的进程: 3410
⏱  每个进程分析时间: 30秒
🔍 开始分析进程 3410...
📊 收集JFR性能数据（30秒）...
✅ JFR数据收集成功: profile_3410/profile_3410.jfr (21025 bytes)
📈 分析JFR数据并生成报告...
✅ CPU 火焰图已生成: profile_3410/flamegraph_cpu_3410.html
✅ ALLOC 火焰图已生成: profile_3410/flamegraph_alloc_3410.html
✅ LOCK 火焰图已生成: profile_3410/flamegraph_lock_3410.html

📊 进程 3410 分析结果:
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 检测到内存分配压力，建议优化对象创建模式
  3. 锁竞争分析: 未发现明显问题
📄 HTML报告已生成: profile_3410/report_3410.html
✅ 进程 3410 分析完成
⏱  总耗时: 31.04秒 (顺序模式)

🎉 所有分析完成！
[gavin@Gavin java_profiler]$ 
```

### 分析多个PID（逗号分隔）

```shell
[gavin@Gavin java_profiler]$ python main.py --pid "3410,3950" --duration 30
============================================================
🐛 Java性能分析工具 - Async Profiler集成
============================================================
找到 async-profiler: Async-profiler 4.1 built on Jul 21 2025
📋 找到Java进程: 3410, 23753, 3950
🔍 使用命令行参数: PID=3410,3950, 时长=30秒
🐢 使用顺序分析模式
🔍 将要分析的进程: 3410, 3950
⏱  每个进程分析时间: 30秒
🔍 开始分析进程 3410...
📊 收集JFR性能数据（30秒）...
✅ JFR数据收集成功: profile_3410/profile_3410.jfr (21282 bytes)
📈 分析JFR数据并生成报告...
✅ CPU 火焰图已生成: profile_3410/flamegraph_cpu_3410.html
✅ ALLOC 火焰图已生成: profile_3410/flamegraph_alloc_3410.html
✅ LOCK 火焰图已生成: profile_3410/flamegraph_lock_3410.html

📊 进程 3410 分析结果:
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 未发现明显问题
  3. 锁竞争分析: 未发现明显问题
📄 HTML报告已生成: profile_3410/report_3410.html
✅ 进程 3410 分析完成
🔍 开始分析进程 3950...
📊 收集JFR性能数据（30秒）...
✅ JFR数据收集成功: profile_3950/profile_3950.jfr (35393 bytes)
📈 分析JFR数据并生成报告...
✅ CPU 火焰图已生成: profile_3950/flamegraph_cpu_3950.html
✅ ALLOC 火焰图已生成: profile_3950/flamegraph_alloc_3950.html
✅ LOCK 火焰图已生成: profile_3950/flamegraph_lock_3950.html

📊 进程 3950 分析结果:
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 检测到内存分配压力，建议优化对象创建模式
  3. 锁竞争分析: 未发现明显问题
📄 HTML报告已生成: profile_3950/report_3950.html
✅ 进程 3950 分析完成
⏱  总耗时: 62.07秒 (顺序模式)

🎉 所有分析完成！
[gavin@Gavin java_profiler]$ 
```



### 启用并发分析（空格分隔）

```shell
[gavin@Gavin java_profiler]$ python main.py --pid "3410 3950" --duration 30 --concurrent
============================================================
🐛 Java性能分析工具 - Async Profiler集成
============================================================
找到 async-profiler: Async-profiler 4.1 built on Jul 21 2025
📋 找到Java进程: 3410, 24028, 3950
🔍 使用命令行参数: PID=3410,3950, 时长=30秒
🚀 启用并发分析，最大线程数: 3
🔍 将要分析的进程: 3410, 3950
⏱  每个进程分析时间: 30秒

🚀 开始并发分析 2 个进程...
🔍 [并发] 开始分析进程 3410...
📊 收集JFR性能数据（30秒）...
🔍 [并发] 开始分析进程 3950...
📊 收集JFR性能数据（30秒）...
✅ JFR数据收集成功: profile_3410/profile_3410.jfr (23257 bytes)
📈 分析JFR数据并生成报告...
✅ JFR数据收集成功: profile_3950/profile_3950.jfr (26476 bytes)
📈 分析JFR数据并生成报告...
✅ CPU 火焰图已生成: profile_3950/flamegraph_cpu_3950.html
✅ CPU 火焰图已生成: profile_3410/flamegraph_cpu_3410.html
✅ ALLOC 火焰图已生成: profile_3410/flamegraph_alloc_3410.html
✅ ALLOC 火焰图已生成: profile_3950/flamegraph_alloc_3950.html
✅ LOCK 火焰图已生成: profile_3410/flamegraph_lock_3410.html

📊 [并发] 进程 3410 分析结果:
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 检测到内存分配压力，建议优化对象创建模式
  3. 锁竞争分析: 未发现明显问题
✅ LOCK 火焰图已生成: profile_3950/flamegraph_lock_3950.html

📊 [并发] 进程 3950 分析结果:
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 检测到内存分配压力，建议优化对象创建模式
  3. 锁竞争分析: 未发现明显问题
📄 HTML报告已生成: profile_3410/report_3410.html
✅ 进程 3410 分析完成
📄 HTML报告已生成: profile_3950/report_3950.html
✅ 进程 3950 分析完成

📊 并发分析完成: 成功 2, 失败 0
⏱  总耗时: 31.10秒 (并发模式)

🎉 所有分析完成！
[gavin@Gavin java_profiler]$ 
```


### 指定并发线程数


```shell
[gavin@Gavin java_profiler]$ python main.py --pid "3410 3950 24305" --duration 30 --concurrent --max-workers 5
============================================================
🐛 Java性能分析工具 - Async Profiler集成
============================================================
找到 async-profiler: Async-profiler 4.1 built on Jul 21 2025
📋 找到Java进程: 3410, 24567, 3950
🔍 使用命令行参数: PID=3410 3950 24305, 时长=30秒
🚀 启用并发分析，最大线程数: 5
⚠  进程 24305 不是有效的Java进程，已跳过
🔍 将要分析的进程: 3410, 3950
⏱  每个进程分析时间: 30秒

🚀 开始并发分析 2 个进程...
🔍 [并发] 开始分析进程 3410...
🔍 [并发] 开始分析进程 3950...
📊 收集JFR性能数据（30秒）...
📊 收集JFR性能数据（30秒）...
✅ JFR数据收集成功: profile_3410/profile_3410.jfr (22917 bytes)
📈 分析JFR数据并生成报告...
✅ JFR数据收集成功: profile_3950/profile_3950.jfr (31963 bytes)
📈 分析JFR数据并生成报告...
✅ CPU 火焰图已生成: profile_3410/flamegraph_cpu_3410.html
✅ CPU 火焰图已生成: profile_3950/flamegraph_cpu_3950.html
✅ ALLOC 火焰图已生成: profile_3410/flamegraph_alloc_3410.html
✅ ALLOC 火焰图已生成: profile_3950/flamegraph_alloc_3950.html
✅ LOCK 火焰图已生成: profile_3950/flamegraph_lock_3950.html

📊 [并发] 进程 3950 分析结果:
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 检测到内存分配压力，建议优化对象创建模式
  3. 锁竞争分析: 未发现明显问题
✅ LOCK 火焰图已生成: profile_3410/flamegraph_lock_3410.html

📊 [并发] 进程 3410 分析结果:
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 检测到内存分配压力，建议优化对象创建模式
  3. 锁竞争分析: 未发现明显问题
📄 HTML报告已生成: profile_3950/report_3950.html
✅ 进程 3950 分析完成
📄 HTML报告已生成: profile_3410/report_3410.html
✅ 进程 3410 分析完成

📊 并发分析完成: 成功 2, 失败 0
⏱  总耗时: 31.06秒 (并发模式)

🎉 所有分析完成！
[gavin@Gavin java_profiler]$ 
```



### 自动修复权限

如果没有修改`kernel`相关参数，执行此脚本会有一个告警，可携带参数`--fix-permissions`自动修复：

```shell
[gavin@Gavin java_profiler]$ python main.py --pid "3410 3950 24305" --duration 30 --concurrent --fix-permissions
============================================================
🐛 Java性能分析工具 - Async Profiler集成
============================================================
找到 async-profiler: Async-profiler 4.1 built on Jul 21 2025
📋 找到Java进程: 3410, 24850, 3950
🔍 使用命令行参数: PID=3410 3950 24305, 时长=30秒
🚀 启用并发分析，最大线程数: 3
⚠  进程 24305 不是有效的Java进程，已跳过
🔍 将要分析的进程: 3410, 3950
⏱  每个进程分析时间: 30秒

🚀 开始并发分析 2 个进程...
🔍 [并发] 开始分析进程 3410...
📊 收集JFR性能数据（30秒）...
🔍 [并发] 开始分析进程 3950...
📊 收集JFR性能数据（30秒）...
✅ JFR数据收集成功: profile_3410/profile_3410.jfr (22863 bytes)
📈 分析JFR数据并生成报告...
✅ JFR数据收集成功: profile_3950/profile_3950.jfr (34393 bytes)
📈 分析JFR数据并生成报告...
✅ CPU 火焰图已生成: profile_3410/flamegraph_cpu_3410.html
✅ CPU 火焰图已生成: profile_3950/flamegraph_cpu_3950.html
✅ ALLOC 火焰图已生成: profile_3410/flamegraph_alloc_3410.html
✅ ALLOC 火焰图已生成: profile_3950/flamegraph_alloc_3950.html
✅ LOCK 火焰图已生成: profile_3410/flamegraph_lock_3410.html

📊 [并发] 进程 3410 分析结果:
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 检测到内存分配压力，建议优化对象创建模式
  3. 锁竞争分析: 未发现明显问题
📄 HTML报告已生成: profile_3410/report_3410.html
✅ 进程 3410 分析完成
✅ LOCK 火焰图已生成: profile_3950/flamegraph_lock_3950.html

📊 [并发] 进程 3950 分析结果:
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 检测到内存分配压力，建议优化对象创建模式
  3. 锁竞争分析: 未发现明显问题
📄 HTML报告已生成: profile_3950/report_3950.html
✅ 进程 3950 分析完成

📊 并发分析完成: 成功 2, 失败 0
⏱  总耗时: 31.11秒 (并发模式)

🎉 所有分析完成！
[gavin@Gavin java_profiler]$
```


### 交互式

#### 指定多个PID&并发

```shell
[gavin@Gavin java_profiler]$ python main.py
============================================================
🐛 Java性能分析工具 - Async Profiler集成
============================================================
找到 async-profiler: Async-profiler 4.1 built on Jul 21 2025
📋 找到Java进程: 3410, 25127, 3950

请输入要分析的Java进程PID（支持多种格式，示例如下）:
  - 留空: 分析所有找到的Java进程
  - 单个PID: 112497 (只分析这个进程)
  - 多个PID: 112497,123676 (用逗号分隔)
  - 多个PID: 112497 123676 (用空格分隔)
  - 范围: 112497-112500 (分析这个范围内的PID)
请输入: 3410,3950
请输入收集时间（秒，默认60）: 20
是否启用并发分析？(y/n，默认y):  
🚀 启用并发分析模式
请输入最大并发线程数（默认3）: 
📊 最大并发线程数: 3
🔍 将要分析的进程: 3410, 3950
⏱  每个进程分析时间: 20秒

🚀 开始并发分析 2 个进程...
🔍 [并发] 开始分析进程 3950...
📊 收集JFR性能数据（20秒）...
🔍 [并发] 开始分析进程 3410...
📊 收集JFR性能数据（20秒）...
✅ JFR数据收集成功: profile_3410/profile_3410.jfr (16719 bytes)
📈 分析JFR数据并生成报告...
✅ JFR数据收集成功: profile_3950/profile_3950.jfr (31507 bytes)
📈 分析JFR数据并生成报告...
✅ CPU 火焰图已生成: profile_3950/flamegraph_cpu_3950.html
✅ CPU 火焰图已生成: profile_3410/flamegraph_cpu_3410.html
✅ ALLOC 火焰图已生成: profile_3950/flamegraph_alloc_3950.html
✅ ALLOC 火焰图已生成: profile_3410/flamegraph_alloc_3410.html
✅ LOCK 火焰图已生成: profile_3410/flamegraph_lock_3410.html

📊 [并发] 进程 3410 分析结果:
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 未发现明显问题
  3. 锁竞争分析: 未发现明显问题
✅ LOCK 火焰图已生成: profile_3950/flamegraph_lock_3950.html
📄 HTML报告已生成: profile_3410/report_3410.html

📊 [并发] 进程 3950 分析结果:
✅ 进程 3410 分析完成
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 检测到内存分配压力，建议优化对象创建模式
  3. 锁竞争分析: 未发现明显问题
📄 HTML报告已生成: profile_3950/report_3950.html
✅ 进程 3950 分析完成

📊 并发分析完成: 成功 2, 失败 0
⏱  总耗时: 21.10秒 (并发模式)

🎉 所有分析完成！
[gavin@Gavin java_profiler]$
```


#### 指定一个PID，无并发提示

```shell
[gavin@Gavin java_profiler]$ python main.py
============================================================
🐛 Java性能分析工具 - Async Profiler集成
============================================================
找到 async-profiler: Async-profiler 4.1 built on Jul 21 2025
📋 找到Java进程: 3410, 25405, 3950

请输入要分析的Java进程PID（支持多种格式，示例如下）:
  - 留空: 分析所有找到的Java进程
  - 单个PID: 112497 (只分析这个进程)
  - 多个PID: 112497,123676 (用逗号分隔)
  - 多个PID: 112497 123676 (用空格分隔)
  - 范围: 112497-112500 (分析这个范围内的PID)
请输入: 3410
请输入收集时间（秒，默认60）: 30
🐢 分析单个进程，使用顺序模式
🔍 将要分析的进程: 3410
⏱  每个进程分析时间: 30秒
🔍 开始分析进程 3410...
📊 收集JFR性能数据（30秒）...
✅ JFR数据收集成功: profile_3410/profile_3410.jfr (23569 bytes)
📈 分析JFR数据并生成报告...
✅ CPU 火焰图已生成: profile_3410/flamegraph_cpu_3410.html
✅ ALLOC 火焰图已生成: profile_3410/flamegraph_alloc_3410.html
✅ LOCK 火焰图已生成: profile_3410/flamegraph_lock_3410.html

📊 进程 3410 分析结果:
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 未发现明显问题
  3. 锁竞争分析: 未发现明显问题
📄 HTML报告已生成: profile_3410/report_3410.html
✅ 进程 3410 分析完成
⏱  总耗时: 31.06秒 (顺序模式)

🎉 所有分析完成！
[gavin@Gavin java_profiler]$ 
```

#### 留空（分析全部Java PID）

```shell
[gavin@Gavin java_profiler]$ python3 main.py 
============================================================
🐛 Java性能分析工具 - Async Profiler集成
============================================================
找到 async-profiler: Async-profiler 4.1 built on Jul 21 2025
📋 找到Java进程: 3410, 23208, 3950

请输入要分析的Java进程PID（支持多种格式，示例如下）:
  - 留空: 分析所有找到的Java进程
  - 单个PID: 112497 (只分析这个进程)
  - 多个PID: 112497,123676 (用逗号分隔)
  - 多个PID: 112497 123676 (用空格分隔)
  - 范围: 112497-112500 (分析这个范围内的PID)
请输入: 
请输入收集时间（秒，默认60）: 600
是否启用并发分析？(y/n，默认y): 
🚀 启用并发分析模式
请输入最大并发线程数（默认3）: 
📊 最大并发线程数: 3
🔍 将要分析的进程: 3410, 23208, 3950
⏱  每个进程分析时间: 600秒

🚀 开始并发分析 3 个进程...
🔍 [并发] 开始分析进程 3410...
📊 收集JFR性能数据（600秒）...
🔍 [并发] 开始分析进程 3950...
📊 收集JFR性能数据（600秒）...
❌ 进程 23208 不存在或已终止，跳过分析
✅ JFR数据收集成功: profile_3410/profile_3410.jfr (135579 bytes)
📈 分析JFR数据并生成报告...
✅ JFR数据收集成功: profile_3950/profile_3950.jfr (173910 bytes)
📈 分析JFR数据并生成报告...
✅ CPU 火焰图已生成: profile_3950/flamegraph_cpu_3950.html
✅ CPU 火焰图已生成: profile_3410/flamegraph_cpu_3410.html
✅ ALLOC 火焰图已生成: profile_3410/flamegraph_alloc_3410.html
✅ ALLOC 火焰图已生成: profile_3950/flamegraph_alloc_3950.html
✅ LOCK 火焰图已生成: profile_3410/flamegraph_lock_3410.html
✅ LOCK 火焰图已生成: profile_3950/flamegraph_lock_3950.html

📊 [并发] 进程 3410 分析结果:
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 检测到内存分配压力，建议优化对象创建模式
  3. 锁竞争分析: 未发现明显问题
📄 HTML报告已生成: profile_3410/report_3410.html
✅ 进程 3410 分析完成

📊 [并发] 进程 3950 分析结果:
  1. CPU分析: 未发现明显问题
  2. 内存分配分析: 检测到内存分配压力，建议优化对象创建模式
  3. 锁竞争分析: 检测到锁竞争，建议减少同步块范围
📄 HTML报告已生成: profile_3950/report_3950.html
✅ 进程 3950 分析完成

📊 并发分析完成: 成功 2, 失败 1
⏱  总耗时: 601.41秒 (并发模式)

🎉 所有分析完成！
[gavin@Gavin java_profiler]$
```


### HTML报告截图

<p><img class="shadow" src="/img/java_profiler/报告示例.png" width="1200" /></p>

## 注意事项

1. **权限要求**：
   - 需要root权限或配置正确的内核参数
   - 确保当前用户有权限访问目标Java进程

2. **资源消耗**：
   - 性能分析会增加目标进程的负载
   - 并发分析会消耗更多系统资源

3. **环境要求**：
   - Linux系统（支持perf事件）
   - Python 3.6+
   - async-profiler已安装并配置

4. **兼容性**：
   - 支持大多数Java版本（Java 8+）
   - 需要与目标JVM架构匹配的async-profiler版本

## 故障排除

### 常见问题及解决方案

1. **"Process not found"错误**：
   - 目标进程可能已终止
   - 检查PID是否正确

2. **权限错误**：
   - 运行修复权限脚本
   - 手动调整内核参数

3. **火焰图生成失败**：
   - 检查async-profiler安装
   - 确认输出目录有写权限

4. **分析结果不准确**：
   - 增加分析时长
   - 确保系统负载稳定

5. **锁竞争火焰图空白**:
   - **锁事件（lock）数据量少**：在分析期间（10秒），目标Java应用程序可能没有发生明显的锁竞争或等待，因此收集到的锁事件数据非常有限
     * 锁事件通常只在发生同步操作（如synchronized块、Lock.lock()等）并且有线程等待锁时才会被记录
     * 如果应用在分析期间没有锁竞争，那么收集到的锁事件就会很少
   - **JFR文件中的锁事件数据不足**：async-profiler 在收集锁事件时，可能因为JVM没有启用相关的监控（如biased locking、锁膨胀等）或者因为锁事件本身频率较低，导致收集到的数据很少。


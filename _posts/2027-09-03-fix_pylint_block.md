---
title: pylint执行过程卡住
date: 2027-09-03 21:00:00
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pylint执行过程中遇见中文字符文件名导致任务卡住
categories:
    - [pylint]
    - [Automation]
tags:
    - pylint
    - Automation
---

# 概述

`pytest`自动化项目入口`run.py`里定义了执行`pylint`操作，但是执行`run.py`时始终卡在生成`pylint`报告阶段，但是生成的`pylint.out`文件`size`是0，等待时间非常久，迟迟没有结果。考虑到当前项目`python`代码量还没有多少（`lines` 3万+），不至于`hang`死。
手工执行了`pylint`命令，发现输出卡在了分析某个含有中文名称（备份了某个py文件，带了中文，描述备份原因）文件上，同时报：
```shell
xxx-旧备份.py contains an non-ASCII characters
```
---

# 问题

`pylint`如何忽略非`ASCII`码字符？

---

# 解决方案

在 `pylintrc` 配置文件中忽略包含中文（非`ASCII`字符）的文件，可以通过以下两种方法实现。核心思路是让 `Pylint` 跳过扫描这些文件：

## 方法一：使用 ignore-patterns 正则匹配（推荐）

在 `pylintrc` 中添加正则表达式，匹配包含非`ASCII`字符的文件名：

```ini
[MASTER]
ignore-patterns = .*[^\x00-\x7F].*  # 匹配包含非ASCII字符的文件/路径
```

## 方法二：使用 ignore 显式忽略目录/文件

如果中文文件集中在特定目录，直接忽略整个目录：

```ini
[MASTER]
ignore = 
    docs/中文目录,   # 包含中文的目录
    data/文件名带中文.txt  # 具体的中文文件
```


### 详细说明

1. **正则表达式原理**：
   - `.*[^\x00-\x7F].*` 匹配任意包含**非`ASCII`字符**的路径。
   - `\x00-\x7F` 覆盖所有`ASCII`字符（英文、数字、基本符号）。
   - `[^\x00-\x7F]` 匹配任何非`ASCII`字符（如中文）。

2. **生成配置文件**（如无现有配置）：

```shell
pylint --generate-rcfile > .pylintrc
```

3. **验证配置**：

运行 `Pylint` 并检查是否跳过目标文件：

```shell
pylint your_project/ --verbose  # 观察输出中被忽略的文件
```

---

## 替代方案（临时命令行）

直接通过命令行忽略：

```shell
pylint --ignore-patterns=".*[^\x00-\x7F].*" your_project/
```

---

### 注意事项

- **确保编码兼容**：检查系统环境是否支持 `UTF-8`（推荐 `Linux/macOS` 或 `WSL`）。
- **更新 Pylint 版本**：旧版本可能存在编码问题，升级至最新版：

```shell
pip install --upgrade pylint
```
- **重命名文件**：长期建议将中文文件名改为英文（符合 `PEP 8` 规范）。

通过以上配置，`Pylint` 将自动跳过包含中文的文件，避免因非`ASCII`字符导致的卡顿或报错。


---
title: MkDocs自动生成pytest自动化接口文档
date: 2027-06-20 23:00:00
author: Gavin Wang
top: True
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 基于MkDOcs，自动解析项目代码树结构，生成最新、完整的接口文档，代码注释风格是Google风格
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---



# MkDocs 自动化文档工具

`MkDocs` 是一个静态站点生成器，它支持`Markdown`和其他`Markdown`扩展。为了简化`MkDocs`的使用并增强其功能，基于 `MkDocs` 的二次开发工具，自动化生成项目文档，集成导航配置、日志管理、进程监控等功能，提升文档编写和维护的效率。


## 功能

- **自动生成文档导航**

该工具能够根据代码目录结构自动生成`MkDocs`所需的导航配置文件。它遍历指定的代码目录，为每个模块创建`Markdown`文件，并生成相应的导航配置。

- **合并配置文件**

工具可以自动合并基础配置和导航配置`YAML`文件，生成最终的`MkDocs`配置文件。这简化了配置管理，确保所有配置项的一致性和准确性。

- **代码目录结构分析**

分析项目的代码目录结构，为每个模块生成相应的文档结构。这有助于保持文档的组织和一致性，确保文档与代码的同步更新。

## 使用流程

- **初始化项目结构**：定义项目的目录结构，包括页面、工具和其他模块的存放路径。
- **生成导航配置**：根据代码目录结构自动生成导航配置文件。
- **合并配置文件**：将基础配置和导航配置合并，生成最终的`MkDocs`配置文件。
- **准备文档文件**：复制必要的文档文件，如索引文件，到文档目录。
- **启动MkDocs服务**：启动`MkDocs`服务，预览和测试文档。


---

## 目录结构

```plaintext
.
├── docs/                    # 生成的文档目录（自动生成）
├── generate_mkdocs_nav.py   # 导航配置生成器
├── generate_mkdocs.py       # MkDocs 文件预处理器
├── index.md                 # 文档首页模板
├── __init__.py
├── logs/                    # 日志文件
├── log_utils.py             # 日志管理模块
├── merge_mkdocs_yaml.py     # YAML 配置合并器
├── mkdocs_base.yml          # 基础 MkDocs 配置
├── mkdocs_path.py           # 全局路径管理
├── README.md
├── run_mkdocs.py            # 主运行入口
└── site/                    # 生成的静态HTML文件目录（自动生成）
```

---

## 设计架构

### 工作流

<img class="shadow" src="/img/in-post/MkDocs/工作流.png" width="1200" />

### 系统top图

<img class="shadow" src="/img/in-post/MkDocs/系统拓扑图.png" width="1200" />

### 类图

#### 工具类图


<img class="shadow" src="/img/in-post/MkDocs/类图.png" width="1200" />

#### 核心模块类图

<img class="shadow" src="/img/in-post/MkDocs/核心模块类图.png" width="1200" />



### 文件调用关系说明

<img class="shadow" src="/img/in-post/MkDocs/文件调用关系.png" width="1200" />



### 活动图(函数级调用链)

<img class="shadow" src="/img/in-post/MkDocs/函数级调用链.png" width="1200" />


---

## 核心功能

### 自动化导航生成

- **脚本**: `generate_mkdocs_nav.py`
- 功能:
  - 遍历 `pages` 和 `utils` 目录，生成 Markdown 文件。
  - 根据目录结构生成层级导航配置（`mkdocs_nav.yml`）。
  - 跳过隐藏文件（以 `.` 开头的目录/文件）。

### 配置文件合并

- **脚本**: `merge_mkdocs_yaml.py`
- 功能:
  - 合并基础配置（`mkdocs_base.yml`）和导航配置（`mkdocs_nav.yml`）。
  - 使用 `ruamel.yaml` 保留原始格式和注释。

### 日志管理

- **模块**: `log_utils.py`
- 功能:
  - 按日期分割日志文件（每天一个文件）。
  - 自动清理 7 天前的旧日志。
  - 支持日志轮转（单个文件最大 20MB）。

### 进程管理

- **脚本**: `run_mkdocs.py`
- 功能:
  - 检查端口占用并终止冲突进程。
  - 后台启动 MkDocs 服务（支持 Windows/Linux）。
  - 通过 PID 文件管理进程生命周期。
  - 优雅处理 `Ctrl+C` 信号，自动清理资源。



---

## 快速开始

### 依赖安装

```bash
pip install mkdocs -U
pip install "mkdocstrings[python]" -U
pip install mkdocs-material -U
pip install ruamel.yaml -U
pip install psutil -U
```

### 运行命令

```bash
python run_mkdocs.py
```

### 自定义配置

1. **修改主题**: 编辑 `mkdocs_base.yml` 中的 `theme` 部分。
2. **扩展导航**: 在 `pages` 目录中添加 `.md` 文件，工具会自动识别。
3. **调整日志策略**: 修改 `log_utils.py` 中的 `maxBytes` 和 `backupCount`。


### 文档浏览效果

<img class="shadow" src="/img/in-post/MkDocs/预览效果.png" width="1200" />

---

## 高级功能

### 多环境支持

- **Windows**: 使用 `subprocess.DETACHED_PROCESS` 启动后台进程。
- **Linux**: 使用 `nohup` 和 `os.setsid` 实现守护进程。

### 安全退出

- 发送 `Ctrl+C` 时，工具会：
  1. 终止 `MkDocs` 服务进程。
  2. 删除 `PID` 文件。
  3. 清理临时目录。

---

## 故障排查

### 常见问题

1. **端口冲突**:

```bash
lsof -i :8000  # 检查占用进程
kill -9 <PID>  # 强制终止
```

2. **导航未更新**:

   - 确保文件保存在 `pages` 或 `utils` 目录。
   - 删除 `mkdocs_nav.yml` 后重新运行工具。

3. **执行mkdocs build --clean 报错**

如下面的一个错误示例：

   ```shell
ERROR - mkdocstrings: testcasebase.api.PC.batch_upload.batch_upload could not be found
ERROR - Error reading page 'testcasebase/api/PC/batch_upload/batch_upload.md':
ERROR - Could not collect 'testcasebase.api.PC.batch_upload.batch_upload'
```

如果发现类似上述错误提示，查看对应源码目录下`py`文件也是对的，对应`md`文件也存在，且`md`文件内容也是正确，且在`python`命令行里也可以正常`import`此模块，说明一个问题：
对应目录下缺少 `__init__.py`文件。
比如上面错误信息中，'testcasebase/api/PC/batch_upload/batch_upload.py'所在目录，并没有`__init__.py`文件，如果添加了此文件，则上述错误消失。
这说明`MkDocs`对`python`的编码规范要求还是比较高的。

### 日志查看

#### 查看方法

```bash
# Windows
logs/mkdocs_service.log

# Linux
tail -f logs/mkdocs_service.log
```

#### 运行日志参考

以 `Windows`平台下运行程序作为示例。

##### 屏显信息

**没有相同服务在运行，打屏信息如下：**

```shell
F:\workspace\MkDocs_tool\automation_api\mkdoc_tool>python run_mkdocs.py
启动 mkdocs serve...
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\site
Building prefix dict from C:\User\Gavin\AppData\Roaming\Python\Python312\site-packages\jieba\dict.txt ...
Loading model from cache C:\User\Gavin\AppData\Local\Temp\jieba.cache
Loading model cost 1.6874887943267822 seconds.
Prefix dict has been built succesfully.
INFO    -  Documentation built in 14.70 seconds
mkdocs serve 已启动，PID: 6100

收到 Ctrl+C 信号，正在终止 mkdocs serve...
删除 PID 文件: F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_serve.pid
```

**有相同服务存在，运行时打屏信息参考如下：**

```shell
F:\workspace\MkDocs_tool\automation_api\mkdoc_tool>python run_mkdocs.py
找到其他实例，PID: 7644, 正在终止...
PID 文件中的进程 2380 不存在或与当前进程相同，跳过
删除 PID 文件: F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_serve.pid
启动 mkdocs serve...
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\site
Building prefix dict from C:\User\Gavin\AppData\Roaming\Python\Python312\site-packages\jieba\dict.txt ...
Loading model from cache C:\User\Gavin\AppData\Local\Temp\jieba.cache
Loading model cost 1.6803882122039795 seconds.
Prefix dict has been built succesfully.
INFO    -  Documentation built in 9.16 seconds
mkdocs serve 已启动，PID: 6764
```


##### 日志文件记录内容

**没有相同服务在运行，日志记录内容参考如下：**

```shell
[2027-06-17 21:36:56] [mkdocs_path.py:77][INFO] 
======================================== 路径配置清单 ========================================
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] current_dir               → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] docs_path                 → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\docs
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] index_md_path             → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\index.md
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] log_dir                   → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\logs
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] log_file_path             → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\logs\mkdocs_service.log
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] mkdocs_base_yaml          → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_base.yml
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] mkdocs_nav_yaml           → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_nav.yml
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] mkdocs_pages_path         → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\pages
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] mkdocs_testcasebase_path  → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\testcasebase
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] mkdocs_utils_path         → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\utils
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] mkdocs_yaml               → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs.yml
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] pid_file_path             → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_serve.pid
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] project_pages_path        → F:\workspace\MkDocs_tool\automation_api\pages
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] project_root              → F:\workspace\MkDocs_tool\automation_api
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] project_testcasebase_path → F:\workspace\MkDocs_tool\automation_api\testcasebase
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] project_utils_path        → F:\workspace\MkDocs_tool\automation_api\utils
[2027-06-17 21:36:56] [mkdocs_path.py:79][INFO] site_path                 → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\site
[2027-06-17 21:36:56] [mkdocs_path.py:80][INFO] 
==========================================================================================

[2027-06-17 21:36:58] [generate_mkdocs.py:40][INFO] 成功创建目录: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\docs)
[2027-06-17 21:36:58] [generate_mkdocs_nav.py:20][INFO] 完成初始化导航配置，开始遍历源码目录结构
[2027-06-17 21:36:58] [merge_mkdocs_yaml.py:24][INFO] 读取基础 YAML 文件： (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_base.yml)
[2027-06-17 21:36:58] [merge_mkdocs_yaml.py:32][INFO] 读取需要追加的 YAML 文件：(F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_nav.yml)
[2027-06-17 21:36:58] [merge_mkdocs_yaml.py:40][INFO] 检查并追加内容
[2027-06-17 21:36:58] [merge_mkdocs_yaml.py:51][INFO] 将合并后的数据写入输出文件： (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs.yml)
[2027-06-17 21:36:58] [generate_mkdocs.py:99][INFO] YAML配置文件合并完成，已保存到： (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs.yml)
[2027-06-17 21:36:58] [generate_mkdocs.py:52][INFO] 完成文件: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\index.md) 复制到: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\docs)
[2027-06-17 21:36:58] [generate_mkdocs.py:86][INFO] 完成文件夹: (F:\workspace\MkDocs_tool\automation_api\pages) 复制到: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool)
[2027-06-17 21:36:58] [generate_mkdocs.py:86][INFO] 完成文件夹: (F:\workspace\MkDocs_tool\automation_api\utils) 复制到: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool)
[2027-06-17 21:36:58] [generate_mkdocs.py:86][INFO] 完成文件夹: (F:\workspace\MkDocs_tool\automation_api\testcasebase) 复制到: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool)
[2027-06-17 21:36:58] [run_mkdocs.py:265][INFO] 启动 mkdocs serve...
[2027-06-17 21:37:28] [run_mkdocs.py:167][INFO] mkdocs build 完成
INFO    -  Building documentation...
INFO    -  Cleaning site directory
Building prefix dict from C:\User\Gavin\AppData\Roaming\Python\Python312\site-packages\jieba\dict.txt ...
Loading model from cache C:\User\Gavin\AppData\Local\Temp\jieba.cache
Loading model cost 1.5622820854187012 seconds.
Prefix dict has been built succesfully.
INFO    -  Documentation built in 9.23 seconds
INFO    -  [21:37:39] Watching paths for changes: 'docs', 'mkdocs.yml'
INFO    -  [21:37:39] Serving on http://192.168.221.230:8000/
[2027-06-17 21:38:27] [run_mkdocs.py:207][INFO] 收到 Ctrl+C 信号，正在终止 mkdocs serve...
[2027-06-17 21:38:27] [run_mkdocs.py:96][INFO] 终止进程树 PID=6376
[2027-06-17 21:38:27] [run_mkdocs.py:99][INFO] 成功终止进程树 PID=6376
[2027-06-17 21:38:27] [run_mkdocs.py:212][INFO] 删除 PID 文件: F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_serve.pid
```

**有相同服务在运行，日志记录内容参考如下：**

```shell
[2027-06-17 21:39:52] [mkdocs_path.py:77][INFO] 
======================================== 路径配置清单 ========================================
[2027-06-17 21:39:52] [mkdocs_path.py:79][INFO] current_dir               → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] docs_path                 → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\docs
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] index_md_path             → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\index.md
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] log_dir                   → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\logs
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] log_file_path             → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\logs\mkdocs_service.log
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] mkdocs_base_yaml          → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_base.yml
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] mkdocs_nav_yaml           → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_nav.yml
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] mkdocs_pages_path         → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\pages
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] mkdocs_testcasebase_path  → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\testcasebase
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] mkdocs_utils_path         → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\utils
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] mkdocs_yaml               → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs.yml
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] pid_file_path             → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_serve.pid
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] project_pages_path        → F:\workspace\MkDocs_tool\automation_api\pages
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] project_root              → F:\workspace\MkDocs_tool\automation_api
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] project_testcasebase_path → F:\workspace\MkDocs_tool\automation_api\testcasebase
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] project_utils_path        → F:\workspace\MkDocs_tool\automation_api\utils
[2027-06-17 21:40:23] [mkdocs_path.py:79][INFO] site_path                 → F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\site
[2027-06-17 21:40:23] [mkdocs_path.py:80][INFO] 
==========================================================================================

[2027-06-17 21:40:24] [run_mkdocs.py:225][INFO] 找到其他实例，PID: 7644, 正在终止...
[2027-06-17 21:40:25] [run_mkdocs.py:144][INFO] PID 文件中的进程 2380 不存在或与当前进程相同，跳过
[2027-06-17 21:40:25] [run_mkdocs.py:153][INFO] 删除 PID 文件: F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_serve.pid
[2027-06-17 21:40:25] [generate_mkdocs.py:36][INFO] 完成文档目录: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\docs) 的清理
[2027-06-17 21:40:25] [generate_mkdocs.py:36][INFO] 完成文档目录: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\site) 的清理
[2027-06-17 21:40:25] [generate_mkdocs.py:36][INFO] 完成文档目录: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\pages) 的清理
[2027-06-17 21:40:25] [generate_mkdocs.py:36][INFO] 完成文档目录: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\utils) 的清理
[2027-06-17 21:40:25] [generate_mkdocs.py:40][INFO] 成功创建目录: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\docs)
[2027-06-17 21:40:25] [generate_mkdocs_nav.py:20][INFO] 完成初始化导航配置，开始遍历源码目录结构
[2027-06-17 21:40:25] [merge_mkdocs_yaml.py:24][INFO] 读取基础 YAML 文件： (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_base.yml)
[2027-06-17 21:40:25] [merge_mkdocs_yaml.py:32][INFO] 读取需要追加的 YAML 文件：(F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs_nav.yml)
[2027-06-17 21:40:25] [merge_mkdocs_yaml.py:40][INFO] 检查并追加内容
[2027-06-17 21:40:25] [merge_mkdocs_yaml.py:51][INFO] 将合并后的数据写入输出文件： (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs.yml)
[2027-06-17 21:40:25] [generate_mkdocs.py:99][INFO] YAML配置文件合并完成，已保存到： (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\mkdocs.yml)
[2027-06-17 21:40:25] [generate_mkdocs.py:52][INFO] 完成文件: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\index.md) 复制到: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool\docs)
[2027-06-17 21:40:25] [generate_mkdocs.py:86][INFO] 完成文件夹: (F:\workspace\MkDocs_tool\automation_api\pages) 复制到: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool)
[2027-06-17 21:40:25] [generate_mkdocs.py:86][INFO] 完成文件夹: (F:\workspace\MkDocs_tool\automation_api\utils) 复制到: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool)
[2027-06-17 21:40:25] [generate_mkdocs.py:86][INFO] 完成文件夹: (F:\workspace\MkDocs_tool\automation_api\testcasebase) 复制到: (F:\workspace\MkDocs_tool\automation_api\mkdoc_tool)
[2027-06-17 21:40:25] [run_mkdocs.py:265][INFO] 启动 mkdocs serve...
[2027-06-17 21:40:37] [run_mkdocs.py:167][INFO] mkdocs build 完成
INFO    -  Building documentation...
INFO    -  Cleaning site directory
Building prefix dict from C:\User\Gavin\AppData\Roaming\Python\Python312\site-packages\jieba\dict.txt ...
Loading model from cache C:\User\Gavin\AppData\Local\Temp\jieba.cache
Loading model cost 1.5781280994415283 seconds.
Prefix dict has been built succesfully.
INFO    -  Documentation built in 8.53 seconds
INFO    -  [21:40:47] Watching paths for changes: 'docs', 'mkdocs.yml'
INFO    -  [21:40:47] Serving on http://192.168.221.230:8000/
```

---

## 设计理念

- **自动化**: 减少手动配置，目录变动自动同步到文档。
- **健壮性**: 完善的进程管理和日志轮转机制。
- **跨平台**: 兼容 `Windows` 和 `Linux` 系统。

---

> 通过此工具，开发者可专注于内容创作，无需手动维护 `MkDocs` 配置，显著提升文档项目的可维护性。


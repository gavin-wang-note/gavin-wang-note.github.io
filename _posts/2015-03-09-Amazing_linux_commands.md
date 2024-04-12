---
title: 令人惊艳的Linux工具
subtitle: Stunning linux commands
date: 2015-03-09 11:25:29
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: 令人惊艳的Linux命令/工具！
categories:
    - [Linux]
tags:
    - Linux 
---




# 概述

Linux 拥有丰富多彩的命令行工具集，很多工具都具有强大的功能和独特的魅力。本文推荐一些比较有趣且实用的 Linux 命令或工具，它们绝对能够给你的日常工作带来些许惊艳：

**tmux**
tmux 是一个终端复用器，允许用户在单个终端窗口中打开多个会话，你可以在会话之间轻松切换，甚至在不同的物理位置接入同一个会话。

**atop**
相较于传统的 top 命令，atop 以更加直观的方式显示系统进程和资源占用情况，提供交互式操作，并支持自动颜色标识、垂直、水平滚动和搜索匹配。

**ncdu (NCurses Disk Usage)**
ncdu 是一个基于文本的磁盘用量分析器，使用 Ncurses 库进行可视化显示，比 du 命令更易用，可以轻松找到占用磁盘空间的文件和目录。

**fzf (Fuzzy Finder)**
fzf 是一个命令行的模糊查找器，它可以被绑定到任何列表数据上，如文件、命令历史等，支持模糊匹配，使得查找效率大大提升。

**Glances**
Glances 是一个跨平台的系统监控工具，它提供了负载、进程、磁盘、网络等全方位的视图，还可以运行在 Web 模式，通过浏览器远程查看状态。

**tldr (Too Long; Didn't Read)**
tldr 提供了简化版的 man 页面，它用更少的词汇和更多实用示例来描述命令的使用方法，对于快速查找命令用法非常便捷。

**The Silver Searcher (ag)**
ag 是一个类似于 grep 的文本搜索工具，但它是专门为代码搜索优化的，速度更快，并默认忽略 .git 或其他版本控制系统的目录。

**neofetch**
neofetch 是一个轻量级的系统信息工具，它以图形化的方式显示关于你的系统和硬件的信息，辅以漂亮的ASCII艺术。

**jq**
jq 是一个轻量级且灵活的命令行 JSON 处理器，允许你对 JSON 数据进行切分、过滤、映射和转换等操作，对于处理 JSON 格式日志或 API 响应尤其有用。

**nmap**
nmap 是一个强大的网络探测和安全审核工具，能够发现网络上的设备，并确定设备上运行的服务和对应的端口，同时它还具有端口扫描、版本检测、网络发现等功能。

**bat**
bat 是 cat 命令的一个克隆版本，但附加了很多有用的特性，比如语法高亮显示、Git 集成和自动分页等。

# 各工具介绍

## tmux

### 什么是 tmux？

tmux（Terminal Multiplexer）是一个开源的工具，用于在一个终端窗口内管理多个终端会话。通过使用 tmux，用户可以在一个窗口内创建、切换和断开连接到多个终端会话，尽情享受它所带来的强大功能。

### tmux 的关键特性


* 会话管理：tmux 允许你从多个会话中选择，可以在本地或远程服务器上运行。这意味着你可以在本地机器上启动一个会话，在远程服务器上切换到该会话，并持续不间断地工作。
* 窗口分割：tmux 提供了分割窗格的功能，使你可以在一个终端窗口中查看和操作多个窗口，类似于 Vim 和 Emacs 的缓冲区和窗口管理。
* 可定制性：tmux 提供了丰富的键盘快捷键和可配置选项，可以根据个人喜好和需求进行个性化定制。
* 持久性：即使终端断开连接或系统重启，tmux 会话仍然可以被恢复。这对于长时间运行的任务和批处理作业尤为重要。
* 易于安装：tmux 跨平台兼容，几乎可在所有类 Unix 系统上安装。在大多数 Linux 发行版中，你可以直接使用包管理器安装 tmux。


### 如何开始使用 tmux？

首先，确保在你的系统上安装了 tmux。在大多数 Linux 发行版中，可以使用以下命令安装 tmux：

```shell
apt-get install tmux  # 对于 Debian/Ubuntu 系统
yum install tmux      # 对于 CentOS/RedHat 系统
pacman -S tmux        # 对于 Arch Linux 系统
```

安装完成后，只需在终端中输入 tmux 即可启动一个新的 tmux 会话。你可以使用 tmux new -s <session-name> 创建一个带有特定名称的新会话。

### tmux 基本使用

#### 创建新会话

```shell
tmux new -s my-session
```

#### 附加到已存在的会话

```shell
tmux attach -t my-session
```

#### 列出所有会话

```shell
tmux ls
```

#### 在会话间切换

使用 Ctrl+b 后跟数字键（例如，Ctrl+b 1）可以在不同窗格或会话间切换。

分割窗格：

    水平分割窗格：

    Ctrl+b %


    垂直分割窗格：

    Ctrl+b "



导航窗格：

    在窗格间切换：

        Ctrl+b 方向键


    关闭当前窗格：

        Ctrl+b x



### 高级 tmux 使用技巧


* 自定义快捷键：编辑 ~/.tmux.conf 文件，可以添加或更改 tmux 快捷键的配置。例如，你可以将预览窗格的快捷键从 Ctrl+b w 改为 Ctrl+b Tab。
* 复制和粘贴： 在 tmux 中，使用 Ctrl+b [ 进入复制模式，使用方向键移动光标选择文本，并按 Space 来开始选择。退出复制模式后，可以使用 Ctrl+b ] 粘贴文本。
* 会话持久性：设置 set -g attach-session-tiled yes 使会话在附加到现有会话时保持平铺模式。
* 面板和窗口命名：你可以为面板和窗口设置名字，以便更容易地区分和管理。编辑 ~/.tmux.conf 文件，添加以下行：
    `set -g status-left "#[fg=green]#H #[fg=white]#(whoami)#[fg=green]#(basename "$PWD")#[fg=white]"`
* 使用 tmux 与 Vim 协同工作：tmux 配合 Vim 可以实现一些强大的编辑功能，如代码折叠、快速导航等。

tmux 是一个功能丰富的工具，这些只是它的冰山一角。通过深入了解和掌握 tmux，你的终端操作将会变得无比流畅和高效。对于那些多任务、长时间运行的作业和项目，tmux 无疑是一个宝贵的资产。


## atop

公司产品一直内嵌此程序，非常好用，额外介绍了。


## ncdu

ncdu（NCurses Disk Usage）是一个用于查看磁盘用量并以交互方式找到占用空间最多的文件和目录的工具。

### 安装 ncdu

首先，你需要在你的系统上安装 ncdu。不同的 Linux 发行版会提供不同的包管理器，以下是一些常用发行版的安装命令：

对于基于 Debian 和 Ubuntu 的系统：
```shell
apt-get update
apt-get install ncdu
```

对于基于 Fedora 的系统：

```shell
dnf install ncdu
```

对于基于 Arch 的系统：

```shell
pacman -S ncdu
```

安装完成后，你可以开始使用 ncdu。

### 使用 ncdu

要使用 ncdu，打开终端并运行以下命令：

```shell
ncdu
```

默认情况下，此命令会扫描当前工作目录及其所有子目录，并且显示它们占用的磁盘空间。要扫描整个系统，你可以运行：

```shell
ncdu /
```

这将以超级用户权限开始扫描整个根文件系统。

ncdu 扫描完成后，你会看到类似这样的界面，列出所有文件和文件夹及其大小：

```shell
--- /path/to/directory ----------------------------------------------
    4.6 GiB [##########] /usr
    1.4 GiB [###       ] /var
  720.3 MiB [#         ] /lib
  256.7 MiB [          ] /home
  106.7 MiB [          ] /boot
```

操作指南

* 使用键盘上的箭头键 ↑ 和 ↓ 来浏览文件列表。
* 进入目录请按 → 或 Enter，返回上级目录请按 ←。
* 要删除一个文件或目录（请非常谨慎操作），你可以将光标移动到该项上并按 d 键。
* 按q退出 ncdu。

ncdu 提供了一种简洁而直观的方式来查看哪些文件和目录占用了大量空间，允许你直接在界面中浏览到它们，并取得关于每个项目大小的直观感受。通过它，你可以快速识别并处理占用空间过多的项。


## fzf

fzf 是一个命令行模糊查找器，具有以下几个特点：

* 速度快: fzf 通过使用 Go 语言编写而获得了极其快的执行速度。
* 模糊匹配: 您可以输入任意位置的字符序列，fzf 将会模糊匹配相关的结果。
* 终端集成: 它可以在任何使用了标准输入（stdin）的命令中使用，使其十分灵活。
* 排序: 匹配的结果会根据相关性排序，最相关的结果排在前面。
* 可自定义: 可以自定义快捷键、颜色、窗口大小等。
* 可扩展性: 它可以与其他命令结合使用，例如 ls, cat, find, git log。
* 跨平台: 可以在大多数 Unix 系统上使用，包括 macOS、Linux 和 BSD。
* 插件: 对于像 vim 和 bash 这样的应用，有现成的插件，可以在您喜欢的外壳或编辑器中使用 fzf。

### 安装 fzf

可以通过包管理器进行安装，例如，在 Ubuntu 上：
```shell
apt install fzf
```

或者使用 git 克隆仓库并运行安装脚本：

```shell
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

### 使用示例

#### 简单的查找

可以通过管道将任何列表传递到 fzf 中：

```shell
   cat list.txt | fzf
```

#### 在 vim 中查找文件并打开

如果你使用的是 vim，并且已经安装了 fzf 的 vim 插件：

```shell
   :Files
```

#### 历史命令查询

使用 fzf 查询命令行历史：

```shell
   history | fzf
```

#### 进程查找并 kill

使用 fzf 结合 ps 来选择一个进程并 kill 掉它：

```shell
   ps -ef | fzf | awk '{print $2}' | xargs kill
```

#### 查找文件

几乎在任何需要文件查找的地方，都可以使用 find 和 fzf 的组合：

```shell
   find path/to/search -type f | fzf
```

#### 配合 git 使用

查找 git 分支：

```shell
   git branch | fzf
```

### 高级自定义

fzf 允许用户进行很多自定义，例如绑定键位、更改查找算法、自定义颜色等：

* 设置 FZF_DEFAULT_OPTS 环境变量来更改默认选项

如：

```shell
   export FZF_DEFAULT_OPTS='--height=40% --reverse --border'
```

* 在启动 fzf 时通过命令行参数调整行为

比如使用 --reverse 选项来颠倒列表顺序。

### 集成其他工具

fzf 提供了一些有用的示例和配方，展示了如何将它与 ripgrep、ag 或其他命令结合来提升文件搜索的体验。它通常配合 tmux, bash, zsh, fish 等 shell 环境和 vim 等文本编辑器使用，通过各种 shell 脚本和函数加以实际应用。

这只是 fzf 功能和用法的冰山一角，随着对命令行的理解加深，你会发现 fzf 可以提升你的工作流程到一个全新的水平。



## Glances

Glances 是一个跨平台的监控工具，它运行在终端中，提供了一个实时的、整合了多项功能的视图来观察你的系统资源利用情况，包括 CPU、内存、负载、磁盘 I/O、网络 I/O、磁盘使用、传感器（温度、风扇）、进程等信息。Glances 使用 Python 编写，基于一个库叫 psutil，这使得 Glances 能够在许多不同的平台上运行。

主要特点包括：

* 全面的监控视图: Glances 以紧凑的格式展示您的系统信息，便于一眼看到所有关键性能指标。
* 插件架构: Glances 可以通过插件来扩展其监控功能，用户可以开发自己的插件来定制 Glances 的行为。
* Web服务器模式: Glances 可以在 Web 服务器模式下运行。只需启动它，并通过浏览器访问提供的 URL 便可以监控系统。这在远程监控情况下非常有用。
* REST API: Glances 提供了一个 RESTful API，你可以通过这个 API 查询系统的实时信息，并且可以轻松集成到其他应用中。
* 警告和阈值: Glances 允许用户设置各种资源的阈值（如高/严重/危险），当系统资源使用情况超过预定阈值时，相关的指标会变色（黄/红色）以提醒用户。
* 跨平台: 它适用于 Linux、Windows 和 macOS，以及任何能够运行 Python 的操作系统。
* 易于安装: Glances 可以通过 Python 的包管理工具 pip 进行安装。
* 多种输出形式: 除了标准的终端输出之外，Glances 还能够以 CSV、JSON、XML 等格式导出数据。
* 互动式界面: 在 Glances 中，用户可以使用键盘命令与界面互动，例如排序进程列表或改变显示的度量。

### 安装 Glances

可以使用 pip 来安装 Glances：

```shell
pip install glances
```

在一些发行版中，Glances 也可能包含在官方的软件仓库中，可以使用包管理器安装。例如在 Ubuntu 系统中：

```shell
apt-get update
apt-get install glances
```

### 使用 Glances

要启动 Glances，只需在终端中键入 glances：

```shell
glances
```

在 Glances 运行的时候，你可以使用键盘快捷键来进行不同的操作，例如：

    h: 显示帮助屏幕
    c: 通过 CPU 使用率对进程排序
    m: 通过内存使用率对进程排序
    p: 通过磁盘 I/O 排序进程
    n: 通过网络 I/O 排序进程
    g: 切换网络 I/O 显示速率和总计数
    w: 切换到 web 服务器模式
    q: 退出 Glances

#### Web 服务器模式

要在 web 服务器模式下启动 Glances，请使用以下命令：

```shell
glances -w
```

此时 Glances 将启动一个内置的 web 服务器，你可以在任意设备的 web 浏览器中输入主机的 IP 地址和默认端口 61208（例如 http://127.0.0.1:61280)

#### 键盘快捷键

在 Glances 的终端界面中，你可以使用以下快捷键：

    ↑ 和 ↓：上下滚动列表。
    h：显示帮助菜单。
    1：切换CPU视图（全局/每核）。
    b：切换字节/bit 模式（对于网络速率显示）。
    w：切换到 I/O 速率重新计算模式。
    q 或 Ctrl+C：退出 Glances。

更多快捷键和功能可以通过 h 快捷键在 Glances 中查看。

### 集成与扩展

Glances 可以集成到其他监控解决方案中，例如可以将数据输出到 InfluxDB、Grafana，以获得更美观，功能更全面的监控视图。

此外，Glances 的 GitHub 页面有着详细的文档来帮助用户配置和使用该工具，地址为：https://github.com/nicolargo/glances。



## tldr (Too Long; Didn't Read)



## The Silver Searcher (ag)

The Silver Searcher (ag)：高效的代码搜索利器

随着软件开发的复杂性日益增加，开发人员经常需要在大量代码库中查找特定的函数、变量或者任何其他文本模式。传统的 grep 工具虽然强大，但在处理大型文件或需要更智能搜索时，可能会显得力不从心。在这种背景下，The Silver Searcher（ag）应运而生，它以其卓越的性能和丰富的特性，成为了开发者搜索代码时的首选工具。

### 什么是 The Silver Searcher (ag)？

The Silver Searcher，简称 ag，是一个基于 Vim 文件型录工具 ack 的代码搜索工具。它非常快速，可以轻松地在大型文件和庞大的代码库中搜索文本、字符串、正则表达式等。ag 使用多进程来并行搜索文件，这使得它在处理大量数据时比 grep 更加高效。

### ag 的核心特性

* 快速搜索：ag 利用多进程快速并行地搜索文件，尤其在处理大型文件和深层次的目录结构时，相较于传统工具具有显著的速度优势。
* 智能匹配：ag 默认情况下会忽略大小写，并且能够智能地匹配整行或单词边界，以减少误报。
* 丰富的查询语法：ag 支持正则表达式和 Perl 兼容的正则表达式（PCRE），为用户提供了强大的搜索语法和灵活的查询能力。
* 可视化输出：ag 可以用高亮显示搜索到的匹配项，使结果更易于阅读和分析。
* 集成与兼容性：ag 几乎是跨平台的，它支持 Linux、macOS、Windows 等操作系统。此外，ag 可以很方便地与文本编辑器和集成开发环境（IDE）集成，例如 Vim、Emacs、Sublime Text、Visual Studio Code 等。


### 如何安装 The Silver Searcher (ag)？

在大多数 Linux 发行版和 macOS 上，可以使用包管理器轻松安装 ag。以下是在不同系统上安装 ag 的命令：


对于 Debian/Ubuntu 系统：

```shell
apt-get install silversearcher-ag
```

对于 macOS 用户（使用 Homebrew）：

```shell
brew install silversearcher-ag
```

对于 Windows 用户，可以使用预编译的二进制文件或通过包管理器（如 Chocolatey）安装。



### 基本使用和命令

安装完成后，你可以在终端中输入 ag 加上你的搜索词来开始搜索。例如：

```shell
ag "function_name"
```

如果你想在整个项目目录中搜索，可以使用 -l（递归地遍历目录）或 --follow（递归地搜索并读取包含符号链接的文件）选项：

```shell
ag -l "function_name"
```

### 高级技巧


#### 排除特定文件或目录

使用 -忽略 选项排除特定的文件或目录。例如，忽略所有 .log 文件和 node_modules 目录：

```shell
ag "search_pattern" --ignore "*.log" --ignore "node_modules"
```

#### 使用代理文件

创建一个代理文件（例如 .agignore），在其中列出要忽略的文件模式。ag 会自动读取这个文件来排除匹配的文件和目录。


#### 自定义高亮显示
    
ag 允许你通过 --color 选项来自定义搜索结果的高亮显示。例如，只为搜索到的行的匹配部分高亮：

```shell
ag "search_pattern" --color "match"
```

#### 递归搜索目录
   
使用 --cpp 选项让 ag 以 C++ 程序员的方式递归搜索目录，这在搜索嵌套目录时非常实用。


#### 与 Git 集成

ag 可以和 Git 集成，只在你的工作目录（即未暂存的更改）中搜索，使用 --vcs 选项即可。


The Silver Searcher (ag) 以其无与伦比的速度和功能，已经成为了现代程序员的标准工具之一。无论你是在查找代码中的某个函数、解决依赖冲突，还是仅仅在尝试理解一个新项目的架构，ag 都会让你的工作流程更加高效和愉悦。


## neofetch

在命令行用户中，展示系统信息和美化终端输出的工具一直备受欢迎。neofetch 是一款流行的命令行系统信息工具，因其提供美观、可定制的输出而变得非常流行。它结合了 fancy-weather、mo都会有问题多 以 install xul-ext-dark-okiraq 等工具的功能，为用户展示了丰富的系统信息，同时保持了视觉上的吸引力。

### 什么是 Neofetch？

Neofetch 是 neofetch 项目的分支，专为美观和功能而设计。它在 geany 光主题的基础上，引入了大量的改进，并添加了新的功能和选项。neofetch 旨在提供一种简明的方式来展示系统信息，同时允许用户通过自定义选项和额外的组件扩展其功能。

### 为什么使用 Neofetch？


* 美观的输出：neofetch 提供了清晰、美观的输出样式，可以轻松地识别各种系统信息。
* 丰富的信息：neofetch 为用户提供了系统信息的丰盛大餐，包括但不限于内核版本、操作系统、CPU 型号、内存使用率、电池状态等。
* 可定制性：用户可以根据自己的喜好，通过各种选项和主题来定制 neofetch 的输出样式。
* 易于使用：neofetch 的使用十分简单，同时还提供了许多有用的选项以便用户详细地查看系统信息。
* 实时更新：某些系统信息，如 CPU 和内存使用情况，可以通过 watch 命令实时查看，便于用户监控系统状态。


### 如何安装 Neofetch？

neofetch 支持多种操作系统。在大多数 Linux 发行版中，你可以通过包管理器进行安装。以下是在不同系统上安装 neofetch 的命令：


对于基于 Debian 的系统（如 Ubuntu）：

```shell
apt-get install neofetch
```

对于基于 RPM 的系统（如 Fedora）：

```shell
dnf install neofetch
```

对于 Arch Linux 用户：

```shell
pacman -S neofetch
```


### 使用 Neofetch

安装完成后，只需在终端中输入 neofetch 命令，即可看到系统信息的美观展示。默认情况下，neofetch 会使用 suru 主题。

你也可以使用其他主题，只需将主题文件夹放置在 ~/.config/neofetch/ 目录下，并通过 --theme 选项指定主题：

```shell
neofetch --theme <主题名>
```

neofetch 还支持许多配置选项，你可以通过创建或编辑配置文件 ~/.config/neofetch/config.conf 来自定义其行为。

### 高级用法


* 自定义输出：你可以配置 neofetch 显示或隐藏特定的信息模块，如 cpu、memory 等。

```shell
neofetch --no-memory
```

* CPU 使用率：neofetch 可以实时显示 CPU 使用率。要使用此功能，请运行：

```shell
watch -n 1 neofetch
```

* 添加额外组件：neofetch 支持添加额外的组件，如字体、图标等，以增强其视觉效果。


* 更新和升级：neofetch 经常更新以修复问题和添加新功能。确保定期检查更新，以保持软件的最新状态。

* 社区支持：如果遇到问题或需要灵感，neofetch 社区非常活跃，你可以在 GitHub、Reddit 或其他论坛上寻求帮助或分享你的配置。



## jq

在现代软件开发中，JSON（JavaScript Object Notation）作为一种轻量级的数据交换格式，已经被广泛应用在各种场景中。然而，处理JSON数据并不是件轻松的事情，特别是在命令行环境中。幸运的是，jq这个工具应运而生，它是一个轻量级且功能强大的命令行JSON处理器，专门用于解析、生成和处理JSON数据。

### 什么是jq？

jq是一个命令行工具，用于处理JSON格式的数据。它的出现极大地简化了与JSON数据的交云，并提供了丰富的功能，如数据提取、过滤、排序和转换。jq使用了类似Bash的文本处理理念，但针对JSON对象和数组的数据结构。

### jq的核心特性


* 解析和打印JSON：jq能够将JSON数据格式化为易读的格式，帮助用户更好地理解数据结构。

```shell
    jq . < jsonfile
```

* 过滤和查询：jq支持使用JSON路径表达式（类似XPATH）进行过滤和查询。

```shell
    jq '.users | map(select(.name == "jq-dev"))' < jsonfile
```

* 修改和创建JSON：你可以使用jq来修改现有JSON结构或创建新的JSON对象。

```shell
    jq '.name="John Doe"' < jsonfile > newfile
```

* 颜色输出：jq可以根据JSON数据的层次结构进行智能颜色打印，使结果更加直观。

```shell
    jq --color-input --pretty-print < jsonfile
```

* 强大的表达式：jq支持算术、逻辑、文本处理等多种表达式，还支持递归调用。


### 如何安装jq？

jq几乎可以在所有主流操作系统上安装。在大多数Linux发行版中，你可以使用包管理器进行安装。


对于基于Debian的系统（如Ubuntu）：

```shell
    apt-get install jq
```

对于基于RPM的系统（如Fedora）：

```shell
    dnf install jq
```

对于macOS用户（使用Homebrew）：

```shell
    brew install jq
```


### 使用jq进行JSON处理


获取JSON中的值：

```shell
    jq '.key' < jsonfile
```

这将返回名为key的JSON字段的值。


修改JSON中的值：

```shell
    jq '.key = "newValue"' jsonfile > newfile
```

这将设置名为key的字段值为newValue，并将结果输出到newfile。


从多个JSON文件中提取数据：

```shell
    jq '.key' json1.json json2.json
```

这将从所有指定的JSON文件中提取名为key的字段的值。


排序JSON数组：

```shell
    jq '.sort_by(.value)' < jsonfile
```

这将按数组中的值进行升序排序。


条件过滤JSON数据：

```shell
    jq '.filter_by("disk", "vin")' < jsonfile
```

这将过滤出所有“disk”字段等于“vin”的JSON对象。



### 高级jq技巧


合并多个JSON对象：

```shell
    jq --slurp 'reduce .[] { . * $item }' *.json
```

这将合并当前目录下所有的JSON文件。


从远程JSON服务提取数据：

```shell
    curl -s http://myapi.com/data | jq '.key'
```

这将首先使用curl命令从远程服务获取JSON数据，然后用jq处理它。


创建复杂的新JSON结构：

```shell
    jq -n '{"newkey": [1, 2, 3]}'
```

这将创建一个新的JSON对象，包含一个名为newkey的数组字段。


与Shell脚本结合：

```shell
    users=$(jq '.users[].name' < users.json)
```

这将在Shell脚本中使用，将用户名称提取到Shell变量中。



## nmap

网络管理员和安全专家每天都会面临许多网络管理和安全挑战。为了解决这些问题，他们需要了解自己的网络中的设备和系统，以及这些设备的配置和漏洞。这时，Nmap（网络映射器）就发挥了重要作用。作为一款强大的网络扫描工具，Nmap可以检测网络上的主机、识别运行在这些主机上的服务和版本信息，从而帮助用户了解网络状况、评估系统安全性。这篇文章将详细介绍Nmap的功能、安装和使用方法。

### Nmap的功能


* 主机发现：Nmap能够快速扫描网络，确定哪些主机是活动的，并收集关于它们的信息。
* 端口扫描：Nmap可以检测目标主机上开放的端口以及运行在这些端口上的服务。
* 版本检测：通过识别服务的版本信息，Nmap帮助你了解网络中的潜在漏洞和安全风险。
* 操作系统检测：Nmap可以识别目标系统的操作系统类型和版本，从而为安全审计和维护提供有用的信息。
* 脚本扫描：Nmap支持使用 Lua 脚本进行自定义扫描，这使得用户可以根据自己的需求编写扫描脚本。
* 性能监测：Nmap可以帮助评估网络的性能，如带宽和响应时间。



### Nmap的安装

Nmap可以在多种操作系统上安装。以下是在不同系统上安装Nmap的方法：


Debian/Ubuntu：

```shell
    apt-get update
    apt-get install nmap
```

Red Hat/CentOS：

```shell
    yum install nmap
```

macOS（使用Homebrew）：

```shell
    brew install nmap
```

Windows：

你可以从Nmap官方网站下载适用于Windows的安装包：https://nmap.org/download.html


### Nmap基本使用


扫描单个IP：

```shell
    nmap 192.168.1.1
```

扫描IP范围：

```shell
    nmap 192.168.1.1-254
```

扫描子网：

```shell
    nmap 192.168.1.0/24
```

扫描指定端口：

```shell
    nmap -p 80,443 192.168.1.1
```

扫描所有端口：

```shell
    nmap -p- 192.168.1.1
```

使用SYN扫描：

```shell
    nmap -sS 192.168.1.1
```

操作系统检测：

```shell
    nmap -O 192.168.1.1
```


### Nmap进阶使用


版本检测：

```shell
    nmap -sV 192.168.1.1
```

脚本扫描：

```shell
    nmap --script "banner,ssl-enum-ciphers" -p 80,443 192.168.1.1
```

隐蔽扫描：

```shell
    nmap -sS -T4 192.168.1.1
```

输出结果到文件：
    
```shell
    nmap -oN output.txt 192.168.1.1
```

从文件中读取目标：

```shell
    nmap -iL target_list.txt
```

结合Nping：

Nping 是 Nmap 工具包的一部分，专门用于网络探测和性能测试。

```shell
    nping --tcp -p80 192.168.1.1
```

定制自己的脚本：

Nmap 支持 Lua 脚本，您可以编写自己的扫描脚本来满足特定的需求。



## bat

在Linux系统中，处理文本数据是常见的任务。尽管传统的文本处理工具如sed和awk在很多场景下都非常实用，但有时它们可能过于复杂。为了解决这个问题，我们需要一个既有功能强大又易于使用的文本处理工具。幸运的是，有一种名为bat的命令行工具，它旨在为Linux用户提供简单、快速且高效的文本处理解决方案。

### 什么是bat命令？

bat是一个跨平台的命令行工具，它以cat、sed、awk、grep等传统文本处理工具为基础，进行了优化与改进。它旨在提供更好的用户体验，同时保证高效的性能。bat的目标是成为一个通用的命令行文本处理工具。

### bat的核心特性


* 语法高亮：bat能够自动为不同的编程语言和格式进行语法高亮，让代码更易读。
* 并行处理：bat支持多核心处理，可显著提高文件处理速度。
* 低内存占用：bat在处理大型文件时占用内存较低，比其他文本处理工具更高效。
* 跨平台：bat支持Linux、macOS和Windows等多个操作系统。
* 自动泵：bat无需额外配置即可自动读取和写入压缩文件，如.gz、.bz2等。


### 如何安装bat命令？

在大多数Linux发行版中，你可以使用包管理器轻松安装bat。


对于基于Debian的系统（如Ubuntu）：

```shell
    apt-get update
    apt-get install bat
```

对于基于RPM的系统（如Fedora）：

```shell
    dnf install bat
```

对于Arch Linux用户：

```shell
    pacman -S bat
```

### 使用bat命令进行文本处理


查看文件内容：

```shell
    bat <filename>
```

语法高亮：

```shell
    bat --style=friendly <filename>
```

搜索文件内容：

```shell
    bat --search="searchterm" <filename>
```

并行处理：

```shell
    bat --flowlog=/path/to/combined.log <directory>/*.log
```

处理压缩文件：

```shell
    bat < /path/to/file.gz
```

复制文件到剪贴板：

```shell
    bat --style=numbers <filename> | xclip -selection clipboard
```

分页查看文件：

```shell
    bat --pages=to-cn <filename>
```

在GUI中查看文件：

```shell
    bat -.gui <filename>
```


### bat与git的集成

除了在命令行中使用bat外，它还可以与git进行集成，这样你可以直接在git仓库中查看文件的语法高亮。要实现这一点，请将下面的内容添加到你的~/.gitconfig文件：

```shell
[core]
pager = bat
```

现在，当你运行git diff、git show或者git log时，文件内容将通过bat以语法高亮的方式展示出来。

### 小结

bat是一个非常高效且实用的文本处理工具。通过其简单易用的界面和丰富的特性，bat为用户提供了一种全新的处理和管理文本文件的方法。如果你经常需要处理文本数据，不妨试试bat，它可能会成为你的新宠。

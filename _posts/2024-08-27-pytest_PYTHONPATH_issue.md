---
title: pytest运行用例设置PYTHONPATH问题
date: 2024-08-27
author: Gavin Wang
img: "/img/pytest/pytest-4.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 用pytest执行测试用例时，如果遇到需要设置PYTHONPATH的问题，常见有哪些解决方法？
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

在使用`pytest`做框架设计时，很多包的`import`已经使用相对路径了，如`from .common.util import random_phone_number`，但在执行`pytest`命令时，还是会提示包没有正确导入的错误(`ModuleNotFoundError`)。

这种问题是如何产生的，以及如何规避，是本文接下来所要介绍的。

# 原因

测试用例执行时遇到需要增加 `PYTHONPATH` 的问题，通常是由以下几个原因造成的：

1. **模块路径问题**：`Python` 解释器在导入模块时会按照 `PYTHONPATH` 环境变量指定的路径去搜索模块。如果 `PYTHONPATH` 没有包含你的模块路径，`Python` 就无法找到并导入模块

2. **目录结构**：如果 `common` 模块不在 `Python` 的搜索路径中，可能是因为当前目录结构不符合 `Python` 包的规范，或者模块没有被正确地放置在包结构中

3. **包初始化**：`Python` 包通常需要一个 `__init__.py` 文件来标识它是一个包，这样 `Python` 解释器才能正确地导入包中的模块。如果 `common` 包或其父包缺少 `__init__.py` 文件，可能会导致导入失败

4. **相对导入错误**：如果 `conftest.py` 被放置在一个不是 `Python` 包的目录中，使用相对导入（如 `from .common.http_session import HttpSession`）将不会工作，因为它假定当前目录是一个 `Python` 包

5. **当前工作目录**：如果当前工作目录不在 `Python` 的模块搜索路径中，或者当前目录的上级目录中没有 `__init__.py` 文件，`Python` 解释器就无法识别模块路径

6. **环境问题**：有时候，虚拟环境没有被激活，或者项目依赖没有被正确安装，也会导致模块无法被导入

7. **权限问题**：在某些情况下，如果模块文件没有正确的读取权限，`Python` 解释器可能无法读取它们

8. **pytest 配置问题**：如果 `pytest` 配置不正确，或者使用了错误的配置文件，也可能导致导入错误

等等等等。

上述原因我们可能会碰到，但实际上因环境不同、原因也总是多样，而此次我所碰到的，只是上述众多原因中的某一个。

在我的情况下，使用 `PYTHONPATH=.` 作为命令行参数解决了此次碰到的问题，这表明在当前目录下，需要将当前目录包含在 `PYTHONPATH` 中以便 `Python` 解释器能够找到它。

为了解决这个问题，我需要做如下调整：

- 确保 `PYTHONPATH` 包含在我的模块路径
- 检查项目目录结构，确保它符合 `Python` 包的要求，并且所有包目录中都有 `__init__.py` 文件
- 如果项目是一个 `Python` 包，使用相对导入

上述三条，首条即此次的原因，要如何解决呢？且看下文。

# 解决方案

## 方案1：临时设置 PYTHONPATH 环境变量

```shell
PYTHONPATH=. pytest -s -v
```

这里，. 表示当前目录，确保测试配置文件 `conftest.py` 和 `common` 模块都在当前目录或其子目录中。

## 方案2：永久设置 PYTHONPATH 环境变量

在 `shell` 配置文件中设置 `PYTHONPATH`，例如 `~/.bashrc` 或 `~/.bash_profile` 或 `~/.profile`：

```shell
export PYTHONPATH="$PYTHONPATH:/path/to/your/project"
```

然后，每次打开新的 `shell` 会话时，它将自动包含你的项目路径。

## 方案3：使用conftest.py文件

在 `conftest.py` 中修改 `sys.path`：

```python
import sys
import os

sys.path.append(os.path.abspath('.'))
```

这将在 `pytest` 运行时临时添加项目根目录到 `PYTHONPATH`。

# 结语

当然还有其他的方法，诸如借助`pytest_config hook`实现，这里就不再一一介绍了。

推荐方案3，因为此方案可以通过编写全局入口，如`run.py`执行指定或全部的测试用例，以及生成代码覆盖率、`pylint`报告等资讯。

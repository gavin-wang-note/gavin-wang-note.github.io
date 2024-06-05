---
title: pytest hook系列之pytest_cmdline_main
date: 2024-09-07 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-18.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest hook之pytest_cmdline_main
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# Overview

`pytest_cmdline_main` 是 `pytest` 的一个钩子（hook），用于自定义 `pytest` 的命令行入口。这是高级用法，可用于深度定制 `pytest` 的行为。

# 使用场景

你可以使用 `pytest_cmdline_main` 钩子在 `pytest` 启动时做一些特殊处理，比如修改配置、处理命令行参数，或在测试运行前后执行特定的操作。

# 参数

* `config: Config` 对象，包含了 `pytest` 的所有配置和命令行参数。


# 示例代码

```python
import pytest

# 定义钩子函数
def pytest_cmdline_main(config):
    # 在这里可以访问和修改 config 对象
    print("Running custom pytest_cmdline_main hook...")
    
    # 获取命令行参数
    args = config.invocation_params.args
    print(f"Command line arguments: {args}")

    # 你可以根据你的需求对 args 进行处理
    if '--example' in args:
        print("Custom argument '--example' detected!")

    # 你可以调用其他 Pytest 函数来继续测试运行
    return pytest.main(args)

# 将钩子函数注册到 Pytest
pytest.main = pytest_cmdline_main

# 运行测试
if __name__ == "__main__":
    pytest.main()
```

**说明：**

* 钩子函数pytest_cmdline_main:
  * 该函数会在 `pytest` 运行时被调用。
  * `config` 参数包含了所有配置和命令行参数。
* 打印命令行参数:
  * 使用 `config.invocation_params.args` 获取传入的命令行参数。
* 处理自定义命令行参数:
  * 检查和处理自定义的命令行参数（例如这里的 `--example`）。
* 继续测试运行:
  * 使用 `pytest.main(args)` 函数继续 `pytest` 的正常运行流程（否则测试可能不会运行）。


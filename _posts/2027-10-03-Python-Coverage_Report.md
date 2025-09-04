---
title: 自动化测试代码覆盖率统计与文件屏蔽
date: 2027-10-03 23:00:00
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
summary: 屏蔽某些文件的覆盖率显示为 `0%` 或 `n/a`
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 自动化测试代码覆盖率统计与文件屏蔽

在使用 Jenkins 进行 CI（持续集成）的过程中，自动化测试代码覆盖率的统计（Coverage Report）是一个关键环节。然而，我们有时会发现某些文件的覆盖率显示为 `0%` 或 `n/a`，这些通常是辅助性或初始化文件，不应纳入统计范围。那么该如何屏蔽这些文件呢？

---

## 示例

实际项目中，以下类型的文件通常不应计入代码覆盖率统计：

- `__init__.py`：Python 包的初始化文件  
- `clear_pyc.py`：清理 Python 和 pytest 缓存文件的独立脚本  
- `run_tests.py`：测试执行的总入口脚本  

这些文件通常不涉及核心业务逻辑，其覆盖率数据缺乏实际参考价值。

## 解决方案

为了屏蔽这些非业务文件，可以在项目根目录下创建或修改 `.coveragerc` 配置文件，通过 `omit` 参数指定需忽略的文件或目录。配置示例如下：

```ini
[run]
omit =
    __init__.py             # 初始化文件
    conftest.py             # pytest 配置文件
    config.py               # 配置文件
    run_tests.py            # 测试入口脚本
    clear_pyc.py            # 清理缓存的脚本
    form_module_data.py     # 其他特定用途的脚本
    lock_data.py            # 其他特定用途的脚本
    */utils/*               # 忽略整个 utils 目录
    */api/*                 # 忽略 api 目录
```

配置后，代码覆盖率工具将自动跳过这些文件，使统计结果更准确地反映业务代码的测试覆盖情况。

## 说明

- `.coveragerc` 是 coverage.py 工具的配置文件，用于定制其行为。
- `omit` 参数支持使用通配符（如 `*`）匹配多个文件或目录。
- 如需更精细的控制，可进一步研究 `.coveragerc` 的其他配置选项。

通过上述方法，可有效排除无统计意义的文件，提升覆盖率报告的可参考性。

---

# .coveragerc 中 omit 的屏蔽规则详解

以下系统梳理 `.coveragerc` 中 `omit` 的屏蔽规则，结合官方文档与社区实践，帮助理解常见配置误区（如“为何 `api/*` 未生效”）及正确写法。

---

###  1. omit 的本质：路径模式匹配列表

在 `[run]` 段落中，`omit` 是一个多行字符串列表，每行代表一个路径模式（pattern）。Coverage.py 在运行时会逐一匹配被测文件路径，若命中则将其排除。

---

###  2. 路径模式的语法细节

| 写法           | 匹配范围                     | 示例                          | 说明                     |
|----------------|------------------------------|-------------------------------|--------------------------|
| `api/*`        | 仅 api 目录下的直接子文件      | `api/a.py` <br>`api/sub/b.py`  | 类似 glob，不递归        |
| `api/**`       | api 目录及其所有子孙目录        | `api/a.py` <br>`api/sub/b.py`  | Coverage ≥ 5.0 生效      |
| `*/api/*`      | 任意父目录下的一级 api 目录     | `proj/api/a.py`              | 通配符可跨层级           |
| `**/api/**`    | 任意位置的 api 目录            | `src/api/…` <br>`vendor/api/…`  | 最保险的递归写法         |
| 绝对/相对路径   | 按字面量匹配                  | `/tmp/proj/api/a.py`           | 不建议，CI 中路径易变    |

>  结论：若需忽略整个 api 目录，应使用 `api/**` 或 `**/api/**`

---

###  3. 路径基准：以 source 或运行目录为根

- 若在 `[run]` 中设置 `source = src`，则模式匹配基于 `src/` 目录。
- 若未设置 `source`，则以 coverage 启动时的工作目录（通常为项目根目录）为基准。
-  常见问题：在 Jenkins/GitHub Actions 中，工作目录可能非项目根目录，导致 `api/**` 未生效。解决方案：显式设置 `source = .` 或在命令行中添加 `--cov=.`。

---

###  4. 其他常见误区

| 场景                        | 原因与解决方案                                                                 |
|-----------------------------|------------------------------------------------------------------------------|
| 将 omit 写在 `[report]` 中   | `omit` 仅在 `[run]` 阶段生效；写在 `[report]` 中无效                         |
| 使用 pytest-cov 未指定配置   | 可能加载了其他配置文件（如 `tox.ini`），需添加 `--cov-config=.coveragerc`     |
| Windows 路径分隔符          | 统一使用 `/`，Coverage 会自动适配                                            |
| 子进程/多进程环境            | 使用环境变量 `COVERAGE_PROCESS_START=.coveragerc` 确保子进程继承同一配置      |

---

###  5. 推荐配置模板

```ini
# .coveragerc
[run]
source = .
omit =
    */tests/*
    */test_*.py
    */*_test.py
    **/migrations/**
    **/api/**
    manage.py
    fabfile.py
branch = True
parallel = True

[report]
skip_covered = True
show_missing = True
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
```

---

###  6. 总结

>  使用 `omit` 彻底忽略目录时，务必使用 `**` 递归通配符，并确认路径基准与配置文件被正确加载。

---

如需调试，可临时添加 `--cov-report=term-missing -v` 参数，观察实际匹配的文件列表，验证排除效果。

---



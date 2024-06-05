---
title: pytest hook系列之pytest_configure
date: 2024-09-04 23:00:00
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
summary: pytest hook之pytest_configure
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation

---

# Overview

`pytest_configure`是一个钩子函数，用于在`pytest`配置和插件初始化完成后立即调用。这个钩子函数通常用于执行全局初始化操作，如设置插件的全局配置、初始化日志记录、设置环境变量等。它允许你在测试运行开始之前执行必要的配置和准备工作。

# 使用场景

* 插件初始化：配置和初始化插件的全局状态和资源
* 全局配置：设置全局变量、环境变量或其他需要在测试开始前设置的信息
* 日志记录：初始化全局的日志记录配置
* 动态配置：根据命令行参数或配置文件动态调整 `pytest` 的行为
* 注入默认 fixture：配置全局的 `fixture` 和测试前初始化工作

# 参数

* config：这是一个 `pytest.Config` 对象，代表了 `pytest` 的配置信息，包含了命令行参数、`ini` 文件配置等所有 `pytest` 配置信息。

# 示例代码

以下是一个使用`pytest_configure`的示例代码，展示如何在测试开始之前进行全局配置和初始化：

## 初始化日志记录和设置全局变量

```python
# conftest.py
import pytest
import logging

def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="dev",
        help="Environment to run tests against: dev/staging/prod"
    )

def pytest_configure(config):
    # 初始化日志记录
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting tests with pytest")
    
    # 设置全局变量
    config.env = config.getoption("--env")
    logging.info(f"Running tests in environment: {config.env}")
```

## 在测试中访问这些配置

```python
# test_example.py
import pytest
import logging

def test_environment(pytestconfig):
    env = pytestconfig.env
    logging.info(f"Test running in environment: {env}")
    assert env in ["dev", "staging", "prod"]
```

**说明:**

* `conftest.py`：在 `conftest.py` 文件中，首先使用 `pytest_addoption` 钩子添加一个命令行选项 `--env`，用于指定测试运行的环境。然后在 `pytest_configure` 中初始化日志记录，并设置一个全局变量 `env`。

* `test_example.py`：在测试用例文件 `test_example.py` 中，使用 `pytestconfig` 对象来访问在 `pytest_configure` 中设置的全局变量 `env`。


# 运行示例

为了测试不同环境，可以在运行 `pytest` 时传递 `--env` 参数：

```shell
pytest --env="staging"
```

你应该会在控制台中看到类似以下的日志输出：

```plaintext
root@Gavin:~/test/hook# pytest --env="staging"
INFO:root:Starting tests with pytest
INFO:root:Running tests in environment: staging
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test/hook
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, dotenv-0.5.2, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                         

test_example.py .                                                                                                                                                                                                                                  [100%]

=================================================================================================================== 1 passed in 0.03s ====================================================================================================================
root@Gavin:~/test/hook#
```

总结

通过`pytest_configure`钩子，你可以在`pytest`初始化完配置和插件后，开始测试运行之前进行任何必要的配置和初始化工作。这个钩子函数非常适合用于插件初始化、全局变量设置、日志记录配置以及根据命令行参数动态调整测试行为等场景。利用这个钩子，可以让你的测试框架更加灵活和强大，适应各种不同的测试需求。

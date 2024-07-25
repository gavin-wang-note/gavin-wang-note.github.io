---
title: 测试用例执行环境切换之pytest-base-url源码解读 
date: 2025-09-14 22:00:00
author: Gavin Wang
img: "/img/pytest/pytest-26.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 测试用例执行环境切换之pytest-base-url源码解读
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述



# 源码解读

## 源码目录结构

从[官网](https://pypi.org/project/pytest-base-url)下载解压到本地：

```shell
root@Gavin:~/pytest_plugin/pytest_base_url-2.1.0# ll
total 60
drwxr-xr-x  4 root root 4096 Jul 25 14:57 ./
drwxr-xr-x 25 root root 4096 Jul 25 14:57 ../
-rw-r--r--  1 root root 1158 Feb  1 06:40 CHANGES.rst
-rw-r--r--  1 root root 1757 Feb  1 06:40 development.rst
-rw-r--r--  1 root root   72 Feb  1 06:40 .gitignore
-rw-r--r--  1 root root  193 Feb  1 06:40 LICENSE
-rw-r--r--  1 root root 6634 Feb  1 06:40 PKG-INFO
-rw-r--r--  1 root root  448 Feb  1 06:40 .pre-commit-config.yaml
-rw-r--r--  1 root root 2035 Feb  1 06:40 pyproject.toml
-rw-r--r--  1 root root 4823 Feb  1 06:40 README.rst
drwxr-xr-x  3 root root 4096 Jul 25 14:57 src/
drwxr-xr-x  2 root root 4096 Jul 25 14:57 tests/
-rw-r--r--  1 root root  744 Feb  1 06:40 tox.ini
root@Gavin:~/pytest_plugin/pytest_base_url-2.1.0# cd src
root@Gavin:~/pytest_plugin/pytest_base_url-2.1.0/src# ll
total 12
drwxr-xr-x 3 root root 4096 Jul 25 14:57 ./
drwxr-xr-x 4 root root 4096 Jul 25 14:57 ../
drwxr-xr-x 2 root root 4096 Jul 25 14:57 pytest_base_url/
root@Gavin:~/pytest_plugin/pytest_base_url-2.1.0/src# cd pytest_base_url/
root@Gavin:~/pytest_plugin/pytest_base_url-2.1.0/src/pytest_base_url# ll
total 16
drwxr-xr-x 2 root root 4096 Jul 25 14:57 ./
drwxr-xr-x 3 root root 4096 Jul 25 14:57 ../
-rw-r--r-- 1 root root    0 Feb  1 06:40 __init__.py
-rw-r--r-- 1 root root 2335 Feb  1 06:40 plugin.py
-rw-r--r-- 1 root root  411 Feb  1 06:40 __version.py
root@Gavin:~/pytest_plugin/pytest_base_url-2.1.0/src/pytest_base_url# 
```


## 源码解读

核心文件是`plugin.py`。


```python
root@Gavin:~/pytest_plugin/pytest_base_url-2.1.0/src/pytest_base_url# cat plugin.py 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import pytest


@pytest.fixture(scope="session")
def base_url(request):
    """Return a base URL"""
    config = request.config
    base_url = config.getoption("base_url")
    if base_url is not None:
        return base_url


@pytest.fixture(scope="session", autouse=True)
def _verify_url(request, base_url):
    """Verifies the base URL"""

    verify = request.config.option.verify_base_url
    if base_url and verify:
        # Lazy load requests to reduce cost for tests that don't use the plugin
        import requests
        from requests.packages.urllib3.util.retry import Retry
        from requests.adapters import HTTPAdapter

        session = requests.Session()
        retries = Retry(backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount(base_url, HTTPAdapter(max_retries=retries))
        session.get(base_url)


def pytest_configure(config):
    if hasattr(config, "workerinput"):
        return  # don't run configure on xdist worker nodes
    base_url = config.getoption("base_url") or config.getini("base_url")
    if base_url is not None:
        config.option.base_url = base_url
        metadata = config.pluginmanager.getplugin("metadata")
        if metadata:
            try:
                from pytest_metadata.plugin import metadata_key

                config.stash[metadata_key]["Base URL"] = base_url
            except ImportError:  # pytest-metadata < 3.x
                config._metadata["Base URL"] = base_url


def pytest_report_header(config, start_path):
    base_url = config.getoption("base_url")
    if base_url:
        return "baseurl: {0}".format(base_url)


def pytest_addoption(parser):
    parser.addini("base_url", help="base url for the application under test.")
    parser.addoption(
        "--base-url",
        metavar="url",
        default=os.getenv("PYTEST_BASE_URL", None),
        help="base url for the application under test.",
    )
    parser.addoption(
        "--verify-base-url",
        action="store_true",
        default=not os.getenv("VERIFY_BASE_URL", "false").lower() == "false",
        help="verify the base url.",
    )
```

1. **导入依赖**:
```python
import os
import pytest
```

导入了 `os` 模块用于环境变量操作，导入 `pytest` 模块用于使用 `pytest` 的钩子和 fixture。

2. **base_url fixture**:
```python
@pytest.fixture(scope="session")
def base_url(request):
    """Return a base URL"""
    config = request.config
    base_url = config.getoption("base_url")
    if base_url is not None:
        return base_url
```

定义了一个 `base_url fixture`，它从 `pytest` 配置中获取 `base_url` 选项，并将其返回。这个 `fixture` 的作用域是会话级别（`session scope`）。

3. **_verify_url fixture**:
```python
@pytest.fixture(scope="session", autouse=True)
def _verify_url(request, base_url):
    """Verifies the base URL"""
    verify = request.config.option.verify_base_url
    if base_url and verify:
        # Lazy load requests to reduce cost for tests that don't use the plugin
        import requests
        from requests.packages.urllib3.util.retry import Retry
        from requests.adapters import HTTPAdapter

        session = requests.Session()
        retries = Retry(backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount(base_url, HTTPAdapter(max_retries=retries))
        session.get(base_url)
```

定义了一个 `_verify_url` fixture，它自动使用（`autouse=True`），并验证 `base_url` 是否有效。如果 `base_url` 存在并且 `verify_base_url` 选项为真，则使用 `requests` 库发送一个 GET 请求到 `base_url`。

4. **pytest_configure 钩子**:
```python
def pytest_configure(config):
    if hasattr(config, "workerinput"):
        return  # don't run configure on xdist worker nodes
    base_url = config.getoption("base_url") or config.getini("base_url")
    if base_url is not None:
        config.option.base_url = base_url
        metadata = config.pluginmanager.getplugin("metadata")
        if metadata:
            try:
                from pytest_metadata.plugin import metadata_key

                config.stash[metadata_key]["Base URL"] = base_url
            except ImportError:  # pytest-metadata < 3.x
                config._metadata["Base URL"] = base_url
   ```

在 `pytest` 配置阶段，如果设置了 `base_url`，则将其存储在配置选项中，并尝试将其添加到 `pytest` 元数据中。

5. **pytest_report_header 钩子**:
```python
def pytest_report_header(config, start_path):
    base_url = config.getoption("base_url")
    if base_url:
        return "baseurl: {0}".format(base_url)
   ```

在 `pytest` 报告的头部添加基础 URL，如果设置了 `base_url`。

6. **pytest_addoption 钩子**:
```python
def pytest_addoption(parser):
    parser.addini("base_url", help="base url for the application under test.")
    parser.addoption(
        "--base-url",
        metavar="url",
        default=os.getenv("PYTEST_BASE_URL", None),
        help="base url for the application under test.",
    )
    parser.addoption(
        "--verify-base-url",
        action="store_true",
        default=not os.getenv("VERIFY_BASE_URL", "false").lower() == "false",
        help="verify the base url.",
    )
```

添加命令行选项和配置文件选项，允许用户设置 `base_url` 和 `verify_base_url`。`--base-url` 选项的默认值可以从环境变量 `PYTEST_BASE_URL` 中获取。

# 结语

插件功能总结：

- 允许用户通过命令行或配置文件设置基础 `URL`。
- 提供了一个 `fixture` 来获取和验证基础 `URL`。
- 在测试报告的头部显示基础 `URL`。
- 通过 `pytest` 钩子和 `fixture` 实现了插件的逻辑。

这个插件非常适合需要对不同环境进行测试的情况，允许用户动态地设置和验证测试目标的基础 `URL`。

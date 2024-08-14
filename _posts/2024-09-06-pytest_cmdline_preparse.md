---
title: pytest hook系列之pytest_cmdline_preparse
date: 2024-09-06 23:00:00
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
summary: pytest hook之pytest_cmdline_preparse
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation

---

# Overview

官网代码如下：

```python
@hookspec(warn_on_impl=WARNING_CMDLINE_PREPARSE_HOOK)
def pytest_cmdline_preparse(config: "Config", args: List[str]) -> None:
    """(**Deprecated**) modify command line arguments before option parsing.

    This hook is considered deprecated and will be removed in a future pytest version. Consider
    using :hook:`pytest_load_initial_conftests` instead.

    .. note::
        This hook will not be called for ``conftest.py`` files, only for setuptools plugins.

    :param config: The pytest config object.
    :param args: Arguments passed on the command line.
    """
```


此`hook`已经被其他`hook pytest_load_initial_conftests`所代替，这里就不介绍它了，后面将有文章专门介绍`pytest_load_initial_conftests`。

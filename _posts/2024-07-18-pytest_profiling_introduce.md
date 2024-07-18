---
title: pytest-profiling插件介绍
date: 2024-07-18 22:00:00
author: Gavin Wang
img: "/img/pytest/pytest-22.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: pytest-profiling插件介绍，协助开发者识别Python代码中的性能瓶颈和优化机会
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

`pytest-profiling` 是一个用于基于 `pytest` 的性能分析插件，它能帮助开发者识别`Python`代码中的性能瓶颈和优化机会。

本文将介绍如何安装、配置和使用该插件，并展示一些常见的应用场景和代码示例。


# 应用场景

- 识别性能瓶颈

使用 `pytest-profiling` 可以帮助识别代码中的性能瓶颈，找出哪些函数或代码段消耗了大量的`CPU`时间或内存资源。

- 优化代码

通过分析性能报告，你可以有针对性地优化代码，例如减少不必要的循环、优化算法复杂度或改进内存管理。


# 安装

首先，确保你已经安装了 `pytest` 和 `pytest-profiling` 插件。可以通过以下命令进行安装：

```shell
pip install pytest pytest-profiling
```

# 测试示例

```python
# Content of test_example.py
root@Gavin:~/pytest_plugin/test# cat test_example.py 
import time

def test_long_time():
    time.sleep(10)
    assert 1 == 1, "[ERROR]  Assert failed."
```

故意等了10秒，看下运行效果：

```shell
root@Gavin:~/pytest_plugin/test# pytest --profile --profile-svg  test_example.py 
Test session starts (platform: linux, Python 3.11.6, pytest 8.2.2, pytest-sugar 1.0.0)
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/pytest_plugin/test
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, profiling-1.7.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, order-1.2.1, progress-1.3.0, twisted-1.14.1, picked-0.5.0, assume-2.4.3, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, sugar-1.0.0, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2, extra-durations-0.1.3, line-profiler-0.2.1
asyncio: mode=Mode.STRICT
collected 1 item                                                                                                                                                                                                                                         

 test_example.py ?                                                                                                                                                                                                                         100% ██████████
Profiling (from /root/pytest_plugin/test/prof/combined.prof):
Wed Jul 17 22:22:21 2024    /root/pytest_plugin/test/prof/combined.prof

         56965 function calls (56696 primitive calls) in 10.041 seconds

   Ordered by: cumulative time
   List reduced from 581 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   10.041   10.041 runner.py:113(pytest_runtest_protocol)
        1    0.000    0.000   10.041   10.041 runner.py:121(runtestprotocol)
        3    0.000    0.000   10.041    3.347 runner.py:225(call_and_report)
    29/11    0.000    0.000   10.041    0.913 _hooks.py:498(__call__)
    29/11    0.000    0.000   10.041    0.913 _manager.py:111(_hookexec)
    29/11    0.001    0.000   10.041    0.913 _callers.py:53(_multicall)
        3    0.000    0.000   10.039    3.346 runner.py:318(from_call)
        3    0.000    0.000   10.039    3.346 runner.py:241(<lambda>)
        1    0.000    0.000   10.002   10.002 runner.py:162(pytest_runtest_call)
        1    0.000    0.000   10.002   10.002 python.py:1630(runtest)
        1    0.000    0.000   10.002   10.002 plugin.py:39(pytest_pyfunc_call)
        1    0.000    0.000   10.002   10.002 test_example.py:3(test_long_time)
        1   10.002   10.002   10.002   10.002 {built-in method time.sleep}
        1    0.000    0.000    0.035    0.035 runner.py:157(pytest_runtest_setup)
        1    0.000    0.000    0.035    0.035 runner.py:498(setup)
        1    0.000    0.000    0.035    0.035 python.py:1634(setup)
        1    0.000    0.000    0.035    0.035 fixtures.py:682(_fillfixtures)
     24/8    0.000    0.000    0.034    0.004 fixtures.py:499(getfixturevalue)
     32/8    0.000    0.000    0.034    0.004 fixtures.py:538(_get_active_fixturedef)
      7/6    0.000    0.000    0.034    0.006 fixtures.py:1028(execute)


SVG profile in /root/pytest_plugin/test/prof/combined.svg.
=============================================================================================================== sum of all tests durations ===============================================================================================================
10.04s

Results (10.16s):
       1 passed
root@Gavin:~/pytest_plugin/test#
```

生成的`svg`图，还是非常赞的，FYI：

<img class="shadow" src="/img/in-post/less_combined.svg" width="800">

<img class="shadow" src="/img/in-post/more_combined.svg" width="1200">

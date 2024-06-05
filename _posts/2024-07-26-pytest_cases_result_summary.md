---
title: 借助pytest hook获取用例执行结果信息汇总
date: 2024-07-26 16:59:18
author: Gavin Wang
img: "/img/pytest/pytest-10.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: hook获取用例执行状态和概要信息
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

# 概述

pytest hook功能很强大，本文简要概述如何借助pytest的`pytest_runtest_makereport`&`pytest_sessionstart`这两个hook，实现用例执行结果的汇总。

至于pytest hook知识点，非本文介绍内容，请读者另行查阅资料。

# 预期效果

预期达到的效果如下：

* 1.结果写入文件
* 2.预期内容参考如下：

```shell
---------summary----------
passed: 1
failed: 2
skipped: 1
error: 1
xfailed: 0
xpassed: 1
---------details----------
[failed]
dir1/test_case_name01
dir1/test_case_name02
dir1/test_case_name03
dir2/test_case_name01

[skipped]
test_case_name

[error]
test_case_name

[xfailed]
test_case_name
# 如果没有，则显示为  --

[xpassed]
  --
```


# Code

## `conftest.py`

```python
import pytest
from collections import defaultdict

# 初始化一个字典，用于保存各种测试状态的数量和测试名称列表
test_results_summary = defaultdict(lambda: {"count": 0, "cases": []})

def pytest_sessionstart(session):
    session.results_summary = test_results_summary

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    global test_results_summary
    
    # 处理测试过程中的结果
    if report.when == 'call':
        if report.failed:
            if "xfail" in item.keywords:
                test_results_summary["xfailed"]["count"] += 1
                test_results_summary["xfailed"]["cases"].append(item.nodeid)
            else:
                test_results_summary["failed"]["count"] += 1
                test_results_summary["failed"]["cases"].append(item.nodeid)
        elif report.skipped:
            test_results_summary["skipped"]["count"] += 1
            test_results_summary["skipped"]["cases"].append(item.nodeid)
        elif "xfail" in item.keywords:
            test_results_summary["xpassed"]["count"] += 1
            test_results_summary["xpassed"]["cases"].append(item.nodeid)
        else:
            test_results_summary["passed"]["count"] += 1
    elif report.failed:
        test_results_summary["error"]["count"] += 1
        test_results_summary["error"]["cases"].append(item.nodeid)

def pytest_sessionfinish(session, exitstatus):
    with open('test_results_summary.txt', 'w') as f:
        f.write("---------summary----------\n")
        for key, value in session.results_summary.items():
            f.write(f"{key}: {value['count']}\n")
        
        f.write("---------details----------\n")
        for key, value in session.results_summary.items():
            if value["cases"]:
                f.write(f"[{key}]\n" + "\n".join(value["cases"]) + "\n")
            else:
                f.write(f"[{key}]\n  --\n")
```

# 效果检验

先写一段测试代码`test_various_statuses.py`，涵盖各种用例执行状态：

```python
# content of test_various_statuses.py
# -*- coding:UTF-8 -*-


import pytest


# 这个测试会通过
def test_passed():
    assert True


# 这个测试会失败
def test_failed():
     assert False


# 这个测试主动抛异常会失败
def test_failed_raise():
    raise Exception("An unexpected error occurred")


# 这个测试会被标记为预期失败，但如果通过了，它将被标记为XPASS
@pytest.mark.xfail
def test_xpass():
   assert True


# 这个测试被标记为预期失败，并且它确实失败了，因此它将被标记为XFAIL
@pytest.mark.xfail
def test_xfailed():
    assert False


# 这个测试会被跳过
@pytest.mark.skip(reason="This test is skipped for demonstration purposes")
def test_skipped():
    assert True


# 使用一个会发生错误的fixture
@pytest.fixture
def error_fixture():
    raise Exception("Error in fixture")


# 这个测试使用了一个错误的fixture，即使测试代码本身是正常的
def test_with_error_fixture(error_fixture):
    assert True
```

执行测试用例：

```shell
root@Gavin:~/test_result_summary# ll
total 16
drwxr-xr-x  2 root root 4096 July 24 11:50 ./
drwx------ 43 root root 4096 July 24 11:48 ../
-rw-r--r--  1 root root 1977 July 24 11:41 conftest.py
-rw-r--r--  1 root root 1009 July 24 11:32 test_various_statuses.py
root@Gavin:~/test_result_summary# pytest -s test_various_statuses.py 
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.4.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/test_result_summary
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, timeout-2.2.0
asyncio: mode=Mode.STRICT
collected 7 items                                                                                                                                                                                                                                        

test_various_statuses.py .FFXxsE

========================================================================================================================= ERRORS =========================================================================================================================
_______________________________________________________________________________________________________ ERROR at setup of test_with_error_fixture ________________________________________________________________________________________________________

    @pytest.fixture
    def error_fixture():
>       raise Exception("Error in fixture")
E       Exception: Error in fixture

test_various_statuses.py:44: Exception
======================================================================================================================== FAILURES ========================================================================================================================
______________________________________________________________________________________________________________________ test_failed _______________________________________________________________________________________________________________________

    def test_failed():
>        assert False
E        assert False

test_various_statuses.py:15: AssertionError
___________________________________________________________________________________________________________________ test_failed_raise ____________________________________________________________________________________________________________________

    def test_failed_raise():
>       raise Exception("An unexpected error occurred")
E       Exception: An unexpected error occurred

test_various_statuses.py:20: Exception
================================================================================================================ short test summary info =================================================================================================================
FAILED test_various_statuses.py::test_failed - assert False
FAILED test_various_statuses.py::test_failed_raise - Exception: An unexpected error occurred
ERROR test_various_statuses.py::test_with_error_fixture - Exception: Error in fixture
========================================================================================= 2 failed, 1 passed, 1 skipped, 1 xfailed, 1 xpassed, 1 error in 0.11s ==========================================================================================
root@Gavin:~/test_result_summary#
```

用例执行结束后，会产生文件`test_results_summary.txt`:

```shell
root@Gavin:~/test_result_summary# ll
total 28
drwxr-xr-x  4 root root 4096 July 24 11:50 ./
drwx------ 43 root root 4096 July 24 11:48 ../
-rw-r--r--  1 root root 1977 July 24 11:41 conftest.py
drwxr-xr-x  2 root root 4096 July 24 11:50 __pycache__/
drwxr-xr-x  3 root root 4096 July 24 11:50 .pytest_cache/
-rw-r--r--  1 root root  364 July 24 11:50 test_results_summary.txt
-rw-r--r--  1 root root 1009 July 24 11:32 test_various_statuses.py
root@Gavin:~/test_result_summary#
```
其内容参考如下：

```shell
root@Gavin:~/test_result_summary# cat test_results_summary.txt 
---------summary----------
passed: 1
failed: 2
xpassed: 1
skipped: 1
error: 1
---------details----------
[passed]
  --
[failed]
test_various_statuses.py::test_failed
test_various_statuses.py::test_failed_raise
[xpassed]
test_various_statuses.py::test_xpass
[skipped]
test_various_statuses.py::test_xfailed
[error]
test_various_statuses.py::test_with_error_fixture
root@Gavin:~/test_result_summary#
```

符合预期要求。


# 结语

上述代码仅是个示例，抛砖引玉，在具体自动化Project中，可按自己的需求调整此文件位置、名称、内容展示等信息。

也可以将此文件的部分内容（如担心非passed状态用例数太多，引发文档内容过多）作为邮箱附件发送CI/CD构建通知。

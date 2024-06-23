---
title: 继续执行中断后的测试用例
date: 2024-06-23
author: Gavin Wang
img: "/img/pytest/pytest-6.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 本文介绍了测试用例在执行过程中被中断，如何续接之前的用例继续执行余下的测试用例，给出了几种实践方案供读者参考
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 概述

碰到这样一种情况：

比如有100个测试用例，第一次执行了20个，但是在执行过程中被中断了，如何在下一次执行余下的80个测试用例？

对于这个问题的解决，想到了插件`pytest-rerunfailures`和`pytest cache`机制，但`pytest-rerunfailures`插件用于执行那些被标记为失败状态的测试用例，而非余下未被执行的测试用例；`cache`机制记录曾经执行失败的测试用例信息，而插件`pytest-rerunfailures`也是借鉴了`pytest cache`中的`lastfailed`内容实现失败用例的重新执行。

分析到这里，发现`pytest`中并没有现成的参数或者插件来实现我们的预期目标，只能另寻他法了。


# 题外篇之pytest cache

先花一些篇幅简单介绍一下`pytest cache`。

`.pytest_cache` 是 `pytest` 自动创建的目录，用于存储缓存数据，帮助提高测试执行效率和管理测试状态。里面包含多个文件和目录，常见内容包括：

* **CACHEDIR.TAG**：标记这个目录是一个缓存目录。
* **README.md**：说明缓存目录的用途。
* **v/cache/**：具体的缓存数据文件存放在这个目录下。

`.pytest_cache/v/cache` 目录

* `v/cache` 目录下存放了各种缓存数据文件，包括 `lastfailed、nodeids` 和 `stepwise` 文件。

`stepwise` 文件

`stepwise` 文件专用于记录上一次运行中失败的测试项目。当启用 `--stepwise` 模式时，`pytest` 会根据这个文件记录的位置，从上次失败的地方继续执行测试。但这也意味着使用此模式后，一旦碰到失败的测试用例，`pytest`就会退出不再执行后续的测试用例了。


我们来看一个本地生成的`.pytest_cache`目录：

```shell
root@Gavin:~/run_left# tree .pytest_cache/
.pytest_cache/
├── CACHEDIR.TAG
├── README.md
└── v
    └── cache
        ├── lastfailed
        ├── nodeids
        └── stepwise

3 directories, 5 files
root@Gavin:~/run_left# 
```

其中`cache`目录下文件内容参考如下：

```shell
root@Gavin:~/run_left/.pytest_cache/v/cache# cat lastfailed 
{
  "test_example.py::test_example_2": true
}root@Gavin:~/run_left/.pytest_cache/v/cache# cat nodeids 
[
  "test_example.py::test_example_1",
  "test_example.py::test_example_2",
  "test_example.py::test_example_3",
  "test_example.py::test_example_4",
  "test_example_boolean.py::test_and_operation",
  "test_example_boolean.py::test_bool_false",
  "test_example_boolean.py::test_bool_true",
  "test_example_boolean.py::test_not_operation",
  "test_example_boolean.py::test_or_operation",
  "test_example_dict.py::test_get_item",
  "test_example_dict.py::test_keys",
  "test_example_dict.py::test_remove_item",
  "test_example_dict.py::test_set_item",
  "test_example_dict.py::test_values",
  "test_example_list.py::test_append",
  "test_example_list.py::test_index",
  "test_example_list.py::test_remove",
  "test_example_list.py::test_reverse",
  "test_example_list.py::test_sort",
  "test_example_math.py::test_addition",
  "test_example_math.py::test_division",
  "test_example_math.py::test_multiplication",
  "test_example_math.py::test_subtraction",
  "test_example_string.py::test_concatenation",
  "test_example_string.py::test_find_substring",
  "test_example_string.py::test_lowercase",
  "test_example_string.py::test_replace",
  "test_example_string.py::test_uppercase"
]root@Gavin:~/run_left/.pytest_cache/v/cache# cat stepwise 
[]root@Gavin:~/run_left/.pytest_cache/v/cache#
```

虽然有失败的测试用例，但上面的`stepwise`文件内容却为空，这是因为用例执行的时候没有携带上参数`--stepwise`；如果携带了，`stepwise`文件内容参考如下：

```shell
root@Gavin:~/run_left/.pytest_cache/v/cache# cat stepwise 
"test_example.py::test_example_2"root@Gavin:~/run_left/.pytest_cache/v/cache# 
root@Gavin:~/run_left/.pytest_cache/v/cache# 
```

注意这里的`nodeids`文件，它记录所有测试用例的标识符，并不是已经执行过了的测试用例，言外之意是记录所有被`pytest`搜集到的测试用例的`ids`信息。


# 解决过程

## 准备工作

准备一些测试用例，内容随便写，有执行成功，也有执行失败的，参考如下：

```shell
root@Gavin:~/run_left# ll
total 32
drwxr-xr-x  2 root root 4096 Jun 21 15:21 ./
drwx------ 43 root root 4096 Jun 21 15:07 ../
-rw-r--r--  1 root root  308 Jun 21 14:54 test_example_boolean.py
-rw-r--r--  1 root root  636 Jun 21 14:34 test_example_dict.py
-rw-r--r--  1 root root  429 Jun 21 14:33 test_example_list.py
-rw-r--r--  1 root root  185 Jun 21 14:33 test_example_math.py
-rw-r--r--  1 root root  210 Jun 21 14:32 test_example.py
-rw-r--r--  1 root root  364 Jun 21 14:33 test_example_string.py
root@Gavin:~/run_left# cat test_example_string.py 
def test_concatenation():
    assert "Hello, " + "World!" == "Hello, World!"

def test_uppercase():
    assert "hello".upper() == "HELLO"

def test_lowercase():
    assert "WORLD".lower() == "world"

def test_find_substring():
    assert "hello world".find("world") != -1

def test_replace():
    assert "hello world".replace("world", "pytest") == "hello pytest"

root@Gavin:~/run_left#
```

## 方案一：文件记录用例执行状态，pytest hook跳过已记录用例

可以使用一个简单的文本文件或`JSON`文件来记录哪些测试已被执行，当然，如果测试用例通过，其标识符也可被记录在文件中；然后编写插件来记录和跳过测试用例（即在`conftest.py`文件中，使用`pytest hooks`来实现这一功能）。

文件`contest.py`内容参考如下：

```python
import pytest
import json
import os

# 定义保存状态的文件
STATUS_FILE = "test_status.json"

# 读取状态文件
def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 写入状态文件
def save_status(status):
    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f)

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    status = load_status()
    nodeid = item.nodeid

    # 如果测试用例已经成功执行过，则跳过
    # 如果想跳过其他状态的测试用例，继续增加状态判断即可
    # if nodeid in status and status[nodeid] == "passed":
    #     pytest.skip(f"Skipping {nodeid}, already passed.")
    if nodeid in status:
        item.add_marker(pytest.mark.skip(reason=f"Skipping {nodeid}, already passed."))

def pytest_runtest_logreport(report):
    if report.when == 'call':
        status = load_status()
        nodeid = report.nodeid

        if report.outcome == "passed":
            status[nodeid] = "passed"
        elif report.outcome == "failed":
            status[nodeid] = "failed"
        elif report.outcome == "skipped":
            status[nodeid] = "skipped"
        
        save_status(status)

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    print(f"Results saved in {STATUS_FILE}")
```

接下来验证一下效果：


```shell
root@Gavin:~/run_left# ll
total 36
drwxr-xr-x  2 root root 4096 Jun 21 14:54 ./
drwx------ 43 root root 4096 Jun 21 14:54 ../
-rw-r--r--  1 root root 1249 Jun 21 14:54 conftest.py
-rw-r--r--  1 root root  308 Jun 21 14:54 test_example_boolean.py
-rw-r--r--  1 root root  636 Jun 21 14:34 test_example_dict.py
-rw-r--r--  1 root root  429 Jun 21 14:33 test_example_list.py
-rw-r--r--  1 root root  185 Jun 21 14:33 test_example_math.py
-rw-r--r--  1 root root  210 Jun 21 14:32 test_example.py
-rw-r--r--  1 root root  364 Jun 21 14:33 test_example_string.py
root@Gavin:~/run_left# pytest -s -v
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-41-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'progress': '1.2.5', 'order': '1.2.1', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/run_left
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, progress-1.2.5, order-1.2.1, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 28 items                                                                                                                                                                                                                                       

test_example.py::test_example_1 PASSED
test_example.py::test_example_2 FAILED
test_example.py::test_example_3 PASSED
test_example.py::test_example_4 PASSED
test_example_boolean.py::test_bool_true PASSED
test_example_boolean.py::test_bool_false PASSED
test_example_boolean.py::test_and_operation PASSED
test_example_boolean.py::test_or_operation PASSED
test_example_boolean.py::test_not_operation ^CResults saved in test_status.json


======================================================================================================================== FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example_2 _____________________________________________________________________________________________________________________

    def test_example_2():
>       assert 1 == 2  # 这个测试用例会失败
E       assert 1 == 2

test_example.py:7: AssertionError
================================================================================================================ short test summary info =================================================================================================================
FAILED test_example.py::test_example_2 - assert 1 == 2
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! KeyboardInterrupt !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
/root/run_left/test_example_boolean.py:17: KeyboardInterrupt
(to show a full traceback on KeyboardInterrupt use --full-trace)
============================================================================================================== 1 failed, 7 passed in 1.42s ===============================================================================================================
root@Gavin:~/run_left#
```

上述用例，在执行过程中，收集到了28个测试用例（`collected 28 items `），执行过程中被中断（`Ctrl+C中断，KeyboardInterrupt`），最终显示`1 failed, 7 passed in 1.42s`，说明执行了8个测试用例，7个通过1个失败了，还余下20个测试用例没有被执行。相应的记录到`test_status.json`文件，内容如下：

```shell
root@Gavin:~/run_left# cat test_status.json | json_pp
{
   "test_example.py::test_example_1" : "passed",
   "test_example.py::test_example_2" : "failed",
   "test_example.py::test_example_3" : "passed",
   "test_example.py::test_example_4" : "passed",
   "test_example_boolean.py::test_and_operation" : "passed",
   "test_example_boolean.py::test_bool_false" : "passed",
   "test_example_boolean.py::test_bool_true" : "passed",
   "test_example_boolean.py::test_or_operation" : "passed"
}
root@Gavin:~/run_left#
```
也说明执行了8个测试用例，7个通过1个失败了，内容和执行用例过程中的屏显输出是匹配的上的。

接下来我们验证一下，余下的20个用例是不是能够被正常执行，已经执行过了的测试用例，是否会被跳过：

```shell
root@Gavin:~/run_left# pytest -s -v
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-41-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'progress': '1.2.5', 'order': '1.2.1', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/run_left
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, progress-1.2.5, order-1.2.1, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 28 items                                                                                                                                                                                                                                       

test_example.py::test_example_1 SKIPPED (Skipping test_example.py::test_example_1, already passed.)
test_example.py::test_example_2 SKIPPED (Skipping test_example.py::test_example_2, already passed.)
test_example.py::test_example_3 SKIPPED (Skipping test_example.py::test_example_3, already passed.)
test_example.py::test_example_4 SKIPPED (Skipping test_example.py::test_example_4, already passed.)
test_example_boolean.py::test_bool_true SKIPPED (Skipping test_example_boolean.py::test_bool_true, already passed.)
test_example_boolean.py::test_bool_false SKIPPED (Skipping test_example_boolean.py::test_bool_false, already passed.)
test_example_boolean.py::test_and_operation SKIPPED (Skipping test_example_boolean.py::test_and_operation, already passed.)
test_example_boolean.py::test_or_operation SKIPPED (Skipping test_example_boolean.py::test_or_operation, already passed.)
test_example_boolean.py::test_not_operation PASSED
test_example_dict.py::test_set_item PASSED
test_example_dict.py::test_remove_item PASSED
test_example_dict.py::test_get_item PASSED
test_example_dict.py::test_keys PASSED
test_example_dict.py::test_values PASSED
test_example_list.py::test_append PASSED
test_example_list.py::test_remove PASSED
test_example_list.py::test_index PASSED
test_example_list.py::test_sort PASSED
test_example_list.py::test_reverse PASSED
test_example_math.py::test_addition PASSED
test_example_math.py::test_subtraction PASSED
test_example_math.py::test_multiplication PASSED
test_example_math.py::test_division PASSED
test_example_string.py::test_concatenation PASSED
test_example_string.py::test_uppercase PASSED
test_example_string.py::test_lowercase PASSED
test_example_string.py::test_find_substring PASSED
test_example_string.py::test_replace PASSEDResults saved in test_status.json


============================================================================================================= 20 passed, 8 skipped in 2.10s ==============================================================================================================
root@Gavin:~/run_left#
```
预期目标达成了么？似乎还少了点啥？如果我再次执行，是否会忽略此次执行的20个测试用例，再次执行了第一次被执行过了的8个测试用例呢？如果再再次执行，是否会如此反复、反复如此呢？

继续验证一下：

在第二次执行了余下的20个测试用例后，文件`test_status.json`内容如下：

```shell
root@Gavin:~/run_left# cat test_status.json | json_pp
{
   "test_example.py::test_example_1" : "passed",
   "test_example.py::test_example_2" : "failed",
   "test_example.py::test_example_3" : "passed",
   "test_example.py::test_example_4" : "passed",
   "test_example_boolean.py::test_and_operation" : "passed",
   "test_example_boolean.py::test_bool_false" : "passed",
   "test_example_boolean.py::test_bool_true" : "passed",
   "test_example_boolean.py::test_not_operation" : "passed",
   "test_example_boolean.py::test_or_operation" : "passed",
   "test_example_dict.py::test_get_item" : "passed",
   "test_example_dict.py::test_keys" : "passed",
   "test_example_dict.py::test_remove_item" : "passed",
   "test_example_dict.py::test_set_item" : "passed",
   "test_example_dict.py::test_values" : "passed",
   "test_example_list.py::test_append" : "passed",
   "test_example_list.py::test_index" : "passed",
   "test_example_list.py::test_remove" : "passed",
   "test_example_list.py::test_reverse" : "passed",
   "test_example_list.py::test_sort" : "passed",
   "test_example_math.py::test_addition" : "passed",
   "test_example_math.py::test_division" : "passed",
   "test_example_math.py::test_multiplication" : "passed",
   "test_example_math.py::test_subtraction" : "passed",
   "test_example_string.py::test_concatenation" : "passed",
   "test_example_string.py::test_find_substring" : "passed",
   "test_example_string.py::test_lowercase" : "passed",
   "test_example_string.py::test_replace" : "passed",
   "test_example_string.py::test_uppercase" : "passed"
}
root@Gavin:~/run_left# 
```

第三次执行用例：

```shell
root@Gavin:~/run_left# pytest -s -v
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-41-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'progress': '1.2.5', 'order': '1.2.1', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/run_left
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, progress-1.2.5, order-1.2.1, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 28 items                                                                                                                                                                                                                                       

test_example.py::test_example_1 SKIPPED (Skipping test_example.py::test_example_1, already passed.)
test_example.py::test_example_2 SKIPPED (Skipping test_example.py::test_example_2, already passed.)
test_example.py::test_example_3 SKIPPED (Skipping test_example.py::test_example_3, already passed.)
test_example.py::test_example_4 SKIPPED (Skipping test_example.py::test_example_4, already passed.)
test_example_boolean.py::test_bool_true SKIPPED (Skipping test_example_boolean.py::test_bool_true, already passed.)
test_example_boolean.py::test_bool_false SKIPPED (Skipping test_example_boolean.py::test_bool_false, already passed.)
test_example_boolean.py::test_and_operation SKIPPED (Skipping test_example_boolean.py::test_and_operation, already passed.)
test_example_boolean.py::test_or_operation SKIPPED (Skipping test_example_boolean.py::test_or_operation, already passed.)
test_example_boolean.py::test_not_operation SKIPPED (Skipping test_example_boolean.py::test_not_operation, already passed.)
test_example_dict.py::test_set_item SKIPPED (Skipping test_example_dict.py::test_set_item, already passed.)
test_example_dict.py::test_remove_item SKIPPED (Skipping test_example_dict.py::test_remove_item, already passed.)
test_example_dict.py::test_get_item SKIPPED (Skipping test_example_dict.py::test_get_item, already passed.)
test_example_dict.py::test_keys SKIPPED (Skipping test_example_dict.py::test_keys, already passed.)
test_example_dict.py::test_values SKIPPED (Skipping test_example_dict.py::test_values, already passed.)
test_example_list.py::test_append SKIPPED (Skipping test_example_list.py::test_append, already passed.)
test_example_list.py::test_remove SKIPPED (Skipping test_example_list.py::test_remove, already passed.)
test_example_list.py::test_index SKIPPED (Skipping test_example_list.py::test_index, already passed.)
test_example_list.py::test_sort SKIPPED (Skipping test_example_list.py::test_sort, already passed.)
test_example_list.py::test_reverse SKIPPED (Skipping test_example_list.py::test_reverse, already passed.)
test_example_math.py::test_addition SKIPPED (Skipping test_example_math.py::test_addition, already passed.)
test_example_math.py::test_subtraction SKIPPED (Skipping test_example_math.py::test_subtraction, already passed.)
test_example_math.py::test_multiplication SKIPPED (Skipping test_example_math.py::test_multiplication, already passed.)
test_example_math.py::test_division SKIPPED (Skipping test_example_math.py::test_division, already passed.)
test_example_string.py::test_concatenation SKIPPED (Skipping test_example_string.py::test_concatenation, already passed.)
test_example_string.py::test_uppercase SKIPPED (Skipping test_example_string.py::test_uppercase, already passed.)
test_example_string.py::test_lowercase SKIPPED (Skipping test_example_string.py::test_lowercase, already passed.)
test_example_string.py::test_find_substring SKIPPED (Skipping test_example_string.py::test_find_substring, already passed.)
test_example_string.py::test_replace SKIPPED (Skipping test_example_string.py::test_replace, already passed.)Results saved in test_status.json


================================================================================================================== 28 skipped in 0.04s ===================================================================================================================
root@Gavin:~/run_left#
```

28个测试用例全部被忽略了，这是因为文件`test_status.json`内容是追加式增加被执行过了的测试用例，从而避免了我们忧虑的问题。


## 方案二：使用pytest的pytest-rerunfailures插件与环境变量

通过保存已完成测试的`nodeid`到环境变量中，在下次运行时读取并跳过已完成的测试。

文件`conftest.py`内容参考如下：

```python
import pytest
import json
import os
import signal
import atexit

# 状态文件路径
STATUS_FILE = "test_status.json"
completed_tests = set()
interrupted = False

# 读取状态
def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()

# 保存状态
def save_status():
    with open(STATUS_FILE, 'w') as f:
        json.dump(list(completed_tests), f)

# 添加命令行选项
def pytest_addoption(parser):
    parser.addoption("--run-until-complete", action="store_true", help="Run until all tests are completed")

# 配置处理
def pytest_configure(config):
    global completed_tests
    if config.getoption("--run-until-complete"):
        completed_tests = load_status()

# 测试设置钩子
def pytest_runtest_setup(item):
    if item.config.getoption("--run-until-complete"):
        if item.nodeid in completed_tests:
            pytest.skip(f"Skipping {item.nodeid}, already executed and passed")

# 测试报告钩子
def pytest_runtest_logreport(report):
    if report.when == 'call' and report.outcome == 'passed':
        completed_tests.add(report.nodeid)
        save_status()

# 进程中断处理
def handle_exit(signum, frame):
    global interrupted
    interrupted = True
    save_status()
    print(f"\nInterrupted! Results saved in {STATUS_FILE}")
    exit(1)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
atexit.register(save_status)

# 会话结束钩子
def pytest_sessionfinish(session, exitstatus):
    if not interrupted:
        save_status()
        print(f"Results saved in {STATUS_FILE}")
```


我们看下执行效果：

第一次执行，中间发生中断：

```shell
root@Gavin:~/run_left# pytest -s -v
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-41-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'progress': '1.2.5', 'order': '1.2.1', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/run_left
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, progress-1.2.5, order-1.2.1, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 28 items                                                                                                                                                                                                                                       

test_example.py::test_example_1 PASSED
test_example.py::test_example_2 FAILED
test_example.py::test_example_3 PASSED
test_example.py::test_example_4 PASSED
test_example_boolean.py::test_bool_true PASSED
test_example_boolean.py::test_bool_false PASSED
test_example_boolean.py::test_and_operation PASSED
test_example_boolean.py::test_or_operation PASSED
test_example_boolean.py::test_not_operation ^C
Interrupted! Results saved in test_status.json
FAILED
test_example_dict.py::test_set_item PASSED
test_example_dict.py::test_remove_item PASSED
test_example_dict.py::test_get_item PASSED
test_example_dict.py::test_keys PASSED
test_example_dict.py::test_values PASSED
test_example_list.py::test_append PASSED
test_example_list.py::test_remove PASSED
test_example_list.py::test_index PASSED
test_example_list.py::test_sort PASSED
test_example_list.py::test_reverse PASSED
test_example_math.py::test_addition PASSED
test_example_math.py::test_subtraction PASSED
test_example_math.py::test_multiplication PASSED
test_example_math.py::test_division PASSED
test_example_string.py::test_concatenation PASSED
test_example_string.py::test_uppercase PASSED
test_example_string.py::test_lowercase PASSED
test_example_string.py::test_find_substring PASSED
test_example_string.py::test_replace PASSED

======================================================================================================================== FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example_2 _____________________________________________________________________________________________________________________

    def test_example_2():
>       assert 1 == 2  # 这个测试用例会失败
E       assert 1 == 2

test_example.py:7: AssertionError
___________________________________________________________________________________________________________________ test_not_operation ___________________________________________________________________________________________________________________

    def test_not_operation():
        assert not False == True
>       time.sleep(5)

test_example_boolean.py:17: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
conftest.py:52: in handle_exit
    exit(1)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = Use exit() or Ctrl-D (i.e. EOF) to exit, code = 1

>   ???
E   SystemExit: 1

<frozen _sitebuiltins>:26: SystemExit
================================================================================================================ short test summary info =================================================================================================================
FAILED test_example.py::test_example_2 - assert 1 == 2
FAILED test_example_boolean.py::test_not_operation - SystemExit: 1
============================================================================================================== 2 failed, 26 passed in 0.61s ==============================================================================================================
root@Gavin:~/run_left#
```

显示2个执行失败，26个成功的，生成的`test_status.json`文件内容参考如下：

```shell
root@Gavin:~/run_left# cat test_
test_example_boolean.py  test_example_dict.py     test_example_list.py     test_example_math.py     test_example.py          test_example_string.py   test_status.json         
root@Gavin:~/run_left# cat test_status.json | json_pp
[
   "test_example_dict.py::test_keys",
   "test_example_list.py::test_index",
   "test_example_string.py::test_concatenation",
   "test_example_dict.py::test_values",
   "test_example_boolean.py::test_and_operation",
   "test_example_dict.py::test_set_item",
   "test_example_math.py::test_subtraction",
   "test_example_list.py::test_reverse",
   "test_example_string.py::test_replace",
   "test_example_dict.py::test_get_item",
   "test_example_list.py::test_append",
   "test_example_dict.py::test_remove_item",
   "test_example_string.py::test_uppercase",
   "test_example_string.py::test_find_substring",
   "test_example.py::test_example_4",
   "test_example.py::test_example_1",
   "test_example_list.py::test_remove",
   "test_example_string.py::test_lowercase",
   "test_example_math.py::test_addition",
   "test_example_boolean.py::test_bool_true",
   "test_example_boolean.py::test_or_operation",
   "test_example_boolean.py::test_bool_false",
   "test_example_math.py::test_division",
   "test_example_math.py::test_multiplication",
   "test_example.py::test_example_3",
   "test_example_list.py::test_sort"
]
root@Gavin:~/run_left# 
```

再次执行测试用例，此时携带参数`--run-until-complete`:

```shell
root@Gavin:~/run_left# pytest -s -v --run-until-complete
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-41-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'progress': '1.2.5', 'order': '1.2.1', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/run_left
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, progress-1.2.5, order-1.2.1, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 28 items                                                                                                                                                                                                                                       

test_example.py::test_example_1 SKIPPED (Skipping test_example.py::test_example_1, already executed and passed)
test_example.py::test_example_2 FAILED
test_example.py::test_example_3 SKIPPED (Skipping test_example.py::test_example_3, already executed and passed)
test_example.py::test_example_4 SKIPPED (Skipping test_example.py::test_example_4, already executed and passed)
test_example_boolean.py::test_bool_true SKIPPED (Skipping test_example_boolean.py::test_bool_true, already executed and passed)
test_example_boolean.py::test_bool_false SKIPPED (Skipping test_example_boolean.py::test_bool_false, already executed and passed)
test_example_boolean.py::test_and_operation SKIPPED (Skipping test_example_boolean.py::test_and_operation, already executed and passed)
test_example_boolean.py::test_or_operation SKIPPED (Skipping test_example_boolean.py::test_or_operation, already executed and passed)
test_example_boolean.py::test_not_operation PASSED
test_example_dict.py::test_set_item SKIPPED (Skipping test_example_dict.py::test_set_item, already executed and passed)
test_example_dict.py::test_remove_item SKIPPED (Skipping test_example_dict.py::test_remove_item, already executed and passed)
test_example_dict.py::test_get_item SKIPPED (Skipping test_example_dict.py::test_get_item, already executed and passed)
test_example_dict.py::test_keys SKIPPED (Skipping test_example_dict.py::test_keys, already executed and passed)
test_example_dict.py::test_values SKIPPED (Skipping test_example_dict.py::test_values, already executed and passed)
test_example_list.py::test_append SKIPPED (Skipping test_example_list.py::test_append, already executed and passed)
test_example_list.py::test_remove SKIPPED (Skipping test_example_list.py::test_remove, already executed and passed)
test_example_list.py::test_index SKIPPED (Skipping test_example_list.py::test_index, already executed and passed)
test_example_list.py::test_sort SKIPPED (Skipping test_example_list.py::test_sort, already executed and passed)
test_example_list.py::test_reverse SKIPPED (Skipping test_example_list.py::test_reverse, already executed and passed)
test_example_math.py::test_addition SKIPPED (Skipping test_example_math.py::test_addition, already executed and passed)
test_example_math.py::test_subtraction SKIPPED (Skipping test_example_math.py::test_subtraction, already executed and passed)
test_example_math.py::test_multiplication SKIPPED (Skipping test_example_math.py::test_multiplication, already executed and passed)
test_example_math.py::test_division SKIPPED (Skipping test_example_math.py::test_division, already executed and passed)
test_example_string.py::test_concatenation SKIPPED (Skipping test_example_string.py::test_concatenation, already executed and passed)
test_example_string.py::test_uppercase SKIPPED (Skipping test_example_string.py::test_uppercase, already executed and passed)
test_example_string.py::test_lowercase SKIPPED (Skipping test_example_string.py::test_lowercase, already executed and passed)
test_example_string.py::test_find_substring SKIPPED (Skipping test_example_string.py::test_find_substring, already executed and passed)
test_example_string.py::test_replace SKIPPED (Skipping test_example_string.py::test_replace, already executed and passed)Results saved in test_status.json


======================================================================================================================== FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example_2 _____________________________________________________________________________________________________________________

    def test_example_2():
>       assert 1 == 2  # 这个测试用例会失败
E       assert 1 == 2

test_example.py:7: AssertionError
================================================================================================================ short test summary info =================================================================================================================
FAILED test_example.py::test_example_2 - assert 1 == 2
======================================================================================================== 1 failed, 1 passed, 26 skipped in 5.14s =========================================================================================================
root@Gavin:~/run_left#
```

显示执行失败的用例和未被执行的用例被执行，上一次被执行过的测试用例被忽略，且会同步更新文件`test_status.json`内容，当第三次执行时候，只执行所有失败的测试用例，此时效果等同于插接件`pytest-rerunfailures`:

如下是第三次执行效果：

```shell
root@Gavin:~/run_left# cat test_status.json  | json_pp
[
   "test_example_dict.py::test_get_item",
   "test_example_string.py::test_uppercase",
   "test_example_math.py::test_addition",
   "test_example_boolean.py::test_bool_true",
   "test_example_dict.py::test_remove_item",
   "test_example_math.py::test_division",
   "test_example_dict.py::test_keys",
   "test_example_list.py::test_sort",
   "test_example_list.py::test_reverse",
   "test_example_math.py::test_subtraction",
   "test_example_boolean.py::test_and_operation",
   "test_example.py::test_example_4",
   "test_example_dict.py::test_set_item",
   "test_example.py::test_example_1",
   "test_example_boolean.py::test_or_operation",
   "test_example_list.py::test_append",
   "test_example_math.py::test_multiplication",
   "test_example_boolean.py::test_bool_false",
   "test_example.py::test_example_3",
   "test_example_boolean.py::test_not_operation",
   "test_example_string.py::test_lowercase",
   "test_example_string.py::test_replace",
   "test_example_string.py::test_find_substring",
   "test_example_list.py::test_remove",
   "test_example_list.py::test_index",
   "test_example_string.py::test_concatenation",
   "test_example_dict.py::test_values"
]
root@Gavin:~/run_left# cat test_status.json  | json_pp | wc -l
29
root@Gavin:~/run_left# pytest -s -v --run-until-complete
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.2.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-41-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.2.2', 'pluggy': '1.5.0'}, 'Plugins': {'random-order': '1.1.1', 'cov': '5.0.0', 'tornasync': '0.6.0.post2', 'instafail': '0.5.0', 'metadata': '3.1.1', 'check': '2.3.1', 'asyncio': '0.23.7', 'rerunfailures': '14.0', 'xdist': '3.6.1', 'selenium': '4.1.0', 'variables': '3.1.0', 'timeout': '2.3.1', 'html': '4.1.1', 'progress': '1.2.5', 'order': '1.2.1', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'allure-pytest': '2.13.5', 'dotenv': '0.5.2'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
sensitiveurl: .*
rootdir: /root/run_left
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, progress-1.2.5, order-1.2.1, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 28 items                                                                                                                                                                                                                                       

test_example.py::test_example_1 SKIPPED (Skipping test_example.py::test_example_1, already executed and passed)
test_example.py::test_example_2 FAILED
test_example.py::test_example_3 SKIPPED (Skipping test_example.py::test_example_3, already executed and passed)
test_example.py::test_example_4 SKIPPED (Skipping test_example.py::test_example_4, already executed and passed)
test_example_boolean.py::test_bool_true SKIPPED (Skipping test_example_boolean.py::test_bool_true, already executed and passed)
test_example_boolean.py::test_bool_false SKIPPED (Skipping test_example_boolean.py::test_bool_false, already executed and passed)
test_example_boolean.py::test_and_operation SKIPPED (Skipping test_example_boolean.py::test_and_operation, already executed and passed)
test_example_boolean.py::test_or_operation SKIPPED (Skipping test_example_boolean.py::test_or_operation, already executed and passed)
test_example_boolean.py::test_not_operation SKIPPED (Skipping test_example_boolean.py::test_not_operation, already executed and passed)
test_example_dict.py::test_set_item SKIPPED (Skipping test_example_dict.py::test_set_item, already executed and passed)
test_example_dict.py::test_remove_item SKIPPED (Skipping test_example_dict.py::test_remove_item, already executed and passed)
test_example_dict.py::test_get_item SKIPPED (Skipping test_example_dict.py::test_get_item, already executed and passed)
test_example_dict.py::test_keys SKIPPED (Skipping test_example_dict.py::test_keys, already executed and passed)
test_example_dict.py::test_values SKIPPED (Skipping test_example_dict.py::test_values, already executed and passed)
test_example_list.py::test_append SKIPPED (Skipping test_example_list.py::test_append, already executed and passed)
test_example_list.py::test_remove SKIPPED (Skipping test_example_list.py::test_remove, already executed and passed)
test_example_list.py::test_index SKIPPED (Skipping test_example_list.py::test_index, already executed and passed)
test_example_list.py::test_sort SKIPPED (Skipping test_example_list.py::test_sort, already executed and passed)
test_example_list.py::test_reverse SKIPPED (Skipping test_example_list.py::test_reverse, already executed and passed)
test_example_math.py::test_addition SKIPPED (Skipping test_example_math.py::test_addition, already executed and passed)
test_example_math.py::test_subtraction SKIPPED (Skipping test_example_math.py::test_subtraction, already executed and passed)
test_example_math.py::test_multiplication SKIPPED (Skipping test_example_math.py::test_multiplication, already executed and passed)
test_example_math.py::test_division SKIPPED (Skipping test_example_math.py::test_division, already executed and passed)
test_example_string.py::test_concatenation SKIPPED (Skipping test_example_string.py::test_concatenation, already executed and passed)
test_example_string.py::test_uppercase SKIPPED (Skipping test_example_string.py::test_uppercase, already executed and passed)
test_example_string.py::test_lowercase SKIPPED (Skipping test_example_string.py::test_lowercase, already executed and passed)
test_example_string.py::test_find_substring SKIPPED (Skipping test_example_string.py::test_find_substring, already executed and passed)
test_example_string.py::test_replace SKIPPED (Skipping test_example_string.py::test_replace, already executed and passed)Results saved in test_status.json


======================================================================================================================== FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example_2 _____________________________________________________________________________________________________________________

    def test_example_2():
>       assert 1 == 2  # 这个测试用例会失败
E       assert 1 == 2

test_example.py:7: AssertionError
================================================================================================================ short test summary info =================================================================================================================
FAILED test_example.py::test_example_2 - assert 1 == 2
============================================================================================================= 1 failed, 27 skipped in 0.14s ==============================================================================================================
root@Gavin:~/run_left#
```

## 方案三：使用数据库存储测试状态

使用数据库（如`SQLite`）来存储测试状态，并在运行过程中查询和更新这些状态。

如果没有安装`SQLite`，执行如下命令进行安装：

```shell
pip install sqlite
```

接下来，逐步实现目标，先创建`utils/database.py`文件：

### utils/database.py文件

```python
import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tests (
        id integer PRIMARY KEY,
        nodeid text NOT NULL UNIQUE,
        status text
    );
    """
    conn.execute(create_table_sql)
    conn.commit()

def insert_test_status(conn, nodeid, status):
    sql = ''' INSERT OR REPLACE INTO tests(nodeid, status) VALUES(?, ?) '''
    conn.execute(sql, (nodeid, status))
    conn.commit()

def get_test_status(conn, nodeid):
    sql = 'SELECT status FROM tests WHERE nodeid=?'
    cur = conn.cursor()
    cur.execute(sql, (nodeid,))
    row = cur.fetchone()
    return row[0] if row else None

def get_all_test_status(conn):
    sql = 'SELECT nodeid FROM tests WHERE status="passed"'
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return [row[0] for row in rows]
```

## 文件conftest.py内容

```python
import pytest
import sqlite3
import os
from utils.database import create_connection, create_table, insert_test_status, get_test_status, get_all_test_status

DB_FILE = "test_status.db"

def pytest_addoption(parser):
    parser.addoption("--run-until-complete", action="store_true", help="Run until all tests are completed")

# 确保数据库表被创建
def pytest_configure(config):
    conn = create_connection(DB_FILE)
    create_table(conn)
    conn.close()

def pytest_sessionstart(session):
    # 在pytest session开始时确保表存在
    conn = create_connection(DB_FILE)
    create_table(conn)
    conn.close()

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    if item.config.getoption("--run-until-complete"):
        conn = create_connection(DB_FILE)
        nodeid = item.nodeid
        status = get_test_status(conn, nodeid)

        if status == "passed":
            pytest.skip(f"Skipping {item.nodeid}, already executed and passed.")
        conn.close()

def pytest_runtest_logreport(report):
    if report.when == 'call':
        conn = create_connection(DB_FILE)
        status = "passed" if report.outcome == "passed" else "failed"
        insert_test_status(conn, report.nodeid, status)
        conn.close()

def pytest_collection_modifyitems(session, config, items):
    if config.getoption("--run-until-complete"):
        conn = create_connection(DB_FILE)
        completed_tests = get_all_test_status(conn)
        remaining_tests = [item for item in items if item.nodeid not in completed_tests]
        items[:] = remaining_tests
        conn.close()
```

## 运行效果

第一次执行，并中断测试用例的执行：

```shell
root@Gavin:~/run_left# pytest
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.2.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/run_left
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, progress-1.2.5, order-1.2.1, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 28 items                                                                                                                                                                                                                                       

test_example.py .F..                                                                                                                                                                                                                               [ 14%]
test_example_boolean.py ....^C

======================================================================================================================== FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example_2 _____________________________________________________________________________________________________________________

    def test_example_2():
>       assert 1 == 2  # 这个测试用例会失败
E       assert 1 == 2

test_example.py:7: AssertionError
================================================================================================================ short test summary info =================================================================================================================
FAILED test_example.py::test_example_2 - assert 1 == 2
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! KeyboardInterrupt !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
/root/run_left/test_example_boolean.py:17: KeyboardInterrupt
(to show a full traceback on KeyboardInterrupt use --full-trace)
============================================================================================================== 1 failed, 7 passed in 0.59s ===============================================================================================================
root@Gavin:~/run_left#
```

此时生成了数据库文件`test_status.db`：

```shell
root@Gavin:~/run_left# ll
total 64
drwxr-xr-x  5 root root  4096 Jun 21 16:36 ./
drwx------ 43 root root  4096 Jun 21 16:36 ../
-rw-r--r--  1 root root  1601 Jun 21 16:33 conftest.py
drwxr-xr-x  2 root root  4096 Jun 21 16:36 __pycache__/
drwxr-xr-x  3 root root  4096 Jun 21 16:36 .pytest_cache/
-rw-r--r--  1 root root   170 Jun 21 16:36 sql.py
-rw-r--r--  1 root root   308 Jun 21 16:02 test_example_boolean.py
-rw-r--r--  1 root root   636 Jun 21 14:34 test_example_dict.py
-rw-r--r--  1 root root   429 Jun 21 14:33 test_example_list.py
-rw-r--r--  1 root root   185 Jun 21 14:33 test_example_math.py
-rw-r--r--  1 root root   210 Jun 21 14:32 test_example.py
-rw-r--r--  1 root root   364 Jun 21 14:33 test_example_string.py
-rw-r--r--  1 root root 12288 Jun 21 16:36 test_status.db
drwxr-xr-x  3 root root  4096 Jun 21 16:34 utils/
root@Gavin:~/run_left#
```

增加一个查询sqlite数据库代码：

```python
root@Gavin:~/run_left# cat sql.py 
import sqlite3 
conn = sqlite3.connect("test_status.db")
cur = conn.cursor()
cur.execute("select * from tests ")

for row in cur.fetchall():
    print(row)

conn.close()
```

第一次执行用例中断后，查询看看有哪些测试用例被执行到：

```shell
root@Gavin:~/run_left# python3 sql.py 
(1, 'test_example.py::test_example_1', 'passed')
(2, 'test_example.py::test_example_2', 'failed')
(3, 'test_example.py::test_example_3', 'passed')
(4, 'test_example.py::test_example_4', 'passed')
(5, 'test_example_boolean.py::test_bool_true', 'passed')
(6, 'test_example_boolean.py::test_bool_false', 'passed')
(7, 'test_example_boolean.py::test_and_operation', 'passed')
(8, 'test_example_boolean.py::test_or_operation', 'passed')
root@Gavin:~/run_left# 
```

再次执行用例，携带上参数`--run-until-complete`:

```shell
pytest --run-until-complete
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.2.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/run_left
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, progress-1.2.5, order-1.2.1, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 28 items                                                                                                                                                                                                                                       

test_example.py F                                                                                                                                                                                                                                  [  4%]
test_example_boolean.py .                                                                                                                                                                                                                          [  9%]
test_example_dict.py .....                                                                                                                                                                                                                         [ 33%]
test_example_list.py .....                                                                                                                                                                                                                         [ 57%]
test_example_math.py ....                                                                                                                                                                                                                          [ 76%]
test_example_string.py .....                                                                                                                                                                                                                       [100%]

======================================================================================================================== FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example_2 _____________________________________________________________________________________________________________________

    def test_example_2():
>       assert 1 == 2  # 这个测试用例会失败
E       assert 1 == 2

test_example.py:7: AssertionError
================================================================================================================ short test summary info =================================================================================================================
FAILED test_example.py::test_example_2 - assert 1 == 2
============================================================================================================== 1 failed, 20 passed in 5.16s ==============================================================================================================
root@Gavin:~/run_left# 
```

此时数据库中存放的记录信息如下：

```shell
root@Gavin:~/run_left# python3 sql.py 
(1, 'test_example.py::test_example_1', 'passed')
(3, 'test_example.py::test_example_3', 'passed')
(4, 'test_example.py::test_example_4', 'passed')
(5, 'test_example_boolean.py::test_bool_true', 'passed')
(6, 'test_example_boolean.py::test_bool_false', 'passed')
(7, 'test_example_boolean.py::test_and_operation', 'passed')
(8, 'test_example_boolean.py::test_or_operation', 'passed')
(9, 'test_example.py::test_example_2', 'failed')
(10, 'test_example_boolean.py::test_not_operation', 'passed')
(11, 'test_example_dict.py::test_set_item', 'passed')
(12, 'test_example_dict.py::test_remove_item', 'passed')
(13, 'test_example_dict.py::test_get_item', 'passed')
(14, 'test_example_dict.py::test_keys', 'passed')
(15, 'test_example_dict.py::test_values', 'passed')
(16, 'test_example_list.py::test_append', 'passed')
(17, 'test_example_list.py::test_remove', 'passed')
(18, 'test_example_list.py::test_index', 'passed')
(19, 'test_example_list.py::test_sort', 'passed')
(20, 'test_example_list.py::test_reverse', 'passed')
(21, 'test_example_math.py::test_addition', 'passed')
(22, 'test_example_math.py::test_subtraction', 'passed')
(23, 'test_example_math.py::test_multiplication', 'passed')
(24, 'test_example_math.py::test_division', 'passed')
(25, 'test_example_string.py::test_concatenation', 'passed')
(26, 'test_example_string.py::test_uppercase', 'passed')
(27, 'test_example_string.py::test_lowercase', 'passed')
(28, 'test_example_string.py::test_find_substring', 'passed')
(29, 'test_example_string.py::test_replace', 'passed')
root@Gavin:~/run_left# 
```

第三次执行，只执行余下失败状态的测试用例了，此时效果等同于插接件`pytest-rerunfailures`：

```shell
root@Gavin:~/run_left# pytest --run-until-complete
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.2.2, pluggy-1.5.0
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
rootdir: /root/run_left
plugins: random-order-1.1.1, cov-5.0.0, tornasync-0.6.0.post2, instafail-0.5.0, metadata-3.1.1, check-2.3.1, asyncio-0.23.7, rerunfailures-14.0, xdist-3.6.1, selenium-4.1.0, variables-3.1.0, timeout-2.3.1, html-4.1.1, progress-1.2.5, order-1.2.1, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, allure-pytest-2.13.5, dotenv-0.5.2
asyncio: mode=Mode.STRICT
collected 28 items                                                                                                                                                                                                                                       

test_example.py F                                                                                                                                                                                                                                  [100%]

======================================================================================================================== FAILURES ========================================================================================================================
_____________________________________________________________________________________________________________________ test_example_2 _____________________________________________________________________________________________________________________

    def test_example_2():
>       assert 1 == 2  # 这个测试用例会失败
E       assert 1 == 2

test_example.py:7: AssertionError
================================================================================================================ short test summary info =================================================================================================================
FAILED test_example.py::test_example_2 - assert 1 == 2
=================================================================================================================== 1 failed in 0.12s ====================================================================================================================
root@Gavin:~/run_left# 
```

# 小结

三种方案各有千秋，读者可根据个人喜好选择，不过我更推荐方案一，更`pytestnic`(自造的词...)，更简洁。

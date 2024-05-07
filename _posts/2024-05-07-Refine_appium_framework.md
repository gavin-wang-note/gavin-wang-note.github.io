---
title: 多手机终端设备下测试用例名称区分
date: 2024-05-07 16:22:18
author: Gavin Wang
img: "/img/pytest/pytest-11.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 多手机终端设备下，pytest测试用例名称区分
categories:
    - [pytest]
    - [Automation]
    - [Appium]
tags:
    - pytest
    - Automation
    - Appium
---

# 概述

上个月基于pytest+appium+allure写了一个APP的[GUI自动化基础测试框架](https://gavin-wang-note.github.io/2024/04/20/pytest_appium_allure_app_gui/)，不过还有不足之处，此次做了一些调整，使得日志的输出和测试用例的展示（包括allure报告中展示）与对应手机终端设备id绑定，方便区分是哪部手机在执行哪个测试用例，以及allure报告清晰区分对应手机终端设备。

# 改造方向

增加内容如下：
1. 日志名称中增加手机设备id信息
2. 测试用例在收集和执行时，以及生成的allure报告，增加手机设备id和手机系统版本信息

# 调整过程

要将设备ID信息从`run_testcases`函数传递到`conftest.py`文件中的`pytest_itemcollected`钩子方法中，你可以利用`pytest`的强大`fixture`机制和配置（`conftest.py`）来实现跨文件共享数据。一种常见的做法是使用`pytest`的内置`config`对象来存储设备信息，然后在需要的地方检索该信息。


* 步骤 1: 修改`run_testcases`函数以便将设备ID信息存储在pytest的配置中

在调用`pytest.main`之前设置全局变量或使用 `pytest` 的 `addoption` 或 `pytest_configure` 钩子来实现，这里我选择的是`addoption`。

首先，在项目根目录下的`conftest.py`中设置一个自定义的配置选项来存储设备信息：

```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--device_id", action="store", default="default_device_id",
                     help="Device ID for mobile device tests")
    parser.addoption("--brand_name", action="store", default="default_brand_name",
                     help="Brand name for mobile device tests")
    parser.addoption("--platform_version", action="store", default="default_platform_version",
                     help="Phone device's plantform version for mobile device tests")
```

然后，在`run_testcases`函数中，在调用`pytest.main`时传递这个手机设备ID信息作为命令行参数：

```python
# run.py
def run_testcases(variables_file):
    """运行测试用例"""
    env = os.environ.copy()
    if 'linux' in os_type:
        allure_path = '/usr/lib/allure-2.27.0/bin'  # 根据实际情况修改
        env['PATH'] = f'{allure_path}:' + env['PATH']

    device = variables_file.split('_')[-1].split('.')[0]
    report_base_path = f"{paths['report']}/{device}"
    log_file = f"{paths['log']}/app_automation_{device}_test.log"

    # 在这里构建你的 pytest 命令并包含设备 ID，手机版本和品牌信息
    with open(f"{paths['config']}/{device}.json", 'r', encoding='utf-8') as file_handle:
        brand_version = yaml.load(file_handle, Loader=yaml.FullLoader)
    brand_name = brand_version['brand_name'].split('\n')[0]
    platform_version = brand_version['platform_version']

    pytest_args = ["--alluredir", f"{report_base_path}/json", "--variables", f"{variables_file}",
                   "--log-file", f"{log_file}", f"--device_id={device}", f"--brand_name={brand_name}",
                   f"--platform_version={platform_version}"]
    pytest.main(pytest_args)
    # 运行 allure 命令和剩余的代码不变
```

步骤 2: 在`testcase/conftest.py`中利用`pytest_configurehook`函数来捕获和传递设备ID信息到测试用例

```python
# testcase/conftest.py
def pytest_configure(config):
    config.device_id = config.getoption("--device_id")
    config.brand_name = config.getoption("--brand_name")
    config.platform_version = config.getoption("--platform_version")
```

步骤 3: 在需要的地方(`testcase/conftest.py`)，例如`pytest_itemcollected`钩子函数，使用存储的设备ID信息

```python
# testcase/conftest.py
def pytest_itemcollected(item):
    device_id = item.config.device_id  # get phone's device id info
    brand_name = item.config.brand_name # get phone's brand info
    platform_version = item.config.platform_version # get phone's platformVersion info
    item.name = f"[{brand_name}_{platform_version}_{device_id}]" + '_' + item.name

    print(f"Test case name was modified to: {item.name}")
```

这样，就可以在测试运行时将设备ID传递给`run_testcases`函数，并且该设备ID将在整个`pytest`会话中可用，包括`conftest.py`钩子方法中。

这是大致思路，除此之外还有一些细节点需要调整，比如如何获取`brand_name`和`platform_version`，参考如下(部分)：

```python
# common/app_info.py
def get_brand(device_id: str) -> str:
    """获取手机品牌"""
    cmd = f"adb -s {device_id} shell getprop ro.product.brand"
    result = exec_cmd(cmd)
    if result:
        return result
    else:
        raise NameError("未获取到手机品牌信息，请确认设备已连接并开启ADB调试模式。")

def generate_device_json(device_id: str) -> None:
    """生成对应device的json文件，内含platform version和brand信息"""
    json_file = f"{paths['config']}/{device_id}.json"
    with open(json_file, 'w') as file_handle:
        brand_name = get_brand(device_id)
        platform_version = get_devices_version(device_id)
        brand_version = {'brand_name': brand_name, 'platform_version': platform_version}
        json.dump(brand_version, file_handle, indent=4, ensure_ascii=False)
    
    logging.info("Generated %s.json success, path:(%s)", json_file)
```

在`run.py`中使用yaml解析这里生成的`{device_id}.json`文件，从而形成手机终端设备与`log`文件的匹配关系：

```shell
root@Gavin:~/MobileAppTestFramework/config# ll
total 28
drwxr-xr-x 2 root root 4096 May  7 15:03 ./
drwxr-xr-x 9 root root 4096 May  7 16:18 ../
-rw-r--r-- 1 root root   62 May  7 15:03 4f54ea68.json
-rw-r--r-- 1 root root   62 May  7 15:03 62b6aca8.json
-rw-r--r-- 1 root root  167 May  7 10:09 config.yml
-rw-r--r-- 1 root root    0 Apr 20 11:28 __init__.py
-rw-r--r-- 1 root root  522 May  7 15:03 variables_4f54ea68.json
-rw-r--r-- 1 root root  522 May  7 15:03 variables_62b6aca8.json
root@Gavin:~/MobileAppTestFramework/config#
```

log文件名称信息：

```shell
root@Gavin:~/MobileAppTestFramework/report/log# ll
total 2112
drwxr-xr-x 2 root root   4096 May  7 15:03 ./
drwxr-xr-x 5 root root   4096 May  7 15:08 ../
-rw-r--r-- 1 root root 464248 May  7 15:04 app_automation_4f54ea68_test.log
-rw-r--r-- 1 root root 486771 May  7 15:04 app_automation_62b6aca8_test.log
-rw-r--r-- 1 root root 586507 May  7 15:04 appium_4723_4f54ea68.log
-rw-r--r-- 1 root root 608036 May  7 15:04 appium_4724_62b6aca8.log
root@Gavin:~/MobileAppTestFramework/report/log#
```


# 最终的效果

多手机终端设备并行执行用例效果：

```shell
root@Gavin:~/MobileAppTestFramework# python3 run.py 
------------------------------------- 准备工作 -------------------------------------

检查操作系统类型是否为Windows或者linux

删除陈旧的variables*.json文件
  Deleted file: config/variables_4f54ea68.json
  Deleted file: config/variables_62b6aca8.json

生成全新的variables*.json文件
  生成新文件: /root/MobileAppTestFramework/config/variables_4f54ea68.json
  生成新文件: /root/MobileAppTestFramework/config/variables_62b6aca8.json

删除所有的device.json文件
  删除文件 config/4f54ea68.json

删除陈旧的variables*.json文件
  Deleted file: config/4f54ea68.json
  生成新文件 config/4f54ea68.json
  删除文件 config/62b6aca8.json

删除陈旧的variables*.json文件
  Deleted file: config/62b6aca8.json
  生成新文件 config/62b6aca8.json

接下来将执行测试用例
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
================================================================================================================== test session starts ===================================================================================================================
platform linux -- Python 3.11.6, pytest-8.0.2, pluggy-1.5.0 -- /usr/bin/python3
cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-28-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/MobileAppTestFramework
configfile: pytest.ini
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, timeout-2.2.0
asyncio: mode=Mode.STRICT
collecting ... cachedir: .pytest_cache
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
sensitiveurl: .*
metadata: {'Python': '3.11.6', 'Platform': 'Linux-6.5.0-28-generic-x86_64-with-glibc2.38', 'Packages': {'pytest': '8.0.2', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '4.1.0', 'order': '1.2.0', 'random-order': '1.1.1', 'tornasync': '0.6.0.post2', 'check': '2.2.2', 'instafail': '0.5.0', 'allure-pytest': '2.13.2', 'asyncio': '0.23.6', 'selenium': '4.1.0', 'xdist': '3.5.0', 'variables': '3.1.0', 'rerunfailures': '13.0', 'html': '4.1.1', 'progress': '1.2.5', 'metadata': '3.0.0', 'twisted': '1.14.1', 'picked': '0.5.0', 'anyio': '4.3.0', 'Faker': '24.0.0', 'trio': '0.8.0', 'repeat': '0.9.3', 'base-url': '2.1.0', 'dependency': '0.6.0', 'timeout': '2.2.0'}, 'JAVA_HOME': '/usr/lib/jdk1.8.0_171', 'Base URL': '', 'Driver': None, 'Capabilities': {}}
rootdir: /root/MobileAppTestFramework
configfile: pytest.ini
plugins: cov-4.1.0, order-1.2.0, random-order-1.1.1, tornasync-0.6.0.post2, check-2.2.2, instafail-0.5.0, allure-pytest-2.13.2, asyncio-0.23.6, selenium-4.1.0, xdist-3.5.0, variables-3.1.0, rerunfailures-13.0, html-4.1.1, progress-1.2.5, metadata-3.0.0, twisted-1.14.1, picked-0.5.0, anyio-4.3.0, Faker-24.0.0, trio-0.8.0, repeat-0.9.3, base-url-2.1.0, dependency-0.6.0, timeout-2.2.0
asyncio: mode=Mode.STRICT
collecting ... Test case name was modified to: [Xiaomi_10_4f54ea68]_test_swipe
Test case name was modified to: [xiaomi_10_62b6aca8]_test_swipe
Test case name was modified to: [Xiaomi_10_4f54ea68]_test_home_page_switch
Test case name was modified to: [Xiaomi_10_4f54ea68]_test_switch_to_recommend
Test case name was modified to: [Xiaomi_10_4f54ea68]_test_switch_to_category
Test case name was modified to: [xiaomi_10_62b6aca8]_test_home_page_switch
Test case name was modified to: [xiaomi_10_62b6aca8]_test_switch_to_recommend
Test case name was modified to: [xiaomi_10_62b6aca8]_test_switch_to_category
collected 4 items                                                                                                                                                                                                                                        

collected 4 items                                                                                                                                                                                                                                        

testcase/01_login/test_login.py::TestLogin::test_swipe PASSED                                                                                                                                                                                      [ 25%]
testcase/02_home_page/test_switch_page.py::TestSwitchpage::test_home_page_switch PASSED                                                                                                                                                                                      [ 25%]
testcase/02_home_page/test_switch_page.py::TestSwitchpage::test_home_page_switch PASSED                                                                                                                                                            [ 50%]
testcase/02_home_page/test_switch_page.py::TestSwitchpage::test_switch_to_recommend PASSED                                                                                                                                                         [ 75%]
testcase/02_home_page/test_switch_page.py::TestSwitchpage::test_switch_to_category PASSED                                                                                                                                                          [100%]

=================================================================================================================== 4 passed in 49.30s ===================================================================================================================
PASSED                                                                                                                                                            [ 50%]
testcase/02_home_page/test_switch_page.py::TestSwitchpage::test_switch_to_recommend PASSED                                                                                                                                                         [ 75%]
testcase/02_home_page/test_switch_page.py::TestSwitchpage::test_switch_to_category PASSED                                                                                                                                                          [100%]

============================================================================================================== 4 passed in 64.77s (0:01:04) ==============================================================================================================
root@Gavin:~/MobileAppTestFramework#
```


单个手机终端设备运行用例：

<img class="shadow" src="/img/in-post/修改用例名称-单设备.png" width="800">

两个手机终端运行测试用例：

<img class="shadow" src="/img/in-post/修改用例名称-多设备.png" width="800">

Allure报告中展示的效果：

<img class="shadow" src="/img/in-post/allure_report_test_case_name.png" width="800">


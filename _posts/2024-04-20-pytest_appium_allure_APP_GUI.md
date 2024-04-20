---
title: pytest+Appium+Allure测试框架设计
date: 2024-04-20 17:12:37
author: Gavin Wang
img: "/img/appium/appium7.png"
top: true
hide: false
cover: true
coverImg:
password:
toc: true
mathjax: false
summary: 基于pytest+Appium设计APP GUI自动化测试框架
categories:
    - [Automation]
    - [Appium]
    - [pytest]
tags:
    - Automation
    - Appium
    - pytest
---

# 概述

本文介绍pytest+Appium+Allure完成某APP的GUI自动化测试框架设计，此框架的设计基于PO设计模式。

通过结合pytest的灵活性和Appium的移动测试专长，我们可以创建一个强大的自动化测试解决方案，它不仅能够提高测试效率，还能确保应用在不同设备和操作系统上的一致性和稳定性。

此次间隔10年再次捡起Appium，借助pytest+appium实现了如下功能：

1. Windows和Linux平台的支持
2. 支持多设备上测试用例的执行，设备与设备之间用例执行、log记录和report等互相独立，互不干扰
3. 任意一设备异常，不影响用例在其他设备上的正常运行
4. 自动匹配设备数，自动生成不同设备的variables.json文件，借助pytest-variables插件实现配置文件独立性
5. 基于PO设计模式，加上Allure漂亮的测试报告和pytest强大的fixture特性，实现用例分层，降低框架维护难度，让使用者有更多的时间focus on业务逻辑设计
6. 异常用例自动截图并报错到指定目录



# Appium Framework简介


Appium测试框架，参考下图：

<img class="shadow" src="/img/in-post/Architecture-of-the-Appium-Framework.jpg" width="800">

测试用例执行过程示意图：

<img class="shadow" src="/img/appium/appium8.jpg" width="400">
<img class="shadow" src="/img/appium/appium7.png" width="700">


# 环境搭建

需要安装&配置的软件如下：

* 安装JAVA，设置JAVA_HOME，JRK等相关环境变量
* 安装Android SDK组件
* 安装Node.js
* 安装Appium&pytest以及pytest相关插件
* 安装Appium-Python-Client

其他python相关安装信息，参考如下：

```shell
root@Gavin:~/MobileAppTestFramework# cat requirements.txt 
allure-pytest==2.13.2
allure-python-commons==2.13.2
Appium-Python-Client==4.0.0
pytest==8.0.2
PyYAML==6.0.1
selenium==4.18.1
root@Gavin:~/MobileAppTestFramework# 
```

具体的安装&配置细节，非本文重点，就不写了，但在安装ANDROID SDK时需要科学上网。

我的测试环境是Windows 11和 Ubuntu 23两套环境，使得一套代码能够分别在Windows和Linux下运行，做到windows和Linux的兼容。



# 测试框架目录结构

测试框架目录结构参考如下：

```shell
root@Gavin:~/MobileAppTestFramework# tree
.
├── app
│   └── com.xkw.client_3.1.1.1.apk  # apk必须要存在，且必须以英文名命名
├── clear_pyc.py                    # 清理python cache目录和pyc文件
├── common            # 存放基础核心功能
│   ├── app_info.py   # 获取app的相关信息，诸如app_name,app_package_name,launchable_activity等
│   ├── appium_server.py  # 启停appium相关动作
│   ├── base_driver.py    # init driver
│   ├── base_page.py      # 基于W3C WebDriver协议，封装APP通用操作，诸如滑动、点击、文本输入、拖拽等
│   ├── __init__.py
│   ├── locators.py       # 分类存放APP各页面element信息
│   └── utils.py          # 通用函数的封装
├── config
│   ├── config.yml        # 一次配置，终生有效
│   ├── __init__.py
│   ├── variables_4f54ea68.json  # 根据当前机器连接的设备数自动生成，自动删除旧的（如果有）再生成新的
│   └── variables_62b6aca8.json  # 根据当前机器连接的设备数自动生成，自动删除旧的（如果有）再生成新的
├── conftest.py           # scope=package，记录当前正在执行的是哪个用例
├── __init__.py
├── pytest.ini            # 定义pytest默认携带的参数和日志格式
├── README.md
├── requirements.txt
├── run.py                # 执行所有测试用例的入口，方便未来CI/CD使用
├── testcase              # 分类存放APP所有功能的测试用例
│   ├── 01_login
│   │   ├── __init__.py
│   │   └── test_login.py
│   ├── 02_home_page
│   │   ├── __init__.py
│   │   └── test_switch_page.py
│   ├── 03_exam_papers
│   │   └── __init__.py
│   ├── conftest.py
│   └── __init__.py
└── testcasebase          # 存放测试用例基类，基于PO设计模式，未来APP功能有变，只需修改此处下相关文件，而不是调整testcase下用例 
    ├── __init__.py
    ├── login_page.py     # 登录相关测试用例
    └── switch_pages.py   # 页面切换、跳转相关测试用例

9 directories, 29 files
root@Gavin:~/MobileAppTestFramework#
```

整体设计思路是基于PO设计模式，借助`pytest`强大的`fixture`实现两层`conftest.py`，做到driver fixture一处定义全局使用，且日志清晰、用例分层、低可维护性和高兼容性。


# report目录

目录结构如下：

```shell
root@Gavin:~/MobileAppTestFramework/report# tree -L 3
.
├── allure
│   ├── 4f54ea68
│   │   ├── html
│   │   └── json
│   └── 62b6aca8
│       ├── html
│       └── json
├── log
│   ├── app_automation_4f54ea68_test.log
│   ├── app_automation_62b6aca8_test.log
│   ├── appium_4723.log
│   └── appium_4724.log
└── screenshot
```

日志、报告和截图，都统一存放在report目录下，按子目录来存放。


## allure report

```shell
├── allure
│   ├── 4f54ea68
│   └── 62b6aca8
``` 

这里表示allure下有两个设备产生的报告原始json文件，以及生成的html报告数据：

```shell
│   └── 62b6aca8
│       ├── html
│       │   ├── app.js
│       │   ├── data
│       │   ├── export
│       │   ├── favicon.ico
│       │   ├── history
│       │   ├── index.html
│       │   ├── plugin
│       │   ├── styles.css
│       │   └── widgets
│       └── json
│           ├── 00dbf1fe-a6c4-4b2f-b52e-053461299c35-attachment.txt
│           ├── 012a3a65-236a-4b81-aaec-3d8d4146232c-container.json
│           ├── 04913ac1-b897-411e-8986-1df178f27212-attachment.txt
│           ├── 05744b50-6d14-449f-8136-964d217df1ef-container.json
│           ├── 059f4c43-b655-4c6b-a990-2022036a7e67-container.json
│           ├── 05c7ed97-b369-4e3f-8d83-f0ad51a9b4a8-result.json
```

## log

```shell
├── log
│   ├── app_automation_4f54ea68_test.log
│   ├── app_automation_62b6aca8_test.log
│   ├── appium_4723.log
│   └── appium_4724.log
```

* `app_automation_{deviceName}_test.log`文件记录对应`deviceName`上测试用例执行日志
* `appium_{serverPort}.log`文件记录对应端口的Appium Server日志信息


## screenshot

此目录存放截图文件，只有当用例执行失败的时候才会截图，正常情况下不截图。


# 配置文件

## config/config.yml

```python
root@Gavin:~/MobileAppTestFramework/config# cat config.yml 
platformName: Android
newCommonTimeout: 36000
skipServerInstallation: True
automationName: UiAutomator2
serverPort: 4723
systemPort: 8200
root@Gavin:~/MobileAppTestFramework/config# 
```

## variables.json

借助pytest的pytest-variables插件，传递不同设备对应的variables.json文件到Appium，从而实现多设备的用例执行。

如下json文件为自动生成，内容参考如下：

```shell
root@Gavin:~/MobileAppTestFramework/config# cat variables_4f54ea68.json 
{
    "server": {
        "url": "http://127.0.0.1:4723"
    },
    "caps": {
        "platformName": "Android",
        "newCommonTimeout": 36000,
        "skipServerInstallation": true,
        "automationName": "UiAutomator2",
        "serverPort": 4723,
        "systemPort": 8200,
        "deviceName": "4f54ea68",
        "platformVersion": "10",
        "appPackage": "com.xkw.client",
        "appActivity": "com.zxxk.page.main.LauncherActivity",
        "udid": "4f54ea68"
    }
}root@Gavin:~/MobileAppTestFramework/config# cat variables_62b6aca8.json 
{
    "server": {
        "url": "http://127.0.0.1:4724"
    },
    "caps": {
        "platformName": "Android",
        "newCommonTimeout": 36000,
        "skipServerInstallation": true,
        "automationName": "UiAutomator2",
        "serverPort": 4724,
        "systemPort": 8201,
        "deviceName": "62b6aca8",
        "platformVersion": "10",
        "appPackage": "com.xkw.client",
        "appActivity": "com.zxxk.page.main.LauncherActivity",
        "udid": "62b6aca8"
    }
}root@Gavin:~/MobileAppTestFramework/config#
```

**说明：**

测试框架在设计之初就考虑了多设备、并发执行用例，实现了根据当前OS连接的手机终端设备数（USB或者WIFI连接），自动生成各个设备对应的variables.json文件，在run.py入口文件中并发传递各个variables.json文件，从而实现有多少台设备就能够启动多少个appium server和多少台设备上的测试用例执行，比如说computer连接有10台设备，有300条测试用例，则这10台设备是各自执行这300条测试用例，而且各个设备是**并行执行**的（不是设备1执行完300条用例，设备2再执行这300条用例哦），互不干扰。



# 代码示例

## common/locators.py

此文件记录APP的元素信息，内容参考如下：

```shell
root@Gavin:~/MobileAppTestFramework/common# cat locators.py 
# -*- coding:UTF-8 -*-
"""分类定义APP各个页面的元素、按钮等信息"""

from appium.webdriver.common.appiumby import AppiumBy

# 启动页同意
agree_btn = (AppiumBy.ID, "com.xkw.client:id/agree_yes")

# 登录页操作
mine_btn = (AppiumBy.ID, "com.xkw.client:id/mine_text")
login_btn = (AppiumBy.ID, "com.xkw.client:id/mine_username")
password_login_btn = (AppiumBy.ID, "com.xkw.client:id/login_mobile_use_password")
username_input = (AppiumBy.ID, "com.xkw.client:id/login_password_username")
password_input = (AppiumBy.ID, "com.xkw.client:id/login_password_password")
login_submit_btn = (AppiumBy.ID, "com.xkw.client:id/login_password_login")
discover_search_box = (AppiumBy.ID, "com.xkw.client:id/discover_search_box")

# 发现页面
discovery_btn = (AppiumBy.ID, "com.xkw.client:id/discover_text")
## 推荐页面
recommend_btn = (AppiumBy.ID, "com.xkw.client:id/recommend_text")
## 分类页面
category_btn = (AppiumBy.ID, "com.xkw.client:id/category_text")
course_synchronization_resources_btn = (AppiumBy.ID, "com.xkw.client:id/category_entrance_left")
knowledge_point_resources_btn = (AppiumBy.ID, "com.xkw.client:id/category_entrance_right")
## 我的页面，上面有定义过，mine_btn

## 通用元素
common_element = (AppiumBy.CLASS_NAME, "android.widget.TextView")
```



## common/utils.py

此文件封装通用的函数，内容参考如下：

```python
root@Gavin:~/MobileAppTestFramework/common# cat utils.py 
#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
"""通用函数的封装"""

import os
import glob
import platform

from pathlib import Path


def os_type():
    """获取操作系统类型，返回 'windows'、'linux' 之类的"""
    return platform.system().lower()


def exec_cmd(cmd):
    """执行命令行并返回内容"""
    result = os.popen(cmd).read()
    return result


# 定义和检查关键目录的路径
def define_paths():
    base_path = Path(__file__).resolve().parent.parent

    paths = {
        'app': base_path / 'app',
        'config': base_path / 'config',
        'log': base_path / 'report' / 'log',
        'report': base_path / 'report' / 'allure',
        'screenshot': base_path / 'report' / 'screenshot'
    }

    # 确保所有需要的目录都存在
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)

    return paths


def find_files(pattern='config/variables*.json'):
    """Find all files matching the given pattern."""
    return glob.glob(pattern)


def delete_files(pattern='config/variables*.json'):
    """Delete all files matching the given pattern."""
    print("\n删除陈旧的variables*.json文件")
    files_to_delete = glob.glob(pattern)
    for file_path in files_to_delete:
        os.remove(file_path)
        print(f"  Deleted file: {file_path}")

# 可以直接在其他模块中调用 define_paths 获取路径信息
paths = define_paths()
os_type = os_type()
```



## common/appium_server.py

此文件封装appium的启停动作，内容参考如下：

```python
root@Gavin:~/MobileAppTestFramework/common# cat appium_server.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""Appium启动、关闭、检查相关操作的封装"""

import socket
import logging
import subprocess

from .utils import paths, os_type, exec_cmd


def open_appium(cmd, port):
    """命令启动appium server"""
    release_port(port)
    logging.info(f"open_appium, cmd: {cmd}")
    with subprocess.Popen(cmd, shell=True) as process:
        process.wait()  # 等待命令执行完成

def close_appium():
    """关闭appium服务器"""
    kill_cmd = {"windows": "taskkill /f /im node.exe", "linux": "pkill node"}
    exec_cmd(kill_cmd[os_type])


def is_port_available(host, port):
    """检测端口是否可用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if sock.connect_ex((host, port)) == 0:  # Port is open
            return False
    return True


def release_port(port):
    """释放给定的TCP端口"""
    check_cmd = {"windows": f"netstat -ano| findstr {port}", "linux": f"netstat -anp| grep :{port}"}
    result = exec_cmd(check_cmd[os_type])
    if str(port) in result:
        pid = result.strip().split(" ")[-1]
        kill_cmd = {"windows": f"taskkill -f -pid {pid}", "linux": f"kill -9 {pid}"}
        exec_cmd(kill_cmd[os_type])
        return True
    return True
```



## 其他核心代码文件简述

当然，比较核心的是：

```shell
-rw-r--r-- 1 root root 3779 Apr 20 14:20 base_driver.py
-rw-r--r-- 1 root root 9634 Apr 20 11:28 base_page.py
```

`base_driver.py`文件，根据传入的variables.json，解析其内容，组装desired_caps内容，并初始化driver，确保windows和linux两个平台都能兼容到，且是后台执行appium命令，并增加了容错校验机制，诸如driver init是否成功，以及如何避免appium server还没有初始化好就发起HTTP请求等容错功能。

`base_page.py`文件，封装了所有通用的动作，诸如元素点击、按钮点击、文本内容清除、文本内容输入、拖拽、滑动、缩放、模拟摇一摇等功能。

除此之外，还有顶层的`conftest.py`，`testcase`目录下的`conftest.py`，以及顶层目录下的`pytest.ini`，这三个文件也是重中之重。

这5个文件组成了整个测试框架的核心。

**说明：**

由于这两个文件code内容较长且复杂，限制于篇幅原因，就不贴具体的code了。



## 测试用例基类示例

如下文件，为模拟页面滑动操作，内容参考如下：

```python
root@Gavin:~/MobileAppTestFramework/testcasebase# cat switch_pages.py 
# -*- coding:UTF-8 -*-
"""APP各个页面的切换操作的封装"""

import allure

from common import locators
from common.base_page import BasePage


class SwitchPage(BasePage):
    """ APP页面切换操作 """
    def enter_discovery(self):
        """进入发现页面"""
        with allure.step("点击切换到[发现]页面"):
            self.click_element(*locators.discovery_btn, doc='发现')
        with allure.step("检查[发现--首页] 页面元素信息"):
            elements = self.find_elements(*locators.common_element, doc="首页")
            self.check_element(elements, "试卷")
            self.check_element(elements, "杏坛荟")

        with allure.step("向左滑动，切换到[试卷]页面"):
            self.swipe_to_left(doc="试卷")
        with allure.step("检查[发现--试卷]页面元素信息"):
            elements = self.find_elements(*locators.common_element, doc="试卷")
            self.check_element(elements, "新卷上架")
            self.check_element(elements, "套卷")

        with allure.step("继续向左滑动，切换到[书城]页面"):
            self.swipe_to_left(doc="书城")
        with allure.step("检查[发现--书城]页面元素信息"):
            elements = self.find_elements(*locators.common_element, doc="书城")
            self.check_element(elements, "新书上架")
            self.check_element(elements, "加入我们")

        with allure.step("继续向左滑动，切换到[高考]页面"):
            self.swipe_to_left(doc="高考")
        with allure.step("检查[发现--高考]页面元素信息"):
            elements = self.find_elements(*locators.common_element, doc="高考")
            self.check_element(elements, "一轮复习")
            self.check_element(elements, "高考动态")

    def enter_recommend(self):
        with allure.step("点击切换到[推荐]页面"):
            self.click_element(*locators.recommend_btn, doc='推荐')
        with allure.step("检查[推荐]页面元素信息"):
            elements = self.find_elements(*locators.common_element, doc="今日")
            self.check_element(elements, "附近")

    def enter_category(self):
        with allure.step("点击切换到[分类]页面"):
            self.click_element(*locators.category_btn, doc='分类')
        with allure.step("连续多次向左滑动，切换到[中职]页面"):
            self.swipe_to_left(doc="小学")
            self.swipe_to_left(doc="初中")
            self.swipe_to_left(doc="高中")
            self.swipe_to_left(doc="中职")
        with allure.step("检查[中职]页面元素信息"):
            course_exist = self.is_element_exist(*locators.course_synchronization_resources_btn,doc="课程同步资源")
            assert course_exist == True, \
            f"[中职]页面没有找到{locators.course_synchronization_resources_btn}元素信息"

            kb_exist = self.is_element_exist(*locators.knowledge_point_resources_btn, doc="知识点资源")
            assert kb_exist == True, \
            f"[中职]页面没有找到{locators.knowledge_point_resources_btn}元素信息"
```



## 测试用例示例

测试用例按功能分目录存放，如下示例为调用基类中操作，实现GUI页面滑动和切换动作，内容参考如下：

```python
root@Gavin:~/MobileAppTestFramework/testcase/02_home_page# cat test_switch_page.py 
# -*- coding:UTF-8 -*-
"""APP页面切换测试用例"""

import pytest
import allure

from testcasebase.switch_pages import SwitchPage


@pytest.fixture(scope="module", autouse=True)
def switch_page(appium_driver):
    return SwitchPage(appium_driver)

@allure.feature("页面切换")
class TestSwitchpage:
    """APP页面切换相关的测试用例"""
    @allure.story("首页页面切换")
    @allure.description("首页页面在首页的子页面之间滑动切换")  # 用例的描述
    @allure.severity(allure.severity_level.NORMAL)
    def test_home_page_switch(self, switch_page):
        switch_page.enter_discovery()

    @allure.story("推荐页面")
    @allure.description("推荐页面检查页面内容信息")  # 用例的描述
    @allure.severity(allure.severity_level.NORMAL)
    def test_switch_to_recommend(self, switch_page):
        switch_page.enter_recommend()

    @allure.story("分类页面")
    @allure.description("分类页面检查页面内容信息")  # 用例的描述
    @allure.severity(allure.severity_level.NORMAL)
    def test_switch_to_category(self, switch_page):
        switch_page.enter_category()
```



# 用例运行效果

## Windows下

连接两台安卓设备：

```shell
C:\Users\Wang>adb devices
List of devices attached
4f54ea68        device
62b6aca8        device


C:\Users\Wang>
```

运行效果（PyCharm）：

<img class="shadow" src="/img/in-post/Windows_run_appium_testcase.png" width="800">


## Linux下

连接了两台手机，均为安卓：

```shell
root@Gavin:~/MobileAppTestFramework# adb devices
List of devices attached
4f54ea68	device
62b6aca8	device

root@Gavin:~/MobileAppTestFramework# 
```

运行效果：

<img class="shadow" src="/img/in-post/Linux_run_appium_testcase.png" width="800">


# 日志片段

在Windows下测试框架运行时产生的日志，参考如下：

```shell
2024-04-20 14:22:29 [appium_server.py:15  ] [ INFO] open_appium, cmd: appium server -ka 36000 -a 127.0.0.1 -p 4723 --allow-cors --use-plugin relaxed-caps --use-drivers uiautomator2 --use-plugin execute-driver --log "/root/MobileAppTestFramework/report/log/appium_4723.log" --local-timezone &
2024-04-20 14:22:31 [base_driver.py:74  ] [ INFO] desired_caps: {'platformName': 'Android', 'newCommonTimeout': 36000, 'skipServerInstallation': True, 'automationName': 'UiAutomator2', 'serverPort': 4723, 'systemPort': 8200, 'deviceName': '4f54ea68', 'platformVersion': '10', 'appPackage': 'com.xkw.client', 'appActivity': 'com.zxxk.page.main.LauncherActivity', 'udid': '4f54ea68'}
2024-04-20 14:22:37 [conftest.py:45  ] [ INFO] Creating common driver fixture
2024-04-20 14:22:37 [conftest.py:8   ] [ INFO] ------------------------------------- Start to run test case ---------------------------------

2024-04-20 14:22:37 [conftest.py:17  ] [ INFO] ----------------------------------- Begin ----------------------------------------
2024-04-20 14:22:37 [conftest.py:18  ] [ INFO] Current test case name : (test_swipe)
2024-04-20 14:22:37 [base_page.py:26  ] [ INFO] (同意并进入)页面，开始查找元素(('id', 'com.xkw.client:id/agree_yes'))
2024-04-20 14:22:40 [base_page.py:30  ] [ INFO] (同意并进入)页面，查找元素(('id', 'com.xkw.client:id/agree_yes'))成功！
2024-04-20 14:22:40 [base_page.py:66  ] [ INFO] (同意并进入)页面，点击元素(('id', 'com.xkw.client:id/agree_yes'))
2024-04-20 14:22:40 [base_page.py:68  ] [ INFO] (同意并进入)页面，点击元素(('id', 'com.xkw.client:id/agree_yes'))成功！
2024-04-20 14:22:40 [base_page.py:109 ] [ INFO] (发现)页面，开始查找元素(('id', 'com.xkw.client:id/discover_search_box'))
2024-04-20 14:22:46 [base_page.py:111 ] [ INFO] (发现)页面，查找元素(('id', 'com.xkw.client:id/discover_search_box'))成功！
2024-04-20 14:22:46 [conftest.py:20  ] [ INFO] ----------------------------------- End ------------------------------------------

2024-04-20 14:22:46 [conftest.py:17  ] [ INFO] ----------------------------------- Begin ----------------------------------------
2024-04-20 14:22:46 [conftest.py:18  ] [ INFO] Current test case name : (test_home_page_switch)
2024-04-20 14:22:46 [base_page.py:26  ] [ INFO] (发现)页面，开始查找元素(('id', 'com.xkw.client:id/discover_text'))
2024-04-20 14:22:47 [base_page.py:30  ] [ INFO] (发现)页面，查找元素(('id', 'com.xkw.client:id/discover_text'))成功！
2024-04-20 14:22:47 [base_page.py:66  ] [ INFO] (发现)页面，点击元素(('id', 'com.xkw.client:id/discover_text'))
2024-04-20 14:22:47 [base_page.py:68  ] [ INFO] (发现)页面，点击元素(('id', 'com.xkw.client:id/discover_text'))成功！
2024-04-20 14:22:47 [base_page.py:42  ] [ INFO] (首页)页面，开始查找一组元素(('class name', 'android.widget.TextView'))
2024-04-20 14:22:48 [base_page.py:46  ] [ INFO] (首页)页面，查找元素(('class name', 'android.widget.TextView'))成功！
2024-04-20 14:22:53 [base_page.py:136 ] [ INFO] 开始获取设备屏幕大小。
2024-04-20 14:22:53 [base_page.py:140 ] [ INFO] 获取设备屏幕大小完成。宽:(1080), 高(2280)
2024-04-20 14:22:53 [base_page.py:150 ] [ INFO] (试卷)页面，开始进行左滑
2024-04-20 14:22:54 [base_page.py:152 ] [ INFO] (试卷)页面，开始左滑完成。
2024-04-20 14:22:55 [base_page.py:42  ] [ INFO] (试卷)页面，开始查找一组元素(('class name', 'android.widget.TextView'))
2024-04-20 14:22:57 [base_page.py:46  ] [ INFO] (试卷)页面，查找元素(('class name', 'android.widget.TextView'))成功！
2024-04-20 14:23:03 [base_page.py:136 ] [ INFO] 开始获取设备屏幕大小。
2024-04-20 14:23:03 [base_page.py:140 ] [ INFO] 获取设备屏幕大小完成。宽:(1080), 高(2280)
2024-04-20 14:23:03 [base_page.py:150 ] [ INFO] (书城)页面，开始进行左滑
2024-04-20 14:23:04 [base_page.py:152 ] [ INFO] (书城)页面，开始左滑完成。
2024-04-20 14:23:04 [base_page.py:42  ] [ INFO] (书城)页面，开始查找一组元素(('class name', 'android.widget.TextView'))
2024-04-20 14:23:06 [base_page.py:46  ] [ INFO] (书城)页面，查找元素(('class name', 'android.widget.TextView'))成功！
2024-04-20 14:23:08 [base_page.py:136 ] [ INFO] 开始获取设备屏幕大小。
2024-04-20 14:23:08 [base_page.py:140 ] [ INFO] 获取设备屏幕大小完成。宽:(1080), 高(2280)
2024-04-20 14:23:08 [base_page.py:150 ] [ INFO] (高考)页面，开始进行左滑
2024-04-20 14:23:09 [base_page.py:152 ] [ INFO] (高考)页面，开始左滑完成。
2024-04-20 14:23:10 [base_page.py:42  ] [ INFO] (高考)页面，开始查找一组元素(('class name', 'android.widget.TextView'))
2024-04-20 14:23:12 [base_page.py:46  ] [ INFO] (高考)页面，查找元素(('class name', 'android.widget.TextView'))成功！
2024-04-20 14:23:14 [conftest.py:20  ] [ INFO] ----------------------------------- End ------------------------------------------

2024-04-20 14:23:14 [conftest.py:17  ] [ INFO] ----------------------------------- Begin ----------------------------------------
2024-04-20 14:23:14 [conftest.py:18  ] [ INFO] Current test case name : (test_switch_to_recommend)
2024-04-20 14:23:14 [base_page.py:26  ] [ INFO] (推荐)页面，开始查找元素(('id', 'com.xkw.client:id/recommend_text'))
2024-04-20 14:23:14 [base_page.py:30  ] [ INFO] (推荐)页面，查找元素(('id', 'com.xkw.client:id/recommend_text'))成功！
2024-04-20 14:23:14 [base_page.py:66  ] [ INFO] (推荐)页面，点击元素(('id', 'com.xkw.client:id/recommend_text'))
2024-04-20 14:23:14 [base_page.py:68  ] [ INFO] (推荐)页面，点击元素(('id', 'com.xkw.client:id/recommend_text'))成功！
2024-04-20 14:23:14 [base_page.py:42  ] [ INFO] (今日)页面，开始查找一组元素(('class name', 'android.widget.TextView'))
2024-04-20 14:23:15 [base_page.py:46  ] [ INFO] (今日)页面，查找元素(('class name', 'android.widget.TextView'))成功！
2024-04-20 14:23:17 [conftest.py:20  ] [ INFO] ----------------------------------- End ------------------------------------------

2024-04-20 14:23:17 [conftest.py:17  ] [ INFO] ----------------------------------- Begin ----------------------------------------
2024-04-20 14:23:17 [conftest.py:18  ] [ INFO] Current test case name : (test_switch_to_category)
2024-04-20 14:23:17 [base_page.py:26  ] [ INFO] (分类)页面，开始查找元素(('id', 'com.xkw.client:id/category_text'))
2024-04-20 14:23:17 [base_page.py:30  ] [ INFO] (分类)页面，查找元素(('id', 'com.xkw.client:id/category_text'))成功！
2024-04-20 14:23:17 [base_page.py:66  ] [ INFO] (分类)页面，点击元素(('id', 'com.xkw.client:id/category_text'))
2024-04-20 14:23:17 [base_page.py:68  ] [ INFO] (分类)页面，点击元素(('id', 'com.xkw.client:id/category_text'))成功！
2024-04-20 14:23:17 [base_page.py:136 ] [ INFO] 开始获取设备屏幕大小。
2024-04-20 14:23:17 [base_page.py:140 ] [ INFO] 获取设备屏幕大小完成。宽:(1080), 高(2280)
2024-04-20 14:23:17 [base_page.py:150 ] [ INFO] (小学)页面，开始进行左滑
2024-04-20 14:23:19 [base_page.py:152 ] [ INFO] (小学)页面，开始左滑完成。
2024-04-20 14:23:19 [base_page.py:136 ] [ INFO] 开始获取设备屏幕大小。
2024-04-20 14:23:19 [base_page.py:140 ] [ INFO] 获取设备屏幕大小完成。宽:(1080), 高(2280)
2024-04-20 14:23:19 [base_page.py:150 ] [ INFO] (初中)页面，开始进行左滑
2024-04-20 14:23:21 [base_page.py:152 ] [ INFO] (初中)页面，开始左滑完成。
2024-04-20 14:23:21 [base_page.py:136 ] [ INFO] 开始获取设备屏幕大小。
2024-04-20 14:23:21 [base_page.py:140 ] [ INFO] 获取设备屏幕大小完成。宽:(1080), 高(2280)
2024-04-20 14:23:21 [base_page.py:150 ] [ INFO] (高中)页面，开始进行左滑
2024-04-20 14:23:23 [base_page.py:152 ] [ INFO] (高中)页面，开始左滑完成。
2024-04-20 14:23:23 [base_page.py:136 ] [ INFO] 开始获取设备屏幕大小。
2024-04-20 14:23:23 [base_page.py:140 ] [ INFO] 获取设备屏幕大小完成。宽:(1080), 高(2280)
2024-04-20 14:23:23 [base_page.py:150 ] [ INFO] (中职)页面，开始进行左滑
2024-04-20 14:23:24 [base_page.py:152 ] [ INFO] (中职)页面，开始左滑完成。
2024-04-20 14:23:25 [base_page.py:109 ] [ INFO] (课程同步资源)页面，开始查找元素(('id', 'com.xkw.client:id/category_entrance_left'))
2024-04-20 14:23:25 [base_page.py:111 ] [ INFO] (课程同步资源)页面，查找元素(('id', 'com.xkw.client:id/category_entrance_left'))成功！
2024-04-20 14:23:25 [base_page.py:109 ] [ INFO] (知识点资源)页面，开始查找元素(('id', 'com.xkw.client:id/category_entrance_right'))
2024-04-20 14:23:25 [base_page.py:111 ] [ INFO] (知识点资源)页面，查找元素(('id', 'com.xkw.client:id/category_entrance_right'))成功！
2024-04-20 14:23:25 [conftest.py:20  ] [ INFO] ----------------------------------- End ------------------------------------------

2024-04-20 14:23:25 [conftest.py:10  ] [ INFO] ------------------------------------- End to run test case -----------------------------------
2024-04-20 14:23:25 [conftest.py:39  ] [ INFO] Quitting the Appium driver
```

# 结语

此框架未来改进点：

* 微调一下，兼容iOS设备
* 可与Jenkins结合，使用pipeline实现CI/CD

这只是框架的雏形，尚需填充业务逻辑和测试用例，需要时间逐步丰富此框框。

# 附录

附带一下我做的其他项目的CI/CD效果图：

<img class="shadow" src="/img/in-post/pipeline_Process_rendering.png" width="1200">

<img class="shadow" src="/img/in-post/jenkins_build_success.png" width="1200" />

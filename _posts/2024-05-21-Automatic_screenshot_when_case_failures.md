---
title: Web用例执行失败自动截图
date: 2024-05-21 23:19:00
author: Gavin Wang
img: "/img/pytest/pytest-4.png"
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: Web用例执行失败自动截图
categories:
    - [python]
    - [pytest]
    - [Automation]
tags:
    - pytest
    - python
    - Automation
---

# 概述

之前写过一篇文章，基于pytest+selenium4.0+allure完成了Web界面自动化测试框架设计工作，代码里面有介绍到截图功能，实现任意一步失败即可截图功能，独立封装了函数`set_img_error`实现：

```python
    def set_img_error(self):
        """用例执行失败截图,并且加入allure测试报告中"""
        # 获取图片存储的文件夹
        time_stamp_tag = get_time_stamp()
        img_path = self.img_path + f"/{time_stamp_tag}.png"
        try:
            self.driver.save_screenshot(filename=img_path)
            logging.error(f"截图成功,文件名称：{time_stamp_tag}.png")
            __file = open(img_path, "rb").read()
            allure.attach(__file, "用例执行失败截图", allure.attachment_type.PNG)
        except Exception as err:
            logging.error(f"执行失败截图未能正确添加进入测试报告:{err}")
            raise err
```

在如下私有函数中调用完成截图功能：

```shell
__wait_element_visible
__wait_element_clickable
__wait_element_exit
```

详细信息，请参考[链接](https://gavin-wang-note.github.io/2024/05/06/web_automation/)。

上述的实现，从我个人角度而言，不算拉胯，能够截取到任意一步出现的地方，截图比较及时。

今天介绍另外一种方法，借助`pytest hook`函数实现，但是，它有一些先天性的缺陷，截图可能有些滞后（I mean：当测试用例执行失败之后再截图，有可能页面已经发生了变化，未必是在第一时间截图，现场可能错失。这就是我想推荐[链接](https://gavin-wang-note.github.io/2024/05/06/web_automation/)它的原因），本文的实现方式，仅供参考。

# 代码展示

## conftest.py内容

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import pytest
import allure

import xlrd

from selenium import webdriver


# 用例失败后自动截图
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    获取用例执行结果的钩子函数
    :param item:
    :param call:
    :return:
    """
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            if "tmpir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
                f.write(report.nodeid + extra + "\n")
            with allure.step('添加失败截图...'):
                allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)


@pytest.fixture(scope='session', autouse=True)
def browser():
    global driver
    driver = webdriver.Chrome()
    return driver
```

## test_case.py内容

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import allure

from selenium.webdriver.common.by import By

LOGIN_PAGE = (By.CSS_SELECTOR, ".account-tab-account")
ACCOUNT_NAME = (By.ID, "username")
PASSWORD = (By.ID, "password")
LOGIN_BUTTON = (By.LINK_TEXT, "登录豆瓣")
URL = "https://accounts.douban.com/passport/login"


def test_login(browser):
    with allure.step("step1：打开登录首页"):
        browser.get(URL)
#    with allure.step("step2：切换到‘密码登录’页面"):
#        browser.find_element(*LOGIN_PAGE).click()
#    with allure.step("step3：输入账号"):
#        browser.find_element(*ACCOUNT_NAME).send_keys("abc@126.com")
#    with allure.step("step4：输入密码"):
#        browser.find_element(*PASSWORD).send_keys("123445")
#    with allure.step("step5：输入密码"):
#        browser.find_element(*LOGIN_BUTTON).click()
    assert False
```

这里故意模拟`assert`失败，让测试用例执行失败，从而验证截图功能能否正常工作。

## run.py

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import pytest


if __name__ == "__main__":
    pytest.main(['--alluredir', './report/json'])
    os.system('cd report')
    os.system('allure generate report/json -o report/html --clean')
```

**说明:**

* 示例代码，是粗糙了点儿（重要的是思路）。

# 运行效果

```shell
================================================= test session starts =================================================
platform win32 -- Python 3.11.4, pytest-8.0.2, pluggy-1.5.0
rootdir: C:\Users\Wang\Desktop\douban
plugins: allure-pytest-2.13.2, Faker-24.0.0, assume-2.4.3, base-url-2.1.0, html-4.1.1, metadata-3.1.1, order-1.1.0, progress-1.2.5, repeat-0.9.1, timeout-2.1.0, variables-3.1.0
collected 1 item

test_case.py
DevTools listening on ws://127.0.0.1:3861/devtools/browser/4d234e8a-fd95-4bd7-8514-fef965af1076
F                                                                                                   [100%]

====================================================== FAILURES =======================================================
_____________________________________________________ test_login ______________________________________________________

browser = <selenium.webdriver.chrome.webdriver.WebDriver (session="691d3b2a85e96cd39faac54af711a982")>

    def test_login(browser):
        with allure.step("step1：打开登录首页"):
            browser.get(URL)
    #    with allure.step("step2：切换到‘密码登录’页面"):
    #        browser.find_element(*LOGIN_PAGE).click()
    #    with allure.step("step3：输入账号"):
    #        browser.find_element(*ACCOUNT_NAME).send_keys("abc@126.com")
    #    with allure.step("step4：输入密码"):
    #        browser.find_element(*PASSWORD).send_keys("123445")
    #    with allure.step("step5：输入密码"):
    #        browser.find_element(*LOGIN_BUTTON).click()
>       assert False
E       assert False

test_case.py:26: AssertionError
=============================================== short test summary info ===============================================
FAILED test_case.py::test_login - assert False
================================================== 1 failed in 2.08s ==================================================
Report successfully generated to report\html
```

Allure报告展示效果：

<img class="shadow" src="/img/in-post/selenium/allure_screen_picture.png" width="800">

# 结语

再次提醒一下，此[链接](https://gavin-wang-note.github.io/2024/05/06/web_automation/)里的实现方法更好一下，胜在截图及时。

当然， Appium测试APP GUI、H5也是适用的，毕竟它们都遵循W3C WebDriver协议。

至于使用哪种方式，根据项目需要。

---
title: "基于Playwright完成页面基本操作的封装"
date: 2026-05-06
author: Gavin Wang
img: "/img/playwright/playwright-2.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: "基于Playwright完成页面基本操作的封装，实现诸如点击（单击、双击）、文本输入、内容清理、页面加载/刷新等动作"
categories:
    - [playwright]
    - [Automation]
tags:
    - playwright
    - Automation
---

# Overview

本文介绍基于`playwright`实现对页面的基本操作的封装，基于PO设计模式完成，FYI~


# code

不费言，直接上代码：

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""页面基本操作封装"""

import os
import time
import allure
import random
import logging
import platform
import asyncio

from playwright.async_api import async_playwright

from utils.common import get_time_stamp
from utils.path_util import get_report_path


class BasePage:
    """页面基本操作封装"""
    # 图片文件夹路径
    report_path = get_report_path()
    img_path = report_path + os.sep + "screenshots"
    # 如果目录不存在，创建它
    if not os.path.exists(report_path):
        os.mkdir(report_path, 0o777)
        os.mkdir(img_path, 0o777)
    if not os.path.exists(img_path):
        os.mkdir(img_path, 0o777)

    # Support Linux and Windows OS
    os_platform = platform.platform()

    @classmethod
    async def init_browser(cls, browser='chromium'):
        """init different browser"""
        async with async_playwright() as p:
            if browser.lower() == 'chromium':
                cls.browser = await p.chromium.launch()
            elif browser.lower() == 'firefox':
                cls.browser = await p.firefox.launch()
            elif browser.lower() == 'webkit':
                cls.browser = await p.webkit.launch()
            else:
                raise ValueError(f"Unsupported browser: {browser}")

            cls.page = await cls.browser.new_page()
            await cls.page.set_viewport_size({"width": 1920, "height": 1080})
            await cls.page.wait_for_timeout(10000)
            return cls.page

    @classmethod
    async def close_browser(cls):
        """Close browser which in opened status"""
        await cls.browser.close()

    async def get_url(self, url):
        """访问指定URL"""
        await self.page.goto(url)

    async def get_current_url_path(self):
        """获取当前页面的URL"""
        return self.page.url

    async def set_img_error(self):
        """用例执行失败截图, 并且加入allure测试报告中"""
        time_stamp_tag = get_time_stamp()
        img_path = f"{self.img_path}/{time_stamp_tag}.png"
        try:
            await self.page.screenshot(path=img_path)
            logging.error("截图成功, 文件名称：%s", {time_stamp_tag}+".png")
            with open(img_path, "rb") as file:
                allure.attach(file.read(), "用例执行失败截图", allure.attachment_type.PNG)
        except Exception as err:
            logging.error("执行失败截图未能正确添加进入测试报告: %s", err)
            raise err

    async def set_img_case(self):
        """用例执行完毕截图，并且将截图加入allure测试报告中"""
        with allure.step("关键步骤截图"):
            img_name = get_time_stamp()
            img_path = f"{self.img_path}/{img_name}.png"
            try:
                await self.page.screenshot(path=img_path)
                logging.debug("用例执行完成, 截图成功, 文件名称: %s", {img_name}+".png")
                with open(img_path, "rb") as file:
                    allure.attach(file.read(), "关键步骤截图", allure.attachment_type.PNG)
            except Exception as err:
                logging.error("测试结果截图, 未能正确添加进入测试报告: %s", err)
                raise err

    async def element_dyeing(self, element):
        """将被操作的元素染色"""
        try:
            await self.page.evaluate("element => element.style.background = 'yellow'; element.style.border = '2px solid red';", element)
        except Exception as err:
            logging.info("无法染色染色失效: %s", err)

    async def wait_for_element(self, selector, timeout=10000):
        """等待元素可见"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
        except TimeoutError as err:
            logging.error("等待元素(%s)超时", selector)
            await self.set_img_error()
            raise err

    async def find_element(self, selector):
        """找到单个元素"""
        await self.wait_for_element(selector)
        try:
            element = await self.page.query_selector(selector)
            await self.element_dyeing(element)
            return element
        except Exception as err:
            logging.error("定位元素(%s)失败", selector)
            await self.set_img_error()
            raise err

    async def find_elements(self, selector):
        """找到多个元素"""
        await self.wait_for_element(selector)
        try:
            elements = await self.page.query_selector_all(selector)
            return elements
        except Exception as err:
            logging.error("定位元素(%s)失败", selector)
            await self.set_img_error()
            raise err

    async def click_element(self, selector):
        """点击元素"""
        element = await self.find_element(selector)
        try:
            await element.click()
        except Exception as err:
            logging.error("点击元素(%s)失败", selector)
            await self.set_img_error()
            raise err

    async def input_text(self, selector, content):
        """输入文本内容"""
        element = await self.find_element(selector)
        try:
            await element.fill(content)
        except Exception as err:
            logging.error("输入文本到元素(%s)失败", selector)
            await self.set_img_error()
            raise err

    async def clear_contents(self, selector):
        """清除文本内容"""
        element = await self.find_element(selector)
        try:
            await element.fill("")
        except Exception as err:
            logging.error("清除元素(%s)内容失败", selector)
            await self.set_img_error()
            raise err

    async def get_element_text(self, selector):
        """获取元素的文本内容"""
        element = await self.find_element(selector)
        try:
            return await element.inner_text()
        except Exception as err:
            logging.error("获取元素(%s)文本内容失败", selector)
            await self.set_img_error()
            raise err

    async def select_contents_menu(self, selector, text):
        """选择下拉菜单中的内容"""
        element = await self.find_element(selector)
        try:
            options = await element.query_selector_all("option")
            for option in options:
                option_text = await option.inner_text()
                if option_text == text:
                    await option.click()
                    break
            else:
                logging.error("选项: (%s)不在下拉列表之中，请检查", text)
        except Exception as err:
            logging.error("选择下拉菜单内容失败: %s", err)
            await self.set_img_error()
            raise err

    async def dispose_alert(self, action="accept"):
        """处理页面alert"""
        try:
            dialog = self.page.on('dialog', lambda dialog: dialog.accept() if action == 'accept' else dialog.dismiss())
            return dialog.message
        except Exception as err:
            logging.error('alert处理异常')
            raise err

    async def refresh_page(self):
        """刷新当前页面"""
        logging.info("刷新页面: (%s)", await self.get_current_url_path())
        await self.page.reload()
```


说明：

如何使用同步模式，去掉上述代码中的`async`和`await`。

---
layout:     post
title:      "借助pytest fixture优化测试用例"
subtitle:   "pytest test case optimization by fixture"
date:       2023-09-10
author:     "Gavin Wang"
catalog:    true
img: "/img/pytest/pytest-7.png"
categories:
    - [Automation]
    - [pytest]
tags:
    - Automation
    - pytest
---



# 概述



近期碰到一个问题，信息如下:



```python
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "www.google.com"

def test_click_1():
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.find_element(
        By.XPATH,
        "div[contains(@class, 'item1')]"
    ).click()
    driver.close()


def test_click_2():
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.find_element(
        By.XPATH,
        "div[contains(@class, 'item2')]"
    ).click()
    driver.close()


def test_click_3():
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.find_element(
        By.XPATH,
        "div[contains(@class, 'item3')]"
    ).click()
    driver.close()
```



问：上述测试用例，如何优化？





# 分析


从示例用例来看，每个test_case中，都有driver的初始化和URL的get动作，以及close()动作；另外就是find_elements要做的事情，除了传递的XPATH元素不一样外，其他动作都一样，所以优化的点有：

* 封装driver初始化与URL的get动作
* 封装close动作
* 优化find_elements，借助pytest.mark.parametrize实现参数化


# 优化结果


```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "www.google.com"


@pytest.fixture()
def fixture_driver():
    driver = webdriver.Chrome()
    driver.get(URL)
    yield driver
    driver.close()


@pytest.mark.parametrize('item', ['item'+str(x) for x in range(1,4)])
def test_case(fixture_driver, item):
    driver.find_elements(By.XPATH, item).click()
```





经过优化后，测试用例更简洁、更契合pytest要求。





# 结语



这里的优化使用pytest的fixture特性，以及借助parametrize实现参数化。

对于pytest的fixture与pytest.mark.parametrize，近期会抽空整理一份示例并做说明。



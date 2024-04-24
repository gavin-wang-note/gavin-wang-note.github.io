---
title: pytest+Selenium+Allure Web自动化测试框架设计
date: 2024-05-06 22:50:37
author: Gavin Wang
# img: "/img/in-post/selenium/Selenium-Xpath-In-Details.png"
img: "/img/in-post/selenium/selenium1.jpg"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: Selenium Web自动化测试框架设计
categories:
    - [pytest]
    - [Automation]
    - [Selenium]
tags:
    - pytest
    - Automation
    - Selenium
---


# 概述

五一闲来无事，趁着假期几天，构建了一个Web自动化测试框架基础版，有个架子，也方便未来不时之需。

此次构建基于pytest+selenium4.0+allure，借助pytest的强大能力，基于PO设计模式完成Web测试框架基础搭建工作。


# 框架结构

```shell
root@Gavin:~/OrangeHRM_Web_Test_Framework# tree 
.
├── clear_pyc.py
├── config
│   ├── config.ini
│   ├── config.py
│   └── __init__.py
├── conftest.py
├── __init__.py
├── pages
│   ├── base_page.py
│   ├── dashboard_page.py
│   ├── employee_page.py
│   ├── __init__.py
│   └── login_page.py
├── pytest.ini
├── README.md
├── reports
├── requirements.txt
├── run_tests.py
├── tests
│   ├── 01_login
│   │   ├── __init__.py
│   │   └── test_login.py
│   ├── 02_employee
│   │   ├── __init__.py
│   │   └── test_employee.py
│   ├── conftest.py
│   └── __init__.py
└── utils
    ├── common.py
    ├── __init__.py
    └── path_util.py

8 directories, 24 files
root@Gavin:~/OrangeHRM_Web_Test_Framework# 
```


# Code介绍

## utils/path_util.py

```python
import os

__all__ = ["get_config_path"]


def get_config_path():
    """
    获取config文件的路径.
    先获得当前的文件的路径，由于config和common同一级，把common替换为config即可.
    """
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + os.sep + "config" + os.sep


def get_report_path():
    """获取测试报告的路径,reports的路径应该在当前目录下"""
    report_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + os.sep + "reports" + os.sep

    return report_path
```


## utils/common.py

这个文件目前要提供的功能是：提供时间戳，方便在封装页面操作时记录诸如元素从不可见到可见、从不可用到可用的时间间隔差。如果未来还有其他通用功能需要增加的，可根据项目实际需求进行添加。

```python
#  -*- coding:UTF-8 -*-

import random
import logging
import datetime
from faker import Faker

fake = Faker()

def get_date_time(**kwargs):
    """返回格式化为年月日小时分秒的日期时间字符串"""
    date_time = (datetime.datetime.now() + datetime.timedelta(**kwargs)).strftime('%Y-%m-%d %H:%M:%S')
    logging.debug("Current date time is : (%s)", date_time)
    return date_time

def get_time_stamp(**kwargs):
    """返回当前的Unix时间戳"""
    return datetime.datetime.now().timestamp()

def remove_duplicates_and_empty(lst):
    """列表去重和删除空元素"""
    seen = set()
    result = []
    for item in lst:
        if item not in seen and item:
            seen.add(item)
            result.append(item)
    return result

def generate_full_name():
    """随机生成英文全名、firstname、lastname"""
    first_name = fake.first_name()
    last_name = fake.last_name()
    full_name =  first_name + ' ' + last_name
    return full_name, first_name, last_name

def generate_gender():
    """随机生成性别"""
    return fake.random_element(elements=('Male', 'Female', 'Non-binary'))

def generate_landline_phone():
    """  随机生成座机（固定电话）号码。"""
    area_codes = ['010', '021', '022', '023', '024', '025']
    area_code = random.choice(area_codes)
    number = ''.join(random.choices('0123456789', k=7))  # 随机生成7位数字
    return f"{area_code}-{number}"

def generate_mobile_phone():
    """随机生成11位移动电话号码"""
    # 常见的手机前缀，这里只列举了一部分，可根据需要添加更多
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                '150', '151', '152', '153', '155', '156', '157', '158', '159',
                '176', '177', '178', '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
    prefix = random.choice(prefixes)
    suffix = ''.join(random.choices('0123456789', k=8))  # 随机生成8位数字
    return f"{prefix}{suffix}"

def generate_nationality():
    """随机生成国籍"""
    return fake.country()

def generate_address():
    """随机生成家庭住址"""
    return fake.address()

def generate_marital_status():
    """随机生成婚姻状况"""
    return fake.random_element(elements=('Married', 'Single', 'Divorced', 'Widowed'))

def generate_birth_date():
    """随机生成出生年月"""
    return fake.date_of_birth(minimum_age=21, maximum_age=61).isoformat()

def generate_age(min_age=18, max_age=60):
    """生成随机年龄，默认范围18至60岁"""
    return random.randint(min_age, max_age)

def generate_postal_code():
    """随机生成邮编号码"""
    return fake.postcode()

def generate_relation():
    """随机生成人员关系"""
    return fake.random_element(elements=('Spouse', 'Parent', 'Sibling', 'Relative', 'Guardian'))

if __name__ == "__main__":
    print("Full Name (Full, First, Last):", generate_full_name())
    print("Gender:", generate_gender())
    print("Random telephone number:", generate_landline_phone())
    print("Phone Number:", generate_mobile_phone())
    print("Nationality:", generate_nationality())
    print("Address:", generate_address())
    print("Marital Status:", generate_marital_status())
    print("Birth Date:", generate_birth_date())
    print("Postal Code:", generate_postal_code())
    print("Relation:", generate_relation())
```

## config/config.ini

```shell
config/config.ini
[orangehrm]
url = http://192.168.23.130/orangehrm-5.6/web/index.php/auth/login
username = admin
password = Huawei123!

[employee]
add_employee_url = http://192.168.23.130/orangehrm-5.6/web/index.php/pim/addEmployee
list_employee_url = http://192.168.23.130/orangehrm-5.6/web/index.php/pim/viewEmployeeList
```


## config/config.py

```python
from configobj import ConfigObj
from utils.path_util import get_config_path


class GetConfig(object):
    """从config.ini文件中获取配置信息"""
    config = ConfigObj(get_config_path() + "config.ini")

    # 获取登录相关配置信息
    login_url = config['orangehrm']['url']
    username = config['orangehrm']['username']
    password = config['orangehrm']['password']

    # 添加员工配置信息
    add_employee_url = config['employee']['add_employee_url']

    # 搜索添加的员工
    list_employee_url = config['employee']['list_employee_url']
```


## pages/base_page.py

Page Object设计模式是一种用于测试自动化的最佳实践，它将每个网页看作一个对象，网页上的元素和操作被封装成统一的接口。这样做的好处是提高了测试代码的可维护性和可读性，同时也方便了测试数据的管理和测试脚本的复用。

在Selenium中使用Page Object设计模式，通常遵循以下步骤：

* 创建Page Object类：为每个页面创建一个类，类中的属性代表页面上的元素，方法代表在页面上可以执行的操作。
* 定义元素定位器：在类中定义元素的定位器（如id、name、css selector等），通常使用By类或直接的定位器字符串。
* 封装元素操作：为页面上的元素创建方法，封装对这些元素的操作（如点击、输入文本等）。
* 封装页面操作：创建方法来封装一系列的用户操作，这些操作通常与页面的业务逻辑相关。
* 实例化Page Object：在测试脚本中实例化页面对象，并使用封装好的方法进行测试。

为了实现所有的测试用例都是在登录成功后执行，以及考虑到异常登录场景，同时还需确保整个用例执行过程无需切换多个浏览器，即在打开的同一个浏览器中完成异常登录、正常登录以及正常登录后的各种功能实现，需要对Selenium的WebDriver和登录OrangeHRM进行封装。同时，根据Page Object设计模式，还需对页面中各种操作，诸如输入框的输入、点击、元素是否可见、元素是否可用、失败截图、被操作元素的着色、查找单个元素、查找多个元素、刷新页面等等进行封装。

```python
# -*- coding:UTF-8 -*-

import os
import time
import allure
import random
import logging

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from utils.common import get_time_stamp
from utils.path_util import get_report_path


class BasePage:
    # 图片文件夹路径
    timeout = 10
    img_path = get_report_path() + os.sep + "screenshots"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(timeout)  # 设置隐式等待时间

    if not os.path.exists(img_path):
        os.mkdir(img_path, mode=0o777)

    def get_url(self, url):
        """
        访问指定URL
        :param url: 链接地址
        """
        self.driver.get(url=url)

    def get_current_url_path(self):
        """
        获取当前页面的URL
        :return: URL
        """
        current_url = self.driver.current_url
        return current_url

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

    def set_img_case(self):
        """用例执行完毕截图，并且将截图加入allure测试报告中"""
        with allure.step("关键步骤截图"):
            img_name = get_time_stamp()
            img_path = self.img_path + f"/{img_name}.png"
            try:
                # 截图前等待1秒防止图片没有正常加载
                time.sleep(1)
                self.driver.save_screenshot(filename=img_path)
                logging.debug(f"用例执行完成，截图成功，文件名称:{img_name}.png")
                # 读取图片信息
                __file = open(file=img_path, mode="rb").read()
                allure.attach(__file, "关键步骤截图", allure.attachment_type.PNG)
            except Exception as err:
                logging.error(f"测试结果截图，未能正确添加进入测试报告:{err}")
                raise err

    def element_dyeing(self, element):
        """将被操作的元素染色
        :rollback: 是否将元素回滚
        """
        try:
            self.driver.execute_script(
                "arguments[0].setAttribute('style', 'background: yellow; border: 2px solid red;');",
                element)
        except Exception as err:
            logging.info(f"无法染色染色失效：{err}")
            pass

    def __wait_element_visible(self, model, locator):
        """
        等待元素可见
        :param model: string, 元素所处的页面
        :param locator: tuple, 元素定位表达式
        """
        logging.debug(f"开始等待页面{model}的元素：{locator}可见")
        try:
            # 获取等待开始时间的时间戳
            start_time = get_time_stamp()
            WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(locator))
            # 计算元素等待的时间
            __wait_time =get_time_stamp() - start_time
            logging.debug(f"页面：{model}上的元素{locator}已可见，共计等待{__wait_time:0.2f}秒")
        except TimeoutException:
            logging.error(f"页面：{model},等待元素{locator}超时")
            self.set_img_error()
            raise TimeoutException(f"页面：{model},等待元素{locator}超时")
        except InvalidSelectorException as err:
            logging.error(f"页面:{model},元素不可见或定位表达式:{locator}异常\n {err}")
            raise InvalidSelectorException('元素定位异常')

    def __wait_element_clickable(self, model, locator):
        """
        等待元素点击
        :param model: string, 元素所处的页面
        :param locator: tuple, 元素定位表达式
        :return: 无返回值
        """
        logging.debug(f"等待页面{model}的元素：{locator}是否可点击")
        try:
            # 获取等待开始时间的时间戳
            start_time = get_time_stamp()
            WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(locator))
            # 计算元素等待的时间
            __wait_time =get_time_stamp() - start_time
            logging.debug(f"页面：{model}上的元素{locator}已可点击，共计等待{__wait_time:0.2f}秒")
        except TimeoutException as err:
            logging.error(f"页面：{model},等待元素{locator}超时")
            self.set_img_error()
            raise err
        except InvalidSelectorException as err:
            logging.error(f"页面:{model},元素不可点击或定位表达式:{locator}异常\n {err}")
            raise err

    def __wait_element_exit(self, model, locator):
        """
        等待元素存在
        :param model: string, 元素所处的页面
        :param locator: tuple, 元素定位表达式
        """
        logging.debug(f"-开始-等待页面{model}的元素：{locator}存在")
        try:
            # 获取等待开始时间的时间戳
            start_time =get_time_stamp()
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(locator))
            # 计算元素等待的时间
            __wait_time =get_time_stamp() - start_time
            logging.debug(f"页面：{model}上的元素{locator}已存在，共计等待{__wait_time:0.2f}秒")
        except TimeoutException as err:
            logging.error(f"页面：{model},等待元素{locator}超时")
            self.set_img_error()
            raise err
        except InvalidSelectorException as err:
            logging.error(f"页面:{model},元素不存在或定位表达式:{locator}异常\n {err}")
            raise err


    ####  由于代码内容较多，中间部分省略，请查看源码获取完整文件  ####

    def refresh_page(self):
        """
        刷新当前页面
        :return: None
        """
        logging.info(f"刷新页面: {self.get_current_url_path()}")
        self.driver.refresh()
```

## pytest.ini

pytest.ini是pytest的重要配置文件，名称和路径固定。此项目中我们希望借助pytest.ini文件完成日志的记录、日志级别的设定、默认参数和插件的使用。

```shell
[pytest]
log_cli = 1
log_cli_level = INFO
log_cli_format = %(lineno)-4d [%(levelname)-5s] %(asctime)s %(filename)s - %(message)s
log_file = reports/test.log
log_file_level = INFO
log_file_format = %(lineno)-4d [%(levelname)-5s] %(asctime)s %(filename)s - %(message)s
addopts = -vrsxX -p no:warnings --full-trace --alluredir=reports/json
norecursedirs = .git
console_output_style = count
```

## tests/conftest.py

```python
tests/conftest.py
import pytest

from pages.login_page import LoginPage
from config.config import GetConfig as config

@pytest.fixture(scope="session", autouse=True)
def login():
    login_page = LoginPage()
    login_page.login(config.username, config.password)
    yield login_page.driver
    login_page.driver.quit()
```


## 登录基类示例

```python
pages/login_page.py
# -*- coding:UTF-8 -*-
import logging

from pages.base_page import BasePage
from config.config import GetConfig as config

from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    URL = config.login_url
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CLASS_NAME, "orangehrm-login-action")
    INVALID_FAILED = (By.CLASS_NAME, "oxd-alert-content-text")
    LOGIN_SUCCESS = (By.CLASS_NAME, "oxd-main-menu-item--name")
    MUST_INPUT = (By.CLASS_NAME, "oxd-input-group__message")
    LOGOUT_DROPDOWN = (By.CLASS_NAME, "oxd-userdropdown-icon")
    LOGOUT = (By.CLASS_NAME, "oxd-userdropdown-link")

    def login(self, username=None, password=None, login_success=True):
        self.get_url(self.URL)
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        # Get element text info
        if login_success:
            logging.info("登录成功后页面元素校验")
            assert '管理员' in self.get_element_text(self.LOGIN_SUCCESS),\
                "[ERROR]  成功登录后，页面没有发现'管理员'字样"
        else:
            if len(username) and len(password):
                logging.info("因输入错误的用户名或密码导致登录失败后的页面元素校验")
                cre_flag = 'Invalid credentials' in self.get_element_text(self.INVALID_FAILED)
                assert cre_flag, \
                    "[ERROR] 输入错误的用户名或密码后，页面缺失'Invalid credentials'字样"
            else:
                logging.info("因输入空的用户名或密码导致登录失败后的页面元素校验")
                need_flag = '需要' in self.get_element_text(self.MUST_INPUT)
                assert need_flag, "[ERROR]  输入空的用户名或密码后，页面缺失'需要'字样"

    def logout(self):
        """
        登出页面，因为conftest.py中定义了一个登录fixture，所以测试登录相关用例的时候，要先登出，此时不quit
        """
        # 点击头像右侧箭头，弹出下拉列表
        self.click_element(self.LOGOUT_DROPDOWN)
        # Get all of elements
        elements = self.find_elements(self.LOGOUT)
        if elements:
            # 有4个元素，分别是关于、Support、更改密码和登出，登出是最后一个
            last_element = elements[-1]
            # self.click_element(last_element)
            last_element.click()
```

## pages/employee_page.py

同理，对于新增雇员及其添加后雇员信息的检查，业务逻辑和业务场景分隔开，即如下两个py文件：

```shell
├── pages
│   ├── employee_page.py
├── tests
│   ├── test_employee.py
```

```python
# -*- coding:UTF-8 -*-
import time
import allure
import logging

from pages.base_page import BasePage
from config.config import GetConfig as config
from utils.common import generate_full_name, remove_duplicates_and_empty

from selenium.webdriver.common.by import By

class EmployeePage(BasePage):
    ADD_EMPLOYEE_URL = config.add_employee_url
    LIST_EMPLOYEE_URL = config.list_employee_url
    FIRST_NAME = (By.NAME, "firstName")
    MIDDLE_NAME = (By.NAME, "middleName")
    LAST_NAME = (By.NAME, "lastName")
    SAVE_BUTTON = (By.CLASS_NAME, "orangehrm-left-space")
    SEARCH_EMPLOYEE = (By.CSS_SELECTOR, 'input[data-v-75e744cd]')
    SEARCH_BUTTOM = (By.CLASS_NAME, "orangehrm-left-space")
    SEARCH_RESULT = (By.CLASS_NAME, "oxd-padding-cell")
    full_name, first_name, last_name = generate_full_name()

    def add_employee(self, firstname=None, moddlename=None, lastname=None):
        firstname = self.first_name if firstname is None else firstname
        lastname = self.last_name if lastname is None else lastname
        logging.info(f"开始添加员工：firsname：（{firstname}）， lastname：（{lastname}）, " \
                      "full_name : ({self.full_name})")
        with allure.step("切换到‘添加员工’页面，并添加员工"):
            self.get_url(self.ADD_EMPLOYEE_URL)
            self.input_text(self.FIRST_NAME, firstname)
            # self.input_text(self.MIDDLE_NAME, moddlename)
            self.input_text(self.LAST_NAME, lastname)
            self.click_element(self.SAVE_BUTTON)
            time.sleep(1)
            logging.info(f"[Success]  完成员工{firstname} {lastname}的添加")

    def navigate_to_employees_list(self):
        with allure.step("跳转页面，跳转到员工列表页面"):
            self.driver.get(self.LIST_EMPLOYEE_URL)
            time.sleep(1)

    def search_new_employee(self, full_name):
        with allure.step("搜索新增加的员工信息"):
            self.input_text(self.SEARCH_EMPLOYEE, full_name)
            self.click_element(self.SEARCH_BUTTOM)
            time.sleep(1) # 等待搜索结果加载

    def verify_search_result(self, first_name, last_name):
        with allure.step("检查搜索结果是否正确"):
            elements = self.find_elements(self.SEARCH_RESULT)
            assert len(elements) > 0, "[ERROR]  没有查询到任何员工信息"
            # 查询到的elements中element.txt内容去重和删除空元素
            search_result = []
            for each_element in elements:
                search_result.append(each_element.text)
            end_result = remove_duplicates_and_empty(search_result)
            search_last_name = end_result[-1]
            search_first_name = end_result[-2]
            assert search_last_name == last_name, f"[ERROR]  没有过滤到{last_name}"
            assert search_first_name == first_name, f"[ERROR]  没有过滤到{first_name}"
            logging.info("[Success]  成功完成账号添加后的检查")
```

## 登录用例tests/test_login.py

test_login.py文件中登录逻辑是对pages/login_page.py中函数的调用，组织成产品登录场景相关测试用例.

```python
import pytest

from pages.login_page import LoginPage
from config.config import GetConfig as config


class TestLoginPage(LoginPage):
    # 因为conftest.py 定义的fixture已经被调用，成功登录了，所以先测试“登出”功能
    def test_logout(self):
        self.logout()

    @pytest.mark.parametrize("login_data", [
        # 正确的用户名和错误的密码
        (config.username, "wrong_password"),
        # 错误的用户名和正确的密码
        ("wrong_username", config.password),
        # 错误的用户名和错误的密码
        ("wrong_username", "wrong_password"),
        # 省略用户名
        ("", config.password),
        # 省略密码
        (config.username, ""),
    ])
    def test_failed_login(self, login_data):
        """Login OrangeHRM Web Failure with different credentials"""
        username, password = login_data
        self.login(username, password, login_success=False)

    @pytest.mark.login
    def test_successful_login(self):
        """Login OrangeHRM Web Success"""
        self.login(username=config.username, password=config.password)
```

## tests/test_employee.py

```python
from utils.common import generate_full_name
from pages.employee_page import EmployeePage


class TestAddEmployee(EmployeePage):
    full_name, first_name, last_name = generate_full_name()
    def test_add_an_employee(self):
        """Add an employee"""
        self.add_employee(firstname=self.first_name, lastname=self.last_name)
        self.navigate_to_employees_list()
        self.search_new_employee(self.full_name)
        self.verify_search_result(self.first_name, self.last_name)
```


# 测试用例执行

## 执行入口run_tests.py

```python
import pytest

if __name__ == '__main__':
    pytest.main()
```

## 执行过程与效果

运行成功后，在项目的reports目录下产生json目录和test.log文件，借助allure完成可视化测试报告的输出，如下图所示：
 
<img class="shadow" src="/img/in-post/allure/web_automation_report.png" width="1200">


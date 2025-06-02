---
title: 用例参数化传递不同平台的登录session
date: 2027-04-06 23:00:00
author: Gavin Wang
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 跨平台session传递到用例参数化中
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---



# 概述

## 现象

在编写自动化测试用例过程中，两个不同终端（运行平台和APP端）功能相同，即使用相同的接口，只是功能展示在Web端和APP端，不可能针对这两端写两份测试用例，如何让独一份测试用例在两端运行？

## 解决方案

借助`pytest`的参数化功能，传递两端所需的登录`session`，从而实现一份用例在两端运行的目的。

# 代码示例

## 不同终端独立的login/logout session

需要针对不同终端，实现各自终端的登录和登出，并返回相关登录成功后的`session`信息，代码参考如下：



### HttpSession.py

实现各平台的登录和登出，以及发起HTTP请求功能的封装，代码参考如下：

```python
import logging
import requests
import urllib.parse

from requests.packages.urllib3.exceptions import InsecureRequestWarning

from utils.config import CONFIG
from .error_codes import httpcode
from one.thing_api import ConfigurationPlatform, APP, OperatingPlatform, OneWindowOperatingPlatform

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class HttpSession:
    def __init__(self):
        # Not verify SSL certificate
        self.verify = False

        # timeout time
        self.timeout = (60, 600)

        # Default header
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'isToken': 'false',
            'connection': 'keep-alive'
        }

        # session information
        self.configuration_platform_session = requests.Session()
        self.operating_platform_session = requests.Session()
        self.ssb_app_session = requests.Session()
        self.ycb_platform_session = requests.Session()

        # Configuration platform login URL, user and password
        self.configuration_platform_base_url = CONFIG['configuration_platform_base_url']
        self.configuration_user = CONFIG['configuration_platform_admin_credentials']['username']
        self.configuration_password = CONFIG['configuration_platform_admin_credentials']['password']

        # Operating platform login URL, user and password
        self.operating_platform_base_url = CONFIG['operating_platform_base_url']
        self.operating_user = CONFIG['operating_platform_admin_credentials']['username']
        self.operating_password = CONFIG['operating_platform_admin_credentials']['password']

        # ssb APP login URL, user and password
        self.ssbapp_base_url = CONFIG['ssbapp_base_url']
        self.ssbapp_user = CONFIG['user_info']['username']
        self.ssbapp_password = CONFIG['user_info']['password']

        # ycb login URL, user and password
        self.ycb_platform_base_url = CONFIG['ycb_base_url']
        self.ycb_user = CONFIG['ycb_user_info']['username']
        self.ycb_password = CONFIG['ycb_user_info']['password']

        # operating login URL, user and password
        self.operating_platform_base_url = CONFIG['operating_platform_base_url']
        self.operating_user = CONFIG['operating_platform_admin_credentials']['username']
        self.operating_password = CONFIG['operating_platform_admin_credentials']['password']

    def configuration_platform_login(self):
        """配置平台登录"""
        login_url = self.configuration_platform_base_url + ConfigurationPlatform().login
        login_data = {
            "username": self.configuration_user,
            "password": self.configuration_password
        }
        self.configuration_platform_session.headers.update(self.header)
        logging.info("[Action] 开始登录配置平台，url: (%s), data: (%s)", login_url, login_data)
        login_res = self.configuration_platform_session.post(login_url, json=login_data)
        login_res_json = login_res.json()
        err_msg = f"[ERROR] 配置平台登录失败，后端接口返回：{login_res.json}"
        assert login_res.json()['msg'] == "操作成功", err_msg
        assert login_res.json()['code'] == httpcode.OK, err_msg
        assert login_res.status_code == httpcode.OK, err_msg
        logging.info("[Success] 登录配置平台成功")

        # Update HTTP header info
        token = login_res_json['token']
        self.configuration_platform_session.headers.update({'Authorization': f'Bearer {token}'})
        return self.configuration_platform_session

    def configuration_platform_logout(self):
        """登出配置平台"""
        logging.info("[Action] 登出配置平台")
        logout_url = self.configuration_platform_base_url + ConfigurationPlatform().logout
        logout_res = self.configuration_platform_session.delete(logout_url)
        err_msg = f"[ERROR] Logout Configuration Platform failed, backend return: {logout_res.json()}"
        assert logout_res.json()['code'] == httpcode.OK, err_msg
        logging.info("[Success] 成功登出配置平台")
    
    def ssbapp_login(self):
        """随时办APP登录"""
        login_url = self.ssbapp_base_url + APP().ssbLogin
        login_data = {
            "username": self.ssbapp_user,
            "password": self.ssbapp_password,
            "userType": "2",
            "platform": "A1"
        }
        self.ssb_app_session.headers.update(self.header)
        logging.info("[Action] 开始登录随时办APP，url: (%s), data: (%s)", login_url, login_data)
        login_res = self.ssb_app_session.post(login_url, json=login_data)
        login_res_json = login_res.json()
        err_msg = f"[ERROR] 随时办APP登录失败，后端接口返回：{login_res.json}"
        assert login_res.json()['msg'] == "操作成功", err_msg
        assert login_res.json()['code'] == httpcode.OK, err_msg
        assert login_res.status_code == httpcode.OK, err_msg
        logging.info("[Success] 登录随时办APP成功")

        # Update HTTP header info
        token = login_res_json['token']
        self.ssb_app_session.headers.update({'Authorization': f'Bearer {token}'})
        return self.ssb_app_session

    def ssbapp_logout(self):
        """登出随时办APP"""
        logging.info("[Action] 登出随时办APP")
        logout_url = self.ssbapp_base_url + APP().ssblogout
        logout_res = self.ssb_app_session.delete(logout_url)
        err_msg = f"[ERROR] Logout 随时办APP Platform failed, backend return: {logout_res.json()}"
        assert logout_res.json()['code'] == HttpStatusCode.OK, err_msg
        logging.info("[Success] 成功登出随时办APP")

    def ycb_platform_login(self):
        """登录一窗办平台"""
        logging.info("[Action] 开始登录一窗办平台，url: (%s), data: (%s)", login_url, login_data)
        login_res = self.ycb_platform_session.post(login_url, json=login_data)
        login_res_json = login_res.json()
        err_msg = f"[ERROR] 一窗办平台登录失败，后端接口返回：{login_res.json}"
        assert login_res.json()['msg'] == "操作成功", err_msg
        assert login_res.json()['code'] == HttpStatusCode.OK, err_msg
        assert login_res.status_code == HttpStatusCode.OK, err_msg
        logging.info("[Success] 登录一窗办平台成功")

        # Update HTTP header info
        token = login_res.json()['token']
        self.ycb_platform_session.headers.update({'Authorization': f'Bearer {token}'})
        logging.info("一窗办平台信息：%s", self.ycb_platform_session.headers)

        return self.ycb_platform_session

    def ycb_platform_logout(self):
        """登出一窗办平台"""
        logging.info("[Action] 登出一窗办平台")
        logout_url = self.ycb_platform_base_url + OneWindowOperatingPlatform().ycb_logout
        logout_res = self.ycb_platform_session.post(logout_url)
        err_msg = f"[ERROR] Logout ycb Platform failed, backend return: {logout_res.json()}"
        assert logout_res.json()['code'] == HttpStatusCode.OK, err_msg
        logging.info("[Success] 成功登出一窗办平台")

    def operating_platform_login(self):
        """登录平台"""
        login_url = self.operating_platform_base_url + OperatingPlatform().operating_login
        login_data = {
            "username": self.operating_user,
            "password": self.operating_password,
            "userType": "2",
            "platform": "A1"
        }
        self.operating_platform_session.headers.update(self.header)

        logging.info("[Action] 开始登录操作平台，url: (%s), data: (%s)", login_url, login_data)
        login_res = self.operating_platform_session.post(login_url, json=login_data)
        login_res_json = login_res.json()
        err_msg = f"[ERROR] 操作平台登录失败，后端接口返回：{login_res.json}"
        assert login_res.json()['msg'] == "操作成功", err_msg
        assert login_res.json()['code'] == httpcode.OK, err_msg
        assert login_res.status_code == httpcode.OK, err_msg
        logging.info("[Success] 登录操作平台成功")

        # Update HTTP header info
        token = login_res_json['token']
        self.operating_platform_session.headers.update({'Authorization': f'Bearer {token}'})
        return self.operating_platform_session

    def operating_platform_logout(self):
        """登出集成办平台"""
        logging.info("[Action] 登出集成办平台")
        logout_url = self.operating_platform_base_url + OperatingPlatform().operating_logout
        logout_res = self.operating_platform_session.post(logout_url)
        err_msg = f"[ERROR] Logout Operating Platform failed, backend return: {logout_res.json()}"
        assert logout_res.json()['code'] == HttpStatusCode.OK, err_msg
        logging.info("[Success] 成功登出集成办平台")

    def send_request(self, method, endpoint, platform_type='configuration', **kwargs):
        """
        发送HTTP请求消息功能的封装
        :param method: such as 'get', 'post', 'put', 'delete'
        :param endpoint: API URL
        :param platform_type: string, different platform
        True means the request is sends from Configuration Platform
        False means from Operating Platforms
        :param kwargs: other parameters, such as data, json, headers and so on.
        :return: response
        """
        request_func = url = ''
        try:
            # Constructing a request function based on a method
            if platform_type.lower() == 'configuration':
                request_func = getattr(self.configuration_platform_session, method.lower())
                url = f"{self.configuration_platform_base_url}{endpoint}"
            # Send request
            elif platform_type.lower() == 'operating':
                request_func = getattr(self.operating_platform_session, method.lower())
                url = f"{self.operating_platform_base_url}{endpoint}"
            elif platform_type.lower() == 'ssbapp':
                request_func = getattr(self.ssb_app_session, method.lower())
                url = f"{self.ssbapp_base_url}{endpoint}"
            elif platform_type.lower() == 'ycb':
                request_func = getattr(self.ycb_platform_session, method.lower())
                url = f"{self.ycb_platform_base_url}{endpoint}"
            else:
                pass

            logging.debug(f"-- Full URL: ({s}, decode url: (%s)", url, urllib.parse.unquote(url))

            auth_failed_flag = False
            try:
                res_code = response.json()['code']
                if res_code in [res_code, response.status_code]:
                    auth_failed_flag = True
            except # pylint: disable=W0702
                pass

            if auth_failed_flag:
                logging.warning("(WARNING) Session timeout, login again.")
                if platform_type.lower() == 'configuration':
                    self.configuration_platform_login()
                    request_func = getattr(self.configuration_platform_session, method.lower())
                elif platform_type.lower() == 'operating':
                    self.operating_platform_login()
                    request_func = getattr(self.operating_platform_session, method.lower())
                elif platform_type.lower() == 'ssbapp':
                    self.ssbapp_login()
                    request_func = getattr(self.ssb_app_session, method.lower())
                elif platform_type.lower() == 'ycb':
                    self.ycb_platform_login()
                    request_func = getattr(self.ycb_platform_session, method.lower())
                else:
                    pass

            response = request_func(url, **kwargs)

            response.raise_for_status()  # Check response status code

            return response
        except AttributeError:
            logging.error("Method: %s is not supported", method)
            return None
        except requests.HTTPError as err:
            logging.error("HTTP Error: %s", err)
            return None
        except requests.RequestException as err:
            logging.error("Request Error: %s", err)
            return None
```



## 全局登录fixture

### conftest.py

此文件放在用例目录所在的顶层目录，实现各个平台的自动登录操作，并返回平台类型`platform`,而`HTTPSession.py`代码中，需要传递`platform_type`，此参数取值使用这里返回的平台类型platform，从而实现区分各个平台的`session`切换，代码参考如下：

```python
"""初始化各项全局登录session"""
import logging
import pytest
from api.http_session import HttpSession
from testcasebase.api.config_platform.thing_config.topic_config import TopicConfig

@pytest.fixture(scope='session', autouse=True)
def configuration_platform_session():
    """配置平台的session"""
    session = HttpSession()
    try:
        session.configuration_platform_login()
        session.platform = "configuration"
        yield session
    finally:
        session.configuration_platform_logout()

@pytest.fixture(scope='session', autouse=True)
def ycb_platform_session():
    """一窗办的session"""
    session = HttpSession()
    try:
        session.ycb_platform_login()
        session.platform = "ycb"
        yield session
    finally:
        session.ycb_platform_logout()

@pytest.fixture(scope='session', autouse=True)
def operating_platform_session():
    """操作平台的session"""
    session = HttpSession()
    try:
        session.operating_platform_login()
        session.platform = "operating"
        yield session
    finally:
        session.operating_platform_logout()


@pytest.fixture(scope='session', autouse=True)
def ssb_app_session():
    """随时办APP session"""
    session = HttpSession()
    try:
        session.app_login()
        session.platform = "ssbapp"
        yield session
    finally:
        session.ssbapp_logout()
```



## 测试用例编写

如下测试用例，定义了一个`fixture platform_type`，使用`pytest`内置`fixture request`，返回参数化参数`params`中提供的`operating_platform_session, ssb_app_session`对应的`session`信息，此`session`信息中存在`session.platform`信息，从而能够获取到`session`是哪个端的，代码参考如下：

```python
class TestCommonAddress(CommonAddress, UserConfig):
    """
    常用地址管理
    """
    @pytest.fixture(params=['operating_platform_session', "ssb_app_session"], scope="class", autouse=True)
    def platform_type(self, request):
        """
        参数/session
        """
        return request.getfixturevalue(request.param)

    @allure.attributes(
        severity='critical',
        testcase=f'{zentao.baseUrl}/zentao/testcase-view-146.html、1109.html', '我的-常用地址-新增常用地址')
    @pytest.mark.parametrize("if_default_address", ['1', '2'])
    def test_save_common_address(self, platform_type, if_default_address):
        """我的-常用地址-新增常用地址"""
        user_info = UserConfig().query_user_info(platform_type)
        logging.info(f"\n获取fixture名称是：%s", platform_type)
        name, _, _ = generate_full_name()
        mobile = generate_mobile_phone()
        xzqh_dict = random.choice(self.query_org_list(platform_type))
        xzqh = xzqh_dict['value']
        xzqh_name = xzqh_dict['text']
        streets = ['中山路', '解放路', '人民路', '长安街', '上海路', '南京路', '广州路', '延安路']
        streets = random.choice(streets)
        house.number = random.randint(1, 999)
        address = f"{street}街道{house.number}号"
        postal_code = generate_postal_code()
        self.save_common_address(platform_type, name=name, mobile=mobile, xzqh_name=xzqh_name,
                                 address=address, postal_code=postal_code, if_default_address=if_default_address,
                                 userid=user_info['userid'])
        c9001 = self.query_common_address_list(platform_type, userid=user_info['userid'])
        if if_default_address:
            self.delete_common_address(platform_type, c9001=c9001, userid=user_info['userid'])

    @allure.attributes(
        severity='critical',
        testcase=f'{zentao.baseUrl}/zentao/testcase-view-246.html', '我的-常用地址-删除常用地址、地址重复(失败)')
```


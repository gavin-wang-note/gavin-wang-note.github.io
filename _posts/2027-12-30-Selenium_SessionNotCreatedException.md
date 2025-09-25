---
title: Selenium自动化启动浏览器报SessionNotCreatedException异常
date: 2027-10-03 23:00:00
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: selenium.common.exceptions.SessionNotCreatedException: Message: session not created
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 概述

`Linux`下使用`Firefox`执行`web`用例，期间出现了一些错误，记录下来。
在用例执行之前，安装了常见的浏览器，诸如`Chrome`和`Firefox`，以及相关`Driver`。

# 相关Driver的安装

## 安装geckodriver

访问`https://github.com/mozilla/geckodriver/releases`，下载合适版本，解压后将`geckodriver`文件移动到`/usr/local/bin/`目录下，并增加可执行权限：
`chmod +x /usr/local/bin/geckodriver`

查看安装的`geckodriver`版本：

```shell
[gavin@Gavin automation]$ geckodriver --version
geckodriver 0.36.0 (a3d508507022 2025-02-24 15:57 +0000)

The source code of this program is available from
testing/geckodriver in https://hg.mozilla.org/mozilla-central.

This program is subject to the terms of the Mozilla Public License 2.0.
You can obtain a copy of the license at https://mozilla.org/MPL/2.0/.
```


## 碰见的问题

### selenium.common.exceptions.SessionNotCreatedException: Message: session not created

#### 日志

日志显示：

```shell
selenium.common.exceptions.SessionNotCreatedException: Message: Failed to set preferences: unknown error; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
```

详细日志信息如下：

```shell
[gavin@Gavin automation]$ python run_tests.py --automation-type=web --browser=firefox
pytest args: ['--alluredir', '/home/gavin/tools/reports/json', '--clean-alluredir', '--automation-type=web', '--cov=.', '--cov-report=xml:/home/gavin/tools/reports/coverage.xml', 'testcase/web']
[INFO] 浏览器检测通过：firefox
================================================================================================ test session starts ================================================================================================
platform linux -- Python 3.9.21, pytest-8.4.1, pluggy-1.6.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: /home/gavin/tools/automation
configfile: pytest.ini
plugins: profiles-0.2.0, xdist-3.8.0, progress-1.3.0, cov-7.0.0, allure-pytest-2.13.5
collected 1 item                                                                                                                                                                                                    

testcase/web/test_web.py::test_web ERROR                                                                                                                                                                       [1/1]
____________________________________________________________________________________________ ERROR at setup of test_web _____________________________________________________________________________________________

browser = 'firefox'

    @pytest.fixture(scope="session", autouse=True)
    def driver_setup(browser):
        """浏览器初始化和清理"""
        from pages.base_page import BasePage
    
        try:
>           BasePage.init_driver(browser=browser)

testcase/web/conftest.py:22:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
pages/base_page.py:75: in init_driver
    cls.driver = webdriver.Firefox(options=options)
../../.local/lib/python3.9/site-packages/selenium/webdriver/firefox/webdriver.py:72: in __init__
    super().__init__(command_executor=executor, options=options)
../../.local/lib/python3.9/site-packages/selenium/webdriver/remote/webdriver.py:263: in __init__
    self.start_session(capabilities)
../../.local/lib/python3.9/site-packages/selenium/webdriver/remote/webdriver.py:366: in start_session
    response = self.execute(Command.NEW_SESSION, caps)["value"]
../../.local/lib/python3.9/site-packages/selenium/webdriver/remote/webdriver.py:458: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x7ff152bcff70>
response = {'status': 500, 'value': '{"value":{"error":"session not created","message":"Failed to set preferences: unknown error","stacktrace":""}}'}

    def check_response(self, response: dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                try:
                    value = json.loads(value_json)
                    if isinstance(value, dict):
                        if len(value) == 1:
                            value = value["value"]
                        status = value.get("error", None)
                        if not status:
                            status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                            message = value.get("value") or value.get("message")
                            if not isinstance(message, str):
                                value = message
                                message = message.get("message")
                        else:
                            message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.SessionNotCreatedException: Message: Failed to set preferences: unknown error; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception                                                                                                                                                                       

../../.local/lib/python3.9/site-packages/selenium/webdriver/remote/errorhandler.py:232: SessionNotCreatedException

During handling of the above exception, another exception occurred:

browser = 'firefox'

    @pytest.fixture(scope="session", autouse=True)
    def driver_setup(browser):
        """浏览器初始化和清理"""
        from pages.base_page import BasePage
    
        try:
            BasePage.init_driver(browser=browser)
            yield
        except Exception as err:
            print(f"浏览器初始化失败: {err}")
>           pytest.fail(f"浏览器初始化失败: {err}")
E           Failed: 浏览器初始化失败: Message: Failed to set preferences: unknown error; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception                                                                                                                                                                                                

testcase/web/conftest.py:26: Failed
----------------------------------------------------------------------------------------------- Captured stdout setup -----------------------------------------------------------------------------------------------
浏览器初始化失败: Message: Failed to set preferences: unknown error; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception

浏览器关闭过程中出现错误: type object 'BasePage' has no attribute 'driver'
------------------------------------------------------------------------------------------------ Captured log setup -------------------------------------------------------------------------------------------------
2025-09-18 09:19:11 [conftest.py:68  ] [ INFO] ------------------------------- Start to run test case ---------------------------------------------
2025-09-18 09:19:11 [selenium_manager.py:100 ] [DEBUG] Selenium Manager binary found at: /home/gavin/.local/lib/python3.9/site-packages/selenium/webdriver/common/linux/selenium-manager
2025-09-18 09:19:11 [selenium_manager.py:113 ] [DEBUG] Executing process: /home/gavin/.local/lib/python3.9/site-packages/selenium/webdriver/common/linux/selenium-manager --browser firefox --language-binding python --output json
2025-09-18 09:19:12 [selenium_manager.py:139 ] [DEBUG] Driver path: /home/gavin/.cache/selenium/geckodriver/linux64/0.36.0/geckodriver
2025-09-18 09:19:12 [selenium_manager.py:139 ] [DEBUG] Browser path: /usr/bin/firefox
2025-09-18 09:19:12 [service.py:226 ] [DEBUG] Started executable: `/home/gavin/.cache/selenium/geckodriver/linux64/0.36.0/geckodriver` in a child process with pid: 63869 using 0 to output -3
2025-09-18 09:19:12 [remote_connection.py:405 ] [DEBUG] POST http://localhost:53489/session {'capabilities': {'firstMatch': [{}], 'alwaysMatch': {'browserName': 'firefox', 'acceptInsecureCerts': True, 'moz:debuggerAddress': True, 'pageLoadStrategy': <PageLoadStrategy.normal: 'normal'>, 'browserVersion': None, 'moz:firefoxOptions': {'binary': '/usr/bin/firefox', 'prefs': {'remote.active-protocols': 1}, 'args': ['-profile', '/root/snap/firefox/common/.cache/mozilla/firefox/shfysd7o.default']}}}}
2025-09-18 09:19:12 [connectionpool.py:241 ] [DEBUG] Starting new HTTP connection (1): localhost:53489
2025-09-18 09:19:12 [connectionpool.py:544 ] [DEBUG] http://localhost:53489 "POST /session HTTP/1.1" 500 0
2025-09-18 09:19:12 [remote_connection.py:438 ] [DEBUG] Remote response: status=500 | data={"value":{"error":"session not created","message":"Failed to set preferences: unknown error","stacktrace":""}} | headers=HTTPHeaderDict({'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-cache', 'content-length': '110', 'date': 'Thu, 18 Sep 2025 01:19:12 GMT'})
2025-09-18 09:19:12 [remote_connection.py:467 ] [DEBUG] Finished Request
___________________________________________________________________ 1 of 1 completed, 0 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 1 Error, 0 ReRun ____________________________________________________________________
----------------------------------------------------------------------------------------------------
```


#### 原因分析

##### 可能出错的原因

如果是Chrome浏览器，导致`SessionNotCreatedException`报错的原因主要有以下几点：

- 浏览器版本不匹配：`ChromeDriver`版本与安装的`Chrome`浏览器版本不兼容。
- `ChromeDriver`路径错误：指定的`ChromeDriver`路径不正确或`ChromeDriver`文件不存在。
- 浏览器未正确安装：浏览器未正确安装或路径未正确配置。
- 权限问题：在某些操作系统上，权限不足可能导致无法启动浏览器会话。

但我现在是`Firefox`，且`Firefox`已经正确安装了，那还有其他可能：

- 浏览器版本过旧：更新浏览器到最新版本。有时，旧版本的浏览器可能不支持Selenium的某些功能。
- Selenium版本问题：确保安装的Selenium版本与浏览器驱动兼容。有时，更新Selenium到最新版本可能有助于解决问题。
- 环境变量问题：确保相关的环境变量（如WEBDRIVER_PATH）已正确设置，以便Selenium可以找到浏览器驱动。
- 防火墙或安全软件：某些防火墙或安全软件可能阻止Selenium启动浏览器。可以尝试临时禁用这些软件，然后再次运行脚本。
- 浏览器设置：某些浏览器设置可能阻止Selenium正常工作。例如，Chrome的“无痕模式”可能会导致问题。确保浏览器设置允许Selenium启动会话。
- Selenium服务器问题：如果正在使用Selenium Grid或远程WebDriver，请确保Selenium服务器正在运行，并且客户端和服务器之间的连接没有问题。

至于本次碰见的此问题原因，我们一点点分析。


##### 版本信息确认

```shell
[gavin@Gavin automation]$ firefox --version
Mozilla Firefox 128.14.0esr
[gavin@Gavin automation]$ pip show selenium
Name: selenium
Version: 4.35.0
Summary: Official Python bindings for Selenium WebDriver
Home-page: https://www.selenium.dev
Author:
Author-email:
License: Apache-2.0
Location: /home/gavin/.local/lib/python3.9/site-packages
Requires: certifi, trio, trio-websocket, typing_extensions, urllib3, websocket-client
Required-by:
[gavin@Gavin automation]$
```

经查询，`Selenium`版本是`4.35.0`，`Firefox`版本是`128.14.0esr`，手工调试一下启动`Firefox`:


```shell
>>> from selenium import webdriver
>>> from selenium.webdriver.firefox.service import Service
>>> options = Options()
>>> driver = webdriver.Firefox(options=options)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/gavin/.local/lib/python3.9/site-packages/selenium/webdriver/firefox/webdriver.py", line 72, in __init__
    super().__init__(command_executor=executor, options=options)
  File "/home/gavin/.local/lib/python3.9/site-packages/selenium/webdriver/remote/webdriver.py", line 263, in __init__
    self.start_session(capabilities)
  File "/home/gavin/.local/lib/python3.9/site-packages/selenium/webdriver/remote/webdriver.py", line 366, in start_session
    response = self.execute(Command.NEW_SESSION, caps)["value"]
  File "/home/gavin/.local/lib/python3.9/site-packages/selenium/webdriver/remote/webdriver.py", line 458, in execute
    self.error_handler.check_response(response)
  File "/home/gavin/.local/lib/python3.9/site-packages/selenium/webdriver/remote/errorhandler.py", line 232, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.WebDriverException: Message: Process unexpectedly closed with status 1

>>>
```

还是失败，增加日志，然后查看详细日志：

 **“让 geckodriver 自己说话”** 当成第一要务——**手动启动它**，看最原始的错误输出：

------------------------------------------------
1. 先手动启动 geckodriver（前台模式）  

```bash
/usr/local/bin/geckodriver --port 4444
```

- 如果 **立即报错** → 把终端里 **完整报错** 贴出来（大概率缺系统库）。  
- 如果 **一直卡着监听** `0.0.0.0:4444` → 说明驱动本身没问题，继续第 2 步。

------------------------------------------------
2. 让 Selenium 连接 **已启动的 geckodriver**（绕开 Selenium 的启动逻辑）  
```python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")          # 先无头，排除显示问题
driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
print("Firefox 启动成功，标题：", driver.title)
driver.quit()
```

- 若 **仍失败** → 手动启动的终端里会滚出 **真正导致崩溃的日志**  
- 若 **成功** → 问题出在 Selenium 自动拉起 geckodriver 的参数/环境

目前看到的错误信息是：

```shell
[gavin@Gavin log]$ /usr/local/bin/geckodriver --port 4444
1758160989973   geckodriver     INFO    Listening on 127.0.0.1:4444
1758161012617   mozrunner::runner       INFO    Running command: MOZ_CRASHREPORTER="1" MOZ_CRASHREPORTER_NO_REPORT="1" MOZ_CRASHREPORTER_SHUTDOWN="1" "/usr/bin/firefox" "--m ... tte" "--remote-debugging-port" "9222" "--remote-allow-hosts" "localhost" "-no-remote" "-profile" "/tmp/rust_mozprofileP2gX8u"
Error: no DISPLAY environment variable specified
```

没有设置回显，设置一下即可：

```shell
export DISPLAY=192.168.1.2：0.0
```
然后在控制台直接执行`Firefox`这个linux命令，看看`Firefox`能不能正常运行，如果还是无法启动`Firefox`，再次使用`geckodriver`记录日志的方式排查问题；如果Linux没有安装可视化桌面，就使用无头模式：

```shell
>>> from selenium import webdriver
>>> from selenium.webdriver.firefox.options import Options
>>>
>>> options = Options()
>>> options.add_argument("--headless")          # 先无头，排除显示问题
>>> driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
>>> print("Firefox 启动成功，标题：", driver.title)
Firefox 启动成功，标题：
>>> dir(driver)
['__abstractmethods__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_abc_impl', '_authenticator_id', '_bidi_session', '_browser', '_browsing_context', '_check_if_window_handle_is_current', '_devtools', '_emulation', '_fedcm', '_file_detector', '_get_cdp_details', '_input', '_is_remote', '_mobile', '_network', '_permissions', '_require_fedcm_support', '_script', '_session', '_shadowroot_cls', '_start_bidi', '_storage', '_switch_to', '_unwrap_value', '_web_element_cls', '_webextension', '_websocket_connection', '_wrap_value', 'add_cookie', 'add_credential', 'add_virtual_authenticator', 'back', 'bidi_connection', 'browser', 'browsing_context', 'capabilities', 'caps', 'close', 'command_executor', 'create_web_element', 'current_url', 'current_window_handle', 'delete_all_cookies', 'delete_cookie', 'delete_downloadable_files', 'dialog', 'download_file', 'emulation', 'error_handler', 'execute', 'execute_async_script', 'execute_cdp_cmd', 'execute_script', 'fedcm', 'fedcm_dialog', 'file_detector', 'file_detector_context', 'find_element', 'find_elements', 'forward', 'fullscreen_window', 'get', 'get_cookie', 'get_cookies', 'get_credentials', 'get_downloadable_files', 'get_pinned_scripts', 'get_screenshot_as_base64', 'get_screenshot_as_file', 'get_screenshot_as_png', 'get_window_position', 'get_window_rect', 'get_window_size', 'implicitly_wait', 'input', 'locator_converter', 'maximize_window', 'minimize_window', 'mobile', 'name', 'network', 'orientation', 'page_source', 'permissions', 'pin_script', 'pinned_scripts', 'print_page', 'quit', 'refresh', 'remove_all_credentials', 'remove_credential', 'remove_virtual_authenticator', 'save_screenshot', 'script', 'session_id', 'set_page_load_timeout', 'set_script_timeout', 'set_user_verified', 'set_window_position', 'set_window_rect', 'set_window_size', 'start_client', 'start_devtools', 'start_session', 'stop_client', 'storage', 'supports_fedcm', 'switch_to', 'timeouts', 'title', 'unpin', 'virtual_authenticator_id', 'webextension', 'window_handles']
>>> driver.quit()
>>>
```

### 解决方案

回到本问题，由于运行自动化多种的Linux并没有桌面系统，所以可以增加无头模式来运行用例，即增加`options.add_argument("--headless")`:

```python
        elif browser.lower() == 'firefox':
            if 'linux' in cls.os_platform.lower():
                from selenium.webdriver.firefox.options import Options
                options = Options()
                options.add_argument("-profile")
                options.add_argument("--headless")   # 此次新增，使用无头模式，规避显示问题
                # The fallowing content of profile, should be replaced by your
                # actually settings which from firefox's 'default:settings'
                options.add_argument("/root/snap/firefox/common/.cache/mozilla/firefox/shfysd7o.default")
                cls.driver = webdriver.Firefox(options=options)
            else:
                cls.driver = webdriver.Firefox()
```

此时再执行用例：

```python
[gavin@Gavin automation]$ python run_tests.py --automation-type=web --browser=firefox
pytest args: ['--alluredir', '/home/gavin/tools/reports/json', '--clean-alluredir', '--automation-type=web', '--cov=.', '--cov-report=xml:/home/gavin/tools/reports/coverage.xml', 'testcase/web']
[INFO] 浏览器检测通过：firefox
================================================================================================ test session starts ================================================================================================
platform linux -- Python 3.9.21, pytest-8.4.1, pluggy-1.6.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: /home/gavin/tools/automation
configfile: pytest.ini
plugins: profiles-0.2.0, xdist-3.8.0, progress-1.3.0, cov-7.0.0, allure-pytest-2.13.5
collected 1 item                                                                                                                                                                                                    

testcase/web/test_web.py::test_web
```

可以看到，不再报错，用例正常执行；如果哪天切换了运行环境，所在的Linux系统有桌面，再注释掉`options.add_argument("--headless")`即可。



---
title: 使用Appium初始化driver碰到的问题记录
date: 2024-04-02 21:52:39
author: Gavin Wang
img:
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: 使用Appium初始化driver碰到的问题记录
categories:
    - [Automation]
    - [Appium]
tags:
    - Automation
    - Appium
---


# 概述

最近在写一个基于pytest+Appium的APP GUI自动化测试框架，使用Appium初始化driver的时候，碰到了各种各样的问题，现把期间碰到的问题做一下小结，供有需要的同学参考。

# 碰到的问题与解决方法

说明：

如下问题，都是接连出现的，即出现了问题1，解决了问题1，再出现问题2，有一定的关联性。

## 问题1：AttributeError: 'NoneType' object has no attribute 'to_capabilities'


```python
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android  import UiAutomator2Options

desired_caps = {
    'platformName': 'Android',
    'platformVersion': '10',
    'deviceName': '62b6aca8',
    'automationName': 'UiAutomator2',
    'appPackage': 'com.xkw.client',
    'appActivity': 'com.zxxk.page.main.MainActivity'
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
```

上述代码执行的时候，报错：

```python
>>> driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Users\Wang\AppData\Local\Programs\Python\Python311\Lib\site-packages\appium\webdriver\webdriver.py", line 229, in __init__
    super().__init__(
  File "C:\Users\Wang\AppData\Local\Programs\Python\Python311\Lib\site-packages\selenium\webdriver\remote\webdriver.py", line 188, in __init__
    capabilities = options.to_capabilities()
                   ^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'to_capabilities'
>>>
```


{% note success %}
解决方法：
{% endnote %}


```python
from appium.webdriver.webdriver import AppiumOptions

appium_options = AppiumOptions()
appium_options.load_capabilities(capabilities)
driver = webdriver.Remote(appium_server_url, options=appium_options)
```


## 问题2: Original error: Neither ANDROID_HOME nor ANDROID_SDK_ROOT environment variable was exported.

在问题1解决后，碰到问题2，报错信息如下：

```shell
UnknownError: An unknown server-side error occurred while processing the command. Original error: Neither ANDROID_HOME nor ANDROID_SDK_ROOT environment variable was exported. Read https://developer.android.com/studio/command-line/variables for more details
    at getResponseForW3CError (C:\Program Files\Appium Server GUI\resources\app\node_modules\appium\node_modules\appium-base-driver\lib\protocol\errors.js:804:9)
    at asyncHandler (C:\Program Files\Appium Server GUI\resources\app\node_modules\appium\node_modules\appium-base-driver\lib\protocol\protocol.js:380:37)
>>>
```

{% note success %}
解决方法：
{% endnote %}

安装android SDK。


## 问题3：need the android.permission.INSTALL_GRANT_RUNTIME_PERMISSIONS permission

报错信息如下：

appium You need the android.permission.INSTALL_GRANT_RUNTIME_PERMISSIONS permission to use the Pa...

{% note success %}
解决方法：
{% endnote %}

手机开发者模式中开启USB调试（安全设置）



## 问题4：UnknownError: An unknown server-side error occurred while processing the command. Original error: Error executing adbExec. 

详细报错信息如下：

```shell
UnknownError: An unknown server-side error occurred while processing the command. Original error: Error executing adbExec. Original error: 'Command 'C:\\Users\\Wang\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe -P 5037 -s 62b6aca8 install -g 'C:\\Program Files\\Appium Server GUI\\resources\\app\\node_modules\\appium\\node_modules\\io.appium.settings\\apks\\settings_apk-debug.apk'' exited with code 1'; Command output: adb: failed to install C:\Program Files\Appium Server GUI\resources\app\node_modules\appium\node_modules\io.appium.settings\apks\settings_apk-debug.apk: Failure [INSTALL_FAILED_USER_RESTRICTED: Install canceled by user]
```

{% note success %}
解决方法：
{% endnote %}

开发者模式中允许USB安装apk


## 问题5：启动Appium Server桌面版报错

报错信息如下：

```shell
UnknownError: An unknown server-side error occurred while processing the command. Original error: Cannot verify the signature of 'C:\Users\Wang\AppData\Local\Temp\2024219-17712-1k7ahp1.639ci\appium-uiautomator2-server-v4.27.0.apk'. Original error: The 'java.exe' binary could not be found neither in PATH nor under JAVA_HOME (The JAVA_HOME environment variable is not set for the current process)
```

{% note success %}
解决方法：
{% endnote %}

启动Appium server桌面版本时，配置java_home路径，如：C:\Program Files\Java\jdk-21


## 问题6：driver初始化时候启动APP报错

报错信息如下：

```shell
Stacktrace:
UnknownError: An unknown server-side error occurred while processing the command. Original error: Cannot start the 'com.xkw.client' application. Visit https://github.com/appium/appium/blob/master/docs/en/writing-running-appium/android/activity-startup.md for troubleshooting. Original error: Error executing adbExec. Original error: 'Command 'C:\\Users\\Wang\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe -P 5037 -s 62b6aca8 shell am start -W -n com.xkw.client/com.zxxk.page.main.MainActivity -S -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -f 0x10200000' exited with code 255'; Command output: Security exception: Permission Denial: starting Intent { act=android.intent.action.MAIN cat=[an uid=2000) not exported from uid 10174
```

{% note success %}
解决方法：
{% endnote %}

出现这样的错误一定是因为当前的appActivity设置的不是app首次进入的appActivity；

获取首次应用的活动名称可以通过 启动一次随机 monkey命令来获取

```shell
adb shell
monkey -p com.XXXX.XXX -vvv 1 
```

过程参考如下：

```shell
C:\Users\Wang>adb shell
lavender:/ $ monkey -p com.xkw.client  -vvv 1
  bash arg: -p
  bash arg: com.xkw.client
  bash arg: -vvv
  bash arg: 1
args: [-p, com.xkw.client, -vvv, 1]
 arg: "-p"
 arg: "com.xkw.client"
 arg: "-vvv"
 arg: "1"
data="com.xkw.client"
:Monkey: seed=1711059478748 count=1
:AllowPackage: com.xkw.client
:IncludeCategory: android.intent.category.LAUNCHER
:IncludeCategory: android.intent.category.MONKEY
// Event percentages:
//   0: 15.0%
//   1: 10.0%
//   2: 2.0%
//   3: 15.0%
//   4: -0.0%
//   5: -0.0%
//   6: 25.0%
//   7: 15.0%
//   8: 2.0%
//   9: 2.0%
//   10: 1.0%
//   11: 13.0%
:Switch: #Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;launchFlags=0x10200000;component=com.xkw.client/com.zxxk.page.main.LauncherActivity;end
    // Allowing start of Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] cmp=com.xkw.client/com.zxxk.page.main.LauncherActivity } in package com.xkw.client
    // Allowing start of Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] cmp=com.xkw.client/com.zxxk.page.main.LauncherActivity } in package com.xkw.client
Events injected: 1
:Sending rotation degree=0, persist=false
:Dropped: keys=0 pointers=0 trackballs=0 flips=0 rotations=0
## Network stats: elapsed time=27ms (0ms mobile, 0ms wifi, 27ms not connected)
// Monkey finished
lavender:/ $
```

这里的'com.zxxk.page.main.LauncherActivity'为启动页，修改后的代码参考如下：

```python
from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android  import UiAutomator2Options

appium_server_url = 'http://localhost:4723/wd/hub'
desired_caps = {
    'platformName': 'Android',
    'platformVersion': '10',
    'deviceName': '62b6aca8',
    'skipServerInstallation': True,
    'automationName': 'UiAutomator2',
    'appPackage': 'com.xkw.client',
    'appActivity': 'com.zxxk.page.main.LauncherActivity'
}

appium_options = AppiumOptions()
appium_options.load_capabilities(desired_caps)
driver = webdriver.Remote(appium_server_url, options=appium_options)
```

## 问题7：滑动操作时报错

滑动时碰到：
```shell
io.appium.uiautomator2.common.exceptions.InvalidElementStateException: Unable to perform W3C actions. Check the logcat output for possible error reports and make sure your input actions chain is valid.
```

{% note success %}
解决方法：
{% endnote %}

获取分辨率或屏幕高和宽，上面报错是因为超屏了，超过了高度和宽度导致的。

代码参考如下：

```python
    def get_size(self):
        """获取屏幕大小"""
        try:
            logging.info("开始获取设备屏幕大小。")
            size = self.driver.get_window_size()
            width = size.get("width")
            height = size.get("height")
            logging.info("获取设备屏幕大小完成。宽:(%s), 高(%s)", width, height)
            return width, height
        except Exception as err:
            logging.error("获取屏幕尺寸失败 ！ 错误为：(%s", err)
            return None
```



## 问题8：启动Appium重复安装apk

每次启动 Appium，运行测试脚本时，都会重新安装 io.appium.uiautomator2.server.apk 和 io.appium.uiautomator2.server.test.apk


{% note success %}
解决方法：
{% endnote %}

caps 增加设置：

```shell
skipServerInstallation：True
```

注意：

* 当设备上没有uiautomator2包时，不能设置skipServerInstallation：True
* 当设备上已安装uiautomator2包，可以设置skipServerInstallation：True -> 解决重复安装问题



## 问题9：启动uiautomatorviewer时报错

报错信息如下：

```shell
ERROR: No suitable Java found. In order to properly use the Android Developer
Tools, you need a suitable version of Java JDK installed on your system.
We recommend that you install the JDK version of JavaSE, available here:
  http://www.oracle.com/technetwork/java/javase/downloads

If you already have Java installed, you can define the JAVA_HOME environment
variable in Control Panel / System / Avanced System Settings to point to the
JDK folder.

You can find the complete Android SDK requirements here:
  http://developer.android.com/sdk/requirements.html
```

{% note success %}
解决方法：
{% endnote %}

这是因为安装了毕竟新的JDK，新版本的JDK中不再含有JRE，而uiautomatorviewer需要JRE。
解决方法是安装一个低版本的JDK，比如安装了JDK18，自动会安装JRE18，然后将JRE18路径配置到系统环境变量中。


## 问题10：使用uiautomatorviewer连接模拟器页面报错

报错信息如下:

```shell
Error while obtaining UI hierarchy XML file: com.android.ddmlib.SyncException: Remote object doesn't exist!
```

{% note success %}
解决方法1：
{% endnote %}

杀死adb服务器并重新启动它。

```shell
adb kill-server

adb start-server
```

命令面板执行这两条命令后再次连接即可

{% note success %}
解决方法2：
{% endnote %}

命令面板运行：`adb reconnect`

运行后再次点击连接即可。

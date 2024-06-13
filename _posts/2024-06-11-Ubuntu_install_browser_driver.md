---
title: 安装和配置浏览器所需的driver
date: 2024-06-11 23:00:00
author: Gavin Wang
img: "/img/in-post/selenium/Selenium-Xpath-In-Details.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 安装和配置浏览器所需的driver
categories:
    - [Automation]
tags:
    - Automation
---

# 概述

之前开发的`Web`自动化只能在`Windows`下运行，且只支持`Chrome`浏览器（`hard code`），后期做了拓展，能够支持`Windows`和`Linux`平台下的多款浏览器，其中`Chrome`和`Firefox`两个平台都支持，对于`IE`和`Edge`只有`Windows`支持。

本文主要介绍一下如何在`Linux`下安装和配置浏览器和`driver`。

`Windows`下安装比较简单，对应`exe`文件下载下来后放在浏览器所在路径即可。

# 安装&配置过程

## Firefox的geckodriver安装

下载地址：

`https://github.com/mozilla/geckodriver/releases`

`windows`下下载后，加压放到`Firefox`安装路径即可。

`Linux`下下载后解压，放在`Firefox`安装路径下， 一般情况下，`Firefox`默认安装路径为`/usr/bin`：


```shell
root@Gavin:/usr/bin# ls -l firefox
-rwxr-xr-x 1 root root 2377 Nov  6  2022 firefox
root@Gavin:/usr/bin# ls -l geckodriver
-rw-r--r-- 1 root root 10413536 Jun 11 15:36 geckodriver
root@Gavin:/usr/bin# chmod a+x geckodriver
```

直接将`geckodriver`放在此目录下，并增加可执行权限，此时通过`selenium`启动`firefox`提示：

<img class="shadow" src="/img/in-post/Profile_Missing.png" width="600">


解决方法：

`Ubuntu`端打开`firefox`浏览器（如使用xmanager），在浏览器中输入`about:profiles`，展示类似如下所示信息：

<img class="shadow" src="/img/in-post/about_profiles.png" width="800">


将`Local Director`处内容复制出来，使用如下代码即可：


```python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument("-profile")
options.add_argument("/root/snap/firefox/common/.cache/mozilla/firefox/shfysd7o.default")
br=webdriver.Firefox(options=options)
br.get("http://www.baidu.com/")
```

`/root/snap/firefox/common/.cache/mozilla/firefox/shfysd7o.default` 替换为你的`Local Director`处内容。

`Linux`下执行如上代码，确定能够正常启动`Firefox browser`。


## Chrome和chromedriver的安装

需要能够访问谷歌：

```shell
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add 
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add 
bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" 
apt -y update
apt -y install google-chrome-stable 
```

成功安装后，展示信息如下：

```shell
root@Gavin:/etc/apt/sources.list.d# dpkg -l | grep -i chrome
ii  chromium-chromedriver                            1:85.0.4183.83-0ubuntu3                   amd64        Transitional package - chromium-chromedriver -> chromium snap
ii  google-chrome-stable                             125.0.6422.141-1                          amd64        The web browser from Google
ii  node-chrome-trace-event                          1.0.3-2                                   all          create a trace of your node app per Google's Trace Event format
root@Gavin:/etc/apt/sources.list.d# 
```

或者访问`https://googlechromelabs.github.io/chrome-for-testing/`进行下载，选择`Stable`版本，并将`chromedriver`移动到`/usr/bin/`目录下。


执行如下代码，检查Linux下启动Chrome是否OK：

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

service = Service(executable_path='/usr/bin/chromedriver')
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.baidu.com/')
```

## 其他

* 由于没有`Mac`， 对于`MocOS Safari`的兼容，暂时不好处理；
* `Windows`下自带的浏览器(`IE, Edge`)，默认安装好`Selenium`后，天然支持，无需做任何安装处理。

## 参考链接

`https://blog.csdn.net/baixvkwfn/article/details/123876636`

`https://blog.csdn.net/weixin_41446370/article/details/136636176`


# 自动化项目中代码示例片段

```python
class BasePage():
    # 图片文件夹路径
    report_path = get_report_path()
    img_path = report_path + os.sep + "screenshots"
    # # 如果目录不存在，创建它
    if not os.path.exists(report_path):
        os.mkdir(report_path, 0o777)
        os.mkdir(img_path, 0o777)
    if not os.path.exists(img_path):
        os.mkdir(img_path, 0o777)

    # Support Linux and Windoes OS
    os_platform = platform.platform()

    @classmethod
    def init_driver(cls, browser='chrome'):
        # 支持不同类型的浏览器
        if browser.lower() == 'chrome':
            if 'linux' in cls.os_platform.lower():
                from selenium.webdriver.chrome.service import Service
                from selenium.webdriver.chrome.options import Options
                service = Service(executable_path='/usr/bin/chromedriver')
                options = Options()
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                cls.driver = webdriver.Chrome(service=service, options=options)
            else:
                cls.driver = webdriver.Chrome()
        elif browser.lower() == 'firefox':
            if 'linux' in cls.os_platform.lower():
                from selenium.webdriver.firefox.options import Options
                options = Options()
                options.add_argument("-profile")
                # The fallowing content of profile, should be replaced by your actually settigns which from firefox's 'default:settings'
                options.add_argument("/root/snap/firefox/common/.cache/mozilla/firefox/shfysd7o.default")
                cls.driver = webdriver.Firefox(options=options)
            else:
                cls.driver = webdriver.Firefox()
        elif browser.lower() == 'ie':
            if 'linux' in cls.os_platform.lower():
                print("\n[ERROR] Not support Linux OS for IE browser\n")
                sys.exit(1)
            cls.driver = webdriver.Ie()
        elif browser.lower() == 'edge':
            if 'linux' in cls.os_platform.lower():
                print("\n[ERROR] Not support Linux OS for Edge browser\n")
                sys.exit(1)
            cls.driver = webdriver.Edge()
        elif browser.lower() == 'safari':
            cls.driver = webdriver.Safari()
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        # 最大化浏览器
        cls.driver.maximize_window()

        # 设置隐式等待时间
        timeout = 10
        cls.driver.implicitly_wait(timeout)

    @classmethod
    def quit_driver(cls):
        if cls.driver:
            cls.driver.quit()
```

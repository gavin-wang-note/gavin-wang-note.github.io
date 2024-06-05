---
layout: post
title:  "Appium+python APP 自动化安装指南"
subtitle: "Appium+python APP automation guide"
date:  2015-07-23
author: "Gavin Wang"
catalog: true
summary: 详细介绍Appium+python开发APP自动化
top: true
img: "img/appium/appium1.jpg"
cover: true
categories:
    - [Automation]
    - [python]
tags:
    - Appium
    - Automation
    - APP
    - python
---


说明：

如果作为服务端，请参考软件安装和Python与python开发环境配置章节；

如果仅作为Client，请参考client安装章节。

# 软件安装

## 安装Nodejs

### 步骤1、下载并安装nodejs

下载nodejs安装包（http://nodejs.org/download/）并进行安装，**安装的时候有选项，记得把环境变量添加到path路径**。

下图红框中表示要下载的版本：

<img class="shadow" src="/img/in-post/current_version.png" width="1200">




### 步骤2、测试nodejs安装是否成功

在cmd中输入node –v，如果出现如下结果，则表明安装成功

<img class="shadow" src="/img/in-post/node_success.png" width="1200">


## **安装android的SKD**

### 步骤1、下载SKD包

安装android的sdk包，(http://developer.android.com/sdk/index.html),运行依赖 sdk中的 'android'工具，并确保你安装了Level17或以上的版本 api。

 

### 步骤2、设置环境变量

（1）解压压缩包到某个目录，如**C:\adt-bundle-windows**

（2）配置系统环境变量

变量名：**ANDROID_HOME**

变量值：**C:\adt-bundle-windows\sdk**

<img class="shadow" src="/img/in-post/ad_home.png" width="1200">



（3）添加系统path路径

变量名：**Path**

变量值：**%ANDROID_HOME%\tools;%ANDROID_HOME%\platform-tools;** 

<img class="shadow" src="/img/in-post/plat_path.png" width="1200">


### 步骤3、SDK包更新

由于谷歌服务器连接不是很稳定， SDK更新或安装其他工具时候会出现无法连接、连接超时、无法下载等问题，针对这个问题，可通过如下方法进行解决：

（1）启动 Android SDK Manager ，打开主界面，依次选择「Tools」、「Options...」，弹出『Android SDK Manager - Settings』窗口；

（2）在『Android SDK Manager - Settings』窗口中，在「HTTP Proxy Server」和「HTTP Proxy Port」输入框内填入mirrors.neusoft.edu.cn和80，并且选中「Force https://... sources to be fetched using http://...」复选框。

（3）设置完成后单击「Close」按钮，关闭『Android SDK Manager - Settings』窗口返回到主界面；依次选择「Packages」、「Reload」。

 

 

## JDK安装

### 步骤1、下载并安装JDK

安装oracle的JDK，本文以jdk1.7为示例，下载地址：

http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html

### 步骤2、设置JAVA_HOME

成功下载并安装后，设置环境变量JAVA_HOME：

变量名：**JAVA_HOME**

变量值：**C:\Program Files\Java\jdk1.7.0_13**

<img class="shadow" src="/img/in-post/java_home.png" width="1200">

### 步骤3、验证jdk是否安装成功

在**cmd**中输入**java -version**，如果出现下图结果，表明jdk1.7安装成功。

<img class="shadow" src="/img/in-post/jdk_success.png" width="1200">

 

## **安装Apache** **Ant** 

### 步骤1、下载Apache Ant

下载地址：http://ant.apache.org/bindownload.cgi）

说明：

​    如果不使用jenkins进行CI操作，则不需要安装它。

### 步骤2、设置环境变量

到C盘，创建apache文件夹，并将下载后的ant解压后，拷贝到此目录下（C:\apache\apache-ant-1.9.4）

然后设置环境变量：

​     变量名： **ANT_HOME**

​     变量值： 你刚解压到的路径： **C:\apache\apache-ant-1.9.4**

<img class="shadow" src="/img/in-post/ant_home.png" width="1200">


设置Path:

变量名：**Path**

变量值：**%ANT_HOME%\bin** 

<img class="shadow" src="/img/in-post/ant_bin.png" width="1200">



### 步骤3、测试ant环境安装成功

运行cmd，输入ant，如果没有指定build.xml就会输出：

<img class="shadow" src="/img/in-post/ant_success.png" width="1200">

查看ant版本

<img class="shadow" src="/img/in-post/ant_version.png" width="1200">

如上信息表明ant已经成功安装。

  

## **安装.net framework组件** 

### 步骤1、下载.net framework

说明：

如果不安装，在进行下一步安装appium时，会报如下错误信息：

<img class="shadow" src="/img/in-post/start_error_appium.png" width="1200">

由于Microsoft Windows Studio 2008和Windows SDK for Windows Server 2008 and .NET Framework 3.5都比较大，很多东西用不到，以及考虑到后期appium更新后对更高版本的邀请，这里选择安装Microsoft .NET Framework 4.5。

Microsoft .NET Framework 4.5 下载地址：http://www.microsoft.com/en-us/download/details.aspx?id=30653

 

### 步骤2、安装.NET Framework 4.5

步骤略。

  

## **安装appium**

### 步骤1、安装appium

使用npm安装appium，在cmd中使用命令**npm install  -g appium** 下载appium（整个过程稍慢，请耐心等待）。

**说明：**

如果安装过程中报如下错：

<img class="shadow" src="/img/in-post/install_appium_error.png" width="1200">

请到“C:\Users\Administrator\AppData\Roaming”目录下，创建npm目录，然后再运行“npm install -g appium”命令即可。

 

### 步骤2、校验appium是否安装成功

安装成功后，在cmd输入**appium**出现以下信息表明安装成功：

<img class="shadow" src="/img/in-post/install_appium_success.png" width="1200">

 

## **安装wd**

启动cmd，在窗口输入npm install wd命令，继续wd的安装：

<img class="shadow" src="/img/in-post/wd.png" width="1200">

# 环境检测

运行cmd， 输入**appium-doctor**检查你的环境是不是都配置好了。 如图：

<img class="shadow" src="/img/in-post/env_check_success.png" width="1200">

整体的环境变量已经配置完毕，接下来要进行 python和selenium的安装、配置。

 

# Python和selenium的安装配置

## 安装python

### 步骤1、下载并安装python2.7.5

链接地址：https://www.python.org/download/releases/2.7.5/

**说明**：

   本文选择python版本为2.7.5，该版本较其他版本比较稳定。

 

### 步骤2、设置python环境变量

变量名：**Path**

变量值：**C:\Python27**

<img class="shadow" src="/img/in-post/python_path.png" width="1200">


## **安装setuptools**

### 步骤1、下载ez_setup.py

参考地址如下：

https://pypi.python.org/pypi/setuptools#windows-7-or-graphical-install

在链接页面中，找到**ez_setup.py**，入下图所示：

<img class="shadow" src="/img/in-post/ez_setup1.png" width="1200">

**右击下载****ez_setup.py****文件到本地**：

<img class="shadow" src="/img/in-post/ez_setup2.png" width="1200">



**注意：**

  **ez_setup.py文件要存放在不包含中文以及空格目录中！**

### 步骤2、安装setuptools

（1）启动cmd，进入ez_setup.py所在目录

（2）执行python ez_setup.py install进行下载安装setuptools：

<img class="shadow" src="/img/in-post/download_setup.png" width="1200">



然后就会在python的安装目录中生成scripts目录，其中有easy_install.exe

<img class="shadow" src="/img/in-post/easy_install_package.png" width="1200">

 

步骤3、设置环境变量

将C:\Python27\Scripts 设置到系统环境变量中：

<img class="shadow" src="/img/in-post/python_path.png" width="1200">

 

## **安装pip**

启动cmd进入命令行，把目录切换到python的安装目录下的Script文件夹下，运行 **easy_inatall pip**命令进行pip在线安装，如下图所示：

<img class="shadow" src="/img/in-post/install_pip.png" width="1200">

 

## **安装python依赖包**

依赖包，如下：

nose

selenium

Appium-Python-Client

启动cmd，分别输入

pip install nose

pip install selenium

pip install Appium-Python-Client

进行安装操作, 如下图所示：

<img class="shadow" src="/img/in-post/appium_client_setup.png" width="1200">


如果系统中已经安装过了，再次进行安装时，会出现类似如下界面所展示的信息：

<img class="shadow" src="/img/in-post/install_nose.png" width="1200">


其他依赖包的安装

| **包名**    | **描述**          |
| ----------- | ----------------- |
| **mysqldb** | 用于Mysql操作使用 |
|             |                   |
|             |                   |
|             |                   |

详见目录; pythond.3rd.lib中可执行文件，双击安装即可。


# Eclipse与python开发环境配置

## **Eclipse下载与安装**

### 步骤1、下载eclipse

链接地址：

http://www.eclipse.org/downloads/

### 步骤2、安装eclipse

下载下来是个压缩包，比如：eclipse-standard-luna-R-win32.zip，无需安装，直接解压即可。

 

**注意：**

   **Eclipse解压后所在目录不能含有中文、空格。**

 

## **Pydev插件安装**

### 步骤1、打开Eclipse工具

### 步骤2、市场中安装pydev

**在eclipse**工具，点击Help，选择Eclipse Marketplace，如下图所示：

<img class="shadow" src="/img/in-post/market.png" width="1200">


在弹出界面中Find出，输入pydev，点击GO进行搜索：

<img class="shadow" src="/img/in-post/go.png" width="1200">

说明：

上图表明我已经安装过了，所以是Uninstall状态，未安装状态应该是install。

 

点击“install“进行pydev插件的安装。

 

### 步骤3、配置pydev

在Window --> Preferences中，点击”Quick Atuo-Config”，并点击OK即可，如下图所示步骤操作：

<img class="shadow" src="/img/in-post/auto_config.png" width="1200">

 

## **建立python工程**

### 步骤1、创建PyDev Project

选择PyDev Project，直接点击Next：

<img class="shadow" src="/img/in-post/project_next.png" width="1200">

命名工程名称（如mpsAutotest），并点击finish，出现提示框后，点击“yes“：

<img class="shadow" src="/img/in-post/next_ok.png" width="1200">

 

### 步骤2、在工程中新建一个Python Package

右键点击src, New>Pydev Package，选择源文件路径及输入包名：

<img class="shadow" src="/img/in-post/pvdev_package.png" width="1200">


### 步骤3、测试工程是否创建正常

在testCase目录下新创建个test.py文件，输入脚本内容：

```python
#/usr/bin/env python
#-*- coding:UTF-8 -*-

import os,sys

def nameInfo(name=None):
    return name


if __name__ == "__main__":
    name = nameInfo('Gikoo')
    print name
    print sys.platform
    print os.path.sep
```

按F9即可看到输出结果：

<img class="shadow" src="/img/in-post/example.png" width="1200">

如上图所示，说明开发环境安装成功

 

# appium启动篇

## **启动appium**

### 步骤1、启动cmd窗口

### 步骤2、执行appium -a 127.0.0.1 -p 4723命令

在cmd中输入 appium -a 127.0.0.1 -p 4723 (-a表示ip，-p表示端口， 可以通过appium -h查看更多命令)，启动appium服务。

如果如下图所示 就表示 appium服务启动成功了：

<img class="shadow" src="/img/in-post/start_appium_success.png" width="1200">



**注意：**

这个窗口不要关闭 因为这是appium的服务，关了就相当于关了服务，后面过程无法执行，而且这个窗口也是 日志输出的窗口，用于排错。

 

# client安装

## 客户端安装步骤如下：

### 安装python并设置python环境变量

详请参考Python和selenium的安装配置章节中安装python与设置环境变量操作

### 安装setuptools

详请参考Python和selenium的安装配置章节中安装setuptools操作

 

### 安装pip后

详请参考Python和selenium的安装配置章节中安装pip操作

### 安装client

启动cmd，分别输入

pip install Appium-Python-Client

pip install selenium

 

 安装selenium ide

安装selenium ide，是为了通过ide录制web界面操作，并通过导出转换为需要的语言代码，进而修改以节约web界面用例开发时间。

## **下载ide文件**

打开火狐浏览器，输入如下网址

 

http://release.seleniumhq.org/selenium-ide/2.0.0/selenium-ide-2.0.0.xpi

 

## **安装xpi文件**

火狐浏览器会自动下载xpi文件，成功安装后弹出类似如下提示：

<img class="shadow" src="/img/in-post/firefox_noty1.png" width="1200">



 

## **重启firefox**

点击“立即安装”即可进行安装操作。

<img class="shadow" src="/img/in-post/after_restart_firefox.png" width="1200">

点击“立即重启”，以加载新安装的ide插件。

 

## **确认安装是否成功**

<img class="shadow" src="/img/in-post/ide_plug.png" width="1200">

至此，appium iede安装完毕。

其他插件，比如firebug、firepath等，直接将下载的文件拖入firefox进行安装即可。或者直接在组建中搜索，然后点击安装即可。

 

 

 

# 参考文档

示例参考：http://testerhome.com/topics/153


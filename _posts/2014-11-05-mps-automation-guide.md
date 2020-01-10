---
layout:     post
title:      "MPS接口自动化测试指南"
subtitle:   "MPS Interface automation test guide"
date:       2014-11-15
author:     "Gavin"
catalog:    true
tags:
    - interface
    - Automation
    - Unittest 
    - Jenkins
---


# 需求描述

## 基本要求:

对服务后台一系列的HTTP接口功能测试，主要涉及POST、PUT、GET、DELETE等类型；
用例与用例之间保持独立，即低耦合。

输入：

根据各接口描述，构造不同的参数输入值，模拟客户端请求。

输出：

服务端响应（HTTP状态码/具体响应数据）。

检验：

用例执行过程中增加断言，判断用例执行成功/失败与否。

结果：

可视化的HTML/XML测试报告；

用例执行过程中日志信息记录。

CI：
与jenkins结合，完成持续构建、自动部署、自动执行，并将结果发送到相关人。

## 实现方法

* 采用python脚本来驱动测试,使用Unittest框架
* 调用HTTP接口，采用python封装好的API
* 测试需要的HTTP，组装字符转处理
* 测试数据以随机数传递到各接口对应参数，确保用例独立性
* 设置1个/多个检查点，校验响应消息中的返回值（通过解析响应消息得到）
* 首次执行需根据实际测试环境，修改下配置文件autotest.config（注：不是每次测试
  都需要修改这个配置文件，只有在变更测试环境情况下才需要修改）



# 测试框架

设计图：

<img class="shadow" src="/img/in-post/mps_automation_design.png" width="1200">


用例执行过程示意图：

<img class="shadow" src="/img/in-post/mps_case_run_process.png" width="1200">


# 自动化使用指南

## 自动化概述

目前使用python的urllib、urllib2模块，封装http请求消息，完成发送json报文到后台，后台处理后，根据http response或其他，并增加断言，以判断用例执行结果是成功还是失败。

   同时组织了用例生成的报告，以及与jenkins结合，实现持续集成，自动执行用例，并将结果以HTML Report方式发送到相关邮箱，及时知道构建结果。



## 测试准备

### 配置文件

只需保证自动化配置文件内容正确即可。配置文件存放在src/common/config/目录下，名称是：autotest.config。配置文件各参数介绍，请参考下图：

<img class="shadow" src="/img/in-post/mps_config.png" width="1200">



### 第三方模块的安装


| 模块名称                   | 安装命令                                                         | 模块说明|
| ---------------------- | ------------------------------------------------------------ |--------------- |
| progressbar          | pip install progressbar                     |进度条 |
| configobj | pip install configobj | 读取配置文件 |
| matplotlib | pip install matplotlib | 绘图使用 |
| dateuti | pip install python-dateutil | 绘图使用 |
| numpy | pip install numpy | 绘图使用 |
| pyparsing | pip install pyparsing | 解析xml文件使用 |




### 账号自定义属性信息不能为必填项

<img class="shadow" src="/img/in-post/mps_account.png" width="1200">

不能存在“自定义账号属性”；存在也可以，但是属性要求是可选的，不能是必填的（因为每个测试环境不同，无法满足每个测试环境创建账号需要的自定义的属性信息）:

<img class="shadow" src="/img/in-post/mps_account2.png" width="1200">




### 存在可用的测试分组

测试环境中需要存在“自动化测试组”这个分组信息。

说明：
目前第3、第4点，已经在测试用例执行入口脚本(interfaceRunner.py)中增加了检测机制，如果检测不通过，则用例退出执行，并给出为何退出原因，方便使用者进行测试环境的调整。

## 测试用例的编写

1、所有用例的编写，放在对应功能目录下testcase目录下，且必须以test开头；

2、每一个函数就是一个测试用例，函数名的命名尽量要有意义，能根据函数名称而知道用例是做哪方面的功能测试；

3、用例要保证独立性，互相不依赖。



示例如下：
成功登录测试用例

<img class="shadow" src="/img/in-post/mps_success_login.png" width="1200">


异常登录测试用例

<img class="shadow" src="/img/in-post/mps_failed_login.png" width="1200">


创建一个通知测试用例

<img class="shadow" src="/img/in-post/mps_notification.png" width="1200">


## 测试用例的执行

有两种执行方式
方式1、通过IDE执行

比如在eclipse中打开某个用例，右击选择Run As Python unit-test：

<img class="shadow" src="/img/in-post/mps_run_by_ide.png" width="1200">


方式2、通过入口脚本执行
入口脚本存放在src目录下，名称：interfaceRunner.py，双击即可执行所有的测试用例：

<img class="shadow" src="/img/in-post/mps_run.png" width="1200">

说明：
选择性的执行用例，可在后期增加，目前只有执行全部用例函数，无选择性执行用例函数。



## 用例执行进度查看
双击src目录下processBar.py，即可查看用例执行进度：

<img class="shadow" src="/img/in-post/mps_progress.png" width="1200">


在网络或server端响应较慢情况下，用例执行耗时非常长（有一次是79个用例耗时47分钟37秒）；经过测试，这79个测试用例，在公网环境正常状态下，只需88秒即可完成。由此也证实了，网络不好的情况下，并不影响自动化测试用例的正常执行。



## 历史测试记录数据展示

每次执行用例（通过执行interfaceRunner.py完成），将测试结果（report目录下Interface_TestReport.xml文件）解析、入库到SQLite  report_history表中，通过统计脚本(statInfoInfo.py)读取数据库中历史记录，以曲线图形展示用例执行成功率。



## 创建sqlite表相关语句

```
CREATE TABLE [report_history] (
  [begintime] DATETIME NOT NULL, 
  [endtime] DATETIME NOT NULL, 
  [total] INT NOT NULL, 
  [passed] INT NOT NULL, 
  [failed] INT NOT NULL, 
  [error] INT NOT NULL,
  PRIMARY KEY (begintime));
```

## 测试报告查看

测试报告在report目录下Interface_TestReport.html文件，部分截图如下：

<img class="shadow" src="/img/in-post/mps_report.png" width="1200">


## 配置文件说明

配置文件在src/common/config目录下，名称为：autotest.config，详细内容与解释，请参考本文附件章节中的“配置文件说明”excel文档。

## 优缺点

### 优点
1、直接使用JSON构造报文
    构造的消息体，直接使用json表示。因为后台使用的是JSON，拿到接口文档后就可直接构造报文了，不需要转换成其他类型的报文（如果使用pyresettest，需要将json转成yaml）。

2、参数化
	所有测试用例中的host、账号隶属于的组织结构的id、接口的URL地址、接口中需要的参数/tooken等信息，都可以从配置文件/基类中获取；

* 变更测试环境，无需对测试用例进行修改，仅需修改config目录下配置文件即可
* cookie是动态变化的，直接从login response中获取，并传递下去，不需要手工干预，不会出现会话过期失效问题
* 参数化的另外一个好处是，可以多样化构造报文中字段各式各样的值，测试/验证后台能否正常处理
* 扩展性强：接口变更后（比如携带的参数调整），直接修改对应基类中构造json报文代码即可。

3、测试记录跟踪、测试结果可视化

 * 记录用例运行过程中的日志;
 * 可生成HTML和XML格式测试报告，界面直观，数据一目了然

4、用例统一管理
     用例执行有一个统一的入口，可执行所有的用例（如果有需要，将来可增加选择性执行用例）

5、成功与jenkins结合，做CI(持续集成)测试
   目前已成功完成与jenkins结合，进行自动构建，并将测试结果（自动化运行日志、测试报告和jenkins构建日志）发送到邮箱，如下图所示：

<img class="shadow" src="/img/in-post/mps_email.png" width="1200">



### 缺点
​    1、用例管理、维护成本稍高一点；

​    2、每个测试用例都是一个函数，用例的编写方面，需要会一点python；
​         对测试而言，有机会去了解后台代码，可以更好的熟悉业务逻辑、对产品进行更
深入的测试，暂时的缺点也会变成后期的优点吧

​    3、用例编写无GUI
​         还是归根到用例的编写上，目前提供的日志与测试用例执行结果（用例中增加了
断言），在一定程度上是有助于定位用例执行失败的原因。



# 搭建Jenkins持续集成环境
## Jenkins的下载与安装
   度娘吧。



## 插件的安装

涉及到的插件，主要有GIt Plugin、Email Extension Plugin和 HTML Publisher plugin3个插件。GIt Plugin用于从github上下载代码；Email Extension Plugin用于持续构建过程后发送邮件；HTML Publisher plugin用于生成邮件中的html报告。
本文以安装git plugin为例进行插件安装的介绍。

## Git Plugin的安装

Jenkins缺省支持CVS，Subversion，Maven和SSH。依次进入"系统管理"-->"插件管理"-->"可选插件".这里列出了目前可以获得的所有的插件。

<img class="shadow" src="/img/in-post/mps_jenkisn_all_plugs.png" width="1200">

选择"Git plugin"，点击下方的"直接安装":

<img class="shadow" src="/img/in-post/mps_update_plugs.png" width="1200">


插件安装已经完成，需要重启jenkins，新插件才能生效。

## 环境配置

依次进入"系统管理"-->"系统设置"，设置Jenkins相关参数。

### 设置git路径

设置获取路径、代码用户名，如下图所示:

<img class="shadow" src="/img/in-post/mps_git.png" width="1200">


### 设置超时时间

源码管理  高级  添加“Additional Behaviours”，设置down代码超时时间：

<img class="shadow" src="/img/in-post/mps_timeout.png" width="1200">


### 构建触发器

如下图所示：

<img class="shadow" src="/img/in-post/mps_trigger.png" width="1200">


表示每周一至周五的23点自动运行。



### 增加构建步骤

执行bat命令，运行接口用例入口脚本，执行所有测试用例，如下图所示：

<img class="shadow" src="/img/in-post/mps_before_build.png" width="1200">


bat命令行代码如下：

```
@echo off
cd C:\Jenkins\workspace\interfaceAutotest\Testing\autotest\intefaceTest\src
python interfaceRunner.py
```



### 构建后操作

如下图所示，增加构建后操作。示例中展示的是将测试报告、测试日志、构建日志发送到指定邮箱。

<img class="shadow" src="/img/in-post/mps_send_email_conf.png" width="1200">


Editable Email Notification中Default Content，内容信息如下：

```
<html>

    <head>
        <title></title>
    </head>

    <body>
        Hi All,捷库接口自动化测试结果 <br>
        <font color="#0B610B" size="4">  请点击红色链接，检查控制台输出，查看本次持续集成构建结果：</font> <a href="${BUILD_URL}console"><b><font color="#DF0101" size="5"> ${ENV, var="JOB_NAME"}</font></b></a>

        <table width="95%" cellpadding="0" cellspacing="0" style="font-size:11pt; font-family:Tahoma, Arial, Helvetica, sans-serif">
            <tr>
                <td>
                    <h2>
                        <font color="#0000FF"  size="4">构建结果 -- ${BUILD_STATUS}</font>
                    </h2>
                </td>
            </tr>
            <tr>
                <td>
                    <br>
                    <b><font color="#0B610B">构建信息:</font></b>
                    <hr size="2" width="100%" align="center">
                </td>
            </tr>
            <tr>
                <td>
                    <ul>
                        <li>项目名称 - ${PROJECT_NAME}</li>
                        <li>构建编号 ： 第${BUILD_NUMBER}次构建</li> 
                        <li>触发原因： ${CAUSE}</li>  
                        <li>构建结果(For xxx) -- <a href="${PROJECT_URL}ws">${PROJECT_URL}ws</a> </li>
                        <li>项目 Url -- <a href="${PROJECT_URL}">${PROJECT_URL}</a></li>
                        <li>构建 Url -- <a href="${BUILD_URL}">${BUILD_URL}</a></li>
                        <li>SVN 版本 -- ${SVN_REVISION} </li>
                    </ul>
                </td>
            </tr>
            <tr>
                <td>
                    <b><font color="#0B610B">自最后一次构建成功后的变 化:</font></b>
                    <hr size="2" width="100%" align="center">
                </td>
            </tr>
            <tr>
                <td>
                    <ul>
                        <li>在此查看历史变化记录: -- <a href="${PROJECT_URL}changes">${PROJECT_URL}changes</a>
                        </li>
                    </ul>${CHANGES_SINCE_LAST_SUCCESS, reverse=true, format="Changes for Build #%n:<br>%c<br>", showPaths=true, changesFormat="<pre>[%a]<br>%m</pre>", pathFormat="&nbsp;&nbsp;&nbsp;&nbsp;%p"}
                </td>
            </tr>        

            <tr>
               <td>
                   <br>
               </td>
            </tr>
            
            <tr>
                <td>
                    <b><font color="#0B610B">失败的测试结果：</font></b>
                    <hr size="2" width="100%" align="center">
                </td>
            </tr>
            <tr>
                <td>
                    <pre style="font-size:11pt; font-family:Tahoma, Arial, Helvetica, sans-serif">

$FAILED_TESTS
</pre><br>
                </td>
            </tr>
            <tr>
                <td>
                    <b><font color="#0B610B">构建日志 (最后 100 行):</font></b>
                    <hr size="2" width="100%" align="center">
                </td>
            </tr>
            <tr>
                <td>
                    测试日志 (如果有运行测试): <a href="${PROJECT_URL}ws/Testing/autotest/intefaceTest/report/interface_autotest.log">${PROJECT_URL}ws/Testing/autotest/intefaceTest/report/interface_autotest.log</a><br>
                    <br>
                </td>
            </tr>
            <tr>
                <td>
                    <textarea cols="80" rows="30" readonly="readonly" style="font-family: Courier New">
${BUILD_LOG, maxLines=100}
</textarea>
                </td>
            </tr>
        </table>

<hr size="2" width="100%" align="center" />  

（说明：本邮件由系统自动生成，请勿回复！）
            <tr> <td>
                   <br>
               </td>
            </tr>
    </body>
</html>
```



### 实践结果

如下为邮件发送后，在Foxmail邮箱中的展示：

<img class="shadow" src="/img/in-post/msp_send_email_show.png" width="1200">



# Jenkins展示乱码问题



## 问题1、控制台输出中文展示是乱码
如下图所示：

<img class="shadow" src="/img/in-post/mps_console.png" width="1200">



## 问题2、邮件中github变化信息乱码

<img class="shadow" src="/img/in-post/mps_github.png" width="1200">



## 问题3、邮件中最后100行记录乱码

<img class="shadow" src="/img/in-post/mps_last_100.png" width="1200">


解决方法
Jenkins中Git仓库变更集中文注释显示乱码问题

C:\Jenkins\jenkins.xml 新增蓝色粗体标记参数(-Dfile.encoding=utf-8)，然后重启Jenkins服务，完毕！

```
  <executable>%BASE%\jre\bin\java</executable>
  <arguments>-Xrs -Xmx256m  -Dfile.encoding=utf-8 -Dhudson.lifecycle=hudson.lifecycle.WindowsServiceLifecycle -jar "%BASE%\jenkins.war" --httpPort=8080</arguments>
```

原因： 

为什么Jenkins 使用 SVN 仓库不会出现非 ANSI 字符乱码，因为 Git 插件获取变更集时保存的不是 XML格式文档（虽然后缀都是.xml），这就导致了显示的时候不知道以什么编码方式来显示，就使用了系统默认编码，中文的也就是GBK。 而 GIT Commit 注释默认是 UTF-8。

## 问题4、接口jenkins控制台中文乱码问题

系统管理--系统设置，增加全局属性，设置LANG=zh_CN.UTF-8，如下图所示：

<img class="shadow" src="/img/in-post/mps_system_conf1.png" width="1200">


如上设置后，重启jenkins服务，进入系统设置 系统信息，查看环境变量，如下图所示：

<img class="shadow" src="/img/in-post/mps_system_conf2.png" width="1200">

再次执行构建，控制台输出如下：

<img class="shadow" src="/img/in-post/mps_console_output.png" width="1200">


# 管理注册用户

详细文档，请参考：

http://blog.csdn.net/wangmuming/article/details/22926025


# 邮箱测试失败（503错误码）

如果在系统管理系统设置中“邮件通知”测试邮箱发邮件失败，请确保“使用SMTP认证”中用户名和密码是正确的：

<img class="shadow" src="/img/in-post/mps_email_503.png" width="1200">

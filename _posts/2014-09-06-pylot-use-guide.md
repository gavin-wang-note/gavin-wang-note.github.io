---
layout:     post
title:      "pylot安装与使用"
subtitle:   "pylot use guide"
date:       2014-09-06
author:     "Gavin"
catalog:    true
tags:
    - pylot
---


## **概述**

Pylot是一个免费的开源工具，用于测试Web服务的性能和可扩展性。它运行HTTP负载测试，这是有用的容量规划，基准，分析和系统调整。pylot使用比较简单。而且测试结果相对稳定，不像Apache的ab工具，同样的url，测试结果飘忽不定。

Pylot产生并发负载（HTTP请求），验证服务器的响应，并制作报告的度量。测试套件的执行和监测，从一个GUI或shell /控制台。

Pylot基于Python开发，和著名的Apache压力测试工具ab一样，默认在命令行运行，也可以通过参数触发GUI界面，当然前提是安装了wxPython的。

 

## **尝试**

在尝试了python2.7.5、python2.6.2版本后，发现这两个版本均存在问题：

1、pylot不支持python2.7，仅支持python2.5或2.6（pylot工具2009年停止更新，然pylot相应的其他插件一直在更新中）

pylot-1.26\pylot_1.26\ui\console\win目录下，cpos.py文件部分内容如下：

```
import sys
 
is_25 = sys.version.startswith('2.5')
is_26 = sys.version.startswith('2.6')

 
if is_25:
  import _consolepos25 as _consolepos
elif is_26:
  import _consolepos26 as _consolepos

getpos = _consolepos.getpos
gotoxy = _consolepos.gotoxy
```

 

2、python2.6出现另外一个问题，tk不支持多线程

```
Generating Results...
Generating Graphs...
ERROR: Unable to generate graphs with Matplotlib

Done generating results. You can view your test at:
results/results_2014.09.06_21.59.10/results.html
Done.

Error in atexit._run_exitfuncs:
Traceback (most recent call last):
 File "C:\Python26\lib\atexit.py", line 24, in _run_exitfuncs
  func(*targs, **kargs)
 File "C:\Python26\lib\site-packages\matplotlib\_pylab_helpers.py", line 89, in
 destroy_all
  manager.destroy()
 File "C:\Python26\lib\site-packages\matplotlib\backends\backend_tkagg.py", lin
e 590, in destroy
  self.window.destroy()
 File "C:\Python26\lib\lib-tk\Tkinter.py", line 1685, in destroy
  for c in self.children.values(): c.destroy()
 File "C:\Python26\lib\lib-tk\Tkinter.py", line 1938, in destroy
  self.tk.call('destroy', self._w)
TclError: out of stack space (infinite loop?)
Error in sys.exitfunc:
Traceback (most recent call last):
 File "C:\Python26\lib\atexit.py", line 24, in _run_exitfuncs
  func(*targs, **kargs)
 File "C:\Python26\lib\site-packages\matplotlib\_pylab_helpers.py", line 89, in
 destroy_all
  manager.destroy()
 File "C:\Python26\lib\site-packages\matplotlib\backends\backend_tkagg.py", lin
e 590, in destroy
  self.window.destroy()
 File "C:\Python26\lib\lib-tk\Tkinter.py", line 1685, in destroy
  for c in self.children.values(): c.destroy()
 File "C:\Python26\lib\lib-tk\Tkinter.py", line 1938, in destroy
  self.tk.call('destroy', self._w)
_tkinter.TclError: out of stack space (infinite loop?)
```

 

综上所述，本文以python2.5为示例，介绍pylot的安装与简单使用。

 

## **软件列表**

| **软件名称**   | **作用**                                                     | **下载地址**                           |
| -------------- | ------------------------------------------------------------ | -------------------------------------- |
| **pylot**      | python的一个功能插件，进行网站压力测试                       | http://www.oschina.net/p/pylot-bug-fix |
| **Python**     | Pylot编译环境（必选）                                        |                                        |
| **Wxpython**   | Python语言的一套优秀的GUI图形库，用于GUI图形化界面展示（可选） |                                        |
| **numpy**      | 可选 - 用于报告以图表                                        |                                        |
| **matplotlib** | 可选 - 用于报告以图表                                        |                                        |
| **six**        | Matplotlib 的require lib                                     |                                        |
| **dateutil**   | Matplotlib 的require lib                                     |                                        |

 

**说明：**

**从Python(不含)以下部分为可选安装软件**

 

## **安装方法**

### 步骤1、下载pylot

登录到开源中国社区，下载pylot修复版即可。

http://www.oschina.net/p/pylot-bug-fix

 

下载后解压到某个目录下，注意，目录/路径中不要含有空格、中文字符，如：G:\pylot-master

 

 

### 步骤2、下载及配置Python以及其他插件

详见下文。

 

## **安装****python**

### 步骤1、下载并安装python2.5

安装，略。

 

### 步骤2、设置python环境变量

变量名：**Path**

变量值：**C:\Python25**

<img class="shadow" src="/img/in-post/pylot_python_path.png" width="1200">

 

### 步骤3、安装其他包

不用numpy和matplotlib，单独使用pylot+python也可以进行压力测试，但是这样测试生成的报表文件里是不包含曲线图的。为了能够图形化展示数据，这里介绍其他依赖包的安装。

Numpy下载地址：

http://sourceforge.net/projects/numpy/files/NumPy/1.4.1/numpy-1.4.1-win32-superpack-python2.5.exe/download?use_mirror=jaist

 

wxPython下载地址：

http://sourceforge.net/projects/wxpython/files/wxPython/2.9.1.1/



选择wxPython2.9-win32-2.9.1.1-py25



Six下载地址：

http://www.lfd.uci.edu/~gohlke/pythonlibs/#six

下载six-1.7.3.win32-py2.6，否则在生成报告过程中会出现如下错误信息：


<img class="shadow" src="/img/in-post/pylot_six_error.png" width="1200">

 

Dateutil下载地址：

http://www.lfd.uci.edu/~gohlke/pythonlibs/#python-dateutil

 

如果没有这个lib，则在生成报告过程中出现如下提示信息：

<img class="shadow" src="/img/in-post/pylot_lib_error.png" width="1200">

 

**说明：**

   **如果在使用过程中，遇到需要安装的一些依赖包，你可以到这里查找：**

**http://www.lfd.uci.edu/~gohlke/pythonlibs/**

 

## **使用pylot**

1、下载完pylot之后，解压到一个目录下，例如：C:\pylot，无需安装。

 

2、配置testcases.xml

   在pylot文件夹里，会看到一个testcases.xml的文件，我们需要更改一下这个文件，用记事本打开它，把需要测试的网页地址添加进去。

```
<testcases>
  <case>
    <url>http://midh.mlpplus.gikoo.cn/e-learning/index-test.html</url>
        <method>GET</method>
  </case>
</testcases>
```



上面代码中，http://midh.mlpplus.gikoo.cn/e-learning/index-test.html为要测试的网址，然后保存文件。



3、执行压力测试

**命令行模式：**



启动cmd，进入pylot所在目录，执行如下命令即可启动压力测试:

<img class="shadow" src="/img/in-post/pylot_performance.png" width="1200">



看到类似以上信息，就表示测试结束了。（如果一直没有出现上图的信息，那可能是并发数太多了，把并发数改少点试试，例如只并发20，不要一下子就并发1000）



**GUI****模式：**



<img class="shadow" src="/img/in-post/pylot_gui.png" width="1200">

​    测试结束后，会在pylot的文件目录里生成一个“results”的文件夹，还生成一个results.html的文件，这个文件记录了详细的测试数据。我们可以进入results的目录，打开这个文件，看看我的测试结果：

<img class="shadow" src="/img/in-post/pylot_result_files.png" width="1200">



点击目录中的results文件，即可打开测试结果：

<img class="shadow" src="/img/in-post/pylot_result_html.png" width="1200">

 

 

## **参数详细说明**

　　Pylot有很多参数，介绍一下：

| -a, --agents=NUM_AGENTS     | 设置同时访问用户数量                                 |
| --------------------------- | ---------------------------------------------------- |
| -d, --duration=DURATION     | 设置总测试时间（秒）                                 |
| -r, --rampup=RAMPUP         | 设置提升量（秒）                                     |
| -i, --interval=INTERVAL     | 设置访问间隔（毫秒）                                 |
| -x, --xmlfile=TEST_CASE_XML | 设置要使用的xml文件，默认testcase.xml                |
| -o, --output_dir=PATH       | 设置输出文件路径                                     |
| -n, --name=TESTNAME         | 设置测试名称                                         |
| -l, --log_msgs              | 设置是否需要日志信息                                 |
| -b, --blocking              | 设置是否开启锁定模式，如果开启会锁定输出直到测试结束 |
| -g, --gui                   | 设置是否使用图形界面                                 |
| -p, --port=PORT             | 设置xml-rpc监听的端口                                |

 

  

## **参考文档**

http://www.webkaka.com/blog/archives/windows-pylot-matplotlib-webstress-test.html



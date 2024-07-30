---
layout:     post
title:      "Fiddler使用总结"
subtitle:   "Fiddler use guide"
date:       2015-08-20
author:     "Gavin Wang"
catalog:    true
categories:
    - [Fiddler]
tags:
    - Fiddler
---


# Fiddler命令行

## 快捷键

### Alt+Q 快速将焦点设置到命令行中

<img class="shadow" src="/img/in-post/fiddler_alter_q.png" width="1200">

 

### Ctrl+I 将当前选中的session中的URL插入到命令行中

<img class="shadow" src="/img/in-post/fiddler_ctrl_i.png" width="1200">

 

### Alt+Ctrl+F 激活已运行的fiddler窗口

Fiddler处于后台运行中，使用如上键，可最大化fiddler窗口

 


## 命令行

### ?sometext

功能说明：在已有的session中，将URL中包含sometext的session项高亮

 

### >size 或 <size

功能说明：在当前session中，高亮选择response的body大小大于或小于size指定的值，单位为byte

示例：

\>3000，将response中body值大于1000bytes的sessions高亮

<2K，将response的body值小于2K的sessions高亮

 

### =status

功能说明：在当前所有的sessions中，将result列中等于status值的session项高亮，即将与status值相同的http状态码高亮

示例：

 =401，即将http状态码为401的sessions高亮

 

### =method

功能说明：在当前所有的sessions中，将request请求中的http method与命令行中method值相同的session项高亮

示例：

 =post，即将method为POST的session项高亮

 

### @host

功能说明：在当前所有的sessions中，将request请求中host项中包含命令行@内容的session项高亮

示例：

 @baidu.com，即会将app.baidu.com、[www.baidu.com、baike.baidu.com等sessions](http://www.baidu.com、baike.baidu.com等sessions)项高亮

 

### boldsometext

功能说明：将新记录的sessions，如果URL中包含sometext内容，就将该sessions的字体加粗。如果要取消加粗，直接输入bold即可。

示例：

 bold baidu.com，即将新记录的sessions中URL内容包含有baidu.com的字样的session字体加粗

 

### bpaftersometext

功能说明：在URL中包含sometext内容的sessions的response位置设置断点，即该sessions的After Response位置。使用这个命令后，会将之前设置的策略清楚。取消该拦截项，直接输入bpafter即可.

示例：

bpafter /q，拦截所有URL中包含有/q内容的response返回值

 

### bpssometext

功能说明：拦截所有状态码与sometext值相同的sessions的Response返回值。使用这个命令后，会将之前设置的策略清除。取消该拦截策略，直接输入bps即可。

示例：

 bps 404，将所有返回404请求的response全部拦截

 

### bpvsometext 或 bpmsometext

功能说明：拦截所有发送的http method与sometext内容相同的sessions网络请求。使用这个命令后，会将之前设置的策略清除。取消拦截策略，直接输入bpv或bpm即可。

示例：

bpv POST，会拦截所有以POST方法发送的网络请求。

 

### bpusometext

功能说明：在URL中包含sometext内容的sessions的Request位置设置断点，即该sessions的before request位置。使用这个命令后，会将之前设置的策略清除。取消该拦截策略，直接输入bpu即可。

示例：

bpu /a.sext，拦截所有URL中包含 /a.sext内容的Request请求。

 

### cls 或clear

功能说明：清除列表中所有的session，功能与Ctrl+X相同

示例：

<img class="shadow" src="/img/in-post/fiddler_cls.png" width="1200">

 

### dump

功能说明：将当期获取到的所有的sessions保存成zip文件，并保存到系统我的文档中的\Fiddler2\Captures文件夹中，命名为dump.saz

 

### g 或 go

功能说明：回复所有被设置断点的session

 

### help

功能说明：打开QuickExec的帮助页面，该页面详细介绍Fiddler的使用

 

### hid

功能说明：将Fiddler隐藏到系统状态栏中




### urlreplace

功能说明：自动将任意URL中的内容sometext1替换成sometext2.使用这个命令后，会清除之前设置的策略。取消该拦截策略，直接输入urlreplace即可。

示例：

urlreplacebaidugoogle，即如果发生的网络请求为[www.baidu.com](http://www.baidu.com)，通过该策略会自动更改为[www.gogle.cn](http://www.gogle.cn)，并发送出去。

 

### start

功能说明：将Fiddler设置为系统代理

 

### stop

功能说明：取消Fiddler为系统代理

 

### show

功能说明：可以将已被隐藏的Fiddler置前。执行该命令需要使用到ExecAction.exe这个程序，该程序的位置为Fiddler的安装目录

示例：

ExecAction.exe show

 

### selectsometext

功能说明：在当前所有sessions中，将header的Contetnt-Type字段包含sometext内容的sessions高亮、可用于选择文件格式等。

示例：

slectcss，即将所有网络请求中Content-Type字段包含css的sessions高亮

 

### selectHeaderOrFlagsometext

功能说明：高亮SessionFlag或header中包含指定sometext内容的session

示例：

例1、select text abc，即在名为text的SessionFlag中，高亮内容为abc的session

例2、select @Response.Set-Cookie baidu.com，即在所有session的Response中，查找name为Set-Cookie值为baidu.com的Session，并高亮

例3、select @Request.X-Requested-With XMLHttpRequest中，即在所有的session的Request中，查找name为.X-Requested-With值为XMLHttpRequest的Session，并高亮

例4、select @Request.X-Requested-With \*，即在所有session的Request中，查找name为X-Requested-With且值为任意值的session，并高亮。

 

### allbutsometext或 keeponlysometext

功能说明：隐藏所有除Content-Type内容包含sometext的session

示例：

allbut xml，隐藏所有Content-Type为非xml的session，即只展示Content-Type为xml的session，其他session被隐藏

 

### quit

功能说明：关闭Fiddler

 

### !dnssometext 或 !nsloolupsometext

功能说明：进行目录域名为sometext的DNS查找，并在LOG选项卡上将结果输出

示例：

  !dnswww.baidu.com，即将www.baidu.com对应的IP地址解析并输出

 

### !listen PORT [CERTHOSTNAME]

功能说明：在另外一个端口增设一个监听器，可选安全的HTTPS证

示例：

 !listen 8080，即可以同时截获通过8080端口的网络请求。

 

 

 

# Fiddler实践

## 问题1、界面增加IP地址

测试过程中发现访问的数据不正确，怀疑是修改的host没有生效导致的。但无法查看手机端访问该数据页面的IP，所以一直无法确认该问题

 

1. 运行fiddler，菜单，Rules->Customize Rules…或者点击右侧tab

“FiddlerScript”

2. Ctrl+F查找“static function Main()”字符串，然后添加下面这行代码：

FiddlerObject.UI.lvSessions.AddBoundColumn("ServerIP", 120, "X-HostIP");

 

3. 保存CustomRules.js或者点击“Save Script”按钮，如下所示：


```shell
static function Main() {

var today: Date = new Date();

FiddlerObject.StatusText = " CustomRules.js was loaded at: " + today;

FiddlerObject.UI.lvSessions.AddBoundColumn("ServerIP", 120, "X-HostIP");
```


4. 查看fiddler，此时IP会添加到所有数据的最后一列，拖到滚动条，即可看到，如下所示：

<img class="shadow" src="/img/in-post/fiddler_ip.png" width="1200">

 

## 问题2、修改端口

测试过程中，手机借来借去是常有的事，也行你刚在一台手机上将自己的IP添加上，过一会这台手机就被某某某拿走了，不一会儿，你的Fiddler上面多了很多会话，不巧其中有个URL的参数id为空。Bug？！然而，重复操作N遍都没法重现。仔细查看请求后发现不是自己使用的手机。如何摆脱曾经的小尾巴，请看下文

在Toolsà Fiddler options --> Connections，如下图所示：

<img class="shadow" src="/img/in-post/fiddler_options.png" width="1200">


Fiddler默认端口号是8888，为了避免这种情况对自己的干扰，在找不到北某某某的拿走的手机时，可以将这个端口修改为其他的，例如：8889，重启Fiddler，再在自己使用的手机上做相应的修改即可。

 

## 问题3、Fiddler的过滤功能

在PC上打开Fiddler用于查看手机端的请求，但总是被PC上来来往往的请求所干扰。如何只查看android上的请求，而不被干扰呢？

Fiddler有强大的filter，通过filter能够只查看自己关注的请求。但是呢，有一些去服务器下载的请求，由于服务器有好多，添加过滤器有可能过滤掉本来想看的内容，例如：某个banner展示成功的前提是：图片资源下载成功。当我们在测试过程中看到banner图显示不出来，到底是banner图的功能有问题呢？还是服务器的问题呢？因此，作为一名认真、负责任的测试同学，我们想要准确定位bug的原因，就需要关注这个过程中发生了什么，而不能简单的跟开发同学说:banner图显示不出来了。

So，这种过滤如何实现呢？正确的处理方式是：

点击Fiddler左下角的Capturing，可以控制是否把Fiddler注册为PC代理，当左下角出现”Capturing”时，Capture Traffic是打开的，此时的IE的Internet选项连接局域网（LAN）设置中的代理服务器是勾选的；否则不勾选，如下图所示：

<img class="shadow" src="/img/in-post/fiddler_internet_set.png" width="1200">

 

## 问题4、生效修改的hosts文件

测试过程中需要访问测试服务器，打开Fiddler，在PC的etc目录下修改了hosts文件却不能不生效，为什么呢？

当Fiddler已经建立会话时，任何修改hosts的行为都不会被Fiddler注意到。可以通过Fiddler的Tools à HOSTS 导入本地的hosts文件。需要指定测试服务器的时候，勾选“Enable remapping of request for one host to a different host or IP, overredding DNS”，否则去掉勾选。

 

## 问题5、测试过程中如何模拟多用户网络场景

这里介绍下模拟低速网络情况。

Fiddler是一个代理，它提供了客户端请求和服务器响应前的回调接口，我们可以在这些接口里自定义一些逻辑。Fiddler的模拟限速就是在客户端请求前来定义限速的逻辑，此逻辑是通过延迟发送数据或接收的数据的时间来限制网络的下载速度和上传速度，从而达到限速的效果。

Fiddler提供了一个功能，可以方便的模拟低速网络环境。方法：Rules à Performances à Simulate Modem Speeds，如图所示：

<img class="shadow" src="/img/in-post/fiddler_rule.png" width="1200">

也可自定义低速网络：

（1）打开Fiddler，Rules --> Customize Rules…，或者在Fiddler中使用Ctrl+R快捷键

（2）搜索关键字“m_SimulateModem”

（3）然后根据自己需要，修改上传与下载速度

<img class="shadow" src="/img/in-post/fiddler_speed.png" width="1200">

 

说明如下：

oSession["request-trickle-delay"] = "300";

\#每上传1K，延迟300ms

oSession["response-trickle-delay"] = "150";

\#没下载1K，延迟150ms

（4）保存修改后，勾选之前的 Simulate Modem Speed 选项。

 

## 问题6、Fiddler保存会话的response内容为乱码

右键点击会话选择“save à Response à Response Body”，保存的文件打开后里面出现乱码。

这是因为Fiddler为了提高性能，将会话的response压缩后进行了传输，查看Transformer的选项卡，如下图所示：

<img class="shadow" src="/img/in-post/fiddler_transfer.png" width="1200">

是否可看到GZIP Encoding处于选中状态？想要正常查看被压缩的数据，需要选择成No Compression，但是出现乱码的情况下，该处是不能点击的，如何解决呢？

方法1:

如果想在会话处理过程中进行Decode，点击Fiddler界面上Decode 按钮，如下图所示：

<img class="shadow" src="/img/in-post/fiddler_decode.png" width="1200">

则会对所有的会话进行decode，这样保存的response就能正常显示了，需要注意：点击“Decode”之后，需要重启Fiddler才能生效。

 

方法2

如果想对所有会话处理之后再进行No Compression（解压缩），可以选择多个会话，右键选择“Decode Selected Sessions”，另外，在会话的response区域看到的却是乱码，上面有黄条提示“Response is encoded and require decoding before inspection.Click here to transform”,杜继英的Transform勾选情况如下图所示：

<img class="shadow" src="/img/in-post/fiddler_garbled.png" width="1200">

处理方法：这种情况下，只要按照提示，点击黄条即可对当前的会话进行decode，但是这样处理只针对当前的会话，是一次性的效果，如果不担心传输性能的话，可以直接使用方法1。

 

## 问题7、模拟http请求


## 模拟http POST请求

对于post请求，需要输入Reuqest Body。而Request Body 默认情况是隐藏起来的。按下面步骤点击显示出Reuqest Body。

1、点击Options

<img class="shadow" src="/img/in-post/fiddler_composer.png" width="1200">

 

2、点击Tear off，如下图

<img class="shadow" src="/img/in-post/fiddler_tearoff.png" width="1200">


点击执行，就可以模拟post请求了。

上图中的消息头，可从别的地方拷贝过来，如下图所示：

<img class="shadow" src="/img/in-post/fiddler_inspectors.png" width="1200">



## 模拟http get操作


下拉框中选择GET，输入请求的地址，输入Request Headers。Request Headers是键值对的格式，用：隔开。点击执行。

<img class="shadow" src="/img/in-post/fiddler_composer2.png" width="1200">

查看get操作获取到的结果：

<img class="shadow" src="/img/in-post/fiddler_get_result.png" width="1200">


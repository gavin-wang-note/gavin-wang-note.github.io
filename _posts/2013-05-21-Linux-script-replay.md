---
layout:     post
title:      "Linux录屏与回放"
subtitle:   "Linux srcipt&scriptreplay"
date:       2013-05-21
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - Linux
---


# 录制与回放终端会话

当你需要为别人在终端上演示某些操作，或者是需要准备一个命令行教程时，通常要一边手动输入命令一边进行演示，或者录制一段演示视频进行播放。如果我们将输入命令后发生的一切，安装一定的先后顺序记录下来，再进行回访，从而使得观众好像身临其境一样，这个想法听起来如何？
命令的输出会显示在终端上，一直到回访内容播放完毕，所有的这些，都可以使用script和scriptreplay命令来实现。


# 预备知识
script 和 scriptreplay命令在绝大多数GNU/Linux发行版本上都可以找到。把终端会话记录到一个文件，可以通过录制终端会话来制作命令行技巧视频，也可以与他人分享会话记录文件，共同研究如何使用这些命令行完成某项任务。

# 实战演练



## script常用选项

更详细的说明可以man script来查看



| 选项                   | 描述                                                         |
| ---------------------- | ------------------------------------------------------------ |
| -a, - -append          | 输出录制的文件，在现有内容上追加新的内容                     |
| -c, - -command         | 直接执行命令，而非是交互式的shell                            |
| -r, - -return          | 返回子shell的退出码                                          |
| -f, - -flush           | 每次操作后都立即刷新缓存。 如果不设置这个选项，则不会实时写入文件 |
| -q, - -quiet           | 可以使script命令以静默模式运行，不显示script启动和exit的命令，用户可以完全察觉不到在录屏 |
| -t, - -timing[=<file>] | 输出录制的时间数据，输出到屏幕或者存到指定文件中，回放的时候用到 |
| -V, - -version         | 显示版本并退出                                               |
| -h, - -help            | 显示使用说明并退出                                           |





## scriptreplay


| 选项                   | 描述                                                         |
| ---------------------- | ------------------------------------------------------------ |
| -t, - -timing file          | 包含记录时序的文件                     |
| -s, - -typescript file | 包含脚本终端输出的文件               |
| -d, –divisor number    | 加速播放速度倍数（可以是小数：放慢） |
| -V, - -version         | 显示版本并退出                       |
| -h, - -help            | 显示使用说明并退出                   |



开始录制终端会话：

```shell
root@host245:~/tmp# script -t 2> timeing.log -a output.session
Script started, file is output.session
root@host245:~/tmp# ls -l
total 4
-rw-r--r-- 1 root root  0 Nov 26 11:38 output.session
-rw-r--r-- 1 root root 78 Nov 26 11:38 timeing.log
root@host245:~/tmp# cd
root@host245:~# cd -
/root/tmp
root@host245:~/tmp# exit
exit
Script done, file is output.session
```

两个文件（timeing.log 和 output.session）被当做script命令的参数，其中timeing.log用于存储时序信息，描述每一个指令在何时运行；另外一个文件output.session用于存储命令输出。

-t选项用于将时序数据导入stderr； 2>则用于将stedrr重定向到timing.log文件。

借助这两个文件：timeing.log（存储时序信息） 和 output.session（存储命令输入信息），我们可以按照下面的方法回放命令的执行过程：

```shell
root@host245:~/tmp# scriptreplay timeing.log output.session 
```



# 工作原理

通常我们会录制桌面环境视频来作为教程使用，不过要注意的是，视频需要更大的存储空间，而终端脚本文件仅仅是文本文件，大小不过KB级别。

script命令同样可以用于建立可在多个用户之间进行广播的视频会话，这是件很有意思的事情，来看看它是如何实现的吧。

打开两个终端，Terminal1 和 Terminal2

在Terminal1中输入如下命令：

```shell
root@host244:~# mkfifo scriptfifo

```



在Terminal2中输入如下命令：

```shell
root@host244:~# cat scriptfifo
```



返回Terminal1，输入以下命令：

```shell
root@host244:~# script -f scriptfifo
root@host244:~# some other linux command, such as ls, cd, mkdir and so on
```



如果需要结束会话，输入exit并按回车，会得到如下信息：

```Script done, file is scriptfifo ```



现在，Terminal1就成了广播员，Terminal2则成为了听众。不管你在Terminal1中输入什么内容，都会在Terminal2或者使用了下列命令的任何终端中实时播放：

```cat scriptfifo```

当你需要为计算机实验室或者Internet上的用户群演示教程时，不妨考虑这个方法，它在节省带宽的同时，也提供了实体试验。


# 另外一个共享屏幕的方法

可以使用tmux，将tmux的session id告知大家，所有人都在Terminal中切换到这个tmux session，一个人的任何输入输出操作， 其他在这个会话中的人都可以看到。缺点是：在这个tmux session的人，都有执行命令的权限。



---
layout:     post
title:      "wc统计为何少了一行"
subtitle:   "wc lost one line"
date:       2020-06-29
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# 概述

使用wc统计文件时，发现文件数量总是少一行，原因何在？

# 实践

## 准备工作

分布准备两个文件，一个是linux平台下通过vi写入的，一个文件是在windows平台，通过记事本写入的，内容如下：


```
root@node244:~/test# cat wins.txt 
1
2
3
4
5
6
7
8
9
0root@node244:~/test# cat linux.txt 
1
2
3
4
5
6
7
8
9
0
root@node244:~/test#
```

注意这里的区别:

<img class="shadow" src="/img/in-post/end_of_file_content.png" height="300px" width="300px">


## 统计效果

```
root@node244:~/test# wc -l wins.txt 
9 wins.txt
root@node244:~/test# wc -l linux.txt 
10 linux.txt
root@node244:~/test# 
``` 

明明文件记录是10条，为何windows平台生成的文件，统计少了？

## 原因分析

wc -l 是按\n作为行结束符统计行数，所以最后一行如果没有\n的话会统计丢失。

```
root@node244:~/test# cat linux.txt | od -c
0000000   1  \n   2  \n   3  \n   4  \n   5  \n   6  \n   7  \n   8  \n
0000020   9  \n   0  \n
0000024
root@node244:~/test# cat wins.txt | od -c
0000000   1  \r  \n   2  \r  \n   3  \r  \n   4  \r  \n   5  \r  \n   6
0000020  \r  \n   7  \r  \n   8  \r  \n   9  \r  \n   0
0000034
root@node244:~/test# 
```

两者的区别如下:

<img class="shadow" src="/img/in-post/end_of_file.png" width="1200">


通过od -c指令，可以看到，windows生成的文件，最后一笔记录后面是没有换行符的，而linux是有的，同时也发现，linux只有\n，这表示换行符，而windows，\r \n，这表示回车换行符，两者是有区别的，即EOF不一样，Linux占用2bytes，而windows占用4bytes，下图是通过UE这个文本编辑器，分别对Linux和windows下产生的文件，转换成16进制看到的效果:

<img class="shadow" src="/img/in-post/HX_diff.png" width="2400">



# 解决方法

Linux平台上，dos2unix一把 windows产生的文件即可。





---
layout:     post
title:      "替换文件中空格"
subtitle:   "Remove space with awk/tr/sed/grep"
date:       2014-06-06
author:     "Gavin"
catalog:    true
tags:
    - awk
    - sed
    - tr
---


# 概述
有时候一些目录下的文件有一些空格，想对这些文件中的空格进行批量删除，该如何做呢？
主要使用awk, tr，sed之类的命令，进行替换操作。

# 目录下文件的整体去除空格

使用shell脚本进行批量处理，示例如下：

```
#!/usr/bin/bash

ls|while read i;do  

    mv "$i" $(echo $i|tr -d ' ') 2>/dev/null  

done 
```

# 单个文件的空格处理--删除所有空格
方法1：
```sed 's/\s//g' input.txt | tr -d '\n' ```

方法2：Perl一行命令

```perl -CS -pe 's/\p{Space}//g' < input > output ```

方法3：
```tr -d ' \t\n\r\f' <inputFile >outputFile ```

方法4:
```sed 's/\s//g'|tr -d '\n' ```

方法5：
```sed s/[[:space:]]//g ```



示例：


比如下面的文件a.txt，内容如下：

```
root@cvm02:~/test# cat a.txt 
1

2
3  4
5
6
7  8
9
```




```root@cvm02:~/test# tr -d ' ' <a.txt  >b.txt```


查看替换后的效果：
```
root@cvm02:~/test# cat b.txt 
1

2
34
5
6
78
9
```


# 删除行首空格


代码如下:

```
sed 's/^[ \t]*//g'
```

说明：

* 第一个/的左边是s表示替换，即将空格替换为空
  * 第一个/的右边是表示后面的以xx开头
  * 中括号表示“或”，空格或tab中的任意一种。这是正则表达式的规范
  * 中括号右边是*，表示一个或多个
* 第二个和第三个\中间没有东西，表示空
* g表示替换原来buffer（缓冲区）中的，sed在处理字符串的时候并不对源文件进行直接处理，先创建一个buffer，但是加g表示对原buffer进行替换
* 整体的意思是：用空字符去替换一个或多个用空格或tab开头的本体字符串



# 删除行末空格


代码如下:

```
sed 's/[ \t]*$//g'
```


和上面稍微有些不同是前面删除了^符，在后面加上了美元符，这表示以xx结尾的字符串为对象。




# awk去除空格

代码如下:



```
awk '{gsub(/^ +| +$/,"",$0);printf $0}'
```



效果：

```
root@cvm02:~/test# cat a.txt | awk '{gsub(/^ +| +$/,"",$0);printf $0}'
123  4567  89root@cvm02:~/test# 
```




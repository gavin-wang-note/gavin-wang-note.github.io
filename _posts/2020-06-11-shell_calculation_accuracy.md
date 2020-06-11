---
layout:     post
title:      "shell计算精度"
subtitle:   "shell script calculation accuracy"
date:       2020-06-11
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - shell
---

# 概述

为何要写这篇问题，因为在上篇文章 <a href="https://gavin-wang-note.github.io/2020/06/10/stastic_ES_write_speed_by_shell_script/" target="_blank">stastic ES write speed by shell script</a>有使用shell去尝试统计ES的写入速度，需要精确到毫秒级别的时间差，但是尝试了expr，let，发现不行，而是awk却可以，所以本文汇总一下，以bash为例，shell中的计算精度问题。


# 实践

## bc

bc是比较常用的Linux中计算器了，简单方便，而且是支持浮点的。一般系统不自带，需要额外安装。


```
root@code80:~# echo 1+2 | bc
3
root@code80:~# echo 1.1*6 | bc
6.6
root@code80:~# echo 5/3 | bc
1
root@code80:~# echo 5/3.0 | bc
1
root@code80:~# echo 5.0/3 | bc
1
root@code80:~# echo 5.1/3 | bc
1
root@code80:~# echo "scale=2;5/3" | bc
1.66
root@code80:~# 
root@code80:~# echo "scale=2;1/2" | bc
.50
root@code80:~# echo "scale=4;1/2" | bc
.5000
root@code80:~# 
```

这里有个问题，如果整数为0，这个整数不会显示，直接显示小数点，解决方法如下:

```
root@code80:~# echo "print 0;scale=2;1/2" | bc
0.50
root@code80:~#
```

## expr

不支持浮点计算，即不支持小数，所以也常被用来判断变量内容或者结果是不是非0整数（expr 0的echo $?不是0）。

另外，expr 后面的两个参数与运算符之间，一定要含有空格:

```
root@code80:~# expr 1+2
1+2
root@code80:~# expr 1 + 2
3
root@code80:~# expr 5/3
5/3
root@code80:~# expr 5 / 3
1
root@code80:~# expr 99 / 3.0
expr: non-integer argument
root@code80:~# expr 99 / 3
33
root@code80:~# expr 0
0
root@code80:~# echo $?
1
root@code80:~# 
```

## $(())

此方法不支持浮点计算。

```
root@code80:~# echo $((1+2.0))
bash: 1+2.0: syntax error: invalid arithmetic operator (error token is ".0")
root@code80:~# echo $((1+2))
3
root@code80:~# echo $((10/2))
5
root@code80:~# echo $((10.1/2))
bash: 10.1/2: syntax error: invalid arithmetic operator (error token is ".1/2")
root@code80:~#
```

## let

不仅不支持浮点计算，而且还只能赋值，不能直接输出。

```
root@code80:~# let a=1+2
root@code80:~# echo $a
3
root@code80:~# let b=10/5
root@code80:~# echo $b
2
root@code80:~# let b=10/3
root@code80:~# echo $b
3
root@code80:~# let c=1.1*2
bash: let: c=1.1*2: syntax error: invalid arithmetic operator (error token is ".1*2")
root@code80:~# 
```

上面的方法，bc一般系统不带需要自行安装，不是很方便，万一系统不联网，又没有安装包，没法使用；其他的几个方法，都不支持浮点数，是否有其他方法支持浮点数的？答案是肯定的，继续往下看。


# 计算浮点数

这里，使用awk获浮点数。

```
root@code80:~# echo | awk "{print 10.2/2}"
5.1
root@code80:~# echo | awk "{print 10*2.1}"
21
root@code80:~# echo | awk "{print 10.2*2.1}"
21.42
root@code80:~# echo | awk "{print 10.2/2}"
5.1
root@code80:~# echo | awk "{print 10.2*2.1}"
21.42
root@code80:~# echo | awk "{print 10.2+2.1}"
12.3
root@code80:~# echo | awk "{print 10.2-2.1}"
8.1
root@code80:~# echo | awk '{print 10.2-2.1}'
8.1
root@code80:~# echo | awk '{print 10.2+2.1}'
12.3
root@code80:~# echo | awk '{print 10.2*2.1}'
21.42
root@code80:~# echo | awk '{print 10.2/2.1}'
4.85714
root@code80:~#
```


将数值参数化试试：

```
root@code80:~# pam1=10.2
root@code80:~# pam2=2.1
root@code80:~# pam3=2
root@code80:~# echo | awk '{print $pam1/$pam2}'
awk: cmd. line:1: (FILENAME=- FNR=1) fatal: division by zero attempted
root@code80:~# echo | awk "{print $pam1/$pam2}"
4.85714
root@code80:~# echo | awk "{print $pam1*$pam2}"
21.42
root@code80:~# echo | awk "{print $pam1-$pam2}"
8.1
root@code80:~# echo | awk "{print $pam1-$pam2*$pam3}"
6
root@code80:~# echo | awk "{print ($pam1-$pam2)*$pam3}"
16.2
root@code80:~#
```


说明：

这里awk后的print，在不使用参数/变量情况下，使用单引号和双引号都可以，推荐使用双引号，养成习惯。

这里小数点后的位数不受控制，比如本文示例中计算出来的结果4.85714，小数点后有5位，如果只想保留指定位数的小数点，加上printf：

```
root@code80:~# echo | awk '{print 10/3}' 
3.33333
root@code80:~# echo | awk '{printf ("%.2f\n",10/3)}' 
3.33
root@code80:~# 
```

看看参数化后的执行效果:

```
root@code80:~# echo | awk "{printf ("%.2f\n",$pam1/$pam2)}"
awk: cmd. line:1: {printf (%.2fn,10/3)}
awk: cmd. line:1:          ^ syntax error
root@code80:~# 
root@code80:~# echo | awk '{printf ("%.2f\n",$pam1/$pam2)}'
awk: cmd. line:1: (FILENAME=- FNR=1) fatal: division by zero attempted
```

报错了，这种情况，建议先在前面的echo中将需要使用的变量输出出来，再进行调用。

```
root@code80:~# echo $pam1 $pam2 | awk '{{printf ("%.2f\n", $1/$2)}}'
3.33
root@code80:~# 
```

说明：

上面的命令示例中，保留2位小数，printf默认是保留6位。



如果碰到科学计数类型的爆大数字，会出问题：

```

t@code80:~# echo "5.9637e+12/100" | bc
(standard_in) 1: syntax error
root@code80:~# 
```

解决方法如下：

```
root@code80:~# echo "5.9637e+12/100" | awk '{printf ("%.0f\n",$1)}'
5963700000000
root@code80:~# echo "5.9637e+12/100" | awk '{printf ("%.2f\n",$1)}'
5963700000000.00
root@code80:~# 
```

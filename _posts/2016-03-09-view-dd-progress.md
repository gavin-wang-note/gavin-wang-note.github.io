---
layout:     post
title:      "查看dd进度"
subtitle:   "view dd progress"
date:       2016-03-09
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - dd 
    - pv 
---

# 概述

dd是一个神奇的命令，可以将硬盘驱动器复制到另一个硬盘驱动器，完全归零硬盘驱动器等。但是，一旦启动 dd 命令，就没法显示它的进度，只是坐在光标处，直到命令最终完成。那么如何监控dd的进展呢？本文以ubuntu环境为例进行阐述。


# 查看dd进度

新status选项添加到dd（GNU Coreutils 8.24+）
dd在GNU Coreutils 8.24+（Ubuntu 16.04及更高版本）中，有一个新status选项可以显示进度：

示例：

```dd if=/dev/urandom of=/dev/null status=progress ```

输出信息：

```
462858752 bytes (463 MB, 441 MiB) copied, 38 s, 12,2 MB/s
```


# 使用kill获取进度

```dd if=/dev/zero of=/tmp/zero.img bs=10M count=100000 ```

想要查看上面的dd命令的执行进度，可以使用下面几种方法：

比如：每5秒输出dd的进度

方法一：

```watch -n 5 pkill -USR1 ^dd$ ```

方法二：

```watch -n 5 killall -USR1 dd ```
	
方法三：

```while killall -USR1 dd; do sleep 5; done ```

方法四：

```while (ps auxww |grep " dd " |grep -v grep |awk '{print $2}' |while read pid; do kill -USR1 $pid; done) ; do sleep 5; done ```

方法五：

```dd if=/path/to/bigimage of=/path/to/newimage conv=sparse bs=262144 & bgid=$!; while true; do sleep 1; kill -USR1 $bgid || break; sleep 4; done ```

上面这个命令，糅合了具体的dd命令，然后kill它来显示进度

<img class="shadow" src="/img/in-post/dd_output_progress.png" width="1200">


# pv显示进度

题外话：

pv不仅仅有显示进度的功能，还有结合dd来限制dd读写速度， e.g:

```pv --rate-limit 2M -q -cN source < /dev/zero |dd of=off_file bs=1M count=1024 iflag=fullblock```

非本文要阐述的内容，有兴趣的可以man pv查看使用手册。

如果没有pv，执行下列命令进行安装

```apt-get install pv ```

## 创建bash包装器，使用pv来显示进度

在.bashrc中增加包装器,将下面内容放入.bashrc文件

```
dd()
{
    local dd=$(which dd); [ "$dd" ] || {
        echo "'dd' is not installed!" >&2
        return 1
    }

    local pv=$(which pv); [ "$pv" ] || {
        echo "'pv' is not installed!" >&2
        "$dd" "$@"
        return $?
    }

    local arg arg2 infile
    local -a args
    for arg in "$@"
    do
        arg2=${arg#if=}
        if [ "$arg2" != "$arg" ]
        then
            infile=$arg2
        else
            args[${#args[@]}]=$arg
        fi
    done

    "$pv" -tpreb "$infile" | "$dd" "${args[@]}"
}
```

source一下.bashrc

之后再来使用dd命令，就可以看到进度了~


## 直接命令行用pv显示进度


示例：

```dd if=/dev/urandom | pv | dd of=/dev/null ```

输出：

```44.2MB 0:00:04 [11.4MB/s] [         <=>                                ] ```

如果想要时间估算，可以使用 --size 指定近似大小：

```dd if=/dev/urandom | pv -s 2G| dd of=/dev/null ```

<img class="shadow" src="/img/in-post/pv_size.png" width="1200">


示例：

写一个文件，并显示进度：

```pv -cN source < /dev/zero | dd of=1g bs=100k count=10240 ```

输出如下：

```
root@host245:~/tmp# pv -cN source < /dev/zero | dd of=1g bs=100k count=10240
   source:  960MB 0:00:01 [ 627MB/s] [         <=>                                                                                                                                                                                                                           ]
7680+2560 records in
7680+2560 records out
1006632960 bytes (1.0 GB) copied, 4.18198 s, 241 MB/s
root@host245:~/tmp# 
```


## 使用pv配合dialog还可以显示进度条对话框：

需要事先安装dialog

```apt-get install dialog ```


```(pv -n /dev/sda | dd of=/dev/zero bs=128M) 2>&1 | dialog --gauge "dd process bar" 10 70 0 ```

<img class="shadow" src="/img/in-post/pv_dialog.png" width="1200">


示例：

克隆磁盘驱动器：

```(pv -n /dev/sda | dd of=/dev/sdh bs=128M conv=notrunc,noerror) 2>&1 | dialog --gauge "Running dd command (cloning), please wait..." 10 70 0 ```


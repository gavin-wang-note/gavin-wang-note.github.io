---
layout:     post
title:      ""
subtitle:   ""
date:       2019-09-09
author:     "Gavin"
catalog:    true
tags:
    - Linux
---

# 概述


本文概述Linux SWAP 有哪些进程在使用，以及如何关闭/开启SWAP。


# 实践


## 查看哪些进程占用swap分区

参考链接： ```https://blog.csdn.net/m0_37886429/article/details/73826868```

```
for i in $(ls /proc | grep "^[0-9]" | awk '$0>100'); do awk '/Swap:/{a=a+$2}END{print '"$i"',a/1024"M"}' /proc/$i/smaps;done| sort -k2nr | head
```

然后根据ps aux | grep pid进行查看是哪个服务占用了swap

一个更详细的命令如下：

{% raw %}```
#!/bin/bash  
# Get current swap usage for all running processes  
# writted by xly  

function getswap {

   SUM=0
   OVERALL=0
   for DIR in `find /proc/ -maxdepth 1 -type d | egrep "^/proc/[0-9]"` ; do
       PID=`echo $DIR | cut -d / -f 3`
           PROGNAME=`ps -p $PID -o comm --no-headers`
           for SWAP in `grep Swap $DIR/smaps 2>/dev/null| awk '{ print $2 }'`
               do
                   let SUM=$SUM+$SWAP
               done
               echo "PID=$PID - Swap used: $SUM - ($PROGNAME )"
               let OVERALL=$OVERALL+$SUM
               SUM=0
    done
    echo "Overall swap used: $OVERALL"
}  

getswap
#getswap|egrep -v "Swap used: 0" 
``` {% endraw %}

# 硬释放swap空间

参考: ```https://blog.51cto.com/9237101/1921268```

```
（1）执行sync
（2）echo 3 > /proc/sys/vm/drop_caches
 (3) swapoff -a
 (4) swapon -a
```

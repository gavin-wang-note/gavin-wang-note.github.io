---
layout:     post
title:      "快速清除rbd image"
subtitle:   "Fast to delete rbd image"
date:       2023-04-21
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# 概述

当集群里出现一个较大的rbd image时，如何快速清理掉它并释放空间，已经存在文章 ：https://cephnotes.ksperis.com/blog/2014/07/04/remove-big-rbd-image/ 做了介绍。
并且对不同的方法做了分析，这里先把结论说下:

| rbd类型    | rbd rm 方法                        | rados -p rm方法                                            |
| ------- | ------------------------- | --------------------------------------------------- |
|未填充很多|	慢|	快|
|已填充很多|	快|	慢 |

在rbd进行删除的时候，即使内部没有对象数据，也一样需要一个个对象去发请求，即使对象不存在，这个可以开日志看到:
在/etc/ceph/ceph.conf中添加

```
[client]
debug_ms=1
log_file=/var/log/ceph/rados.log
```

# 实践

dd写，bs=1M,写了40G的数据：
```
root@pytest-83-19:~# dd if=/dev/zero of=/dev/rbd0 bs=1M count=40960
40960+0 records in
40960+0 records out
42949672960 bytes (43 GB, 40 GiB) copied, 261.264 s, 164 MB/s
```

## rbd image 信息


```
root@pytest-83-19:~# rbd ls
889795de-fafb-4fca-9bf1-9b984e6124d2.img
root@pytest-83-19:~# rbd info rbd/889795de-fafb-4fca-9bf1-9b984e6124d2.img
rbd image '889795de-fafb-4fca-9bf1-9b984e6124d2.img':
	size 600GiB in 614400 objects
	order 20 (1MiB objects)
	used objects: 0
	block_name_prefix: rbd_data.30dc419495cff
	format: 2
	features: layering
	flags: 
	create_timestamp: Fri Apr 21 14:26:48 2023
root@pytest-83-19:~#


```

## 原始的快速删除方法


```
root@pytest-83-19:~# time rados -p rbd ls | grep '^rbd_data.30dc419495cff' | xargs -n 200  rados -p rbd rm

real	2m5.564s
user	0m46.126s
sys	0m4.718s
root@pytest-83-19:~# 
```




## 开启多进程删除的方法

这个比上面那种方法好的是：

* 可以显示当前删除的进度
* 可以指定删除的进程并发数
* 可以显示当时正在删除的对象
* 可以增加一个中断时间降低负载

首先获取一个需要快速删除的rbd的列表:

### 获取prifix

```
root@pytest-83-19:~# rbd info rbd/889795de-fafb-4fca-9bf1-9b984e6124d2.img | grep prefix
	block_name_prefix: rbd_data.30dc419495cff
root@pytest-83-19:~# 
```

### 获取列表

```
root@pytest-83-19:~# rados -p rbd ls |grep rbd_data.30dc419495cff > delobject
```

这里可以看下内容有没有问题，检查确认下:

```
root@pytest-83-19:~# vim delobject 
rbd_data.30dc419495cff.0000000000008e90
rbd_data.30dc419495cff.00000000000047a4
rbd_data.30dc419495cff.000000000000063f
............... 如下内容省略 ..........
```


删除的fast_remove.sh脚本如下：

```
root@node161:~# cat fast_remove.sh 
#!/bin/bash

process=400
objectlistfile="./delobject"
deletepool=san-pool


delete_fun()
  {
      date "+%Y-%m-%d %H:%M:%S"
      rados -p $deletepool rm $1
      #sleep 1
  }


concurrent()
 {
     start=$1 && end=$2 && cur_num=$3
     mkfifo   ./fifo.$$ &&  exec 4<> ./fifo.$$ && rm -f ./fifo.$$
     for ((i=$start; i<$cur_num+$start; i++)); do
         echo "init  start delete process $i" >&4
     done

     for((i=$start; i<=$end; i++)); do
         read -u 4
         {
             # echo -e "-- current delete: [:delete $i/$objectnum  $REPLY]"
             delob=`sed -n "${i}p" $objectlistfile`
             delete_fun $delob
             # echo "delete $delob done"  1>&4  # write to $ff_file
         } &
     done
     wait
 }

objectnum=`cat $objectlistfile | wc -l`
concurrent 1 $objectnum $process
root@node161:~#
```


### 测试结果


如下为Physical node的测试结果：

```
400 并发:
root@node161:~# time rados -p san-pool ls | grep '^rbd_data.3bba6b8b4567' | xargs -n 400  rados -p san-pool rm

real	0m55.853s
user	0m40.324s
sys	0m1.949s
root@node161:~# 


1200 并发:
root@node161:~# time rados -p san-pool ls | grep '^rbd_data.3bba6b8b4567' | xargs -n 1200  rados -p san-pool rm

real	0m53.060s
user	0m38.611s
sys	0m1.221s
root@node161:~# 
```

脚本删除结果（400并发）：

```
400 并发:
2023-04-21 17:55:16
-- current delete: [:delete 40960/40960  delete rbd_data.3bba6b8b4567.00000000000007b1 done]
2023-04-21 17:55:16
2023-04-21 17:55:16

real	1m59.236s
user	30m37.312s
sys	25m4.611s
root@node161:~#


1200 并发：

real	1m30.148s
user	24m40.103s
sys	19m49.270s
root@node161:~# 
```


尝试了VM以及Phsical Machine，多轮次测试验证，脚本删除的效果并不佳.




# 改版(2024-04-28)

{% raw %}```
#!/bin/bash

LOG="del.log"
TASK_NO=100
POOL_NAME=$1
RBD_IMAGE_NAME=$2
DEL_OBJECT="rbd_del_objects"
PAGED_FILE_NAME='del-object-page-'


function usage()
{
   echo -e "*****************************************"
   echo "usae: $0 POOL_NAME IMAGE_NAME"
   echo -e ""
   echo "  e.g.: $0 rbd fad9f42b-a255-4871-8515-38b96e8e4fa2.img"
   echo -e ""
   echo -e "*****************************************"
   exit 1
}


function env_check()
{
    rbd_info=`rbd info $1/$2`
    if [[ -z ${rbd_info} ]]; then
        echo ""
        echo "[ERROR]  POOL ($1) or Image ($2) not found, eixt!!"
        echo ""
        exit 2
    fi
}


function get_delete_object()
{
   start_time=`date "+%G-%m-%d %H:%M:%S"`

   block_name_prefix=`rbd info $1/$2 | grep block_name_prefix | awk '{{print $NF}}'`
   rados -p $1 ls | grep ${block_name_prefix} > ${DEL_OBJECT}

   end_time=`date "+%G-%m-%d %H:%M:%S"`
   time_distance=$(expr $(date +%s -d "${end_time}") - $(date +%s -d "${start_time}"))
   echo -e "[${end_time}]  Generate ${DEL_OBJECT} cost ${time_distance}s" | tee -a ${LOG}
}


function clean_objects()
{
    del_no=`cat ${DEL_OBJECT} | wc -l`
    if [[ $del_no -eq 1 ]]; then
        echo ""
        echo "[ERROR]  No record to delete, exit!!!" 
        echo ""
        exit 3
    fi

    rm -rf ${PAGED_FILE_NAME}*

    split_no=1000
    file_no=$(($del_no/${split_no}))
    suffix_length=${#file_no}
    PAGED_FILE_NAME="del-object-page-"


    split_start_time=`date "+%G-%m-%d %H:%M:%S"`
    echo -e "[${end_time}]  Generate ${DEL_OBJECT} cost ${time_distance}s" | tee -a ${LOG}

    # Each file has 1000 lines
    split -l 1000 $DEL_OBJECT -d -a ${suffix_length} ${PAGED_FILE_NAME}
    ls | grep ${PAGED_FILE_NAME} | awk -F "-" '{d=sprintf("%d" ,$4);system("mv "$0" '${PAGED_FILE_NAME}'"d".txt")}'

    split_end_time=`date "+%G-%m-%d %H:%M:%S"`
    split_time_distance=$(expr $(date +%s -d "${split_end_time}") - $(date +%s -d "${split_start_time}"))
    echo -e "[${split_end_time}]  Split ${file_no} file(s) cost ${split_time_distance}s" | tee -a ${LOG}

    echo -e "***************************************  ceph df ****************************************" | tee -a ${LOG}
    # Get output of 'ceph df' again
    cur_time=`date "+%G-%m-%d %H:%M:%S"`
    echo -e "[${cur_time}]  ceph df:" >> ${LOG}
    ceph df | tee -a ${LOG}
    echo "" >> ${LOG}

    echo -e "***********************************  Delete Objects *************************************" | tee -a ${LOG}

    del_obj_start_time=`date "+%G-%m-%d %H:%M:%S"`
    echo -e "[${del_obj_start_time}]  Delete Objects" >> ${LOG}
    echo -e "[${del_obj_start_time}]  1000 records per pickup file, which will be delete from ${file_no} file(s)" | tee -a ${LOG}

    if [[ ${file_no} -gt ${TASK_NO} ]];then
       loop_times=$(expr ${file_no} / ${TASK_NO})
       echo -e "[DEBUG]  Total loop times : $(expr ${loop_times} + 1)" >> ${LOG}
       for((i=0;i<=${loop_times};i++))
       do
           _start=$(expr ${TASK_NO} \* ${i})
           start=$(expr ${_start} + 1)
           multiplier=$(expr ${i} + 1)
           end=$(expr ${TASK_NO} \* ${multiplier})

           if [[ ${end} -ge ${file_no} ]];then
               end=${file_no}
           fi
           echo -e "[DEBUG]  Loop time : ${i}, delete from ${start} to ${end}" >> ${LOG}
           for((j=${start};j<=${end};j++))
           do
               cmd="cat ${PAGED_FILE_NAME}${j}.txt | xargs -I{} -P 10 rados -p rbd rm {}"
               echo "$cmd" >> ${LOG}
               eval "$cmd" &
           done
           wait
       done
    else
       for((i=0;i<=$file_no;i++))
       do
           cmd="cat ${PAGED_FILE_NAME}${i}.txt | xargs -I{} -P 10 rados -p rbd rm {}"
           echo "$cmd" >> ${LOG}
           eval "$cmd" &
       done
       wait
    fi

    del_obj_end_time=`date "+%G-%m-%d %H:%M:%S"`
    del_obj_time_distance=$(expr $(date +%s -d "${del_obj_end_time}") - $(date +%s -d "${del_obj_start_time}"))
    echo -e "[${del_obj_end_time}]  Delete Objects cost ${del_obj_time_distance}s" | tee -a ${LOG}

    echo -e "***************************************  ceph df ****************************************" | tee -a ${LOG}
    # Get output of 'ceph df' again
    cur_time=`date "+%G-%m-%d %H:%M:%S"`
    echo -e "[${cur_time}]  ceph df:" >> ${LOG}
    ceph df | tee -a ${LOG}
}


# Usage
if [[ $# -lt 2 ]]; then
    usage
fi

env_check $1 $2
get_delete_object $1 $2
clean_objects
``` {% endraw %}


本文参考：

``` https://www.cnblogs.com/zphj1987/p/13575449.html ```


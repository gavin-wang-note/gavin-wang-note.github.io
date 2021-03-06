---
layout:     post
title:      "利用oceanfile批量构造文件并统计cephfs速度"
subtitle:   "Used oceanfile to generate lots of files and calc write speed for cephfs"
date:       2020-07-06
author:     "Gavin"
catalog:    true
tags:
    - shell
---


# 概述

前段时间RD优化了rocksdb，S3的性能有显著提升，在此基础上，利用RD自研工具验证cepfhs 写速度，每间隔5million个文件进行一次写速度的统计。

# shell script

直接上脚本，参考如下:

```
root@node76:~/oceanfile# cat run_oceanfile.sh 
#!/bin/bash

EFILE=/usr/local/bin/oceanfile
target_no=5000000
WRITE_DIR="/vol/nas02/"
LOG="/var/log/nas_ocean.log"


function check_arch()
{   
    new_arch=(`echo $arch | tr ',' ' '` )
    total_no=1 
    for var in ${new_arch[@]}
    do  
        # echo $var
        let total_no*=$var
    done 

    if [[ ${total_no} -ne ${target_no} ]]; then
        echo ''
        echo '[ERROR]  The current round amount of data: (${total_no}) is less than expected amount of data: (${target_no})'
        echo ''
        exit 1
    fi
}


if [ $# != 3 ] ; then
    echo ""
    echo "USAGE: $0 parallel size arch"
    echo "  e.g.: $0 20 64 10,10,10,10,100"
    echo ""
    exit 1;
fi

parallel=$1
file_size=$2  # Unit is K
arch=$3

# Check arch numbers
check_arch

for round in {1..22}
do
    while (( $(ps aux | grep -w oceanfile | grep -v grep | wc -l) >= 1 )); do
        sleep 60
    done

    write_dir=${WRITE_DIR}/round_${round}

    if [[ ! -d ${write_dir} ]]; then
        mkdir -p ${write_dir}
    fi

    echo $(date) ROUND ${round} BEGIN  >>$LOG 2>&1
    start_time=`echo $[$(date +%s%N)/1000000]`
    ${EFILE} -d ${write_dir} -p ${parallel} -s ${file_size}k -b ${file_size}k -a ${arch} -i 5 >>$LOG 2>&1 
    end_time=`echo $[$(date +%s%N)/1000000]`

    diff=`expr ${end_time} - ${start_time}`
    time_diff=`echo | awk "{print $diff/1000}"`
    avg_speed=`echo | awk "{print ${target_no}/${time_diff}}"`
   
    # echo ROUND $round "* ${target_no}  cost $time_diff (ms) avg_speed $avg_speed"
    printf "ROUND %-8s  %12d (Files)       Cost %10.2f (s)  Avage: %8.2f\n" $round $target_no $time_diff $avg_speed
    
    echo >>$LOG 2>&1
    echo "ROUND $round  * $target_no (files) cost $time_diff (s)  avg_speed: $avg_speed" >> $LOG 2>&1
    echo $(date) ROUND ${round} FINISH  >>$LOG 2>&1
    echo >>$LOG 2>&1
    echo >>$LOG 2>&1
done
```

# 运行效果

<img class="shadow" src="/img/in-post/cephfs_write_speed.png" width="1200">



---
layout:     post
title:      "Calc NAS write speed by oceanfile tools"
subtitle:   "Calc NAS write speed by oceanfile tools"
date:       2021-04-06
author:     "Gavin Wang"
catalog:    true
categories:
    - [shell]
tags:
    - shell
---



# Overview

With the help of colleague Bean Li's oceanfile tool, a simple, quick pressure test of the product's NAS performance, so I wrote a test script to quickly know the results.



# Script

```shell
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

---
layout:     post
title:      "快速清除S3 Bucket下Objects"
subtitle:   "Fast to delete S3 Objects"
date:       2023-04-26
author:     "Gavin"
catalog:    true
tags:
    - ceph
---


# 概述

客户现场碰到ceph集群在 Recovery，但是 backfill full,需要清理掉部分数据。

本文针对Bucket下上千万的Object的清理，如何做到又快，又不出现将集群压死（集群压力过大），需要寻求一个平衡点，故本文介绍删除方法，相关参数可根据实际环境进行调测。



# 测试环境

* NJ Lab 4U36B，3台物理设备，每个node 3盘组RAID0, 内置两颗3.84T威刚NVME SSD
* 每个节点12个OSD，总计36个OSD
* 2+1 EC Pool 作为 S3 Data Pool
* 3台Client，运行Cosbench，向单一Bucket中灌入512KiB和 5MiB 大小的对象，按 1:1 比例灌入，大约写入300000个对象


# Object清理思路

* 利用aws s3api list-object-versions携带query参数，获取指定Bucket下待清理Objects
* 利用aws s3api delete-objects 去delete Objects 


流程大致如下：

* 支持清理多个prefix objects
* 支持被清理Bucket enable/disable Version下objects的清理
* 支持并发处理

   1) 每次获取指定数量（e.g:50000）的Objects

   2) 获取到的原始数据，并发分割成子文件，每个文件最多只含有1000个待删除Objects

   3) 并发读取各个子文件进行Objects的delete操作

# 测试结果


## Bucket 没有启用version

```
*****************************************************************************************
[2023-04-26 08:45:45]  ceph df:
GLOBAL:
    SIZE       AVAIL      RAW USED     %RAW USED
    786TiB     766TiB      20.7TiB          2.63
POOLS:
    NAME                          ID     USED        %USED     MAX AVAIL     OBJECTS
    .rgw.root                     1      1.07KiB         0        108TiB           4
    default.rgw.control           2           0B         0        224TiB           8
    default.rgw.meta              3      2.14KiB         0        225TiB          15
    default.rgw.log               4           0B         0        224TiB         288
    .ezs3                         5       210KiB         0        234TiB           7
    data                          6      5.81TiB      1.96        290TiB     6643190
    default.rgw.buckets.data      7           0B         0        290TiB           0
    .ezs3.central.log             8       214KiB         0        235TiB         113
    .ezs3.statistic               9           0B         0        246TiB           0
    metadata                      10      123MiB         0        361TiB        1056
    default.rgw.buckets.index     11     10.8GiB         0        206TiB         643
    ec                            13      726GiB      0.15        479TiB      297854
    rbd                           14          0B         0        291TiB           0
    san-pool                      15     4.59TiB      1.26        361TiB     4814435
*********************************  Generate Objects file  *******************************
[2023-04-26 08:48:31]  ceph df:
GLOBAL:
    SIZE       AVAIL      RAW USED     %RAW USED
    786TiB     767TiB      19.6TiB          2.50
POOLS:
    NAME                          ID     USED        %USED     MAX AVAIL     OBJECTS
    .rgw.root                     1      1.07KiB         0        108TiB           4
    default.rgw.control           2           0B         0        224TiB           8
    default.rgw.meta              3      2.14KiB         0        225TiB          15
    default.rgw.log               4           0B         0        224TiB         288
    .ezs3                         5       210KiB         0        234TiB           7
    data                          6      5.81TiB      1.96        290TiB     6643190
    default.rgw.buckets.data      7           0B         0        291TiB           0
    .ezs3.central.log             8       214KiB         0        235TiB         113
    .ezs3.statistic               9           0B         0        246TiB           0
    metadata                      10      123MiB         0        362TiB        1056
    default.rgw.buckets.index     11     10.8GiB         0        206TiB         643
    ec                            13     16.2GiB         0        480TiB        3323
    rbd                           14          0B         0        292TiB           0
    san-pool                      15     4.59TiB      1.25        362TiB     4814435
*********************************  Generate Objects file  *******************************
[2023-04-26 08:48:32]  Generate Objects file
aws s3api list-object-versions --endpoint-url=http://localhost --bucket "bucket01" --prefix "Veeam/" --page-size 1000 --max-items 50000 --query "[Versions][].{Key: Key}" >> Veeam-all.json
[2023-04-26 08:48:32]  Generate Veeam-all.json cost 0s
[2023-04-26 08:48:32]  Matched objects versions count : 0 to delete
*********************************  Calc total cost time *********************************
[2023-04-26 08:48:32]  Total cost 167s
```


清理速度：

```
(726 - 16.2) / 167 = 4.25GiB/s
(297854 - 3323) / 167 = 1763 Objects/s
```



## Bucket 启用 version

```
root@node161:~# bash empty_bucket_v1.2.sh 
***** This script will to delete objects which PREFIX is Veeam *****
*****************************************************************************************
GLOBAL:
    SIZE       AVAIL      RAW USED     %RAW USED 
    786TiB     766TiB      20.7TiB          2.63 
POOLS:
    NAME                          ID     USED        %USED     MAX AVAIL     OBJECTS 
    .rgw.root                     1      1.07KiB         0        108TiB           4 
    default.rgw.control           2           0B         0        224TiB           8 
    default.rgw.meta              3      2.14KiB         0        225TiB          15 
    default.rgw.log               4           0B         0        224TiB         288 
    .ezs3                         5       210KiB         0        234TiB           7 
    data                          6      5.81TiB      1.96        290TiB     6643190 
    default.rgw.buckets.data      7           0B         0        290TiB           0 
    .ezs3.central.log             8       214KiB         0        235TiB         115 
    .ezs3.statistic               9           0B         0        246TiB           0 
    metadata                      10      123MiB         0        361TiB        1056 
    default.rgw.buckets.index     11     17.9GiB         0        206TiB         674 
    ec                            13      734GiB      0.15        479TiB      597759 
    rbd                           14          0B         0        291TiB           0 
    san-pool                      15     4.59TiB      1.26        361TiB     4814435 
*********************************  Generate Objects file  *******************************
 
***** This script will to delete objects which PREFIX is Veeam *****
Deleted Veeam-all.json...
*****************************************************************************************
GLOBAL:
    SIZE       AVAIL      RAW USED     %RAW USED 
    786TiB     767TiB      19.6TiB          2.50 
POOLS:
    NAME                          ID     USED        %USED     MAX AVAIL     OBJECTS 
    .rgw.root                     1      1.07KiB         0        108TiB           4 
    default.rgw.control           2           0B         0        224TiB           8 
    default.rgw.meta              3      2.14KiB         0        225TiB          15 
    default.rgw.log               4           0B         0        224TiB         288 
    .ezs3                         5       210KiB         0        234TiB           7 
    data                          6      5.81TiB      1.96        290TiB     6643190 
    default.rgw.buckets.data      7           0B         0        291TiB           0 
    .ezs3.central.log             8       214KiB         0        235TiB         115 
    .ezs3.statistic               9           0B         0        246TiB           0 
    metadata                      10      123MiB         0        362TiB        1056 
    default.rgw.buckets.index     11     17.9GiB         0        206TiB         674 
    ec                            13     1.38GiB         0        480TiB         541 
    rbd                           14          0B         0        292TiB           0 
    san-pool                      15     4.59TiB      1.25        362TiB     4814435 
*********************************  Generate Objects file  *******************************
aws s3api list-object-versions --endpoint-url=http://localhost --bucket "bucket01" --prefix "Veeam/" --page-size 1000 --max-items 50000 --query "[Versions,DeleteMarkers][].{Key: Key, VersionId: VersionId}"  >> Veeam-all.json
[2023-04-26 09:05:57]  Generate Veeam-all.json cost 1s
[2023-04-26 09:05:57]  Matched objects versions count : 0 to delete
[WARN]  Matched (0) object to delete, exit!!!
 
*********************************  Calc total cost time *********************************
[2023-04-26 09:05:57]  Total cost 314s
root@node161:~# 
```

清理速度：

```
(734 - 1.38) / 314 = 2.33 GiB/s
(597759 - 541) / 314 = 1901 Objects/s
```



TiB 级别的大量数据的删除：

说明：
  * 如下删除动作，是先全部Dump完被删除对象，再并发清理。 Script后来有调整，防止最初的dump原始数据耗时太久出现异常。
  * 如下记录，仅做一个参考（通过其他的测试，从结果上看，Script后来的调整并没有出现删除衰减掉线严重现象）
  * 全部Dump出来记录再删除，如果这个dump的速度跟不上业务写入的速度（假定业务会持续写入），会出现一直都在dump数据，肯定会消耗比较多的Memory；所以跳转成每次只dump 5万笔记录，然后并发对这5万笔记录清理。

```
*****************************************************************************************
[2023-04-25 15:57:06]  ceph df:
GLOBAL:
    SIZE       AVAIL      RAW USED     %RAW USED
    786TiB     754TiB      32.9TiB          4.18
POOLS:
    NAME                          ID     USED        %USED     MAX AVAIL     OBJECTS
    .rgw.root                     1      1.07KiB         0        106TiB           4
    default.rgw.control           2           0B         0        220TiB           8
    default.rgw.meta              3      2.14KiB         0        221TiB          15
    default.rgw.log               4           0B         0        220TiB         288
    .ezs3                         5           0B         0        230TiB           4
    data                          6      5.81TiB      2.00        285TiB     6643190
    default.rgw.buckets.data      7           0B         0        286TiB           0
    .ezs3.central.log             8       212KiB         0        231TiB         113
    .ezs3.statistic               9           0B         0        242TiB           0
    metadata                      10      123MiB         0        355TiB        1056
    default.rgw.buckets.index     11     8.45GiB         0        203TiB        3203
    ec                            13     8.83TiB      1.84        471TiB     7784745
    rbd                           14          0B         0        286TiB           0
    san-pool                      15     4.59TiB      1.28        355TiB     4814435
*********************************  Generate Objects file  *******************************
[2023-04-25 15:57:06]  Generate Objects file
aws s3api list-object-versions --endpoint-url=http://localhost --bucket "bucket01" --prefix "Veeam/" --page-size 10000 --query "[Versions,DeleteMarkers][].{Key: Key, VersionId: VersionId}"  >> Veeam-all.json
[2023-04-25 16:28:21]  Generate Veeam-all.json cost 1875s
[2023-04-25 16:28:21]  Matched objects versions count: 3839000 to delete
************************************  Split files  **************************************
[2023-04-25 16:28:43]  Split files
[2023-04-25 16:30:46]  Split json file cost 123s
***********************************  Delete Objects *************************************
[2023-04-25 16:30:46]  Delete Objects
[2023-04-25 16:30:46]  1000 records per pickup file, which will be delete from 3839 files
[DEBUG]  Total loop times : 39
[DEBUG]  Loop time : 0, delete from 1 to 100
aws s3api delete-objects --bucket bucket01 --delete file://Veeam-page-1.json --endpoint-url=http://localhost
........................................ 中间内容省略 ......................................
aws s3api delete-objects --bucket bucket01 --delete file://Veeam-page-3838.json --endpoint-url=http://localhost
aws s3api delete-objects --bucket bucket01 --delete file://Veeam-page-3839.json --endpoint-url=http://localhost
[2023-04-25 16:58:19]  Delete Objects cost 1653s
*********************************  Calc total cost time *********************************
[2023-04-25 16:58:19]  Total cost 3673s
***************************************  ceph df ****************************************
[2023-04-25 16:58:19]  ceph df:
GLOBAL:
    SIZE       AVAIL      RAW USED     %RAW USED
    786TiB     767TiB      19.7TiB          2.51
POOLS:
    NAME                          ID     USED        %USED     MAX AVAIL     OBJECTS
    .rgw.root                     1      1.07KiB         0        108TiB           4
    default.rgw.control           2           0B         0        224TiB           8
    default.rgw.meta              3      2.14KiB         0        225TiB          15
    default.rgw.log               4           0B         0        224TiB         288
    .ezs3                         5           0B         0        234TiB           4
    data                          6      5.81TiB      1.96        290TiB     6643190
    default.rgw.buckets.data      7           0B         0        291TiB           0
    .ezs3.central.log             8       213KiB         0        235TiB         113
    .ezs3.statistic               9           0B         0        246TiB           0
    metadata                      10      123MiB         0        362TiB        1056
    default.rgw.buckets.index     11     8.45GiB         0        206TiB        1698
    ec                            13     73.5GiB      0.01        480TiB      119043
    rbd                           14          0B         0        292TiB           0
    san-pool                      15     4.59TiB      1.25        362TiB     4814435
```

删除速度：

```
root@node162:~# python
Python 2.7.12 (default, Oct  5 2020, 13:56:01) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 8.83 * 1024 - 73.5
8968.42
>>> (8.83 * 1024 - 73.5) / 3673.0
2.4417152191668934
>>> 
>>> (7784745 - 119043) / 3673.0
2087.041110808603
>>> 
```

相当于 2.44GiB/s，或2087Objects/s的删除速度。




# 测试结果汇总

| 删除的数据量    | 删除的Objects数   | Bucket是否启用Version |  耗时      |  删除速度        |
| ------- | ------------------------- | ----------------------| ---------- | ---------------- |
| From 726GiB to 16.2GiB | From 297854 to 3323 | No | 167s | 4.25GiB/s; 1763 Objects/s |
| From 734GiB to 1.38GiB | From 597759 to 541  | Yes | 314s (-10s) | 2.33 GiB/s; 1901 Objects/s|
| From 8.83TiB to 73.5GiB | From 7784745 to 119043 | Yes |  3673s | 2.442GiB/s; 2087.04 Objects/s |



说明：

* 整个清理过程中，对于最后恰巧要处理的记录为1000笔，script在sed page-0.json文件上有瑕疵，10s左右会超时，导致额外浪费了10s时间（不影响删除效果，Script就不修改了）



# Script 内容

## prefix.txt文件说明

prefixes.txt，这个文件要存在，里面记录被删除Object的前缀，如果有多个前缀，每行一个前缀记录，参考如下：

单个prefix信息：
e.g:

```
root@node161:~# cat prefixes.txt 
Veeam
root@node161:~# 
```

多个prefix信息：
e.g:

```
root@node161:~# cat prefixes.txt 
Veeam
Video
Stream
root@node161:~# 
```

## Script 内容

{% raw %}```
#!/bin/sh

LOG="del.log"
TASK_NO=100        # Maximum deletion concurrency allowed
MAX_ITEMS=50000    # List-version fetches the maximum number of records at a time
BUCKET="bucket01"
VERSION_SPLIT_NUMBER=4000  # One complete record every 4 line for query out if bucket enable version, i.e. 1000 Objects
NO_VERSION_SPLIT_NUMBER=3000  # One complete record every 3 line for query out if bucket not enable version, i.e. 1000 Objects
PREFIXES_FILE="prefixes.txt"  # If has many preifix, each line one record


function empty_bucket(){
version_tag=`aws s3api get-bucket-versioning --bucket ${BUCKET} --endpoint-url=http://localhost`
if [[ ${version_tag} =~ 'Enabled' ]];then
    version_flag='enable'
else
    version_flag='disable'
fi

if [ -f "$PREFIXES_FILE" ]; then
    while read -r current_prefix
    do
        printf '***** This script will to delete objects which PREFIX is %s *****\n' "$current_prefix"

        OLD_OBJECTS_FILE="$current_prefix-all.json"

        if [ -f "$OLD_OBJECTS_FILE" ]; then
            printf 'Deleted %s...\n' "$OLD_OBJECTS_FILE"

            rm "$OLD_OBJECTS_FILE"
            rm -rf $current_prefix-page-*.json
        fi

        echo -e "*****************************************************************************************" | tee -a ${LOG}
        # At first, get output of 'ceph df'
        cur_time=`date "+%G-%m-%d %H:%M:%S"`
        echo -e "[${cur_time}]  ceph df:" >> ${LOG}
        ceph df | tee -a ${LOG}

        echo -e "*********************************  Generate Objects file  *******************************" | tee -a ${LOG}
        gen_obj_start_time=`date "+%G-%m-%d %H:%M:%S"`
        echo -e "[${gen_obj_start_time}]  Generate Objects file" >> ${LOG}

        if [[ ${version_flag} == 'disable' ]]; then
            cmd="aws s3api list-object-versions --endpoint-url=http://localhost --bucket \"$BUCKET\" --prefix \"$current_prefix/\" --page-size 1000 --max-items ${MAX_ITEMS} --query \"[Versions][].{Key: Key}\" >> $OLD_OBJECTS_FILE"
        else
            cmd="aws s3api list-object-versions --endpoint-url=http://localhost --bucket \"$BUCKET\" --prefix \"$current_prefix/\" --page-size 1000 --max-items ${MAX_ITEMS} --query \"[Versions,DeleteMarkers][].{Key: Key, VersionId: VersionId}\"  >> $OLD_OBJECTS_FILE"
        fi

        echo -e "$cmd" | tee -a ${LOG}
        eval "$cmd"
        gen_obj_end_time=`date "+%G-%m-%d %H:%M:%S"`
        gen_obj_time_distance=$(expr $(date +%s -d "${gen_obj_end_time}") - $(date +%s -d "${gen_obj_start_time}"))
        echo -e "[${gen_obj_end_time}]  Generate $OLD_OBJECTS_FILE cost ${gen_obj_time_distance}s" | tee -a ${LOG}

        no_of_obj=$(cat "$OLD_OBJECTS_FILE" | jq 'length')
        if [[ "$no_of_obj" = "" ]]; then
            no_of_obj=0
        fi

        # Get old version Objects
        echo -e "[${gen_obj_end_time}]  Matched objects versions count : $no_of_obj to delete" | tee -a ${LOG}

        # If $OLD_OBJECTS_FILE, means no need to generate again, exit
        if [[ ${no_of_obj} -eq 0 ]]; then
            echo -e "[WARN]  Matched (${no_of_obj}) object to delete, exit!!!"
            echo ""

            end_time=`date "+%G-%m-%d %H:%M:%S"`
            time_distance=$(expr $(date +%s -d "${end_time}") - $(date +%s -d "${start_time}"))

            echo -e "*********************************  Calc total cost time *********************************" | tee -a ${LOG}
            echo -e "[${end_time}]  Total cost ${time_distance}s" | tee -a ${LOG}
            echo ""
            echo -e "*****************************************************************************************" | tee -a ${LOG}
            exit 2
        fi

        echo -e "************************************  Split files  **************************************" | tee -a ${LOG}
        split_obj_start_time=`date "+%G-%m-%d %H:%M:%S"`
        echo -e "[${split_obj_start_time}]  Split files" >> ${LOG}

        # 1st, modify the $OLD_OBJECTS_FILE
        ## Delete the first line
        sed -i '1d' $OLD_OBJECTS_FILE
        ## Replace the last line, change ']' to ','
        sed -i '$s/]/,/' $OLD_OBJECTS_FILE

        # 2nd, split file
        ## If enable version, each 4 line is one record
        ## If not enable version, each 3 line is one record
        split_no=1000
        file_no=$(($no_of_obj/${split_no}))
        suffix_length=${#file_no}
        paged_file_name="$current_prefix-page-"

        # echo -e "----  file_no : ${file_no}" | tee -a ${LOG}
        # echo -e "----  ${no_of_obj},${split_no}" | tee -a ${LOG}
        # split -l ${VERSION_SPLIT_NUMBER} $OLD_OBJECTS_FILE -d -a ${suffix_length} ${paged_file_name} && ls | grep ${paged_file_name} | xargs -n1 -i mv {} {}.json

        if [[ ${version_flag} == 'disable' ]]; then 
            split -l ${NO_VERSION_SPLIT_NUMBER} $OLD_OBJECTS_FILE -d -a ${suffix_length} ${paged_file_name}
        else
            split -l ${VERSION_SPLIT_NUMBER} $OLD_OBJECTS_FILE -d -a ${suffix_length} ${paged_file_name}
        fi

        # 3rd, rename file, e.g: Change name from Veeam-page-75 to Veeam-page-75.json, $3 is 75 in example
        # ls | grep Veeam-page- | awk -F "-" '{d=sprintf("%d" ,$3);system("mv "$0" Veeam-page-"d".json")}'
        ls | grep ${paged_file_name} | awk -F "-" '{d=sprintf("%d" ,$3);system("mv "$0" '${paged_file_name}'"d".json")}'

        # 4th, modify each split file
        ## First line add content of '{"Objects":['
        ## Last line replace ',' to '], "Quiet":true}'
        for((i=0;i<=$file_no;i++))
        do
            src_file_name="${paged_file_name}$i.json"
            sed -i '1i{"Objects":[' ${src_file_name}
            if  [[ ${no_of_obj} -le ${split_no} ]]; then  # Only one or two files need to split
                # sed -i '$s/,/], "Quiet":true}/' ${src_file_name}
                sed -i '$a\], "Quiet":true}' ${src_file_name}
            else
                if [[ $i != $file_no ]]; then
                    sed -i '$s/},/}\n], "Quiet":true}/' ${src_file_name}
                else
                    sed -i '$s/,/], "Quiet":true}/' ${src_file_name}
                fi
            fi
        done

        split_obj_end_time=`date "+%G-%m-%d %H:%M:%S"`
        split_obj_time_distance=$(expr $(date +%s -d "${split_obj_end_time}") - $(date +%s -d "${split_obj_start_time}"))
        echo -e "[${split_obj_end_time}]  Split json file cost ${split_obj_time_distance}s" | tee -a ${LOG}

        echo -e "***********************************  Delete Objects *************************************" | tee -a ${LOG}
        del_obj_start_time=`date "+%G-%m-%d %H:%M:%S"`
        echo -e "[${del_obj_start_time}]  Delete Objects" >> ${LOG}
        page_file_prefix="$current_prefix-page"
        echo -e "[${del_obj_start_time}]  1000 records per pickup file, which will be delete from ${file_no} file(s)" | tee -a ${LOG}

        # If file_no is too large, needs to be split into multiple tasks to be executed sequentially,
        # avoiding too much system resource usage due to simultaneous initiation
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
                   cmd="aws s3api delete-objects --bucket $BUCKET --delete file://${page_file_prefix}-${j}.json --endpoint-url=http://localhost"
                   echo "$cmd" >> ${LOG}
                   eval "$cmd" &
               done
               wait
           done
        else
           for((i=0;i<=$file_no;i++))
           do
               cmd="aws s3api delete-objects --bucket $BUCKET --delete file://${page_file_prefix}-${i}.json --endpoint-url=http://localhost"
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
    done < "$PREFIXES_FILE"
else
    echo "$PREFIXES_FILE does not exist."
    exit 1
fi
}


function loop_delete(){
    start_time=`date "+%G-%m-%d %H:%M:%S"`

    for((i=0;i<100000;i++))
    do
       empty_bucket
    done
}


# Action
loop_delete

``` {% endraw %}


# 参考文档

```
https://stackoverflow.nilmap.com/question?dest_url=https://stackoverflow.com/questions/29809105/how-do-i-delete-a-versioned-bucket-in-aws-s3-using-the-cli
https://serverfault.com/questions/679989/most-efficient-way-to-batch-delete-s3-files
https://stackoverflow.nilmap.com/question?dest_url=https://stackoverflow.com/questions/10054985/how-to-delete-files-recursively-from-an-s3-bucket
```

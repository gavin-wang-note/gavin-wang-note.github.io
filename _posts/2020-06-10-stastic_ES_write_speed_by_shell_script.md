---
layout:     post
title:      "脚本统计ES写入速度"
subtitle:   "Stastic ES write speed by shell script"
date:       2020-06-10
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - shell
---


# 概述

本文介绍下如何call API的方式去统计ES的写速度，当然，你可以使用监控工具去统计，不在本文描述范围。


# 哪些API可以获取到ES index中的数据量

这里介绍两种API,参考如下：

```
_cat/count?v&format=json&pretty
```

吐出信息参考如下：


```
[
  {
    "epoch" : "1591598061",
    "timestamp" : "06:34:21",
    "count" : "3626228"
  }
]
```

另外一种是

```
index_name/_cat/indices?v&pretty
```

输出示例参考如下:


```
root@node248:/opt/datasearch# curl -XGET -s 'localhost:9200/_cat/indices?v&pretty'
health status index                uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   rgw-default-fb9bb242 fZDCxLRPRKS1hn6GD_PE-g  12   0    8796770         6075      3.3gb          3.3gb
root@node248:/opt/datasearch# 
```

说明：

因为ES集群中只有一个index，所以可以不带index_name，如果有多个，在不带具体index_name情况下，或查询出所有的，建议根据所需进行查询。



# 这两个API，哪个更合适？

先说```_cat/count?v&format=json&pretty ```， 它的吐出信息中，epoch其实就是时间戳，但精度只到秒级别，如果要计算ES写入速度：获取前后两个count的值，以及前后两个epoch的值，分别做差，使用前者的差值，除以后者的差值，得到当前ES的写入速度，效果如下：


```
root@node76:~# python calc_es_write_speed.py 
-------  Timestamp ----------- Total Counts ---------- Counts diff --------- Time diff ------- ES speed -------
	 1591778958 	       4645564 		       1616  	        	3 		  538
	 1591778961 	       4647574 		       921  			2 		  460
	 1591778964 	       4649407 		       755  			1 		  755
	 1591778967 	       4651841 		       849  			1 		  849
	 1591778971 	       4654225 		       1062  			2 		  531
	 1591778974 	       4656417 		       1012  			2 		  506
	 1591778978 	       4658627 		       1151  			2 		  575
	 1591778981 	       4661607 		       1067  			1 		  1067
.................................................. 中间数据省略 ................................................                                            
	 1591779923 		5264956 		873  			1 		   873
	 1591779926 		5267410 		845  			1 		   845
	 1591779929 		5269377 		1030  			1 		   1030
	 1591779933 		5271217 		933  			2 		   466
	 1591779936 		5273646 		973  			1 		   973
---------------------------------------------------------------------------------------------------------------
AVG speed : 700.153333333
root@node76:~# 
```

弊端比较明显了，精度不够，有时除以1，有时除以2，比如上次统计是1000，下次就可能是500了。

另外一种API ```index_name/_cat/indices?v&pretty ```,通过观察，大约60秒左右才会更新一次数据，更新频率不大，但是计算起止时间可以自己控制，精度也可以自己控制。


# 脚本

分别使用了 ```_cat/count?v&format=json&pretty``` 和 ```index_name/_cat/indices?v&pretty ``` 这两个API，写了统计脚本，本文只给出shell 使用```index_name/_cat/indices?v&pretty ```的示例,脚本内容如下:

```
#!/bin/bash

TOTAL_COUNTS=10000000
LOG_FILE=es_speed.log
TITLE_NAME="------ Timestamp ------  Total Counts ------ Time Diff ------ Count Diff ------  AVG Speed ------"


# start_time=`echo $[$(date +%s%N)/1000000]`
cur_counts=`curl -XGET -s 'localhost:9200/_cat/indices?v&pretty' | grep 'rgw-default' | awk '{{print $7}}' 2>&1`

echo ${TITLE_NAME} | tee ${LOG_FILE}

while [ ${cur_counts} -lt ${TOTAL_COUNTS} ]
do
    before_counts=${cur_counts}

    start_time=`echo $[$(date +%s%N)/1000000]`
    sleep 60

    cur_counts=`curl -XGET -s 'localhost:9200/_cat/indices?v&pretty' | grep 'rgw-default' | awk '{{print $7}}' 2>&1`
    end_time=`echo $[$(date +%s%N)/1000000]`

    if [[ ${cur_counts} -ne ${before_counts}  ]]; then
        diff=`expr ${end_time} - ${start_time}`
        time_diff=`echo | awk "{print $diff/1000}"`
        count_diff=`expr ${cur_counts} - ${before_counts}`
        avg_speed=`echo | awk "{print ${count_diff}/${time_diff}}"`

        echo "      ${end_time}       ${cur_counts}           ${time_diff}           ${count_diff}             ${avg_speed}" | tee ${LOG_FILE}
    else
        echo "${end_time}    [WARN]  Get the same count : (${cur_counts}) in adjacent intervals, wait 2 seconds" >> ${LOG_FILE}
        sleep 2
    fi
done
```


输出内容示例如下:

```
root@node76:~# bash speed_calc_es.sh 
------ Timestamp ------ Total Counts ------ Time Diff ------ Count Diff ------ AVG Speed ------
      1591781812805       6372650           60.043           44556             742.068
      1591781934909       6416426           60.04           43776             729.114
      1591782057108       6509848           60.128           93422             1553.72
      1591782117259       6554868           60.131           45020             748.699
      1591782177403       6604810           60.118           49942             830.733
      1591782237568       6648911           60.139           44101             733.318
      1591782359825       6692497           60.114           43586             725.056
      1591782419957       6735616           60.115           43119             717.275
      1591782542227       6833050           60.121           97434             1620.63
      1591782602341       6958258           60.088           125208             2083.74
```


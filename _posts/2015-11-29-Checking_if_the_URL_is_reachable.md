---
layout:     post
title:      "检查URL是否可达"
subtitle:   "Checking if the URL is reachable"
date:       2015-11-29
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - shell
---


# 概述

今天查看某公众号发现一篇shell脚本，用来侦测网络URl是否可达，直接抄袭过来备用。


# 代码

```shell
#!/usr/bin/env bash 

# Description: Web check with curl

#定义颜色
red='\e[0;31m'
RED='\e[1;31m'
green='\e[0;32m'
GREEN='\e[1;32m'
blue='\e[0;34m'
BLUE='\e[1;34m'
cyan='\e[0;36m'
CYAN='\e[1;36m'
NC='\e[0m'

date=`date +%Y-%m-%d' '%H:%M:%S` 

# 定义User Agent
ua="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36"
pass_count=0
fail_count=0

# 需要检测的url
urls=(
    "http://www.bing.com"
)

function request(){
    status=$(curl -sk -o /dev/null --retry 1 --connect-timeout 1 -w '%{http_code}' --user-agent "$ua" $1)
    if [ $status -eq '200' -o $status -eq '301' \
                           -o $status -eq '302' ]; then
        echo -e "[${GREEN} Passed ${NC}] => $1"
  ((pass_count ++))
    else
        echo -e "[${RED} Failed ${NC}] => $1"
  ((fail_count ++))
    fi
}

function main(){
    echo "Start checking ..."
    for((i=0;i<${#urls[*]};i++)) 
        do 
        request ${urls[i]};
        done
    # 输出检测通过和失败的记录
    echo -e "======================== Summary ======================== "
    echo -e "Total: ${cyan} $((pass_count + fail_count))${NC}  Passed: ${green}${pass_count}${NC}  Failed: ${red}${fail_count}${NC} Time: $date"
       
}

main $*
```


测试效果：

```shell
[ wyz@node2 ~]$ bash check_url.sh 
Start checking ...
[ Passed ] => http://www.bing.com
======================== Summary ======================== 
Total:  1  Passed: 1  Failed: 0 Time: 2023-11-29 18:11:57
[ wyz@node2 ~]$ 
```

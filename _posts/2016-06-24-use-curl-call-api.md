---
layout:     post
title:      "Curl调用CGI完成UI操作"
subtitle:   "Use curl call API"
date:       2016-06-24
author:     "Gavin"
catalog:    true
tags:
    - curl
---

# 引言

Web UI上的所有操作都对应一个CGI(大多是一个HTTP GET请求)，因此如果想快速地进行大量UI操作，可以直接call CGI去完成想要的工作。对于发送一个HTTP请求，绝大多数编程语言都可以做到。如果是自动化测试开发，可能会选择python等比较全面的工具，但如果只是偶尔用之，一个小小的curl，一两行命令就可以满足要求。

# 示例

## Step1 记录下cookie文件test.cookie

--cookie-jar可简化做-c，仅需要登录一次，除非会话过期

```
curl --cookie-jar test.cookie --insecure "https://10.16.17.191:8080/cgi-bin/ezs3/json/login?user_id=admin&password=1"
```

## Step2 调用对应的API

--cookie可简化做-b，该示例是创建一个叫pool01的pool

```
curl --cookie ezstor.cookie --insecure "https://10.16.17.191:8080/cgi-bin/ezs3/json/poolcreate?poolname=pool01"
```

# 扩展

如何抓取API?

可以借助浏览器，F12，就可以抓取自己care的API了

# 完整脚本示例

* 说明:
* * 本示例，用于创建集群

```
#!/bin/bash

public_ip=(
172.17.59.101
172.17.59.102
172.17.59.103
)
storage_ip=(
192.168.100.101
192.168.100.102
192.168.100.103
)
license_info=(
CLAWCT-PTWAV4-4K66F0-C3RH9O-8ATUKF-YDO14G-11WI568
CLB2LB-GF94W0-2O11R5-NA4E9L-5B5XRM-9DFK0V-72438U
CLB8TT-70LYWW-5ZYPBB-H0AAR4-126WJ0-VC8END-1H4H309
)
osd_device=sdb

public_iface=eth0
cluster_iface=eth1
root_passwd=1
cluster_name=automation
ui_account=admin
ui_account_passwd=1
rep_no=2
ntp_server_ip=202.120.2.101
enable_timeout=480


function check_network()
{
    # public_interface network status check
    echo "@1.Start to check network."
    echo -e "  [Public interface]:"
    for(( i=0; i<${#public_ip[@]}; i++ ))
    do
        public_network_status=`ping -c 4 ${public_ip[i]} | grep "packet loss" | awk -F " " '{print $6}'`
        if [[ x"${public_network_status}" == x"0%" ]]; then
            echo -e "    ${public_ip[i]}  -->  OK"
        else
            echo -e "    ${public_ip[i]}  -->  OK"
            return 1
        fi
    done
    
    # storage_interface network status check
    echo -e "  [Storeage interfae]:"
    for(( i=0;i<${#storage_ip[@]}; i++ ))
    do
        storage_network_status=`ping -c 4 ${storage_ip[i]} | grep "packet loss" | awk -F " " '{print $6}'`
        if [[ x"${storage_network_status}" == x"0%" ]]; then
            echo -e "    ${storage_ip[i]}  -->  OK"
        else
            echo -e "    ${storage_ip[i]}  -->  OK"
            return 1
        fi
    done
    return 0
}

function check_apache()
{ 
    # network is bad, do not start apache
    ret=`echo $?`
    if [[ ${ret} -eq 1 ]]; then
        echo -e "[ERROR]  network check finish, network is bad."
        return 1
    else
        echo -e "[Success]  network check finish, network is ok."
    fi
    
    echo -e "\n@2.Start to check apache service."
    for(( i=0; i<${#public_ip[@]}; i++ ))
    do
        for(( i=0; i<3; i++ ))
        do
            ret_code=$(curl -I -m 10 -o /dev/null -s -w %{http_code} --insecure --cookie-jar cookie.jar "https://${public_ip[i]}:8080/cgi-bin/ezs3/json/login?user_id=root&password=${root_passwd}")
            if [[ x"${ret_code}" != x"200" ]]; then
                echo -e "[ERROR]  Apache's service is bad on ${public_ip[i]}, error code is ${ret_code}"
                return 1
            else
                echo -e "  Apache service on ${public_ip[i]}  -->  OK"
            fi
        done
    done

    echo -e "[Success] Check Apache service finished, all apache's service are OK."
    return 0

:<<!
    # add host to sshpass known list
    for(( i=0; i<${#public_ip[@]}; i++ ))
    do
        #echo ${apache_status}
        sshpass -p p@ssw0rd ssh -o StrictHostKeyChecking=no root@${public_ip[i]} pidof apache2
        #apache_status="sshpass -p p@ssw0rd ssh -o StrictHostKeyChecking=no root@${public_ip[i]} pidof apache2"
        #echo ${apache_status}
    done
    
    # check apache whether or not start
    for(( i=0; i<${#public_ip[@]}; i++ ))
    do
        apache_status="sshpass -p p@ssw0rd ssh -o StrictHostKeyChecking=no root@${public_ip[i]} pidof apache2"
        if [[ x"${apache_status}" == x"" ]]; then
            echo "apache not started @${public_ip[i]}."
            return 1
        else
            echo "apache started ${public_ip[i]}."
        fi
    done
    return 0
!
}

function check_license()
{
   license_array_len=${#license_info[@]}
   storage_ip_len=${#storage_ip[@]}

   if [[ x"${license_array_len}" -ne x"${storage_ip_len}" ]]; then
      echo -e "    [ERROR] Licesne number should same as the number of nodes\n"
      return 1 
   fi
}


function create_cluster()
{
    for(( i=0;i<${#storage_ip[@]};i++))
    do
        if [[ ${i} -eq 0 ]]; then 
            cluster_ip+=${storage_ip[i]}
        else
            cluster_ip+=+${storage_ip[i]}
        fi
    done

    echo -e "Login with root account, then create the cluster\n"
    curl --insecure --cookie-jar cookie.jar "https://${public_ip[0]}:8080/cgi-bin/ezs3/json/login?user_id=root&password=${root_passwd}"
    
    curl --insecure --cookie cookie.jar "https://${public_ip[0]}:8080/cgi-bin/ezs3/json/create_cluster?admin_account=${ui_account}&admin_passwd=${ui_account_passwd}&cluster_name=${cluster_name}&license_key=&mons=${cluster_ip#*+}&nodes=${cluster_ip}&ntp_server_list=${ntp_server_ip}&rack_id=0&rep_no=2&use_rack_aware=false"
 
    echo -e "Account of root logout\n"
    curl --insecure --cookie cookie.jar "https://${public_ip[0]}:8080/cgi-bin/ezs3/json/logout"
    
    echo -e "Remove cookie.jar\n"
    rm -rf cookie.jar
    echo -e "Sleep 100s, to wait root session timeout\n"
    sleep 100
    
    echo -e "Login UI with ${ui_account}, then input license/create OSD/enable GW\n"
    curl --insecure  --cookie-jar ui-cookie.jar "https://${public_ip[0]}:8080/cgi-bin/ezs3/json/login?user_id=${ui_account}&password=${ui_account_passwd}"
}


function input_license()
{
    for(( i=0;i<${#storage_ip[@]};i++))
    do 
        echo -e "    Input lincesne ${license_info[i]} on ${storage_ip[i]}\n"
        curl --insecure --cookie ui-cookie.jar "https://${public_ip[0]}:8080/cgi-bin/ezs3/json/license_set?ip=${storage_ip[i]}&key=${license_info[i]}"
        sleep 1
    done
}

function create_and_enable_osd()
{
    for(( i=0;i<${#storage_ip[@]};i++))
    do 
        echo -e "    Create OSD on node ${storage_ip[i]}\n"
        curl --insecure --cookie ui-cookie.jar "https://${public_ip[0]}:8080/cgi-bin/ezs3/json/storage_volume_add" --data "host=${storage_ip[i]}&name=osd&sv_type=0&data_devs=%5B%22%2Fdev%2F${osd_device}%22%5D&journal_dev=data&cache_dev=&spare_devs=%5B%5D&dedup=false&compress=false&memory_conserve=false&enable_osd=true&ip=${storage_ip[i]}&cluster_iface=${cluster_iface}&public_iface=${public_iface}&pool_to_join=default&add_metadata_pool=true"
        echo -e "    Enable  OSD on node ${storage_ip[i]}\n"
        curl --insecure --cookie ui-cookie.jar "https://${public_ip[0]}:8080/cgi-bin/ezs3/json/node_role_enable_osd?ip=${storage_ip[i]}&sv_list=osd&cluster_iface=${cluster_iface}&public_iface=${public_iface}"
        echo -e "    Check OSD up/down status on node ${storage_ip[i]}\n"
        j=1
        while [[ ${j} -le ${enable_timeout} ]]
        do
           osd_up_nums=`ceph osd tree | grep -A 2 default_${storage_ip[i]} | grep -i up| wc -l 2>&1`
           if [[ ${osd_up_nums} -ge 1 ]]; then
               echo -e "        [SUCCESS] OSD is up on node ${storage_ip[i]}\n"
               break
           else
               echo -e "        Node ${storage_ip[i]}, the $j time(s) check OSD up status, total check times is ${enable_timeout}\n"
           fi
           let j++
           sleep 1
        done
    done
}


function enable_gw()
{
    for(( i=0;i<${#storage_ip[@]};i++))
    do
        echo -e "    Enable Gateway on node ${storage_ip[i]}\n"
        curl --insecure --cookie ui-cookie.jar "https://${public_ip[0]}:8080/cgi-bin/ezs3/json/gateway_role_enable?ip=${storage_ip[i]}&public_iface=${public_iface}"
        echo -e "    Check GW enabled status on node ${storage_ip[i]}\n"
        j=1
        while [[ ${j} -le ${enable_timeout} ]]
        do
           ctdb_status=`ctdb status | grep ${storage_ip[i]} | awk '{print $3}'| sed 's/ //g' 2>&1`
           if [[ x"${ctdb_status}" == x"OK" ]]; then
               echo -e "        [SUCCESS] GW is enabled\n"
               break
           else
               echo -e "        Node ${storage_ip[i]}, the $j time(s) to check ctdb status, total check times is ${enable_timeout}\n"
           fi
           let j++
           sleep 1
        done
    done
}

function cluster_health()
{
    echo -e "Check cluster health status\n"
    health_status=`ceph -s | grep -i health | awk '{print $NF}' | sed 's/ //g' 2>&1`
    i=1
    while [[ $i -le ${enable_timeout} ]]
    do
        if [[ x"${health_status}" != x"HEALTH_OK" ]]; then
            echo -e "  The $i time(s) to check cluster health, total check times is ${enable_timeout}\n"
            let i++
            sleep 1
        else
            echo -e "  [Success] Cluster health is OK\n"
            break
        fi
    done
}

function clean_env()
{
    echo -e "Clean current env\n"
    rm ui-cookie.jar
}

#curl -I -o /dev/null -s -w %{http_code} --insecure --cookie-jar cookie.jar "https://172.16.146.130:8080/cgi-bin/ezs3/json/login?user_id=root&password=${root_passwd}"
#code_status=$(curl -I -o /dev/null -s -w %{http_code} --insecure --cookie-jar cookie.jar "https://172.16.146.130:8080/cgi-bin/ezs3/json/login?user_id=root&password=${root_passwd}")
#echo "status: ${code_status}"
#echo "http_code: ${http_code}"

check_network
check_apache
echo -e "Do some general checks\n"
check_license
echo -e "    Check whether the licesne number is the same as the number of nodes    [Success]\n"

create_cluster
input_license
create_and_enable_osd
enable_gw
cluster_health
clean_env

```


---
layout:     post
title:      "mds damaged test script"
subtitle:   "mds damaged test script"
date:       2020-08-26
author:     "Gavin"
catalog:    true
tags:
    - mds
    - ceph
    - shell
---


# Scripts

mds_damaged.sh

{% raw %}```
#!/bin/bash

loop_cnt=1000
ctdb_wait_time=500
ceph_wait_time=60
throughput_wait_time=300
throughput_min=200
node_num=3
pgnum=25600
errno=0

function send_mail()
{
    echo "$1"
    python -c "from ezs3.mail_notification import MailNotificationManager; \
               MailNotificationManager().send_mail('Quit of ctdb_event_lost scipt: ${1}', '${1}')"
}

turn_on_debug()
{
#    onnode all 'echo "module libceph +ftpl" > /sys/kernel/debug/dynamic_debug/control' 2>/dev/null
#    onnode all 'echo "file caps.c +ftpl" > /sys/kernel/debug/dynamic_debug/control' 2>/dev/null
    ceph tell osd.* injectargs '--debug-osd 20/20' 2&>/dev/null
#    ceph tell osd.* injectargs '--debug-ms 20/20' 2&>/dev/null
    ceph tell mds.* injectargs '--debug-mds 20/20' 2&>/dev/null
}

turn_off_debug()
{
#    onnode all 'echo "module libceph -ftpl" > /sys/kernel/debug/dynamic_debug/control' 2>/dev/null
#    onnode all 'echo "file caps.c -ftpl" > /sys/kernel/debug/dynamic_debug/control' 2>/dev/null
    ceph tell osd.* injectargs '--debug-osd 0/0' 2&>/dev/null
    ceph tell osd.* injectargs '--debug-ms 0/0' 2&>/dev/null
    ceph tell mds.* injectargs '--debug-mds 0/0' 2&>/dev/null
}

function truncate_files_if_near_full()
{
    usage=`df -h .|tail -n 1|sed -nr 's/.* ([0-9]+)%.*/\1/gp'`
    if (( $usage > 80 ));then
        echo "`date`: WARN! root partition usage is over 80%, truncate all logs on all nodes."
        onnode -p all 'truncate --size 0 /var/log/ceph/ceph*.log;truncate --size 0 /var/log/kern.log;truncate --size 0 /var/log/syslog'
    fi
}

function wait_until_ctdb_ok()
{
    expect_num=$1
    max_wait_time=$2
    current_time=0
    while [[ $current_time -lt $max_wait_time ]];do
        current_ctdb_ok=`ctdb status 2>/dev/null|grep OK|wc -l`
        if [ $current_ctdb_ok -eq $expect_num ];then
            break
        fi
        #truncate_files_if_near_full
        sleep 5
        current_time=$((current_time+5))
        #echo "...elapse: $current_time, ctdb: ${current_ctdb_ok}"
    done
    if [[ $current_time -ge $max_wait_time ]];then
        turn_off_debug
        #send_mail "Fail!!! After wait $max_wait_time seconds, ctdb number is still $current_ctdb_ok, should be $expect_num, exit!"
        echo "`date`: Fail!!! After wait $max_wait_time seconds, ctdb number is still $current_ctdb_ok, should be $expect_num, exit!"
    fi
    echo $current_time
}

function wait_until_ceph_ok()
{
    max_wait_time=$1
    current_time=0
    while [[ $current_time -lt $max_wait_time ]];do
        ceph -s|grep "$pgnum active+clean" >/dev/null
        if [ $? -eq 0 ];then
            ceph -s|grep "mons down" >/dev/null
            if [ $? -ne 0 ];then
                break
            fi
        fi
        #truncate_files_if_near_full
        sleep 5
        current_time=$((current_time+5))
    done
    if [[ $current_time -ge $max_wait_time ]];then
        turn_off_debug
        #send_mail "Fail!!! After wait $max_wait_time seconds, ceph is not healthy, but is `ceph health`, exit!"
        echo "`date`: Fail!!! After wait $max_wait_time seconds, ceph is not healthy, but is `ceph health`, exit!"
    fi
    echo $current_time

}

function wait_until_throughput_ok()
{
    max_wait_time=$1
    current_time=0
    while [[ $current_time -lt $max_wait_time ]];do
        throughput=`ceph -s |sed -nr 's/.*client.*rd, ([0-9]+).*rd.*/\1/gp'`
        if (( throughput > throughput_min ));then
            break
        fi
        sleep 5
        current_time=$((current_time+5))
    done
    if [[ $current_time -ge $max_wait_time ]];then
        turn_off_debug
        #send_mail "Fail!!! After wait $max_wait_time seconds, throughput is still only $throughput MiB/s, exit!"
        echo "`date`: Fail!!! After wait $max_wait_time seconds, throughput is still only $throughput MiB/s, exit!"
    fi
    echo $current_time
}

function find_ctdb_master()
{
    pnn=$(ctdb status| sed -nr 's/Recovery master:([0-3])/\1/p')
    echo $(ctdb status| sed -nr "s/pnn:$pnn 10.10.51.([0-9]+).*/\1/p")
}

for ((i=1;i<=$loop_cnt;i++));do
    echo "===================$i==================="
    turn_on_debug
    ip="10.16.172.$(find_ctdb_master)"
    echo "`date`: Find the master ip: $ip"
    case "$ip" in 
        "10.16.172.51")
            intdev=enp94s0f1
        ;;
        "10.16.172.52")
            ctdb setrecmasterrole off
            sleep 20
            #ctdb setrecmasterrole on
            echo "`date`: Skip this round due to script is running on 52"
            continue
        ;;
        "10.16.172.53")
            intdev=enp94s0f1
        ;;
        *)
          echo "`date`: Invalid master ip: $ip, quit!"
          exit 1
        ;;
    esac
    echo "`date`: ssh $ip ifconfig $intdev down"
    ssh $ip ifconfig $intdev down
    sleep 30
    cost_time=$(wait_until_ctdb_ok $((node_num-1)) $ctdb_wait_time)
    if [[ $cost_time =~ "Fail" ]];then
        echo $cost_time
        exit 1 
    fi
    echo "`date`: After $((cost_time+30))s, ctdb OK nodes reaches $((node_num-1))."
    echo "`date`: ssh $ip ifconfig $intdev up"
    ssh $ip ifconfig $intdev up
    sleep 11
    echo "`date`: ssh $ip ifconfig $intdev down"
    ssh $ip ifconfig $intdev down
    sleep 35
    echo "`date`: systemctl stop ceph-mon.target"
    systemctl stop ceph-mon.target
    sleep 10
    echo "`date`: ssh $ip ifconfig $intdev up"
    ssh $ip ifconfig $intdev up
    sleep 10
    echo "`date`: systemctl start ceph-mon.target"
    systemctl disable ceph-mon.target 2&> /dev/null
    systemctl enable ceph-mon.target 2&> /dev/null
    systemctl start ceph-mon.target 2&> /dev/null
    cost_time=$(wait_until_ctdb_ok $node_num $ctdb_wait_time)
    if [[ $cost_time =~ "Fail" ]];then
        echo $cost_time
        exit 1 
    fi
    echo "`date`: After ${cost_time}s, ctdb OK nodes reaches ${node_num}."
    cost_time=$(wait_until_ceph_ok $ceph_wait_time)
    if [[ $cost_time =~ "Fail" ]];then
        echo $cost_time
        exit 1 
    fi
    echo "`date`: After ${cost_time}s, ceph becomes HEALTH_OK."
    onnode all 'ls /var/log/cores/ -lhrt' 2>/dev/null|grep ezcore.tp_peering
    if [[ $? -eq 0 ]]; then
        turn_off_debug
        #send_mail "`date`: FAIL!! Core dump of peering yielded."
        echo "`date`: FAIL!! Core dump of peering yielded."
        exit 1
    fi
    onnode all 'rm -f /var/log/cores/ezcore.msgr*' 2>/dev/null
    onnode all 'ls /var/log/cores -lhrt' 2>/dev/null|grep ezcore
    if [[ $? -eq 0 ]]; then
#        onnode all 'rm -f /var/log/cores/ezcore*' 2>/dev/null
#        echo "`date`: WARN!! Other core dump yielded."
        turn_off_debug
        #send_mail "`date`: FAIL!! Core dump yielded."
        echo "`date`: FAIL!! Core dump yielded."
        exit 1
    fi
    ceph -s | grep "mds daemon damaged"
    if [[ $? -eq 0 ]]; then
        turn_off_debug
        #send_mail "`date`: FAIL!! mds daemon damaged."
        echo "`date`: FAIL!! mds daemon damaged."
        exit 1
    fi
    onnode -p all 'truncate --size 0 /var/log/ceph/ceph*.log;truncate --size 0 /var/log/kern.log;truncate --size 0 /var/log/syslog; truncate --size 0 /var/log/rsyslog.debug '
#     cost_time=$(wait_until_throughput_ok $throughput_wait_time)
#     echo "`date`: After ${cost_time}s, nfs traffic achieves ${throughput_min} MiB/s."
    echo "`date`: Sleep 10s to end this loop."
    sleep 10
    echo "Loop $i pass."
done
turn_off_debug
``` {% endraw %}


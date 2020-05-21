---
layout:     post
title:      "控制keepalive VIP漂移范围"
subtitle:   "keepalive contro VIP floating range"
date:       2020-05-21
author:     "Gavin"
catalog:    true
tags:
    - keepalive
---

# 概述

产品有配置keepalive功能，但该功能目前仅通过priority来控制VIP在不同节点间漂移，此处的不同节点，是集群内部的所有节点。

我们先看看下各个节点（以3节点为例），keepalive.conf内容信息，参考如下：

== node243

```
root@node243:/etc/keepalived# cat keepalived.conf 
global_defs {
    vrrp_version 3
}

vrrp_instance VRRP0 {
    state BACKUP
#   Specify the network interface to which the virtual address is assigned
    interface enp5s0f0
    virtual_router_id 89
#   Set the value of priority lower on the backup server than on the master server
    priority 3
    advert_int 0.4
    track_interface {
        bond1
    }
    virtual_ipaddress {
        12.7.3.89
    }
}
```

== node244

```
root@node244:/var/log# cat /etc/keepalived/keepalived.conf 
global_defs {
    vrrp_version 3
}

vrrp_instance VRRP0 {
    state BACKUP
#   Specify the network interface to which the virtual address is assigned
    interface enp5s0f0
    virtual_router_id 89
#   Set the value of priority lower on the backup server than on the master server
    priority 2
    advert_int 0.4
    track_interface {
        bond1
    }
    virtual_ipaddress {
        12.7.3.89
    }
}
```

== node245

```
root@node245:/etc/keepalived# cat keepalived.conf 
global_defs {
    vrrp_version 3
}

vrrp_instance VRRP0 {
    state BACKUP
#   Specify the network interface to which the virtual address is assigned
    interface bond0
    virtual_router_id 89
#   Set the value of priority lower on the backup server than on the master server
    priority 1
    advert_int 0.4
    track_interface {
        bond1
    }
    virtual_ipaddress {
        12.7.3.89
    }
}
```

通过上面的配置文件，可以看出来，各个节点间的priority值不一样，仅仅是通过priority来控制VIP的漂移。

讲到这里，问题来了，如果客户生产环境因预算不足，只能有2个节点物理设备，按照产品部署要求，>=3个节点，势必会需要一台VM作为仲裁节点（不承担任何业务数据，仅启用ceph-mon参与mon election用），那就不能讲这台VM纳入keepalive VIP漂移范围了，即keepalive VIP不能落到这台VM上。

# 改进

问题已经清晰了，那么，如何控制VIP，落在指定的设备节点上呢？

通过查询一些资料，更改keepalive.conf配置文件信息，可以达到预期效果：



## 更改后的keepalive.conf信息

== node243

```
root@node243:/etc/keepalived# cat keepalived.conf 
global_defs {
   notification_email {
   root@localhost
   }
   notification_email_from keepalived@localhost
   smtp_server 127.0.0.1
   smtp_connect_timeout 30
   router_id node243                    #主调度器的主机名
   vrrp_mcast_group4 224.26.1.1             #发送心跳信息的组播地址
    
}

vrrp_instance VI_1 {
    state MASTER                            #主调度器的初始角色
    interface enp5s0f0                      #虚拟IP工作的网卡接口
    virtual_router_id 89                    #虚拟路由的ID
    priority 100                            #主调度器的选举优先级
    advert_int 1
    virtual_ipaddress {
        12.7.3.89                     #虚拟IP
    }
}

virtual_server 12.7.3.89 80 {         #LVS配置段，VIP
    delay_loop 6
    lb_algo rr                              #调度算法轮询
    lb_kind DR                              #工作模式DR
    nat_mask 255.255.252.0
#    persistence_timeout 50                  #持久连接，在测试时需要注释，否则会在设置的时间内把请求都调度到一台RS服务器上面
    protocol TCP
    sorry_server 127.0.0.1 80               #Sorry server的服务器地址及端口
    real_server 12.7.3.243 80 { 
        weight 1 
        HTTP_GET {                          #健康状态检测方法
            url {
              path /
              status_code 200               #状态判定规则
            }
            connect_timeout 1
            nb_get_retry 3
            delay_before_retry 1
        }
    }

    real_server 12.7.3.244 80 {
        weight 1
        HTTP_GET {
            url {
              path /
                status_code 200
            }
            connect_timeout 1
            nb_get_retry 3
            delay_before_retry 1
        }
    }
}
```

== node244

```
root@node244:/etc/keepalived# cat keepalived.conf 
global_defs {
   notification_email {
   root@localhost
   }
   notification_email_from keepalived@localhost
   smtp_server 127.0.0.1
   smtp_connect_timeout 30
   router_id node244                #备份调度器的主机名
   vrrp_mcast_group4 224.26.1.1         #这个组播地址需与集群内的其他主机相同

}

vrrp_instance VI_1 {
    state BACKUP                        #初始角色，备份服务器需设置为BACKUP
    interface enp5s0f0
    virtual_router_id 89                #虚拟路由的ID一定要和集群内的其他主机相同
    priority 90                         #选举优先级，要比主调度器地一些
    advert_int 1
    virtual_ipaddress {
        12.7.3.89
    }
}
                #余下配置和主服务器相同
virtual_server 12.7.3.89 80 {
    delay_loop 6
    lb_algo rr
    lb_kind DR
    nat_mask 255.255.252.0
#    persistence_timeout 50              
    protocol TCP
    sorry_server 127.0.0.1 80

    real_server 12.7.3.243 80 {
        weight 1
        HTTP_GET {
            url {
              path /
              status_code 200
            }
            connect_timeout 1
            nb_get_retry 3
            delay_before_retry 1
        }
    }

    real_server 12.7.3.244 80 {
        weight 1
        HTTP_GET {
            url {
              path /
                status_code 200
            }
            connect_timeout 1
            nb_get_retry 3
            delay_before_retry 1
        }
    }
}
```


== node245

```
root@node245:/etc/keepalived# cat keepalived.conf 
global_defs {}
root@node245:/etc/keepalived# 
```


## 验证效果

### 重启所有节点的keepalive服务

```
root@node245:/etc/keepalived# onnode -p all 'systemctl restart keepalived.service'
root@node245:/etc/keepalived# 
```

检查syslog，是否有keepalive日常日志，以及keepalive进程是否存在。如果都没有问题，说明keepalive启动正常。



### 检查VIP落在哪个node上

```
root@node243:/etc/keepalived# ip a | grep '12.7.3.89'
    inet 12.7.3.89/32 scope global enp5s0f0
root@node243:/etc/keepalived# 

```

说明当前VIP 12.7.3.89落在node243上，这个也符合keepalive.conf中的设定（priority=100，另外一个是90，最后一个node没有）

### 停用node243的keepalive服务

```
root@node243:/etc/keepalived# systemctl stop keepalived.service 
root@node243:/etc/keepalived# ip a | grep '12.7.3.89'
root@node243:/etc/keepalived# 
```

### 再次检查VIP落在哪个node上

```
root@node243:/etc/keepalived# ip a | grep '12.7.3.89'
root@node243:/etc/keepalived# 

```

```
root@node244:/etc/keepalived# ip a | grep '12.7.3.89'
    inet 12.7.3.89/32 scope global enp5s0f0
root@node244:/etc/keepalived# 
```

```
root@node245:/etc/keepalived# ip a | grep '12.7.3.89'
root@node245:/etc/keepalived# 
```

### 停用node244的keepalive服务

```
root@node244:/etc/keepalived# systemctl stop keepalived.service 
```

### 再次检查VIP落在哪个node上

```
root@node243:/etc/keepalived# ip a | grep '12.7.3.89'
root@node243:/etc/keepalived# 
```

```
root@node244:/etc/keepalived# ip a | grep '12.7.3.89'
root@node244:/etc/keepalived# 
```

```
root@node245:/etc/keepalived# ip a | grep '12.7.3.89'
root@node245:/etc/keepalived# 
```

# 结语

至此，通过上述验证方法，可以控制住keepalive的VIP漂移到哪些指定的host上。

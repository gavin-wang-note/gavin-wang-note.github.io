---
layout:     post
title:      "Config QCT switch port network"
subtitle:   "Config QCT switch port network"
date:       2021-02-09
author:     "Gavin Wang"
catalog:    true
categories:
    - [switch]
tags:
    - switch
---



# Overview

QCT 100G switch, need to do port adaptation.

# Action

```shell
admin@Switch:~$ sudo qnos-cli
[sudo] password for admin: 

(Switch) #configure 


show interface port-mode


interface 0/17


(Switch) (Interface 0/17)#port-mode ?

1x100G                   Configure the port as a single 100G port
1x40G                    Configure the port as a single 40G port
2x50G                    Configure the port as two 50G ports.
4x10G                    Configure the port as four 10G ports
4x25G                    Configure the port as four 25G ports

(Switch) (Interface 0/17)#port-mode 1x100G

(Switch) (Interface 0/18)#exit

(Switch) (Config)#exit

(Switch) #copy running-config startup-config
```


# 设置级联

## SwtichA 操作

```shell
admin@Switch:~$ sudo qnos-cli
(Switch) #configure
(Switch) (Config)#interface port-channel 64
(Switch) (Config)#no staticcapability
(Switch) (Config)#switchport mode trunk
(Switch) (Config)#mlag peer-link
(Switch) (Config)#interface 0/31
(Switch) (Interface 0/31)#channel-group 64 mode active
(Switch) (Interface 0/31)#exit
(Switch) (Config)#mlag
(Switch) (Config)#mlag domain 1
(Switch) (Config)#mlag peer-keepalive enable
(Switch) (Config)#mlag peer-keepalive destination 172.17.75.248 source 172.17.75.249
(Switch) (Config)#exit
```

## SwtichB 操作

```shell
admin@Switch:~$ sudo qnos-cli
(Switch) #configure
(Switch) (Config)#interface port-channel 64
(Switch) (Config)#no staticcapability
(Switch) (Config)#switchport mode trunk
(Switch) (Config)#mlag peer-link
(Switch) (Config)#interface 0/31
(Switch) (Interface 0/31)#channel-group 64 mode active
(Switch) (Interface 0/31)#exit
(Switch) (Config)#mlag
(Switch) (Config)#mlag domain 1
(Switch) (Config)#mlag peer-keepalive enable
(Switch) (Config)#mlag peer-keepalive destination 172.17.75.249 source 172.17.75.248
(Switch) (Config)#exit
```


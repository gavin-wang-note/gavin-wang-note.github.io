---
layout:     post
title:      "使用shell实现节点间ssh互信"
subtitle:   "ssh key mutual trust between hosts"
date:       2015-09-22
author:     "Gavin Wang"
catalog:    true
categories:
    - [Linux]
tags:
    - ssh
    - shell
---

# 概述

说假设有一个100台节点的Hadoop集群，要配置节点之间的SSH免密码登录，该如何用shell脚本实现？



# 实现过程



## 方案1：脚本实现

```shell
#!/bin/expect
#循环100台机器的IP地址，生成密钥文件authorized_keys

for ip in {cat ip.list}
do
  ssh user@$ip ssh-keygen -t rsa  &>/dev/null
  expect{
        "yes/no" { send "yes\r";exp_continue}
        "password:"{send "$passwd\r";exp_continue}
       }

  cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys &> /dev/null  
  exit

  if [ !-f ~/.ssh/authorized_keys ];<br>   then
    touch ~/.ssh/authorized_keys<br>   fi
  ssh user@$ip cat ~/.ssh/authorized_keys >> ~/.ssh/authorized_keys  &> /dev/null
  expect{
        "yes/no" { send "yes\r";exp_continue}
        "password:"{send "$passwd\r";exp_continue}
       }  
done

 
#scp authorized_keys 文件到各台机器上面。
for ip in {cat ip.list}
do
  scp ~/.ssh/authorized_keys user@$ip:~/.ssh/ 
  expect{
        "yes/no" { send "yes\r";exp_continue}
        "password:"{send "$passwd\r";exp_continue}
       }  
done
```



## 方案2：所有node使用相同key

将第一个node上生成的dsa public key（一般是/root/.ssh/id_dsa.pub），scp到其他节点的/root/.ssh/目录下，即所有节点的dsa public key都一样，自然就实现ssh的互信了。

这里介绍个快速传递ssh key的命令，ssh-copy-id ：

ssh-copy-id 将本机的公钥复制到远程机器的authorized_keys文件中，ssh-copy-id也能让你到远程机器的home, ~./ssh , 和 ~/.ssh/authorized_keys的权利。

语法格式如下：

```shell
 ssh-copy-id 将key写到远程机器的 ~/ .ssh/authorized_key.文件中 
```

示例：

```shell
 ssh-copy-id -i .ssh/id_rsa.pub 用户名字@192.168.x.xxx
```


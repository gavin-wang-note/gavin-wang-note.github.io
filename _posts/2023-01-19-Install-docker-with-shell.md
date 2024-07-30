---
layout:     post
title:      "一键安装 docker 的 shell 脚本"
subtitle:   "Linux shell to install Docker"
date:       2023-01-19
author:     "Gavin Wang"
catalog:    true
categories:
    - [shell]
    - [Docker]
tags:
    - Linux
    - shell 
    - Docker 
---

# 概述

一键安装Docker的shell脚本，脚本比较粗糙，将就用。


# Script Content


```shell
yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine


echo -e " =========== 1.delete exist docker ================\n\n"

echo -e "step 1: 安装必要的一些系统工具"
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

echo -e "\n\nStep 2: 添加软件源信息，国内 Repository 更加稳定"
sudo yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

version=sudo cat /etc/redhat-release|sed -r 's/.* ([0-9]+)\..*/\1/'

if $version=7; then
        echo  -e "\n\nStep 3: 更新 Centos version is : $version; run yum makecache fast"
        sudo yum makecache fast
elif $version=8; then
        echo -e "\n\nStep 3: 更新Centos version is : $version; run yum makecache fast"
        sudo dnf makecache
fi

echo -e "=========== 2.完成配置 docker Repository ================\n\n"

# 安装最新版本的 Docker Engine 和 Container
sudo yum install docker-ce docker-ce-cli containerd.io
sudo yum -y install docker-ce


echo -e "=========== 3.成功安装完 docker ================\n\n"

sudo systemctl enable docker
sudo systemctl start docker

echo -e "=========== 4.自启动 docker ================\n\n"


# 1.创建一个目录
sudo mkdir -p /etc/docker


# 2.编写配置文件
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["http://hub-mirror.c.163.com",
    "https://docker.mirrors.ustc.edu.cn",
    "https://reg-mirror.qiniu.com",
    "http://f1361db2.m.daocloud.io"
  ]
}
EOF


sudo systemctl daemon-reload
sudo systemctl restart docker

echo -e "=========== 5.配置国内镜像加速 ================\n\n"

docker ps -a
```

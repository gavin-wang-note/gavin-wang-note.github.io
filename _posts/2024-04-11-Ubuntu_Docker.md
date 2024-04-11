---
layout:     post
title:      "Ubuntu23下Docker部署"
subtitle:   "Ubuntu23下Docker部署"
date:       2024-04-11
author:     "Gavin Wang"
catalog:    true
img: "/img/docker/docker1.png"
categories:
    - [python]
    - [Docker]
tags:
    - Linux
    - python 
    - Docker
---


# 概述

很久没有碰Docker了，今天在VM下（基于Ubuntu23 Server）安装docker，记录一下。

# 安装Docker

使用如下脚本，一键部署docker

```python
import os
import sys
import subprocess


# 检查当前用户是否是root用户
def is_root_user():
    print("  检查是否为root用户")
    return os.geteuid() == 0

# 尝试执行一个需要sudo权限的命令，判断是否具有sudo权限
def has_sudo_permission():
    print("  检查是否具有sudo权限")
    try:
        # 这里我们尝试更改一个只有root用户才能更改的系统文件的权限
        # 如果有sudo权限，这个命令会被sudo执行并成功更改权限
        # 注意：这是一个无害的命令，只是尝试更改文件的权限并不会真的创建文件
        subprocess.run(['sudo', 'chmod', '755', '/etc/passwd'], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        # 如果捕获到CalledProcessError异常，说明没有sudo权限
        return False

# 检查是否具有执行安装的权限
def check_root_privilege():
    print("\nStep1.检查当前用户是否有root权限")
    if not is_root_user() or not has_sudo_permission():
        print("Error: You must have root privileges to install Docker. Please run as root or use 'sudo'.")
        sys.exit(1)

# 执行命令并检查返回值
def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{' '.join(command)}': {e}")
        sys.exit(1)

# 主函数，安装Docker
def install_docker():
    # 检查当前用户是否是root用户
    check_root_privilege()
    
    # 更新软件包索引
    print('\nStep2.apt-get update')
    run_command(["sudo", "apt-get", "update"])
    
    # 安装Docker所需的依赖包
    print("\nStep3.安装Docker所需的依赖包")
    run_command(["sudo", "apt-get", "install", "-y", "apt-transport-https",
                 "ca-certificates", "curl", "gnupg", "lsb-release"])
    
    # 添加Docker的官方GPG密钥
    print("\nStep4.添加Docker的官方GPG密钥")
    try:
        # 使用Popen来执行管道命令
        process = subprocess.Popen(["curl", "-fsSL", "https://download.docker.com/linux/ubuntu/gpg"],
                                   stdout=subprocess.PIPE)
        # 将curl命令的输出通过管道传递给apt-key add命令
        gpg_key = process.communicate()[0].decode().strip()
        # 添加GPG密钥
        run_command(["echo", gpg_key, "|", "sudo", "apt-key", "add"])
    except subprocess.CalledProcessError as e:
        print(f"Error adding Docker GPG key: {e}")
        sys.exit(1)

    # 设置稳定的Docker仓库
    # 你需要根据你的系统版本替换LSB_RELEASE_OUTPUT变量的值
    print("\nStep5.设置稳定的Docker仓库")

    # 获取系统的LSB版本和发行版代号
    lsb_release_output = subprocess.check_output(['lsb_release', '-cs', '|', 'grep', '-v', 'No']).decode().strip()
    
    run_command(["sudo", "add-apt-repository", "deb [arch=amd64] https://download.docker.com/linux/ubuntu",
                 f"{lsb_release_output}", "docker", "stable"])

    # 移除错误的Docker仓库（如果已添加）
    run_command(["sudo", "rm", "-rf", "/etc/apt/sources.list.d/docker.list"])
    
    # 构造正确的Docker仓库URL
    docker_repository = f"https://download.docker.com/linux/ubuntu {lsb_release_output}"
    
    # 添加Docker的官方仓库到系统的sources.list文件
    run_command(["sudo", "add-apt-repository", " deb [arch=amd64] " + docker_repository + " docker-ce stable"])
    
    # 更新软件包索引
    run_command(["sudo", "apt-get", "update"])

    # 再次更新软件包索引
    print("\nStep6.再次更新软件包索引")
    run_command(["sudo", "apt-get", "update"])
    
    # 安装Docker Engine
    print("\nStep7.安装Docker Engine")
    run_command(["sudo", "apt-get", "install", "-y", "docker-ce", "docker-ce-cli", "containerd.io"])
    
    # 启动Docker服务
    print("\nStep8.启动Docker服务")
    run_command(["sudo", "systemctl", "enable", "docker"])
    run_command(["sudo", "systemctl", "start", "docker"])
    
    print("[Success]Docker has been successfully installed!")

if __name__ == "__main__":
    install_docker()
```

执行成功后，检查Docker是否被成功安装：

```shell
root@Service:~# docker ps
CONTAINER ID   IMAGE             COMMAND       CREATED        STATUS             PORTS     NAMES
root@Service:~#
```

出现如上信息，表明Docker成功安装。


# 安装docker-compose

前往官网`https://github.com/docker/compose/releases`，查看最新版本，比如v2.26.1，使用如下命令进行安装：

```shell
curl -L "https://github.com/docker/compose/releases/download/v2.26.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

安装后，执行`docker-compose --version`检查是否安装成功：

```shell
root@Service:~# docker-compose --version
Docker Compose version v2.26.1
root@Service:~# 
```

如上表示成功安装了docker-compose v2.26.1版本。




# 安装docker-machine

前往官网`https://github.com/docker/machine/releases`获取最新release版本号，比如`v0.16.2`，执行如下命令进行安装：

```shell
base=https://github.com/docker/machine/releases/download/v0.16.2 &&
curl -L $base/docker-machine-$(uname -s)-$(uname -m) >/tmp/docker-machine &&
mv /tmp/docker-machine /usr/local/bin/docker-machine &&
chmod +x /usr/local/bin/docker-machine
```

检查安装效果：

```shell
root@Service:~# docker-machine --version
docker-machine version 0.16.2, build bd45ab13
root@Service:~# docker-machine ls
NAME   ACTIVE   DRIVER   STATE   URL   SWARM   DOCKER   ERRORS
root@Service:~# 
```




# docker-machine 使用

接下来通过 virtualbox 来介绍 docker-machine 的使用方法。其他云服务商操作与此基本一致，具体可以参考每家服务商的指导文档。

说明：

  请从`https://www.virtualbox.org/wiki/Downloads`下载并安装virtualbox，并设置环境变量。

比如我的环境是Ubuntu 23，直接 `apt-get install virtualbox` 进行安装。


## 列出可用的机器

```shell
root@Service:~# docker-machine ls
NAME   ACTIVE   DRIVER   STATE   URL   SWARM   DOCKER   ERRORS
root@Service:~# 
```
显示为空。


## 创建可用的机器

创建一台名为 Gavin 的机器:

```shell
docker-machine create --driver virtualbox Gavin
```

创建过程如下：

```shell
root@Service:~# docker-machine create --driver virtualbox Gavin
Creating CA: /root/.docker/machine/certs/ca.pem
Creating client certificate: /root/.docker/machine/certs/cert.pem
Running pre-create checks...
Error with pre-create check: "VBoxManage not found. Make sure VirtualBox is installed and VBoxManage is in the path"
root@Service:~# 
```

* --driver：指定用来创建机器的驱动类型，这里是 virtualbox。 

这个时候再次列出可用机器：

```shell
root@Service:~# docker-machine create --driver virtualbox Gavin
Running pre-create checks...
(Gavin) No default Boot2Docker ISO found locally, downloading the latest release...
(Gavin) Latest release for github.com/boot2docker/boot2docker is v19.03.12
(Gavin) Downloading /root/.docker/machine/cache/boot2docker.iso from https://github.com/boot2docker/boot2docker/releases/download/v19.03.12/boot2docker.iso...
(Gavin) 0%....10%....20%....30%....40%....50%....60%....70%....80%....90%....100%
Creating machine...
(Gavin) Copying /root/.docker/machine/cache/boot2docker.iso to /root/.docker/machine/machines/Gavin/boot2docker.iso...
(Gavin) Creating VirtualBox VM...
(Gavin) Creating SSH key...
(Gavin) Starting the VM...
(Gavin) Check network to re-create if needed...
(Gavin) Found a new host-only adapter: "vboxnet0"
Error creating machine: Error in driver during machine creation: Error setting up host only network on machine start: /usr/bin/VBoxManage hostonlyif ipconfig vboxnet0 --ip 192.168.99.1 --netmask 255.255.255.0 failed:
VBoxManage: error: Code E_ACCESSDENIED (0x80070005) - Access denied (extended info not available)
VBoxManage: error: Context: "EnableStaticIPConfig(Bstr(pszIp).raw(), Bstr(pszNetmask).raw())" at line 252 of file VBoxManageHostonly.cpp
```

这里报错了，提示权限问题，暂时没解决掉，先放着吧。


# 常见错误


## 执行docker-compose up提示'services must be a mapping'

```shell
root@Service:~/composetest# docker-compose up
services must be a mapping
root@Service:~/composetest# 
```

错误信息 "services must be a mapping" 表示 docker-compose 命令无法执行，因为在执行过程中没有找到正确格式的 docker-compose.yml 文件，或者该文件格式不正确。
对于YML文件，注意如下细节：

* 缩进问题：YAML 文件非常依赖正确的缩进，且只接受空格作为缩进字符，不接受制表符（Tab）。请确保每一级缩进都使用了两个或更多的空格，并且层级结构保持一致。

* 行尾的空格：YAML 文件中的每一行末尾都不能有任何额外的字符，包括空格。




## 进入容器报错'stat /bin/bash: no such file or directory: unknown'

```shell
root@Service:~# docker exec -it 085bdc5ed931 /bin/bash
OCI runtime exec failed: exec failed: unable to start container process: exec: "/bin/bash": stat /bin/bash: no such file or directory: unknown
root@Service:~# 
```


解决方法：
更换shell类型：

```shell
root@Service:~# docker exec -it 085bdc5ed931 /bin/bash
OCI runtime exec failed: exec failed: unable to start container process: exec: "/bin/bash": stat /bin/bash: no such file or directory: unknown
root@Service:~# docker exec -it 085bdc5ed931 /bin/sh
/data # 
/data # 
/data # cat /etc/shells 
# valid login shells
/bin/sh
/bin/ash
/data # 
```

我们还可以通过echo $SHELL 命令来查看当前使用的Shell类型。

下面我们进行一些常见Shell的讲解：
(1) BourneShell(sh)：是由AT&T Bell实验室的 Steven Bourne为AT&T的Unix开发的，它是Unix的默认Shell，也是其它Shell的开发基础。Bourne Shell在编程方面相当优秀，但在处理与用户的交互方面不如其它几种Shell。

(2) BourneAgain Shell (即bash)：是自由软件基金会(GNU)开发的一个Shell，它是Linux系统中一个默认的Shell。Bash不但与Bourne Shell兼容，还继承了C Shell、Korn Shell等优点。

(3) ash：ash Shell是由Kenneth Almquist编写的，是Linux 中占用系统资源最少的一个小Shell，它只包含24个内部命令，因而使用起来很不方便。

(4) CShell(csh)：是加州伯克利大学的Bill Joy为BSD Unix开发的，共有52个内部命令，与sh不同，它的语法与C语言很相似。它提供了Bourne Shell所不能处理的用户交互特征，如命令补全、命令别名、历史命令替换等。但是，C Shell与BourneShell并不兼容。该Shell其实是指向/bin/tcsh这样的一个Shell，也就是说，csh其实就是tcsh。

(5) KornShell(ksh)：是AT&T Bell实验室的David Korn开发的，共有42 条内部命令，它集合了C Shell和Bourne Shell的优点，并且与Bourne Shell向下完全兼容。Korn Shell的效率很高，其命令交互界面和编程交互界面都很好。

(6) zch：是Linux 最大的Shell之一，由Paul Falstad完成，共有84 个内部命令。如果只是一般的用途，没有必要安装这样的Shell。

注释：bash是 Bourne Again Shell 的缩写，是linux标准的默认shell ，它基于Bourne shell，吸收了C shell和Korn shell的一些特性。bash完全兼容sh，也就是说，用sh写的脚本可以不加修改的在bash中执行。




## docker-machine create 报错 E_ACCESSDENIED (0x80070005)

```shell
(Gavin) Found a new host-only adapter: "vboxnet1"
Error creating machine: Error in driver during machine creation: Error setting up host only network on machine start: /usr/bin/VBoxManage hostonlyif ipconfig vboxnet1 --ip 192.168.99.1 --netmask 255.255.255.0 failed:
VBoxManage: error: Code E_ACCESSDENIED (0x80070005) - Access denied (extended info not available)
VBoxManage: error: Context: "EnableStaticIPConfig(Bstr(pszIp).raw(), Bstr(pszNetmask).raw())" at line 252 of file VBoxManageHostonly.cpp
```

解决方法：

暂时未找到有效解决方法，先搁置。


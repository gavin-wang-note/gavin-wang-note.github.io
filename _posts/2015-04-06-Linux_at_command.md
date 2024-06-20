---
title: Linux下一次性任务(at和batch命令)
date: 2015-04-06 23:01:57
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: Linux下at和batch实现一次性任务执行
categories:
    - [Linux]
tags:
    - Linux
---

# Overview

我们知道，在Linux中可以使用cron实现周期性任务，但如果我有一个一次性任务，该如何做呢？

也许你会说，可以使用nohup或者tmux里执行类似这样的指令达到预期目的：

```shell
sleep 7200; ./do_st.sh
```

即根据当前时间，计算一下预期需要等到多久，再执行具体命令。

Hmm，太trick了...

今天介绍另外一种方式，使用`at`命令。

# at 介绍

在 Linux 中，你可以使用 `at` 命令来安排一次性的定时任务。`at` 命令允许你在将来的某个时间点执行一个命令或一组命令。


##  安装

对于基于 `Debian` 的系统（如 `Ubuntu`）：

```shell
sudo apt-get update
sudo apt-get install at
```

对于基于 `Red Hat` 的系统（如 `CentOS` 或 `Fedora`）：

```shell    
sudo yum install at
···

或者，如果你使用的是 dnf：

```shell
sudo dnf install at
···

## 使用 `at` 命令安排任务

假设你想在 5 分钟后运行以下命令：
       
```shell
echo "Hello, World!" > /tmp/hello.txt
```

你可以这样做：

```shell
echo "echo 'Hello, World!' > /tmp/hello.txt" | at now + 5 minutes
```

这里，`echo` 命令用于将待执行的命令传递给 `at`, `now + 5 minutes` 指定了任务的执行时间。


## 查看已安排的任务

使用 `atq` 命令查看已安排的任务及其作业号：

```shell 
atq
```

输出可能如下所示：

```shell
Job 1 at 2015-04-06 15:00
```

## 取消已安排的任务

如果你想取消一个已安排的任务，可以使用 `atrm` 命令，后面跟上作业号：

```shell
atrm 1
```

这里，1 是你想取消的任务的作业号。

## 使用 at 的交互模式

我们还可以将 `at` 命令与 `-t` 选项一起使用，以指定确切的日期和时间：

```shell
at -t 2015-04-06 15:00
```

然后，你会进入一个提示符，可以输入要安排的命令。输入完成后，按 `Ctrl + D` 保存并退出。

## 使用 batch 命令

`batch`命令是 `at` 的一个变体，它会在系统负载较低时运行任务。这可以用于不紧急的任务：

```shell
echo "echo 'Hello, World!' > /tmp/hello.txt" | batch
```

或者，使用交互模式：

```shell        
batch
```

然后输入命令，完成后按 `Ctrl + D` 保存并退出。


# 应用场景示例

## 使用at的场景和示例

### 安排一次性任务


你想在明天的某个特定时间运行一个脚本:

```shell
at 9:00 PM tomorrow <<END
/path/to/your/script.sh
END
```

### 发送提醒邮件

你想要在一周后的今天发送一封提醒邮件给自己:

```shell 
echo "This is a reminder for the meeting next week." | at now + 1 week
```

### 系统维护

你需要在夜间执行系统维护任务，比如运行 `apt-get update` 和 `apt-get upgrade`。

```shell  
echo "sudo apt-get update && sudo apt-get upgrade -y" | at 2:00 AM
```

### 定时备份

你想要每天凌晨2点自动运行备份脚本:

```shell
echo "/path/to/backup.sh" | at 2:00 AM
```

### 定时关机

你需要在特定时间自动关闭系统:

```shell 
echo "sudo shutdown -h now" | at 5:00 PM
```

## 使用 batch 的场景和示例

### 低优先级数据处理

你有一项数据处理任务，不需要立即完成，可以在系统负载较低时运行:

```shell  
echo "/path/to/data_processing.sh" | batch
```

### 夜间运行的低优先级任务

你想要在夜间系统负载较低时运行一个长时间的计算任务:

```shell
echo "/path/to/long_computation.sh" | batch -t 23:00
```

### 系统清理任务

你需要定期清理日志文件和临时文件，这可以在夜间进行，以减少对系统性能的影响:

```shell        
echo "/path/to/system_cleanup.sh" | batch
```

### 定期数据库维护

数据库需要定期维护，比如每周日的凌晨1点运行数据库清理脚本:

```shell
echo "/path/to/db_maintenance.sh" | batch -t 01:00
```

### 非紧急的文件传输

你需要在网络负载较低时进行文件传输，比如在夜间:

```shell
echo "rsync -avz /source/ /destination/" | batch
```

**注意**

* `at` 和 `batch` 命令通常在后台运行，不会显示命令的输出。如果你想查看输出，可以将输出重定向到文件中，如上例所示。
* `at` 和 `batch` 命令的具体行为可能会因系统和配置的不同而有所差异。在使用这些命令时，你应该检查你的系统文档以了解它们的具体用法和选项。此外，出于安全考虑，确保你了解这些命令的权限和潜在风险。


# 重点内容

（2024-06-20新增了本小结内容）

## at命令精确到分钟的00秒开始执行

比如

```shell
echo command ｜ at now + 10 minutes 
```

表示10分钟后运行，但严格意义上来讲，10分钟后是不精确的，因为`at`命令精确到分钟，在分钟的00秒开始执行。

比如现在时间是 `10:16:29`，理论执行时间应该在10分钟之后，也就是`10:26:29`，但实际上执行时间是`10:26:00`。

## at命令持久化

如果`at command`设定的任务，在任务指定时间到来之前，操作系统发生了重启，那么在重启后，`at command` 指定的时间到来的时候，命令是会正常运行的。

这是因为`at`把将来要执行的命令持久化了，写入了硬盘，如果中间发生了重启，`at`依然可以找到尚未执行的命令，在约定的时间到来之后，继续执行。

持久化的位置是（Ubuntu系统）：

```shell
root@Gavin:~# echo "echo haha >> future" |at  now + 10 minute
warning: commands will be executed using /bin/sh
job 1 at Thu Jun 20 14:02:00 2024
root@Gavin:~# cd /var/spool/cron/atjobs/
root@Gavin:/var/spool/cron/atjobs# ll
total 16
drwxrwx--T 2 daemon daemon 4096 Jun 20 13:52 ./
drwxr-xr-x 5 root   root   4096 Jun 20 13:42 ../
-rwx------ 1 root   daemon 3571 Jun 20 13:52 a0000101b5212a*
-rw------- 1 daemon daemon    6 Jun 20 13:52 .SEQ
root@Gavin:/var/spool/cron/atjobs# 
```

对于Ubuntu而言， `/var/spool/cron/atjobs` 是存放任务的文件夹。下面有一个文件`a0000101b5212a`， 这个文件是何意？

* 0 char， 表示`queue id`
* 1～5     16进制，表示`job id`
* 6～13    16 进制，等于 `expect_time/60`

取出来最后8位：

```shell
root@Gavin:/var/spool/cron/atjobs# printf %d 0x01b5212a
28647722root@Gavin:/var/spool/cron/atjobs# echo 28647722*60 |bc
1718863320
root@Gavin:/var/spool/cron/atjobs# date -d @1718863320
Thu Jun 20 02:02:00 PM CST 2024
root@Gavin:/var/spool/cron/atjobs#
```

将最后8位16进制转换成10进制，值为28647722。将28647722乘以60，即为任务应该执行的时间，timestamp为1718863320，转换成可读的时间，为：

```shell
Thu Jun 20 02:02:00 PM CST 2024
```

## at 命令执行文件

如果要执行的任务，写在了脚本里，可以采用如下方式：

```shell
at 02:00  -f /usr/local/bin/mysql_backup.sh
```

即02:00分，执行 `/usr/local/bin/mysql_backup.sh`脚本。


## at 任务查看、展开与删除

### 查看at任务

使用`at -l` 查看：

```shell
root@Gavin:~# at -l
2	Thu Jun 20 14:20:00 2024 a root
1	Thu Jun 20 14:02:00 2024 a root
3	Thu Jun 20 14:30:00 2024 a root
root@Gavin:~# 
```

第一列为`job id`。


### 展开at任务

使用`at -c job_id`命令，查看at详细任务信息：

```shell
root@Gavin:~# at -c 2
#!/bin/sh
# atrun uid=0 gid=0
# mail root 0
umask 22
JAVA_HOME=/usr/lib/jdk1.8.0_171; export JAVA_HOME
JRE_HOME=/usr/lib/jdk1.8.0_171/jre; export JRE_HOME
PWD=/root; export PWD
LOGNAME=root; export LOGNAME
XDG_SESSION_TYPE=tty; export XDG_SESSION_TYPE
HOME=/root; export HOME
LANG=en_US.UTF-8; export LANG
LS_COLORS=rs=0:di=01\;34:ln=01\;36:mh=00:pi=40\;33:so=01\;35:do=01\;35:bd=40\;33\;01:cd=40\;33\;01:or=40\;31\;01:mi=00:su=37\;41:sg=30\;43:ca=00:tw=30\;42:ow=34\;42:st=37\;44:ex=01\;32:\*.tar=01\;31:\*.tgz=01\;31:\*.arc=01\;31:\*.arj=01\;31:\*.taz=01\;31:\*.lha=01\;31:\*.lz4=01\;31:\*.lzh=01\;31:\*.lzma=01\;31:\*.tlz=01\;31:\*.txz=01\;31:\*.tzo=01\;31:\*.t7z=01\;31:\*.zip=01\;31:\*.z=01\;31:\*.dz=01\;31:\*.gz=01\;31:\*.lrz=01\;31:\*.lz=01\;31:\*.lzo=01\;31:\*.xz=01\;31:\*.zst=01\;31:\*.tzst=01\;31:\*.bz2=01\;31:\*.bz=01\;31:\*.tbz=01\;31:\*.tbz2=01\;31:\*.tz=01\;31:\*.deb=01\;31:\*.rpm=01\;31:\*.jar=01\;31:\*.war=01\;31:\*.ear=01\;31:\*.sar=01\;31:\*.rar=01\;31:\*.alz=01\;31:\*.ace=01\;31:\*.zoo=01\;31:\*.cpio=01\;31:\*.7z=01\;31:\*.rz=01\;31:\*.cab=01\;31:\*.wim=01\;31:\*.swm=01\;31:\*.dwm=01\;31:\*.esd=01\;31:\*.avif=01\;35:\*.jpg=01\;35:\*.jpeg=01\;35:\*.mjpg=01\;35:\*.mjpeg=01\;35:\*.gif=01\;35:\*.bmp=01\;35:\*.pbm=01\;35:\*.pgm=01\;35:\*.ppm=01\;35:\*.tga=01\;35:\*.xbm=01\;35:\*.xpm=01\;35:\*.tif=01\;35:\*.tiff=01\;35:\*.png=01\;35:\*.svg=01\;35:\*.svgz=01\;35:\*.mng=01\;35:\*.pcx=01\;35:\*.mov=01\;35:\*.mpg=01\;35:\*.mpeg=01\;35:\*.m2v=01\;35:\*.mkv=01\;35:\*.webm=01\;35:\*.webp=01\;35:\*.ogm=01\;35:\*.mp4=01\;35:\*.m4v=01\;35:\*.mp4v=01\;35:\*.vob=01\;35:\*.qt=01\;35:\*.nuv=01\;35:\*.wmv=01\;35:\*.asf=01\;35:\*.rm=01\;35:\*.rmvb=01\;35:\*.flc=01\;35:\*.avi=01\;35:\*.fli=01\;35:\*.flv=01\;35:\*.gl=01\;35:\*.dl=01\;35:\*.xcf=01\;35:\*.xwd=01\;35:\*.yuv=01\;35:\*.cgm=01\;35:\*.emf=01\;35:\*.ogv=01\;35:\*.ogx=01\;35:\*.aac=00\;36:\*.au=00\;36:\*.flac=00\;36:\*.m4a=00\;36:\*.mid=00\;36:\*.midi=00\;36:\*.mka=00\;36:\*.mp3=00\;36:\*.mpc=00\;36:\*.ogg=00\;36:\*.ra=00\;36:\*.wav=00\;36:\*.oga=00\;36:\*.opus=00\;36:\*.spx=00\;36:\*.xspf=00\;36:\*\~=00\;90:\*#=00\;90:\*.bak=00\;90:\*.old=00\;90:\*.orig=00\;90:\*.part=00\;90:\*.rej=00\;90:\*.swp=00\;90:\*.tmp=00\;90:\*.dpkg-dist=00\;90:\*.dpkg-old=00\;90:\*.ucf-dist=00\;90:\*.ucf-new=00\;90:\*.ucf-old=00\;90:\*.rpmnew=00\;90:\*.rpmorig=00\;90:\*.rpmsave=00\;90:; export LS_COLORS
SSH_CONNECTION=192.168.23.1\ 32889\ 192.168.23.129\ 22; export SSH_CONNECTION
LESSCLOSE=/usr/bin/lesspipe\ %s\ %s; export LESSCLOSE
XDG_SESSION_CLASS=user; export XDG_SESSION_CLASS
ANDROID_HOME=/usr/lib/android-sdk; export ANDROID_HOME
LESSOPEN=\|\ /usr/bin/lesspipe\ %s; export LESSOPEN
USER=root; export USER
SHLVL=1; export SHLVL
XDG_SESSION_ID=191; export XDG_SESSION_ID
CLASSPATH=.:/usr/lib/jdk1.8.0_171/lib:/usr/lib/jdk1.8.0_171/jre/lib; export CLASSPATH
XDG_RUNTIME_DIR=/run/user/0; export XDG_RUNTIME_DIR
SSH_CLIENT=192.168.23.1\ 32889\ 22; export SSH_CLIENT
DEBUGINFOD_URLS=https://debuginfod.ubuntu.com\ ; export DEBUGINFOD_URLS
XDG_DATA_DIRS=/usr/share/gnome:/usr/local/share:/usr/share:/var/lib/snapd/desktop; export XDG_DATA_DIRS
PATH=/usr/lib/android-sdk/tools:/usr/lib/android-sdk/platform-tools:/usr/lib/jdk1.8.0_171/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin; export PATH
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/0/bus; export DBUS_SESSION_BUS_ADDRESS
SSH_TTY=/dev/pts/6; export SSH_TTY
OLDPWD=/var/spool/cron/atjobs; export OLDPWD
cd /root || {
	 echo 'Execution directory inaccessible' >&2
	 exit 1
}
echo haha >> future

root@Gavin:~#
```

### 删除at任务

使用`atrm job_id`删除对应`job id`的`at`任务：

```shell
root@Gavin:~# at -l
2	Thu Jun 20 14:20:00 2024 a root
1	Thu Jun 20 14:02:00 2024 a root
3	Thu Jun 20 14:30:00 2024 a root
root@Gavin:~# atrm 1
root@Gavin:~# at -l
2	Thu Jun 20 14:20:00 2024 a root
3	Thu Jun 20 14:30:00 2024 a root
root@Gavin:~#
```

# Overall

使用 `at` 命令安排一次性定时任务是一种简单而有效的方法，适用于需要在将来某个时间点执行的任务。

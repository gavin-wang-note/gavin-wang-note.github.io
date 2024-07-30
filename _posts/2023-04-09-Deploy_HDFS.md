---
layout:     post
title:      "Linux下部署HDFS"
subtitle:   "Deploy HDFS"
date:       2023-04-09
author:     "Gavin Wang"
catalog:    true
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: Linux下部署HDFS详细安装过程
categories:
    - [HDFS]
    - [HadoopFS]
tags:
    - HDFS
    - HadoopFS
---



# HDFS 安装部署

## 一、系统浅析

HDFS是Hadoop生态下的分布式文件系统, 其中，DataNode和NameNode是HDFS的两大核心。

NameNode（名称节点）：

保存整个文件系统的目录信息、文件信息及分块信息，如果主 NameNode 失效，切换到Secondary NameNode。

NameNode管理文件系统的命名空间，它维护着文件系统树及整棵树内所有的文件和目录，即元数据（MetaData）。

如果NameNode不可用，那么等同于整个HDFS文件系统不可用。如果NameNode由于故障导致磁盘数据丢失，那么等同于整个HDFS文件系统数据丢失。如果NameNode块映射关系的内存爆满，那么等同于整个HDFS文件系统无法再继续存储，也就是意味着NameNode内存决定了HDFS能够存储的块数量。

DataNode（数据节点）：

分布在廉价的计算机上，用于存储Block块文件。 DataNode角色的节点是真正存放块（block）数据的节点，当DataNode启动时，它将扫描其本地文件系统，生成与每个本地文件相对应的所有HDFS数据块的列表，并将此报告发送到NameNode。该报告称为BlockReport。 

现在需要将hdfs部署在我司scaler之上。即可以通过 HDFS客户端上载文件，然后底层存储接入scaler，以scaler存储HDFS数据。

## 二、scaler 集群部署

本文以scaler 8.3 版本详细说明HDFS部署在scaler上的操作过程。

1、创建集群

关于scaler 8.3部分的部署暂不描述。

2、创建pool hdfs

3、将pool hdfs 加入cephfs data pool

4、新建sharefolder，名字为hdfs

5、在hdfs下创建文件夹备HDFS的namenode、datanode、jornalnode使用

```shell
root@host11:/var/share/ezfs/shareroot/hdfs# mkdir host11 host12 host13
root@host11:/var/share/ezfs/shareroot/hdfs# mkdir -p host11/name host11/data host11/jn
root@host11:/var/share/ezfs/shareroot/hdfs# mkdir -p host12/name host12/data host12/jn
root@host11:/var/share/ezfs/shareroot/hdfs# mkdir -p host13/name host13/data host13/jn
查看目录结构：
root@host11:/var/share/ezfs/shareroot/hdfs# tree
├── host11
│   ├── data
│   └── name
│   └── jn
├── host12
│   ├── data
│   └── name
│   └── jn
├── host13
│   ├── data
│   └── name
│   └── jn
```

 

## 三、HDFS部署

### 1、hadoop下载

```shell
wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.2/hadoop-3.3.2.tar.gz
```

### 2、解压

在所有节点上解压hadoop包， 命令如下

```shell
tar -zxvf hadoop-3.3.2.tar.gz -C /usr/local/
```

### 3、重命名

在所有节点上重命名hadoop

```shell
onnode all mv /usr/local/hadoop-3.3.2 /usr/local/hadoop
 
```

### 4、环境变量配置

Hadoop安装时需要配置一些环境变量，如指定HADOOP_HOME位置，指定java环境变量等，主要集中在两个配置文件中。

修改/etc/profile配置

```shell
vim /etc/profile
# 添加如下配置
export HADOOP_HOME=/usr/local/hadoop
export PATH=.:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin:$PATH
# export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
# export PATH=$JAVA_HOME/bin:$PATH
# export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
 
```

加载环境变量


```shell
source /etc/profile
```

 

修改hadoop-env.sh配置

hadoop-env.sh为hadoop运行环境定义hadoop运行环境相关的配置信息

```shell
vim /usr/local/hadoop/etc/hadoop/hadoop-env.sh
# 添加如下配置
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre/
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop
export HADOOP_SECURE_LOG=/var/log/hdfs
export HADOOP_ROOT_LOGGER=INFO,console
export HADOOP_DAEMON_ROOT_LOGGER=INFO,RFA
export HADOOP_SECURITY_LOGGER=INFO,NullAppender
export HADOOP_AUDIT_LOGGER=INFO,NullAppender
export HDFS_NAMENODE_OPTS="-Dhadoop.security.logger=INFO,RFAS"
export HDFS_SECONDARYNAMENODE_OPTS="-Dhadoop.security.logger=INFO,RFAS"
```

 

修改dev_env.sh配置

```shell
vim /etc/profile.d/dev_env.sh
# 添加如下配置
export HADOOP_HOME=/usr/local/hadoop
export PATH=.:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin:$PATH
 
```

以上配置文件完成，需要同步复制到其它所有节点

### 5、修改目录权限

用户名及用户组

```shell
chown -R root /usr/local/hadoop
chgrp -R root /usr/local/hadoop
```

### 6、验证

```shell
root@host12:/usr/local/hadoop/etc/hadoop#  hadoop version
Hadoop 3.3.2
Source code repository git@github.com:apache/hadoop.git -r 0bcb014209e219273cb6fd4152df7df713cbac61
Compiled by chao on 2022-02-21T18:39Z
Compiled with protoc 3.7.1
From source with checksum 4b40fff8bb27201ba07b6fa5651217fb
This command was run using /usr/local/hadoop/share/hadoop/common/hadoop-common-3.3.2.jar
```

如上提示即为配置成功

### 7、修改HDFS配置文件

Hadoop所有的配置文件都存在于安装目录下的etc/hadoop中，需要修改如下配置文件

#### 7.1、core-site.xml配置

core-site.xml：集群全局参数，用于定义系统级别的参数，如HDFS URL 、Hadoop的临时目录等 

·    fs.defaultFS：HDFS的默认访问路径。 

·    hadoop.tmp.dir：Hadoop临时文件的存放目录，可自定义。

```shell
vim /usr/local/hadoop/etc/hadoop/core-site.xml

<configuration>
   <property>
       <name>fs.defaultFS</name>
       <value>hdfs://mycluster</value> 
   </property>
   <property>
       <name>hadoop.tmp.dir</name>
       <value>/usr/local/hadoop/tmp</value>
   </property>
   <property>
       <name>ha.zookeeper.quorum</name>
       <value>host11:2181,host12:2181,host13:2181</value>
   </property>
</configuration>
 
```

#### 7.2、修改hdfs hdfs-site.xml配置

hdfs-site.xml HDFS 如名称节点和数据节点的存放位置、文件副本的个数、文件的读取权限等

```shell
vim /usr/local/hadoop/etc/hadoop/hdfs-site.xml

<configuration>
    <!-- 定义集群名称 -->
    <property>
        <name>dfs.nameservices</name>
        <value>mycluster</value>
    </property>
    <!-- 定义集群中NameNode节点 -->
    <property>
        <name>dfs.ha.namenodes.mycluster</name>
        <value>nn1,nn2,nn3</value>
    </property>
    <!-- nn1的RPC通信地址 host11为实际机器的hostname -->
    <property>
        <name>dfs.namenode.rpc-address.mycluster.nn1</name>
        <value>host11:9000</value>
    </property>
    <!-- nn2的RPC通信地址 host12为实际机器的hostname -->
    <property>
        <name>dfs.namenode.rpc-address.mycluster.nn2</name>
        <value>host12:9000</value>
    </property>
    <!-- nn3的RPC通信地址 host13为实际机器的hostname -->
    <property>
        <name>dfs.namenode.rpc-address.mycluster.nn3</name>
        <value>host13:9000</value>
    </property>
    <!-- nn1的http通信地址  host11为实际机器的hostname-->
    <property>
        <name>dfs.namenode.http-address.mycluster.nn1</name>
        <value>host11:50070</value>
    </property>
    <!-- nn2的http通信地址 host12为实际机器的hostname-->
    <property>
        <name>dfs.namenode.http-address.mycluster.nn2</name>
        <value>host12:50070</value>
    </property>
    <!-- nn3的http通信地址 host13为实际机器的hostname -->
    <property>
        <name>dfs.namenode.http-address.mycluster.nn3</name>
        <value>host13:50070</value>
    </property>
    <!-- 指定NameNode元数据在JournalNode上的存放位置 hostname以实际配置为准 -->
    <property>
        <name>dfs.namenode.shared.edits.dir</name>
        <value>qjournal://host11:8485;host12:8485;host13:8485/mycluster</value>
    </property>
    <!-- 配置隔离机制，即同一时刻只能有一台服务器对外响应 -->
    <property>
        <name>dfs.ha.fencing.methods</name>
        <value>sshfence</value>
    </property>
    <!-- 使用隔离机制时需要ssh无秘钥登录-->
    <property>
        <name>dfs.ha.fencing.ssh.private-key-files</name>
        <value>/root/.ssh/id_rsa</value>
    </property>
    <!-- 1、声明journalnode服务器存储目录 目录结构在上文中已经创建，如果不创建则会报错
         2、/host11/jn， 每个节点都需要修改为自己节点hostname，三个节点各不相同
    -->
    <property>
        <name>dfs.journalnode.edits.dir</name>
        <value>/var/share/ezfs/shareroot/hdfs/host11/jn</value>
    </property>
    <!-- 关闭权限检查-->
    <property>
        <name>dfs.permissions.enable</name>
        <value>false</value>
    </property>
    <!-- 访问代理类：client，mycluster，active配置失败自动切换实现方式-->
    <property>
        <name>dfs.client.failover.proxy.provider.mycluster</name>             
        <value>org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider</value>
    </property>
    <!-- namenode存储目录，每个节点各不相同，目录结构已经在上文中创建-->
    <property>
        <name>dfs.name.dir</name>
        <value>/var/share/ezfs/shareroot/hdfs/host11/name</value>
    </property>
    <!--DateNode存储目录，没有则新建-->
    <property>
        <name>dfs.data.dir</name>
        <value>/var/share/ezfs/shareroot/hdfs/host11/data</value>
    </property>
    <!--文件在HDFS系统中的副本数-->
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>
    <property>
        <name>hadoop.http.staticuser.user</name>
        <value>root</value>
    </property>
    <property>
        <name>dfs.ha.automatic-failover.enabled</name>
        <value>true</value>
    </property>
</configuration>
 
```

#### 7.3、修改启停配置

修改启动的配置文件：start-dfs.sh

```shell
vim /usr/local/hadoop/sbin/start-dfs.sh
# 添加如下配置
HDFS_DATANODE_USER=root
HADOOP_SECURE_USER=root
HDFS_NAMENODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root
HDFS_ZKFC_USER=root
HDFS_JOURNALNODE_USER=root

```

修改停用的配置文件：stop-dfs.sh

```shell
vim /usr/local/hadoop/sbin/stop-dfs.sh
# 添加如下配置
HDFS_DATANODE_USER=root
HADOOP_SECURE_USER=root
HDFS_NAMENODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root
HDFS_ZKFC_USER=root
HDFS_JOURNALNODE_USER=root
 
```

#### 7.4、workers 设置

```shell
vim /usr/local/hadoop/etc/hadoop/workers
host11
host12
host13
# 以实际机器的hostname为准
 
```

#### 7.5、hosts设置

服务器端host配置

```shell
vim /etc/hosts
172.17.73.11 host11
172.17.73.12 host12
172.17.73.13 host13
# 需要把127.0.1.1 注释掉，否则后面会出错。
# 以实际机器的hostname为准

```

#### 7.6、创建软件链接

```shell
onnode all ln -s /usr/share/elasticsearch/jdk/bin/jps /bin/jps
 
```

## 四、zookeeper部分：

### 1、解压

```shell
tar -zxvf /home/btadmin/zookeeper.tar.gz -C /usr/local
 
```

### 2、创建文件夹

```shell
mkdir -p /usr/local/zookeeper/zkData
 
```

### 3、修改文件名

```shell
mv /usr/local/zookeeper/conf/zoo_sample.cfg /usr/local/zookeeper/conf/zoo.cfg
```

### 4、修改文件zoo.cfg

```shell
vim /usr/local/zookeeper/conf/zoo.cfg

#添加如下配置

dataDir=/usr/local/zookeeper/zkData/
server.1=host11:2888:3888
server.2=host12:2888:3888
server.3=host13:2888:3888
 
admin.serverPort=8085
 
```

###   5、修改目录权限

用户名及用户组

```shell
chown -R root /usr/local/zookeeper
chgrp -R root /usr/local/zookeeper
```

### 6、修改文件myid文件

在多个节点上分别配置myid文件，序号依次增加

在第一个节点值为1

```shell
vim /usr/local/zookeeper/zkData/myid
1
```

在第二个节点值为2

```shell
vim /usr/local/zookeeper/zkData/myid
2
```

在第三个节点值为3

```shell
vim /usr/local/zookeeper/zkData/myid
3
```

## 五、启动集群

HDFS HA配置完成后，下面我们将集群启动

### 1、先启动zookeeper集群

```shell
# 在所有节点分别执行如下命令：
/usr/local/zookeeper/bin/zkServer.sh start
 
# 在第一个节点执行如下命令：
hdfs zkfc -formatZK
 
# 在所有节点执行如下命令：
hdfs --daemon start zkfc
```

执行成功后可看：

```shell
root@host13:/home/btadmin# jps
180491 Jps
154684 DFSZKFailoverController
 
# 看到DFSZKFailoverController表示启动成功
```

### 2、启动HDFS

删除各个节点的$HADOOP_HOME/tmp目录下的所有文件（如果是新建环境不需要此步）

在各个节点分别执行下面命令，启动三台JournalNode ：

```shell
hdfs --daemon start journalnode
```


 启动结果如下

```shell
root@host11:/usr/local/hadoop/sbin# jps
494797 JournalNode
 
# 表示JournalNode启动成功
```

### 3、格式化namenode

只在第一个节点上执行namenode格式化。

注意：如果没有启动JournalNode，格式化将失败

```shell
hdfs namenode -format
 
```

出现如下输出代表格式化成功：

```shell
2023-04-21 13:51:54,909 INFO util.GSet: 0.25% max memory 1.7 GB = 4.4 MB
2023-04-21 13:51:54,909 INFO util.GSet: capacity      = 2^19 = 524288 entries
2023-04-21 13:51:54,927 INFO metrics.TopMetrics: NNTop conf: dfs.namenode.top.window.num.buckets = 10
2023-04-21 13:51:54,927 INFO metrics.TopMetrics: NNTop conf: dfs.namenode.top.num.users = 10
2023-04-21 13:51:54,927 INFO metrics.TopMetrics: NNTop conf: dfs.namenode.top.windows.minutes = 1,5,25
2023-04-21 13:51:54,932 INFO namenode.FSNamesystem: Retry cache on namenode is enabled
2023-04-21 13:51:54,932 INFO namenode.FSNamesystem: Retry cache will use 0.03 of total heap and retry cache entry expiry time is 600000 millis
2023-04-21 13:51:54,934 INFO util.GSet: Computing capacity for map NameNodeRetryCache
2023-04-21 13:51:54,934 INFO util.GSet: VM type       = 64-bit
2023-04-21 13:51:54,934 INFO util.GSet: 0.029999999329447746% max memory 1.7 GB = 538.1 KB
2023-04-21 13:51:54,934 INFO util.GSet: capacity      = 2^16 = 65536 entries
2023-04-21 13:51:56,366 INFO namenode.FSImage: Allocated new BlockPoolId: BP-1632620897-127.0.1.1-1682056316366
2023-04-21 13:51:56,461 INFO common.Storage: Storage directory /var/share/ezfs/shareroot/hdfs/host11/name has been successfully formatted.
2023-04-21 13:51:57,003 INFO namenode.FSImageFormatProtobuf: Saving image file /var/share/ezfs/shareroot/hdfs/host11/name/current/fsimage.ckpt_0000000000000000000 using no compression
2023-04-21 13:51:57,139 INFO namenode.FSImageFormatProtobuf: Image file /var/share/ezfs/shareroot/hdfs/host11/name/current/fsimage.ckpt_0000000000000000000 of size 399 bytes saved in 0 seconds .
2023-04-21 13:51:57,171 INFO namenode.NNStorageRetentionManager: Going to retain 1 images with txid >= 0
2023-04-21 13:51:57,230 INFO namenode.FSNamesystem: Stopping services started for active state
2023-04-21 13:51:57,231 INFO namenode.FSNamesystem: Stopping services started for standby state
2023-04-21 13:51:57,235 INFO namenode.FSImage: FSImageSaver clean checkpoint: txid=0 when meet shutdown.
2023-04-21 13:51:57,235 INFO namenode.NameNode: SHUTDOWN_MSG: 
/************************************************************
SHUTDOWN_MSG: Shutting down NameNode at host11/127.0.0.1
************************************************************
```

### 4、启动第一个节点的namenode

注意：namenode在启动前必须执行格式化namenode操作，如果不执行，则启动namenode操作失败

如果先启动namenode失败后，需要再格式化namenode的话，需要把name data jn文件夹下的内容全部删除，/tmp/下hadoop部分的内容删除后，格式化namenode才能成功

在第一个节点启动namenode， 启动namenode后会生成images元数据

```shell
hdfs --daemon start namenode
```

### 5、启动第二，三个节点的bootstrapStandby

在启动第二，三节点的namenode之前 ，需要先执行同步数据操作，将第一个节点上的NameNode元数据拷贝到第二个，第三个节点上。命令如下：

```shell
hdfs namenode -bootstrapStandby
```

输出以下信息代表拷贝成功：

```shell
18/03/15 14:28:01 INFO common.Storage: Storage directory /opt/modules/hadoop-2.7.1/tmp/dfs/name has been successfully formatted.
```

启动第二，三节点namenode，命令如下

```shell
hdfs --daemon start namenode
```

### 6、启动所有节点的datanode

在所有节点上启动datanode

```shell
hdfs --daemon start datanode
```

 

### 7、切换nn1为namenode active

```shell
hdfs haadmin -transitionToActive nn1
```

 

### 8、确认服务状态

```shell
onnode all jps
 
>> NODE: 10.10.10.11 <<
439493 Jps
416240 DataNode
377026 DFSZKFailoverController
380124 JournalNode
368555 QuorumPeerMain
421097 NameNode
 
>> NODE: 10.10.10.12 <<
218659 Jps
163971 JournalNode
213088 DataNode
178596 NameNode
161803 DFSZKFailoverController
155512 QuorumPeerMain
 
>> NODE: 10.10.10.13 <<
206103 DataNode
156919 JournalNode
209579 NameNode
148043 QuorumPeerMain
154684 DFSZKFailoverController
209885 Jps
```

至此，HDAP集群搭建完成

## 六、客户端配置

修改客户端hosts配置文件：

打开文件c:\Windows\System32\drivers\etc\hosts

```shell
172.17.73.11 host11
172.17.73.12 host12
172.17.73.13 host13
```



## 七、HDFS使用

使用浏览器打开HDFS 客户端

```shell
http://172.17.73.11:50070/
```

<img class="shadow" src="/img/in-post/HDFS-1.png" width="1200">

可以看到当前节点是NN1且处于active状态

上传文件，打开如下界面

<img class="shadow" src="/img/in-post/HDFS-2.png" width="1200">

<img class="shadow" src="/img/in-post/HDFS-3.png" width="1200">

上传文件后如下：

<img class="shadow" src="/img/in-post/HDFS-4.png" width="1200">

上传成功！

 

## 八、遇到问题及解决方法

问题1、第二或第三个节点执行BootstrapStandby 格式无法成功。 显示如下

```shell
2023-04-21 13:55:00,314 INFO ipc.Client: Retrying connect to server: host11/172.17.73.11:9000. Already tried 0 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)
2023-04-21 13:55:01,315 INFO ipc.Client: Retrying connect to server: host11/172.17.73.11:9000. Already tried 1 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)
2023-04-21 13:55:02,316 INFO ipc.Client: Retrying connect to server: host11/172.17.73.11:9000. Already tried 2 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)
2023-04-21 13:55:03,317 INFO ipc.Client: Retrying connect to server: host11/172.17.73.11:9000. Already tried 3 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)
2023-04-21 13:55:04,319 INFO ipc.Client: Retrying connect to server: host11/172.17.73.11:9000. Already tried 4 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)
2023-04-21 13:55:05,320 INFO ipc.Client: Retrying connect to server: host11/172.17.73.11:9000. Already tried 5 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)
2023-04-21 13:55:06,322 INFO ipc.Client: Retrying connect to server: host11/172.17.73.11:9000. Already tried 6 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)
2023-04-21 13:55:07,323 INFO ipc.Client: Retrying connect to server: host11/172.17.73.11:9000. Already tried 7 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)
2023-04-21 13:55:08,324 INFO ipc.Client: Retrying connect to server: host11/172.17.73.11:9000. Already tried 8 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)
2023-04-21 13:55:09,326 INFO ipc.Client: Retrying connect to server: host11/172.17.73.11:9000. Already tried 9 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)
2023-04-21 13:55:09,335 WARN ha.BootstrapStandby: Unable to fetch namespace information from remote NN at host11/172.17.73.11:9000: Call From host15/172.17.73.15 to host11:9000 failed on connection exception: java.net.ConnectException: Connection refused; For more details see:  http://wiki.apache.org/hadoop/ConnectionRefused
2023-04-21 13:55:19,352 WARN ha.BootstrapStandby: Unable to fetch namespace information from remote NN at host16/172.17.73.16:9000: Call From host15/172.17.73.12 to host16:9000 failed on connection exception: java.net.ConnectException: Connection refused; For more details see:  http://wiki.apache.org/hadoop/ConnectionRefused
2023-04-21 13:55:19,353 ERROR ha.BootstrapStandby: Unable to fetch namespace information from any remote NN. Possible NameNodes: [RemoteNameNodeInfo [nnId=nn1, ipcAddress=host11/172.17.73.11:9000, httpAddress=http://host11:50070], RemoteNameNodeInfo [nnId=nn3, ipcAddress=host16/172.17.73.16:9000, httpAddress=http://host16:50070]]
2023-04-21 13:55:19,357 INFO util.ExitUtil: Exiting with status 2: ExitException
2023-04-21 13:55:19,360 INFO namenode.NameNode: SHUTDOWN_MSG: 
/************************************************************
SHUTDOWN_MSG: Shutting down NameNode at host12/172.17.73.12
************************************************************/

```

解决：

查看端口的使用情况，发现请求的9000端口使用情况如下：

```shell
root@host11:/tmp# lsof -i:9000
COMMAND    PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
java    498909 root  330u  IPv4 689923      0t0  TCP 127.0.1.1:9000 (LISTEN)
端口的ip是127.0.1.1
```

进一步查原因，发现/etc/hosts里host11的ip是127.0.1.1，而请求的是172.17.13.11

把/etc/hosts里127.0.1.1注释掉。重启node1

然后按顺序重新启动journalnode. namenode

再次查看

```shell
root@host11:/usr/local/hadoop/sbin# lsof -i:9000
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
java 
```

结果正常


问题二：无法上传文件，如下

<img class="shadow" src="/img/in-post/HDFS-5.png" width="1200">

解决方法：

```shell
root@host11:/usr/local/hadoop/sbin# hdfs haadmin -getServiceState nn2
active
 
```

从UI上登录active节点即可


<img class="shadow" src="/img/in-post/HDFS-6.png" width="1200">

问题三：上传文件失败

<img class="shadow" src="/img/in-post/HDFS-7.png" width="1200">

解决方法：

客户端没有配置host

打开文件c:\Windows\System32\drivers\etc\hosts

添加三个节点的host

```shell
172.17.73.11 host11
172.17.73.12 host12
172.17.73.13 host13
```

再次尝试

<img class="shadow" src="/img/in-post/HDFS-8.png" width="1200">


文件上传成功！

 

问题四：启动zookeeper失败

bug现象：

<img class="shadow" src="/img/in-post/HDFS-9.png" width="1200">

log：

```shell
2023-04-24 14:37:11,952 [myid:] - WARN  [main:ConstraintSecurityHandler@759] - ServletContext@o.e.j.s.ServletContextHandler@1b68ddbd{/,null,STARTING} has uncovered http methods for path: /*
2023-04-24 14:37:11,961 [myid:] - INFO  [main:ContextHandler@915] - Started o.e.j.s.ServletContextHandler@1b68ddbd{/,null,AVAILABLE}
2023-04-24 14:37:11,970 [myid:] - ERROR [main:ZooKeeperServerMain@86] - Unable to start AdminServer, exiting abnormally
org.apache.zookeeper.server.admin.AdminServer$AdminServerException: Problem starting AdminServer on address 0.0.0.0, port 8080 and command URL /commands
        at org.apache.zookeeper.server.admin.JettyAdminServer.start(JettyAdminServer.java:188)
        at org.apache.zookeeper.server.ZooKeeperServerMain.runFromConfig(ZooKeeperServerMain.java:155)
        at org.apache.zookeeper.server.ZooKeeperServerMain.initializeAndRun(ZooKeeperServerMain.java:113)
        at org.apache.zookeeper.server.ZooKeeperServerMain.main(ZooKeeperServerMain.java:68)
        at org.apache.zookeeper.server.quorum.QuorumPeerMain.initializeAndRun(QuorumPeerMain.java:141)
        at org.apache.zookeeper.server.quorum.QuorumPeerMain.main(QuorumPeerMain.java:91)
Caused by: java.io.IOException: Failed to bind to /0.0.0.0:8080
        at org.eclipse.jetty.server.ServerConnector.openAcceptChannel(ServerConnector.java:349)
        at org.eclipse.jetty.server.ServerConnector.open(ServerConnector.java:310)
        at org.eclipse.jetty.server.AbstractNetworkConnector.doStart(AbstractNetworkConnector.java:80)
        at org.eclipse.jetty.server.ServerConnector.doStart(ServerConnector.java:234)
        at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:73)
        at org.eclipse.jetty.server.Server.doStart(Server.java:401)
        at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:73)
        at org.apache.zookeeper.server.admin.JettyAdminServer.start(JettyAdminServer.java:179)
        ... 5 more
Caused by: java.net.BindException: Address already in use
        at sun.nio.ch.Net.bind0(Native Method)
        at sun.nio.ch.Net.bind(Net.java:461)
        at sun.nio.ch.Net.bind(Net.java:453)
        at sun.nio.ch.ServerSocketChannelImpl.bind(ServerSocketChannelImpl.java:222)
        at sun.nio.ch.ServerSocketAdaptor.bind(ServerSocketAdaptor.java:85)
        at org.eclipse.jetty.server.ServerConnector.openAcceptChannel(ServerConnector.java:344)
        ... 12 more
Unable to start AdminServer, exiting abnormally
 
```

原因：

端口占用是8080…

解决办法：

在zoo.cfg中增加admin.serverPort=没有被占用的端口号


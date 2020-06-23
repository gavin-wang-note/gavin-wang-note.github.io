---
layout:     post
title:      "基于Robot Framework做VirtualStore的自动化"
subtitle:   "Robot Framework automation for VirtualStore"
date:       2016-04-11
author:     "Gavin"
catalog:    true
tags:
    - robotframework
    - Automation
---


## ENV



| **Type**    | **Version**                      | **Desc**                                                     |
| ----------- | -------------------------------- | ------------------------------------------------------------ |
| **OS**      | Ubuntu 16.04                     | Need lib higher  libc lib/python/apache, out storage ISO not match |
| **Jenkins** | 2.32.3                           | Jenkins                                                      |
| **RF**      | 3.0.2 (Python  2.7.12 on linux2) | Robot framework,  used for running RF testcases              |

 

 

## Install Jenkins



### install Jenkins




```
jenkins@jenkins:~$ wget -q -O - https://jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -
OK
jenkins@jenkins:~$ sudo sh -c 'echo deb http://pkg.jenkins-ci.org/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
jenkins@jenkins:~$
sudo apt-get update 
sudo apt-get install jenkins 
```



### Check Jenkins service status




```
jenkins@jenkins:~$ sudo service jenkins status

● jenkins.service - LSB: Start Jenkins at boot time
  Loaded: loaded (/etc/init.d/jenkins; bad; vendor preset: enabled)
  Active: active (exited) since 五 2017-03-03 18:03:06 CST; 46s ago
   Docs: man:systemd-sysv-generator(8)

3月 03 18:03:05 jenkins systemd[1]: Starting LSB: Start Jenkins at boot time...
3月 03 18:03:05 jenkins jenkins[5041]: * Starting Jenkins Continuous Integration Server jenkins
3月 03 18:03:05 jenkins su[5059]: Successful su for jenkins by root
3月 03 18:03:05 jenkins su[5059]: + ??? root:jenkins
3月 03 18:03:05 jenkins su[5059]: pam_unix(su:session): session opened for user jenkins by (uid=0)
3月 03 18:03:06 jenkins jenkins[5041]:  ...done.
3月 03 18:03:06 jenkins systemd[1]: Started LSB: Start Jenkins at boot time.
```



### jenkins path



```
Access path：http://localhost:8080 
Installed path：/var/lib/jenkins 
Log path：/var/log/jenkins
Create a project directory in Jenkins installation directory of the jobs.
```



### First login Jenkins UI




###### Getting Started


<img class="shadow" src="/img/in-post/rf/clip_image002.jpg" width="1200">

 

###### after input Administrator password

<img class="shadow" src="/img/in-post/rf/clip_image004.jpg" width="1200">

 

###### Select “Install suggested plugins”

<img class="shadow" src="/img/in-post/rf/clip_image006.jpg" width="1200">

 

###### Create First Admin User

<img class="shadow" src="/img/in-post/rf/clip_image008.jpg" width="1200">

 

<img class="shadow" src="/img/in-post/rf/clip_image010.jpg" width="1200">

 

###### Save and Finish

<img class="shadow" src="/img/in-post/rf/clip_image012.jpg" width="1200">

 

Login Jenkins UI

<img class="shadow" src="/img/in-post/rf/clip_image014.jpg" width="1200">

 

<img class="shadow" src="/img/in-post/rf/clip_image016.jpg" width="1200">

 

## install RF and Third library

 

### Install Robotframework



##### install RF



```
sudo apt-get install python-pip
sudo pip install --upgrade pip
sudo pip install robotframework
```



##### install RF library



```
sudo apt-get install python-wxgtk*
sudo pip install robotframework-ride
sudo pip install --upgrade robotframework-httplibrary
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
#此步骤如果不执行，会出现安装cryptography失败，具体错误参考“setup cryptography failed”章节的内容。
sudo pip install --upgrade robotframework-SSHLibrary
```



##### other package



```
sudo apt-get install sshpass
sudo apt-get install open-iscsi
sudo apt-get install fio
```



##### Problems encountered



###### setup cryptography failed



```
  writing top-level names to src/cryptography.egg-info/top_level.txt
  writing dependency_links to src/cryptography.egg-info/dependency_links.txt
  writing entry points to src/cryptography.egg-info/entry_points.txt
  reading manifest file 'src/cryptography.egg-info/SOURCES.txt'
  reading manifest template 'MANIFEST.in'
  no previously-included directories found matching 'docs/_build'
  warning: no previously-included files matching '*' found under directory 'vectors'
  writing manifest file 'src/cryptography.egg-info/SOURCES.txt'
  running build_ext
  generating cffi module 'build/temp.linux-x86_64-2.7/_padding.c'
  creating build/temp.linux-x86_64-2.7
  generating cffi module 'build/temp.linux-x86_64-2.7/_constant_time.c'
  generating cffi module 'build/temp.linux-x86_64-2.7/_openssl.c'
  building '_openssl' extension
  creating build/temp.linux-x86_64-2.7/build
  creating build/temp.linux-x86_64-2.7/build/temp.linux-x86_64-2.7
  x86_64-linux-gnu-gcc -pthread -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fno-strict-aliasing -Wdate-time -D_FORTIFY_SOURCE=2 -g -fstack-protector-strong -Wformat -Werror=format-security -fPIC -I/usr/include/python2.7 -c build/temp.linux-x86_64-2.7/_openssl.c -o build/temp.linux-x86_64-2.7/build/temp.linux-x86_64-2.7/_openssl.o
  build/temp.linux-x86_64-2.7/_openssl.c:434:30: fatal error: openssl/opensslv.h: No such file or directory
  compilation terminated.
  **error: command 'x86_64-linux-gnu-gcc' failed with exit status 1**
  

 ----------------------------------------
Command "/usr/bin/python -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-CbMI0T/cryptography/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-T5kRVj-record/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-build-CbMI0T/cryptography/

Reference resources：
  https://cryptography.io/en/latest/installation/#building-cryptography-on-linux

```

 

### Modify HttpLibrary code



##### Linux


```
vi /usr/local/lib/python2.7/dist-packages/HttpLibrary/__init__.py

Increase the following records, global cancelled certificate verification：

import ssl

ssl._create_default_https_context = ssl._create_unverified_context
```


##### Windows


```
  Modify file of C:\Python27\Lib\site-packages\HttpLibrary\__init__.py, increase the following records, global cancelled certificate verification：

import ssl

ssl._create_default_https_context = ssl._create_unverified_context
```




## Running RF test cases



### Case execution condition

```

1. 3 nodes cluster, each node of disk space is greater than 8G

2. Each node disk/vdisk numbers shall not be less than 4 (> = 4)
```




 instructions:

```
 This part of the inspection is in test case of rf-automation\testcase\01_Create_Cluster\Prepare Cluster.robot\01_ENV_Check
```




### Problems encountered



###### 1. SSL certificate verify failed




When running RF test case, occur SSLcertificate verify failed issue:



<img class="shadow" src="/img/in-post/rf/clip_image018.jpg" width="1200">

 

The solution：



  Refer to the "Modify HttpLibrary code" section. Here only capture the record, if don't modify this problem will appear.

 



###### 2. Wait Until Keyword Succeeds occur CannotSendRequest



<img class="shadow" src="/img/in-post/rf/clip_image020.jpg" width="1200">


```
20160516 13:55:43.636 : INFO : ${osd_state} = OFFLINE

20160516 13:55:43.637 : INFO : 

Argument types are:

<type 'str'>

<type 'unicode'>

20160516 13:55:43.637 : FAIL : OFFLINE != ONLINE

20160516 13:55:48.649 : FAIL : BadStatusLine: ''

20160516 13:55:53.656 : FAIL : CannotSendRequest

20160516 13:55:58.674 : FAIL : CannotSendRequest

20160516 13:56:03.679 : FAIL : CannotSendRequest

20160516 13:56:08.685 : FAIL : CannotSendRequest

20160516 13:56:13.695 : FAIL : CannotSendRequest

20160516 13:56:18.704 : FAIL : CannotSendRequest

20160516 13:56:23.718 : FAIL : CannotSendRequest

20160516 13:56:28.726 : FAIL : CannotSendRequest

20160516 13:56:33.742 : FAIL : CannotSendRequest

20160516 13:56:38.762 : FAIL : CannotSendRequest

20160516 13:56:43.780 : FAIL : CannotSendRequest

20160516 13:56:48.799 : FAIL : CannotSendRequest

20160516 13:56:53.817 : FAIL : CannotSendRequest

20160516 13:56:58.836 : FAIL : CannotSendRequest

20160516 13:57:03.852 : FAIL : CannotSendRequest

20160516 13:57:08.867 : FAIL : CannotSendRequest

20160516 13:57:13.881 : FAIL : CannotSendRequest

20160516 13:57:18.890 : FAIL : CannotSendRequest

20160516 13:57:23.898 : FAIL : CannotSendRequest

20160516 13:57:28.912 : FAIL : CannotSendRequest

20160516 13:57:33.921 : FAIL : CannotSendRequest

20160516 13:57:38.936 : FAIL : CannotSendRequest

20160516 13:57:43.952 : FAIL : CannotSendRequest

20160516 13:57:43.958 : FAIL : Keyword 'Get OSD State' failed after retrying for 2 minutes. The last error was: CannotSendRequest

Ending test:  interfaceAuto.Testcase.02 Host Configuration.Add storage volume.Single partition
```


The solution：


```
root@host1:/# vi /etc/apache2/apache2.conf

modify 

   KeepAliveTimeout 5 

to 

   KeepAliveTimeout 100

Units are seconds, then restart apache2 service。
```


instructions：



  This is united into the robot file of rf-automation\testcase\01_Create_Cluster\Prepare Cluster.robot. If still appear, please check whether the apache conf was successfully modified, or to check the test case in file of Prepare Cluster.robot execute success or not.

 

 

 

###### 3.  Forbidden root login



  The RF test case exceutor is Jenkins, sometimes need root user to perform or switch to root user(e.g: ssh 127.0.0.1), because of user of root was banned to login, so some test case will fail.

 

The solution：



Allow root login：


```
1. modify /etc/ssh/sshd_config

vi /etc/ssh/sshd_config

 

2、allow root login

search “#PermitRootLogin no”， 

delete "#", and set "No" to "Yes", then save the file. Like this:

# PermitRootLogin prohibit-password

PermitRootLogin yes

 

At last, restart ssh service.
```



###### 4.  Client mount nfs return 32



The bellow is test case of "Create NFS share folder":

<img class="shadow" src="/img/in-post/rf/clip_image022.jpg" width="1200">

 



when client mount nfs, the output is:

```
Failed to restart nfs-kernel-server.service: Unit nfs-kernel-server.service not found.

root@jenkins:~# mount -t nfs 10.10.0.127:/vol/nas01 /mnt/nfs

mount: wrong fs type, bad option, bad superblock on 10.10.0.127:/vol/nas01,

​    missing codepage or helper program, or other error

​    (for several filesystems (e.g. nfs, cifs) you might

​    need a /sbin/mount.<type> helper program)

 

​    In some cases useful info is found in syslog - try

​    dmesg | tail or so.
```



The solution：




```
Install nfs-common and cifs-utils
apt-get install nfs-common
apt-get install cifs-utils
```



Then, file of mount.nfs and mount.cifs created in dir of /sbin.




## Create Jenkins Porject

 

### Enter an item name

<img class="shadow" src="/img/in-post/rf/clip_image024.jpg" width="1200">

 

Click "OK"

### Source Code Management

<img class="shadow" src="/img/in-post/rf/clip_image026.jpg" width="1200">

 

### Build Triggers

<img class="shadow" src="/img/in-post/rf/clip_image028.jpg" width="1200">

### Build Environment

<img class="shadow" src="/img/in-post/rf/clip_image030.jpg" width="1200">

### Build

<img class="shadow" src="/img/in-post/rf/clip_image032.jpg" width="1200">

  set properties file path to get ISO_NAME and RF running times. Before setting, should install this plug, search keyword is "inject".

<img class="shadow" src="/img/in-post/rf/clip_image034.jpg" width="1200">

 

### Post-build Actions 

###### Install robot framework plug

  install robot framework plug to get total test cases/success test cases/failed test cases/ignore test cases and so on.

<img class="shadow" src="/img/in-post/rf/clip_image036.jpg" width="1200">

 

###### Editable Email Notification

Input follow content in "Default Content":

```
<html>
  <head>
​    <title></title>
  </head>
  <body>
​    Hi All, <br>
​      This is the SEG Robot Framework Interface Automation Test Results. <br>
​    <font color="#0B610B" size="3"> Please click on the red link, check the console output, and check the continuous integration build results:</font> <a href="${BUILD_URL}console"><b><font color="#DF0101" size="3"> ${ENV, var="JOB_NAME"}</font></b></a>
        <table width="95%" cellpadding="0" cellspacing="0" style="font-size:11pt; font-family:Tahoma, Arial, Helvetica, sans-serif">
​      <tr>
​        <td>
​          <h2>
​            <font color="#0000FF" size="4">Result: Passing rate - ${TEST_COUNTS,var="PASS"}&#47;${TEST_COUNTS}</font>
​          </h2>
​        </td>
​      </tr>
​      <tr>
​        <td>
​          <br>
​          <b><font color="#0B610B">Build information:</font></b>
​          <hr size="2" width="100%" align="center">
​        </td>
​      </tr>
​      <tr>
​        <td>
​          <ul>
​            <li>Project Name    -- ${PROJECT_NAME}</li>
​            <li>Run ISO Version   -- ${ISO_NAME} </li>
​            <li>RF Start/End Time  -- From ${START_TIME} To ${END_TIME}</li>
​            <li>Build Serial Number -- The ${BUILD_NUMBER} times build</li>
​            <li>Trigger Reason   -- ${CAUSE}</li> 
​             <li>Build Result    -- <a href="${PROJECT_URL}${BUILD_NUMBER}/robot/">${PROJECT_URL}${BUILD_NUMBER}/robot/</a> </li>
​            <li>Project URL     -- <a href="${PROJECT_URL}">${PROJECT_URL}</a></li>
​            <li>Build URL      -- <a href="${BUILD_URL}">${BUILD_URL}</a></li>
​            <li>Total cases     -- $TEST_COUNTS</li>
​            <li>Pass cases      -- ${TEST_COUNTS,var="pass"}</li>
​            <li>Fail cases      -- ${TEST_COUNTS,var="fail"}</li>
​            <li>Skip cases     -- ${TEST_COUNTS,var="skip"}</li>
​            <li>Git Version     -- ${GIT_REVISION,length=8} </li>
​          </ul>
​        </td>
​      </tr>
​      <tr>
​        <td>
​          <b><font color="#0B610B">Since the last success build of the change</font></b>
​          <hr size="2" width="100%" align="center">
​        </td>
​      </tr>
​      <tr>
​        <td>
​          <ul>
​            <li>In this view the historical change: -- <a href="${PROJECT_URL}changes">${PROJECT_URL}changes</a>
​            </li>
​          </ul>${CHANGES_SINCE_LAST_SUCCESS, reverse=true, format="Changes for Build #%n:<br>%c<br>", showPaths=true, changesFormat="<pre>[%a]<br>%m</pre>", pathFormat="&nbsp;&nbsp;&nbsp;&nbsp;%p"}
​        </td>
​      </tr>
​      
​      <tr>
​        <td>
​          <br>
​        </td>
​      </tr>
​      <tr>
​        <td>
​          <b><font color="#0B610B">Failure of the test results:</font></b>
​          <hr size="2" width="100%" align="center">
​        </td>
​      </tr>
​      <tr>
​        <td>
          <pre style="font-size:11pt; font-family:Tahoma, Arial, Helvetica, sans-serif">

$FAILED_TESTS

</pre><br>
​        </td>
​      </tr>
​      <tr>
​        <td>
​          <b><font color="#0B610B">Build log (The last 100 rows record):</font></b>
​          <hr size="2" width="100%" align="center">
​        </td>
​      </tr>
​      <tr>
​        <td>
​          The test log (if run the test): <a href="${PROJECT_URL}${BUILD_NUMBER}/console">${PROJECT_URL}${BUILD_NUMBER}/console</a><br>
​          <br>
​        </td>
​       </tr>
​    </table>

<hr size="2" width="100%" align="center" /> 
(Note: This E-mail generated by system automatically, please do not reply!)

​      <tr> <td>
​          <br>
​        </td>
​      </tr>
  </body>
</html>
```



###### Add publish robot framework test results



<img class="shadow" src="/img/in-post/rf/clip_image038.jpg" width="1200">

Then, save it.

 

### Jenkins System Config



###### Config System



<img class="shadow" src="/img/in-post/rf/clip_image040.jpg" width="1200">

 



###### Set System Admin e-mail address



<img class="shadow" src="/img/in-post/rf/clip_image042.jpg" width="1200">



###### Extended E-mail Notification



<img class="shadow" src="/img/in-post/rf/clip_image044.jpg" width="1200">

 

###### E-mail Notification

<img class="shadow" src="/img/in-post/rf/clip_image046.jpg" width="1200">

 

project的详细配置，请参考Nanking lab 172.16.146.234的设置。

 

### E-mail Over View



The below is the received email, e.g:



<img class="shadow" src="/img/in-post/rf/clip_image048.jpg" width="1200">

 

 

 

### Open report.html failed



just like this:

<img class="shadow" src="/img/in-post/rf/clip_image050.jpg" width="1200">

This is a bug of Jenkins, the work around is:

https://issues.jenkins-ci.org/browse/JENKINS-32118

 

Run the command in Script Console:

```
system.setProperty("hudson.model.DirectoryBrowserSupport.CSP","sandbox allow-scripts; default-src 'none'; img-src 'self' data: ; style-src 'self' 'unsafe-inline' data: ; script-src 'self' 'unsafe-inline' 'unsafe-eval' ;")
```


That's all.


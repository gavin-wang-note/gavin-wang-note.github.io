---
layout:     post
title:      "基于Nose Framework做产品自动化"
subtitle:   "Nose automation documentation"
date:       2019-12-31
author:     "Gavin"
catalog:    true
tags:
    - Automation
    - nose
---

# 前言

自2018-05-01提交第一个commit以来，在不影响正常测试工作release版本情况下，断断续续的持续了1年8个月的自动化开发在今天(2019-12-31)收尾了，总测试用例数为1310个，一路走来深有感慨。。。。。。

虽然收尾了，但后期版本功能发生变化，或者用例开发过程中有一些bug未考虑到导致用例执行失败的，还是需要对用例进行修改、优化，总之，一个产品自动化的完善，需要一个循序渐进的过程，持之以恒，总会渐变渐好！

本文记录了在开发产品自动化期间(Base on Ubuntu12.04)，所需要的一些条件、碰到的问题、注意事项等，如果想了解Nose framework的具体使用，请参考Nose官网吧，官网有详细的guide。

# 必要的安装/升级/修改

说明：
* 在线安装，所以存储节点要配置 dns server；
* 本章节的如下操作，无需手动安装，只需要执行 run.py，自动完成本章节的所有安装动作。本章节仅为了记录要安装哪些模块、插件、修改等信息。

## 1、非产品OS 作为客户端需要安装的软件

本章节以 ubuntu 为例，其他类型的 OS，不做考虑，且 OS 并不是我们的产品。

需要安装 multipath-tools， fio，openssh-server（支持 ssh 指令）， open-iscsi（支持 iscsiadm指令）， NFS  和 CIFS。 上述软件安装指令如下：

```
apt-get install open-iscsi
apt-get install openssh-server apt-get install multipath-tools apt-get install fio
apt-get install cifs-utils
apt-get install nfs-kernel-server
```

如果客户端是官方的Ubuntu，那肯定是没有安装 NFS 和 CIFS 的，mount NFS/CIFS 会出问题：

```
root@nose-ubuntu:/mnt# mount -t nfs 10.16.172.246:/vol/nose_nas /mnt/test mount: wrong fs type, bad option, bad superblock on 10.16.172.246:/vol/nose_nas,
missing codepage or helper program, or other error (for several filesystems (e.g. nfs, cifs) you might need a /sbin/mount.<type> helper program)

In some cases useful info is found in syslog - try dmesg | tail or so.


root@nose-ubuntu:/mnt# mount -t cifs //10.16.172.246/nose_nas_src /mnt/test/ mount: wrong fs type, bad option, bad superblock on //10.16.172.246/nose_nas_src,
missing codepage or helper program, or other error (for several filesystems (e.g. nfs, cifs) you might
need a /sbin/mount.<type> helper program)

In some cases useful info is found in syslog - try dmesg | tail or so.

root@nose-ubuntu:/mnt# dmesg | tail
[  141.523611] device-mapper: multipath: Failing path 65:0. [ 141.638465] device-mapper: multipath: Failing path 65:32. [ 141.638545] device-mapper: multipath: Failing path 65:112. [ 141.687588] device-mapper: multipath: Failing path 65:112. 
[846862.989111] FS-Cache: Loaded
[846862.997304] RPC: Registered named UNIX socket transport module. [846862.997307] RPC: Registered udp transport module. [846862.997308] RPC: Registered tcp transport module.
[846862.997309] RPC: Registered tcp NFSv4.1 backchannel transport module.
[846863.007999] FS-Cache: Netfs 'nfs' registered for caching

```

所以需要进行安装，成功安装后，内容如下：

```
root@nose:~# dpkg -l | grep nfs
ii  libnfs4:amd64                        1.10.0-7.0+854+6b837f908                   amd64        NFS client library (shared library)
ii  libnfsidmap2:amd64                   0.25-5                                     amd64        NFS idmapping library
ii  nfs-common                           1:1.2.8-6ubuntu1.2                         amd64        NFS support files common to client and server
ii  nfs-kernel-server                    1:1.2.8-6ubuntu1.2                         amd64        support for NFS kernel server
```

说明：
* 目前 run.py 有做检查，但不进行安装，具体安装操作，尚需手动执行。

## 2、安装python-pip

```
apt-get install python-pip
```

## 3、升级requests模块

```
pip install --upgrade --ignore-installed requests --index-url=https://pypi.python.org/simple

root@44:/var/cache/apt/archives# pip install --upgrade --ignore-installed requests --index-url=https://pypi.python.org/simple
Downloading/unpacking requests
  Downloading requests-2.18.4.tar.gz (126Kb): 126Kb downloaded
  Running setup.py egg_info for package requests
    
    warning: no files found matching 'NOTICE'
Downloading/unpacking chardet>=3.0.2,<3.1.0 (from requests)
  Downloading chardet-3.0.4.tar.gz (1.9Mb): 1.9Mb downloaded
  Running setup.py egg_info for package chardet
    
    warning: no files found matching 'requirements.txt'
Downloading/unpacking idna>=2.5,<2.7 (from requests)
  Downloading idna-2.6.tar.gz (135Kb): 135Kb downloaded
  Running setup.py egg_info for package idna
    
    warning: no previously-included files matching '*.pyc' found under directory 'tools'
    warning: no previously-included files matching '*.pyc' found under directory 'tests'
Downloading/unpacking urllib3>=1.21.1,<1.23 (from requests)
  Downloading urllib3-1.22.tar.gz (226Kb): 226Kb downloaded
  Running setup.py egg_info for package urllib3
    
    warning: no previously-included files matching '*' found under directory 'docs/_build'
Downloading/unpacking certifi>=2017.4.17 (from requests)
  Downloading certifi-2018.4.16.tar.gz (149Kb): 149Kb downloaded
  Running setup.py egg_info for package certifi
    
Installing collected packages: requests, chardet, idna, urllib3, certifi
  Found existing installation: requests 1.2.3
    Uninstalling requests:
      Successfully uninstalled requests
  Running setup.py install for requests
    
    warning: no files found matching 'NOTICE'
  Found existing installation: chardet 2.0.1
    Uninstalling chardet:
      Successfully uninstalled chardet
  Running setup.py install for chardet
    
    warning: no files found matching 'requirements.txt'
    Installing chardetect script to /usr/local/bin
  Running setup.py install for idna
    
    warning: no previously-included files matching '*.pyc' found under directory 'tools'
    warning: no previously-included files matching '*.pyc' found under directory 'tests'
  Found existing installation: urllib3 1.6
    Uninstalling urllib3:
      Successfully uninstalled urllib3
  Running setup.py install for urllib3
    
    warning: no previously-included files matching '*' found under directory 'docs/_build'
  Running setup.py install for certifi
    
Successfully installed requests chardet idna urllib3 certifi
Cleaning up...
```

说明：
* request模块，目前仅有wechat告警有使用到，升级不会对存储节点中python lib带来额外影响。

## 4、安装configobj模块

```
pip install configobj
```

## 5、使用html 报告

参考资料: ```https://pypi.org/project/nose-html-reporting/ ```

安装命令：

```
pip install nose-html-reporting
```

## 6、安装nose

存储节点系统安装好后自带nose，无需安装、升级。

## 7、修改nose_html_reporting/__init__.py

如果不修改，会报如下错误：

<img class="shadow" src="/img/in-post/modify_nose_html_report_init.png" width="1200">

解决方法：

```vi /usr/local/lib/python2.7/dist-packages/nose_html_reporting-0.2.3-py2.7.egg/nose_html_reporting/__init__.py ```

修改 ```/usr/local/lib/python2.7/dist-packages/nose_html_reporting-0.2.3-py2.7.egg/nose_html_reporting目录下__init__.py，```
将203行 ```lstrip_blocks=True ```注释掉，并删除掉产生的pyc文件。

```
root@44:/home/nose_test/src# cd /usr/local/lib/python2.7/dist-packages/nose_html_reporting/
root@44:/usr/local/lib/python2.7/dist-packages/nose_html_reporting# rm __init__.pyc
```

说明：
* 修过__init__.py操作无需人工干预，run.py脚本中已经有修过动作。

## 8、安装nose-testconfig

```
pip install nose-testconfig --index-url=https://pypi.python.org/simple
```

这个模块是nose的插件，用户用例执行时，接受用户指定的自定义循环执行用例的次数，必须安装。

## 9、安装关键字高亮plugin

参考资料

```
https://gitee.com/walkingnine/colorunit
https://pypi.org/project/colorama/#files
```

需要安装如下这个包：

```
colorama-0.3.9.tar.gz
walkingnine-colorunit.gz
```

说明：
* 安装上面安装包后，源码有问题，需要修改一些东西，这里是修改好了后，重新打了安装包。

特别说明：
* 测试用例中不需要添加下列步骤中内容，只要在nosetests执行用例的时候，使用--with-colorunit参数即可。

```
import nose; 
from colorunit import ColorUnit
  和：
if __name__ == '__main__':
    nose.main(addplugins = [ColorUnit()])
```

## 10、用例进度

参考资料

```
https://github.com/erikrose/blessings
https://github.com/erikrose/nose-progressive
```

源码要求依赖nose 1.2.x，目前产品Ubuntu 14.04自带nose 版本是1.1.2，所以更改了源码版本要求，并重新打包，无需再次修过，直接安装python_3rd_lib目录下对应安装包即可。

## 11、pylint执行报错

<img class="shadow" src="/img/in-post/nose_pylint_error.png" width="1200">

原因:

未安装pylint， 解决方法：

进入nose_framework/python_3rd_lib/，解压pylint-1.7.6.tar.gz，进入解压缩目录，重新进行pylint的安装：

```
cd pylint-1.7.6
python setup.py install
```

# nose的日常使用

## 1、常用参数介绍

```
-v : debug模式，看到具体执行情况，推荐大家执行时用这个选项。
-s : nose会捕获标准输出，调试的print代码默认不会打印。
   nosetest -s 可打开output输出，否则全部通过时不打印stdout。
   
-x : 一旦case失败立即停止，不执行后续case
-w : 指定一个目录运行测试。目录可以是相对路径或绝对路径.
--tests : 默认情况下，nosetests会执行所有的测试用例，若想单独只执行一个case，
       执行nosetest --tests 后跟要测试的文件(nosetests后面直接跟文件名，其实也可以
       直接运行该case。
--collect-only :  nosetests --collect-only -v，不运行程序，只是搜集并输出各个case的名称。
--processes ： 需要安装插件，--processes=20， 并发执行用例，解决用例总体执行时间
--with-progressive： 需要安装插件，实时展示用例执行进度
--with-colorunit ： 需要安装插件，用例执行结果展示的stdout，以颜色高亮展示
--with-html ： 需要安装插件，且需要和--html-report结合起来使用。这个插件，生成HTML
             格式的测试报告，该测试报告，是以report2.jinja2作为模板。 如果要指定自
             定义模板，可以使用--html-report-template参数，示例如下：
--with-colorunit --with-html --html-report=../report/sds.html --html-report-template=/usr/local/lib/python2.7/dist-packages/nose_html_reporting/templates/report2.jinja2

--tc : 需要安装插件，指定用例运行次数，目前参数名称写死：runs，示例：--tc=runs:20
```

## 2、工具nose.tools的使用

### 打标签

打标签的好处是，可以执行带有某些特定tag的用例，这里用tag，是借用了RF的概念，示例如下：

```
from nose.plugins.attrib import attr
@attr('slow')
def test_big_download():
    pass

@attr(speed='slow')
def test_big_download():
    pass
```

执行的时候，带上 -a参数：

```nosetests -a '!slow' ```

### 是否测试

测试脚本中引入：```from nose.tools import nottest,istest ```

1）不测试的方法：方法名上加修饰器@nottest；

2）指定为测试方法：方法名上加修饰器@istest（方法名无需符合命名规则）

### 断言

```
>>> from nose import tools
>>> dir(tools)
['TimeExpired', '__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__', 'assert_almost_equal', 'assert_almost_equals', 'assert_dict_contains_subset', 'assert_dict_equal', 'assert_equal', 'assert_equals', 'assert_false', 'assert_greater', 'assert_greater_equal', 'assert_in', 'assert_is', 'assert_is_instance', 'assert_is_none', 'assert_is_not', 'assert_is_not_none', 'assert_items_equal', 'assert_less', 'assert_less_equal', 'assert_list_equal', 'assert_multi_line_equal', 'assert_not_almost_equal', 'assert_not_almost_equals', 'assert_not_equal', 'assert_not_equals', 'assert_not_in', 'assert_not_is_instance', 'assert_not_regexp_matches', 'assert_raises', 'assert_raises_regexp', 'assert_regexp_matches', 'assert_sequence_equal', 'assert_set_equal', 'assert_true', 'assert_tuple_equal', 'eq_', 'istest', 'make_decorator', 'nontrivial', 'nontrivial_all', 'nottest', 'ok_', 'raises', 'set_trace', 'timed', 'trivial', 'trivial_all', 'with_setup']
>>>
```

# nose setUP/tearDown 介绍

nose里面有多种可用的setup和teardown

## 1、Package级别的

写在init.py文件里包装

```
def setup_package():
    pass

def teardown_package():
    pass
```

## 2、Module级别的

```
def setup_module():
    pass

def teardown_module():
    pass
```
	
## 3、Class级别的

包装class,所以只执行一次

```
root@Scaler03:~# cat class_method.py
class TestClass():
    @classmethod
    def setup_class(cls):
        print "class method setup"
        
    @classmethod
    def teardown_class(cls):
        print "class method teardown"
        
    
    def test1(self):
        print "test1"

    def test2(self):
        print "test2"

    def test3(self):
        print "test3"
root@Scaler03:~#
```

执行结果

<img class="shadow" src="/img/in-post/nose_eg01.png" width="1200">

在nose中，不需要写类，只写函数可能就足够了，所以直接在一个文件中写:

```
root@Scaler03:~# cat nose_method_setup.py
def setup():
    print "setup"

def teardown():
    print "teardown"

def test_xxx():
    print "this is test xxx"

def test_yyy():
    print "this is test yyy"

root@Scaler03:~#
```

类似的，也是对整个文件而言，效果同上，测试结果如下：

<img class="shadow" src="/img/in-post/nose_eg02.png" width="1200">

## 4、Class方法级别

包装每一个test方法，所以每一个test函数的前后都会执行。

```
root@node97:/home/nose_framework/src/testcase/Function_Test/case_2_Accounts# cat ../../../testcasebase/Account/wyz.py
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from __future__ import unicode_literals

import logging


from common.testcasebase import TestBase


class WYZManager(TestBase):
    """  account manager test case base class  """

    def __init__(self):
        super(WYZManager, self).__init__()
root@node97:/home/nose_framework/src/testcase/Function_Test/case_2_Accounts# cat wyz_test.py
#!/usr/bin/env python


from testcasebase.Account.wyz import WYZManager


class TestNose(WYZManager):
    def setUp(self):
       print "\nsetup"

    def tearDown(self):
        print("teardown")

    def test_case1(self):
        """  case 1  """
        print("this is test case 1")

    def test_case2(self):
        """  case 2  """
        print("this is test case 2")

    def test_case3(self):
        """  case 3  """
        print("this is test case 3")
```

执行结果：

<img class="shadow" src="/img/in-post/nose_eg03.png" width="1200">

从执行结果可以看出，测试类中的setUp 和 tearDown，会在每个测试用例中调用，即每个测试用例执行前，都会执行一次setUp，用例执行结束后，会执行tearDown。

## 5、包装某个函数

测试函数也可定义setup和teardown属性，它们将会在测试函数开始和结束的时候运行。还可以使用@with_setup装饰器，该方式尤其适用于在相同的模块中的许多方法需要相同的setup操作

示例：

```
root@Scaler03:~# cat fun_nose_setup.py
from nose.tools import with_setup

def setup_func():
    print "set up test fixtures\n"
 
def teardown_func():
    print "tear down test fixtures\n"
 
@with_setup(setup_func, teardown_func)
def test1():
    print "test1"
    
@with_setup(setup_func, teardown_func)
def test2():
    print "test2"
    
    
@with_setup(setup_func, teardown_func)
def test3():
    print "test3"    
root@Scaler03:~# 
```

执行结果
 
<img class="shadow" src="/img/in-post/nose_eg04.png" width="1200">

# 用例编写规则要求

1、test_xxxx.py尽量避免逻辑操作，纯粹是function的调用

2、测试用例的名称，建议携带上用例的编号

例如：
 
<img class="shadow" src="/img/in-post/test_link_case_no.png" width="400">

test_9143_same_daemon_different_signal， 对应TestLink的用例为：```Sc-9143:Same daemon, different signal core file ```

3、测试用例的__doc__，不得含有中文字符

例如：

``` """  Sc-9143:Same daemon，different signal core file  """ ```

这里的逗号，是中文符号，会导致用例报错：

<img class="shadow" src="/img/in-post/doc_error.png" width="1200">

4、用例__doc__内容，以TestLink中名称为准

对于SEG自己增加的测试用例，需要以[SEG]开头， 参考如下：

<img class="shadow" src="/img/in-post/nose_case_doc.png" width="400">

5、避免测试用例之间存在依赖关系

（1）每个测试suite中的测试用例互相不依赖；

（2）测试suite中的用例，尽可能避免依赖关系

如TestLInke中上一个用例是创建，下一个用例是删除，则合并这两个用例为一个自动化测试用例。

6、日志记录对齐要求

执行动作的记录，开头增加[Action]；检查动作的记录，开头增加[Check];

断言记录的log，开头增加[ERROR]； 操作成功的log，开头增加[SUCCESS]； 不需要检查点的，开头增加[Skip]；

具体要求如下：

**[Prepare]** **后面跟2****个空格；**

**[Action]** **后面跟3****个空格**

**[Start]** **后面跟4****个空格**

**[Check]** **后面跟4****个空格**

**[Success]** **后面跟2****个空格**

**[Skip]** **后面跟5****个空格**

**debug****级别的log****，内容前面跟2****个-****，之后** **再加2****个空格**

**assert****中，[ERROR]** **后面跟2****个空格**

7、用例的执行顺序

执行 nosetests -s 可看到调用顺序， 用例执行顺序，根据ASSII进行排序，在用例有关联情况下，需要对用例名称增加数字编号，来人为的干预用例执行顺序，比如test_1_xxx, test_2_yyy。

8、代码规范要求

执行pylint，确保检查结果分值=10

```pylint -r y testcasebase/Virtual_Storage/vs_user.py --rcfile=./pylintrc ```

MESSAGE_TYPE 有如下几种：

* (C) 惯例。违反了编码风格标准
* (R) 重构。写得非常糟糕的代码。
* (W) 警告。某些 Python 特定的问题。
* (E) 错误。很可能是代码中的错误。
* (F) 致命错误。阻止 Pylint 进一步运行的错误

9、用例文件权限

统一使用 644 权限，否则默认情况下无法被 nosetests search 到，自然就不会被执行到，因为 nosetesst 默认只查找 644 权限的文件。

10、避免在 class 与 setup_class 之间做比较重的动作

比如下文中的 RRS 用例 test_remote_replication_tasks.py（下文代码是一个不可取的代码， 这里仅做示例用）
 
<img class="shadow" src="/img/in-post/bad_eg.png" width="1200">

在class TestReplicationTask 与setup_class 之间，启用了RRS 服务、创建了S3 账号并创建bucket， 最后上传了一些 object 到 bucket 中。正常情况下，这部分动作应该是在用例被执行之前要做的，然后会立刻执行 setup_class 中的动作，接着执行用例，最后 teardown。实际上，在run.py  去执行所有测试用例的时候， 在 init 完所有的 class 之后（即创建完 session 后），会 先执行所有 test_xx.py 中定义在 class  与 setup_class 之间的所有动作， 这也无可厚非，但是，由于约束了用例的执行顺序，case_2_Accounts 会优先于 case_5_Remote_DR 被执行， 而 case_2_Accounts 里将其他 pool 设置为 S3 pool 的动作，这势必会清理掉在执行 run.py init 结束后所创建的所有 bucket 与 bucket 下的 object，到 case_5_Remote_DR 被执行时，曾经创建的 bucket 与 bucket 下的 object 早已不复存在，自然 case_5_Remote_DR 下面的相关用例就会失败。

故而，建议：

避免在 class 与setup_class 之间做比较重的动作。对于较重的动作，放在 setup_class 中， 好处有 2：

（1）	避免被其他 class import 时做更多、更重的动作

（2）	避免用例 suite 间前后有依赖关系，给用例排查带来难度

11、用例文件名称、用例中定义变量名称全局唯一

对于测试用例中定义的变量，诸如 NAS 文件夹名称、子目录名称、iSCSI target 名称、volume 名称、pool 名称、cephfs 名称、用例执行过程中产生的文件的名称等等，要保持全局唯一， 即所有用例中不出现同名的文件名、目录名、pool 名等。当有用例出错时，可以根据这个名称，定位到是哪个用例产生了问题，因为具有唯一性，可以排除其他用例带来的干扰。


# nose的其他插件

## 1、用例设定依赖关系

需要安装 nose-dep plugin，具体操作，请参考如下链接： https://github.com/Zitrax/nose-dep

说明:
* 这个 module 目前已经移除，本文档内容暂时留存，不删除，以作备用。

## 2、用例执行顺序

这里介绍插件：nose-randomly

可以通过 ```pip install nose-randomly ```

进行安装，成功安装后：
 
<img class="shadow" src="/img/in-post/nose_plug01.png" width="1200">

默认是按时间来做为随机种子来打乱用例顺序的，也可以自己定义种子。


# 配置文件说明

说明：
* 配置文件在 src/config/autotest.config，包括但不限制于集群配置、客户端配置、AD/LDAP配置、检查周期、集群服务启用/停用等相关配置信息，全部在这个配置文件中，在运行用例前，务必确保这个配置文件的准确性。

## 1、autotest.config 说明

！！！ 这个文件的内容，需要根据被测环境进行实际修改 ！！！

```
[CLUSTER]	
root_pass = "p@ssw0rd"	# 被测集群 root 密码，务必要正确
ssh_port = 22
cluster_name = NOSE	# 被测集群名称，仅适用于新建集群情况下；在已有集群下跑用例，不用改
osd_device = sdb	# 哪个分区被用于创建 OSD，仅适用于全新安装系统后 nose 自动创建集群
public_iface = ens160		# public interface 网口名称，务必要正确
storage_iface = ens192	# storage interface 网口名称，务必要正确
rep_no = 2	# 集群副本数，默认 2 副本ntp_server_ip = 202.120.2.101 # NTP server 地址dns_ip = 172.17.75.100 # DNS IP 地 址
storage_ips = "10.10.1.97 10.10.1.98 10.10.1.99" # 存储节点 storage 网络，以单个空格分割
public_ips = "172.17.75.97 172.17.75.98 172.17.75.99" # 存储节点 public 网络，以单个空格分割
forth_node_storage_ip = "10.10.10.249"  # 第四个节点的storage ip地址
license =
"3TYRSI-7IA0OW-109QON-LAZ8RV-27AICZ-FQBB3U-DLJW2P,3TYY0Z-Y3MUPS-0QRA8N-B5A8MT-7KOI1V-D9 T0RD-18X7QLW,3TZ49H-OOZOQO-1H5HY2-BAD4SB-236PNQ-VXNNGG-IY0LEH" # 这里是 Controller
license

[LOGING]
host = https://localhost:8080	# 访问存储 UI 的地址，无须修改
user_id= admin	# 访问 UI 的管理员账号
password = 1	# 访问 UI 的管理员账号对应的密码

[AD/LDAP]
ad_server_addr = 172.17.75.231	# AD 的相关设置
port = 389
ad_base_dns = "DC=hype,DC=com"
ad_admin_account = "hype\Administrator" 
ad_admin_passwd = "Trend#123" 
ad_search_dn = "CN=Users,DC=hype,DC=com" 
ad_acl_folder = 'Shares'
ad_acl_user = 'zhangsan' 
ad_acl_user_passwd = 'bigtera@123' 
ac_guest_folder = 'Guest'

ldap_server_addr = 172.17.75.199	# LDAP 的相关设置
ldap_base_dns = "dc=bigtera-os,dc=com" ldap_admin_account = "cn=admin,dc=bigtera-os,dc=com" ldap_admin_passwd = "12345678"
ldap_search_dn = "dc=bigtera-os,dc=com"

[TAKEOVERIP]
# ctdb takeover ip
takeover_ips = "172.17.73.91/24 172.17.73.92/24 172.17.73.93/24" #GW 接管 IP 地址，以空格分割

# S3 takeover IP
s3_takeover_ips = "172.17.73.94/24,94 172.17.73.95/24,95 172.17.73.96/24,96" # S3 的接管
IP 地址，以空格分割，格式必须是 IP/掩码位数

[SNMP]	# 这部分只要产品不发生变化，这里就不需要更改
mib_id = ".2.25.31690.11968.43142.4581.44107.2.42453.50459"
snmp_cluster_number = ".1.1"
snmp_product_name = ".1.2"
snmp_product_version = ".1.3"
snmp_fsid = ".1.4"
snmp_cluster_health = ".1.5"
snmp_cluster_disk_total_size = ".1.6"
snmp_cluster_disk_user_size = ".1.7"
snmp_read_io = ".1.8"
snmp_write_io = ".1.9"

esxi_vm_host_name = 'SEG_nose_client(!!!Do not power off it!!!)' # nose client 在 ESXi 侧
 
ipmi_ip = "172.17.75.221"	# nose client 是物理机（对应上面的 white_list_ip 参数），这个物理机的IPMI 地址
ipmi_user = 'ADMIN'	# IPMI 的系统管理员账号名称
ipmi_user_passwd = 'ADMIN'	# IPMI 系统管理员账号的密码 

[BACKUP] # nose 用例执行过程中备份文件的存档目录，这里不需要修改
backup_base_path = "/tmp/nose_backup/"
ezs3_log_backup = "/tmp/nose_backup/log_ezs3/"
test_case_output_path = "/tmp/nose_backup/test_case_output"

[RETRY]
retry_interval = 5 # 间隔 5 秒尝试一次，做 check 或 mount 之类的动作
retry_timeout = 40 # 总共尝试次数，默认 40 次

[DAEMON_SERVICE]	# 服务的重启、停止相关动作，不同版本的操作系统指令不一样
# restart or stop or start deamon service
restart_ezmonitor = "/etc/init.d/ezmonitor restart"
restart_csmonitor = "/etc/init.d/csmonitor restart"
restart_ezfs_agent = "/etc/init.d/ezfs-agent restart"
restart_ezfs_recycle_flusher = "/etc/init.d/ezfs-recycle-flusher restart"
restart_eziscsi = "/etc/init.d/eziscsi restart"
restart_eziscsi_rbd_clean = "/etc/init.d/eziscsi-rbd-cleaner restart"
restart_apache = "/etc/init.d/apache2 restart"
restart_rgw = "/etc/init.d/radosgw restart"
restart_smart_monitor = "/etc/init.d/ezs3-smart-monitor restart"
restart_ezs3_agent = "/etc/init.d/ezs3-agent restart"

restart_ctdb = "/etc/init.d/ctdb restart"
start_ctdb = "/etc/init.d/ctdb start"
stop_ctdb = "/etc/init.d/ctdb stop"

restart_multipath_tool = "/etc/init.d/multipath-tools restart"
restart_resolvconf = "/etc/init.d/resolvconf restart"

# For ceph service
ceph_start = "/etc/init.d/ceph start"
start_mon = "/etc/init.d/ceph start mon"
start_mds = "/etc/init.d/ceph start mds"
start_osd = "/etc/init.d/ceph start osd"
start_all_osd = "/etc/init.d/ceph -a start osd"
start_all_mon = "/etc/init.d/ceph -a start mon"
start_all_mds = "/etc/init.d/ceph -a start mds"
# # Start all of ceph service on all node(osd, mon and mds)
start_all_ceph_service = "/etc/init.d/ceph -a start"

restart_mon = "/etc/init.d/ceph restart mon"
restart_mds = "/etc/init.d/ceph restart mds"

stop_mon = "/etc/init.d/ceph stop mon"
stop_mds = "/etc/init.d/ceph stop mds"
stop_osd = "/etc/init.d/ceph stop osd"

start_assign_osd = "/etc/init.d/ceph start osd."
stop_assign_osd = "/etc/init.d/ceph stop osd."

# # For keepalived
stop_keepalived = "/etc/init.d/keepalived stop"
```

## 2、log.config 说明

！！！ 这个文件的内容，无需更改 ！！！

```
#logger.conf
###############################################
[loggers]
keys=root
[logger_root]
level=DEBUG
handlers=hand01
###############################################
[handlers]
keys=hand01
[handler_hand01]
class=StreamHandler
level=ERROR
formatter=form02
args=(sys.stdout,)

[handler_hand02]
class=FileHandler
level=DEBUG
formatter=form01
args=('nose_autotest.log','w')
###############################################
[formatters]
keys=form01,form02
[formatter_form01]
format=%(asctime)s %(filename)-8s[line:%(lineno)-4s] %(levelname)-6s %(message)s
datefmt=%a, %d %b %Y %H:%M:%S
[formatter_form02]
format=%(asctime)s %(filename)-8s[line:%(lineno)-4s] %(levelname)-6s %(message)s
# format=%(name)-12s: %(levelname)-8s %(message)s
datefmt=
###############################################
[nosetests]
verbosity=2
logging-format=%(asctime)s %(filename)-8s[line:%(lineno)-4s] %(levelname)-6s %(message)s
```

# 测试用例的执行

## 1、执行某个test suite

```nosetests -v -x testcase/test_account.py:ManagerAccount --with-html --html-report=../report/nose.html --html-report-template=/usr/local/lib/python2.7/dist-packages/nose_html_reporting/templates/report2.jinja2 ```

说明：
* 这里的ManagerAccount， 是test_account.py的一个class。

## 2、执行指定测试用例

```nosetests -v -x testcase/test_account.py:TestManagerAccount.test_add_user_success --with-html --html-report=../report/nose.html ```

说明：
* 这里的test_add_user_success， 是具体的测试用例，表明这个用例是test_account.py文件中TestManagerAccount类下的用例

## 3、执行多个测试用例/测试集合

如果是执行不同测试集合中的不同用例，示例如下：


```nosetests -v --with-progressive --with-html --html-report=../report/test.html testcase/Function_Test/case_4_Virtual_Storages/NAS/test_NAS_general_management.py:TestN ASGeneral.test_434_create_nfs_cifs_folder testcase/Function_Test/case_7_Statistics_Logs/test_query_export_log.py:TestLogs.test_74
5_4_query_log_by_category_node_management ```

## 4、多进程并发测试

携带参数--processes， 如--processes=2

可以缩短测试时间，同时，要一并携带上 --process-restartworker和 --process-timeout参数，--process-timeout数值要比较大（单位：秒），否则可能会出现内存泄露。

示例如下：

```nosetests -v -x --tc=runs:3 --process-restartworker --process-timeout=100000 --processes=5 testcase/Function_Test/case_4_Virtual_Storages/NAS/test_samba_account.py ```

## 5、dry-run

只列出要执行哪些用例

```nosetests --collect-only  -v ```

## 6、运行不同模块下不同用例

```nosetests -v -x --tests=testcase/test_account.py:ManagerAccount,testcase/test_mds.py:restart_mds --with-html --html-report=../report/nose.html ```


## 7、用例执行时关键字高亮

使用前面安装的colurunit plugin，用例执行时带上参数--with-colorunit

```nosetests --with-colorunit -s -x -v --with-html --html-report=../report/nose_all_cases.html ```


## 8、用例执行显示进度

```nosetests --with-progressive --with-colorunit -s -x -v --with-html --html-report=../report/nose_all_cases.html ```

输出示例：

<img class="shadow" src="/img/in-post/nose_eg04.png" width="1200">

这里源码有个问题，同时使用高亮和进度，会导致高亮和进度在用例执行结果信息输出时，两部分信息展示混杂在一起，已经修改源码解决，安装后无需做任何调整。

## 9、循环运行用例

携带runs参数，并制定循环执行的次数，如果不携带该参数，默认不循序，即只运行一次（特殊用例除外，比如账号中只创建、删除，不做检查，最后做一轮检查的场景）。

```nosetests -s -x -v --with-progressive --with-colorunit --with-html --html-report=../report/sds.html testcase/Function_Test/case_4_Virtual_Storages/NAS/test_samba_account.py:TestSambaAccount.test_add_delete_samab_user_no_check --tc=runs:50 ```

说明:
* 如果不指定runs，默认不循环，即只执行用例一次（Code写死）。

# 编写用例碰到的问题

## 1、用例无法生成 html report

Jenkins 或者手动执行用例无法生成 html report
 
<img class="shadow" src="/img/in-post/nose_report_error.png" width="1200"> 

原因：

任意一个测试用例存在UnicodeDecodeError assert 错误，都会导致html 报告的无法生成。

解决方法：

找出有 UnicodeDecodeError 断言错误的用例，往往是测试中文相关的测试用例，解决UnicodeDecodeError。

## 2、用例执行失败，提示 nose_html_reporting addError init__() takes at least 3 arguments (2 given)

堆栈信息显示：

<img class="shadow" src="/img/in-post/nose_report_error2.png" width="1200">

这个原因，往往是测试用例编写上出了问题，可以通过增加 log 或执行 pylint 来检查一下。
 
## 3、用例文件权限问题

如下图所示，测试用例文件的权限不能是 755，建议统一设置为 644，否则用例无法被nosetest 查找到，也就不会被执行到（nose 默认情况下并不测试那些拥有可执行权限的文件）。
 
<img class="shadow" src="/img/in-post/nose_primession01.png" width="1200">

如果要执行可以加上 --exe, 如 nosetests --exe, 或者去掉可执行属性chmod 644 xxx.py

<img class="shadow" src="/img/in-post/nose_primession02.png" width="600">

## 4、用例多轮调测成功后方可提交代码

下面的示例指令：

```nosetests -v --tc=runs:1 --with-xunit --traverse-namespace --process-restartworker
--process-timeout=432000 --processes=10 --with-coverage
--cover-package=/home/nose_framework/src/ --cover-inclusive --with-progressive
--with-colorunit --with-html --html-report=/home/nose_framework/src/../report/rrs.html -c config/log.config
/home/nose_framework/src/testcase/Function_Test/case_5_Remote_DR/test_remote_replication_tasks.py ```

是完整的调测某一个suite 下的所有 case 指令， 第一遍整体调试没有问题后，将--tc=runs:1 调整成 --tc=runs:2， 再次执行用例，确保所有用例都是成功的，而且 html report 也成功生成 ， 方 可 提 交 测 试 代 码 ， ！ ！ ！ 请 务 必 这 样 做 ！ ！ ！ （ 参 考test_9339_reupload_onject_to_bucket_after_new_s3_pool）。


## 5、用例执行期间，VM 被重启

下图为用例执行卡在了凌晨 01:28:32
 
<img class="shadow" src="/img/in-post/nose_vm_boot01.png" width="600">

查看对应时间点的 node：

<img class="shadow" src="/img/in-post/nose_vm_boot02.png" width="600">

VM 的确被重启了，所有执行用例的进程都不在了：
 
<img class="shadow" src="/img/in-post/nose_vm_boot03.png" width="500">

因 VM 使用 converger 提供的 LUN， converger 环境在那个时间点前后并没有异常；对应 ESXi
在那个时间点前有一个告警：

<img class="shadow" src="/img/in-post/nose_vm_boot04.png" width="600">

除此之外，并未发现其他问题，即这个自动重启的原因未知。

后来在 ESXi 对应 VM 目录下，vmware.log 文件中：

<img class="shadow" src="/img/in-post/nose_vm_boot05.png" width="600">
<img class="shadow" src="/img/in-post/nose_vm_boot06.png" width="600">
 
根 据 VMWare KB 的 解 释 ： ```https://kb.vmware.com/s/article/2000542 kern panic ```，导致虚机被重启。

目前尚无有效解决方法，先放大内存看看（从 4G 调整为 6G）

## 6、执行用例的存储节点（VM），nose 占用过多内存

<img class="shadow" src="/img/in-post/nose_memory_leak.png" width="600">

由于现在用例数比较多，nose 运行时间长，目前尚不知在何种状况下导致 nose 占用了过多的内存。根据官方提供的资料：

<img class="shadow" src="/img/in-post/nose_memory_leak2.png" width="300">

增加--proces-restartworker 可以避免内存泄露，但 run.py 是有携带这个参数的，没看到效果。目前推测是**失败的用例较多导致**的，也许提高用例的成功率，能够解决这个问题，持续跟踪该问题。

7、apache2 服务异常，导致 ConnectionError，Cannot assign requested address

<img class="shadow" src="/img/in-post/apache_error.png" width="600">

这里发现对应节点的 apache2 service 已经不存在了，导致后续用例全部失败，暂时未知具体原因，目前想到的规避方法如下：

方法 1：修改 http_session.py 中 HTTP session header 中 Connection，由‘keep-alive’调整为‘close’， 同时，在发起 HTTP request 后，sleep 0.01 秒。

方法 2：需要增加一个 watchdog，来拉起 apache 服务。

目前上述两个方法暂时未动手，这里先记录一下，如果未来还会发生，再来处理。

2019-05-28 再次发生：

<img class="shadow" src="/img/in-post/apache_error2.png" width="600">

apache2 进程全部退出

<img class="shadow" src="/img/in-post/apache_exit_log.png" width="600">

目前对 http_session.py 做如下调整：

(1)将 HTTP session header 中 Connection，由‘keep-alive’调整为‘close’

<img class="shadow" src="/img/in-post/keep_alive.png" width="600">

(2)捕获 ConnectionError 异常，并重启 apache2 服务

<img class="shadow" src="/img/in-post/connection_exception.png" width="600">

2019-10-10:

鉴于之前的修复，问题再次发生，现在 http_session.py 增加如下内容：

```
requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
self.session.keep_alive = False # 关闭多余连接
```

但问题依然存在。

2019-10-11:

再次修复，删除```requests.adapters.DEFAULT_RETRIES = 5 ```,将 ```session.keep_alive = False ``` 放在 http_request 函数里，继续观察一下吧，下次问题再次发生时候，执行 netstat -tn 或者netstat \| grep -c tcp，来查看是否是有太多处于"TIME_WAIT" 状态的 TCP 连接导致问题的发生； 如果是， 需要考虑优化下当前 automation 创建 session、使用session 问题了。

## 8、规避logretate 使得apache reload 导致发送 HTTP request 后台返回 500

<img class="shadow" src="/img/in-post/backend_return_500.png" width="600">

在00:17 前后，会发生Logrotate，其中有一步apache reload，假如此刻恰巧有发送HTTP request，此时 apache  服务状态异常，后台返回 500 错误码。 为了规避这个问题，自动化做了特殊处理，即在发送 HTTP 请求时，hard code 去判断此刻是否是 00:16，如果是，等待150 秒进行规避。
 
<img class="shadow" src="/img/in-post/skip_logrotate.png" width="600">

## 9、规避client mount SAN device 出现 already mounted or busy

<img class="shadow" src="/img/in-post/mount_busy.png" width="600">

如上图所示，当 nose 日志显示客户端 mount 出现 device already mounted or busy 状况时， 会影响后续几个用例的正常执行。

目前尚未找到解决方法，只能重启机器，但是此种情况下，reboot or reboot -f 指令往往失效，只能硬重启。

目前解决方法是：

无论客户端是 VM 还是物理机，

* （1）	执行 run.py 时，重启一次 Client；
* （2）	当 mount SAN device 出现 device already mounted or busy，重启一次 Client

对于 VM，通过 ssh 跳转到 ESXi 执行，所以 ESXi 需要开启 SSH 服务
 
```vim-cmd vmsvc/power.off {vm_id}&& vim-cmd vmsvc/power.on {vm_id} ```

对于物理机，通过执行 ipmitool 命令还 power reset 一下，达到重启机器的目的：

```ipmitool -I lanplus -H {客户端 IP 地址} -U{管理员账号} -P {管理员账号密码} power reset	```

# 注意事项

## 1、VM 系统分区磁盘大小要大于 140G

在创建 VM 分配磁盘大小时，需要系统对应磁盘的分区大小是 140G，之所以有这个要求，是因为需要使用操作系统的一个子分区（比如 sda4）作为 cephfs 的 cache，如果 total size 是 32G，那 sda4 只有几百 M，无法满足 cache size 最低是 10G 的要求。鉴于此，通过 PXE 自动安装 VM 对应的配置文件 nose_70_97-99，osdisksize 要设置成 140：

经验证，如果设置成 128G， 则 sda4 是 6G， 设置成 256， sda4 是 134G

``` 
sda	8:0	0	256G 0 disk
├─sda1	8:1		0	7M	0 part
├─sda2	8:2		0	95.4G 0 part /
├─sda3	8:3		0	26.7G 0 part [SWAP]
└─sda4	8:4		0	134G	0 part
sdb	8:16	0		32G	0 disk
sdc	8:32	0		32G	0 disk
sdd	8:48	0		32G	0 disk
sde	8:64	0		32G	0 disk
```

在 os disk size 是 140G 的情况下，确保 sda4（18G）有超过 10G 的空间大小。

## 2、测试用例不要在第一个或最后一个节点上执行

有一些 S3 takeover IP 的用例，会执行 reboot 或 ifdown 第一个或最后一个节点的 public和storage NIC，故而，避免在第一个或最后一个节点上执行用例。目前 run.py 脚本有做约束性检查。

## 3、客户端存在 dsa key

在配置文件中设置的white_list_ip，如下图所示：

<img class="shadow" src="/img/in-post/key_1.png" width="300">

white_list_ip 这台机器所在的/root/.ssh/目录下，需要存在 id_dsa.pub 这个文件：

<img class="shadow" src="/img/in-post/key_2.png" width="300">
 
如果不存在，需要执行下来命令来产生：

```ssh-keygen -t dsa ```

只所以需要这个 key 的原因，是 RRS automation 需要从远端获取这个 sshkey，否则会导致RRS SSH KEY 这部分相关用例失败（test_remote_SSH_keys.py）。

说明：
* 这部分操作，无需人工干预，已经放到run.py 脚本中了。

## 4、客户端启用 multi-path

如果默认没有启用，在确保安装了 multipath-tool 的情况下，将下列命令写入/etc/rc.local
```/etc/init.d/multipath-tools start ```

上述命令，需要书写在exit 0 前面。

## 5、客户端定期重启

由于当前客户端是一台 VM，建议用例执行前重启一下这台VM，主要目的在于:

### 1、释放无效的 dm 设备

！！！此条适用于所有 nose automation 的 client，无论是物理机还是 VM ！！！

<img class="shadow" src="/img/in-post/dm_device1.png" width="1200"> 
 
对于上图，除了 27d7e5983bd6f7dc5 对应的 dm 设备是有效的，其他的 dm 设备都是无效的，一旦这个 client login 一个 iSCSI LUN 后，如果 map 到了上面一个已经存在的 dm 设备， mkfs 的时候会报类似如下的错误：

```/dev/dm-2 is apparently in use by the system; will not make a filesystem here! ```

尝试使用 dmsetup remove -f device_name 指令去删除，命令卡住，**目前尚无解决方法， 只能重启机器**，重启后恢复正常：

<img class="shadow" src="/img/in-post/dm_device2.png" width="600">

另外，在 kernen.log 中发现很多的“BUG: unable to handle kernel NULL pointer dereference at (null)”，如下图所示：

<img class="shadow" src="/img/in-post/dm_device3.png" width="600">

不确定这个野指针是否导致 dm 设备的残留。

### 2、释放资源，避免客户端响应过慢

如果客户端是物理机，可忽略重启操作。设置脚本：

```
root@NoseClient:/usr/local/bin# cat /usr/local/bin/reboot_machine.sh #!/bin/bash

reboot -f root@NoseClient:/usr/local/bin#
```

每天凌晨3 点（Jenkins 是每天3:20 执行用例，因为这个时刻ISO 正好从台北同步到南京LAB， 当然也可自由设定执行时间）进行 VM 的重启动作：

```
root@NoseClient:/usr/local/bin# cat /etc/cron.d/reboot_machine PATH=/bin:/usr/bin:/sbin

1 3 * * * root bash /usr/local/bin/reboot_machine.sh >/dev/null 2>&1 root@NoseClient:/usr/local/bin#
```

## 6、能编写但需要延迟编写的用例，增加 raise SkipTest

比如在写Folder quota 这部分的测试用例，里面有 RRS 和 pool quota 相关的几个case， 因 RRS 或 pool quota 相关 class base 尚未具备，可以标记这部分用例为skip 状态，这样做的目的是避免不加skip 而在将来被忽略掉，导致这部分用例并没有编写。

主要目的:

* 1、意在提醒 skip 状态的用例要在将来被完成
* 2、某些用例只适用于物理机，VM 无法验证，增加判断，对于 VM 要 skip

skip 示例请参考如下链接：

```http://swordstyle.com/func_test_tutorial/part_one/extra_skip_test.html ```

```
class TestFolderQuota(ShareFolderManager): @loop_run()
def test_1090_folder_quota_less_than_pool_quota(self):
""" Sc-1090:Folder quota < Pool Quota [limited by folder quota] """ raise SkipTest
```

## 7、base class 里，禁止函数名称含有 test

nose 运行用例的时候，根据正则匹配测试用例，会匹配到含有 test 的函数，会认为这个函数是一个测试用例，故而要避免此种情况的发生，test 可以使用单词examination 代替。 

<img class="shadow" src="/img/in-post/skip_start_test.png" width="600">

## 8、创建VS 时，pool 名称必须以nose 开头

目前是 hard code 的限制，否则对 pool 的一些检验会无法通过。

## 9、AD 侧存在一个 Shares 和 Guest 共享目录

目前是 hard code 的限制：

<img class="shadow" src="/img/in-post/hard_code1.png" width="600">

在 NAS migration 用例里，涉及到 Windows Server 提供的 folder，目前写在 config 中：
 
<img class="shadow" src="/img/in-post/hard_code2.png" width="300"> 

## 10、ESXi 开启 SSH 服务

如果 client 是ESXi 上的一台 VM，则需要 ESXi 开启 SSH 服务，因为需要通过 ssh ESXi， 执行重启 VM 操作。

# 测试结果展示

说明：
* 用例执行过程中产生日志文件和生成一个HTML格式的测试报告，日志文件名称（默认：nose_autotest.log）在src/config/ autotest.config中配置，以及打印的日志级别（默认：DEBUG）， 也在这个配置文件中设置。

## 1、屏显输出信息

示例：

```root@node98:/home/nose_framework/src# nosetests -s -x -v --processes=10  --with-progressive --with-colorunit --with-html --html-report=../report/sds.html testcase/Function_Test/case_2_Accounts/test_SDS_admin_account_settings.py ```

<img class="shadow" src="/img/in-post/display_01.png" width="600">
-------------------------------------------------------  中间内容省略  -----------------------------------------------
<img class="shadow" src="/img/in-post/display_02.png" width="600">

## 2、自动化产生的日志文件

日志文件路径：report/ nose_autotest.log，内容示例如下：
 
<img class="shadow" src="/img/in-post/nose_log_file.png" width="600">

## 3、HTML测试报告

html 测试报告默认路径为：report/ all_test_cases.html，示例如下：

<img class="shadow" src="/img/in-post/nose_report_show.png" width="600">

说明：
* 绿色： 表明用例执行成功， Success状态
* 橙色： 表明用例执行失败， Fail状态
* 红色： 表明用例执行发生错误， Error状态

点击左下角的“Full log raw output”， 展示用例执行期间记录的日志信息，如果出错，也会将异常详细信息记录下来：

<img class="shadow" src="/img/in-post/nose_fail_log.png" width="1200">

# Nose存在的问题

## 1、nose memory leak

目前nose是执行在存储节点上，对于VM而言，赋予VM的VMemory并不是很大，而nosetests有时候占用70%以上的内存，引发集群异常，此种状况的发生，会导致VM内存不足，没法保证集群正常运行。

这点，本文之前的章节有提及到，怀疑问题的发生点，在于过多的测试用例执行失败，引发nose 要capture过多的信息放在memory里。

## 2、nose crash

此问题在2019-12-19 00:52:31 左右发生，直接导致nose崩溃，终止用例的执行。
 
<img class="shadow" src="/img/in-post/nose_crash01.png" width="600">
<img class="shadow" src="/img/in-post/nose_crash02.png" width="600">
<img class="shadow" src="/img/in-post/nose_crash03.png" width="600">

产品成功检测到nosetests core dump了。

# 代码分支介绍

Master是6.3， 其他分支以具体版本号创建分支。 Master分支目前暂停用例编写/更新。

# 与jenkins结合

## 用到的jenkins插件

Jenkins拥有丰富的第三方插件，可以用来帮助我们完成各种各样的雪球。下列是本文中用到的几个插件：

* Junit Plugin: 用来展示nose框架生成的单元测试报表
* Cobertura Plugin：用来展示Python代码测试覆盖率报表
* Violations：用来展示Python静态代码审查报表，支持pylint、jslint等

## jenkins的job配置

下文以 nose-7.0 project为示例。

### 1）创建Credentials
 
<img class="shadow" src="/img/in-post/nose_jenkins1.png" width="600">

<img class="shadow" src="/img/in-post/nose_jenkins2.png" width="600">

<img class="shadow" src="/img/in-post/nose_jenkins3.png" width="600">

### 2）设置remote ssh

进入jenkisn--系统管理--系统设置界面，在“SSH remote hosts”处，新增新的ssh remote hosts，并进行check connection，如下图所示：

<img class="shadow" src="/img/in-post/nose_jenkins4.png" width="600">

连接测试成功后，保存退出。

## 3）配置nose-7.0 project

### General

进入nose-7.0 project，设置如下：
 
<img class="shadow" src="/img/in-post/nose_jenkins5.png" width="600">

### 源码管理

<img class="shadow" src="/img/in-post/nose_jenkins6.png" width="600">

下载到 /work/automation-test/nose_7.0/nose_framework/

### 构建触发器

<img class="shadow" src="/img/in-post/nose_jenkins7.png" width="600">

### 构建环境

<img class="shadow" src="/img/in-post/nose_jenkins8.png" width="600">

需要执行的脚本命令如下：

```
# delete report on 234
cd /var/lib/jenkins/jobs/nose_7.0/workspace;
rm -rf report;
sleep 2;

# install VM
sshpass -p 1 ssh -p 22 172.17.75.235 -l root "/root/batch_install_vs/batch_install_vs.py /root/batch_install_vs/config/nose/nose_70_97-99"

# scp code to VM
cd /work/automation-test/nose_7.0/nose_framework;
rm -rf build.properties;
rm -rf report;
cd jenkins;chmod a+x *;
ssh-keygen -f "/var/lib/jenkins/.ssh/known_hosts" -R 172.17.75.98;
./rsync_nose.sh 172.17.75.98 root p@ssw0rd
```
<img class="shadow" src="/img/in-post/nose_jenkins9.png" width="600">

相关命令如下：

```
cd /work/automation-test/nose_7.0/nose_framework/jenkins; 
./rsync_report.sh 172.17.75.98 root p@ssw0rd;
./jenkins_build_properties.sh
```

外部变量的使用：

<img class="shadow" src="/img/in-post/nose_jenkins10.png" width="600">
 
路径设置为：

```/work/automation-test/nose_7.0/nose_framework/build.properties ```

这里使用Inject environment variables的目的，是为了发送邮件内容中，展示任务是从什么时间开始、什么时间点结束，用例执行成功、失败等情况，以及被测试版本信息。


### 构建后操作

发送邮件:
 
<img class="shadow" src="/img/in-post/nose_jenkins11.png" width="600">

HTML内容如下：

```
<html>
    <head>
        <title></title>
    </head>
    <body>
        <h2 style="color: #5e9ca0; text-align: center;">
            Note:(This email generated by system automatically, please do not reply!)
        </h2>
        <table class="editorDemoTable" style="height: 549px; width: 811px;">
            <thead>
                <tr>
                    <td style="background-color: #3498db; text-align: center; width: 801px;" colspan="2" nowrap="nowrap">
                        <h2>
                            <span style="color: #000000;">SEG V7.0 NOSE Automation Test Result</span>
                        </h2>
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #3498db; width: 801px; text-align: left;" colspan="2" nowrap="nowrap">
                        <span style="color: #000000;">Build Information</span>
                    </td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="background-color: #beedc7; width: 150px;" nowrap="nowrap">
                        <span style="color: #000000;">Test Result</span>
                    </td>
                    <td style="background-color: #beedc7; width: 643px;" nowrap="nowrap">
                        <span style="color: #000000;">&nbsp;</span>
                        <ul>
                            <li>
                                <span style="color: #000000;">Total Cases:&nbsp; &nbsp; ${TEST_COUNTS}</span>
                            </li>
                            <li>
                                <span style="color: #000000; background-color: #008000;">Pass&nbsp; Cases:&nbsp; &nbsp; ${TEST_PASS}</span>
                            </li>
                            <li>
                                <span style="color: #000000; background-color: #ffff00;">Fail&nbsp; &nbsp;Cases:&nbsp; &nbsp; ${TEST_FAIL}</span>
                            </li>
                            <li>
                                <span style="color: #000000; background-color: #3366ff;">Skip&nbsp; Cases:&nbsp; &nbsp; ${TEST_SKIP}</span>
                            </li>
                            <li>
                                <span style="color: #000000; background-color: #ff0000;">Error Cases:&nbsp; &nbsp; ${TEST_ERROR}</span>
                            </li>
                        </ul>
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #beedc7; width: 150px;" nowrap="nowrap">
                        <span style="color: #000000;">Product Version</span>
                    </td>
                    <td style="background-color: #beedc7; width: 643px;" nowrap="nowrap">
                        <span style="color: #000000;">$PRODUCT_VERSION</span>
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #beedc7; width: 150px;" nowrap="nowrap">
                        Time Consuming
                    </td>
                    <td style="background-color: #beedc7; width: 643px;" nowrap="nowrap">
                        <span style="color: #000000;">From ($START_TIME) To ($END_TIME)</span>
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #beedc7; width: 150px;" nowrap="nowrap">
                        <span style="color: #000000;">Project Name</span>
                    </td>
                    <td style="background-color: #beedc7; width: 643px;" nowrap="nowrap">
                        <span style="color: #000000;">$PROJECT_NAME</span>
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #beedc7; width: 150px;" nowrap="nowrap">
                        <span style="color: #000000;">Build Number</span>
                    </td>
                    <td style="background-color: #beedc7; width: 643px;" nowrap="nowrap">
                        <span style="color: #000000;">$BUILD_NUMBER</span>
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #beedc7; width: 150px;" nowrap="nowrap">
                        <span style="color: #000000;">Build Status</span>
                    </td>
                    <td style="background-color: #beedc7; width: 643px;" nowrap="nowrap">
                        <span style="color: #000000;">$BUILD_STATUS</span>
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #beedc7; width: 150px;" nowrap="nowrap">
                        <span style="color: #000000;">Trigger Reason</span>
                    </td>
                    <td style="background-color: #beedc7; width: 643px;" nowrap="nowrap">
                        <span style="color: #000000;">${CAUSE}</span>
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #3498db; width: 801px; text-align: left;" colspan="2" nowrap="nowrap">
                        <span style="color: #000000;">Test Information</span>
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #beedc7; border-color: gray; width: 150px;" nowrap="nowrap">
                        <span style="color: #000000;">Build&nbsp;Result</span>
                    </td>
                    <td style="background-color: #beedc7; border-color: gray; width: 643px;" nowrap="nowrap">
                        <span style="color: #000000;"><a style="color: #000000;" title="Build Result" href="${BUILD_URL}console">${BUILD_URL}</a></span>
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #beedc7; border-color: gray; width: 150px;" nowrap="nowrap">
                        <span style="color: #000000;">Build Log</span>
                    </td>
                    <td style="background-color: #beedc7; border-color: gray; width: 643px;" nowrap="nowrap">
                        <span style="color: #000000;"><a style="color: #000000;" title="Build Log" href="${BUILD_URL}console">${BUILD_URL}console</a></span>
                    </td>
                </tr>
                <tr>
                    <td style="background-color: #beedc7; border-color: gray; width: 150px;" nowrap="nowrap">
                        <span style="color: #000000;">Log&amp;Report</span>
                    </td>
                    <td style="background-color: #beedc7; border-color: gray; width: 643px;" nowrap="nowrap">
                        <br>
                        <ul>
                            <li>
                                <span style="color: #000000;">Test Report:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <a style="color: #000000;" title="Test Report" href="${BUILD_URL}testReport">${BUILD_URL}testReport</a></span>
                            </li>
                            <li>
                                <span style="color: #000000;">Pylint Violations Report:&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; <a style="color: #000000;" title="Pylint Violations Report" href="${BUILD_URL}violations">${BUILD_URL}violations</a></span>
                            </li>
                            <li>
                                <span style="color: #000000;">Cobertura Coverage Report:&nbsp;&nbsp; <a style="color: #000000;" title="Cobertura Coverage Report" href="${BUILD_URL}cobertura">${BUILD_URL}cobertura</a></span>
                            </li>
                        </ul>
                    </td>
                </tr>
             </tbody>
        </table>
    </body>
</html>
```

邮件附件信息

<img class="shadow" src="/img/in-post/nose_jenkins12.png" width="1200">

在Attachment处，填写如下附件路径信息：

```report/create_cluster.html,report/setup_cluster.html,report/all_test_cases.html,report/nose_autotest.log ```


设置Publish JUnit test result report
 
<img class="shadow" src="/img/in-post/nose_jenkins13.png" width="1200">

设置Publish Cobertura coverage report

<img class="shadow" src="/img/in-post/nose_jenkins14.png" width="1200">
 

设置 Report Violation
 
<img class="shadow" src="/img/in-post/nose_jenkins15.png" width="1200">

在pylint处，录入report/pylint
 
<img class="shadow" src="/img/in-post/nose_jenkins16.png" width="1200">

### 4）部分命令记录

这部分命令，已经写入到run.py中，如果想手动单独执行，可以参考如下命令

#### 生成nosetests.xml

```nosetests --tc=runs:1 --with-xunit --traverse-namespace --with-coverage --cover-package=/home/nose_framework/src --cover-inclusive --with-progressive --with-colorunit --with-html --html-report=../report/all_case.html ```

#### 生成coverage.xml

```python -m coverage xml --include=/home/nose_framework/src* ```

#### pylint

```
cd /home/nose_framework/src

pylint --rcfile=.pylintrc -f parseable -d I0011,R0801 * | tee pylint.out
```

#### 效果图

<img class="shadow" src="/img/in-post/nose_jenkins17.png" width="1200">

说明：
* 1、右侧，pylint，显示代码规范质量曲线图
* 2、点击" Code Coverage" 查看测试代码覆盖率
* 3、点击 “最新测试结果”，查看具体的HTML测试报告

##### 测试代码覆盖率

<img class="shadow" src="/img/in-post/nose_jenkins18.png" width="1200">

##### HTML展示用例测试结果

<img class="shadow" src="/img/in-post/nose_jenkins19.png" width="1200">

##### 邮件接收人接收到的邮件信息

<img class="shadow" src="/img/in-post/nose_jenkins20.png" width="1200">

# Jenkins 碰到的问题


## 1、无法正常发送邮件

test邮件是OK的，但是每次build的结果，无法正常发送邮件，console信息显示：

<img class="shadow" src="/img/in-post/nose_jenkins21.png" width="1200">

问题解决方法

这个问题是Jenkins管理用户的一个问题，它可以自动从git或者svn读取用户信息以及邮件（如果git等中设置了的话）， 但它不又不创建Jenkins上的用户，所以你可以在pepole列表上看到有用户名，但在jenkins的用户列表上又没有该用户。

修复的方法也比较简单，就是用admin登陆jenkins，帮所有people列表上的用户设置一下默认密码（自己约定）并保存，则会创建相应的jenkins用户了，这样用户就都是registrered用户了。

详请参考：```https://www.oschina.net/question/3567295_2246136 ```

## 2、Console 信息出现颜色值

如下图所示

<img class="shadow" src="/img/in-post/nose_jenkins22.png" width="1200">

上图中的“[32m[1m”即为颜色值，不太美观，改进之。

Jenkins 有 一 个 插 件 AnsiColor， 详 请 参 考 ： ```https://www.jianshu.com/p/12083063957b?utm_campaign=maleskine&utm_content=note&ut m_medium=seo_notes&utm_source=recommendation ```

安装成功并重启Jenkins 服务后，在 Build Environment 处，选择“Color ANSI Console Output”，并设置“ANSI color map”为 xterm 即可：

<img class="shadow" src="/img/in-post/nose_jenkins23.png" width="1200">

效果图：

<img class="shadow" src="/img/in-post/nose_jenkins24.png" width="800">


---
layout:     post
title:      "pytest+request+allure自动化指南"
subtitle:   "Use guide of pytest+request+allure"
date:       2020-03-07
author:     "Gavin"
catalog:    true
tags:
    - Automation
---


# 概述

之前一直用nose完成了产品的1000多个自动化用例，再来学习一下pytest。

本文基于Ubuntu16.04，介绍pytest+request+allure的安装与使用，并结合产品，给出具体示例。



# 安装pytest、测试所需lib与pytest plugin

## 安装pytest

升级python-pip

```
pip install --upgrade pip
```

需要先升级python-pip，否则安装pytest可能会报：

```
root@ubuntu16:~# pip install -U pytest
Collecting pytest
  Downloading https://files.pythonhosted.org/packages/f0/5f/41376614e41f7cdee02d22d1aec1ea028301b4c6c4523a5f7ef8e960fe0b/pytest-5.3.5.tar.gz (990kB)
    100% |████████████████████████████████| 993kB 9.5kB/s 
  Running setup.py (path:/tmp/pip-build-lmAIQc/pytest/setup.py) egg_info for package pytest produced metadata for project name unknown. Fix your #egg=pytest fragments.
Collecting py>=1.5.0 (from unknown)
  Downloading https://files.pythonhosted.org/packages/99/8d/21e1767c009211a62a8e3067280bfce76e89c9f876180308515942304d2d/py-1.8.1-py2.py3-none-any.whl (83kB)
    100% |████████████████████████████████| 92kB 12kB/s 
Collecting packaging (from unknown)
  Downloading https://files.pythonhosted.org/packages/98/42/87c585dd3b113c775e65fd6b8d9d0a43abe1819c471d7af702d4e01e9b20/packaging-20.1-py2.py3-none-any.whl
Collecting attrs>=17.4.0 (from unknown)
  Downloading https://files.pythonhosted.org/packages/a2/db/4313ab3be961f7a763066401fb77f7748373b6094076ae2bda2806988af6/attrs-19.3.0-py2.py3-none-any.whl
Collecting more-itertools>=4.0.0 (from unknown)
  Downloading https://files.pythonhosted.org/packages/a0/47/6ff6d07d84c67e3462c50fa33bf649cda859a8773b53dc73842e84455c05/more-itertools-8.2.0.tar.gz (82kB)
    100% |████████████████████████████████| 92kB 11kB/s 
    Complete output from command python setup.py egg_info:
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/tmp/pip-build-lmAIQc/more-itertools/setup.py", line 5, in <module>
        from more_itertools import __version__
      File "/tmp/pip-build-lmAIQc/more-itertools/more_itertools/__init__.py", line 1, in <module>
        from .more import *  # noqa
      File "/tmp/pip-build-lmAIQc/more-itertools/more_itertools/more.py", line 480
        yield from iterable
                 ^
    SyntaxError: invalid syntax
    
    ----------------------------------------
Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-build-lmAIQc/more-itertools/
You are using pip version 8.1.1, however version 20.0.2 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
root@ubuntu16:~# 
```



成功升级python-pip后，安装pytest

```
root@ubuntu16:~# pip install -U pytest
WARNING: pip is being invoked by an old script wrapper. This will fail in a future version of pip.
Please see https://github.com/pypa/pip/issues/5599 for advice on fixing the underlying issue.
To avoid this problem you can invoke Python with '-m pip' instead of running pip directly.
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support
Collecting pytest
  Downloading pytest-4.6.9-py2.py3-none-any.whl (231 kB)
     |████████████████████████████████| 231 kB 9.2 kB/s 
Collecting atomicwrites>=1.0
  Downloading atomicwrites-1.3.0-py2.py3-none-any.whl (5.9 kB)
Collecting pluggy<1.0,>=0.12
  Downloading pluggy-0.13.1-py2.py3-none-any.whl (18 kB)
Collecting packaging
  Using cached packaging-20.1-py2.py3-none-any.whl (36 kB)
Collecting attrs>=17.4.0
  Using cached attrs-19.3.0-py2.py3-none-any.whl (39 kB)
Collecting importlib-metadata>=0.12; python_version < "3.8"
  Downloading importlib_metadata-1.5.0-py2.py3-none-any.whl (30 kB)
Collecting six>=1.10.0
  Downloading six-1.14.0-py2.py3-none-any.whl (10 kB)
Collecting funcsigs>=1.0; python_version < "3.0"
  Downloading funcsigs-1.0.2-py2.py3-none-any.whl (17 kB)
Collecting wcwidth
  Downloading wcwidth-0.1.8-py2.py3-none-any.whl (17 kB)
Collecting more-itertools<6.0.0,>=4.0.0; python_version <= "2.7"
  Downloading more_itertools-5.0.0-py2-none-any.whl (52 kB)
     |████████████████████████████████| 52 kB 10 kB/s 
Collecting pathlib2>=2.2.0; python_version < "3.6"
  Downloading pathlib2-2.3.5-py2.py3-none-any.whl (18 kB)
Collecting py>=1.5.0
  Using cached py-1.8.1-py2.py3-none-any.whl (83 kB)
Collecting pyparsing>=2.0.2
  Downloading pyparsing-2.4.6-py2.py3-none-any.whl (67 kB)
     |████████████████████████████████| 67 kB 16 kB/s 
Collecting contextlib2; python_version < "3"
  Downloading contextlib2-0.6.0.post1-py2.py3-none-any.whl (9.8 kB)
Collecting zipp>=0.5
  Downloading zipp-1.1.0-py2.py3-none-any.whl (4.6 kB)
Collecting configparser>=3.5; python_version < "3"
  Downloading configparser-4.0.2-py2.py3-none-any.whl (22 kB)
Collecting scandir; python_version < "3.5"
  Downloading scandir-1.10.0.tar.gz (33 kB)
Building wheels for collected packages: scandir
  Building wheel for scandir (setup.py) ... done
  Created wheel for scandir: filename=scandir-1.10.0-cp27-cp27mu-linux_x86_64.whl size=38910 sha256=318f6b008a74163b37a42f027091fa98a43455d9ea1e46866cd3f5851d74e271
  Stored in directory: /root/.cache/pip/wheels/58/2c/26/52406f7d1f19bcc47a6fbd1037a5f293492f5cf1d58c539edb
Successfully built scandir
Installing collected packages: atomicwrites, contextlib2, six, scandir, pathlib2, zipp, configparser, importlib-metadata, pluggy, pyparsing, packaging, attrs, funcsigs, wcwidth, more-itertools, py, pytest
Successfully installed atomicwrites-1.3.0 attrs-19.3.0 configparser-4.0.2 contextlib2-0.6.0.post1 funcsigs-1.0.2 importlib-metadata-1.5.0 more-itertools-5.0.0 packaging-20.1 pathlib2-2.3.5 pluggy-0.13.1 py-1.8.1 pyparsing-2.4.6 pytest-4.6.9 scandir-1.10.0 six-1.14.0 wcwidth-0.1.8 zipp-1.1.0
root@ubuntu16:~#
```

确认pytest版本

```
root@ubuntu16:~# pytest --version
This is pytest version 4.6.9, imported from /usr/local/lib/python2.7/dist-packages/pytest.pyc
setuptools registered plugins:
  pytest-ssh-0.1 at /usr/local/lib/python2.7/dist-packages/pytest_ssh-0.1-py2.7.egg/pytest_ssh/plugin.py
root@ubuntu16:~# 
```

## 安装pytest-progress

```
root@ubuntu16:~# pip install pytest-progress
```




## 安装 pytest-sugar

```
root@ubuntu16:~# pip install pytest-sugar
```


## 安装pytest-allure

注意，pytest-allure 与 pytest-allure-adaptor 互相冲突（https://blog.csdn.net/sinat_40831240/article/details/89711263），且pytest-allure-apaptor已经不维护了，建议安装pytest-allure。

```
root@ubuntu16:~# pip install allure-pytest
```


## 安装测试所需的模块

比如发起HTTP请求的request模块之类的，具体根据所需安装。


# 使用过程中碰到的问题

## request InsecureRequestWarning告警

用例执行时，出现如下文所示的告警内容：

```
root@ubuntu16:/home/pytest_framework/src# python -m pytest testcase/case_2_Accounts/test_common_account_settings.py
Test session starts (platform: linux2, Python 2.7.12, pytest 4.6.9, pytest-sugar 0.9.2)
rootdir: /home/pytest_framework/src
plugins: ssh-0.1, progress-1.2.1, metadata-1.8.0, sugar-0.9.2, html-1.22.1
collecting ... 
====================================================================================== warnings summary =======================================================================================
/usr/lib/python2.7/dist-packages/urllib3/connectionpool.py:794
  /usr/lib/python2.7/dist-packages/urllib3/connectionpool.py:794: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.org/en/latest/security.html
    InsecureRequestWarning)

testcase/case_2_Accounts/test_common_account_settings.py:14
  /home/pytest_framework/src/testcase/case_2_Accounts/test_common_account_settings.py:14: PytestCollectionWarning: cannot collect test class 'TestCommonAccountSettings' because it has a __init__ constructor (from: testcase/case_2_Accounts/test_common_account_settings.py)
    class TestCommonAccountSettings(AccountManager):

-- Docs: https://docs.pytest.org/en/latest/warnings.html

Results (2.97s):
```

这里有两个告警，一个是request的，一个是测试用例的 \__init__ constructor，

对于request

```
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
```

对于测试用例，在执行用例时，可以增加```-W ignore::pytest.PytestCollectionWarning```进行屏蔽
示例如下：

```
root@ubuntu16:/home/pytest_framework/src# python -m pytest testcase/case_2_Accounts/test_common_account_settings.py -W ignore::pytest.PytestCollectionWarning
Test session starts (platform: linux2, Python 2.7.12, pytest 4.6.9, pytest-sugar 0.9.2)
rootdir: /home/pytest_framework/src
plugins: ssh-0.1, progress-1.2.1, metadata-1.8.0, sugar-0.9.2, html-1.22.1
collecting ... 

Results (1.77s):
```

参考链接如下：

https://stackoverflow.com/questions/58624641/how-to-prevent-pytestcollectionwarning-when-testing-class-testament-via-pytest
https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho


pytest会跳过类中定义__init__()的用例

参考：

```
https://stackoverflow.com/questions/21430900/py-test-skips-test-class-if-constructor-is-defined
```

文中有这么一段：

```
py.test purposely skips classes which have a constructor. The reason for this is that classes are only used for structural reasons in py.test and do not have any inherent behaviour, while when actually writing code it is the opposite and much rarer to not have an .__init__() method for a class.
```

目前所写的测试用例并未通过增加```-W ignore::pytest.PytestCollectionWarning```参数来规避，而是契合上文提及的要求，避免在test case中出现\__init__


## 生成allure测试报告时，找不到allure

```
root@ubuntu16:/home/pytest_framework/src# allure serve allure-results/
allure: command not found
root@ubuntu16:/home/pytest_framework/src# 
```

解决方法：

### 在线安装

```
apt-add-repository ppa:qameta/allure
apt-get update 
apt-get install allure
```


### 本地安装

下载了最新的allure-commandline（https://dl.bintray.com/qameta/maven/io/qameta/allure/allure-commandline/2.13.2/）

将allure-commandline.tar.gz解压后，在python_3rd_lib目录下，有一个bin目录，目录下有allure和allure.bat

目前看，只能使用allure-command目录下的allure命令，将可执行文件allure拷贝到/usr/bin/目录下，执行allure会报错：

```
root@ubuntu16:/home/pytest_framework/src# allure generate ../report/ -o ./allure-reports/
Error: Could not find or load main class ru.yandex.qatools.allure.CommandLine
```

将allure命令路径，写到配置~/.bashrc文件中：
Step1. 将解压后的allure-2.13.2目录，复制到/opt目录下

Step2. 修改~/.bashrc文件，增加如下一行

```alias allure='/opt/allure-2.13.2/bin/allure' ```

Step3. Source一下~/.bashrc

至此，后面就可以直接使用allure命令了

```
root@ubuntu16:/home/pytest_framework# allure generate ./allure-results/ -o ./report/ --clean
Report successfully generated to ./report
root@ubuntu16:/home/pytest_framework# 
```


参考：

```https://stackoverflow.com/questions/43875741/allure-command-not-found-on-linux ```




## 使用allure生成报告时候，提示没有JAVA_HOME

```
root@ubuntu16:/home/pytest_framework/src# allure generate ../report/ -o ./allure-reports/
Could not find java implementation: try to set JAVA_HOME, JRE_HOME or add java to PATH
root@ubuntu16:/home/pytest_framework/src# 
```

这是因为allure是基于JAVA开发的，它的运行需要java的支持。

解决方法：

Step1、下载jdk相应版本，放入 /opt并解压


Step2、配置环境变量

```
vi /etc/profile
```

在最后加入(修改为自己的存放目录)

```
export JAVA_HOME=/opt/jdk1.8.0_161
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$CLASSPATH
export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
```

Step3、保存后source一下profile文件

执行 java –version显示如下即成功：

```
root@ubuntu16:~# source /etc/profile
root@ubuntu16:~# java -version
java version "1.8.0_161"
Java(TM) SE Runtime Environment (build 1.8.0_161-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.161-b12, mixed mode)
root@ubuntu16:~# 
```



## allure报告空白

一打开index.html，显示空白（下图是window本地访问）：

<img class="shadow" src="/img/in-post/allure_report_index_null.png" width="1200">


解决方法：

参考： https://blog.csdn.net/feishicheng/article/details/91970402

allure使用了两种方式来渲染页面。分别是allure open 和 allure serve。前者用于在本地渲染和查看结果，后者用于在本地渲染后对外展示结果。这里我们使用allure open。运行命令 allure open allure-report即可自动打开浏览器展示渲染好的结果。这里的allure-report为allure generate生成的结果所在目录。

根据上面的方法，成功展示如下：

<img class="shadow" src="/img/in-post/allure_cmd_bat.png" width="1200">

<img class="shadow" src="/img/in-post/allure_html_null.png" width="1200">

对于Ubuntu来说，则是执行如下操作：

```
root@ubuntu16:/home/pytest_framework/report# allure generate json/ -o html --clean
Report successfully generated to html
root@ubuntu16:/home/pytest_framework/report# allure open html/
Starting web server...
2020-03-07 11:43:22.434:INFO::main: Logging initialized @490ms to org.eclipse.jetty.util.log.StdErrLog
Can not open browser because this capability is not supported on your platform. You can use the link below to open the report manually.
Server started at <http://127.0.1.1:44307/>. Press <Ctrl+C> to exit
```



## 给Allure report中增加测试环境信息

在allure html report界面，有一项测试环境信息，如何展示被测环境的信息呢？

<img class="shadow" src="/img/in-post/allure_report_env_null.png" width="1200">

在allure html report生成前，在对应的json目录下增加environment.properties ：

```
root@ubuntu16:/home/pytest_framework/report/json# cat environment.properties 
Product=Scaler 7.0-889 (202002280200~2b00e3b44)
HostIP=172.17.75.97
StartTime=2020-03-02 17:58:56
EndTime=2020-03-03 20:04:25

root@ubuntu16:/home/pytest_framework/report/json# 
```

然后再生成allure html report：

<img class="shadow" src="/img/in-post/allure_report_env_show.png" width="1200">


## Allure html report中不展示log的日期

如下图所示，在查看测试用例运行日志时，log里面并没有日期记录，一旦测试用例失败，可以根据展示的日期，迅速判断问题发生前后时间点，根据前后时间点查找产品日志：

<img class="shadow" src="/img/in-post/allure_report_no_time.png" width="1200">



解决方法：

在pytest.ini文件中，增加了log_format && log_data_format

```
log_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_date_format=%Y-%m-%d %H:%M:%S
```

这样生成的allure html report中，就会有时间戳了：

<img class="shadow" src="/img/in-post/allure_report_show_timestamp.png" width="1200">



## Allure html report中出现[[32m之类的符号

如下图所示：

<img class="shadow" src="/img/in-post/allure_report_log_color.png" width="1200">



查看了pytest的help信息，有这么一项：

```
--color=color         color terminal output (yes/no/auto).
```

在用例执行时，携带上这个参数（--color=no），则不会在report中展示这些符号了。



## Allure html report Overview界面不显示类别和趋势

没显示“Categories”，是因为只有在测试用例出错的情况下，这个区域才会显示；

没显示“Trend”，是因为需要与集成工具（比如jenkins）使用后方可展示。

# 完整参数用例示例

## 代码目录结构

```
root@ubuntu16:/home/pytest_framework# ll
total 56
drwxr-xr-x 8 root root  4096 Mar  7 11:56 ./
drwxr-xr-x 4 root root  4096 Mar  7 11:55 ../
-rw-r--r-- 1 root root     0 Feb 21 11:20 __init__.py
drwxr-xr-x 3 root root  4096 Mar  4 14:03 python_3rd_lib/
drwxr-xr-x 4 root root  4096 Mar  7 11:43 report/
drwxr-xr-x 6 root root  4096 Mar  7 11:55 src/
root@ubuntu16:/home/pytest_framework#
root@ubuntu16:/home/pytest_framework# cd src
root@ubuntu16:/home/pytest_framework/src# ll
total 60
drwxr-xr-x 6 root root  4096 Mar  7 11:55 ./
drwxr-xr-x 8 root root  4096 Mar  7 11:56 ../
-rw-r--r-- 1 root root   579 Mar  2 13:46 clear_pyc.py
drwxr-xr-x 2 root root  4096 Mar  7 11:54 common/
drwxr-xr-x 2 root root  4096 Mar  5 11:37 config/
-rw-r--r-- 1 root root  1186 Mar  4 15:33 conftest.py
-rw-r--r-- 1 root root     0 Mar  2 13:46 __init__.py
-rw-r--r-- 1 root root 17511 Mar  2 13:46 .pylintrc
-rw-r--r-- 1 root root   472 Mar  7 10:53 pytest.ini
-rw-r--r-- 1 root root   291 Mar  4 14:06 run.py
drwxr-xr-x 3 root root  4096 Mar  7 11:54 testcase/
drwxr-xr-x 3 root root  4096 Mar  7 11:54 testcasebase/
root@ubuntu16:/home/pytest_framework/src# 
root@ubuntu16:/home/pytest_framework/src/common# ll
total 80
drwxr-xr-x 2 root root  4096 Mar  7 11:54 ./
drwxr-xr-x 6 root root  4096 Mar  7 11:55 ../
-rw-r--r-- 1 root root 18822 Mar  2 13:46 api.py
-rw-r--r-- 1 root root  6678 Mar  2 13:46 config.py
-rw-r--r-- 1 root root  4874 Mar  2 13:46 errors.py
-rw-r--r-- 1 root root  9727 Mar  2 13:46 http_session.py
-rw-r--r-- 1 root root     0 Mar  2 13:46 __init__.py
-rw-r--r-- 1 root root   741 Mar  2 13:46 path_util.py
-rw-r--r-- 1 root root  6296 Mar  3 15:05 ssh.py
-rw-r--r-- 1 root root  9462 Mar  2 13:46 util.py
root@ubuntu16:/home/pytest_framework/src/common# 
```

说明：

* common目录下
  * * api.py 存放产品的CGI
    * ssh.py 用来建立当前客户端到服务端的ssh链接；
    * path_util.py 获取配置文件路径和测试报告路径
    * util.py 常用函数的封装，比如创建指定长度的字符串、数字串、智能等待等
    * http_session.py 封装发起不同类型的HTTP消息，以及返回结果
    * errors.py 存放产品错误码，以及常见的HTTP返回状态码（200,401,500等）
* testcase 存放具体测试用例，纯粹调用testcasebase的函数，所有的检查点，全部放在testcasebase中
* testcasebase 各个用例基类，构造http消息体，发送http请求，对请求结果做检测，对产品应用层做检测
* config目录，存放被测环境配置信息
* run.py 给jenkins使用，执行所有测试用例或指定用例的入口



## 主要文件内容

### conftest.py

```
import pytest
import logging

@pytest.fixture(scope='package', autouse=True)
def testsuite_setup_teardown():
    logging.info('------------------------------------- Start to run test case ---------------------------------\n')
    yield
    logging.info('------------------------------------- End to run test case------------------------------------')


@pytest.fixture(scope='function', autouse=True)
def testcase_setup_teardown():
    case_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]

logging.info('----------------------------------- Begin ----------------------------------------')
logging.info('Current test case name : (%s)', case_name)
yield
logging.info('----------------------------------- End ------------------------------------------\n')
```



### pytest.ini

```
root@ubuntu16:/home/pytest_framework/src# cat pytest.ini 
[pytest]
log_cli = false
log_level = NOTSET
log_file = ../report/pytest_autotest.log
log_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_date_format=%Y-%m-%d %H:%M:%S
log_file_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_file_date_format=%Y-%m-%d %H:%M:%S
log_cli_level = INFO
log_cli_format = %(asctime)s [%(filename)s:%(lineno)-4s] [%(levelname)5s] %(message)s
log_cli_date_format=%Y-%m-%d %H:%M:%S
root@ubuntu16:/home/pytest_framework/src#
```


## api.py部分内容

```
root@ubuntu16:/home/pytest_framework/src/common# cat api.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""  All of API """

from __future__ import unicode_literals

from config import GetConfig as config


class LoginInterface(object):
    """  Login API  """
login_interface = config.host + '/cgi/login?'

```



## 测试用例基类示例


```
root@ubuntu16:/home/pytest_framework/src/testcasebase/Account# cat account.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""  Account class base  """

from __future__ import unicode_literals

import json
import urllib
import logging
import requests

from common.http_session import HttpSession
from common.config import GetConfig as config
from common.errors import HttpCode, StatusCode
from common.api import LoginInterface, AccountInterface
from common.util import rand_low_ascii, assert_check, ssh_session


ETC_PASSWD = "/etc/passwd"


class AccountManager(object):
    """  Account manager test case base class  """

    session = HttpSession().login_session()

    @staticmethod
    def add_user_data(user_id=None, display_name=None, email=None, password=None, confirm_password=None,
                      account_type=None, account_dn=None):
        """
        add account data
        :param user_id, string, account id
        :param display_name, string, an account display name
        :param email, string, email address for an account
        :param password, int or string, password for an account
        :param confirm_password, int or string, password for an account
        :param account_type, string, account type
        :param account_dn, string, account dn
        """

        data = {
            'user_id': user_id,
            'display_name': display_name,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'type': account_type,
            'dn': account_dn
        }

        return data

    def add_user(self, user_id=None, display_name=None, email=None, password=None, confirm_password=None,
                 account_type=None, account_dn=None, expect_return_code=None, need_check=None):
        """
        add account
        :param user_id, string, account id
        :param display_name, string, an account display name
        :param email, string, email address for an account
        :param password, int or string, password for an account
        :param confirm_password, int or string, password for an account
        :param account_type, string, account type
        :param account_dn, string, account dn
        :param expect_return_code, string, expected http response content return code, default is success
        :param need_check, bool, check sync result or not, defualt value is True, it means check
        """
        user_id = rand_low_ascii(6) if user_id is None else user_id
        display_name = user_id if display_name is None else display_name
        email = rand_low_ascii() + u'@163.com' if email is None else email
        password = '1' if password is None else password
        confirm_password = password if confirm_password is None else confirm_password
        account_type = '' if account_type is None else account_type
        account_dn = '' if account_dn is None else account_dn
        expect_return_code = StatusCode.SUCCESS if expect_return_code is None else expect_return_code
        need_check = True if need_check is None else need_check

        add_user_url = AccountInterface().add_acount
        add_user_data = self.add_user_data(user_id=user_id,
                                           display_name=display_name,
                                           email=email,
                                           password=password,
                                           confirm_password=confirm_password,
                                           account_type=account_type,
                                           account_dn=account_dn)

        logging.info('[Action]   Start to add a user: (%s)', user_id)
        add_user_request = HttpSession().http_request(self.session, 'GET', add_user_url, params=add_user_data)
        logging.info('[Check]    Check add user : (%s) result', user_id)
        add_user_err_msg = '[ERROR] Add user account fail, background return: {}'.format(add_user_request.text)
        assert HttpCode.SUCCESS == add_user_request.status_code
        assert expect_return_code == json.loads(add_user_request.text)['return_code']

        if expect_return_code == StatusCode.SUCCESS:
            if account_type != "AD":
                if need_check is True:
                    self.check_user_sync_rados(user_id)
                    self.check_user_in_radosgw(user_id)
                    # self.check_user_sync_system(user_id)
                    self.check_user_sync_samba(user_id)
                    logging.info('[Success]  Add account : (%s) success.', user_id)
                else:
                    logging.info('[SKIP]     Need_check is : (%s), so no need to check', need_check)
            else:
                if need_check is True:
                    self.check_user_sync_rados(user_id)
                    logging.info('[Success]  Add AD/LDAP account success.')
                else:
                    logging.info('[SKIP]     Import user from AD/LDAP, but need_check is : (%s), '
                                 'so does not need to check', need_check)
            return user_id
        else:
            logging.info("[Abnormal Scene Test]  Add an account failed as expected, "
                         "backend return: (%s)", add_user_request.text)
            return

    @assert_check
    def check_user_sync_system(self, user_id, vs_name=None):
        """
        :param user_id, string, a user name
        :param vs_name, string, a virtual storage name
        """
        logging.info("[Check]   Start to check user : (%s) sync to system", user_id)

        # should not in /etc/passwd
        vs_name = 'Default' if vs_name is None else vs_name

        all_ctdb_nodes = get_ctdb_nodes(vs_name).strip()
        ctdb_nodes = list()

        for line in all_ctdb_nodes.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            ctdb_nodes.append(line)

        for each_node in ctdb_nodes:
            cmd = "cat {} | grep {} | awk -F ':' '{{print $1}}'".format(each_node, ETC_PASSWD, user_id)
            res_status, etc_passwd = ssh_session().run_cmd(cmd)
            logging.info("[Check]    [Add user]  Check user in : /etc/passwd on node : (%s)", each_node)
            err_msg = 'Found account : ({}) in /etc/passwd on node : ({})'.format(user_id, each_node)
            assert '' == etc_passwd.strip(), err_msg

    @assert_check
    def check_user_sync_samba(self, user_id):
        """
        :param user_id, string, a user name
        """
        logging.info("[Check]   Start to check user : (%s) sync to samba", user_id)

        # should not in samba
        res_status, ctdb_db_tmp = ssh_session().run_cmd("pdbedit -L | grep {}".format(user_id))
        ctdb_db_user = ctdb_db_tmp.split(":")

        logging.info("[Check]    [Add user]  Check user in samba: pdbedit -L | grep %s", user_id)
        err_msg = '[ERROR]  Found ({}) in samba'.format(user_id)
        assert '' == ctdb_db_user[0], err_msg

    @assert_check
    def check_user_sync_rados(self, user_id, op_type=None):
        """
        Check in rados
        :param user_id, string, a user name
        :param op_type, string, add or del
        """
        logging.info("[Check]    Start to check user : (%s) sync to rados", user_id)

        op_type = 'add' if op_type is None else op_type

        res_status, user_in_rados = ssh_session().run_cmd("rados -p default.rgw.users.uid ls | grep {}".format(user_id))

        logging.info("[Check]    [Add user]  Check user in rados : "
                     "rados -p default.rgw.users.uid ls | grep %s", user_id)
        if op_type == 'add':
            err_msg = '[ERROR]  Not found ({}) in rados'.format(user_id)
            assert user_id == user_in_rados.strip(), err_msg
        elif op_type == 'del':
            err_msg = '[ERROR]  Found ({}) in rados'.format(user_id)
            assert '' == user_in_rados.strip(), err_msg

    @assert_check
    def check_user_in_radosgw(self, user_id):
        """
        :param user_id, string, a user name
        """
        logging.info("[Check]   Start to check user : (%s) in radosgw", user_id)

        res_status, user_info = ssh_session().run_cmd("radosgw-admin --uid={} user info".format(user_id))
        assert user_id in user_info, "[ERROR]  Not found user in radosgw-admin, will retry again."

    @staticmethod
    def delete_user_data(user_id):
        """
        delete user, return HTTP get url
        :param user_id, string, account id
        """
        request_body = {'user_ids': '["' + user_id + '"]'}

        data = urllib.urlencode(request_body)
        return data

    def delete_user(self, user_id, expected_return_code=None, need_check=None):
        """
        delete user operation
        :param user_id, string, account id
        :param expected_return_code, strins, return status code
        :param need_check, bool, check account sync results
        """
        expected_return_code = StatusCode.SUCCESS if expected_return_code is None else expected_return_code
        need_check = True if need_check is None else need_check

        # logging.debug('Structure delete account HTTP message body')
        delete_user_url = AccountInterface().del_user
        delete_user_body = self.delete_user_data(user_id)

        logging.info('[Action]   Delete account : (%s)', user_id)
        for i in xrange(10):
            delete_user_res = HttpSession().http_request(self.session, 'POST', delete_user_url, data=delete_user_body)
            if json.loads(delete_user_res.text)['return_code'] == StatusCode.DELETE_USER_ERROR:
                # Delete user failed, KVStoreError: KVStoreError: fetching entry sds_admin_account timeout
                logging.warn("[Warn]  Delete user : (%s) failed, backend return : (%s)", user_id, delete_user_res.text)
                time.sleep(5)
            else:
                break

        logging.info('[Check]    Check delete user result.')

        delete_user_err_msg = "[ERROR]  Delete user failed, background return is {}".format(delete_user_res)
        assert HttpCode.SUCCESS == delete_user_res.status_code, delete_user_err_msg
        assert expected_return_code == json.loads(delete_user_res.text)['return_code'], delete_user_err_msg

        if need_check is True:
            self.check_user_sync_rados(user_id, op_type='del')
            logging.info('[Success]  Delete user : (%s) success.', user_id)
        else:
            logging.info("[SKIP]     Set need_check is : (%s), so no need to check", need_check)
root@ubuntu16:/home/pytest_framework/src/testcasebase/Account# 
```





## 测试用例示例



```
root@ubuntu16:/home/pytest_framework/src/testcase/case_2_Accounts# cat test_common_account_settings.py 
#!/usr/bin/env python

# -*- coding:UTF-8 -*-

"""  Test case of common account settings  """

from __future__ import unicode_literals

import allure
import logging

from common.errors import StatusCode
from testcasebase.Account.account import AccountManager


class TestCommonAccountSettings(AccountManager):
    """  test case for: common account settings  """
@allure.tag('RAT')
def test_add_user_success(self):
    """  Sc-48:Create new user  """
    user_id = self.add_user()
    self.delete_user(user_id)
```



## 用例的执行

示例如下：

```
root@ubuntu16:/home/pytest_framework/src# python clear_pyc.py; clear; PYTHONPATH=. py.test -v --cache-clear --alluredir ../report/json testcase/case_2_Accounts/test_common_account_settings.py 
```



# 与Jenkins结合

非本文重点，略


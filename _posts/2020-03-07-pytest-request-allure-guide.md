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

https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-python


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

下载allure-commandline（https://dl.bintray.com/qameta/maven/io/qameta/allure/allure-commandline/2.13.2/）

将allure-commandline.tar.gz解压后，在python_3rd_lib目录下，有一个bin目录，目录下有allure和allure.bat

使用allure-command目录下的allure命令，将可执行文件allure拷贝到/usr/bin/目录下，执行allure会报错：

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



## Allure html report中出现[32m、[0m之类的符号

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
  * * api.py 存放产品的API接口地址
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
            {% raw %}cmd = "cat {} | grep {} | awk -F ':' '{{print $1}}'".format(each_node, ETC_PASSWD, user_id) {% endraw %}
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

## 用例的执行入口

通过调用run.py，完成环境的检查、相关包的安装、以及用例的执行。

运行环境是Ubuntu14.04，经过多次摸索，确定只能使用pytest-4.6.9，脚本具体内容如下：

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Install package, ENV check and run test case  """

from __future__ import unicode_literals

import os
import sys
import time
import getopt
import shutil
import pexpect

from ezs3.cluster import ClusterManager
from ezs3.utils import get_storage_ip
from ezs3.notify_manager import WebEventCache
from ezs3.command import do_cmd, DoCommandError

from common.cluster import ClusterInfo, OSCheck
from common.path_util import get_report_path
from common.config import GetConfig as config


def clean_pyc():
    """  Clean pyc files  """
    for dirs, folders, files in os.walk('.'):
        for each_file in files:
            root, end = os.path.splitext(each_file)
            if end == '.pyc':
                os.remove(os.path.abspath(os.path.join(dirs, each_file)))


def mkdir_report_path():
    """  Create report path if not exist   """
    report_path = get_report_path()
    if not os.path.exists(report_path):
        os.mkdir(report_path)

    return report_path


def rm_sessions():
    """  Delete all session files in /tmp/sessions  """
    sessions_path = "/tmp/sessions"
    session_files_num = do_cmd('ls -l {}/* | wc -l', 30, True).strip()
    if int(session_files_num) != 0 and os.path.exists(sessions_path):
        storage_ip = get_storage_ip()
        WebEventCache(storage_ip).clean_all()
        do_cmd("rm {}/*".format(sessions_path), 30)


def get_test_product_version():
    """
    Get product version for jenkins email content
    """
    media_info = "/var/log/installer/media-info"
    version = '/etc/ezs3/version'

    if os.path.exists(media_info):
        full_version = do_cmd('cat {}'.format(media_info), 30).strip()
        p_version = full_version.split()[2] + ' ' + full_version.split()[3] + ' ' + full_version.split()[7]
    else:
        p_version = do_cmd('cat {}'.format(version), 30, True).strip()

    do_cmd("echo '{}' > ../report/version.txt".format(p_version), 30, True)


def physical_or_vm(ip=None):
    """
    Adjust the IP address is a physical machine or a VM
    :param ip, client IP or local host(if None)
    """
    cmd = 'dmidecode -s system-product-name | grep -v "#"'
    if ip:
        client_ip_passwd = config.white_ip_root_password
        port = config.ssh_port
        client_ip = config.white_list_ip
        if ip != client_ip:
            print "    [ERROR]    The given IP : ({}) is not same as client IP in " \
                  "autotest.config, exit!!!\n".format(ip)

        dmidecode_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port, client_ip, cmd)
        system_produce = do_cmd(dmidecode_cmd, 30, True).strip()
    else:
        system_produce = do_cmd(cmd, 30, True).strip()

    if not system_produce:
        print "        [ERROR]    Not get the system product name for client ({}), make sure the\n" \
              "                   client exist and power on\n".format(client_ip)
        sys.exit(0)

    if 'VM' in system_produce or 'Virtual' in system_produce:
        return False
    else:
        return True


def append_write(file_name, add_content):
    """
    Append content to file
    :param file_name, string. a file name, needs full path
    :param add_content, string, some content which will added to file_name
    """
    with open(file_name, 'a') as f:
        f.write(add_content)


def run_node_check():
    """  Check run node and configuration in autotest.conf   """
    print "[Step 1]  Check test case execution node.\n"

    public_ips = config.public_ips
    all_public_ips = public_ips.split()
    all_public_ips.sort()
    storage_ips = config.storage_ips
    all_storage_ips = storage_ips.split()
    public_iface = config.public_iface
    storage_iface = config.storage_iface
    client_ip = config.white_list_ip
    client_ip_passwd = config.white_ip_root_password
    port = config.ssh_port

    # Check the client, should install NFS and CIFS, need to remove old SSH to skip
    # error of "Permission denied (publickey,password)"
    do_cmd("ssh-keygen -f '/root/.ssh/known_hosts' -R {}".format(client_ip), 30, True)

    print "    1-1 [Check]    Client : ({}) should install fio, multipath-tools, \n" \
          "                   openssh-server, open-iscsi and  NFS and CIFS".format(client_ip)

    grep_fio = "dpkg -l | grep fio"
    grep_multipath = "dpkg -l | grep multipath-tools"
    grep_ssh = "dpkg -l | grep openssh"
    grep_scsi = "dpkg -l | grep open-iscsi"
    grep_nfs = "dpkg -l | grep nfs"
    grep_cifs = "dpkg -l | grep cifs"

    remote_fio = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port, client_ip, grep_fio)
    remote_multipath = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port,
                                                                        client_ip, grep_multipath)
    remote_ssh = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port, client_ip, grep_ssh)
    remote_scsi = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port, client_ip, grep_scsi)
    remote_nfs = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port, client_ip, grep_nfs)
    remote_cifs = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port, client_ip, grep_cifs)

    fio_exist = do_cmd(remote_fio, 30, True).strip()
    multipath_exist = do_cmd(remote_multipath, 30, True).strip()
    ssh_exist = do_cmd(remote_ssh, 30, True).strip()
    scsi_exist = do_cmd(remote_scsi, 30, True).strip()
    nfs_exist = do_cmd(remote_nfs, 30, True).strip()
    cifs_exist = do_cmd(remote_cifs, 30, True).strip()

    if not fio_exist:
        print "        [ERROR]    Client : ({}) not install fio, please run " \
              "'apt-get install fio' to install it\n".format(client_ip)
        sys.exit(0)

    if not multipath_exist:
        print "        [ERROR]    Client : ({}) not install multipath-tools, please run " \
              "'apt-get install multipath-tools ' to install it\n".format(client_ip)
        sys.exit(0)

    if not ssh_exist:
        print "        [ERROR]    Client : ({}) not install openssh-server, please run " \
              "'apt-get install openssh-server' to install it\n".format(client_ip)
        sys.exit(0)

    if not scsi_exist:
        print "        [ERROR]    Client : ({}) not install open-iscsi, please run " \
              "'apt-get install open-iscsi' to install it\n".format(client_ip)
        sys.exit(0)

    if not nfs_exist:
        print "        [ERROR]    Client : ({}) not install NFS, please run " \
              "'apt-get install nfs-kernel-server' to install it \n".format(client_ip)
        sys.exit(0)

    if not cifs_exist:
        print "        [ERROR]    Client : ({}) not install CIFS, please run " \
              "'apt-get install cifs-utils' to install it \n".format(client_ip)
        sys.exit(0)

    print "        [Success]  Client : ({}) installed fio, multipath-tools,\n" \
          "                   openssh-server, open-iscsi and  NFS and CIFS\n".format(client_ip)

    print "    1-2 [Check]    The running node must be non-first and non-last node"
    nums = len(all_public_ips)
    if nums < 3:
        print "        [ERROR]    A minimum of 3 nodes is required to execute test case, so exit!!!\n"
        sys.exit(0)

    list_before = all_public_ips[:nums-2]
    list_after = all_public_ips[nums-1:]

    list_union = list_before + list_after
    ip_a_info = do_cmd("ip a", 10, True).strip()
    for each_ip in list_union:
        if each_ip in ip_a_info:
            print "        [ERROR]    Forbidden to run case on first or last node, so exit!!!\n"
            sys.exit(0)
    else:
        print "        [Success]  Check the running node IP address successfully\n"

    print "    1-3 [Check]    The network between all nodes should be smooth"
    # Check public network for each node
    for each_public_ip in all_public_ips:
        ping_public_ip_res = do_cmd("ping {} -c 1".format(each_public_ip), 30, True)
        if ping_public_ip_res == "":
            print "        [ERROR]    Public IP of : ({}) unreachable, please check the public IP settings " \
                  "in autotest.config, and the node has been booted normally .".format(each_public_ip)
            sys.exit(0)
        else:
            print "        [Success]  Public IP of : ({}) reachable".format(each_public_ip)

    # Check storage network for each node
    for each_storage_ip in all_storage_ips:
        ping_storage_ip_res = do_cmd("ping {} -c 1".format(each_storage_ip), 30, True)
        if ping_storage_ip_res == "":
            print "        [ERROR]    The storage network of the fourth node is different from other nodes\n"
            sys.exit(0)
        else:
            print "        [Success]  Storage IP of : ({}) reachable".format(each_storage_ip)

    # Check the 4th nodes ip
    storage_ip_pref_1th = '.'.join(all_storage_ips[0].split('.')[:-1])
    storage_ip_pref_4th = '.'.join(config.host_4th_storage_ip.split('.')[:-1])
    if storage_ip_pref_1th == storage_ip_pref_4th:
        print "        [Success]  The forth node's storage IP can be used"
    else:
        print "        [ERROR]    Storage IP of : ({}) unreachable, please check the storage IP settings " \
                  "in autotest.config, and the node has been booted normally .".format(each_storage_ip)
        sys.exit(0)

    print "\n    1-4 [Check]    Check public and storage network interface on each node"
    for each_ip in all_public_ips:
        grep_pub_net_cmd = "ip a | grep {}".format(config.public_iface)
        grep_storage_net_cmd = "ip a | grep {}".format(config.storage_iface)
        rempte_grep_pub_net = "sshpass -p {} ssh -p {} -l root {} '{}'".format(config.root_pass,
                                                                               config.ssh_port, each_ip,
                                                                               grep_pub_net_cmd)
        rempte_storage_pub_net = "sshpass -p {} ssh -p {} -l root {} '{}'".format(config.root_pass,
                                                                                  config.ssh_port, each_ip,
                                                                                  grep_storage_net_cmd)

        grep_pub_net = do_cmd(rempte_grep_pub_net, 30, True).strip()
        grep_storage_net = do_cmd(rempte_storage_pub_net, 30, True).strip()

        if grep_pub_net and grep_storage_net:
            print "        [Success]  Public and Storage interface is correct on node ({})".format(each_ip)
        elif grep_pub_net and not grep_storage_net:
            print "        [ERROR]    Storage interface is incorrect on node ({}) in " \
                  "config/autotest.config\n".format(each_ip)
            sys.exit(0)
        elif not grep_pub_net and grep_storage_net:
            print "        [ERROR]    Public interface is incorrect on node ({}) " \
                  "in config/autotest.config\n".format(each_ip)
            sys.exit(0)
        else:
            print "        [ERROR]    Both Public and Storage interface is incorrect " \
                  "on node ({}) in config/autotest.config\n".format(each_ip)
            sys.exit(0)

    print "\n    1-5 [Check]    Check OSD device on each node, make sure the disk partition exist.\n" \
          "                   If OSD disk partition size gap on each node can not be too large, \n" \
          "                   otherwise PG is difficult to reach a healthy state in a short time"
    osd_device = config.osd_device
    disk_size_list = []

    for each_ip in all_public_ips:
        grep_dev_cmd = "lsblk | grep {} | head -n 1".format(osd_device)
        remote_grep_dev_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(config.root_pass,
                                                                               config.ssh_port, each_ip,
                                                                               grep_dev_cmd)
        grep_dev = do_cmd(remote_grep_dev_cmd, 30, True).strip()
        if 'SWAP' in grep_dev:
            print "        [ERROR]    OSD device is a OS partition on node ({}), please to \n" \
                   "                   check 'osd_device' " \
                   "in config/autotest.config\n".format(each_ip)
            sys.exit(0)

        if not grep_dev:
            print "        [ERROR]    Has no disk partition of ({}) on node ({}), please to \n" \
                   "                   check 'osd_device' in config/autotest.config\n".format(osd_device, each_ip)
            sys.exit(0)

        # Get size of OSD disk partition
        disk_size = grep_dev.split()[-3]
        if disk_size.endswith('G'):
            disk_size_list.append(disk_size.split('G')[0])
        elif disk_size.endswith('T'):
            disk_size_list.append(int(float(disk_size.split('T')[0]) * 1024))
        else:
            print "        [ERROR]    Get size of OSD disk partition is incorrect : ({})".format(disk_size)
            sys.exit(0)

    # Check OSD disk partition size
    if int(float(max(disk_size_list))) / int(float(min(disk_size_list))) > 2000:
        print "        [ERROR]    Size of OSD disk partition is very larger than other " \
               "node on node ({})".format(disk_size)
        sys.exit(0)

    print "        [Success]  Check OSD device on each node success\n"

    print "    1-6 [Check]    Service of apache on each node should be in running state"
    for each_ip in all_public_ips:
        ps_cmd = "ps -ef | grep apache | grep -v grep | wc -l"
        remote_ps_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(config.root_pass, 22, each_ip, ps_cmd)
        apache_pid_no = do_cmd(remote_ps_cmd, 60).strip()
        if int(apache_pid_no) == 0:
            print "        [ERROR]    Service of Apache2 is not running on node ({}), try to start it".format(each_ip)
            start_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(config.root_pass, 22,
                                                                         each_ip, config.restart_apache)
            do_cmd(start_cmd, 40, True)
            apache_pid_no = do_cmd(remote_ps_cmd, 60, True).strip()
            if int(apache_pid_no) == 0:
                print "        [ERROR]    Service of Apache2 is still not running on node ({}) after try " \
                     "to start it, so exit!!!\n".format(each_ip)
                sys.exit(0)
        else:
            print "        [Success]  Service of Apache2 is running on node ({})".format(each_ip)

    # Check ESXi host IP or IPMI IP
    print "\n    1-7 [Check]    Check ESXi host IP config or IPMI IP config in config/autotest.config"
    system_produce = physical_or_vm(ip=client_ip)
    # # Client is a VM
    if system_produce is False:
        list_vm_cmd = "vim-cmd vmsvc/getallvms"
        remote_list_vm_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(config.esxi_root_passwd, port,
                                                                              config.esxi_ip, list_vm_cmd)
        all_vms = do_cmd(remote_list_vm_cmd, 30, True).strip()
        if config.esxi_vm_host_name not in all_vms:
            print "        [ERROR]    Incorrect information in config/autotest.config about ESXi:\n" \
                  "                   (1) Not enabled SSH service on ESXi?\n" \
                  "                   (2) Wrong vm_host_name in config/autotest.config?\n" \
                  "                   (3) Wrong IP address or wrong password for root in config/autotest.config?\n"
            sys.exit(0)
        else:
            print "        [Success]  ESXi host information is correct in config/autotest.config\n"
    else:
        # Client is a physical machine
        get_ipmi_cmd = 'ipmitool lan print | grep "IP Address"'
        remote_get_ipmi_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port,
                                                                               client_ip, get_ipmi_cmd)
        ipmi_info = do_cmd(remote_get_ipmi_cmd, 30, True).strip()
        if ipmi_info:
            get_ipmi_ip = ipmi_info.split('\n')[-1].split(':')[-1].strip()
        else:
            get_ipmi_ip = 'not-get'

        if config.ipmi_ip not in ipmi_info:
            print "        [ERROR]    ipmi_ip is not correct in config/autotest.config, currently \n" \
                  "                   acquired : ({}), but in conf is : ({})\n".format(get_ipmi_ip, config.ipmi_ip)
            sys.exit(0)
        else:
            # Check ipmi user
            ipmi_user_list = []
            list_ipmi_user_cmd = "ipmitool user list -c"
            remote_list_user_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port,
                                                                                    client_ip, list_ipmi_user_cmd)
            ipmi_uses = do_cmd(remote_list_user_cmd, 30, True).strip()
            for each_user in ipmi_uses.split('\n'):
                user_name = each_user.split(',')[1]
                ipmi_user_list.append(user_name)

            if config.ipmi_user not in ipmi_user_list:
                print "        [ERROR]    ipmi_user is not correct in config/autotest.config\n"
                sys.exit(0)
            else:
                print "        [Success]  IPMI user is correct in config/autotest.config"

            # Check ipmi user's password
            try:
                list_frc_cmd = "ipmitool -H {} -I lanplus -U {} -P {} fru list".format(config.ipmi_ip,
                                                                                       config.ipmi_user,
                                                                                       config.ipmi_user_passwd)
                do_cmd(list_frc_cmd, 30).strip()
                print "        [Success]  IPMI of ipmi_user_passwd is correct in config/autotest.config\n"
            except DoCommandError as ex:
                if 'Unable to establish' in str(ex):
                    print "        [ERROR]    IPMI of ipmi_user_passwd is not correct in config/autotest.config\n"
                    sys.exit(0)
                else:
                    print "        [ERROR]    Get FRU list failed, backend return : ({})".format(str(ex))
                    sys.exit(0)

    # Check AD and LDAP reachable or not
    print "    1-8 [Check]    Check AD and LDAP reachable or not in config/autotest.config"
    ad_ip = config.ad_server_addr
    ldap_ip = config.ldap_server_addr

    if ad_ip == ldap_ip:
        print "        [ERROR]    AD IP is same as LDAP IP, please check AD and LDAP settings in autotest.config\n"
        sys.exit(0)

    ping_ad_res = do_cmd("ping {} -c 1".format(ad_ip), 60, True).strip()
    if ping_ad_res == "":
        print "        [ERROR]    AD : ({}) unreachable, please check AD settings " \
               "in autotest.config.".format(ad_ip)
        sys.exit(0)
    else:
        print "        [Success]  AD   : ({}) reachable".format(ad_ip)

    ping_ldap_res = do_cmd("ping {} -c 1".format(ldap_ip), 60, True).strip()
    if ping_ldap_res == "":
        print "        [ERROR]    LDAP : ({}) unreachable, please check LDAP " \
               "settings in autotest.config.".format(ldap_ip)
        sys.exit(0)
    else:
        print "        [Success]  LDAP : ({}) reachable\n".format(ldap_ip)

    # If other cluster has configured the DNS IP, should exit
    print "    1-9 [Check]    Check DNS IP in config/autotest.config"
    dns_ip = config.dns_ip
    try:
        ping_dns_res = do_cmd("ping -c2 {}".format(dns_ip), 60).strip()
        if ping_dns_res and '0% packet loss' in ping_dns_res:
            print "        [ERROR]    DNS IP of ({}) in config/autotest.config is used, " \
                      "please check the Environment.\n".format(dns_ip)
            sys.exit(0)
    except Exception as ex:
        print "        [Success]  DNS IP : ({}) is available in config/autotest.config\n".format(dns_ip)

    # If other environment used this takeover IP, should exit
    print "    1-10 [Check]    Check takeover IP in config/autotest.config"
    takeover_ip_list = []

    takeover_ips = config.takeover_ips
    for each_ip in takeover_ips.split():
        takeover_ip_list.append(each_ip.split('/')[0])

    node_ip_prefix = all_public_ips[0].split('.')[0:2]
    prefix_ip = takeover_ip_list[0].split('.')[0:2]
    if node_ip_prefix != prefix_ip:
        print "         [ERROR]    Takeover IP and public ip are not in same segment\n" \
              "                    Takeover IP is : {} \n" \
              "                    public ip is : {} \n" \
              "                    please check the Environment.\n".format(takeover_ips, public_ips)
        sys.exit(0)

    for each_takeover_ip in takeover_ip_list:
        ping_cmd = 'ping -c2 {}'.format(each_takeover_ip)
        try:
            ping_res = do_cmd(ping_cmd, 60).strip()
            if ping_res and '0% packet loss' in ping_res:
                print "         [ERROR]    Takeover IP of ({}) in config/autotest.config is used, " \
                      "please check the Environment.\n".format(each_takeover_ip)
                sys.exit(0)
        except Exception as ex:
            # print "        [ERROR]    Ping takeover IP : {} occur
            # exception : ({})".format(each_takeover_ip, str(ex))
            pass
    print "         [Success]  Takeover IP is available in config/autotest.config"

    # If other cluster used S3 takeover IP, should exit
    s3_takeover_ips = config.s3_takeover_ips
    s3_prefix_ip = s3_takeover_ips.split()[0].split('/')[0].split('.')[0:2]
    if node_ip_prefix != s3_prefix_ip:
        print "         [ERROR]    S3 takeover IP and public ip are not same segment, s3 takeover IP is {}, " \
                              "public ip is {}, please check the Environment.\n".format(s3_prefix_ip, public_ips)
        sys.exit(0)

    s3_vips = [each_ip.split(',')[0].split('/')[0] for each_ip in s3_takeover_ips.split()]
    s3_vip_union = list((set(s3_vips).union(set(all_public_ips))) ^ (set(s3_vips) ^ set(all_public_ips)))
    if len(s3_vip_union) > 0:
        print "         [ERROR]    S3 takeover IP in config/autotest.config should not include " \
               "cluster public IP, please check the Environment.\n"
        sys.exit(0)
    # # Check ping result
    for each_s3_vip in s3_vips:
        ping_cmd = "ping -c2 {}".format(each_s3_vip)
        try:
            ping_res = do_cmd(ping_cmd, 60).strip()
            if ping_res and '0% packet loss' in ping_res:
                print "         [ERROR]    S3 takeover IP of ({}) in config/autotest.config is used, " \
                      "please check the Environment.\n".format(each_s3_vip)
                sys.exit(0)
        except Exception as ex:
            # print "        [ERROR]    Ping S3 takeover IP : {} occur
            #  exception : ({})".format(each_takeover_ip, str(ex))
            pass
    print "         [Success]  S3 takeover IP is available in config/autotest.config\n"

    # Check public or storage interface should config in autotest.conf
    print "    1-11 [Check]    Check public and storage interface from config/autotest.config"

    iface = []
    local_iface = do_cmd('cat /etc/network/interfaces | grep iface').strip()
    for each_iface in local_iface.split('\n'):
        iface.append(each_iface.split()[1])

    if public_iface not in iface or storage_iface not in iface:
        print "         [ERROR]    public_iface or storage_iface is not correct in config/autotest.config\n"
        sys.exit(0)
    else:
        print "         [Success]  Public and storage interface are correct in config/autotest.config\n"

    # Check cluster network speed, avoid having more bandwidth unused
    print "    1-12 [Check]    Check public interface BW performance and DNS ip segment"

    all_nic_speed = {}
    for each_iface in iface:
        each_speed_info = do_cmd("ethtool {} | grep Speed | grep -v Unknown".format(each_iface), 30, True).strip()
        each_speed = each_speed_info.split(':')[-1].split('Mb/s')[0]
        all_nic_speed[each_iface] = each_speed.strip()

    local_public_speed_info = do_cmd("ethtool {} | grep Speed".format(public_iface), 30, True).strip()
    local_public_speed = local_public_speed_info.split(':')[-1].split('Mb/s')[0].strip()

    max_speed = max(all_nic_speed.values())
    max_speed_iface = []
    for key, value in all_nic_speed.iteritems():
        if value == max_speed:
            max_speed_iface.append(key)

    if int(max_speed) > int(local_public_speed):
        print "         [ERROR]    May not use 10G network, check public_iface or " \
              "storage_iface in config/autotest.config\n"
        sys.exit(0)
    else:
        # Check DNS ip, should use same segment network with public NIC
        _ip = []
        for each_nic in max_speed_iface:
            ip_info = do_cmd("ip a | grep 'scope global {}'".format(each_nic), 30, True).strip()
            if ip_info:
                ip = ip_info.split()[1].split('/')[0]
                _ip.append(ip)
        
        _ip_prefix = []
        for each_prefix in _ip:
            _ip_prefix.append('.'.join(each_prefix.split('.')[:-2]))

        dns_ip = config.dns_ip
        dns_ip_prefix = '.'.join(dns_ip.split('.')[:-2])
        if dns_ip_prefix not in _ip_prefix:
            print "         [ERROR]    DNS ip in config/autotest.config is not correct, " \
                   "should start with these segments : ({})\n".format(_ip_prefix)
            sys.exit(0)

    print "         [Success]  Use correct public interface and config dns ip correct in config/autotest.config\n"

    # Check local host IP should config in autotest.conf
    print "    1-13 [Check]    Local host IP should configed in config/autotest.config"

    ceph_conf = "/etc/ceph/ceph.conf"
    health = do_cmd("ceph health detail", 60, True).strip()
    if 'HEALTH_OK' in health and os.path.exists(ceph_conf):
        pub_ifce_info = do_cmd("cat {} | grep 'public interface'".format(ceph_conf), 15).strip()
        sto_ifce_info = do_cmd("cat {} | grep 'storage interface'".format(ceph_conf), 15).strip()
        pub_ifce = pub_ifce_info.split('=')[-1].strip()
        sto_ifce = sto_ifce_info.split('=')[-1].strip()

        if pub_ifce != public_iface or sto_ifce != storage_iface:
            print "         [ERROR]    Check public or storage interface failed, please check " \
                   "config/autotest.config. "
            print "                    Get public interface from ceph.conf is ({}), " \
                  "but in config/autotest.config is ({})".format(pub_ifce, public_iface)
            print "                    Get storage interface from ceph.conf is ({}), " \
                  "but in config/autotest.config is ({})\n".format(sto_ifce, storage_iface)
            sys.exit(0)
        else:
            print "         [Success]  Check public and storage interface success " \
                  "from config/autotest.config and ceph.conf"

        {% raw %}scope_pub_cmd = "ip a | grep 'scope global {}' | awk '{{print $2}}'".format(pub_ifce) {% endraw %}
        {% raw %}scope_sto_cmd = "ip a | grep 'scope global {}' | awk '{{print $2}}'".format(sto_ifce) {% endraw %}
        local_pub_ip_info = do_cmd(scope_pub_cmd, 15).strip()
        local_sto_ip_info = do_cmd(scope_sto_cmd, 15).strip()
        local_pub_ip = local_pub_ip_info.split('/')[0]
        local_sto_ip = local_sto_ip_info.split('/')[0]

        if local_pub_ip in all_public_ips and local_sto_ip in all_storage_ips:
            print "         [Success]  Cluster is Health OK, check public and storage " \
                  "IP address in config/autotest.config success\n"
        else:
            print "         [ERROR]    Local host ip is not in config/autotest.config " \
                  "of storage_ips or public_ips\n"
            sys.exit(0)
    else:
        local_ip = []
        {% raw %}local_ip_info = do_cmd("ip a | grep 'scope global' | awk '{{print $2}}'", 30).strip() {% endraw%}

        for each_ip in local_ip_info.split("\n"):
            local_ip.append(each_ip.split('/')[0])
        # List union
        public_ret_list = list((set(all_public_ips).union(set(local_ip))) ^ (set(all_public_ips) ^ set(local_ip)))
        storage_ret_list = list((set(all_storage_ips).union(set(local_ip))) ^ (set(all_storage_ips) ^ set(local_ip)))

        if len(public_ret_list) > 0 and len(storage_ret_list) > 0:
            print "         [Success]  Check public and storage IP address in config/autotest.config success\n"
        else:
            print "         [ERROR]    Local host ip is not in config/autotest.config of storage_ips or " \
                  "public_ips, please check config/autotest.config\n"
            sys.exit(0)

    # Check the node of cluster IP should not be as client
    print "    1-14 [Check]    Check the node of cluster IP should not be as client"

    client_ips_list = [config.white_list_ip, config.white_second_ip, config.black_list_ip]
    client_ip_union = list((set(client_ips_list).union(set(all_public_ips))) ^
                           (set(client_ips_list) ^ set(all_public_ips)))
    if len(client_ip_union) > 0:
        print "         [ERROR]    In config/autotest.config, at [CLIENTS], client IP should not " \
              "same as cluster nodes's IP\n"
        sys.exit(0)

    print "         [Success]  Check IP and interface success in config/autotest.config\n"

    # Check the client, should has /root/.ssh/id_dsa.pub, used for RRS SSH key
    id_dsa_pub = "/root/.ssh/id_dsa.pub"
    print "    1-15 [Check]    Client : ({}) should has file of ({})".format(client_ip, id_dsa_pub)

    ls_cmd = "ls -l {}".format(id_dsa_pub)
    remote_ls_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port,
                                                                     client_ip, ls_cmd)
    ls_dsa_pub_flag = do_cmd(remote_ls_cmd, 20, True).strip()
    if ls_dsa_pub_flag:
        print "         [Success]  Client : ({}) has file of ({})".format(client_ip, id_dsa_pub)

        # If client is a cluster of Virtual Storage node, which reset-node or create cluster for many
        # times(not refresh install OS), will has many old ssh key in /root/.ssh/authorized_keys
        expect_pub_files_list = ['/root/.ssh/id_dsa.pub', '/root/.ssh/id_ecdsa.pub', '/root/.ssh/id_rsa.pub']
        {% raw %}ls_pub_files = "ls -l /root/.ssh/id*.pub | awk '{{print $NF}}'" {% endraw %}
        cat_auth_keys_file = "cat /root/.ssh/authorized_keys"
        client_ls_pub_files = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port,
                                                                               client_ip, ls_pub_files)
        client_ls_auth_files = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port,
                                                                                client_ip, cat_auth_keys_file)
        # If client has file of /root/.ssh/authorized_keys, break
        client_auth_keys_res = do_cmd(client_ls_auth_files, 30, True).strip()
        # print "--------- client_auth_keys_res : ({})".format(client_auth_keys_res)
        if client_auth_keys_res:
            # A cluster node as client
            key_content_cmd = "ceph config-key get ssh_authorized_keys > /tmp/kv_key.txt"
            remote_key_content_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port,
                                                                                      client_ip, key_content_cmd)
            kv_store_res = do_cmd(remote_key_content_cmd, 30, True).strip()
            if kv_store_res:
                cat_id_rsa_pub = "cat /root/.ssh/id_rsa.pub > /tmp/ssh_keys.txt"
                cat_id_ecdsa_pub = "cat /root/.ssh/id_ecdsa.pub >> /tmp/ssh_keys.txt"
                cat_id_dsa_pub = "cat /root/.ssh/id_dsa.pub >> /tmp/ssh_keys.txt"
                mix_cmd = "{};{};{}".format(cat_id_rsa_pub, cat_id_ecdsa_pub, cat_id_dsa_pub)
                remote_echo_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port,
                                                                                   client_ip, mix_cmd)
                do_cmd(remote_echo_cmd, 30)
                diff_cmd = "diff /tmp/kv_key.txt /tmp/ssh_keys.txt"
                remote_diff_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port,
                                                                                   client_ip, diff_cmd)
                diff_res = do_cmd(remote_diff_cmd, 30).strip()
                if diff_res:
                    print "         [Action]   Need to change content of /root/.ssh/authorized_keys " \
                          "on client : ({})".format(client_ip)
                    put_kv_store = "ceph config-key put ssh_authorized_keys -i /tmp/ssh_keys.txt"
                    remote_put_kv_store = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port,
                                                                                           client_ip, put_kv_store)
                    do_cmd(remote_put_kv_store, 30)
            else:
                print "         [SKIP]     Cluster node as client, but no need to change content of " \
                      "/root/.ssh/authorized_keys "

            # Not a cluster node as client
            client_ls_pub_files_res = do_cmd(client_ls_pub_files, 30, True).strip()
            if client_ls_pub_files_res:
                pub_list = client_ls_pub_files_res.split('\n')
                pub_list.sort()
                # Like this : ['/root/.ssh/id_dsa.pub', '/root/.ssh/id_ecdsa.pub', '/root/.ssh/id_rsa.pub']
                if set(expect_pub_files_list).issubset(set(pub_list)) is False:
                    print "         [ERROR]    expect_pub_files_list : ({}) is not a subset of " \
                          "pub_list : ({})\n".format(expect_pub_files_list, pub_list)
                else:
                    # Check content of /root/.ssh/authorized_keys, if has many same host name, should change it
                    {% raw %}cat_auth_keys_cmd = "cat /root/.ssh/authorized_keys | awk '{{print $NF}}'" {% endraw %}
                    get_content_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port,
                                                                                       client_ip, cat_auth_keys_cmd)
                    auth_keys_res = do_cmd(get_content_cmd, 30).strip()
                    if len(auth_keys_res.split('\n')) - len(set(auth_keys_res.split('\n'))) > 2:
                        # authorized_keys has some old ssh keys, need to change it
                        print "         [Action]   Need to change content of /root/.ssh/authorized_keys " \
                              "on client : ({})".format(client_ip)
                        cat_id_rsa_pub = "cat /root/.ssh/id_rsa.pub > /tmp/ssh_keys.txt"
                        cat_id_ecdsa_pub = "cat /root/.ssh/id_ecdsa.pub >> /tmp/ssh_keys.txt"
                        cat_id_dsa_pub = "cat /root/.ssh/id_dsa.pub >> /tmp/ssh_keys.txt"
                        mix_cmd = "{};{};{}".format(cat_id_rsa_pub, cat_id_ecdsa_pub, cat_id_dsa_pub)
                        remote_echo_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port,
                                                                                           client_ip, mix_cmd)
                        do_cmd(remote_echo_cmd, 30)
                    else:
                        print "         [Success]  Correct content of /root/.ssh/authorized_keys " \
                              "on client : ({})\n".format(client_ip)
            else:
                print "         [SKIP]     Not a cluster node as client, but no need to change content of " \
                      "/root/.ssh/authorized_keys\n"
        else:
            print "         [Success]  Client : ({}) has no file of /root/.ssh/authorized_keys, " \
                  "do nothing\n".format(client_ip)
    else:
        print "         [WARN]     Client : ({}) has no file of ({}), now install " \
              "it".format(client_ip, id_dsa_pub)

        import pexpect
        gen_cmd = "ssh-keygen -t dsa"
        remote_gen_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd, port,
                                                                          client_ip, gen_cmd)
        process = pexpect.spawn(remote_gen_cmd)
        match_enter_file = process.expect("Enter file in which to save the key")
        if match_enter_file == 0:
            process.sendline('\n')
        else:
            print "         [ERROR]    Not match content of 'Enter file in which to save the key'\n"

        match_enter_passphrase = process.expect("Enter passphrase")
        if match_enter_passphrase == 0:
            process.sendline('\n')
        else:
            print "         [ERROR]    Not match content of 'Enter passphrase'\n"

        match_enter_passphrase_again = process.expect("Enter same passphrase again")
        if match_enter_passphrase_again == 0:
            process.sendline('\n')
        else:
            print "         [ERROR]    Not match content of 'Enter same passphrase again'\n"

        process.close()

        # ls_dsa_pub_flag = install_on_remote_check(remote_ls_cmd)
        ls_dsa_pub_flag = do_cmd(remote_ls_cmd, 20, True).strip()
        if not ls_dsa_pub_flag:
            print "         [ERROR]    Client : ({}) has no file of ({}), please run " \
                  "'ssh-keygen -t dsa' to generate it\n".format(client_ip, id_dsa_pub)
            sys.exit(0)
        else:
            print "         [Success]  Generate dsa key on client : ({}) success\n".format(client_ip)

    print "    1-16 [Check]    Check cluster public IP and client IP segment"
    pub_ip_prefix = '.'.join(config.public_ips.split()[0].split('.')[:-2])
    client_1st_ip_prefix = '.'.join(config.white_list_ip.split()[0].split('.')[:-2])
    client_2nd_ip_prefix = '.'.join(config.white_second_ip.split()[0].split('.')[:-2])
    client_black_ip_prefix = '.'.join(config.black_list_ip.split()[0].split('.')[:-2])

    if pub_ip_prefix == client_1st_ip_prefix == client_2nd_ip_prefix == client_black_ip_prefix:
        print "         [Success]  Client IP prefix : ({}) is same as cluster public " \
              "ips : ({})".format(config.white_list_ip, config.public_ips)
    else:
        if pub_ip_prefix != client_1st_ip_prefix:
            print "         [ERROR]    Client first client IP address segment : ({}) is not on the same network\n" \
                  "                    segment as the public IP : ({})\n".format(config.white_list_ip,
                                                                                 config.public_ips)
            sys.exit(0)

        if pub_ip_prefix != client_2nd_ip_prefix:
            print "         [ERROR]    The second client IP address segment : ({}) is not on the same network\n" \
                  "                    segment as the public IP : ({})\n".format(config.white_second_ip,
                                                                                 config.public_ips)
            sys.exit(0)

        if pub_ip_prefix != client_black_ip_prefix:
            print "         [ERROR]    Client black IP address segment : ({}) is not on the same network\n" \
                  "                    segment as the public IP : ({})\n".format(config.black_list_ip,
                                                                                 config.public_ips)
            sys.exit(0)


def unlink_unavailable_scsi_session():
    # Clean all of target nodes on client, it is necessary to check the file system to ensure client
    # does not try to re-establish the connection on future boot operations
    port = config.ssh_port
    client_ip = config.white_list_ip
    client_ip_passwd = config.white_ip_root_password

    white_second_ip = config.white_second_ip
    white_second_ip_root_password = config.white_second_ip_root_password
    black_list_ip = config.black_list_ip
    black_ip_root_password = config.black_ip_root_password

    # Use rm on first client, because this client is only used by pytest
    rm_iqn_cmd = "rm -rf /etc/iscsi/nodes/iqn*"
    remote_rm_iqn_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd,
                                                                         port, client_ip, rm_iqn_cmd)
    do_cmd(remote_rm_iqn_cmd, 60, True).strip()

    rm_tgt_cmd = "rm -rf /etc/iscsi/send_targets/*"
    remote_rm_tgt_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(client_ip_passwd,
                                                                         port, client_ip, rm_tgt_cmd)
    do_cmd(remote_rm_tgt_cmd, 60, True).strip()

    # Delete all of folder which name include pytest, then rm unavailable link file in send_targets
    {% raw %}ls_session_cmd = "iscsiadm -m session | grep pytest | sed 's/,1//g' | awk '{{print $3, $NF}}'" {% endraw %}
    rm_iqn_cmd = "rm -rf /etc/iscsi/nodes/iqn*pytest*"
    rm_tgt_cmd = "for f in $(find /etc/iscsi/send_targets/ -type l); do [ ! -e $f ] && rm -rf $f; done"

    remote_ls_2nd_session_cmd = 'sshpass -p {} ssh -p {} -l root {} "{}"'.format(white_second_ip_root_password,
                                                                                 port, white_second_ip, ls_session_cmd)
    remote_ls_3rd_session_cmd = 'sshpass -p {} ssh -p {} -l root {} "{}"'.format(black_ip_root_password,
                                                                                 port, black_list_ip, ls_session_cmd)

    session_res_2nd = do_cmd(remote_ls_2nd_session_cmd, 30, True).strip()
    if session_res_2nd:
        for each_session in session_res_2nd.split("\n"):
            each_session_list = each_session.split()
            logout_cmd = "iscsiadm -m node -T {} -p {} --logout".format(each_session_list[1], each_session_list[0])
            delete_cmd = "iscsiadm -m node -o delete -T {} -p {}".format(each_session_list[1], each_session_list[0])
            remote_logout_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(white_second_ip_root_password,
                                                                                 port, white_second_ip, logout_cmd)
            remote_delete_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(white_second_ip_root_password,
                                                                                 port, white_second_ip, delete_cmd)
            do_cmd(remote_logout_cmd, 30, True)
            do_cmd(remote_delete_cmd, 30, True)

    session_res_3rd = do_cmd(remote_ls_3rd_session_cmd, 30, True).strip()
    if session_res_3rd:
        for each_session in session_res_3rd.split("\n"):
            each_session_list = each_session.split()
            logout_cmd = "iscsiadm -m node -T {} -p {} --logout".format(each_session_list[1], each_session_list[0])
            delete_cmd = "iscsiadm -m node -o delete -T {} -p {}".format(each_session_list[1], each_session_list[0])
            remote_logout_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(black_ip_root_password,
                                                                                 port, black_list_ip, logout_cmd)
            remote_delete_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(black_ip_root_password,
                                                                                 port, black_list_ip, delete_cmd)
            do_cmd(remote_logout_cmd, 30, True)
            do_cmd(remote_delete_cmd, 30, True)

    remote_rm_2nd_iqn_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(white_second_ip_root_password,
                                                                             port, white_second_ip, rm_iqn_cmd)
    remote_rm_2nd_tgt_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(white_second_ip_root_password,
                                                                             port, white_second_ip, rm_tgt_cmd)
    remote_rm_3rd_iqn_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(black_ip_root_password, port,
                                                                             black_list_ip, rm_iqn_cmd)
    remote_rm_3rd_tgt_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(black_ip_root_password, port,
                                                                             black_list_ip, rm_tgt_cmd)

    do_cmd(remote_rm_2nd_iqn_cmd, 60, True).strip()
    do_cmd(remote_rm_2nd_tgt_cmd, 60, True).strip()
    do_cmd(remote_rm_3rd_iqn_cmd, 60, True).strip()
    do_cmd(remote_rm_3rd_tgt_cmd, 60, True).strip()


def check_dns_set():
    """  Check DNS setting in network  """
    print "[Step 2]  Check DNS setting in order to connect to WWW to install some packages"
    ping_res = do_cmd("ping www.baidu.com -c 1", 60, True).strip()

    if ping_res == "":
        print "\n    [ERROR]    Not set dns or dns is not work, please check network settings.\n"
        sys.exit(0)
    elif "icmp_seq=1" in ping_res:
        print "\n    [Success]  DNS works well\n"


def pre_check(cmd, version):
    """
    :param cmd, string, command line
    :param version, string, package version
    """
    try:
        expect_ver = do_cmd(cmd, 30, True).strip()
        if expect_ver != "":
            expect_ver = expect_ver.split()[2]

        return version == expect_ver
    except IndexError as ex:
        print "{}".format(str(ex))


def install_on_remote_check(cmd):
    """
    Check the remote has been install or not install the package, such as pv at client
    return True or False, True means has been install; False means not install
    :param cmd, string, a command line will run on remote server
    """
    res = os.popen(cmd)
    res_info = res.read()

    if len(res_info.split()) > 0:
        return True
    else:
        return False


def install_package():
    """  Install some python package for pytest  """
    python_pip_flag = pre_check("dpkg -l | grep python-pip", "1.0-1build1")
    python_configobj_flag = pre_check("dpkg -l | grep python-configobj", "4.7.2+ds-3build1")
    unzip_flag = pre_check("dpkg -l | grep unzip", "6.0-4ubuntu2.5")
    stress_flag = pre_check("dpkg -l | grep stress", "1.0.1-1ubuntu1")
    pytest_plugins = do_cmd("pytest --fixtures | grep -w plugins | head -n 1", 30, True)

    if os.path.exists("../python_3rd_lib"):
        current_path = os.getcwd()
        client_ip = config.white_list_ip
        passwd = config.white_ip_root_password
        port = config.ssh_port

        print "\n[Step 3]  Install packages ...\n"
        os.chdir("../python_3rd_lib")

        print "    3-1. Upgrade apt source "
        os.system("apt-get update")

        print "    3-2. Install unzip"
        if unzip_flag:
            print "         unzip has been installed, skip\n"
        else:
            os.system("dpkg -i unzip_6.0-4ubuntu2.5_amd64.deb")

        print "    3-3. Install and upgrade python-pip"
        # pylint needs setuptools version >12, so need install a high level version of setuptools
        if os.path.exists("/usr/local/lib/python2.7/dist-packages/setuptools-40.6.3-py2.7.egg"):
            print "         Has been installed setuptools-40.6.3, skip"
        else:
            os.system("unzip -o setuptools-40.6.3.zip; cd setuptools-40.6.3; python setup.py install")

        if python_pip_flag:
            print "         python-pip has been installed, skip\n"
        else:
            os.system("dpkg -i python-pip_1.0-1build1_all.deb")

        # os.system("pip install --upgrade pip")

        print "    3-4. Install python-configobj"
        if python_configobj_flag:
            print "         python-configobj has been installed, skip\n"
        else:
            os.system("dpkg -i python-configobj_4.7.2+ds-3build1_all.deb")

        print "    3-5. Install more-itertools"
        if os.path.exists("/usr/local/lib/python2.7/dist-packages/more_itertools-3.0.0-py2.7.egg"):
            print "         Has been installed more_itertools-3.0.0, skip\n"
        else:
            os.system("tar -zxvf more-itertools-3.0.0.tar.gz;"
                      "cd more-itertools-3.0.0/; "
                      "python setup.py install; cd ../")

        print "    3-6. Install zipp"
        if os.path.exists("/usr/local/lib/python2.7/dist-packages/zipp-1.0.0-py2.7.egg"):
            print "         Has been installed zipp, skip\n"
        else:
            os.system("tar -zxvf zipp-1.0.0.tar.gz; "
                      "cd zipp-1.0.0/; "
                      "python setup.py install; cd ../")

        print "    3-7. Install pytest"
        if os.path.exists("/usr/local/lib/python2.7/dist-packages/pytest-4.6.9-py2.7.egg/pytest.py"):
            print "         pytest has been installed, skip\n"
        else:
            # os.system("pip install -U pytest") for V8.0
            os.system("tar -zxvf pytest-4.6.9.tar.gz; "
                      "cd pytest-4.6.9/; "
                      "python setup.py install; cd ../")

        print "    3-8. Install pytest-progress"
        if os.path.exists("/usr/local/lib/python2.7/dist-packages/pytest_progress-1.2.1-py2.7.egg"):
            print "         Plugin of progress has been installed, skip\n"
        else:
            os.system("tar -zxvf pytest-progress-1.2.1.tar.gz; "
                      "cd pytest-progress-1.2.1/; "
                      "python setup.py install; cd ../")

        print "    3-9. Install syslog-tool"
        if os.path.exists("/usr/local/lib/python2.7/dist-packages/pytest_cov-2.8.1-py2.7.egg/pytest-cov.pth"):
            print "          Has been installed pytest-cov, skip\n"
        else: 
            os.system("tar -zxvf pytest-cov-2.8.1.tar.gz; "
                      "cd pytest-cov-2.8.1/; "
                      "python setup.py install; cd ../")

        print "    3-10. Install JDK"
        # Modify /etc/profile
        target_file = "/etc/profile"
        res = do_cmd("cat {} | grep JAVA_HOME".format(target_file), 20, True).strip()
        add_content = """
export JAVA_HOME=/opt/jdk1.8.0_161
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$CLASSPATH
export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
"""

        if os.path.exists("/opt/jdk1.8.0_161/release"):
            print "          Has been installed JDK, skip\n"

            if not res:
                append_write(target_file, add_content)
                os.system(". {}".format(target_file))
        else:
            os.system("tar -zxvf jdk-8u161-linux-x64.tar.gz -C /opt/")

            if not res:
                append_write(target_file, add_content)
                os.system(". {}".format(target_file))

        print "    3-11. Install allure_pytest"
        if os.path.exists("/usr/local/lib/python2.7/dist-packages/allure_pytest-2.8.11-py2.7.egg"):
            print "          Has been installed allure_pytest, skip\n"
        else:
            os.system("tar -xvf allure-pytest-2.8.11.tar; "
                      "cd allure-pytest-2.8.11/; "
                      "python setup.py install; cd ../")

        print "    3-12. Install allure_command"

        bashrc_file = "/root/.bashrc"
        allure_cmd_path = "/opt/allure-2.13.2/bin/allure"
        res = do_cmd("cat {} | grep allure".format(bashrc_file), 20, True).strip()
        add_content = "alias allure='{}'".format(allure_cmd_path)

        if os.path.exists(allure_cmd_path):
            print "          Has been installed allure_command, skip\n"

            if not res:
                append_write(bashrc_file, add_content)
                os.system(". {}".format(bashrc_file))
        else:
            os.system("unzip allure-commandline-2.13.2.zip -d /opt/")

            if not res:
                append_write(bashrc_file, add_content)
                os.system(". {}".format(bashrc_file))

        print "    3-13. Install pylint"
        if os.path.exists("/usr/local/lib/python2.7/dist-packages/pylint-1.7.6-py2.7.egg/pylint/epylint.py"):
            print "          pylint-1.7.6 has been installed, skip\n"
        else:
            os.system("tar -zxvf pylint-1.7.6.tar.gz; "
                      "cd pylint-1.7.6; "
                      "python setup.py install; cd ../")

        print "    3-14. Install pv at client : {}".format(client_ip)
        pv_cmd = "dpkg -l | grep -w pv"
        remote_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(passwd, port, client_ip, pv_cmd)
        # print remote_cmd
        pv_flag = install_on_remote_check(remote_cmd)
        if pv_flag:
            print "          PV has been installed on client {}, skip\n".format(client_ip)
        else:
            # Sync pv deb to remote
            sync_file_cmd = "scp pv_1.2.0-1_amd64.deb root@{}:/root/".format(client_ip)
            pexpect.run(sync_file_cmd, events={'yes': 'yes', 'password:': passwd + '\n'}, logfile=sys.stdout)

            # Install package on remote
            install_cmd = "dpkg -i /root/pv_1.2.0-1_amd64.deb"
            remote_install_cmd = "sshpass -p {} ssh -p {} -l root {} '{}'".format(passwd, port, client_ip, install_cmd)
            os.system(remote_install_cmd)

        print "    3-15. Remove old ssh key from /root/.ssh/known_hosts for client : {}\n".format(client_ip)
        do_cmd("ssh-keygen -f '/root/.ssh/known_hosts' -R {}".format(client_ip), 30, True)

        print "    3-16. Install stress"
        if stress_flag:
            print "          stress has been installed, skip\n"
        else:
            os.system("dpkg -i stress_1.0.1-1ubuntu1_amd64.deb ")

        print "    3-17. Install syslog-tool"
        do_cmd('cp -r syslog-tool /home/')
        do_cmd('cd /home/syslog-tool; make clean ; make')
        if os.path.exists("/home/syslog-tool/tsyslog.ko"):
            print "          syslog-tool install success\n"
        else:
            do_cmd('cd /home/syslog-tool; make clean ; make')

        print "    3-18. Install pytest-repeat"
        if os.path.exists("/usr/local/lib/python2.7/dist-packages/pytest_repeat-0.8.0-py2.7.egg"):
            print "          Has been installed pytest-repeat, skip\n"
        else:
            os.system("tar -zxvf pytest-repeat-0.8.0.tar.gz; "
                      "cd pytest-repeat-0.8.0/; "
                      "python setup.py install; cd ../")

        print "    3-19. Install pytest-timeout"
        if os.path.exists("/usr/local/lib/python2.7/dist-packages/pytest_timeout-1.3.4-py2.7.egg"):
            print "          Has been installed pytest-timeout, skip\n"
        else:
            os.system("tar -zxvf pytest-timeout-1.3.4.tar.gz; "
                      "cd pytest-timeout-1.3.4/; "
                      "python setup.py install; cd ../")

        print "    3-20. Install configparser"
        if os.path.exists("/usr/local/lib/python2.7/dist-packages/configparser-4.0.2-py2.7.egg"):
            print "          Has been installed configparser, skip\n"
        else:
            os.system("tar -zxvf configparser-4.0.2.tar.gz; "
                      "cd configparser-4.0.2/; "
                      "python setup.py install; cd ../")

        print "    3-21. Install pyparsing"
        if os.path.exists("/usr/local/lib/python2.7/dist-packages/pyparsing-2.4.6-py2.7.egg"):
            print "          Has been installed pyparsing, skip\n"
        else:
            os.system("tar -zxvf pyparsing-2.4.6.tar.gz; "
                      "cd pyparsing-2.4.6/; "
                      "python setup.py install; cd ../")

        print "    3-22. Install scandir"
        if os.path.exists("/usr/local/lib/python2.7/dist-packages/scandir-1.10.0-py2.7-linux-x86_64.egg"):
            print "          Has been installed scandir, skip\n"
        else:
            os.system("tar -zxvf scandir-1.10.0.tar.gz; "
                      "cd scandir-1.10.0/; "
                      "python setup.py install; cd ../")

        os.chdir(current_path)

    else:
        print "         [ERROR]    Path {} is not exists!".format("../python_3rd_lib")
        sys.exit(2)


def del_report_dir():
    """  Delete the report directory  """
    print "    5 [Check]    Check if the report directory is deleted\n"

    if os.path.exists("../report"):
        shutil.rmtree("../report")
        print "      [Success]  Delete report directory success"
    else:
        print "      [SKIP]     No need to delete report directory"

    mkdir_report_path()


def reboot_client_clean_session():
    print "[Step 6]  Restart client, and clean unavailable scsi session\n"

    client_ip = config.white_list_ip

    print "    6-1 [Check]    Power off then power on for client : {}\n".format(client_ip)
    # First, reboot client if it is a VM, then check network
    OSCheck().reboot_client_node()

    print "    6-2 [Check]    Check network of client : {}".format(client_ip)
    for i in xrange(30):
        ping_res = do_cmd("ping {} -c 5".format(client_ip), 60, True).strip()
        if ping_res:
            print "        [Success]  Client of ({}) works well\n".format(client_ip)
            break
        else:
            time.sleep(3)
    else:
        print "        [ERROR]    Client of ({}) is not work, please check network settings.\n".format(client_ip)
        sys.exit(0)

    print "    6-3 [Clean]    Delete all of iqn on client, make sure client will not try " \
          "to re-establish the discard connection\n"
    unlink_unavailable_scsi_session()


def check_cluser_has_san():
    """
    Cluster should has no iSCSI or FC LUN under Default Virtual Storage.
    Otherwise, assigning GW to VS will report "ASSIGN_GWGROUP_ERROR": 1402
    Caused many use cases to fail
    """
    print "    7-1 [Check]    Check SAN devices created on Default Virtual Storage"
    res = do_cmd("scstadmin --list_device", 60, True).strip()

    if 'tgt' in res or 'nulldev' in res:
        print "        [Warn]     Has been create SAN device in Default Virtual " \
              "Storage, now delete it/them!\n"
        from testcasebase.Virtual_Storage.iSCSI import SANManager
        SANManager().env_clean_san()
    else:
        print "        [Success]  SAN device has not been created in Default Virtual Storage.\n"


def check_cluster_health():
    """  pg is all active + clean  """
    print "    7-2 [Check]    Check all PG state"
    try:
        pg_stat = ClusterInfo().get_pg_stat()
        if pg_stat is True:
            print "        [Success]  ALL PG is active+clean.\n"
            return True
        else:
            print "        [ERROR]    All PG is not active+clean, will exit!\n"
            return False
    except RuntimeError:
        print "        [Warn]     ClusterManager failed: no monitors found, " \
              "maybe the cluster has not been created.\n"
        return False


def check_ctdb_status():
    """  Check ctdb status  """
    print "    7-3 [Check]    Check ctdb state"

    for i in xrange(10):
        ctdb_status_ok = do_cmd("ctdb status | grep OK | wc -l", 30, True).strip()
        ctdb_status_not_ok = do_cmd("ctdb status | grep pnn | grep -v OK | wc -l", 30, True).strip()

        if int(ctdb_status_ok) >= 3 and int(ctdb_status_not_ok) == 0:
            print "        [Success]  ctdb status is OK\n"
            break
        else:
            time.sleep(6)
    else:
        print "        [ERROR]    Ctdb is not OK, need more than 3 ctdbs with OK status, so exit!\n"
        sys.exit()


def restart_rgw():
    """
    In order to avoid rgw not starting, here to restart the rgw service of all nodes
    """
    print "    7-4 [Check]    Restart RGW service\n"
    all_nodes = ClusterInfo().get_all_nodes()
    for each_node in all_nodes:
        try:
            do_cmd('ssh {} {}'.format(each_node, config.restart_rgw), 30)
        except Exception as ex:
            do_cmd('ssh {} {}'.format(each_node, config.restart_rgw), 10, True)


def modify_apache_conf():
    """  Modify apache.conf to make session is available  """
    print "    7-5 [Check]    Check apache conf"

    all_nodes = ClusterManager().list_nodes()
    apache_conf = "/etc/apache2/apache2.conf"

    for each_node in all_nodes:
        {% raw %}res = do_cmd("ssh {} cat {} | grep -w KeepAlive | grep -v '#' | "
                     "awk '{{print $2}}'".format(each_node, apache_conf), 30).strip() {% endraw %}
        if res == "On":
            print "        [Action]   Start to modify ({}) on node ({}) to " \
                  "change KeepAlive to Off".format(apache_conf, each_node)
            do_cmd('ssh {} \"sed -i \'s/KeepAlive On/KeepAlive Off/\'\" {}'.format(each_node, apache_conf), 30)
            do_cmd("ssh {} {}".format(each_node, config.restart_apache))
        else:
            print "        [Success]  Has been changed KeepAlive from On to Off on node : ({})".format(each_node)


def modify_webpy_session():
    """  Modify /usr/lib/cgi-bin/ezs3/index.py, to change session from 1800 to 86400(24Hours)  """
    index_py = "/usr/lib/cgi-bin/ezs3/index.py"
    print "\n    7-6 [Check]    Check  session timeout in {}".format(index_py)

    if not os.path.exists(index_py):
        print "    [ERROR]    File of {} does not exist"
    else:
        all_nodes = ClusterManager().list_nodes()
        for each_node in all_nodes:
            {% raw %}res = do_cmd("ssh {} cat {} | grep web.config.session_parameters | "
                         " grep timeout | awk '{{print $NF}}'".format(each_node, index_py), 30).strip() {% endraw %}
            if res == '1800':
                print "        [Action]   Start to modify ({}) on node ({}) to " \
                  "change session from 1800 to 86400".format(index_py, each_node)
                do_cmd('ssh {} \"sed -i \'s/ = 1800/ = 86400/\'\" {}'.format(each_node, index_py), 30)
                do_cmd("ssh {} {}".format(each_node, config.restart_apache))
            else:
                print "        [Success]  Has been changed session from 1800 to 86400 " \
                      "on node : ({})".format(each_node)


def check_disk_nums():
    """  Check disk numbers, each vm has more than 6 disks  """
    print "    7-7 [Check]    Check disk nums"
    all_nodes_ip = ClusterInfo().get_all_nodes()
    for each_node in all_nodes_ip:
        disks = do_cmd("ssh {} lsscsi | grep -v INTEL | grep -v NVME | grep "
                       "disk | wc -l".format(each_node), 30, True).strip()
        if int(disks) < 6:
            print "        [ERROR]    Disk member on node : ({}) is not match automation test.".format(each_node)
            sys.exit()
        break
    else:
        print "        [Success]  Check disk numbers pass.\n"


def run_create_cluster():
    """  Create the cluster   """
    is_created_cluster = False
    is_config_cluster = False
    is_cluster_health = False

    res = do_cmd("ceph -s", 90, True).strip()
    if res == '':
        # Not create cluster
        is_created_cluster = False
        is_config_cluster = False
        is_cluster_health = False
    else:
        if 'fsmap' not in res or 'no osds' in res or "client io" not in res:
            # Create cluster, but not create OSD/MDS
            is_created_cluster = True
            is_config_cluster = False
            is_cluster_health = False
        elif 'stuck' in res or 'peering' in res or 'recovery' in res or 'osds are down' in res:
            is_created_cluster = True
            is_config_cluster = True
            is_cluster_health = False
        elif "client io" in res and 'fsmap' in res and 'up:active' in res and 'active+clean' in res:
            osd_stat = do_cmd("ceph -s | grep osdmap", 60, True).strip()
            osd_stat = osd_stat.split()
            all_osd = osd_stat[2]
            up_osd = osd_stat[4]
            in_osd = osd_stat[6]
            if int(all_osd) == int(up_osd) and int(up_osd) == int(in_osd):
                is_created_cluster = True
                is_config_cluster = True
                is_cluster_health = True
            else:
                is_created_cluster = True
                is_config_cluster = True
                is_cluster_health = False

    return is_created_cluster, is_config_cluster, is_cluster_health


def check_cluster_state():
    """  Check cluster status   """
    source_path = os.getcwd()
    report_path = mkdir_report_path()

    print "[Step 7]  Start checking that the cluster environment meets the " \
          "requirements for automation case execution\n"

    cluster_state = run_create_cluster()
    # print cluster_state[0], cluster_state[1], cluster_state[2]

    if cluster_state[0] is False:
        # Generate run time of start
        do_cmd("date '+%Y-%m-%d %H:%M:%S' > {}/time.txt".format(report_path), 60)

        print "    7-1 [Check]    Not create cluster. First, create cluster, " \
              "then create&enable OSD/MDS service.\n"
        create_cls_cmd = "PYTHONPATH=. py.test -v -s --cache-clear --full-trace --alluredir ../report/json " \
                         "{}/prepare/create_cluster/test_cluster_creation_wizard.py".format(source_path)
        # print "create_cls_cmd is : {}".format(create_cls_cmd)
        os.system(create_cls_cmd)

        enable_service_cmd = "PYTHONPATH=. py.test -v -s --cache-clear --full-trace --alluredir ../report/json " \
                         "{}/prepare/setup_cluster/test_config_cluster.py".format(source_path)
        # print "enable_service_cmd is : {}".format(enable_service_cmd)
        os.system(enable_service_cmd)

        cluster_flag = check_cluster_health()
        if cluster_flag:
            restart_rgw()
            modify_apache_conf()
            modify_webpy_session()

        cook_file = source_path + os.sep + "cookie.jar"
        if os.path.exists(cook_file):
            os.unlink(cook_file)

        # Check the cluster created result
        res = do_cmd("ceph -s", 60, True).strip()
        if not res:
            print "\n      [ERROR]    Create cluster failed, please to view log of " \
                  "pytest_autotest.log under report directory!!!\n"
            sys.exit()
    elif cluster_state[0] is True and cluster_state[1] is False:
        print "    7-1 [Check]    Not create&enable OSD/MDS service, now create&enable OSD/MDS\n"

        # Generate run time of start
        do_cmd("date '+%Y-%m-%d %H:%M:%S' > {}/time.txt".format(report_path), 60)

        enable_service_cmd = "PYTHONPATH=. py.test -v -s --cache-clear --full-trace --alluredir ../report/json " \
                             "{}/prepare/setup_cluster/test_config_cluster.py".format(source_path)
        # print "enable_service_cmd is : {}".format(enable_service_cmd)
        os.system(enable_service_cmd)
        cluster_flag = check_cluster_health()
        if cluster_flag:
            restart_rgw()
            modify_apache_conf()
            modify_webpy_session()
    elif cluster_state[0] is True and cluster_state[1] is True and cluster_state[2] is False:
        print "    7-1 [Check]    Cluster is not health, Skip to run test case, exit!"
        sys.exit()
    else:
        print "        [Success]  The current tested environment cluster is normal, and all test \n" \
              "                   cases are run directly.\n"

        # Generate  run time of start
        do_cmd("date '+%Y-%m-%d %H:%M:%S' > {}/time.txt".format(report_path), 60)

        check_cluser_has_san()
        cluster_flag = check_cluster_health()
        if cluster_flag:
            check_ctdb_status()
            # check_disk_nums()
            restart_rgw()
            modify_apache_conf()
            modify_webpy_session()


def run_part_or_all_test_case(part=False, case_file=None):
    """
    Running part or all of test case
    :param part, bool, True means to run all of test case
    :param case_file, string, some python file name of case, split by space, the base path is current path
    like "testcase/Function_Test/case_2_Accounts/test_account_ad.py Function_Test/
    case_3_Hosts/Roles/test_SAN_volume_cache.py"
    """
    # If setup cluster failed, no need to run all test case
    # Check cluster and ctdb health status
    cls_health = check_cluster_health()
    if cls_health is False:
        print "\n        [ERROR]    Cluster is not health, so no need to run all test case, exit!"
        sys.exit()
    check_ctdb_status()

    print "[Step 8]  Start to run test cases\n"

    source_path = os.getcwd()
    report_path = mkdir_report_path()

    skip_path = source_path + os.sep + "prepare"

    if not part:
        run_all_cmd = "PYTHONPATH=. py.test -v -s -m 'not migration' --cache-clear --full-trace " \
                      "--cov-report xml:../report/coverage.xml --cov=./ --cov-config .coveragerc --ignore={} " \
                      "--alluredir ../report/json {}".format(skip_path, source_path)

        print "    8-1 Start to run all of test case\n"
        os.system(run_all_cmd)
    else:
        run_part_cmd = "PYTHONPATH=. py.test -v -s --cache-clear --full-trace " \
                      "--cov-report xml:../report/coverage.xml --cov=./ --cov-config .coveragerc " \
                      "--alluredir ../report/json {}".format(case_file)

        print "    8-1 Start to run part of test case\n"
        os.system(run_part_cmd)

    # Move converage source file to report
    coverage_source = source_path + os.sep + ".coverage"
    if os.path.exists(coverage_source):
        do_cmd("mv {} {}/../report".format(coverage_source, source_path))

    # Generate pylint output
    print "    8-2 Start to Generate pylint output\n"

    try:
        do_cmd("pylint --rcfile={}/.pylintrc -f parseable -d I0011,R0801 "
               "{}/testcasebase* | tee {}/../report/pylint.out".format(source_path, source_path, source_path))
    except Exception as ex:
        print "      Generate pylint failed, backend return : ({})\n".format(str(ex))

    # Generate run time of end
    do_cmd("date '+%Y-%m-%d %H:%M:%S' >> {}/time.txt".format(report_path), 60)

    # Compress pytest_autotest.log
    pytest_log_path = "{}/pytest_autotest.log".format(report_path)
    new_name = "{}.gz".format(pytest_log_path)
    if os.path.exists(pytest_log_path):
        do_cmd("tar -zcvf {} {}".format(new_name, pytest_log_path), 60)
    else:
        print "      [ERROR]    No file of {}\n".format(pytest_log_path)

    # Compress html report, if the html is larger than 30M, send email failed
    # html_path = "{}/{}".format(report_path, report_name)
    # if os.path.exists(html_path):
    #     new_name = "{}.gz".format(report_name)
    #     do_cmd("tar -zcvf {}/{} {}".format(report_path, new_name, html_path), 60)
    # else:
    #     print "      [ERROR]    No html file of {}\n".format(html_path)

    # Generate environment.properties for allure
    report_path = get_report_path()
    time_file = report_path + os.sep + "time.txt"
    version_file = report_path + os.sep + "version.txt"
    env_file = report_path + os.sep + "json/environment.properties"

    host_ip = config.public_ips.split()[1]
    start_time = do_cmd("cat {} | head -n 1".format(time_file), 20, True).strip()
    end_time = do_cmd("tac {} | head -n 1".format(time_file), 20, True).strip()
    product_name = do_cmd("cat {}".format(version_file), 20, True).strip()

    write_content = """Host_IP : {}
Start_Time : {}
End_Time : {}
Product_Info : {}
""".format(host_ip, start_time, end_time, product_name)

    do_cmd("echo '{}' > {}".format(write_content, env_file), 30)

    # Generate allure html report
    # do_cmd(". ~/.bashrc;allure generate --clean ../report/json -o ../report/html")
    do_cmd(". /etc/profile;/opt/allure-2.13.2/bin/allure generate --clean ../report/json -o ../report/html")


def main():
    opts, args = getopt.getopt(sys.argv[1:], '-t', ['testcase='])
    for opt_name, opt_value in opts:
        if opt_name == '-t':
            part_flag = True
            break
    else:
        part_flag = False

    print '-' * 80
    run_node_check()

    print '-' * 80
    check_dns_set()

    print '-' * 80
    install_package()

    print '-' * 80
    del_report_dir()

    print '-' * 80
    reboot_client_clean_session()

    print '-' * 80
    check_cluster_state()

    print '-' * 80
    rm_sessions()
    get_test_product_version()
    run_part_or_all_test_case(part=part_flag, case_file=' '.join(args))

    print '-' * 80


if __name__ == "__main__":
    main()
```

# 与Jenkins结合

非本文重点，此处省略。

附带脚本

此脚本放在jenkins账号的email-templates目录下:

```
jenkins@ubuntu-16:~/email-templates$ pwd
/var/lib/jenkins/email-templates
jenkins@ubuntu-16:~/email-templates$ ls -l
total 20
-rw-rw-r-- 1 jenkins jenkins  5697 Mar 27 16:57 allure-report.groovy
-rw-rw-r-- 1 jenkins jenkins 10764 Jun 17  2019 email-template.groovy
jenkins@ubuntu-16:~/email-templates$
```

allure-report.groovy文件内容如下：

```
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<style type="text/css">
/*base css*/
    body
    {
      margin: 0px;
      padding: 15px;
    }

    body, td, th
    {
      font-family: "Lucida Grande", "Lucida Sans Unicode", Helvetica, Arial, Tahoma, sans-serif;
      font-size: 10pt;
    }

    th
    {
      text-align: left;
    }

    h1
    {
      margin-top: 0px;
    }
    a
    {
      color:#4a72af
    }
/*div styles*/

.status{background-color:<%= 
            build.result.toString() == "SUCCESS" ? 'green' : 'red' %>;font-size:28px;font-weight:bold;color:white;width:720px;height:52px;margin-bottom:18px;text-align:center;vertical-align:middle;border-collapse:collapse;background-repeat:no-repeat}
.status .info{color:white!important;text-shadow:0 -1px 0 rgba(0,0,0,0.3);font-size:32px;line-height:36px;padding:8px 0}
</style>
<body>
<div class="content round_border">
                <div class="status">
                        <p class="info">pytest automation build <%= build.result.toString().toLowerCase() %></p>
                </div>
                <!-- status -->
                        <table>
                                <tbody>
                                        <tr>
                                                <th>Project:</th>
                                                <td>${project.name}</td>
                                        </tr>
                                        <tr>
                                                <th>Build ${build.displayName}:</th>
                                                <td><a
                                                        href="${rooturl}${build.url}">${rooturl}${build.url}</a></td>
                                        </tr>
                                        <tr>
                                                <th>Product Version:</th>
                                                <td><%=build.environment['PRODUCT_VERSION']%></td>
                                        </tr>
                                        <tr>
                                                <th>Date of build:</th>
                                                <td>${it.timestampString}</td>
                                        </tr>
                                        <tr>
                                                <th>Build duration:</th>
                                                <td>${build.durationString}</td>
                                        </tr>
                                        <tr>
                                                <td colspan="2">&nbsp;</td>
                                        </tr>
                                </tbody>

                        </table>
                <!-- main -->
        <% def artifacts = build.artifacts
            if(artifacts != null && artifacts.size() > 0) { %>

                        <b>Build Artifacts:</b>
                        <ul>
            <%          artifacts.each() { f -> %>
                <li><a href="${rooturl}${build.url}artifact/${f}">${f}</a></li>
            <%          } %>
                        </ul>
        <% } %>
  <!-- artifacts -->

<% 
  lastAllureReportBuildAction = build.getAction(ru.yandex.qatools.allure.jenkins.AllureReportBuildAction.class)
  lastAllureBuildAction = build.getAction(ru.yandex.qatools.allure.jenkins.AllureBuildAction.class)

  if (lastAllureReportBuildAction) {
    allureResultsUrl = "${rooturl}${build.url}allure"
    allureLastBuildSuccessRate = String.format("%.2f", lastAllureReportBuildAction.getPassedCount() * 100f / lastAllureReportBuildAction.getTotalCount())
  }
%>

<%
pylintResultsUrl = "${rooturl}${build.url}violations"
coberturaResultsUrl = "${rooturl}${build.url}cobertura"
%>

<% if (lastAllureReportBuildAction) { %>
<h2>Allure Results</h2>
<table>
            <tbody>
                        <tr>
                            <th>Total Allure tests run:</th>
                            <td><a href="${allureResultsUrl}">${lastAllureReportBuildAction.getTotalCount()}</a></td>
                        </tr>
                        <tr>
                            <th><span style="color: #000000; background-color: #ffff00;">Failed:</span></th>
                            <td><span style="color: #000000; background-color: #ffff00;">${lastAllureReportBuildAction.getFailedCount()} </span></td>
                        </tr>
                        <tr>
                            <th><span style="color: #000000; background-color: #008000;">Passed:</span></th>
                            <td><span style="color: #000000; background-color: #008000;">${lastAllureReportBuildAction.getPassedCount()} </span></td>
                        </tr>
                        <tr>
                            <th><span style="color: #000000; background-color: #3366ff;">Skipped:</span></th>
                            <td><span style="color: #000000; background-color: #3366ff;">${lastAllureReportBuildAction.getSkipCount()} </span></td>
                        </tr>
                        <tr>
                            <th><span style="color: #000000; background-color: #ff0000;">Broken:</span></th>
                            <td><span style="color: #000000; background-color: #ff0000;">${lastAllureReportBuildAction.getBrokenCount()} </span></td>
                        </tr>
                        <tr>
                            <th>Success rate: </th>
                            <td>${allureLastBuildSuccessRate}%  </td>
                        </tr>

            </tbody>
</table>

<br>
<img lazymap="${allureResultsUrl}/graphMap" src="${allureResultsUrl}/graph" alt="Allure results trend"/>
</br>

<br>
<font size=4><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pylint history trend</b></font>
</br>
<br>
<img lazymap="${pylintResultsUrl}" src="${pylintResultsUrl}/graph" alt="pylint"/>
</br>

<br>
<font size=4><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Code Coverage history trend</b></font>
</br>
<br>
<img lazymap="${coberturaResultsUrl}/graphMap" src="${coberturaResultsUrl}/graph"/>
</br>
<% } %>                  
  <!-- content -->
  <!-- bottom message -->
</body>
```

说明：
    脚本内容中有一个PRODUCT_VERSION变量，通过‘Inject environment vairables’来定义。

<img class="shadow" src="/img/in-post/inject_env_variables.png" width="800">

上一张Jenkins运行后发email报告图吧:

<img class="shadow" src="/img/in-post/jenkins_allure.png" width="800">


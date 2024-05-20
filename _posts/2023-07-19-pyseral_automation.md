---
layout:     post
title:      "Windows下使用pyserial实现嵌入式产品串口自动化测试框架设计与开发"
subtitle:   "pyserial Embedded Automation Test Framework for Windows"
date:       2023-07-19
author:     "Gavin Wang"
catalog:    true
top: true
img: "/img/pytest/pytest-8.png"
summary: pytest基于pyserial模块做嵌入式产品串口功能自动化
password: Huawei123!
theme: flip
categories:
    - [Automation]
    - [pytest]
tags:
    - Automation
    - python
    - pytest
    - serial
---


# 概述

本文介绍如何基于 python + pytest + pyserial + allure，完成嵌入式产品自动化框架的设计与用例编写。


# 预期目标

* 有可视化报告输出，展示被测版本信息、串口ID，以及运行过程中日志，包括但不限制于串口的输入与输出信息
* 根据产测工具输入的命令行，解析串口输出数据，校验输出结果是否符合预期要求，如果满足要求，则判断此测试项测试通过；否则测试项测试失败
* 细化每一个测试程序的每一个测试项与测试子项，封装成独立函数，便于后期用例组合参数完成用例功能设计工作
* 支持指定用例或用例集合下测试用例的执行
* 支持指定用例执行次数，默认1次
* 先兼容一个产品，再逐步兼容其他产品，优先打磨框架



# 设计思路


理应画个设计思路与流程图的，比较懒，略了吧......



# 基础环境安装/部署


windows下安装python2.x系列，由于python lib有相互依赖关系，本文介绍python-2.7.13下部署pytest。

所需安装包信息，参考下文信息(不全，仅展示部分重要lib)。



## pytest相关基础包

```shell
allure-pytest-2.8.11
allure-python-commons-2.8.11
allure-commandline-2.13.2
configobj-4.7.2
coverage-5.1
func_timeout-4.3.5
pylint-1.7.6
pytest-4.6.11
pytest-progress-1.2.1
pytest-repeat-0.8.0
pytest-ordering-develop
```



安装成功后，显示如下信息，表明安装成功：

```shell
E:\automation\src>pytest --version
This is pytest version 4.6.11, imported from C:\Python27\lib\site-packages\pytest.pyc
setuptools registered plugins:
  pytest-cov-2.12.1 at C:\Python27\lib\site-packages\pytest_cov\plugin.py
  pytest-timeout-1.3.4 at C:\Python27\lib\site-packages\pytest_timeout-1.3.4-py2.7.egg\pytest_timeout.pyc
  pytest-ordering-0.6 at C:\Python27\lib\site-packages\pytest_ordering-0.6-py2.7.egg\pytest_ordering\__init__.pyc
  pytest-progress-1.2.1 at C:\Python27\lib\site-packages\pytest_progress-1.2.1-py2.7.egg\pytest_progress.pyc
  pytest-repeat-0.8.0 at C:\Python27\lib\site-packages\pytest_repeat-0.8.0-py2.7.egg\pytest_repeat.pyc
  allure-pytest-2.8.11 at C:\Python27\lib\site-packages\allure_pytest-2.8.11-py2.7.egg\allure_pytest\plugin.pyc

E:\automation\src>
```



## java相关安装包

```shell
jdk-8u171-windows-x64
```


安装好 JRE 后，配置 windows下 allure 环境变量信息，让 windows 的 dos 命令或 PowerShell 能够识别到allure命令。出现如下信息，说明 allure 始终正常：

<img class="shadow" src="/img/in-post/serial/allure_help.png" width="1200">



# 框架目录结构


## 整体目录结构介绍


```shell
 E:\automation 的目录

2023/07/19  10:31    <DIR>          .
2023/07/19  10:31    <DIR>          ..
2023/07/19  10:44    <DIR>          doc
2023/07/19  10:37    <DIR>          report
2023/07/19  10:36    <DIR>          src
               0 个文件              0 字节
               8 个目录 459,405,893,632 可用字节

E:\automation>
```


说明：

* doc 目录下存放一些介绍文档，包括但不限制于当前框架使用说明、用例编写规范说明、pytest 框架介绍等
* report 目录下存放生成的 allure 报告，主体内容以 json 格式存放，借助allure 生成可视化html报告
* src 目录存放源码，为框架核心内容



## report目录介绍

```shell
E:\automation\report>dir
 驱动器 E 中的卷没有标签。
 卷的序列号是 EE05-33CD

 E:\automation\report 的目录

2023/07/19  10:37    <DIR>          .
2023/07/19  10:37    <DIR>          ..
2023/07/19  10:36            31,765 coverage.xml
2023/07/19  10:37    <DIR>          html
2023/07/19  10:36    <DIR>          json
2023/07/19  10:31             4,842 pylint.out
2023/07/19  10:36             9,271 pytest_autotest.log
2023/07/19  10:31                13 version.txt
               4 个文件         45,891 字节
               4 个目录 459,405,893,632 可用字节

E:\automation\report>
```


说明：

* coverage.xml 为 当前测试用例代码覆盖率统计信息，供 CI/CD 解析使用
* html 目录为 allure 可视化报告
* json 目录为生成的 allure 原始报告数据
* pylint.out 文件为当前测试框架 python 代码相关规范、语法统计信息，供 CI/CD 解析使用
* pytest_autotest.log 文件为用例执行过程中记录的日志信息
* version.txt 文件记录被测版本信息，用于 allure 生成 html 测试报告展示版本信息使用



## src目录介绍



```shell
E:\automation\src>dir
 驱动器 E 中的卷没有标签。
 卷的序列号是 EE05-33CD

 E:\automation\src 的目录

2023/07/19  11:09    <DIR>          .
2023/07/19  11:09    <DIR>          ..
2023/06/25  16:37            17,584 .pylintrc
2023/06/25  16:37               579 clear_pyc.py
2023/07/19  11:09    <DIR>          common
2023/07/14  15:34    <DIR>          config
2023/06/25  16:37               806 conftest.py
2023/06/26  14:44               647 pytest.ini
2023/07/17  17:18             7,626 run.py
2023/07/19  11:09    <DIR>          testcase
2023/07/19  11:09    <DIR>          testcasebase
2023/06/25  16:37                 0 __init__.py
               7 个文件         47,722 字节
               6 个目录 459,405,946,880 可用字节

E:\automation\src>dir common
 驱动器 E 中的卷没有标签。
 卷的序列号是 EE05-33CD

 E:\automation\src\common 的目录

2023/07/19  11:09    <DIR>          .
2023/07/19  11:09    <DIR>          ..
2023/07/11  14:58               804 config.py
2023/06/25  16:37               711 path_util.py
2023/07/19  09:31             6,410 pyserial.py
2023/07/19  11:09    <DIR>          tools
2023/07/18  17:28             7,813 util.py
2023/06/25  16:37                 0 __init__.py
               5 个文件         15,738 字节
               3 个目录 459,405,946,880 可用字节

E:\automation\src>dir config
 驱动器 E 中的卷没有标签。
 卷的序列号是 EE05-33CD

 E:\automation\src\config 的目录

2023/07/14  15:34    <DIR>          .
2023/07/14  15:34    <DIR>          ..
2023/07/14  15:34               160 autotest.config
               1 个文件            160 字节
               2 个目录 459,405,946,880 可用字节

E:\automation\src>dir testcase
 驱动器 E 中的卷没有标签。
 卷的序列号是 EE05-33CD

 E:\automation\src\testcase 的目录

2023/07/19  11:09    <DIR>          .
2023/07/19  11:09    <DIR>          ..
2023/06/25  16:37               364 conftest.py
2023/07/19  10:25               980 test_01_comprehensive_test.py
2023/07/18  18:43                30 test_02_watch_dog.py
2023/07/19  10:26             1,468 test_03_electronic_disk.py
2023/06/25  16:37                 0 __init__.py
               7 个文件          4,393 字节
               2 个目录 459,405,946,880 可用字节

E:\automation\src>dir testcasebase
 驱动器 E 中的卷没有标签。
 卷的序列号是 EE05-33CD

 E:\automation\src\testcasebase 的目录

2023/07/19  11:09    <DIR>          .
2023/07/19  11:09    <DIR>          ..
2023/07/19  10:30             1,696 ComprehensiveTest.py
2023/07/19  10:28             5,722 ElectronicDisk.py
2023/07/19  10:24             2,552 ProductInit.py
2023/07/18  17:30               335 WatchDog.py
2023/06/25  16:37                 0 __init__.py
               5 个文件         10,305 字节
               2 个目录 459,405,946,880 可用字节

E:\automation\src>
```



说明：

* `common` 目录，存放公用基类
* `config` 目录，存放配置信息，诸如设置的串口信息，波特率等
* `run.py` 是程序主入口，支持根据传参执行全部用例与部分用例
* `testcase` 目录存放具体的测试用例
* `testcasebase` 目录存放各个功能的基类



# 框架核心内容


重点在pyserial串口操作上，以及各个功能点的基类中发送串口命令、解析串口命令、判断串口输出结果正确与否。



适配产品的 python serial 部分代码如下(最新的代码未放出，这里只抛砖引玉)：


```python
#!/usr/bin/env python
# -*- coding: GBK -*-

"""  pyserial operation  """

from __future__ import unicode_literals

import sys
import glob
import time
import serial
import logging

from config import GetConfig as config
from util import change_timestamp_to_time


class PySerial():
    def __init__(self, send_str="Send Test", receive="Send Test", timeout=3):
        # super(PySerial, self).__init__()
        self.port = config.port
        self.baudrate = config.baudrate
        self.send_str = send_str
        self.receive = receive
        self.timeout = timeout

    def serial_connect(self, check_loop_send=False):
        """
        Connect to the serial port
        :param check_loop_send， bool， True means send and receive message from COM1 to COM1 in recycle
        """
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            # Enlarge the buffer, default is 4096bytes, if the output which is larger than 4096bytes,
            # call read_all() only get 4096bytes content, max is 2147483647(but not works, so set it less)
            self.serial.set_buffer_size(rx_size=2147483600, tx_size=2147483600)

            if check_loop_send:
                self.check_device()
        except Exception as ex:
            logging.error("[ERROR]  Port: (%s), baud rate: (%s), timeout: (%s)", self.port,
                          self.baudrate, self.timeout)
            logging.error("[ERROR]  Connect to serial failed, backend return : (%s)", str(ex))
            sys.exit(1)

        return self.serial

    @staticmethod
    def list_serial_ports():
        """
        Lists serial port names
        :raises EnvironmentError:   On unsupported or unknown platforms
        :returns: A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
    
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
    
        return result

    def serial_alive(self):
        """   If port alive, return True, else return False   """
        port_status = False

        if self.serial.isOpen():
            port_status = True

        return port_status

    def check_device(self):
        """  Check the device  """
        write_len = self.serial.write(self.send_str.encode('GBK'))
        logging.debug("--   write_len: %s", write_len)
        time.sleep(0.5)
        byte_data = self.serial.read(write_len).decode('GBK')
        logging.debug("--  self.send_str : (%s)", self.send_str)
        logging.debug("--  byte_data : (%s)", byte_data)
        if byte_data != self.receive.encode('GBK'):
            raise ValueError("Check Device Failed:send_str: '{}' not equal to receive: '{}', "
                             "actually receive : '{}'".format(self.send_str, self.receive, byte_data))

    def send_command(self, cmd_str):
        """  Send command  """
        # Clean the input buffer, clean the return values
        self.serial.reset_input_buffer()

        logging.debug("--  [DEBUG]  Write command string : (%s)", cmd_str)
        self.serial.write((cmd_str + '\r\n').encode('GBK'))

    def read_serial_data(self, count=None, all_data=False, flush_flag=False):
        """  Read the data, count Unit is byte, default is 1 byte  """
        logging.debug('--  [DEBUG]  Read count : (%s), all_data : (%s)', count, all_data)

        if flush_flag:
            # Flush current serial cache, if clean cache, can call serial.readline() to get new data
            self.serial.flushInput()

        if all_data:
            return self.serial.read_all().decode('GBK')
        else:
            count = 1 if count is None else count
            return self.serial.read(count).decode('GBK')

    def read_last_line(self):
        """
        Read the last line of output of serial, if not match, return None
        """
        all_line = self.serial.read_all().decode('GBK')
        logging.debug("--  [DEBUG]  all_line : ({})".format(all_line))
        all_line_list = [x for x in all_line.split('\n') if x]
        if len(all_line_list):
            return all_line_list[-1]
        else:
            return

    def read_until_matched(self, key_words):
        """
        Get some info when read from serial until match some key words
        @return:
        """
        logging.debug("--  Get key words : (%s) from serial cache", key_words)

        matched = self.serial.read_until(key_words).decode('GBK')

        return matched

    def write_serial_output_to_file(self, file_name):
        """
        Write serial output into a file
        @param file_name: string, a file name which to record the serial output information
        """
        logging.debug('--  [DEBUG]  Write data into file : (%s)', file_name)

        while True:
            if self.serial.in_waiting > 0:  # If serial has data to read
                full_data = self.serial.readline().decode('GBK').strip()
                # split_data = full_data.splitlines()
                with open(file_name, 'a+') as f:
                    f.write(full_data)
            else:
                break

    def has_buffer(self):
        """
        Get serial buffer
        @return: True or False
        """
        logging.debug("--  [DEBUG]  ser.in_waiting : (%s)", self.serial.in_waiting)
        if self.serial.in_waiting > 0:
            buffer_size = self.serial.in_waiting
            logging.debug('--  [DEBUG]  buffer size : (%s)', buffer_size)
            time.sleep(15)
            current_buffer_size = self.serial.in_waiting
            logging.debug('--  [DEBUG]  current buffer size : (%s)', current_buffer_size)
            if buffer_size != current_buffer_size:
                return True
        else:
            logging.debug('--  [DEBUG]  Enter else, return False, has no serial buffer')
            return False

    def wait_serial_output(self):
        logging.info("[Action]  等待串口回显信息")
        time.sleep(5)

        for i in range(120):
            if self.has_buffer():
                logging.debug("--  [%d times] 有串口缓存信息，等待2秒钟", i+1)
                time.sleep(2)
            else:
                break

    def serial_close(self):
        """  Close serial connection  """
        self.serial.close()

```


# 用例编写基本规则要求


## 1. 能编写但需要延迟编写的用例，增加 raise SkipTest 


如果两个功能之间有依赖，某个功能尚未编码结束，先写了其中一个功能，另外一个功能需要先标记成skip状态，这样做的目的： 

* 意在提醒 skip 状态的用例要在将来被完成 
* 某些用例需要手工执行上下电动作，只能手工测试，需要增加skip



## 2. Base Class 里，禁止函数名称含有 test  

pytest 运行用例的时候，根据正则匹配测试用例，会匹配到含有 test 开头的函数，会认为这个函 数是一个测试用例，故而要避免此种情况的发生，如果一定要在基类里写test，可以使用单词 examination 代替。



## 3. test_xx.py 无逻辑内容


test_xxxx.py是用例集，此用例集里纯粹是函数的调用，无任何业务逻辑，业务逻辑全部在testcasebase里。


## 4. 测试用例名称携带编号  


用例需携带上 \__doc__，此信息为用例Title， 且以服务器上（如TestLink）记录的名称为准。

例如： 

``` test_143_same_daemon_different_signal ```

对应 TestLink 的用例为：

``` FC-143:Same daemon, different signal core file ```



## 5. 测试用例的\__doc__，不得含有中文字符  


例如： ``` FC-143:Same daemon，different signal core file ``` 这里的逗号，是中文符号，会导致用例报错。



## 6、避免测试用例之间存在依赖关系 


* 每个测试 suite 中的测试用例互相不依赖
* 测试 suite 中的用例，尽可能避免依赖关系，如 TestLink 中上一个用例是创建，下一个用例是删除，则合并这两个用例为一个自动化测试用例。 



## 7、日志记录对齐要求  


为了让记录的log内容看起来更对其，对于code中的日志记录，规则要求如下：

* 执行动作的记录，开头增加[Action]
* 检查动作的记录，开头增加[Check]
* 断言记录的 log，开头增加[ERROR]
* 操作成功的 log，开头增加[SUCCESS]
* 不需要检查点 的，开头增加[Skip]



具体要求如下： 

* [Prepare] 后面跟 2 个空格
* [Action] 后面跟 3 个空格
* [Start] 后面跟 4 个空格
* [Check] 后面跟 4 个空格
* [Success] 后面跟 2 个空格
* [Skip] 后面跟 5 个空格
* debug 级别的 log，内容前面跟 2 个-，之后 再加 2 个空格
* assert 中，[ERROR] 后面跟 2 个空格 



## 8、用例的执行顺序 


pytest用例执行顺序，根据 ASSII 进行排序，单个用例文件中则是以用例编写先后顺序执行。

在用例有关联情 况下，需要对用例名称增加数字编号，人为的干预用例执行顺序，比如 test_1_xxx, test_2_yyy；或者借助pytest-order plugin来约束住用例见关系。



## 9、代码规范要求


执行 pylint，确保检查结果分值等于10, e.g :

```pylint -r y common/pyserial.py --rcfile=.pylintrc```


<img class="shadow" src="/img/in-post/serial/run-pylint.png" width="1200">


MESSAGE_TYPE 有如下几种： 

(C) 惯例，违反了编码风格标准 

(R) 重构，写得非常糟糕的代码

(W) 警告，某些 Python 特定的问题

(E) 错误，很可能是代码中的错误

(F) 致命错误，阻止 Pylint 进一步运行的错误




## 10. 用例文件名称、用例中定义变量名称全局唯一 


对于测试用例中定义的变量，要保持全局唯一，当有用例出错时，可以根据这个名称，定位到是哪个用例产生了问题，因为具有唯一性，可以排除其他用例带来的干扰，尤其对于用例规模上千后，此笨方法会比较有效。

当有用例出错时，可以根据这个名称，定位到是哪个用例产生了问题，因为具有唯一性，可以排除其他用例带来的干扰。




# 用例编写


测试用例仅仅是逻辑的调用，组合各个函数，构造成一个完整的测试场景。

这里以电子盘测试为示例，参考如下：



```test_03_electronic_disk.py ``` 内容参考如下：



```python
#!/usr/bin/env python
# -*- coding: GBK -*-

"""  Check output of electronic disk test information  """

from __future__ import unicode_literals

import allure

from src.common.pyserial import PySerial
from src.testcasebase.ElectronicDisk import ElectronicDiskTest


class TestElectronicDiskTest(ElectronicDiskTest):
    """    Test case of electronic disk test   """
    serial = PySerial()

    def setup(self):
        with allure.step("连接到串口"):
            self.serial.connect()

    def teardown(self):
        with allure.step("关闭串口连接"):
            self.serial.close()

    def test_electronic_disk(self):
        with allure.step("输入 '1' 开始电子盘测试"):
            self.check_electronic_disk_test_menu()

    def test_filesystem_performance(self):
        with allure.step("电子盘测试 --> 1.电子盘文件系统读写性能测试"):
            self.data_storage_filesystem_read_write_performance_test()

    def test_emcc_performance(self):
        with allure.step("电子盘测试 --> 2.EMMC多任务读写测试"):
            self.emmc_multi_task_read_write_test()

    def test_data_encry_performance_test(self):
        with allure.step("电子盘测试 --> 3.电子盘文件系统数据加密解密性能测试"):
            self.data_encry_test()

    def test_folder_files_created_performance_test(self):
        with allure.step("电子盘测试 --> 4.电子盘文件夹与文件数创建性能测试"):
            self.folder_file_created_performance()
```



非常明显的看出来，这里没有逻辑，完全是具体函数的调用。对应测试项功能的发起、返回结果的校验，完全在被调用函数里，所以，框架的另外一个重心，就是各个功能点的基类函数。



# 用例执行


## 执行全部用例


src 目录下，执行 ```python run.py```, 如下所示：


```shell
E:\automation\src>python run.py
--------------------------------------------------------------------------------
[Step 1]  [Check]    Check if the report directory is deleted

          [SKIP]     No need to delete report directory
--------------------------------------------------------------------------------
[Step 2]  Check test case execution node.

    2-1 [Check]    Current node should install python, pyest

        [Success]  List some serial ports success

    2-2 [Check]    Should be able to access the serial ports

        [Success]  Access serial port : (COM7) success

--------------------------------------------------------------------------------
[Step 3]  Start to run test case

    3-1 Start to run all of test case

============================= test session starts =============================
platform win32 -- Python 2.7.13, pytest-4.6.11, py-1.11.0, pluggy-0.13.1 -- C:\Python27\python.exe
cachedir: .pytest_cache
rootdir: E:\automation\src, inifile: pytest.ini
plugins: cov-2.12.1, timeout-1.3.4, ordering-0.6, progress-1.2.1, repeat-0.8.0, allure-pytest-2.8.11
collected 11 items

testcase/test_01.py::test_a PASSED                                      [ 1/11]
_ 1 of 11 completed, 1 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _

testcase/test_01.py::test_b PASSED                                      [ 2/11]
_ 2 of 11 completed, 2 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _

testcase/test_01.py::TestFramework::test_eq PASSED                      [ 3/11]
_ 3 of 11 completed, 3 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _

testcase/test_01.py::TestFramework::test_not_eq PASSED                  [ 4/11]
_ 4 of 11 completed, 4 Pass, 0 Fail, 0 Skip, 0 XPass, 0 XFail, 0 Error, 0 ReRun _

testcase/test_01_comprehensive_test.py::TestComprehensiveTest::test_comprehensive

---------- coverage: platform win32, python 2.7.13-final-0 -----------
Coverage XML written to file ../report/coverage.xml
```


## 执行部分用例


执行 ```python run.py -t xxx yyy zzz```， 其中xxx yyy zzz表示不同的用例文件

```shell
E:\automation\src>python run.py -t testcase/test_01_comprehensive_test.py testcase/test_02_watch_dog.py
```


## 执行某个测试用例


方法1： run.py为入口

e.g:

```
python run.py -t testcase/test_01_comprehensive_test.py::TestComprehensiveTest::test_comprehensive
```


<img class="shadow" src="/img/in-post/serial/run_single_case_1.png" width="1200">



方法2： pytest命令行执行

e.g:

```shell
pytest --cov-report xml:../report/coverage.xml --cov=./ --cov-config .coveragerc --alluredir ../report/json testcase/test_01_comprehensive_test.py::TestComprehensiveTest::test_comprehensive
```


<img class="shadow" src="/img/in-post/serial/run_single_case_2.png" width="1200">





## 循环执行用例



用例执行有多种方式，一是指定整个py文件，而是指定到具体测试用例，无论哪种方式，携带上--count，示例如下：



### 某个用例循环多次执行



```shell
E:\automation\src>pytest --cov-report xml:../report/coverage.xml --cov=./ --cov-config .coveragerc --alluredir ../report/json testcase/test_01_comprehensive_test.py::TestComprehensiveTest::test_comprehensive --count=10
```


<img class="shadow" src="/img/in-post/serial/case_counts.png" width="1200">





### 某个测试集合下用例循环多次执行



```shell
E:\automation\src>pytest --cov-report xml:../report/coverage.xml --cov=./ --cov-config .coveragerc --alluredir ../report/json testcase/test_01.py --count=10
```


<img class="shadow" src="/img/in-post/serial/case_counts-2.png" width="1200">





# 测试报告



## HTML可视化报告的展示

run.py运行结束后，会在report目录下生成json目录与文件，执行allure相关命令，生成可视化 html 报告：



```shell
E:\automation>cd report
E:\automation\report>allure generate json -o html --clean
Report successfully generated to html
E:\automation\report>allure open html -p 11111
Starting web server...
2023-07-19 14:56:21.859:INFO::main: Logging initialized @183ms to org.eclipse.jetty.util.log.StdErrLog
Server started at <http://192.168.56.1:11111/>. Press <Ctrl+C> to exit
```



浏览器打开 ```http://192.168.56.1:11111```地址，预览如下：

<img class="shadow" src="/img/in-post/serial/allure_report.png" width="1200">


如果 allure 命令生成 report 时，未指定 -p 参数，会随机生成一个未被占用的5位数字的端口号：



```shell
E:\automation\report>allure open html
Starting web server...
2023-07-19 15:00:17.760:INFO::main: Logging initialized @180ms to org.eclipse.jetty.util.log.StdErrLog
Server started at <http://192.168.56.1:52014/>. Press <Ctrl+C> to exit
```



## 失败用例的检查


html可视化报告中给出哪些用例失败，可根据记录到的log信息进行用例失败检查，判断是产品存在Bug还是用例编写问题。





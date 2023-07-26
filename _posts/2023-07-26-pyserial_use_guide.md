---
layout:     post
title:      "pyserial 使用指导"
subtitle:   "pyserial use guide"
date:       2023-07-26
author:     "Gavin"
catalog:    true
tags:
    - python
    - serial
---


# 概述


利用pyserial，可以访问串口，发送串口命令，当然，根据串口返回结果，判断命令执行正确性。

本文简介pyserial一些常用函数的使用方法与场景，并做一些阐述。





# 实践


## 初始化(连接串口)


### 串口连接示例



```
>>> import serial
>>> ser = serial.Serial('COM7', 115200, timeout=1)
```



不同平台连接不同类型串口，示例如下：

```
ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5) # 使用USB连接串行口
ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5) # 使用树莓派的GPIO口连接串行口
ser = serial.Serial("com1", 9600, timeout=0.5)# winsows系统使用com1口连接串行口
ser = serial.Serial("/dev/ttyS1", 9600, timeout=0.5)# Linux系统使用com1口连接串行口
```



连接串口时，除了主要的几个参数显示携带外，其他参数可以使用默认值，当然，可以携带全部参数，示例如下：



当然， 可以在连接串口时，携带上全部参数：



```
ser = serial.Serial(
port=None,              # number of device, numbering starts at
# zero. if everything fails, the user
# can specify a device string, note
# that this isn't portable anymore
# if no port is specified an unconfigured
# an closed serial port object is created
baudrate=9600,          # baud rate
bytesize=EIGHTBITS,     # number of databits
parity=PARITY_NONE,     # enable parity checking
stopbits=STOPBITS_ONE,  # number of stopbits
timeout=None,           # set a timeout value, None for waiting forever
xonxoff=0,              # enable software flow control
rtscts=0,               # enable RTS/CTS flow control
interCharTimeout=None   # Inter-character timeout, None to disable
)
```





### **对象属性**

- name —— 设备名字
- port —— 读或者写端口，比如示例中的'COM7'，这里只接受字符串类型内容
- baudrate —— 波特率，比如示例中的115200，波特率端口，默认9600
- bytesize —— 字节大小
- parity —— 校验位
- stopbits —— 停止位，取值(1,2)
- timeout —— 读超时设置
- writeTimeout —— 写超时
- xonxoff —— 软件流控
- rtscts —— 硬件流控
- dsrdtr —— 硬件流控
- interCharTimeout —— 字符间隔超时



### 属性介绍



说明：

​    如未显示携带，pyserial设有默认值。



**name**

```
>>> print ser.name
COM7

```



**port**

```
>>> print ser.port
COM7
>>> print ser.portstr
COM7
>>>
```



**baudrate**

```
>>> print ser.baudrate
115200
>>>
```



**bytesize**

```
>>> print ser.bytesize
8
```



**parity**

```
>>> print ser.parity
N
```



**stopbits**

```
>>> print ser.stopbits
1
```



**timeout**

```
>>> print ser.timeout
None
```



关于timeout：

```
timeout=None            # wait forever
timeout=0               # non-blocking mode (return immediately on read)
timeout=x               # set timeout to x seconds (float allowed)
```





**writeTimeout**

```
>>> print ser.writeTimeout
None
```



**xonxoff**

```
>>> print ser.xonxoff
False
```



**rtscts**

```
>>> print ser.rtscts
False
```



**dsrdtr**

```
>>> print ser.dsrdtr
False
```



**interCharTimeout**

```
>>> print ser.interCharTimeout
None
>>>
```





**一个命令获取当前串口属性信息**：



```
>>> ser.getSettingsDict
<bound method Serial.getSettingsDict of Serial<id=0x2cc3358, open=True>(port='com7', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False)>
>>>
```







## 查看pyserial 属性信息



```
>>> import serial
>>> ser = serial.Serial('COM7', 115200)
>>> dir(ser)
['BAUDRATES', 'BYTESIZES', 'PARITIES', 'STOPBITS', '_GetCommModemStatus', '_SAVED_SETTINGS', '__abstractmethods__', '__class__', '__delattr__', '__doc__', '__enter__', '__exit__', '__format__', '__getattribute__', '__hash__', '__init__', '__iter__', '__metaclass__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_abc_cache', '_abc_negative_cache', '_abc_negative_cache_version', '_abc_registry', '_cancel_overlapped_io', '_checkClosed', '_checkReadable', '_checkSeekable', '_checkWritable', '_close', '_reconfigure_port', '_update_break_state', '_update_dtr_state', '_update_rts_state', 'applySettingsDict', 'apply_settings', 'baudrate', 'break_condition', 'bytesize', 'cancel_read', 'cancel_write', 'cd', 'close', 'closed', 'cts', 'dsr', 'dsrdtr', 'dtr', 'exclusive', 'fileno', 'flush', 'flushInput', 'flushOutput', 'getCD', 'getCTS', 'getDSR', 'getRI', 'getSettingsDict', 'get_settings', 'inWaiting', 'in_waiting', 'interCharTimeout', 'inter_byte_timeout', 'iread_until', 'isOpen', 'isatty', 'next', 'open', 'out_waiting', 'parity', 'port', 'read', 'read_all', 'read_until', 'readable', 'readall', 'readinto', 'readline', 'readlines', 'reset_input_buffer', 'reset_output_buffer', 'ri', 'rs485_mode', 'rts', 'rtscts', 'seek', 'seekable', 'sendBreak', 'send_break', 'setDTR', 'setPort', 'setRTS', 'set_buffer_size', 'set_output_flow_control', 'stopbits', 'tell', 'timeout', 'truncate', 'writable', 'write', 'writeTimeout', 'write_timeout', 'writelines', 'xonxoff']
>>>
```





**对象常用方法**

- ser.isOpen() —— 查看端口是否被打开
- ser.open() —— 打开端口
- ser.close() —— 关闭端口
- ser.read() —— 从端口读字节数据。默认1个字节
- ser.read_all() —— 从端口接收全部数据，默认4096字节
- ser.write("s") —— 向端口写数据 "s"
- ser.readline() —— 读一行数据
- ser.readlines() —— 读多行数据
- in_waiting —— 返回接收缓存中的字节数，方法同inWaiting()
- flush() —— 等待所有数据写出
- flushInput() —— 丢弃接收缓存中的所有数据
- flushOutput() —— 终止当前写操作，并丢弃发送缓存中的数据
- read_until("s") —— 读取串口数据，知道出现预期字符串"s"就终止读取
- set_buffer_size(rx_size=value1, tx_size=value2) —— 设置buffer 大小，默认4096bytes，上限2147483647
- sendBreak()   —— send break condition
- setRTS(level=1)  —— set RTS line to specified logic level
- setDTR(level=1) —— set DTR line to specified logic level
- getCTS()  —— return the state of the CTS line
- getDSR()  —— return the state of the DSR line
- getRI()  —— return the state of the RI line
- getCD() —— return the state of the CD line










# 常用代码示例



说明：

​      如下示例，借助虚拟串口软件（Virtual Serial Port Driver Pro）创建了两个虚拟串口（COM7 和 COM8），并将两个串口短接（即COM7与COM8互通，形成回环）



### 获取当前设备上所有串口信息



```
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
```





### 字符串的发送接收



```
import serial
ser = serial.Serial('COM7', 115200)
writen = ser.write('Hello, i send a string command to serial')
print writen
recevied = ser.read(writen )
print recevied
```



其中，read(value)方法的参数value为需要读取的字符长度：

* 如果指定了value的值，当且仅当串口 buffer内容长度小于value值时，read动作会一直等待，直到串口buffer >= value时，read结束。比如read(10)，而buffer内容长度超过10字节，则只读取前面10个字节内容。
* 如果想要全部读取，提供两个方法：

​     （1）inWaiting() 或者 in_waiting：监测接收字符。 inWaitting返回接收字符串的长度值，然后把这个值赋给read做参数。

​     （2）read_all() ：读取全部字符



说明:

​    inWaiting()或者in_wating，使用如下：

```
>>> ser.inWaiting()
36L
>>> ser.in_waiting
36L
>>>
```

如果有非零值，说明串口buffer中有内容可读。



​    read_all() 使用如下:

```
>>> ser.read_all()
'I received what you send, thanks.'
>>>
```



还有另外一个方法readall()，但是没有理解掉这个方法，使用readall()读取数据时，无论设置多大的buffer size，无论发送多大的数据包过去，命令始终卡着，无任何输出，即使携带上回车换行也没有效果。





### 十六进制显示

十六进制显示的实质是把接收到的字符串转换成其对应的ASCII码，然后将ASCII码值再转换成十六进制数显示出来，这样就可以显示特殊字符了。

在这里定义了一个函数，如hexShow(argv)，代码如下：



```
#!/usr/bin/env python
# -*- coding:UTF-8 -*

import serial


def hexShow(argv):
    result = ''
    hLen = len(argv)
    for i in xrange(hLen):
        hvol = ord(argv[i])
        hhex = '%02x'%hvol
        result += hhex+' '

    print 'hexShow:', result

ser = serial.Serial('COM8',9600)
str_input = raw_input('Enter some words:')
writen_str = ser.write(str_input)
print "--  writen_str : ({})".format(writen_str)

read_str = ser.read(writen_str)
print "--  read_str : ({})".format(read_str)

hexShow(read_str)

ser.close()
```



测试结果如下：

```
C:\Users\Administrator>python C:\Users\Administrator\Desktop\hexShow.py
Enter some words:hex shows test
--  writen_str : (14)
--  read_str : (hex shows test)
hexShow: 68 65 78 20 73 68 6f 77 73 20 74 65 73 74
```





### 十六进制发送



十六进制发送实质是发送十六进制格式的字符串，如'\xaa'，'\x0b'。重点在于怎么样把一个字符串转换成十六进制的格式，有两个误区：

1）'\x'+'aa'是不可以的，涉及到转义符反斜杠

2）'\x'+'aa'和r'\x'+'aa'也不可以的，这样的打印结果虽然是\xaa，但赋给变量的值却是'\xaa'



这里用到decode函数：



```
>>> s ='aabbccddee'
>>> s.decode('hex')
'\xaa\xbb\xcc\xdd\xee'
>>>
```



需要注意一点，如果字符串 s 的长度为奇数，则decode会报错：

```
>>> s ='aabbccdde'
>>> s.decode('hex')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python27\lib\encodings\hex_codec.py", line 42, in hex_decode
    output = binascii.a2b_hex(input)
TypeError: Odd-length string
>>>
```



可以按照实际情况，用字符串的切片操作，在字符串的开头或结尾加一个'0'。



假如在串口助手以十六进制发送字符串"abc"，那么你在python中则这样操作：

```serial.write(”\x61\x62\x63") ```



当然，还有另外一个方法也可以达到相同目的：

```
s = "abc"
strHex = binascii.b2a_hex(s)
# print strHex
strhex = strHex.decode("hex")
# print strhex
ser.write(strhex);
```





### 读取串口记录的最后一行



```
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
```





### 判断 buffer 是否有内容



```
    def has_buffer(self):
        """
        Get serial buffer
        @return: True or False
        """
        if self.serial.in_waiting > 0:
            buffer_size = self.serial.in_waiting
            time.sleep(5)
            current_buffer_size = self.serial.in_waiting
            if buffer_size != current_buffer_size:
                return True
        else:
            return False
```





### 读取串口内容并记录到文件



```
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
```





### 读取串口内容直到匹配到预期字符串



```
    def read_until_matched(self, key_words):
        """
        Get some info when read from serial until match some key words
        @return:
        """
        logging.debug("--  Get key words : (%s) from serial cache", key_words)

        matched = self.serial.read_until(key_words).decode('GBK')

        return matched
```



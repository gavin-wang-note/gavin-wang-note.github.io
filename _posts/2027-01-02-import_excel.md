---
title: Excel内容正确，为何还是无法导入
date: 2027-01-02 23:00:00
author: Gavin Wang
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 使用 libreOffice 修正 Excel sharedstrings.xml 内容
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---


# 概述

在产品自动化测试开发过程中，需要构造`Excel`数据，然后被产品解析、导入。
为了确保构造的`Excel`内容的准确性，先是手工在产品页面增加了一笔记录，然后导出，命名为`exported.lxsx`，然后使用`python`生成一个内容相同的`Excel`文件，人工对比了各项数据（`Excel`的表头、单元格合并、各行各列的内容），都是正确的，但是：
`python`构造的`Excel`文件导入时被产品无法正常解析数据。

但我发现另外一个现象：

将`python`构造的`Excel`文件，使用`Windows Office`或者`WPS`软件打开后再保存，此时的文件就可以被产品正常解析、导入。



# 原因分析

这是因为`Excel`是二进制文件，并不是纯文本文件，将产生导出的`exported.lxsx`解压，和使用`python`生成的具有内容相同的`Excel`文件解压，得到两个独立的解压后的文件夹，使用`Beyond Compare`工具对比解压后的文件中的各项内容，发现`sharedstrings.xml`的内容是有很大差异的，而`sharedstrings`是共享字符串的详细定义，一句话来说，共享字符串(`sharedStrings`)就是一个字符串表，将相同的字符串只存一份共享，来优化工作表的性能。

所以，本次碰到的问题，难点在于如何构造符合预期的`sharedstrings.xml`文件内容，而使用`Windows Office`或者`WPS`软件打开后再保存，`Windows Office`或者`WPS`软件帮我们生成了正确的`sharedstrings.xml`内容。

正常情况下，如果想生成一个`Excel`文件，是要构造二进制压缩包中的各个文件内容，然后压缩成`Excel`，这种操作难度显然超出了预期，那有没有其他方式帮我们解决此次碰到的问题呢？

答案是肯定的。

# 解决方法

既然使用`Windows Office`或者`WPS`软件打开后再保存后的`Excel`能够正常被产品解析，那来找找，是否有合适的三方库帮我们实现类似的操作。
通过一番查找，找到了`LibreOffice`，使用它帮我们转换一下`Excel`文件内容，即将`python`生成的`Excel`文件打开后再保存


## 示例代码

```python
import os
import subprocess

def open_and_save_excel(file_path, save_path):
    if os.name == "nt":  # Windows 平台
        import win32com.client
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        try:
            workbook = excel.Workbooks.Open(file_path)
            workbook.SaveAs(save_path)
            workbook.Close(SaveChanges=False)
        finally:
            excel.Quit()
    else:  # Linux 平台
        # 使用 unoconv 或 LibreOffice
        command = ["unoconv", "-f", "xlsx", "-o", save_path, file_path]
        subprocess.run(command, check=True)

# 使用示例
file_path = "/path/to/your/file.xlsx"
save_path = "/path/to/save/file.xlsx"
open_and_save_excel(file_path, save_path)
```

## windows和Linux平台的兼容

为了程序兼容`Windows`和`Linux`，需要分别针对这两个平台安装`libreOffice`，在代码使用上做细分区别，参考如下：

```python
# For windows
import win32com.client

def open_and_save_excel(file_path, save_path):
    # 启动 Excel 应用程序
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False  # 设置为不可见（后台运行）

    try:
        # 打开文件
        workbook = excel.Workbooks.Open(file_path)
        
        # 保存文件
        workbook.SaveAs(save_path)
        
        # 关闭文件
        workbook.Close(SaveChanges=False)
    finally:
        # 退出 Excel 应用程序
        excel.Quit()

# 使用示例
file_path = r"C:\path\to\your\file.xlsx"
save_path = r"C:\path\to\save\file.xlsx"
open_and_save_excel(file_path, save_path)



# For Linux

## 方法1
import subprocess

def open_and_save_excel(file_path, save_path):
    # 使用 unoconv 打开并保存文件
    command = ["unoconv", "-f", "xlsx", "-o", save_path, file_path]
    subprocess.run(command, check=True)

# 使用示例
file_path = "/path/to/your/file.xlsx"
save_path = "/path/to/save/file.xlsx"
open_and_save_excel(file_path, save_path)


## 方法2
import subprocess

def open_and_save_excel(file_path, save_path):
    # 使用 LibreOffice 打开并保存文件
    command = [
        "soffice", "--headless", "--convert-to", "xlsx",
        "--outdir", "/path/to/save", file_path
    ]
    subprocess.run(command, check=True)

# 使用示例
file_path = "/path/to/your/file.xlsx"
save_path = "/path/to/save/file.xlsx"
open_and_save_excel(file_path, save_path)
```

当然，实际使用时，需要将上面代码合并成一个`function`，对于Linux，是使用`unoconv`（需要安装`unoconv`）还是`soffice`（安装`libreOffice`）。


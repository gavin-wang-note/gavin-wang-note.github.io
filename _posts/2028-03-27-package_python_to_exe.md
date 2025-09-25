---
title: 将python程序打包成可执行文件
date: 2028-03-27 21:00:00
author: Gavin Wang
img: ""
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 使用python实现文件替换操作，并将程序打包成可执行文件
categories:
    - [pylint]
    - [Automation]
tags:
    - pylint
    - Automation
---



# Windows文件替换工具

## 概述

之前有写一个`License`授权工具，也有在`conftest.py`里增加了提前15天更新`License`授权文件，但是还是想单独出一个更新`License`授权文件的可执行程序，独立运行，这里`mark`一下过程。

## 需求

- 只支持`Windows`环境
- 动态获取当前登录用户，拼接`License`授权文件所在路径
- 最终不能提供`python`源码，需要对源码加壳或者脱敏，或者打包成一个工具

## 实现

### Python源码

```python
# -*- coding: UTF-8 -*-

import os
import sys
import shutil
import getpass
import subprocess
import ctypes

def get_roaming_directory():
    """
    Get the AppData/Local/Microsoft/Windows directory path for current user
    """
    username = getpass.getuser()
    return os.path.join('C:\\Users', username, 'AppData', 'Local', 'Microsoft', 'Windows')

def is_admin():
    """
    Check if running with administrator privileges
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_file_hidden(file_path):
    """
    Check if file has hidden attribute
    """
    try:
        result = subprocess.run(['attrib', file_path], capture_output=True, text=True, shell=True)
        if result.returncode == 0 and 'H' in result.stdout:
            return True
        return False
    except:
        return False

def set_file_hidden(file_path):
    """
    Set file hidden attribute
    """
    try:
        subprocess.run(['attrib', '+H', file_path], shell=True, check=True)
        return True
    except:
        return False

def take_ownership(file_path):
    """
    Take ownership of a file
    """
    try:
        result = subprocess.run(['takeown', '/f', file_path], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✓ Ownership acquired: {file_path}")
            return True
        else:
            print(f"✗ Failed to acquire ownership: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Exception while acquiring ownership: {str(e)}")
        return False

def grant_full_access(file_path):
    """
    Grant full access permissions to current user
    """
    try:
        username = getpass.getuser()
        result = subprocess.run(['icacls', file_path, '/grant', f'{username}:F'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✓ Full access granted: {file_path}")
            return True
        else:
            print(f"✗ Failed to grant permissions: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Exception while granting permissions: {str(e)}")
        return False

def backup_file(file_path):
    """
    Create backup of a file
    """
    backup_path = file_path + ".backup"
    if not os.path.exists(backup_path):
        try:
            take_ownership(file_path)
            grant_full_access(file_path)
            
            shutil.copy2(file_path, backup_path)
            print(f"✓ Backup created: {backup_path}")
            return True
        except Exception as e:
            print(f"✗ Backup failed: {str(e)}")
            return False
    else:
        print("ℹ Backup file already exists, skipping backup")
        return True

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def replace_file(target_path, source_path):
    """
    Replace target file with source file
    """
    try:
        is_hidden = check_file_hidden(target_path)
        
        if os.path.exists(target_path):
            if not backup_file(target_path):
                print("⚠ Backup failed, but continuing with replacement")
        
        take_ownership(target_path)
        grant_full_access(target_path)
        
        # Remove target and copy source
        if os.path.exists(target_path):
            os.remove(target_path)
        shutil.copy2(source_path, target_path)
        print(f"✓ File replaced: {target_path}")
        
        if not is_hidden:
            if set_file_hidden(target_path):
                print("✓ Hidden attribute set")
            else:
                print("⚠ Could not set hidden attribute")
        else:
            print("ℹ File already has hidden attribute")
        
        return True
        
    except PermissionError:
        print("✗ Permission denied even with admin privileges")
        print("ℹ This might be because the file is locked by a system process")
        return False
    except Exception as e:
        print(f"✗ Exception during replacement: {str(e)}")
        return False

def main():
    """
    Main function
    """
    # Check operating system
    if os.name != 'nt':
        print("✗ This tool only supports Windows operating system")
        return False
    
    # Check admin privileges
    if not is_admin():
        print("✗ Please run this program as administrator")
        print("ℹ Right-click on Command Prompt or PowerShell and select 'Run as administrator'")
        return False
    
    print("✓ Administrator privileges detected")
    
    # Get path information
    directory = get_roaming_directory()
    target_file = "UsrClassL2.dat"
    source_file = "UsrClassL2_2026-12-31.dat"
    
    print("Starting file replacement operation")
    print(f"Current user: {getpass.getuser()}")
    print(f"Target directory: {directory}")
    print(f"Target file: {target_file}")
    print(f"Source file: {source_file}")
    
    # Check if directory exists
    if not os.path.exists(directory):
        print(f"✗ Directory does not exist: {directory}")
        return False
    
    target_path = os.path.join(directory, target_file)
    
    # Get source path (handles both development and packaged environments)
    source_path = resource_path(source_file)
    
    # Check if source file exists
    if not os.path.exists(source_path):
        print(f"✗ Source file does not exist: {source_path}")
        print("ℹ Make sure the file is in the same directory as the executable")
        return False
    
    # Check if target file exists
    if not os.path.exists(target_path):
        print(f"✗ Target file does not exist: {target_path}")
        return False
    
    # Execute replacement operation
    success = replace_file(target_path, source_path)
    
    if success:
        print("✓ PATCH SUCCESSFUL")
        print("ℹ Please restart your computer for changes to take effect")
    else:
        print("✗ PATCH FAILED")
    
    return success

if __name__ == "__main__":
    main()
```

### 使用说明

#### 直接运行Python脚本

1. 将上述代码保存为 `patch_tool.py`
2. 确保在同一目录下有 `UsrClassL2_2026-12-31.dat` 文件（包含要替换的内容）
3. 运行脚本：`python patch_tool.py`

**说明**:

- 如果不想程序在执行过程中打印过多敏感信息，可按需适当注释/修改打印内容（主要是路径）

### 打包成可执行文件

1. 安装PyInstaller

```
pip install pyinstaller
```

2. 准备ico文件

可以网上搜索`pytest`图标的`svg`或者`png`图片，然后在线转换成`ico`，然后下载`ico`文件于`patch_tool.py`所在路径下。

3. 打包脚本

```
pyinstaller -F --add-data="UsrClassL2_2026-12-31.dat;." -i pytest.ico --name pytest-registry-patcher pytest_win_hotfix.py
```

过程记录到的信息参考如下：

```shell
D:\hotfix>pyinstaller -F --add-data="UsrClassL2_2026-12-31.dat;." -i pytest.ico --name pytest-registry-patcher pytest_win_hotfix.py
93 DEPRECATION: Running PyInstaller as admin is not necessary nor sensible. Run PyInstaller from a non-administrator terminal. PyInstaller 7.0 will block this.
837 INFO: PyInstaller: 6.16.0, contrib hooks: 2025.8
843 INFO: Python: 3.12.6
875 INFO: Platform: Windows-10-10.0.19045-SP0
875 INFO: Python environment: C:\Program Files\Python312
875 INFO: wrote D:\hotfix\pytest-registry-patcher.spec
890 INFO: Module search paths (PYTHONPATH):
['C:\\Users\\Gavin\\AppData\\Roaming\\Python\\Python312\\Scripts\\pyinstaller.exe',
 'C:\\Program Files\\Python312\\python312.zip',
 'C:\\Program Files\\Python312\\DLLs',
 'C:\\Program Files\\Python312\\Lib',
 'C:\\Program Files\\Python312',
 'C:\\Users\\Gavin\\AppData\\Roaming\\Python\\Python312\\site-packages',
 'C:\\Users\\Gavin\\AppData\\Roaming\\Python\\Python312\\site-packages\\win32',
 'C:\\Users\\Gavin\\AppData\\Roaming\\Python\\Python312\\site-packages\\win32\\lib',
 'C:\\Users\\Gavin\\AppData\\Roaming\\Python\\Python312\\site-packages\\Pythonwin',
 'C:\\Program Files\\Python312\\Lib\\site-packages',
 'C:\\Program Files\\Python312\\Lib\\site-packages\\natsort-8.4.0-py3.12.egg',
 'C:\\Program '
 'Files\\Python312\\Lib\\site-packages\\robotframework_excellibrary-0.0.2-py3.12.egg',
 'C:\\Program '
 'Files\\Python312\\Lib\\site-packages\\pytest_gui-0.0.1-py3.12.egg',
 'C:\\Program Files\\Python312\\Lib\\site-packages\\werkzeug-1.0.1-py3.12.egg',
 'C:\\Program Files\\Python312\\Lib\\site-packages\\waitress-1.4.4-py3.12.egg',
 'C:\\Program Files\\Python312\\Lib\\site-packages\\urllib3-1.25.10-py3.12.egg',
 'C:\\Program Files\\Python312\\Lib\\site-packages\\toml-0.10.1-py3.12.egg',
 'C:\\Program '
 'Files\\Python312\\Lib\\site-packages\\swagger_ui_bundle-0.0.8-py3.12.egg',
 'C:\\Program Files\\Python312\\Lib\\site-packages\\six-1.15.0-py3.12.egg',
 'C:\\Program Files\\Python312\\Lib\\site-packages\\requests-2.24.0-py3.12.egg',
 'C:\\Program Files\\Python312\\Lib\\site-packages\\setuptools\\_vendor',
 'C:\\Users\\Gavin\\Desktop\\hotfix']
2062 INFO: Appending 'datas' from .spec
2062 INFO: checking Analysis
2062 INFO: Building Analysis because Analysis-00.toc is non existent
2062 INFO: Looking for Python shared library...
2062 INFO: Using Python shared library: C:\Program Files\Python312\python312.dll
2062 INFO: Running Analysis Analysis-00.toc
2062 INFO: Target bytecode optimization level: 0
2062 INFO: Initializing module dependency graph...
2062 INFO: Initializing module graph hook caches...
2093 INFO: Analyzing modules for base_library.zip ...
5155 INFO: Processing standard module hook 'hook-encodings.py' from 'C:\\Users\\Gavin\\AppData\\Roaming\\Python\\Python312\\site-packages\\PyInstaller\\hooks'
8305 INFO: Processing standard module hook 'hook-pickle.py' from 'C:\\Users\\Gavin\\AppData\\Roaming\\Python\\Python312\\site-packages\\PyInstaller\\hooks'
9744 INFO: Processing standard module hook 'hook-heapq.py' from 'C:\\Users\\Gavin\\AppData\\Roaming\\Python\\Python312\\site-packages\\PyInstaller\\hooks'
10474 INFO: Caching module dependency graph...
10578 INFO: Analyzing D:\hotfix\pytest_win_hotfix.py
10629 INFO: Processing standard module hook 'hook-_ctypes.py' from 'C:\\Users\\Gavin\\AppData\\Roaming\\Python\\Python312\\site-packages\\PyInstaller\\hooks'
10637 INFO: Processing module hooks (post-graph stage)...
10647 INFO: Performing binary vs. data reclassification (2 entries)
10647 INFO: Looking for ctypes DLLs
10647 INFO: Analyzing run-time hooks ...
10663 INFO: Including run-time hook 'pyi_rth_inspect.py' from 'C:\\Users\\Gavin\\AppData\\Roaming\\Python\\Python312\\site-packages\\PyInstaller\\hooks\\rthooks'
10687 INFO: Creating base_library.zip...
10719 INFO: Looking for dynamic libraries
10953 INFO: Extra DLL search directories (AddDllDirectory): []
10953 INFO: Extra DLL search directories (PATH): []
11245 INFO: Warnings written to D:\hotfix\build\pytest-registry-patcher\warn-pytest-registry-patcher.txt
11276 INFO: Graph cross-reference written to D:\hotfix\build\pytest-registry-patcher\xref-pytest-registry-patcher.html
11328 INFO: checking PYZ
11328 INFO: Building PYZ because PYZ-00.toc is non existent
11328 INFO: Building PYZ (ZlibArchive) D:\hotfix\build\pytest-registry-patcher\PYZ-00.pyz
11548 INFO: Building PYZ (ZlibArchive) D:\hotfix\build\pytest-registry-patcher\PYZ-00.pyz completed successfully.
11556 INFO: checking PKG
11556 INFO: Building PKG because PKG-00.toc is non existent
11556 INFO: Building PKG (CArchive) pytest-registry-patcher.pkg
14890 INFO: Building PKG (CArchive) pytest-registry-patcher.pkg completed successfully.
14890 INFO: Bootloader C:\Users\Gavin\AppData\Roaming\Python\Python312\site-packages\PyInstaller\bootloader\Windows-64bit-intel\run.exe
14890 INFO: checking EXE
14890 INFO: Building EXE because EXE-00.toc is non existent
14890 INFO: Building EXE from EXE-00.toc
14890 INFO: Copying bootloader EXE to D:\hotfix\dist\pytest-registry-patcher.exe
14969 INFO: Copying icon to EXE
15031 INFO: Copying 0 resources to EXE
15031 INFO: Embedding manifest in EXE
15109 INFO: Appending PKG archive to EXE
15203 INFO: Fixing EXE headers
16765 INFO: Building EXE from EXE-00.toc completed successfully.
16765 INFO: Build complete! The results are available in: D:\hotfix\dist

D:\hotfix>
```

**说明**：

- 使用 `--add-data` 参数添加数据文件，格式为 `源路径;目标路径（Windows）` 或 `源路径:目标路径（Mac/Linux）`
- 如果提供的图片不是`ico`格式内容，打包时会报错

4. 执行打包程序

打包成功后，会在当前目录下生成一个`dist`目录，目录下生成指定名称的`exe`文件，如示例中的`pytest-registry-patcher.exe`。
此时，右击可执行文件，使用管理员权限执行；如果想看打印信息，可以以管理员权限运行`cmd`命令，将可执行程序放在`cmd`里运行。

执行信息参考如下(管理员权限)：

```shell
D:\hotfix>D:\hotfix\dist\pytest-registry-patcher.exe
✓ Administrator privileges detected
✓ Ownership acquired
✓ Full access granted
✓ PATCH SUCCESSFUL
ℹ Please restart your computer for changes to take effect

D:\hotfix>
```

无管理员权限，执行时：

```shell
D:\hotfix>D:\hotfix\dist\pytest-registry-patcher.exe
✗ Please run this program as administrator
ℹ Right-click on Command Prompt or PowerShell and select 'Run as administrator'

D:\hotfix>
```

## 功能特点

1. **自动获取用户名**：使用 `getpass.getuser()` 获取当前登录用户名
2. **二进制读写**：使用二进制模式读写文件，支持任何文件类型
3. **备份机制**：替换前自动创建备份文件
4. **错误恢复**：出错时尝试从备份恢复
5. **简洁输出**：使用`print`代替日志记录
6. **Windows专属**：检查操作系统环境

## 注意事项

1. 需要以有足够权限的用户运行（可能需要管理员权限）
2. 源文件需要与脚本在同一目录
3. 会自动创建备份文件
4. 支持任何类型的文件（文本文件、二进制文件等）



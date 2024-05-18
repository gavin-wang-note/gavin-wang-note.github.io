---
title: 透过adb获取Andriod APP CRASH 时日志信息
date: 2024-05-01 17:12:37
author: Gavin Wang
img: "/img/Linux/android.jpg"
top: false
hide: false
cover: false
coverImg:
password:
toc: true
mathjax: false
summary: 获取APP CRASH日志信息
categories:
    - [python]
    - [adb]
tags:
    - python
    - adb
---

# 概述

以前写个一个类似的脚本，此次在python3下作了调整，支持内嵌adb monkey命令，即自动执行adb monkey命令情况下，自动收集手机log信息。

# Code

代码示例参考如下：

```python
import os
import re
import sys
import time
import platform
import subprocess


class AppLog:
    '''运行Monkey，并获取Android设备日志'''
    subprocesses = []  # 初始化存储子进程的列表

    def run_adb_monkey(self, package_name, round_count, log_file_path):
        """在后台运行 adb monkey 测试"""
        monkey_command = [
            'adb', 'shell', 'monkey', '-p', package_name, '-v', 
            '--throttle', '500', str(round_count)
        ]

        with open(log_file_path, 'a') as log_file:
            complete_process = subprocess.run(
                monkey_command, 
                stdout=log_file, stderr=log_file, text=True, check=False
            )
        return complete_process

    @staticmethod
    def os_type():
        """获取操作系统类型"""
        return platform.system().lower()

    @staticmethod
    def get_log_file_path(log_name='test_logcat.txt'):
        """定义日志文件路径"""
        return os.path.abspath(os.path.join(os.path.dirname(__file__), log_name))

    @staticmethod
    def android_home_exists():
        """检查ANDROID_HOME环境变量是否设置"""
        return "ANDROID_HOME" in os.environ

    @staticmethod
    def adb_command(os_type):
        """检查adb命令是否存在"""
        root_dir = os.path.join(os.environ["ANDROID_HOME"], "platform-tools")
        adb_name = "adb.exe" if os_type == 'windows' else "adb"

        for path, _, files in os.walk(root_dir):
            if adb_name in files:
                return os.path.join(path, adb_name)
        return None

    @staticmethod
    def get_device_id():
        """获取设备ID"""
        os.system('adb kill-server && sleep 3 && adb start-server && sleep 5')
        devices_output = os.popen("adb devices").read().strip()

        if not devices_output or 'error' in devices_output:
            sys.exit(f'[ERROR] Get devices error: {devices_output}')

        matches = re.findall(r'^(\S+)\tdevice$', devices_output, re.MULTILINE)
        if not matches:
            sys.exit('[ERROR] No devices found or device unauthorized.')

        return matches[0]

    @staticmethod
    def check_logcat_available():
        """检查logcat命令是否可用"""
        log_cat_output = os.popen("adb logcat -g").read()
        if "Unable to open log device" in log_cat_output:
            sys.exit(f'[ERROR] {log_cat_output}')

    def get_log_to_file(self, device_id, file_path):
        """后台调用 logcat 获取日志到文件"""
        clear_buffer_command = ['adb', '-s', device_id, 'logcat', '-c']
        get_log_command = ['adb', '-d', '-s', device_id, 'logcat', '-v', 'time', '-s', '*:W']

        subprocess.run(clear_buffer_command, capture_output=True)
        log_process = subprocess.Popen(
            get_log_command, 
            stdout=open(file_path, 'a'), 
            stderr=subprocess.STDOUT
        )
        return log_process

    def terminate_subprocess(self, process):
        """终止指定的子进程"""
        try:
            process.terminate()  # 尝试安全终止
            process.wait(timeout=5)  # 等待进程终止
        except subprocess.TimeoutExpired:
            process.kill()  # 进程没有响应.terminate()，强制终止

    @staticmethod
    def backup_log_file_if_needed(file_path):
        """备份超过大小的日志文件"""
        if os.path.exists(file_path) and os.path.getsize(file_path) >= 20 * 1024 * 1024:
            timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
            dirname, basename = os.path.split(file_path)
            name, ext = os.path.splitext(basename)
            new_name = f'{name}_{timestamp}{ext}'
            new_path = os.path.join(dirname, new_name)
            os.rename(file_path, new_path)


if __name__ == '__main__':
    print('-' * 75)
    app_log = AppLog()

    if not app_log.android_home_exists():
        sys.exit("\nANDROID_HOME not set. Please set the Android SDK path in ANDROID_HOME environment variable.\n")
    
    os_type = app_log.os_type()
    adb_path = app_log.adb_command(os_type)
    if not adb_path:
        sys.exit(f'\nADB command not found for OS: {os_type}')

    log_file_path = app_log.get_log_file_path()
    device_id = app_log.get_device_id()
    app_log.check_logcat_available()
    app_log.get_log_to_file(device_id, log_file_path)
    app_log.backup_log_file_if_needed(log_file_path)

    # 运行 adb monkey 命令
    package_name_to_test = 'com.xkw.client'
    monkey_rounds = 1000  # 修改为你想要的轮次数量
    monkey_log_path = app_log.get_log_file_path('monkey_test_log.txt')  # 也可以自定义日志文件的路径   
    monkey_process = app_log.run_adb_monkey(package_name_to_test, monkey_rounds, monkey_log_path)

    if monkey_process.returncode == 0:  # 确保 Monkey 测试顺利完成
        # 获取系统日志
        device_id = app_log.get_device_id()
        log_file_path = app_log.get_log_file_path()
        log_process = app_log.get_log_to_file(device_id, log_file_path)

        # 这里可以实现其他逻辑，例如等待或者处理日志

        # 程序结束前终止logcat日志收集进程
        app_log.terminate_subprocess(log_process)

        # 如果需要，备份日志文件
        app_log.backup_log_file_if_needed(log_file_path)
```

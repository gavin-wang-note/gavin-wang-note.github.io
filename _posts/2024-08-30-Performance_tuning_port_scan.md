---
title: Performance tuning for a port scan script
date: 2024-08-30
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
summary: Performance tuning a Linux port scan script
categories:
    - [python]
tags:
    - python
---

# Overview

A long time ago to check the information, came across this script, save it has not been used, today finishing computer files, found this file, vaguely remember that it is a compatriot in Taiwan to write, specifically his blog site can not be remembered (such as copyright infringement, please contact me to delete).
This script to achieve the specified machine port range scanning, and determine whether the available ports, the shortcomings are the lack of concurrency, the overall implementation of low performance.

# Source code

The original code is referenced below:

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import sys 
from datetime import datetime
from time import strftime


def checkPort(minPort, maxPort) :
    try:
        if int(int(minPort) >= 0 and int(maxPort) >= 0 and int(maxPort) >= int(minPort)):

            ports = range(int(minPort), int(maxPort) + 1) # 定義掃描 port 範圍
            return ports
        else:
            print("\n Range of Ports. Error")
            print("[!] Exiting...")
            sys.exit(1)
    except Exception:
         print("\n Range of Ports. Error")
         print("[!] Exiting...")
         sys.exit(1)
def checkHost(targetIP):
    conf.L3socket = L3RawSocket # 是為了讓 lookback 能夠運行
    conf.verb = False # 書初步顯示
    try:
        ping = sr1(IP(dst = targetIP)/ICMP(),timeout=1) # 定義 ping 的封包
        print("\n[*] Target is Up, Beginning Scan...")
    except Exception:
        print("\n[!] Couldn't Resolve Target")
        print("[!] Exiting...")
        traceback.print_exc()
        sys.exit(1)
def scanport(port):
    conf.L3socket = L3RawSocket
    try:
        srcPort = RandShort() # Client 端隨機產生 port 
        conf.verb = False
        SYN_ACK_Packet = sr1(IP(dst = targetIP)/TCP(sport = srcPort, dport = port, flags = "S"),timeout=3) # 定義 TCP SYN/ACK 封包
        packetFlags = SYN_ACK_Packet.getlayer(TCP).flags # 取得 flag
        return isFlags(packetFlags)
        RSTpkt = IP(dst = targetIP)/TCP(sport = srcPort, dport = port, flags = "R") # 定義 TCP　RST 封包
        send(RSTpkt) # 第三層（網路層），發送
    except KeyboardInterrupt:
        RSTpkt = IP(dst = target)/TCP(sport = srcPort, dport = port, flags = "R")
        send(RSTpkt)
        print("\n[*] User Requested Shutdown...")
        print("[*] Exiting...")
        sys.exit(1)

def isFlags(packetFlags): # 比對回應的 TCP flag
    if packetFlags == SYNACK:
        return True
    else:
        return False
        
def getTime():
    return datetime.now() # 取得時間

def totalTime(startTime, endTime):
    print("[*] Total Scan Duration: " + str(endTime - startTime)) # 起始時間跟結束時間，耗費多久

def scanStart():
    print("[*] Scanning Started at " + strftime("%H:%M:%S") + "!\n")

def scanningPrintOpenPort(ports): # 掃描 port 
    for port in ports:
        status = scanport(port)
        isPortOpen(status, port)

def isPortOpen(status, port): # 檢測 port 是否開啟
    if status == True:
        print("Port " + str(port) + ": Open")


# TCP flag
SYNACK = 0x12 
RSTACK = 0x14
startTime = getTime() # 掃描開始時間
try:
    targetIP = input("[*] Enter Target IP Address: ")
    minPort = input("[*] Enter Minumum Port Number: ")
    maxPort = input("[*] Enter Maximum Port Number: ")
    ports = checkPort(minPort, maxPort) # 檢查輸入的 port ，Port 範圍 0 ~ 65536
except KeyboardInterrupt:
    print("\n[*] User Requested Shutdown...")
    print("[*] Exiting...")
    sys.exit(1)

#ports = range(int(minPort), int(maxPort)+1)

checkHost(targetIP) # 確認輸入 IP 使否能 ping 
scanStart() 

scanningPrintOpenPort(ports) # 掃描使用者輸入的 Port

endTime = getTime() # 掃描結束時間

print("\n[*] Scanning Finished!")

totalTime(startTime,endTime) # 總共花費時間
```

# Performance Tuning

Performance tuning towards increased concurrency:

```python
root@Gavin:~# cat scan_2.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import logging
from concurrent.futures import ThreadPoolExecutor
from scapy.all import *
import sys
from datetime import datetime

# 设置Scapy的日志级别为ERROR
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# 检查端口范围
def checkPort(minPort, maxPort):
    try:
        minPort = int(minPort)
        maxPort = int(maxPort)
        if minPort < 0 or maxPort < minPort:
            raise ValueError("Invalid port range")
        return range(minPort, maxPort + 1)
    except ValueError as e:
        print(f"\n Range of Ports Error: {e}")
        sys.exit(1)

# 检查主机是否可达
def checkHost(targetIP):
    conf.L3socket = L3RawSocket
    conf.verb = 0
    try:
        ping = sr1(IP(dst=targetIP)/ICMP(), timeout=1)
        if not ping:
            raise Exception("Target is Down")
        print("\n[*] Target is Up, Beginning Scan...")
    except Exception as e:
        print(f"\n[!] Couldn't Resolve Target: {e}")
        sys.exit(1)

# 扫描端口并返回端口状态
def scan_port(port):
    srcPort = RandShort()
    packet = IP(dst=targetIP)/TCP(sport=srcPort, dport=port, flags="S")
    response = sr1(packet, timeout=3)
    return response is not None and response.haslayer(TCP) and response.getlayer(TCP).flags == "SA"

# 异步扫描端口
def scan_ports(ports):
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(scan_port, ports))
        for port, is_open in enumerate(results):
            if is_open:
                print(f"Port {port}: Open")

# 获取当前时间
def getTime():
    return datetime.now()

# 打印扫描总耗时
def totalTime(startTime, endTime):
    duration = endTime - startTime
    if duration.total_seconds() < 0:
        print(f"[*] Total Scan Duration: {duration}")
    else:
        print(f"[*] Total Scan Duration: {duration}")

# 主函数
def main():
    global targetIP
    try:
        targetIP = input("[*] Enter Target IP Address: ")
        minPort = input("[*] Enter Minimum Port Number: ")
        maxPort = input("[*] Enter Maximum Port Number: ")
        ports = checkPort(minPort, maxPort)
        checkHost(targetIP)
        startTime = getTime()  # 获取扫描开始时间
        print("[*] Scanning Started at " + strftime("%H:%M:%S") + "!\n")
        scan_ports(ports)
        endTime = getTime()  # 获取扫描结束时间
        print("\n[*] Scanning Finished!")
        totalTime(startTime, endTime)
    except KeyboardInterrupt:
        print("\n[*] User Requested Shutdown...")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

In this optimized version, I made the following changes:

- Used concurrent.futures.ThreadPoolExecutor to create a thread pool so that thread resources can be managed more efficiently.
- Modified the scanport function to scan_port so that it returns a boolean value of whether the port is open or not.
- Created the scan_ports function to perform port scans concurrently using the map method of ThreadPoolExecutor.
- Removed the isFlags and isPortOpen functions from the original code, as the port status is now returned directly by scan_port.
- Moved SYNACK and RSTACK constant definitions to appropriate locations in the code and fixed the value of SYNACK (should be 0x12).
- Optimized exception handling to ensure that a clear error message is provided and the program exits when an error occurs.

# Comparison of execution time before and after performance tuning

Before Performance Tuning

```shell
root@Gavin:~# python3 scan.py 
[*] Enter Target IP Address: 192.168.23.129
[*] Enter Minumum Port Number: 443
[*] Enter Maximum Port Number: 6666

[*] Target is Up, Beginning Scan...
[*] Scanning Started at 12:38:20!

Port 3000: Open
Port 3001: Open
Port 4000: Open
Port 6000: Open

[*] Scanning Finished!
[*] Total Scan Duration: 0:04:06.791587
root@Gavin:~# python3 scan.py 
[*] Enter Target IP Address: 192.168.23.129
[*] Enter Minumum Port Number: 443
[*] Enter Maximum Port Number: 6666 

[*] Target is Up, Beginning Scan...
[*] Scanning Started at 12:46:08!

Port 3000: Open
Port 3001: Open
Port 4000: Open
Port 6000: Open

[*] Scanning Finished!
[*] Total Scan Duration: 0:03:47.173049
root@Gavin:~# 
```

After Performance Tuning:

```shell
root@Gavin:~# python3 scan_2.py 
[*] Enter Target IP Address: 192.168.23.129
[*] Enter Minimum Port Number: 443
[*] Enter Maximum Port Number: 6666

[*] Target is Up, Beginning Scan...
[*] Scanning Started at 13:50:48!

Port 2557: Open
Port 2558: Open
Port 3557: Open
Port 5557: Open

[*] Scanning Finished!
[*] Total Scan Duration: 0:00:23.715606
root@Gavin:~# python3 scan_2.py 
[*] Enter Target IP Address: 192.168.23.129
[*] Enter Minimum Port Number: 443
[*] Enter Maximum Port Number: 6666

[*] Target is Up, Beginning Scan...
[*] Scanning Started at 13:51:46!

Port 2557: Open
Port 2558: Open
Port 3557: Open
Port 5557: Open

[*] Scanning Finished!
[*] Total Scan Duration: 0:00:23.666786
root@Gavin:~#
```
The time taken has dropped from about 4 minutes to about 23 second.
Coooooooooool. 

---
layout:     post
title:      "获取SSD寿命"
subtitle:   "Get life span for SSD device"
date:       2020-01-22
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# 前言

SSD虽然不是机械盘，但上面的晶元伴随着数据的擦写，导致晶元厚度越来越薄，当晶元厚度薄到一定程度时，意味着SSD寿命已尽，对于存储产品，更迫切的需要知道当前集群里使用的SSD，其寿命还有多少。

目前lab里常见的SSD，型号有S4610，S3700和NVME的，NVME的是PCI-e类型的，但intelS4600，S4610，S7300之类型号的SSD，有的设备是在RAID卡上，但有的设备上又不在RAID卡上。如何确定这些NVME，在RAID卡和不在RAID卡上的SSD的剩余寿命呢？

# NVME类型的SSD的使用寿命获取

## 方法1：借助nvmemgr获取

NVME有一个driver，这个driver可以监控NVMESSD的状态以及获取实时信息，有兴趣的可以参考nvmemgr driver的help信息：

```
root@CVM-01:~# nvmemgr 
nvmemgr version: 00.06.202
usage: nvmemgr <command> [<options>] <target> [<args>]

  list                          List all the controllers and namespaces on this machine
  monitor                       Show basic infomations of the controller in real time
  dump                          Dump the controller registers of the NVMe controller
  identify                      Describe the controller/namespace capabilities and status
  getlogpage                    Return a data buffer containing the log page requested
  asynceventreq                 Request controller to report status/error/health information as these events occurs
  getfeature                    Retrieve the attributes of the feature specified
  setfeature                    Specify the attributes of the feature specified
  fwactivate                    Verify a valid f/w image has been downloaded and activate it
  fwdownload                    Download the firmware image for a future update to the controller
  formatnvm                     Low level format a namespace or all namespace on a controller
  reset                         Initiate an NVM subsystem reset
  locate                        locate nvme device
  cpu-cycle                     Get the cpu performance cycle statistics
  io-count                      Get the I/O counter statistics
  ipc-stats                     Get the IPC statistics
  link-stats                    Get the PCIe link statistics
  io-latency                    Get the I/O latency statistics
  backend-stats                 Get the backend statistics
  flash-latency                 Get the flash latency statistics
  sched-statistic               Get the schedule manager statistics
  sched-rderr                   Get the schedule manager read error state
  sched-wrerr                   Get the schedule manager write error state
  flash-msg-history             Get flash message history
  lun-mgr-sts                   Get lun manager status
  phy-bufid-sts                 Get physical buffer ID status
  dump-pageframe                Dump a page frame with physical flash address
  get-pedata                    Get PE data
  read-retry                    Read retry and dump a data frame with physical flash address
  nvme-dump-msglog              Dump each proccessor's message
  pcie-dump-msglog              Dump each proccessor's message via pcie
  parse-raw-msglog              Parse the raw binary firmware message log
  node-map                      Show the node map
  dump-core-mem                 Dump processor core memory
  pcie-dump-dataframe           Dump a data frame with physical flash address via pcie
  pcie-prog-page                Program a page with physical flash address via pcie
  pcie-erase-block              Erase a block with physical flash address via pcie
  pcie-read-ddr                 Read ddr data out via pcie
  pcie-dump-csr                 Dump command status register value
  pcie-pause                    Force the target node enter the pause state in interrupt context
  pcie-resume                   Exit the pause state
  dump-ftl                      Dump ftl table
  nvme-abrupt-shutdown          Simulate abrupt shutdown via nvme
  pcie-abrupt-shutdown          Simulate abrupt shutdown via pcie
  lookup-chunkInfo              Get lookup chunk Info
  read-eeprom                   Read 32 bits value from eeprom with offset at a time
  write-eeprom                  Write 32 bits value to eeprom with offset at a time
  fw-describe                   Display the firmware description more than version-nmuber only.
  oob-fw-download               Download the firmware image to the oob module
  oob-fw-version                Get the version of oob firmware image in mcu
  oob-fw-activate               Activate the oob firmware image in mcu
  oob-vpd-enable                Execute enable/disable/get_status of oob vpd flag
  set-oob-vpd-model-serial      Set oob vpd model number/serial number
  get-oob-vpd-model-serial      Get oob vpd model number/serial number
  oob-nvme-enable               Execute enable/disable/get_status of oob nvme flag
  set-pcie-id                   Set the PCIe device/vendor/sub-system IDs
  get-pcie-id                   Get the PCIe device/vendor/sub-system IDs
  lookup-statistic              Get the lookup manager statistics
  dump-sb                       Dump super block informations
  allfwdownload                 Download both controller and oob firmware
  write-flash                   Recover bricked PBlaze4 card via write new firmware
  force-pcie-mode               Force drive boot into PCIe mode, always used before write-flash
  read-pci-cmd                  Read out pcicmd&sts reg value
  force-set-pci-cmd             Force set Pci Cmd register MSE and BME bit to 1
  force-sb-open                 Force super block open
  clear-sb-open                 Clear super block open
  pcie-get-rsts                 Get recovery status
  micron-force-wp               Force Micron PB4 into write protect mode
  micron-clear-wp               Clear Micron PB4 from write protect mode
  micron-lowlevelformat         Low level format Micron PB4
  micron-clear-errorlogs        Clear event and error logs for Micron PB4
  micron-set-erase-count        Set erase count for Micron PB4
  micron-bgtask-switch          Execute enable/disable bg task for Micron PB4
  micron-create-small-drive     Create small drive for Micron PB4
  micron-read-flash-prog-cnt    Read flash program count for Micron PB4
  micron-mark-block-as-bad      Mark block as bad for Micron PB4
  micron-del-retired-block      Delete retired block for Micron PB4
  micron-get-bad-block-cnt      Get bad block count for Micron PB4
  micron-get-bad-block-info     Get bad block info for Micron PB4
  micron-get-erase-count        Get erase count for Micron PB4
  micron-get-error-log          Get error log for Micron PB4
  micron-physical-to-lba        Calculate physical address to lba for Micron PB4
  micron-lba-to-physical        Calculate lba to physical address for Micron PB4
  micron-get-config-data        Get drive config data for Micron PB4
  micron-get-rbec               Get read bit error count for Micron PB4
  micron-read-fid               Read fid for Micron PB4
  micron-erase-direct           Erase direct for Micron PB4
  micron-vu-lock                Lock vu for Micron PB4
  micron-seq-wr                 Sequencer write for Micron PB4
  micron-seq-rd                 Sequencer read for Micron PB4
  micron-rd-otp                 Read otp for Micron PB4
  micron-get-temp-thro          Get temp throttling for Micron PB4
  micron-set-temp-thro          Set temp throttling for Micron PB4
  micron-read-temp-sensors      Read all temp sensors for Micron PB4
  micron-vu-unlock              Unlock vu for Micron PB4
  help                          Display all the standard and Memblaze specific NVMe commands

More details about a specific command, see 'nvmemgr command [--help | -h]'
root@CVM-01:~# 
```

言归正传，如何通过nvmemgr这个工具获取NVME SSD的寿命呢？

## Step1. 获取NVME的controller name

```
root@CVM-01:~# nvmemgr list | grep controller
controller nvme0 (namespace nvme0n1):
controller  (namespace nvme0n1p1):
controller  (namespace nvme0n1p10):
controller  (namespace nvme0n1p11):
controller  (namespace nvme0n1p12):
controller  (namespace nvme0n1p13):
controller  (namespace nvme0n1p14):
controller  (namespace nvme0n1p15):
controller  (namespace nvme0n1p16):
controller  (namespace nvme0n1p17):
controller  (namespace nvme0n1p18):
controller  (namespace nvme0n1p19):
controller  (namespace nvme0n1p2):
controller  (namespace nvme0n1p20):
controller  (namespace nvme0n1p21):
controller  (namespace nvme0n1p22):
controller  (namespace nvme0n1p23):
controller  (namespace nvme0n1p24):
controller  (namespace nvme0n1p25):
controller  (namespace nvme0n1p3):
controller  (namespace nvme0n1p4):
controller  (namespace nvme0n1p5):
controller  (namespace nvme0n1p6):
controller  (namespace nvme0n1p7):
controller  (namespace nvme0n1p8):
controller  (namespace nvme0n1p9):
```

这里，显示当前系统里，NVME controller name是 ```nvme0 ```


## Step2. 使用nvmemgr monitor获取对应controller信息

```
root@CVM-01:~# nvmemgr monitor -i 1000 -p --ctrl nvme0
Manufacture Name:              Memblaze Technology Co.,Ltd
Product Name:                  PBlaze4
Model Number:                  INTEL SSDPEDMD800G4                     8DV10131
Serial Number:                 CVFT521000FK800CGN  INTEL SSDPEDMD800G4                     8DV10131
Available Capacity:            800.16GB
Percentage of Spare Space      100%
Threshold of Spare Space       10%
Percentage of Device Life Used 4%
Total Read                     1.50TB
Total Write:                   620.36GB
Name:                          /dev/nvme0
Firmware:                      8DV10131
Power Cycles:                  109
Power-on Hours:                18485
Device Temperature:            -273C          -273C      -273C     
Power:                         0W             0W         0W        
Status:                        Safe          
Current Read IOPS:             0.00K
Current Write IOPS:            0.00K
Current Read Bandwidth:        0.00MB/s
Current Write Bandwidth:       0.00MB/s

Manufacture Name:              Memblaze Technology Co.,Ltd
Product Name:                  PBlaze4
Model Number:                  INTEL SSDPEDMD800G4                     8DV10131
Serial Number:                 CVFT521000FK800CGN  INTEL SSDPEDMD800G4                     8DV10131
Available Capacity:            800.16GB
Percentage of Spare Space      100%
Threshold of Spare Space       10%
Percentage of Device Life Used 4%
Total Read                     1.50TB
Total Write:                   620.36GB
Name:                          /dev/nvme0
Firmware:                      8DV10131
Power Cycles:                  109
Power-on Hours:                18485
Device Temperature:            -273C          -273C      -273C     
Power:                         0W             0W         0W        
Status:                        Safe          
Current Read IOPS:             0.00K
Current Write IOPS:            0.02K
Current Read Bandwidth:        0.00MB/s
Current Write Bandwidth:       0.07MB/s
```

上面吐出信息，有一行```Percentage of Device Life Used 4% ```,这里意味着，这块SSD，目前已经使用了4%的寿命，还有96%的可用寿命。



## 方法2：通过NVME smart信息获取

直接上代码

```
root@CVM-01:~# cat get_nvme_ssd_life_time.py 
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""  Get NVME SSD lift left  """

from __future__ import unicode_literals

import os
import ctypes
import ctypes.util


class NVMEPassthruCommand(ctypes.Structure):
    _fields_ = [
        ('opcode', ctypes.c_ubyte),
        ('flags', ctypes.c_ubyte),
        ('rsvd1', ctypes.c_uint16),
        ('nsid', ctypes.c_uint32),
        ('cdw2', ctypes.c_uint32),
        ('cdw3', ctypes.c_uint32),
        ('metadata', ctypes.c_uint64),
        ('addr', ctypes.c_uint64),
        ('metadata_len', ctypes.c_uint32),
        ('data_len', ctypes.c_uint32),
        ('cdw10', ctypes.c_uint32),
        ('cdw11', ctypes.c_uint32),
        ('cdw12', ctypes.c_uint32),
        ('cdw13', ctypes.c_uint32),
        ('cdw14', ctypes.c_uint32),
        ('cdw15', ctypes.c_uint32),
        ('timeout_ms', ctypes.c_uint32),
        ('result', ctypes.c_uint32)
    ]


class NVMESmartLog(ctypes.Structure):
    _fields_ = [
        ('critical_warning', ctypes.c_ubyte),
        ('temperature', ctypes.c_ubyte * 2),
        ('avail_spare', ctypes.c_ubyte),
        ('spare_thresh', ctypes.c_ubyte),
        ('percent_used', ctypes.c_ubyte),
        ('rsvd6', ctypes.c_ubyte * 26),
        ('data_units_read', ctypes.c_ubyte * 16),
        ('data_units_written', ctypes.c_ubyte * 16),
        ('host_reads', ctypes.c_ubyte * 16),
        ('host_writes', ctypes.c_ubyte * 16),
        ('ctrl_busy_time', ctypes.c_ubyte * 16),
        ('power_cycles', ctypes.c_ubyte * 16),
        ('power_on_hours', ctypes.c_ubyte * 16),
        ('unsafe_shutdowns', ctypes.c_ubyte * 16),
        ('media_errors', ctypes.c_ubyte * 16),
        ('num_err_log_entries', ctypes.c_ubyte * 16),
        ('warning_temp_time', ctypes.c_uint32),
        ('critical_comp_time', ctypes.c_uint32),
        ('temp_sensor', ctypes.c_uint16 * 8),
        ('thm_temp1_trans_count', ctypes.c_uint32),
        ('thm_temp2_trans_count', ctypes.c_uint32),
        ('thm_temp1_total_time', ctypes.c_uint32),
        ('thm_temp2_total_time', ctypes.c_uint32),
        ('rsvd232', ctypes.c_ubyte * 280)
    ]


class IoctlGeneric(object):
    _IOC_NRBITS = 8
    _IOC_TYPEBITS = 8
    _IOC_SIZEBITS = 14
    _IOC_DIRBITS = 2
    _IOC_NONE = 0
    _IOC_WRITE = 1
    _IOC_READ = 2

    @classmethod
    def ioc(cls, direction, request_type, request_nr, size):
        _IOC_NRSHIFT = 0
        _IOC_TYPESHIFT = _IOC_NRSHIFT + cls._IOC_NRBITS
        _IOC_SIZESHIFT = _IOC_TYPESHIFT + cls._IOC_TYPEBITS
        _IOC_DIRSHIFT = _IOC_SIZESHIFT + cls._IOC_SIZEBITS
        return (
            (direction << _IOC_DIRSHIFT) |
            (request_type << _IOC_TYPESHIFT) |
            (request_nr << _IOC_NRSHIFT) |
            (size << _IOC_SIZESHIFT)
        )

NVME_ADMIN_IDENTIFY = 0x06
NVME_LOG_SMART = 0x02
NVME_ADMIN_GET_LOG_PAGE = 0x02
NSID = 0xffffffff
_ioctl_fn = None

def _get_ioctl_fn():
    global _ioctl_fn
    if _ioctl_fn is not None:
        return _ioctl_fn
    libc_name = ctypes.util.find_library('c')
    if not libc_name:
        raise Exception('Unable to find c library')
    libc = ctypes.CDLL(libc_name, use_errno=True)
    _ioctl_fn = libc.ioctl
    return _ioctl_fn


def ioctl(fd, request, *args):
    ioctl_args = [ctypes.c_int(fd), ctypes.c_ulong(request)] + list(args)

    try:
        ioctl_fn = _get_ioctl_fn()
    except Exception as e:
        raise NotImplementedError(
            'Unable to get ioctl()-function from C library: {err}'.format(err=str(e)))

    res = ioctl_fn(*ioctl_args)
    if res < 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err))
    return res

def IOWR(request_type, request_nr, size):
    calc = IoctlGeneric()
    return calc.ioc(calc._IOC_READ | calc._IOC_WRITE, ord(request_type), request_nr, size)

def nvme_submit_admin_passthru(fd, cmd):
    NVME_IOCTL_ADMIN_CMD = IOWR('N', 0x41, ctypes.sizeof(cmd))
    return ioctl(fd, NVME_IOCTL_ADMIN_CMD, ctypes.byref(cmd))

def get_smart_log(dev_name):
    try:
        fd = os.open(dev_name, os.O_RDONLY)
        smart_log = NVMESmartLog()
        ret = nvme_get_log(fd, NSID, NVME_LOG_SMART, smart_log)
    except Exception as ex:
        raise RuntimeError("can not get device smart log : (%s)", str(ex))
    finally:
        os.close(fd)
    return smart_log

def nvme_get_log(fd, nsid, log_id, data):
    admin_cmd = NVMEPassthruCommand()
    admin_cmd.opcode = NVME_ADMIN_GET_LOG_PAGE
    admin_cmd.nsid = nsid
    admin_cmd.addr = ctypes.addressof(data)
    data_len = ctypes.sizeof(data)
    admin_cmd.data_len = data_len
    numd = (data_len >> 2) - 1
    numdu = numd >> 16
    numdl = numd & 0xffff
    admin_cmd.cdw10 = log_id | (numdl << 16)
    admin_cmd.cdw11 = numdu
    return nvme_submit_admin_passthru(fd, admin_cmd)

if __name__ == '__main__':
    dev_name= '/dev/nvme0n1'
    smart_log = get_smart_log(dev_name)
    print smart_log.percent_used
```

执行效果：

```
root@CVM-01:~# python get_nvme_ssd_life_time.py 
4
root@CVM-01:~# 
```

结果返回是4，说明只使用了4%的寿命，还剩余96%的寿命，这里计算出来的，和通过nvmemgr monitor获取到的，完全一致~



# 非NVME SSD寿命获取

## 如何区分SSD是不是在RAID卡上呢？


### SSD 不在RAID卡上

```
root@node243:~# lsscsi
[0:0:9:0]    enclosu GOOXIBM  2U12SXP 24Sx12G  B013  -        
[0:0:13:0]   disk    ATA      INTEL SSDSC2KG48 0100  /dev/sdk 
[0:0:23:0]   disk    ATA      INTEL SSDSC2KG48 0121  /dev/sdl 
[0:2:0:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdd 
[0:2:1:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sda 
[0:2:2:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdb 
[0:2:3:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdc 
[0:2:4:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sde 
[0:2:5:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdf 
[0:2:6:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdg 
[0:2:7:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdh 
[0:2:8:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdi 
[0:2:9:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdj
```


### SSD 在RAID卡上

```
root@node243:~# lsblk -d -o name,rota
NAME ROTA
sda     1
sdb     1
sdc     1
sdd     1
sde     1
sdf     1
sdg     1
sdh     1
sdi     1
sdj     1
sdk     1
sdl     1
root@node243:~# lsscsi 
[0:0:9:0]    enclosu GOOXIBM  2U12SXP 24Sx12G  B013  -        
[0:2:0:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdd 
[0:2:1:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sda 
[0:2:2:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdb 
[0:2:3:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdc 
[0:2:4:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sde 
[0:2:5:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdf 
[0:2:6:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdg 
[0:2:7:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdh 
[0:2:8:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdi 
[0:2:9:0]    disk    AVAGO    MR9361-8i        4.68  /dev/sdj 
[0:2:10:0]   disk    AVAGO    MR9361-8i        4.68  /dev/sdk 
[0:2:11:0]   disk    AVAGO    MR9361-8i        4.68  /dev/sdl 
root@node243:~# 
```


对比了一下 ```lsscsi ```吐出的信息，发现在RAID卡上的SSD，都会含有RAID卡的型号，而且没法直接看出是否是SSD，自然也没法分辨出SSD分区信息。

本文RAID卡型号是LSI的，显示是AVAGO，截取了片段信息，如下:

```
root@CVM-01:~# /opt/MegaRAID/MegaCli/MegaCli64 adpallinfo -a0
                                     
Adapter #0

==============================================================================
                    Versions
                ================
Product Name    : AVAGO 3108 MegaRAID
Serial No       : 
FW Package Build: 24.15.0-0018
```


## SSD不在RAID卡上，SSD寿命的获取

说明：

* 通过```lsblk```或者```lsscsi```命令，都可以获取SSD分区信息
* 如果SSD在RAID卡上，但是设置成JBOD模式，依然可以通过本章节方法获取SSD寿命

### Step1. 先获取到SSD分区信息
```
root@node-196:~# lsblk -d -o name,rota
NAME ROTA
rbd0    0
sdd     0
sdb     1
sde     0
sdc     1
sda     1
root@node-196:~# lsscsi 
[0:0:8:0]    enclosu AIC CORP SAS 6G Expander  0b01  -        
[0:2:0:0]    disk    LSI      MR9271-8i        3.24  /dev/sda 
[0:2:1:0]    disk    LSI      MR9271-8i        3.24  /dev/sdb 
[0:2:2:0]    disk    LSI      MR9271-8i        3.24  /dev/sdc 
[1:0:0:0]    disk    ATA      INTEL SSDSC2BA40 0270  /dev/sdd 
[2:0:0:0]    disk    ATA      INTEL SSDSC2BA40 0270  /dev/sde 
root@node-196:~# 
```

如上，可以看出，SSD对应分区是/dev/sdd 和 /dev/sde，对于rbd0，是存储export出来的device，这里忽略它。

### Step2. 查看smart信息

```
root@node-196:~# smartctl -a /dev/sdd
smartctl 7.0 2018-12-30 r4883 [x86_64-linux-4.14.148-server] (local build)
Copyright (C) 2002-18, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===
Model Family:     Intel 730 and DC S35x0/3610/3700 Series SSDs
Device Model:     INTEL SSDSC2BA400G3
Serial Number:    BTTV449301BQ400HGN
LU WWN Device Id: 5 5cd2e4 04b73452c
Firmware Version: 5DV10270
User Capacity:    400,088,457,216 bytes [400 GB]
Sector Sizes:     512 bytes logical, 4096 bytes physical
Rotation Rate:    Solid State Device
Form Factor:      2.5 inches
Device is:        In smartctl database [for details use: -P show]
ATA Version is:   ACS-2 T13/2015-D revision 3
SATA Version is:  SATA 2.6, 6.0 Gb/s (current: 6.0 Gb/s)
Local Time is:    Thu Jan 23 10:10:27 2020 CST
SMART support is: Available - device has SMART capability.
SMART support is: Enabled

=== START OF READ SMART DATA SECTION ===
SMART overall-health self-assessment test result: PASSED

General SMART Values:
Offline data collection status:  (0x02)	Offline data collection activity
					was completed without error.
					Auto Offline Data Collection: Disabled.
Self-test execution status:      (   0)	The previous self-test routine completed
					without error or no self-test has ever 
					been run.
Total time to complete Offline 
data collection: 		(    2) seconds.
Offline data collection
capabilities: 			 (0x79) SMART execute Offline immediate.
					No Auto Offline data collection support.
					Suspend Offline collection upon new
					command.
					Offline surface scan supported.
					Self-test supported.
					Conveyance Self-test supported.
					Selective Self-test supported.
SMART capabilities:            (0x0003)	Saves SMART data before entering
					power-saving mode.
					Supports SMART auto save timer.
Error logging capability:        (0x01)	Error logging supported.
					General Purpose Logging supported.
Short self-test routine 
recommended polling time: 	 (   1) minutes.
Extended self-test routine
recommended polling time: 	 (   2) minutes.
Conveyance self-test routine
recommended polling time: 	 (   2) minutes.
SCT capabilities: 	       (0x003d)	SCT Status supported.
					SCT Error Recovery Control supported.
					SCT Feature Control supported.
					SCT Data Table supported.

SMART Attributes Data Structure revision number: 1
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  5 Reallocated_Sector_Ct   0x0032   100   100   000    Old_age   Always       -       0
  9 Power_On_Hours          0x0032   100   100   000    Old_age   Always       -       37769
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       324
170 Available_Reservd_Space 0x0033   100   100   010    Pre-fail  Always       -       0
171 Program_Fail_Count      0x0032   100   100   000    Old_age   Always       -       0
172 Erase_Fail_Count        0x0032   100   100   000    Old_age   Always       -       0
174 Unsafe_Shutdown_Count   0x0032   100   100   000    Old_age   Always       -       271
175 Power_Loss_Cap_Test     0x0033   100   100   010    Pre-fail  Always       -       614 (179 4205)
183 SATA_Downshift_Count    0x0032   100   100   000    Old_age   Always       -       0
184 End-to-End_Error        0x0033   100   100   090    Pre-fail  Always       -       0
187 Reported_Uncorrect      0x0032   100   100   000    Old_age   Always       -       0
190 Temperature_Case        0x0022   077   074   000    Old_age   Always       -       23 (Min/Max 18/26)
192 Unsafe_Shutdown_Count   0x0032   100   100   000    Old_age   Always       -       271
194 Temperature_Internal    0x0022   100   100   000    Old_age   Always       -       34
197 Current_Pending_Sector  0x0032   100   100   000    Old_age   Always       -       0
199 CRC_Error_Count         0x003e   100   100   000    Old_age   Always       -       0
225 Host_Writes_32MiB       0x0032   100   100   000    Old_age   Always       -       20629803
226 Workld_Media_Wear_Indic 0x0032   100   100   000    Old_age   Always       -       5468
227 Workld_Host_Reads_Perc  0x0032   100   100   000    Old_age   Always       -       13
228 Workload_Minutes        0x0032   100   100   000    Old_age   Always       -       2263937
232 Available_Reservd_Space 0x0033   100   100   010    Pre-fail  Always       -       0
233 Media_Wearout_Indicator 0x0032   095   095   000    Old_age   Always       -       0
234 Thermal_Throttle        0x0032   100   100   000    Old_age   Always       -       0/0
241 Host_Writes_32MiB       0x0032   100   100   000    Old_age   Always       -       20629803
242 Host_Reads_32MiB        0x0032   100   100   000    Old_age   Always       -       3310760

SMART Error Log Version: 1
No Errors Logged

SMART Self-test log structure revision number 1
Num  Test_Description    Status                  Remaining  LifeTime(hours)  LBA_of_first_error
# 1  Short offline       Completed without error       00%     27499         -

SMART Selective self-test log data structure revision number 1
 SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS
    1        0        0  Not_testing
    2        0        0  Not_testing
    3        0        0  Not_testing
    4        0        0  Not_testing
    5        0        0  Not_testing
Selective self-test flags (0x0):
  After scanning selected spans, do NOT read-scan remainder of disk.
If Selective self-test is pending on power-up, resume after 0 minute delay.

root@node-196:~#
```

上面吐出的信息，有一行```Media_Wearout_Indicator```，这行有一列```WORST```，它对应的值，就是当前SSD寿命剩余百分比值，比如这里的95%，表示此块SSD还有95%的使用寿命。


## SSD在RAID卡上，SSD寿命的获取

### Step1. 获取SSD分区名称

尝试使用lsblk去获取

```
root@node243:~# lsblk -d -o name,rota
NAME ROTA
sda     1
sdb     1
sdc     1
sdd     1
sde     1
sdf     1
sdg     1
sdh     1
sdi     1
sdj     1
sdk     1
sdl     1
root@node243:~# 
```

发现吐出的结果全部是1，很显然，当SSD在RAID卡上，且加入RAID组后，lsblk无法获取出哪个分区是SSD了。。。怎么破？

换个思路，使用megacli命令试试：

```
root@node243:~# /opt/MegaRAID/MegaCli/MegaCli64 ldpdinfo aall | grep -Ei 'Device Id:|Inquiry Data:|Raw Size:'
Enclosure Device ID: 9
Device Id: 24
Raw Size: 279.396 GB [0x22ecb25c Sectors]
Inquiry Data: SEAGATE ST300MM0048     N001W0K156RV            
Enclosure Device ID: 9
Device Id: 12
Raw Size: 3.638 TB [0x1d1c0beb0 Sectors]
Inquiry Data: K3H25KAL            HGST HUS726040ALE610                    APGNTD05
Enclosure Device ID: 9
Device Id: 14
Raw Size: 3.638 TB [0x1d1c0beb0 Sectors]
Inquiry Data: V6G6BUJN            HGST HUS726T4TALE6L4                    VKGNW40H
Enclosure Device ID: 9
Device Id: 17
Raw Size: 3.638 TB [0x1d1c0beb0 Sectors]
Inquiry Data: V6G6GRHN            HGST HUS726T4TALE6L4                    VKGNW40H
Enclosure Device ID: 9
Device Id: 15
Raw Size: 3.638 TB [0x1d1c0beb0 Sectors]
Inquiry Data: V6G6DTSN            HGST HUS726T4TALE6L4                    VKGNW40H
Enclosure Device ID: 9
Device Id: 16
Raw Size: 3.638 TB [0x1d1c0beb0 Sectors]
Inquiry Data: V6G6GREN            HGST HUS726T4TALE6L4                    VKGNW40H
Enclosure Device ID: 9
Device Id: 19
Raw Size: 3.638 TB [0x1d1c0beb0 Sectors]
Inquiry Data: V6G6GL3N            HGST HUS726T4TALE6L4                    VKGNW40H
Enclosure Device ID: 9
Device Id: 20
Raw Size: 3.638 TB [0x1d1c0beb0 Sectors]
Inquiry Data: V6G4B65N            HGST HUS726T4TALE6L4                    VKGNW40H
Enclosure Device ID: 9
Device Id: 18
Raw Size: 3.638 TB [0x1d1c0beb0 Sectors]
Inquiry Data: V6G6B6NN            HGST HUS726T4TALE6L4                    VKGNW40H
Enclosure Device ID: 9
Device Id: 21
Raw Size: 3.638 TB [0x1d1c0beb0 Sectors]
Inquiry Data: V6G6GYJN            HGST HUS726T4TALE6L4                    VKGNW40H
Enclosure Device ID: 9
Device Id: 23
Raw Size: 447.130 GB [0x37e436b0 Sectors]
Inquiry Data: BTYM7406012Z480BGN  INTEL SSDSC2KG480G7                     SCV10121
Enclosure Device ID: 9
Device Id: 13
Raw Size: 447.130 GB [0x37e436b0 Sectors]
Inquiry Data: BTYM72940D40480BGN  INTEL SSDSC2KG480G7                     SCV10100
root@node243:~# 
```

这里有一列信息```Inquiry Data```，表示每个Device的序列号，里面有品牌信息，其中，```INTEL SSDSC2KG480G7```表示这块盘，是INTEL SSD，容量480G，至此，可以知道，```Device Id: 13```（这很重要）这块盘，是SSD，对应分区是/dev/sdl（至于如何确认RAID卡上RAID组对应哪个系统分区（盘符）信息，参考我的其他推文）

## Step2. smartctl获取smart信息

```
root@node243:~# smartctl -a -d megaraid,23 /dev/sdl
smartctl 6.6 2016-05-31 r4324 [x86_64-linux-4.1.49-server] (local build)
Copyright (C) 2002-16, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===
Device Model:     INTEL SSDSC2KG480G7
Serial Number:    BTYM7406012Z480BGN
LU WWN Device Id: 5 5cd2e4 14ec10087
Firmware Version: SCV10121
User Capacity:    480,103,981,056 bytes [480 GB]
Sector Sizes:     512 bytes logical, 4096 bytes physical
Rotation Rate:    Solid State Device
Form Factor:      2.5 inches
Device is:        Not in smartctl database [for details use: -P showall]
ATA Version is:   ACS-3 T13/2161-D revision 5
SATA Version is:  SATA 3.2, 6.0 Gb/s (current: 6.0 Gb/s)
Local Time is:    Thu Jan 23 11:20:45 2020 CST
SMART support is: Available - device has SMART capability.
SMART support is: Enabled

=== START OF READ SMART DATA SECTION ===
SMART Status not supported: ATA return descriptor not supported by controller firmware
SMART overall-health self-assessment test result: PASSED
Warning: This result is based on an Attribute check.

General SMART Values:
Offline data collection status:  (0x00)	Offline data collection activity
					was never started.
					Auto Offline Data Collection: Disabled.
Self-test execution status:      (   0)	The previous self-test routine completed
					without error or no self-test has ever 
					been run.
Total time to complete Offline 
data collection: 		(    0) seconds.
Offline data collection
capabilities: 			 (0x79) SMART execute Offline immediate.
					No Auto Offline data collection support.
					Suspend Offline collection upon new
					command.
					Offline surface scan supported.
					Self-test supported.
					Conveyance Self-test supported.
					Selective Self-test supported.
SMART capabilities:            (0x0003)	Saves SMART data before entering
					power-saving mode.
					Supports SMART auto save timer.
Error logging capability:        (0x01)	Error logging supported.
					General Purpose Logging supported.
Short self-test routine 
recommended polling time: 	 (   1) minutes.
Extended self-test routine
recommended polling time: 	 (   2) minutes.
Conveyance self-test routine
recommended polling time: 	 (   2) minutes.
SCT capabilities: 	       (0x003d)	SCT Status supported.
					SCT Error Recovery Control supported.
					SCT Feature Control supported.
					SCT Data Table supported.

SMART Attributes Data Structure revision number: 1
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  5 Reallocated_Sector_Ct   0x0032   099   099   000    Old_age   Always       -       4
  9 Power_On_Hours          0x0032   100   100   000    Old_age   Always       -       6198
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       85
170 Unknown_Attribute       0x0033   099   099   010    Pre-fail  Always       -       0
171 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       1
172 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       0
174 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       58
175 Program_Fail_Count_Chip 0x0033   100   100   010    Pre-fail  Always       -       477858433335
183 Runtime_Bad_Block       0x0032   100   100   000    Old_age   Always       -       0
184 End-to-End_Error        0x0033   100   100   090    Pre-fail  Always       -       0
187 Reported_Uncorrect      0x0032   100   100   000    Old_age   Always       -       0
190 Airflow_Temperature_Cel 0x0022   076   068   000    Old_age   Always       -       24 (Min/Max 17/33)
192 Power-Off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       58
194 Temperature_Celsius     0x0022   100   100   000    Old_age   Always       -       24
197 Current_Pending_Sector  0x0012   100   100   000    Old_age   Always       -       0
199 UDMA_CRC_Error_Count    0x003e   100   100   000    Old_age   Always       -       0
225 Unknown_SSD_Attribute   0x0032   100   100   000    Old_age   Always       -       1298207
226 Unknown_SSD_Attribute   0x0032   100   100   000    Old_age   Always       -       1392
227 Unknown_SSD_Attribute   0x0032   100   100   000    Old_age   Always       -       17
228 Power-off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       371377
232 Available_Reservd_Space 0x0033   099   099   010    Pre-fail  Always       -       0
233 Media_Wearout_Indicator 0x0032   099   099   000    Old_age   Always       -       0
234 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       0
241 Total_LBAs_Written      0x0032   100   100   000    Old_age   Always       -       1298207
242 Total_LBAs_Read         0x0032   100   100   000    Old_age   Always       -       279079
243 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       1893917

SMART Error Log Version: 1
No Errors Logged

SMART Self-test log structure revision number 1
No self-tests have been logged.  [To run self-tests, use: smartctl -t]

SMART Selective self-test log data structure revision number 1
 SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS
    1        0        0  Not_testing
    2        0        0  Not_testing
    3        0        0  Not_testing
    4        0        0  Not_testing
    5        0        0  Not_testing
Selective self-test flags (0x0):
  After scanning selected spans, do NOT read-scan remainder of disk.
If Selective self-test is pending on power-up, resume after 0 minute delay.

root@node243:~# 
```

这是一个完整的SSD 分区的smart信息，信息有些多，过滤一下，只获取我们关心的几个值就好：

```
root@node243:~# smartctl -a -d megaraid,23 /dev/sdl | grep -Ei 'Device Model|Serial Number|User Capacity|Media_Wearout_Indicator'
Device Model:     INTEL SSDSC2KG480G7
Serial Number:    BTYM7406012Z480BGN
User Capacity:    480,103,981,056 bytes [480 GB]
233 Media_Wearout_Indicator 0x0032   099   099   000    Old_age   Always       -       0
root@node243:~# 
```

从smart吐出的信息可以看出，这块SSD的使用寿命还有99%(对应smart信息的WORST那一列的值)


那如果不带device id，能直接通过smartctl获取SSD寿命信息么？

```
root@node243:~# smartctl -a /dev/sdl
smartctl 6.6 2016-05-31 r4324 [x86_64-linux-4.1.49-server] (local build)
Copyright (C) 2002-16, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===
Vendor:               AVAGO
Product:              MR9361-8i
Revision:             4.68
User Capacity:        479,559,942,144 bytes [479 GB]
Logical block size:   512 bytes
Logical Unit id:      0x600605b00d75873025bc3ae7a8d1ad1b
Serial number:        001badd1a8e73abc253087750db00506
Device type:          disk
Local Time is:        Thu Jan 23 11:22:10 2020 CST
SMART support is:     Unavailable - device lacks SMART capability.

=== START OF READ SMART DATA SECTION ===
Current Drive Temperature:     0 C
Drive Trip Temperature:        0 C

Error Counter logging not supported

Device does not support Self Test logging
root@node243:~# 
```

从吐出信息来看，是没有的~~



说明：

* 由于lab里只有intel的SSD，这个SSD使用寿命对应smart项是233（Media_Wearout_Indicator），但并不是所有类型的SSD的都是233，参考如下：

```
SSD_INDICATOR = {
    'INTEL': '233',
    'INDILINX': '209',
    'MICRON': '202',
    'SAMSUNG': '177',
    'SANDFORCE': '231'
}
```


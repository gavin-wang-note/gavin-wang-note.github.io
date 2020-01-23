---
layout:     post
title:      "利用modinfo查看kernel使用的driver版本"
subtitle:   "Use modinfo to get driver version which used in kernel"
date:       2020-01-22
author:     "Gavin"
catalog:    true
tags:
    - Linux
---


# 前言

Linux modinfo命令用于显示kernel模块的信息，确切讲，会显示kernel模块的对象文件，以及显示该模块的相关信息。

# 语法

```
root@node243:~# modinfo -h
Usage:
	modinfo [options] filename [args]
Options:
	-a, --author                Print only 'author'
	-d, --description           Print only 'description'
	-l, --license               Print only 'license'
	-p, --parameters            Print only 'parm'
	-n, --filename              Print only 'filename'
	-0, --null                  Use \0 instead of \n
	-F, --field=FIELD           Print only provided FIELD
	-k, --set-version=VERSION   Use VERSION instead of `uname -r`
	-b, --basedir=DIR           Use DIR as filesystem root for /lib/modules
	-V, --version               Show version
	-h, --help                  Show this help
root@node243:~# 

```

# 实践

今天碰到需要给技嘉设备（型号：S451-3R0）更新系统里的QLogic driver，技嘉工程师提供的文件名称为server_driver_qlogic_lan_8.18.16.0.zip，从这里可以看出版本是8.18.16.0，问题来了，我要如何知道，当前系统里QLogic版本是多少？如果版本比技嘉工程师提供的高，自然就不需要更新这个驱动；如果比这个低，那就需要了。


## 查看系统里QLogic driver在内核中加载的模块名称

使用的```lspci -vvv```命令，下面只截取片段信息:

```
3f:00.0 Ethernet controller: QLogic Corp. Device 8070 (rev 02)
        Subsystem: Gigabyte Technology Co., Ltd Device 1000
        Control: I/O- Mem+ BusMaster+ SpecCycle- MemWINV- VGASnoop- ParErr- Stepping- SERR+ FastB2B- DisINTx+
        Status: Cap+ 66MHz- UDF- FastB2B- ParErr- DEVSEL=fast >TAbort- <TAbort- <MAbort- >SERR- <PERR- INTx-
        Latency: 0, Cache Line Size: 32 bytes
        Interrupt: pin A routed to IRQ 411
        Region 0: Memory at b7d20000 (64-bit, prefetchable) [size=128K]
        Region 2: Memory at b7c00000 (64-bit, prefetchable) [size=1M]
        Region 4: Memory at b7d50000 (64-bit, prefetchable) [size=64K]
        Expansion ROM at b8680000 [disabled] [size=512K]
        Capabilities: [40] Power Management version 3
                Flags: PMEClk- DSI- D1- D2- AuxCurrent=375mA PME(D0+,D1-,D2-,D3hot+,D3cold+)
                Status: D0 NoSoftRst+ PME-Enable- DSel=0 DScale=0 PME-
        Capabilities: [50] MSI: Enable- Count=1/8 Maskable+ 64bit+
                Address: 0000000000000000  Data: 0000
                Masking: 00000000  Pending: 00000000
        Capabilities: [70] Express (v2) Endpoint, MSI 00
                DevCap: MaxPayload 512 bytes, PhantFunc 0, Latency L0s unlimited, L1 unlimited
                        ExtTag+ AttnBtn- AttnInd- PwrInd- RBE+ FLReset+
                DevCtl: Report errors: Correctable- Non-Fatal- Fatal- Unsupported-
                        RlxdOrd- ExtTag+ PhantFunc- AuxPwr- NoSnoop+ FLReset-
                        MaxPayload 256 bytes, MaxReadReq 512 bytes
                DevSta: CorrErr+ UncorrErr- FatalErr- UnsuppReq+ AuxPwr+ TransPend-
                LnkCap: Port #0, Speed 8GT/s, Width x8, ASPM not supported, Exit Latency L0s unlimited, L1 <8us
                        ClockPM+ Surprise- LLActRep- BwNot-
                LnkCtl: ASPM Disabled; RCB 64 bytes Disabled- CommClk+
                        ExtSynch- ClockPM- AutWidDis- BWInt- AutBWInt-
                LnkSta: Speed 8GT/s, Width x8, TrErr- Train- SlotClk+ DLActive- BWMgmt- ABWMgmt-
                DevCap2: Completion Timeout: Range ABCD, TimeoutDis+, LTR+, OBFF Via message/WAKE#
                DevCtl2: Completion Timeout: 50us to 50ms, TimeoutDis-, LTR-, OBFF Disabled
                LnkCtl2: Target Link Speed: 8GT/s, EnterCompliance- SpeedDis-
                         Transmit Margin: Normal Operating Range, EnterModifiedCompliance- ComplianceSOS-
                         Compliance De-emphasis: -6dB
                LnkSta2: Current De-emphasis Level: -3.5dB, EqualizationComplete+, EqualizationPhase1+
                         EqualizationPhase2+, EqualizationPhase3+, LinkEqualizationRequest-
        Capabilities: [b0] MSI-X: Enable+ Count=129 Masked-
                Vector table: BAR=4 offset=00000000
                PBA: BAR=4 offset=00001000
        Capabilities: [d0] Vital Product Data
                Product Name: QLogic FastLinQ QL41212H 25GbE Adapter
                Read-only fields:
                        [PN] Part number: AH2010406-01 02
                        [SN] Serial number: AFE1702F15357
                        [V0] Vendor specific: FFV8.18.01
                        [RV] Reserved: checksum good, 4 byte(s) reserved
                End
        Capabilities: [100 v2] Advanced Error Reporting
                UESta:  DLP- SDES- TLP- FCP- CmpltTO- CmpltAbrt- UnxCmplt- RxOF- MalfTLP- ECRC- UnsupReq- ACSViol-
                UEMsk:  DLP- SDES- TLP- FCP- CmpltTO- CmpltAbrt- UnxCmplt- RxOF- MalfTLP- ECRC- UnsupReq- ACSViol-
                UESvrt: DLP+ SDES+ TLP- FCP+ CmpltTO- CmpltAbrt- UnxCmplt- RxOF+ MalfTLP+ ECRC- UnsupReq- ACSViol-
                CESta:  RxErr- BadTLP- BadDLLP- Rollover- Timeout- NonFatalErr+
                CEMsk:  RxErr- BadTLP- BadDLLP- Rollover- Timeout- NonFatalErr+
                                AERCap: First Error Pointer: 00, GenCap+ CGenEn- ChkCap+ ChkEn-
        Capabilities: [148 v1] Virtual Channel
                Caps:   LPEVC=0 RefClk=100ns PATEntryBits=1
                Arb:    Fixed- WRR32- WRR64- WRR128-
                Ctrl:   ArbSelect=Fixed
                Status: InProgress-
                VC0:    Caps:   PATOffset=00 MaxTimeSlots=1 RejSnoopTrans-
                        Arb:    Fixed- WRR32- WRR64- WRR128- TWRR128- WRR256-
                        Ctrl:   Enable+ ID=0 ArbSelect=Fixed TC/VC=01
                        Status: NegoPending- InProgress-
        Capabilities: [168 v1] Device Serial Number 00-00-00-00-00-00-00-00
        Capabilities: [178 v1] Power Budgeting <?>
        Capabilities: [188 v1] Alternative Routing-ID Interpretation (ARI)
                ARICap: MFVC- ACS-, Next Function: 1
                ARICtl: MFVC- ACS-, Function Group: 0
        Capabilities: [198 v1] #19
        Capabilities: [1f8 v1] Transaction Processing Hints
                Interrupt vector mode supported
                Device specific mode supported
                Steering table in MSI-X table
        Capabilities: [284 v1] Latency Tolerance Reporting
                Max snoop latency: 0ns
                Max no snoop latency: 0ns
        Capabilities: [28c v1] Vendor Specific Information: ID=0002 Rev=3 Len=100 <?>
        Capabilities: [38c v1] Vendor Specific Information: ID=0001 Rev=1 Len=038 <?>
        Capabilities: [3c4 v1] #1f
        Capabilities: [3d0 v1] Vendor Specific Information: ID=0003 Rev=1 Len=054 <?>
        Capabilities: [424 v1] #15
        Kernel driver in use: qede
```

从上面信息看到，qlogic driver，被kernel加载使用的叫qede

## 查看qede版本

```
root@node150:~# lsmod | grep qede
qede                  143360  0 
qed                   880640  1 qede
vxlan                  40960  2 i40e,qede
ptp                    20480  2 i40e,qede
root@node150:~# modinfo qede
filename:       /lib/modules/4.1.49-server/updates/dkms/qede.ko
version:        8.33.9.0
license:        GPL
description:    QLogic FastLinQ 4xxxx Ethernet Driver
srcversion:     AFABFD8F281A74624107FE7
alias:          pci:v00001077d00008090sv*sd*bc*sc*i*
alias:          pci:v00001077d00008070sv*sd*bc*sc*i*
alias:          pci:v00001077d00001664sv*sd*bc*sc*i*
alias:          pci:v00001077d00001656sv*sd*bc*sc*i*
alias:          pci:v00001077d00001654sv*sd*bc*sc*i*
alias:          pci:v00001077d00001644sv*sd*bc*sc*i*
alias:          pci:v00001077d00001636sv*sd*bc*sc*i*
alias:          pci:v00001077d00001666sv*sd*bc*sc*i*
alias:          pci:v00001077d00001634sv*sd*bc*sc*i*
depends:        ptp,vxlan,qed
vermagic:       4.1.49-server SMP mod_unload modversions 
parm:           debug: Default debug msglevel (uint)
parm:           int_mode: Force interrupt mode other than MSI-X:(1 INT#x; 2 MSI) (uint)
parm:           gro_disable: Force HW gro disable:(0 enable (default); 1 disable) (uint)
parm:           err_flags_override: Bitmap for disabling or forcing the actions taken according to the respective error flags bits (uint)
parm:           rdma_lag_support: RDMA Bonding support enable - preview mode (uint)
root@node150:~# 
```

从lsmod吐出信息可以看到，当前系统中QLogic driver版本是8.33.9.0，高于技嘉工程师提供的版本，所有不需要跟新


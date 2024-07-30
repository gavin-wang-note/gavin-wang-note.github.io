---
layout:     post
title:      "因存在多文件系统导致OSD启用失败"
subtitle:   "OSD mount failed by many filesystems"
date:       2020-08-31
author:     "Gavin Wang"
catalog:    true
categories:
    - [ceph]
tags:
    - ceph
---

# 概述

今天在创建OSD并启用它的时候，出现了如下一个错误:

```shell
[2020-08-31 10:23:32,948] [ERROR] [2163] [ezs3.storage_volume] [enable:816] enable osd fail
Traceback (most recent call last):
  File "/usr/lib/python2.7/dist-packages/ezs3/storage_volume.py", line 803, in enable
    self.mount(True)
  File "/usr/lib/python2.7/dist-packages/ezs3/storage_volume.py", line 1284, in mount
    options + data_dev_options)
  File "/usr/lib/python2.7/dist-packages/ezs3/storage_volume.py", line 257, in mount
    ','.join(options), fstab_path, mountpoint))
  File "/usr/lib/python2.7/dist-packages/ezs3/remote.py", line 201, in callable
    return func(*args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/ezs3/command.py", line 140, in do_cmd
    raise DoCommandError(err, p.returncode, output, cmdstr)
DoCommandError: DoCommandError: errno 1 stdout '' stderr 'mount: /dev/mapper/g-osd-2: more filesystems detected. This should not happen,
       use -t <type> to explicitly specify the filesystem type or
       use wipefs(8) to clean up the device.
' cmd 'mount -o noauto,nodelalloc,nomtime,noatime,journal_path=/dev/mapper/g-osd-2-ext4j /dev/mapper/g-osd-2 /data/osd.8'
[2020-08-31 10:23:32,949] [ERROR] [2163] [ezs3.node_management] [enable:1115] enable storage volume g-osd-2 osd 8 failed
Traceback (most recent call last):
  File "/usr/lib/python2.7/dist-packages/ezs3/node_management.py", line 1106, in enable
    osd_id = sv.enable(sip, cip, osd_id)
  File "/usr/lib/python2.7/dist-packages/ezs3/storage_volume.py", line 817, in enable
    raise e
DoCommandError: DoCommandError: errno 1 stdout '' stderr 'mount: /dev/mapper/g-osd-2: more filesystems detected. This should not happen,
       use -t <type> to explicitly specify the filesystem type or
       use wipefs(8) to clean up the device.
' cmd 'mount -o noauto,nodelalloc,nomtime,noatime,journal_path=/dev/mapper/g-osd-2-ext4j /dev/mapper/g-osd-2 /data/osd.8'
```

# 解决思路

看到这个错误的时候，直接使用了sgdisk -Z /dev/sdX 抹掉分区，回头尝试，还是同样的错误信息， 回想之前做的操作，分区有被用来做ZFS类型的OSD,会不会是它导致的?

使用wipefs指令，查看文件系统信息:

```shell
root@pytest-80-12:~# wipefs /dev/sdg2
offset               type
----------------------------------------------------------------
0x1ffe6c800          zfs_member   [raid]
                     LABEL: pytest_advance_osd_lba
                     UUID:  8560903119562917028

0x438                ext4   [filesystem]
                     UUID:  01c5f798-2e00-4527-ae90-c5442d0f8f6e

root@pytest-80-12:~# wipefs /dev/sdf2
offset               type
----------------------------------------------------------------
0x1ffe7fc00          zfs_member   [raid]
                     LABEL: pytest_edit_osd_hkq
                     UUID:  6743149755630861260

0x438                ext4   [filesystem]
                     UUID:  146c1897-efe8-4f9e-b05c-391601dc33fd
```

果然，这里显示同一个分区，有两个文件系统类型，一个是zfs_member，后面的[raid]表示是software raid，的确是之前使用过这个分区做过OSD;后面还有一个ext4的文件系统类型，两个文件系统类型并存，导致mount时候失败了。


# 解决方法

只用wipefs -a -f /dev/sdX来抹掉信息即可，有时候可能要抹掉多次，参考如下：


```shell
root@host248:/dev# wipefs /dev/sdc1
offset               type
----------------------------------------------------------------
0x574dfe70000        zfs_member   [raid]
                     LABEL: softraid
                     UUID:  13987007202510144699

root@host248:/dev# wipefs /dev/sdc1 |grep zfs_member | awk '{{print $1}}' | xargs -I{} wipefs -o {} /dev/sdc1
/dev/sdc1: 8 bytes were erased at offset 0x574dfe70000 (zfs_member): 0c b1 ba 00 00 00 00 00
root@host248:/dev# wipefs /dev/sdc1 |grep zfs_member | awk '{{print $1}}' | xargs -I{} wipefs -o {} /dev/sdc1
/dev/sdc1: 8 bytes were erased at offset 0x574dfe6d000 (zfs_member): 0c b1 ba 00 00 00 00 00
root@host248:/dev# wipefs /dev/sdc1 |grep zfs_member | awk '{{print $1}}' | xargs -I{} wipefs -o {} /dev/sdc1
/dev/sdc1: 8 bytes were erased at offset 0x574dfe6c000 (zfs_member): 0c b1 ba 00 00 00 00 00
root@host248:/dev# wipefs /dev/sdc1 |grep zfs_member | awk '{{print $1}}' | xargs -I{} wipefs -o {} /dev/sdc1
/dev/sdc1: 8 bytes were erased at offset 0x574dfe6b000 (zfs_member): 0c b1 ba 00 00 00 00 00
root@host248:/dev# wipefs /dev/sdc1 |grep zfs_member | awk '{{print $1}}' | xargs -I{} wipefs -o {} /dev/sdc1
/dev/sdc1: 8 bytes were erased at offset 0x574dfe6a000 (zfs_member): 0c b1 ba 00 00 00 00 00
root@host248:/dev# wipefs /dev/sdc1 |grep zfs_member | awk '{{print $1}}' | xargs -I{} wipefs -o {} /dev/sdc1
/dev/sdc1: 8 bytes were erased at offset 0x574dfe69000 (zfs_member): 0c b1 ba 00 00 00 00 00
root@host248:/dev# wipefs /dev/sdc1 |grep zfs_member | awk '{{print $1}}' | xargs -I{} wipefs -o {} /dev/sdc1
/dev/sdc1: 8 bytes were erased at offset 0x574dfe68000 (zfs_member): 0c b1 ba 00 00 00 00 00
root@host248:/dev# wipefs /dev/sdc1 |grep zfs_member | awk '{{print $1}}' | xargs -I{} wipefs -o {} /dev/sdc1
/dev/sdc1: 8 bytes were erased at offset 0x574dfea6000 (zfs_member): 0c b1 ba 00 00 00 00 00
root@host248:/dev# wipefs /dev/sdc1 |grep zfs_member | awk '{{print $1}}' | xargs -I{} wipefs -o {} /dev/sdc1
/dev/sdc1: 8 bytes were erased at offset 0x574dfea5000 (zfs_member): 0c b1 ba 00 00 00 00 00
root@host248:/dev# wipefs /dev/sdc1 |grep zfs_member | awk '{{print $1}}' | xargs -I{} wipefs -o {} /dev/sdc1
/dev/sdc1: 8 bytes were erased at offset 0x574dfea4000 (zfs_member): 0c b1 ba 00 00 00 00 00
root@host248:/dev# wipefs /dev/sdc1 |grep zfs_member | awk '{{print $1}}' | xargs -I{} wipefs -o {} /dev/sdc1
root@host248:/dev# wipefs /dev/sdc1 |grep zfs_member | awk '{{print $1}}' | xargs -I{} wipefs -o {} /dev/sdc1
root@host248:/dev# wipefs /dev/sdc1
root@host248:/dev#
```

# 参考文档

```shell
https://bbs.archlinux.org/viewtopic.php?id=202587
https://wiki2.xbits.net:4430/hardware:lsi:wipefs%E6%B8%85%E9%99%A4raid%E4%BF%A1%E6%81%AF
```


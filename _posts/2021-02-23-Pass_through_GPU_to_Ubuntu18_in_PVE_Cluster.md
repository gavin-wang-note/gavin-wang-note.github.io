---
layout:     post
title:      "PVE集群给Ubuntu18.04直通GPU"
subtitle:   "Pass through GPU in PVE clusteri to Ubuntu18.04 VM"
date:       2021-02-23
author:     "Gavin"
catalog:    true
tags:
    - Linux
    - PVE
    - GPU
    - Pass through
---



# 配置修改



## ConvergerOne侧配置修改



### Step1 修改/etc/default/grub

 

`vi /etc/default/grub`

 

在 quiet后面，增加“**intel_iommu=on video=efifb:off,vesafb:off**”，完整内容如下所示：

```
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on video=efifb:off,vesafb:off 915.modeset=0 nomodeset net.ifnames=1 biosdevname=0"

GRUB_CMDLINE_LINUX="video=VGA-1:800x600"

GRUB_GFXMODE=800x600

GRUB_GFXPAYLOAD_LINUX=keep
```



说明：

1. iommu开启直通分组
2. efifb:off 禁用efi启动的显示设备
3. vesafb:off 禁用legacy启动的显示设备



保存后，执行如下指令更新grub：

```
update-grub
```



### Step 2 加载模块



编辑 /etc/modules，直接添加以下几个模块：

```
vfio
vfio_iommu_type1
vfio_pci
vfio_virqfd
```





### Step 3 阻止驱动加载


因为ConvergetOne启动时会尝试加载显卡驱动，为了避免pve占用显卡，需要阻止pve的显卡驱动加载。



#### 3.1 添加驱动黑名单



编辑/etc/modprobe.d/pve-blacklist.conf

vi /etc/modprobe.d/pve-blacklist.conf 

添加以下内容

```
# block AMD driver

blacklist radeon
blacklist amdgpu

# block NVIDIA driver

blacklist nouveau
blacklist nvidia
blacklist nvidiafb

# block INTEL driver

blacklist snd_hda_intel
blacklist snd_hda_codec_hdmi
blacklist i915
```



编辑/etc/modprobe.d/blacklist.conf，执行如下指令，增加blacklist



```
  echo "blacklist radeon" >> /etc/modprobe.d/blacklist.conf 
  echo "blacklist nouveau" >> /etc/modprobe.d/blacklist.conf 
  echo "blacklist nvidia" >> /etc/modprobe.d/blacklist.conf
```





#### 3.2 添加显卡到直通设备中



查看所有pci设备。

```
lspci
```

由于我们已经知道了当前设备用的是什么型号的GPU卡，这里直接过滤：

```
root@gpu01:~# lspci |grep -i Tesla
02:00.0 3D controller: NVIDIA Corporation GP102GL [Tesla P40] (rev a1)
root@gpu01:~# 
```

找到了前面的硬件id（上面显示的是**02:00**），获取核心显卡的硬件id：



```
root@gpu01:~# lspci -n -s 02:00
02:00.0 0302: 10de:1b38 (rev a1)
root@gpu01:~# 
```



找到显卡后记下硬件id，形式是`xxxx:xxxx`，比如上面的Tesla P40的核心显卡的硬件id是**`10de:1b38`**。
编辑`/etc/modprobe.d/vfio.conf`

```
vi /etc/modprobe.d/vfio.conf
```

添加以下内容注意！把**10de:1b38**换成你的显卡的硬件id：

```
echo "options vfio-pci ids=10de:1b38 disable_vga=1" > /etc/modprobe.d/vfio.conf
```

然后查看内容是否正确：

```
root@gpu01:~# cat /etc/modprobe.d/vfio.conf
options vfio-pci ids=10de:1b38 disable_vga=1
root@gpu01:~# 
```



最后执行`update-initramfs -u` 生效配置。



### Step 4 重启机器



重启ConvergerOne宿主机。



### Step 5 安装虚机



等待ConvergerOne宿主机重启好，集群恢复健康后，创建Ubuntu18.04的vm，配置参考如下：

<p><img class="shadow" src="/img/in-post/pve/image-20210223153926661.png" width="1200" /></p>

此时是VM是没有直通GPU设备的。



# VM侧配置修改



VM OS成功 安装后进行配置文件的修改操作（以下操作以root用户进行修改）。



#### 编辑 /etc/modprobe.d/kvm.conf



```
echo "options kvm ignore_msrs=1 report_ignored_msrs=0" > /etc/modprobe.d/kvm.conf
```





# 安装驱动前准备工作



## 禁用Nouveau驱动



### 编辑黑名单

```
vi /etc/modprobe.d/blacklist-nouveau.conf
```



添加两行语句：

```
blacklist nouveau
options nouveau modeset=0
```



### 更新initramfs

```
update-initramfs -u
```



输出信息参考如下：



```
root@vmgpu:~# update-initramfs -u
update-initramfs: Generating /boot/initrd.img-4.15.0-55-generic
root@vmgpu:~# 
```



### 重启 VM

```
reboot
```



### 验证



终端执行如下指令：

```
lsmod | grep nouveau
```

如果没有结果表示禁用成功。



## 安装gcc&make



由于安装NVIDIA driver需要7.4版本的gcc和make指令，需进行gcc与make的安装。

```
apt-get update
apt-get install gcc 7.4.0
apt-get install make
```



## VM增加GPU PCI-e设备



将VM关机，并增加GPU设备：


<p><img class="shadow" src="/img/in-post/pve/image-20210223160023098.png" width="1200" /></p>

<p><img class="shadow" src="/img/in-post/pve/image-20210223160848107.png" width="1200" /></p>



完整的UI展示VM信息参考如下：

<p><img class="shadow" src="/img/in-post/pve/image-20210223180038078.png" width="1200" /></p>



注意：

1、不要勾选主GPU，否则VM启动报错：

```
/dev/rbd0
kvm: failed to find file '/usr/share/qemu-server/bootsplash.jpg'
kvm: -device vfio-pci,host=0000:02:00.0,id=hostpci0,bus=pci.0,addr=0x10,rombar=0,x-vga=on: vfio 0000:02:00.0: failed getting region info for VGA region index 8: Invalid argument
device does not support requested feature x-vga
TASK ERROR: start failed: command '/usr/bin/kvm -id 100 -name vm100 -chardev 'socket,id=qmp,path=/var/run/qemu-server/100.qmp,server,nowait' -mon 'chardev=qmp,mode=control' -chardev 'socket,id=qmp-event,path=/var/run/qmeventd.sock,reconnect=5' -mon 'chardev=qmp-event,mode=control' -pidfile /var/run/qemu-server/100.pid -daemonize -smbios 'type=1,uuid=6739feef-a51c-4ec4-b24f-e80cb402a832' -smp '8,sockets=2,cores=4,maxcpus=8' -nodefaults -boot 'menu=on,strict=on,reboot-timeout=1000,splash=/usr/share/qemu-server/bootsplash.jpg' -vga none -nographic -cpu 'kvm64,+lahf_lm,+sep,+kvm_pv_unhalt,+kvm_pv_eoi,enforce,kvm=off' -m 4096 -device 'pci-bridge,id=pci.1,chassis_nr=1,bus=pci.0,addr=0x1e' -device 'pci-bridge,id=pci.2,chassis_nr=2,bus=pci.0,addr=0x1f' -device 'vmgenid,guid=9ee6f244-c03d-4e0f-852e-3790f8d09adf' -device 'piix3-usb-uhci,id=uhci,bus=pci.0,addr=0x1.0x2' -device 'usb-tablet,id=tablet,bus=uhci.0,port=1' -device 'vfio-pci,host=0000:02:00.0,id=hostpci0,bus=pci.0,addr=0x10,rombar=0,x-vga=on' -device 'virtio-balloon-pci,id=balloon0,bus=pci.0,addr=0x3' -iscsi 'initiator-name=iqn.1993-08.org.debian:01:2ffe281c6e13' -device 'virtio-scsi-pci,id=scsihw0,bus=pci.0,addr=0x5' -drive 'file=/dev/rbd/rbd/vm-100-disk-0,if=none,id=drive-scsi0,discard=on,format=raw,cache=none,aio=native,detect-zeroes=unmap' -device 'scsi-hd,bus=scsihw0.0,channel=0,scsi-id=0,lun=0,drive=drive-scsi0,id=scsi0,bootindex=100' -netdev 'type=tap,id=net0,ifname=tap100i0,script=/var/lib/qemu-server/pve-bridge,downscript=/var/lib/qemu-server/pve-bridgedown,vhost=on' -device 'virtio-net-pci,mac=B6:5F:BC:F0:3D:9F,netdev=net0,bus=pci.0,addr=0x12,id=net0,bootindex=300' -machine 'type=pc+pve1'' failed: exit code 1
```



2、 不要勾选PCIE-Express选择，否则VM启动报错：


<p><img class="shadow" src="/img/in-post/pve/image-20210223161023563.png" width="1200" /></p>



# 安装驱动



事先准备好NVIDIA的driver，本文以  **NVIDIA-Linux-x86_64-460.32.03.run** 示例。



```
root@vmgpu:~# chmod a+x NVIDIA-Linux-x86_64-460.32.03.run 
root@vmgpu:~# ./NVIDIA-Linux-x86_64-460.32.03.run 
```



安装过程记录如下：



忽略gcc版本告警：

<p><img class="shadow" src="/img/in-post/pve/image-20210223161702180.png" width="1200" /></p>

<p><img class="shadow" src="/img/in-post/pve/image-20210223161729108.png" width="1200" /></p>



开始Build kernel modules：

<p><img class="shadow" src="/img/in-post/pve/image-20210223161755290.png" width="1200" /></p>



出现了warning，直接一路回车就好：

<p><img class="shadow" src="/img/in-post/pve/image-20210223161825771.png" width="1200" /></p>

<p><img class="shadow" src="/img/in-post/pve/image-20210223161834580.png" width="1200" /></p>


install NVIDIA Accolerated Graphics Driver：

<p><img class="shadow" src="/img/in-post/pve/image-20210223161846564.png" width="1200" /></p>



提示安装成功：

<p><img class="shadow" src="/img/in-post/pve/image-20210223161930679.png" width="1200" /></p>


重启VM，检查驱动是否被成功安装：



```
root@vmgpu:~# lsmod | grep nvidia
nvidia_drm             49152  0
nvidia_modeset       1220608  1 nvidia_drm
nvidia              33988608  1 nvidia_modeset
drm_kms_helper        167936  1 nvidia_drm
drm                   401408  3 drm_kms_helper,nvidia_drm
root@vmgpu:~# 
```





```
root@vmgpu:~# nvidia-smi 
Tue Feb 23 16:40:19 2021       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 460.32.03    Driver Version: 460.32.03    CUDA Version: 11.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla P40           Off  | 00000000:00:10.0 Off |                    0 |
| N/A   28C    P0    50W / 250W |      0MiB / 22919MiB |      3%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```



如下图所示：

<p><img class="shadow" src="/img/in-post/pve/image-20210223162330661.png" width="1200" /></p>


出现如上信息，表明成功安装了驱动。



# 其他信息



## 不支援BISO类型为OVMF下GPU的直通

更改VM BIOS 类型为OVMF，支持q35，如下图所示：

<p><img class="shadow" src="/img/in-post/pve/image-20210223173032251.png" width="1200" /></p>



按照上面的部署步骤安装NVIDIA-Linux-x86_64-460.32.03.run：



<p><img class="shadow" src="/img/in-post/pve/image-20210223173124492.png" width="1200" /></p>



对应log内容：

```
   /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-drm/nvidia-drm-modeset.c: In function '__will_generate_flip_event':
   /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-drm/nvidia-drm-modeset.c:96:23: warning: unused variable 'primary_plane' [-Wunused-variable]
        struct drm_plane *primary_plane = crtc->primary;
                          ^~~~~~~~~~~~~
     CC [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-drm/nvidia-drm-helper.o
     CC [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-drm/nv-pci-table.o
     CC [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-drm/nvidia-drm-gem-nvkms-memory.o
     CC [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-drm/nvidia-drm-gem-user-memory.o
     CC [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-drm/nvidia-drm-gem-dma-buf.o
     CC [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-drm/nvidia-drm-format.o
   ld -r -o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-interface.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-frontend.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-pci.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-acpi.o /tmp/selfgz19048/NVIDIA-Linux-x86_
   64-460.32.03/kernel/nvidia/nv-cray.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-dma.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-i2c.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-mmap.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-p2p.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-pat.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-procfs.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-usermap.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-vm.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-vtophys.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/os-interface.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/os-mlock.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/os-pci.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/os-registry.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel
   /nvidia/os-usermap.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-modeset-interface.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-pci-table.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-kthread-q.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-memdbg.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-ibmnpu.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-report-err.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-rsync.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-msi.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv-caps.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nv_uvm_interface.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nvlink_linux.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/nvlink_caps.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia/linux_nvswitch.o /tmp/selfgz19048/NVIDI
   A-Linux-x86_64-460.32.03/kernel/nvidia/procfs_nvswitch.o
   ld -r -o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-modeset/nv-modeset-interface.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-modeset/nvidia-modeset-linux.o /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-modeset/nv-kthread-q.o
     LD [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia.o
     LD [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-uvm.o
     LD [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-modeset.o
     LD [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-drm.o
     Building modules, stage 2.
     MODPOST 4 modules
     CC      /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-drm.mod.o
     CC      /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-modeset.mod.o
     CC      /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-uvm.mod.o
     CC      /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia.mod.o
     LD [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-drm.ko
     LD [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia.ko
     LD [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-uvm.ko
     LD [M]  /tmp/selfgz19048/NVIDIA-Linux-x86_64-460.32.03/kernel/nvidia-modeset.ko
   make[1]: Leaving directory '/usr/src/linux-headers-4.15.0-55-generic'
-> done.
-> Kernel module compilation complete.
-> Unable to determine if Secure Boot is enabled: No such file or directory
```



## GPU卡供电不足导致成功安装驱动后无法使用GPU卡



对应VM kern.log片断信息如下：

```
Feb 23 08:23:46 gpu01 kernel: [   12.954627] [drm] [nvidia-drm] [GPU ID 0x00000010] Loading driver
Feb 23 08:23:46 gpu01 kernel: [   12.954628] [drm] Initialized nvidia-drm 0.0.0 20160202 for 0000:00:10.0 on minor 1
Feb 23 08:23:46 gpu01 kernel: [   13.025196] EXT4-fs (sda2): mounted filesystem with ordered data mode. Opts: (null)
Feb 23 08:23:46 gpu01 kernel: [   13.111410] audit: type=1400 audit(1614068624.068:2): apparmor="STATUS" operation="profile_load" profile="unconfined" name="/usr/bin/lxc-start" pid=735 comm="apparmor_parser"
Feb 23 08:23:46 gpu01 kernel: [   13.112890] audit: type=1400 audit(1614068624.072:3): apparmor="STATUS" operation="profile_load" profile="unconfined" name="/usr/bin/man" pid=736 comm="apparmor_parser"
Feb 23 08:23:46 gpu01 kernel: [   13.112893] audit: type=1400 audit(1614068624.072:4): apparmor="STATUS" operation="profile_load" profile="unconfined" name="man_filter" pid=736 comm="apparmor_parser"
Feb 23 08:23:46 gpu01 kernel: [   13.112895] audit: type=1400 audit(1614068624.072:5): apparmor="STATUS" operation="profile_load" profile="unconfined" name="man_groff" pid=736 comm="apparmor_parser"
Feb 23 08:23:46 gpu01 kernel: [   13.113310] audit: type=1400 audit(1614068624.072:6): apparmor="STATUS" operation="profile_load" profile="unconfined" name="/usr/lib/snapd/snap-confine" pid=737 comm="apparmor_parser"
Feb 23 08:23:46 gpu01 kernel: [   13.113312] audit: type=1400 audit(1614068624.072:7): apparmor="STATUS" operation="profile_load" profile="unconfined" name="/usr/lib/snapd/snap-confine//mount-namespace-capture-helper" pid=737 comm="apparmor_parser"
Feb 23 08:23:46 gpu01 kernel: [   13.114956] audit: type=1400 audit(1614068624.072:8): apparmor="STATUS" operation="profile_load" profile="unconfined" name="/usr/sbin/tcpdump" pid=739 comm="apparmor_parser"
Feb 23 08:23:46 gpu01 kernel: [   13.116269] audit: type=1400 audit(1614068624.080:9): apparmor="STATUS" operation="profile_load" profile="unconfined" name="lxc-container-default" pid=733 comm="apparmor_parser"
Feb 23 08:23:46 gpu01 kernel: [   13.116272] audit: type=1400 audit(1614068624.080:10): apparmor="STATUS" operation="profile_load" profile="unconfined" name="lxc-container-default-cgns" pid=733 comm="apparmor_parser"
Feb 23 08:23:46 gpu01 kernel: [   13.116277] audit: type=1400 audit(1614068624.080:11): apparmor="STATUS" operation="profile_load" profile="unconfined" name="lxc-container-default-with-mounting" pid=733 comm="apparmor_parser"
Feb 23 08:23:46 gpu01 kernel: [   15.853079] new mount options do not match the existing superblock, will be ignored
Feb 23 08:24:46 gpu01 kernel: [   77.010198] random: crng init done
Feb 23 08:24:46 gpu01 kernel: [   77.010218] random: 7 urandom warning(s) missed due to ratelimiting
Feb 23 08:25:00 gpu01 kernel: [   90.796257] NVRM: GPU 0000:00:10.0: GPU does not have the necessary power cables connected.
Feb 23 08:25:00 gpu01 kernel: [   90.825600] NVRM: GPU 0000:00:10.0: RmInitAdapter failed! (0x25:0x1c:1262)
Feb 23 08:25:00 gpu01 kernel: [   90.825801] NVRM: GPU 0000:00:10.0: rm_init_adapter failed, device minor number 0
Feb 23 08:25:00 gpu01 kernel: [   91.062551] NVRM: GPU 0000:00:10.0: GPU does not have the necessary power cables connected.
Feb 23 08:25:00 gpu01 kernel: [   91.092368] NVRM: GPU 0000:00:10.0: RmInitAdapter failed! (0x25:0x1c:1262)
Feb 23 08:25:00 gpu01 kernel: [   91.092560] NVRM: GPU 0000:00:10.0: rm_init_adapter failed, device minor number 0
Feb 23 08:25:15 gpu01 kernel: [  105.451286] NVRM: GPU 0000:00:10.0: GPU does not have the necessary power cables connected.
Feb 23 08:25:15 gpu01 kernel: [  105.451804] NVRM: GPU 0000:00:10.0: RmInitAdapter failed! (0x25:0x1c:1262)
Feb 23 08:25:15 gpu01 kernel: [  105.452011] NVRM: GPU 0000:00:10.0: rm_init_adapter failed, device minor number 0
Feb 23 08:25:15 gpu01 kernel: [  105.718690] NVRM: GPU 0000:00:10.0: GPU does not have the necessary power cables connected.
Feb 23 08:25:15 gpu01 kernel: [  105.719179] NVRM: GPU 0000:00:10.0: RmInitAdapter failed! (0x25:0x1c:1262)
Feb 23 08:25:15 gpu01 kernel: [  105.719362] NVRM: GPU 0000:00:10.0: rm_init_adapter failed, device minor number 0
```



解决方法：

   拆机箱，将Tesla P40这块GPU的两根电源线都接上，之前是只接了一根电源线。


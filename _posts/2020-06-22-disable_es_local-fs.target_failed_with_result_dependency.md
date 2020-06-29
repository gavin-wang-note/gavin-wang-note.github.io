---
layout:     post
title:      "频繁启用&停用ES服务，出现local-fs.target failed with result dependency"
subtitle:   "Loop enable&disable ES service occure 'local-fs.target failed with result dependency'"
date:       2020-06-22
author:     "Gavin"
catalog:    true
tags:
    - python
    - elasticsearch
---


# 概述

Ubuntu16.04，产品新增了Elasticsearch功能，在测试ES服务启用过程冲，选择240G 的Intel S4510 型号的SSD一块作为ES的data：

```
Model Family:     Intel S4510/S4610/S4500/S4600 Series SSDs
Device Model:     INTEL SSDSC2KG240G8
```

在频繁测试ES服务启&停过程中，发现有个node上的众多服务接收到终止信号(15),而且复现几率非常的高,此时ipmi console出现如下信息：


<img class="shadow" src="/img/in-post/emergency_mode.png" width="1200">


执行systemctl \-\-failed，信息如下：


<img class="shadow" src="/img/in-post/systemctl_failed.png" width="1200">



使用 'journalctl -xb'，dump的信息中，未找到问题发生的原因，只有类似如下的片断信息：

```
Jun 19 18:20:17 node76 kernel: ata2.00: Enabling discard_zeroes_data
Jun 19 18:20:17 node76 multipath[829224]: sdf: using deprecated getuid callout
Jun 19 18:20:18 node76 kernel: ata2.00: Enabling discard_zeroes_data
Jun 19 18:20:18 node76 kernel:  sdf: sdf1
Jun 19 18:20:18 node76 multipath[829250]: sdf: using deprecated getuid callout
Jun 19 18:20:19 node76 multipath[829286]: sdf: using deprecated getuid callout
Jun 19 18:20:19 node76 sshd[829305]: Accepted publickey for root from 10.10.10.75 port 53688 ssh2: RSA SHA256:5/ngrgVfOOOLNuPyS1dflwHrc/sN9BSgDxNHVmJA0UE
Jun 19 18:20:19 node76 sshd[829305]: pam_unix(sshd:session): session opened for user root by (uid=0)
Jun 19 18:20:19 node76 systemd-logind[1841]: New session 3065 of user root.
-- Subject: A new session 3065 has been created for user root
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- Documentation: http://www.freedesktop.org/wiki/Software/systemd/multiseat
--
-- A new session with the ID 3065 has been created for the user root.
--
-- The leading process of the session is 829305.
Jun 19 18:20:19 node76 systemd[1]: Started Session 3065 of user root.
-- Subject: Unit session-3065.scope has finished start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
--
-- Unit session-3065.scope has finished starting up.
--
-- The start-up result is done.
Jun 19 18:20:19 node76 multipath[829322]: sdf: using deprecated getuid callout
Jun 19 18:20:19 node76 sshd[829305]: Received disconnect from 10.10.10.75 port 53688:11: disconnected by user
Jun 19 18:20:19 node76 sshd[829305]: Disconnected from 10.10.10.75 port 53688
Jun 19 18:20:19 node76 sshd[829305]: pam_unix(sshd:session): session closed for user root
Jun 19 18:20:19 node76 systemd-logind[1841]: Removed session 3065.
-- Subject: Session 3065 has been terminated
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- Documentation: http://www.freedesktop.org/wiki/Software/systemd/multiseat
--
-- A session with the ID 3065 has been terminated.
Jun 19 18:20:19 node76 kernel: ata2.00: Enabling discard_zeroes_data
Jun 19 18:20:19 node76 sshd[829336]: Accepted publickey for root from 10.10.10.75 port 53694 ssh2: RSA SHA256:5/ngrgVfOOOLNuPyS1dflwHrc/sN9BSgDxNHVmJA0UE
Jun 19 18:20:19 node76 sshd[829336]: pam_unix(sshd:session): session opened for user root by (uid=0)
Jun 19 18:20:19 node76 kernel:  sdf: sdf1
Jun 19 18:20:19 node76 systemd-logind[1841]: New session 3066 of user root.
-- Subject: A new session 3066 has been created for user root
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- Documentation: http://www.freedesktop.org/wiki/Software/systemd/multiseat
--
-- A new session with the ID 3066 has been created for the user root.
--
-- The leading process of the session is 829336.
Jun 19 18:20:19 node76 systemd[1]: Started Session 3066 of user root.
-- Subject: Unit session-3066.scope has finished start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
--
-- Unit session-3066.scope has finished starting up.
--
-- The start-up result is done.
Jun 19 18:20:19 node76 multipath[829356]: sdf: using deprecated getuid callout
Jun 19 18:20:19 node76 sshd[829336]: Received disconnect from 10.10.10.75 port 53694:11: disconnected by user
Jun 19 18:20:19 node76 sshd[829336]: Disconnected from 10.10.10.75 port 53694
Jun 19 18:20:19 node76 sshd[829336]: pam_unix(sshd:session): session closed for user root
Jun 19 18:20:19 node76 systemd-logind[1841]: Removed session 3066.
-- Subject: Session 3066 has been terminated
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- Documentation: http://www.freedesktop.org/wiki/Software/systemd/multiseat
--
-- A session with the ID 3066 has been terminated.
Jun 19 18:20:20 node76 sshd[829382]: Accepted publickey for root from 10.10.10.75 port 53696 ssh2: RSA SHA256:5/ngrgVfOOOLNuPyS1dflwHrc/sN9BSgDxNHVmJA0UE
Jun 19 18:20:20 node76 sshd[829382]: pam_unix(sshd:session): session opened for user root by (uid=0)
Jun 19 18:20:20 node76 systemd-logind[1841]: New session 3067 of user root.
-- Subject: A new session 3067 has been created for user root
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- Documentation: http://www.freedesktop.org/wiki/Software/systemd/multiseat
--
-- A new session with the ID 3067 has been created for the user root.
--
-- The leading process of the session is 829382.
Jun 19 18:20:20 node76 systemd[1]: Started Session 3067 of user root.
-- Subject: Unit session-3067.scope has finished start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
--
-- Unit session-3067.scope has finished starting up.
--
-- The start-up result is done.
Jun 19 18:20:20 node76 sshd[829382]: Received disconnect from 10.10.10.75 port 53696:11: disconnected by user
Jun 19 18:20:20 node76 sshd[829382]: Disconnected from 10.10.10.75 port 53696
Jun 19 18:20:20 node76 sshd[829382]: pam_unix(sshd:session): session closed for user root
Jun 19 18:20:20 node76 systemd-logind[1841]: Removed session 3067.
-- Subject: Session 3067 has been terminated
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- Documentation: http://www.freedesktop.org/wiki/Software/systemd/multiseat
--
-- A session with the ID 3067 has been terminated.
Jun 19 18:20:20 node76 sshd[829415]: Accepted publickey for root from 10.10.10.75 port 53702 ssh2: RSA SHA256:5/ngrgVfOOOLNuPyS1dflwHrc/sN9BSgDxNHVmJA0UE
Jun 19 18:20:20 node76 sshd[829415]: pam_unix(sshd:session): session opened for user root by (uid=0)
Jun 19 18:20:20 node76 systemd-logind[1841]: New session 3068 of user root.
-- Subject: A new session 3068 has been created for user root
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- Documentation: http://www.freedesktop.org/wiki/Software/systemd/multiseat
--
-- A new session with the ID 3068 has been created for the user root.
--
-- The leading process of the session is 829415.
Jun 19 18:20:20 node76 systemd[1]: Started Session 3068 of user root.
-- Subject: Unit session-3068.scope has finished start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
--
-- Unit session-3068.scope has finished starting up.
--
-- The start-up result is done.
Jun 19 18:20:20 node76 kernel: ata2.00: Enabling discard_zeroes_data
Jun 19 18:20:20 node76 kernel:  sdf: sdf1
Jun 19 18:20:20 node76 kernel: ata2.00: Enabling discard_zeroes_data
Jun 19 18:20:20 node76 kernel:  sdf:
Jun 19 18:20:20 node76 multipath[829431]: sdf: using deprecated getuid callout
Jun 19 18:20:20 node76 sshd[829415]: Received disconnect from 10.10.10.75 port 53702:11: disconnected by user
Jun 19 18:20:20 node76 sshd[829415]: Disconnected from 10.10.10.75 port 53702
Jun 19 18:20:20 node76 sshd[829415]: pam_unix(sshd:session): session closed for user root
Jun 19 18:20:20 node76 systemd-logind[1841]: Removed session 3068.
-- Subject: Session 3068 has been terminated
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- Documentation: http://www.freedesktop.org/wiki/Software/systemd/multiseat
--
-- A session with the ID 3068 has been terminated.
Jun 19 18:20:21 node76 systemd-udevd[829425]: inotify_add_watch(9, /dev/sdf1, 10) failed: No such file or directory
Jun 19 18:20:21 node76 multipath[829479]: sdf: using deprecated getuid callout
Jun 19 18:20:21 node76 multipath[829507]: sdf: using deprecated getuid callout
Jun 19 18:20:21 node76 kernel: ata2.00: Enabling discard_zeroes_data
Jun 19 18:20:21 node76 kernel:  sdf:
Jun 19 18:20:21 node76 multipath[829550]: sdf: using deprecated getuid callout
Jun 19 18:20:22 node76 kernel: ata2.00: Enabling discard_zeroes_data
Jun 19 18:20:22 node76 kernel:  sdf:
Jun 19 18:20:22 node76 multipath[829590]: sdf: using deprecated getuid callout
Jun 19 18:20:22 node76 multipath[829616]: sdf: using deprecated getuid callout
Jun 19 18:20:23 node76 kernel: ata2.00: Enabling discard_zeroes_data
Jun 19 18:20:23 node76 kernel: ata2.00: Enabling discard_zeroes_data
Jun 19 18:20:23 node76 kernel: ata2.00: Enabling discard_zeroes_data
Jun 19 18:20:23 node76 multipath[829658]: sdf: using deprecated getuid callout
Jun 19 18:20:23 node76 multipath[829685]: sdf: using deprecated getuid callout

..............................此处省略一部分信息......................................

Jun 19 18:22:48 node76 systemd[1]: Started Session 3077 of user root.
-- Subject: Unit session-3077.scope has finished start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
--
-- Unit session-3077.scope has finished starting up.
--
-- The start-up result is done.
Jun 19 18:22:59 node76 sshd[844776]: Accepted publickey for root from 10.16.172.75 port 41614 ssh2: RSA SHA256:5/ngrgVfOOOLNuPyS1dflwHrc/sN9BSgDxNHVmJA0UE
Jun 19 18:22:59 node76 sshd[844776]: pam_unix(sshd:session): session opened for user root by (uid=0)
Jun 19 18:22:59 node76 systemd-logind[1841]: New session 3078 of user root.
-- Subject: A new session 3078 has been created for user root
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- Documentation: http://www.freedesktop.org/wiki/Software/systemd/multiseat
--
-- A new session with the ID 3078 has been created for the user root.
--
-- The leading process of the session is 844776.
Jun 19 18:22:59 node76 systemd[1]: Started Session 3078 of user root.
-- Subject: Unit session-3078.scope has finished start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
--
-- Unit session-3078.scope has finished starting up.
--
-- The start-up result is done.
Jun 19 18:22:59 node76 radosgw[793492]: 2020-06-19 18:22:59.685447 7f3df412b700 -1 received  signal: Terminated from  PID: 1 task name: /sbin/init  UID: 0
Jun 19 18:22:59 node76 radosgw[793492]: 2020-06-19 18:22:59.685486 7f3e336e4040 -1 shutting down
Jun 19 18:22:59 node76 systemd[1]: Stopping Ceph rados gateway...
-- Subject: Unit ceph-radosgw@radosgw.0.service has begun shutting down
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
--
```


重新开机启动后，syslog日志片断如下:


```
Jun 18 18:19:35 node75 kernel: [174076.635228] ata2.00: Enabling discard_zeroes_data
Jun 18 18:19:35 node75 kernel: [174076.639312]  sdf:
Jun 18 18:19:35 node75 multipath: sdf: using deprecated getuid callout
Jun 18 18:19:35 node75 ntpd[3446]: Listen normally on 68 bond0 10.16.172.79:123
Jun 18 18:19:35 node75 ntpd[3446]: Listen normally on 69 bond0 10.16.172.80:123
Jun 18 18:19:35 node75 ntpd[3446]: new interface(s) found: waking up resolver
Jun 18 18:19:35 node75 systemd-udevd[149835]: inotify_add_watch(9, /dev/sdf1, 10) failed: No such file or directory
Jun 18 18:19:35 node75 systemd[1]: Mounting /opt/datasearch/0...
Jun 18 18:19:35 node75 mount[149927]: mount: special device /dev/disk/by-partlabel/datasearch0 does not exist
Jun 18 18:19:35 node75 systemd[1]: opt-datasearch-0.mount: Mount process exited, code=exited status=32
Jun 18 18:19:35 node75 systemd[1]: Failed to mount /opt/datasearch/0.
Jun 18 18:19:35 node75 systemd[1]: opt-datasearch-0.mount: Unit entered failed state.
Jun 18 18:19:35 node75 multipath: sdf: using deprecated getuid callout
Jun 18 18:19:36 node75 kernel: [174077.640278] ata2.00: Enabling discard_zeroes_data
Jun 18 18:19:36 node75 kernel: [174077.642668]  sdf:
Jun 18 18:19:37 node75 kernel: [174078.789459] ata2.00: Enabling discard_zeroes_data
Jun 18 18:19:37 node75 kernel: [174078.794294] ata2.00: Enabling discard_zeroes_data
Jun 18 18:19:37 node75 kernel: [174078.800320] ata2.00: Enabling discard_zeroes_data
Jun 18 18:19:38 node75 kernel: [174079.491352] ata2.00: Enabling discard_zeroes_data
Jun 18 18:19:38 node75 multipath: message repeated 5 times: [ sdf: using deprecated getuid callout]
Jun 18 18:19:40 node75 systemd[1]: Stopping ezs3 bucket logging agent service...
Jun 18 18:19:44 node75 systemd[1]: Stopped ezs3 bucket logging agent service.
Jun 18 18:19:44 node75 systemd[1]: Reloading.
Jun 18 18:19:44 node75 systemd[1]: Reloading.
Jun 18 18:19:44 node75 systemd[1]: Started ACPI event daemon.
Jun 18 18:19:44 node75 systemd[1]: Stopping Ceph rados gateway...
Jun 18 18:19:44 node75 radosgw[138955]: 2020-06-18 18:19:44.455571 7f349a88c700 -1 received  signal: Terminated from  PID: 1 task name: /sbin/init  UID: 0
Jun 18 18:19:44 node75 radosgw[138955]: 2020-06-18 18:19:44.455636 7f34d9e45040 -1 shutting down
Jun 18 18:19:44 node75 systemd[1]: Stopped Ceph rados gateway.
Jun 18 18:19:44 node75 systemd[1]: Reloading.
Jun 18 18:19:44 node75 systemd[1]: Reloading.
Jun 18 18:19:44 node75 systemd[1]: Started ACPI event daemon.
Jun 18 18:19:45 node75 radosgw[131963]: 2020-06-18 18:19:45.107577 7fcfdfa6a700 -1 received  signal: Terminated from  PID: 1 task name: /sbin/init  UID: 0
Jun 18 18:19:45 node75 radosgw[131963]: 2020-06-18 18:19:45.107620 7fd01f023040 -1 shutting down
Jun 18 18:19:45 node75 systemd[1]: Stopping Ceph rados gateway...
Jun 18 18:19:45 node75 systemd[1]: Stopped Ceph rados gateway.
Jun 18 18:19:45 node75 systemd[1]: Started Ceph rados gateway.
Jun 18 18:19:45 node75 systemd[1]: Reloading.
Jun 18 18:19:45 node75 systemd[1]: Reloading.
Jun 18 18:19:45 node75 systemd[1]: Started ACPI event daemon.
Jun 18 18:19:45 node75 systemd[1]: Stopped ezs3 bucket logging agent service.
Jun 18 18:19:45 node75 systemd[1]: Starting ezs3 bucket logging agent service...
Jun 18 18:19:45 node75 systemd[1]: Stopped ezs3 bucket logging agent service.
Jun 18 18:19:45 node75 systemd[1]: Starting ezs3 bucket logging agent service...
Jun 18 18:19:46 node75 systemd[1]: ezs3-bucket-logging-agent.service: Supervising process 152415 which is not our child. We'll most likely not notice when it exits.
Jun 18 18:19:46 node75 systemd[1]: Started ezs3 bucket logging agent service.
Jun 18 18:19:46 node75 systemd[1]: Reloading.
Jun 18 18:19:46 node75 systemd[1]: Reloading.
Jun 18 18:19:47 node75 systemd[1]: Started ACPI event daemon.
Jun 18 18:19:53 node75 Keepalived[149387]: Stopping
Jun 18 18:19:53 node75 Keepalived_vrrp[149388]: (VRRP0) sent 0 priority
Jun 18 18:19:53 node75 systemd[1]: Stopping Keepalive Daemon (LVS and VRRP)...
Jun 18 18:19:53 node75 avahi-daemon[1704]: Withdrawing address record for 10.16.172.80 on bond0.
Jun 18 18:19:53 node75 avahi-daemon[1704]: Withdrawing address record for 10.16.172.79 on bond0.
Jun 18 18:19:53 node75 Keepalived_vrrp[149388]: (DATASEARCH) sent 0 priority
Jun 18 18:19:54 node75 Keepalived_vrrp[149388]: Stopped
Jun 18 18:19:54 node75 Keepalived[149387]: Stopped Keepalived v2.0.10 (09/19,2019), git commit 6.0-rc1-9509-gb73d9e153
Jun 18 18:19:54 node75 systemd[1]: Stopped Keepalive Daemon (LVS and VRRP).
Jun 18 18:19:54 node75 systemd[1]: Started Keepalive Daemon (LVS and VRRP).
Jun 18 18:19:54 node75 Keepalived[154125]: Starting Keepalived v2.0.10 (09/19,2019), git commit 6.0-rc1-9509-gb73d9e153
Jun 18 18:19:54 node75 Keepalived[154125]: Running on Linux 4.14.148-server #1 SMP Thu Jun 11 18:49:19 CST 2020 (built for Linux 4.4.176)
Jun 18 18:19:54 node75 Keepalived[154125]: Command line: '/usr/sbin/keepalived' '--dont-fork'
Jun 18 18:19:54 node75 Keepalived[154125]: Opening file '/etc/keepalived/keepalived.conf'.
Jun 18 18:19:54 node75 Keepalived[154125]: Starting VRRP child process, pid=154126
Jun 18 18:19:54 node75 Keepalived_vrrp[154126]: Registering Kernel netlink reflector
Jun 18 18:19:54 node75 Keepalived_vrrp[154126]: Registering Kernel netlink command channel
Jun 18 18:19:54 node75 Keepalived_vrrp[154126]: Opening file '/etc/keepalived/keepalived.conf'.
Jun 18 18:19:54 node75 Keepalived_vrrp[154126]: Registering gratuitous ARP shared channel
Jun 18 18:19:54 node75 Keepalived_vrrp[154126]: (VRRP0) Entering BACKUP STATE (init)
Jun 18 18:19:55 node75 ntpd[3446]: Deleting interface #68 bond0, 10.16.172.79#123, interface stats: received=0, sent=0, dropped=0, active_time=20 secs
Jun 18 18:19:55 node75 ntpd[3446]: Deleting interface #69 bond0, 10.16.172.80#123, interface stats: received=0, sent=0, dropped=0, active_time=20 secs
Jun 18 18:19:56 node75 Keepalived_vrrp[154126]: (VRRP0) Entering MASTER STATE
Jun 18 18:19:56 node75 Keepalived_vrrp[154126]: (VRRP0) using locally configured advertisement interval (400 milli-sec)
Jun 18 18:19:56 node75 avahi-daemon[1704]: Registering new address record for 10.16.172.79 on bond0.IPv4.
Jun 18 18:19:57 node75 ntpd[3446]: Listen normally on 70 bond0 10.16.172.79:123
Jun 18 18:19:57 node75 ntpd[3446]: new interface(s) found: waking up resolver
Jun 18 18:20:01 node75 CRON[154717]: (root) CMD (bash /usr/local/bin/monitor_ctdb.sh >/dev/null 2>&1)
Jun 18 18:21:49 node75 systemd[1]: Started Session 3232 of user root.
Jun 18 18:22:01 node75 CRON[165327]: (root) CMD (bash /usr/local/bin/monitor_ctdb.sh >/dev/null 2>&1)
Jun 18 18:22:03 node75 systemd[1]: Stopping ezrpc service...
Jun 18 18:22:04 node75 systemd[1]: Started Session 3234 of user root.
Jun 18 18:22:05 node75 systemd[1]: Stopped ezrpc service.
Jun 18 18:22:05 node75 systemd[1]: Starting ezrpc service...
Jun 18 18:22:05 node75 systemd[1]: Started Session 3235 of user root.
Jun 18 18:22:05 node75 systemd[1]: Started Session 3236 of user root.
Jun 18 18:22:05 node75 systemd[1]: ezrpc.service: Supervising process 165656 which is not our child. We'll most likely not notice when it exits.
Jun 18 18:22:05 node75 systemd[1]: Started ezrpc service.
Jun 18 18:22:06 node75 systemd[1]: Started Session 3237 of user root.
Jun 18 18:22:07 node75 systemd[1]: Started Session 3238 of user root.
Jun 18 18:22:09 node75 systemd[1]: Started Session 3239 of user root.
Jun 18 18:22:10 node75 systemd[1]: Started Session 3240 of user root.
Jun 18 18:22:10 node75 systemd[1]: Started Session 3241 of user root.
Jun 18 18:22:10 node75 systemd[1]: Started Session 3242 of user root.
Jun 18 18:22:10 node75 systemd[1]: Started Session 3243 of user root.
Jun 18 18:22:11 node75 systemd[1]: Started Session 3244 of user root.
Jun 18 18:22:11 node75 systemd[1]: Started Session 3245 of user root.
Jun 18 18:22:13 node75 systemd[1]: Started Session 3246 of user root.
Jun 18 18:22:14 node75 systemd[1]: Started Session 3247 of user root.
Jun 18 18:22:17 node75 systemd[1]: Started Session 3248 of user root.
Jun 18 18:22:22 node75 kernel: [174244.149039] ata2.00: Enabling discard_zeroes_data
Jun 18 18:22:22 node75 multipath: sdf: using deprecated getuid callout
Jun 18 18:22:23 node75 kernel: [174245.160084] ata2.00: Enabling discard_zeroes_data
Jun 18 18:22:23 node75 kernel: [174245.163924]  sdf:
Jun 18 18:22:24 node75 kernel: [174246.313987] ata2.00: Enabling discard_zeroes_data
Jun 18 18:22:24 node75 kernel: [174246.320486] ata2.00: Enabling discard_zeroes_data
Jun 18 18:22:24 node75 kernel: [174246.326831] ata2.00: Enabling discard_zeroes_data
Jun 18 18:22:25 node75 kernel: [174247.217690] ata2.00: Enabling discard_zeroes_data
Jun 18 18:22:26 node75 kernel: [174247.496059] ata2.00: Enabling discard_zeroes_data
Jun 18 18:22:27 node75 kernel: [174248.504647] ata2.00: Enabling discard_zeroes_data
Jun 18 18:22:27 node75 kernel: [174248.512515]  sdf:
Jun 18 18:22:27 node75 multipath: message repeated 8 times: [ sdf: using deprecated getuid callout]
Jun 18 18:22:28 node75 kernel: [174249.667311] ata2.00: Enabling discard_zeroes_data
Jun 18 18:22:28 node75 kernel: [174249.673618] ata2.00: Enabling discard_zeroes_data
Jun 18 18:22:28 node75 systemd[1]: Started Session 3258 of user root.
Jun 18 18:22:28 node75 multipath: sdf: using deprecated getuid callout
Jun 18 18:22:29 node75 kernel: [174250.362596] ata2.00: Enabling discard_zeroes_data
Jun 18 18:22:30 node75 kernel: [174251.374819] ata2.00: Enabling discard_zeroes_data
Jun 18 18:22:30 node75 kernel: [174251.379011]  sdf: sdf1
Jun 18 18:22:30 node75 kernel: [174252.064736] ata2.00: Enabling discard_zeroes_data
Jun 18 18:22:30 node75 kernel: [174252.069092]  sdf: sdf1
Jun 18 18:22:30 node75 multipath: message repeated 5 times: [ sdf: using deprecated getuid callout]
Jun 18 18:22:34 node75 systemd[1]: Started Session 3259 of user root.
Jun 18 18:22:34 node75 systemd[1]: Started Session 3260 of user root.
Jun 18 18:22:35 node75 systemd[1]: Started Session 3261 of user root.
Jun 18 18:22:37 node75 kernel: [174258.563000] EXT4-fs (sdf1): mounted filesystem with ordered data mode. Opts: (null)
Jun 18 18:22:37 node75 systemd[1]: Failed to set up mount unit: Device or resource busy
Jun 18 18:22:37 node75 systemd[1]: Reloading.
Jun 18 18:22:37 node75 systemd[1]: Started ACPI event daemon.
Jun 18 18:22:37 node75 systemd[1]: Reloading.
Jun 18 18:22:38 node75 systemd[1]: Started ACPI event daemon.
Jun 18 18:22:38 node75 systemd[1]: Reloading.
Jun 18 18:22:38 node75 systemd[1]: Started ACPI event daemon.
Jun 18 18:22:38 node75 systemd[1]: Starting Elasticsearch...
Jun 18 18:22:38 node75 elasticsearch[169315]: OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was deprecated in version 9.0 and will likely be removed in a future release.
Jun 18 18:22:42 node75 systemd[1]: Started Session 3262 of user root.
Jun 18 18:22:49 node75 systemd[1]: Started Session 3263 of user root.
Jun 18 18:22:50 node75 systemd[1]: Started Session 3264 of user root.
Jun 18 18:22:51 node75 systemd[1]: Started Session 3265 of user root.
Jun 18 18:22:51 node75 systemd[1]: Started Elasticsearch.
Jun 18 18:22:52 node75 elasticsearch[169315]: loading dict /usr/share/elasticsearch/plugins/jieba/dic/user.dict
Jun 18 18:22:52 node75 elasticsearch[169315]: loading dict /usr/share/elasticsearch/plugins/jieba/dic/sougou.dict
Jun 18 18:22:53 node75 systemd[1]: Started Session 3266 of user root
```

说明一下：

上文中的sdf这个分区，是启用ES时选择的ES DATA disk,为了能够复现这个问题，写了支script指定循环次数去启用，停用ES 服务，并检查对应的挂载点，ES集群健康状态，ceph集群健康状态（因为出现shutdown ceph核心服务进行，ceph集群不健康作为退出条件）.


# 问题复现使用的python脚本


{% raw %}```
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import sys
import time
import json
import requests
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def login_session(public_ip, user_id, password):
    login_url = "https://{}:8080/auth".format(public_ip)
    login_data = {"user_id": user_id, "password": password}

    session = requests.session()
    session.keep_alive = False
    session.headers.update({'Accept': 'application/json, text/javascript, */*; q=0.01'})
    response = session.request("POST", login_url, json=login_data, verify=False)

    if response.status_code != 200:
        print("[ERROR]    Login web error, http status code is {} \n".format(response.status_code))
        sys.exit(1)

    return session


def http_request(session, http_method, url, params=None, data=None, public_ip=None, user_id=None, password=None):
    params = {} if params is None else params
    data = {} if data is None else data

    # set SSL Verify to False
    session.verify = False

    # Set session keep alive to False
    session.keep_alive = False

    if "cgi-bin" in url:
        # Legacy CGI
        try:
            response = session.request(http_method, url, params=params, data=data)
        except ConnectionError as ex:
            time.sleep(2)
            response = session.request(http_method, url, params=params, data=data)

        if response.status_code == 401:
            session = login_session(public_ip, user_id, password)
            response = session.request(http_method, url, params=params, data=data)
    else:
        # Restful CGI
        response = session.request(http_method, url, params=params, json=data)

        if response.status_code == 401:
            session = login_session(public_ip, user_id, password)
            response = session.request(http_method, url, params=params, json=data)

    if response.status_code == 500:
        print("[ERROR]    Send HTTP request failed, backend return 500, internal server error \n")
        sys.exit(1)

    return response


def es_enable_data(public_ip, storage_ip, vip):

    data = {
        "ip":storage_ip,
        "vip":vip,
        "router_id":"80",
        "num_shards":"6",
        "num_replicas":"1",
        "storage_location":"disk",
        "disks":"[\"/dev/sdf\"]"
    }

    return data


def enable_es(public_ip, storage_ip, session, http_method, url, data):
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("\n[{}] [Action]   Start to enable ES service on node : ({})".format(cur_time, storage_ip))

    response = http_request(session, http_method, url, data=data)

    if json.loads(response.text)['return_code'] == 0:
        progress_url = "https://{}:8080/cgi-bin/ezs3/json/elasticsearch_role_progress".format(public_ip)
        check_progress(session, storage_ip, progress_url)

        check_es_service_file(storage_ip)
        check_mount_point(storage_ip)
        check_fstab(storage_ip)
    else:
        print("[ERROR]    Enable ES service failed, backend return : ({})".format(response.text))
        sys.exit(1)


def es_disable_data(storage_ip):
    data = {'ip': storage_ip}

    return data

def disable_es(public_ip, storage_ip, session, http_method, url, data):
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("\n[{}] [Action]   Disable ES service on node : ({})".format(cur_time, storage_ip))

    response = http_request(session, http_method, url, data=data)

    if json.loads(response.text)['return_code'] == 0:
        progress_url = "https://{}:8080/cgi-bin/ezs3/json/elasticsearch_role_progress".format(public_ip)
        check_progress(session, storage_ip, progress_url, enable_flag=False)

        check_fstab(storage_ip, enable_flag=False)
        check_mount_point(storage_ip, enable_flag=False)
        check_es_service_file(storage_ip, enable_flag=False)
    else:
        print("[ERROR]    Disable ES service failed, backend return : ({})".format(response.text))
        sys.exit(1)


def progress_params(storae_ip, enable='true'):
    param = {'ip': storae_ip, 'enable': enable}

    return param


def get_enable_progress(session, url, param):
    for i in xrange(60):
        response = http_request(session, "GET", url, params=param) 
        res = json.loads(response.text)
        if res['return_code'] == 0:
            progress = res['response']['info']['progress']
            if progress == 100:
                break
            else:
                if i == 30:
                    print("                                 Wait for more than 150s, go on")
                if i >= 58:
                    print("                                 ES progress is : ({})".format(progress))
                time.sleep(5)
    else:
        cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print("[{}] [ERROR]    Check ES progress failed, exit! \n".format(cur_time))
        sys.exit(1)


def check_progress(session, storage_ip, url, enable_flag=True):
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    if enable_flag:
        print("[{}] [Check]    Check ES enable progress on node : ({})".format(cur_time, storage_ip))
        param = progress_params(storage_ip)
    else:
        print("[{}] [Check]    Check ES disable progress on node : ({})".format(cur_time, storage_ip))
        param = progress_params(storage_ip, enable='false')

    get_enable_progress(session, url, param=param)


def get_radosgw_pid(hosts):
    host_rgw_pid = {}
    for each_host in hosts:
        pid = os.popen("ssh {} ps aux | grep client.radosgw.0 | grep -v grep | awk '{{print $2}}'").read().strip()
        if pid:
            host_rgw_pid[each_host] = pid
        else:
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print("[{}] [ERROR]    Not get radosgw pid on node :({})".foramt(cur_time, each_host))
            sys.exit(1)

    return host_rgw_pid


def check_fstab(storage_ip, enable_flag=True):
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("[{}] [Check]    Check mount config in /etc/fstab on node : ({})".format(cur_time, storage_ip))

    fstab_content = os.popen("ssh {} 'cat /etc/fstab | grep datasearch'".format(storage_ip)).read().strip()
    if enable_flag:
        if "datasearch" not in fstab_content:
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print("[{}] [ERROR]    Enable ES, but not find mount point information in /etc/fstab \n".format(cur_time))
            sys.exit(1)
    else:
        if "datasearch" in fstab_content:
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print("[{}] [ERROR]    Disable ES, but still find mount point information in /etc/fstab \n".format(cur_time))
            sys.exit(1)


def check_mount_point(storage_ip, enable_flag=True, pre_check=False):
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    if not pre_check:
        print("[{}] [Check]    Check mount point on node : ({})".format(cur_time, storage_ip))

    mount_info = os.popen("ssh {} 'mount | grep datasearch'".format(storage_ip)).read().strip()
    if enable_flag:
        if not mount_info:
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print("[{}] [ERROR]    Enable ES, but not find mount point \n".format(cur_time))
            sys.exit(1)
    else:
        if mount_info:
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            if not pre_check:
                print("[{}] [ERROR]    Disable ES, but still find mount point \n".format(cur_time))
            else:
                print("[{}] [ERROR]    Precheck before enable ES, but still find mount point on node : ({}) \n".format(cur_time, storage_ip))
            sys.exit(1)


def check_es_service_file(storage_ip, enable_flag=True):
    file_path = "/etc/systemd/system/multi-user.target.wants/elasticsearch.service"
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("\n[{}] [Check]    Check {}".format(cur_time, file_path))

    if enable_flag:
        if not os.path.exists(file_path):
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print("[{}] [ERROR]  Enable ES, but not find ({}) \n".format(cur_time, file_path))
            sys.exit(1)
    else:
        if os.path.exists(file_path):
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print("[{}] [ERROR]  Disable ES, but still find ({}) \n".format(cur_time, file_path))
            sys.exit(1)


def check_es_cluster_helath(public_ip):
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("\n[{}] [Check]    Check ES cluster status".format(cur_time))

    cmd = "curl -s GET http://{}:9200/_cluster/health | json_pp | grep status".format(public_ip)
    for i in xrange(30):
        es_health = os.popen(cmd).read().strip()
        if 'green' not in es_health:
            time.sleep(5)
            if i == 29:
                cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                print("[{}] [ERROR]    ES Cluser helath status is : ({})".format(cur_time, es_health))
        else:
            break
    else:
        cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print("[{}] [ERROR]  Wait 60s, but ES cluser status is not 'green' \n".format(cur_time))
        sys.exit(1)


def check_ceph_cluster_health():
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("\n[{}] [Check]    Check ceph cluster status".format(cur_time))

    cmd = "ceph -s | grep health"
    for i in xrange(30):
        ceph_health = os.popen(cmd).read().strip()
        if "HEALTH_OK" not in ceph_health:
            time.sleep(5)
        else:
            break
    else:
        cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print("[{}] [ERROR]  Wait 60s, but ceoh cluser status is not 'HEALTH_OK' \n".format(cur_time))
        sys.exit(1)


def force_clean(storage_ip):
    print("[Action]   Start to force to clean umount and disk on node : ({})".format(storage_ip))

    umount_cmd = "ssh {} 'umount /opt/datasearch/0'".format(storage_ip)
    sgdisk_o = "ssh {} 'sgdisk -o /dev/sdf'".format(storage_ip)
    sgdisk_z = "ssh {} 'sgdisk -Z /dev/sdf'".format(storage_ip)
    ude = "ssh {} 'udevadm settle'".format(storage_ip)
    wip = " ssh {} 'wipefs -a -f /dev/sdf'".format(storage_ip)
    rm_folder = "ssh {} 'rm -rf /opt/datasearch/0/'".format(storage_ip)
    os.popen(umount_cmd)
    os.popen(sgdisk_o)
    os.popen(sgdisk_z)
    os.popen(ude)
    os.popen(wip)
    os.popen(rm_folder)


def loop_run(loop_times):
    password = "1"
    user_id = "admin"
    vip = "10.16.172.80/22"
    public_ip = "10.16.172.75"
    storage_ips = ["10.10.10.75", "10.10.10.76", "10.10.10.77"]

    session = login_session(public_ip, user_id, password)
    enable_es_url = "https://{}:8080/cgi-bin/ezs3/json/elasticsearch_role_enable".format(public_ip)
    disable_es_url = "https://{}:8080/cgi-bin/ezs3/json/elasticsearch_role_disable".format(public_ip)

    for i in xrange(loop_times):
        print("\n---------------------------------------------- {} --------------------------------------------".format(i+1))
        # Before disable, check datasearch mount point again, because not known why the mount point mount again
        cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print("[{}] [Check]    Precheck mount point on each node before enable ES service".format(cur_time))

        # Only check once by the first time
        if i < 1:
            for each_storage_ip in storage_ips:
                check_mount_point(each_storage_ip, enable_flag=False, pre_check=True)
            time.sleep(1)
        else:
            for j in xrange(10):
                for each_storage_ip in storage_ips:
                    check_mount_point(each_storage_ip, enable_flag=False, pre_check=True)
                time.sleep(1)

        # # Force clean
        # for each_storae_ip in storage_ips:
        #     force_clean(each_storae_ip)

        # Enable ES service on all node
        for each_storage_ip in storage_ips:
            enable_es_data = es_enable_data(public_ip, each_storage_ip, vip)
            enable_es(public_ip, each_storage_ip, session, "POST", enable_es_url, data=enable_es_data)

        # Check ES cluser status
        os.popen("iptables -F")
        check_es_cluster_helath(public_ip)

        # Disable ES service on all node
        for each_storage_ip in storage_ips:
            disable_es_data = es_disable_data(each_storage_ip) 
            disable_es(public_ip, each_storage_ip, session, "POST", disable_es_url, data=disable_es_data)


        # Check ceph cluster status
        check_ceph_cluster_health()
        time.sleep(2)

        # # Force clean
        # for each_storae_ip in storage_ips:
        #     force_clean(each_storae_ip)


if __name__ == '__main__':
    loop_times = sys.argv[1]

    if loop_times < 1:
        print("[ERROR]  loop_times must >=1 \n")
        sys.exit(1)

    loop_run(int(loop_times))
``` {% endraw %}


# 执行效果


```
root@node75:~# python enable_disable_es.py 3

---------------------------------------------- 1 --------------------------------------------
[Action]   Start to force to clean umount and disk on node : (10.10.10.75)
umount: /opt/datasearch/0: mountpoint not found
[Action]   Start to force to clean umount and disk on node : (10.10.10.76)
umount: /opt/datasearch/0: mountpoint not found
[Action]   Start to force to clean umount and disk on node : (10.10.10.77)
umount: /opt/datasearch/0: mountpoint not found

[2020-06-19 14:17:39] [Action]   Start to enable ES service on node : (10.10.10.75)
[2020-06-19 14:17:40] [Check]    Check ES enable progress on node : (10.10.10.75)
[2020-06-19 14:19:41] [Check]    Check mount config in /etc/fstab on node : (10.10.10.75)
[2020-06-19 14:19:41] [Check]    Check mount point on node : (10.10.10.75)

[2020-06-19 14:19:41] [Action]   Start to enable ES service on node : (10.10.10.76)
[2020-06-19 14:19:41] [Check]    Check ES enable progress on node : (10.10.10.76)
[2020-06-19 14:20:22] [Check]    Check mount config in /etc/fstab on node : (10.10.10.76)
[2020-06-19 14:20:22] [Check]    Check mount point on node : (10.10.10.76)

[2020-06-19 14:20:22] [Action]   Start to enable ES service on node : (10.10.10.77)
[2020-06-19 14:20:22] [Check]    Check ES enable progress on node : (10.10.10.77)
[2020-06-19 14:20:58] [Check]    Check mount config in /etc/fstab on node : (10.10.10.77)
[2020-06-19 14:20:58] [Check]    Check mount point on node : (10.10.10.77)

[2020-06-19 14:20:58] [Check]    Check ES cluster status

[2020-06-19 14:21:04] [Action]   Disable ES service on node : (10.10.10.75)
[2020-06-19 14:21:04] [Check]    Check ES disable progress on node : (10.10.10.75)
[2020-06-19 14:21:14] [Check]    Check mount config in /etc/fstab on node : (10.10.10.75)
[2020-06-19 14:21:14] [Check]    Check mount point on node : (10.10.10.75)

[2020-06-19 14:21:14] [Action]   Disable ES service on node : (10.10.10.76)
[2020-06-19 14:21:14] [Check]    Check ES disable progress on node : (10.10.10.76)
[2020-06-19 14:21:24] [Check]    Check mount config in /etc/fstab on node : (10.10.10.76)
[2020-06-19 14:21:25] [Check]    Check mount point on node : (10.10.10.76)

[2020-06-19 14:21:25] [Action]   Disable ES service on node : (10.10.10.77)
[2020-06-19 14:21:25] [Check]    Check ES disable progress on node : (10.10.10.77)
[2020-06-19 14:21:50] [Check]    Check mount config in /etc/fstab on node : (10.10.10.77)
[2020-06-19 14:21:50] [Check]    Check mount point on node : (10.10.10.77)

[2020-06-19 14:21:51] [Check]    Check ceph cluster status
[Action]   Start to force to clean umount and disk on node : (10.10.10.75)
umount: /opt/datasearch/0: mountpoint not found
[Action]   Start to force to clean umount and disk on node : (10.10.10.76)
umount: /opt/datasearch/0: mountpoint not found
[Action]   Start to force to clean umount and disk on node : (10.10.10.77)
umount: /opt/datasearch/0: mountpoint not found

---------------------------------------------- 2 --------------------------------------------
[Action]   Start to force to clean umount and disk on node : (10.10.10.75)
umount: /opt/datasearch/0: mountpoint not found
[Action]   Start to force to clean umount and disk on node : (10.10.10.76)
umount: /opt/datasearch/0: mountpoint not found
[Action]   Start to force to clean umount and disk on node : (10.10.10.77)
umount: /opt/datasearch/0: mountpoint not found

[2020-06-19 14:22:13] [Action]   Start to enable ES service on node : (10.10.10.75)
[2020-06-19 14:22:14] [Check]    Check ES enable progress on node : (10.10.10.75)
                                 Wait for more than 150s, go on
                                 ES progress is : (30)
                                 ES progress is : (30)
[2020-06-19 14:27:16] [ERROR]    Check ES progress failed, exit! 

root@node75:~#
```


# 为何会出现 'local-fs.target failed with result dependency'


这篇文章： ```https://unix.stackexchange.com/questions/416640/how-to-disable-systemd-agressive-emergency-shell-behaviour ```

有提及到:

```
If you search through the unit files, there are only a very few ways for the boot to fall back to emergency.target. It's usually when a .mount unit for a local filesystem fails, causing local-fs.target to fail. Or when your initramfs fails to mount the root filesystem, if your initramfs uses systemd.

local-fs.target has OnFailure=emergency.target. And it gets failed because units for local filesystems are automatically added to the Requires list of local-fs.target (unless they have DefaultDependencies=no).
```

没有尝试去修改 ```/lib/systemd/system/local-fs.target ``` 中 ```OnFailure=``` 为空(此文件中DefaultDependencies=no)，也没有新增```/etc/systemd/system/local-fs.target.d/nofail.conf ```文件单独去设置``OnFailure=``` 为空。


# 解决方法

由于担心修改```local-fs.target ```会带来额外影响，这里没有采用修改```OnFailure=``` 为空的方法，具体处理方法如下：

使用systemctl show查看local-fs.target requires

```
root@node76:/var/log# systemctl show --property Requires local-fs.target
Requires=-.mount opt-datasearch-0.mount
root@node76:/var/log#
```

这里有个opt-datasearch-0.mount，而这个正好是ES data所对应的挂载点信息，说明启停ES服务时动了/etc/fstab文件了，新增或删除了/etc/fsta对应的ES挂载点信息了，依照这个思路，调整一下产品修改/etc/fstab时间点，在停用ES时，最先去修改/etc/fstab文件，然后才去执行清理zone-group、umount、formate disk，disable es等等动作，然后使用上述脚本验证了30次，问题没有再次浮现。而在调整前，几次就会复现。


# 推论

产品停用ES时：

<img class="shadow" src="/img/in-post/disable_es1.png" width="1200">

上图中，红色箭头1，是自己手动添加的，这个步骤，原先是放在红色箭头2的函数里的。 可以看出，停用ES服务时，先拔除了elasticsearch的开机自启动，再进行ES disk分区的擦写操作（其中包括修改/etc/fstab文件）：

<img class="shadow" src="/img/in-post/disable_es2.png" width="1200">

<img class="shadow" src="/img/in-post/disable_es3.png" width="1200">

而ES disk对应的mount挂载点：

<img class="shadow" src="/img/in-post/fstab_content.png" width="1200">

options 选项是auto,部分journalctl -xb信息如下：

```
Jun 19 18:30:02 node76 kernel: ata2.00: Enabling discard_zeroes_data
Jun 19 18:30:02 node76 kernel:  sdf: sdf1
Jun 19 18:30:02 node76 kernel: ata2.00: Enabling discard_zeroes_data
Jun 19 18:30:02 node76 kernel:  sdf:
Jun 19 18:30:02 node76 multipath[854423]: sdf: using deprecated getuid callout
Jun 19 18:30:02 node76 systemd-udevd[854418]: inotify_add_watch(9, /dev/sdf1, 10) failed: No such file or directory
Jun 19 18:30:02 node76 systemd[1]: Mounting /opt/datasearch/0...
-- Subject: Unit opt-datasearch-0.mount has begun start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
--
-- Unit opt-datasearch-0.mount has begun starting up.
Jun 19 18:30:02 node76 systemd[1]: Stopped target Local File Systems.
-- Subject: Unit local-fs.target has finished shutting down
cal-fs.targetlocal-fs.target
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
--
```

推断，local-fs.target requires ```opt-datasearch-0.mount```，而对应挂载点出现'not found'(见开篇'systemctl --failed'的输出信息)，导致local-fs.target出现timeout（DefaultTimeoutStartSec=90，/etc/systemd/system.conf文件中，默认90s），而local-fs.target.wants是需要/etc/fstab,这里还有个Conflicts=shutdown.target

<img class="shadow" src="/img/in-post/local-fs.target.wants.png" width="1200">

最终应该是触发了shutdown操作，停止了众多的服务，而被停止的服务，是依赖于local-fs.target的，以ceph-osd为示例：

<img class="shadow" src="/img/in-post/ceph-osd.target.wants.png" width="1200">


# 结语

分析至此，基本上知道问题的所在了，具体解法如下：

* 启用ES服务时，等ES相关的服务启用好后，最最后更改/etc/fstab文件；
* 停用ES服务时，第一步就是更改/etc/fstab文件。


# 参考文档

```
https://zhangguanzhang.github.io/2019/01/30/fstab/
https://www.freedesktop.org/software/systemd/man/systemd.mount.html
https://www.freedesktop.org/software/systemd/man/systemd-system.conf.html#
http://www.jinbuguo.com/systemd/systemd.special.html
https://unix.stackexchange.com/questions/416640/how-to-disable-systemd-agressive-emergency-shell-behaviour
https://www.freedesktop.org/software/systemd/man/systemd.unit.html
```


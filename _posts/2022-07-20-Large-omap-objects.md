---
layout:     post
title:      "获取ceph large omap object"
subtitle:   "Get Large omap Object"
date:       2022-07-20
author:     "Gavin"
catalog:    true
tags:
    - ceph
---


# 概述

前几天客户报自己的一套原生ceph集群出现 'Large omap objects'告警，请我们免费技术支持一下解决这个告警。

告警信息如下所示：


<img class="shadow" src="/img/in-post/Large_omap_objects.jpg" width="1200">




# 过程

网上找了个script，再此基础上完善了一下，获取到具体哪个Object omap较大，脚本内容参考如下：

```
#!/usr/bin/env python

import os
import sys
import time
import json
import rados
import rbd

ceph_conf_path = '/etc/ceph/ceph.conf'
rados_connect_timeout = 5

if not os.path.exists(ceph_conf_path):
    print("[ERROR] Incorrect path of ceph.conf, exit!!!")
    sys.exit(1)

class RADOSClient(object):
    def __init__(self,driver,pool=None):
        self.driver = driver
        self.client, self.ioctx = driver._connect_to_rados(pool)
    def __enter__(self):
        return self
    def __exit__(self, type_, value, traceback):
        self.driver._disconnect_from_rados(self.client, self.ioctx)

class RBDDriver(object):
    def __init__(self,ceph_conf_path,rados_connect_timeout,pool=None):
        self.ceph_conf_path = ceph_conf_path
        self.rados_connect_timeout = rados_connect_timeout
        self.pool = pool
    def _connect_to_rados(self, pool=None):
        client = rados.Rados(conffile=self.ceph_conf_path)
        try:
            if self.rados_connect_timeout >= 0:
                client.connect(timeout=self.rados_connect_timeout)
            else:
                client.connect()
            if self.pool == None:
                ioctx = None
            else:
                ioctx = client.open_ioctx(self.pool)
            return client, ioctx
        except rados.Error:
            msg = "Error connecting to ceph cluster."
            client.shutdown()
            raise msg

    def _disconnect_from_rados(self, client, ioctx=None):
        if ioctx == None:
            client.shutdown()
        else:
            ioctx.close()
            client.shutdown()

class cmd_manager():
    def get_large_omap_obj_pool_name(self):
        with RADOSClient(RBDDriver(ceph_conf_path,rados_connect_timeout)) as dr:
            result = ''
            cmd = '{"prefix": "health", "detail": "detail", "format": "json"}'
            result = dr.client.mon_command(cmd,result)
            if result[0] == 0:
                res_ = json.loads(result[1])
                if len(res_["checks"]) and res_["checks"].has_key("LARGE_OMAP_OBJECTS"):
                    return res_["checks"]['LARGE_OMAP_OBJECTS']['detail'][0]['message'].split("'")[1]
            else:
                return False
    def get_pg_list_by_pool(self, pool_name):
        with RADOSClient(RBDDriver(ceph_conf_path, rados_connect_timeout)) as dr:
            result = ''
            cmd = '{"prefix": "pg ls-by-pool", "poolstr": "' + pool_name + '", "format": "json"}'
            result = dr.client.mon_command(cmd,result)
            if result[0] == 0:
                return json.loads(result[1])
            else:
                return False

cmd_ = cmd_manager()
pool_name =  cmd_.get_large_omap_obj_pool_name()
if pool_name:
    print "Large omap objects pool_name = {0}".format(pool_name)
    res =  cmd_.get_pg_list_by_pool(pool_name)
    for i in res:
        num_large_objs = i["stat_sum"]["num_large_omap_objects"]
        if num_large_objs != 0:
            print "pgid={0} OSDs={1} num_large_omap_objects={2}".format(i["pgid"], i["acting"], num_large_objs)
else:
    print "[Cool] Not find objects pool_name, as expected, so exit."
```

# 问题解决


客户的这个问题解决，归根节点是RGW reshard 太小导致的（关闭了auto reshard功能），单个bucket中objects数量超过了20万(osd_deep_scrub_large_omap_object_key_threshold),放大这个告警阈值（ ceph daemon osd.\* injectargs "--osd_deep_scrub_large_omap_object_key_threshold 300000"）虽然能解决客户问题，但客户坚持不修改，说是要遵守规则，不能惯着业务端的人，至此唯一的解决方法就是迁移走bucket中的一部分数据，然后执行deep scrub来解决了（放大shard能解决，但部分index无法落到SSD上，影响整体性能）。

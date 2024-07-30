---
layout:     post
title:      "Get filemap from OSD map"
subtitle:   "Get filemap from OSD map"
date:       2021-08-09
author:     "Gavin Wang"
catalog:    true
categories:
    - [python]
tags:
    - python
---



# Script of get_fibmap.py

```python
#!/usr/bin/env python
import sys
import argparse
from ezs3.command import do_cmd

osd_map = {
    "0":"172.17.59.173",
    "1":"172.17.59.173",
    "2":"172.17.59.174",
    "3":"172.17.59.174",
    "4":"172.17.59.175",
    "5":"172.17.59.175"
}

def print_fibmap(obj_name, osd_id, node):
    pg = do_cmd("ceph osd map data {} | awk '{{print $11}}'|tr -d \"()\"".format(obj_name))
    obj_path = do_cmd("find /data/osd.{}/current/{}_head/ -name \"*{}*\"".format(osd_id, pg.strip(), obj_name), _host=node)
    layout = do_cmd("hdparm --fibmap {}|grep -v sectors".format(obj_path.strip()), _host=node)
    print layout

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    args = parser.parse_args()
    file_path = args.filepath
    cephfs_map = do_cmd("cephfs '{}' map".format(file_path))
    for line in cephfs_map.strip().split('\n'):
        if "OSD" not in line:
            element = line.strip().split()
            obj_name = element[1]
            osd_id = element[4]
            node = osd_map[osd_id]
            print_fibmap(obj_name, osd_id, node)

if __name__ == '__main__':
    main()
```


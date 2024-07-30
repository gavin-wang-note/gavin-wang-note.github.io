---
layout:     post
title:      "Upload and download S3 Big metadata"
subtitle:   "Upload and download S3 Big metadata"
date:       2017-04-24
author:     "Gavin Wang"
catalog:    true
categories:
    - [python]
tags:
    - python
---



# 概述

因应标，要求支持64M大小的`metadata`，所以南京Office测试一下，如何给`ceph S3 Object`上传一个比较大的`metadata`。



# 脚本内容

`s3_big_meta_data_upload_download.py`

```python
#-*-coding:UTF-8-*-

import io
import boto
import glob

import boto.s3.connection
import os
from boto.s3.key import Key
access_key ='VZRCDG5Y7JZTJLCYDZ5T'
secret_key = '8Wl8tyqSY2Url88umtlJ6zkfk5nu6tts+8GDVAx3'

META_SIZE_THREASHOLD = 2500

def upload_file_with_meta(objfile, xml_file, bucket_handle):
    ##debug print "begin upload_file with meta func,,objfile:{},xml_file:{},key:{},".format(objfile,xml_file)

    content = ""
    try:
        with io.open(xml_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False

    k = bucket_handle.new_key(objfile)
    ##debug print "begin upload key_name {}".format(key)
    print "length content is {}".format(len(content) )
    if len(content) < META_SIZE_THREASHOLD:
        ##debug print "xml as metadata:"

        k.set_metadata("descriptions", content)
        k.set_contents_from_filename(objfile)
        print "upload finish"
    else:                                                                      
        #创建属性对象（属性对象key命名为*.MP4.meta），将xml 文件存入对象  
        external_meta = u"{}.meta".format(objfile)     
        k.set_metadata("meta1", external_meta)                                                        
        k.set_contents_from_filename(objfile)      
                                                   
        meta_k = bucket_handle.new_key(external_meta)     
        meta_k.set_contents_from_filename(xml_file)
        print "upload mp4 and xml object finish"


def download_file_with_meta(bucket_handle, key_name):
    try:
        key= bucket_handle.get_key(key_name)
        if 'descriptions' in key.metadata.keys():
            xml_content=key.metadata['descriptions']
            key.get_contents_to_filename(key.name)
            
            xml_file=key_name[:-4]+'.xml'
            with io.open(xml_file, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            print "download finish"
                
        else:
            #下载对象                                           
            print key.get_contents_to_filename(key.name)
            key.get_contents_to_filename(key.name)              
                                                            
            #下载对象的属性                                        
            external_meta=key.metadata['meta1']               
            meta_key=bucket_handle.get_key(external_meta)   
            
            #属性对象下载为xml 文件，名称为xml_name                      
            xml_name=meta_key.name[:-9]+'.xml'              
            ##debug print xml_name                                  
            meta_key.get_contents_to_filename(xml_name)     
            print "download mp4 and xml object finish"
    except Exception as e:
        print str(e)

#建立连接
print "createt connection BEGIN \n"
conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = '10.10.0.127',
        is_secure=False,    #uncomment if you are not using ssl
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )
print conn

print "createt connection  END\n"

bucket_name = "material"
bucket = conn.lookup(bucket_name)
if bucket == None :
    print "bucket {} is not exists".format(bucket_name)
    # 创建bucket 
    bucket = conn.create_bucket(bucket_name)
    # 再次列出所有的bucket，查看是否存在新建的bucket
    for bucket in conn.get_all_buckets():
        print "{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
                )

#查看bucket中的所有对象
print "list all the OBJECTS in bucket, empty of course"
bucket = conn.lookup(bucket_name)
for key in bucket.list():
    print "{name}\t{size}\t{modified}".format(
                name = key.name,
                size = key.size,
                modified =
                key.last_modified,
           )
print "list all the OBJECTS in bucket END\n"
   

# 上传对象的同时，设置对象的元数据信息

filelist = glob.glob("/var/share/ezfs/shareroot/material/*.mp4")
for fi in filelist:
    f_xml = fi[:-4] + ".xml"
    key = os.path.basename(fi) 
    upload_file_with_meta(fi,f_xml,bucket)
print "end filelist"


# download object
for fi in filelist:
    # key = os.path.basename(fi) 
    key = os.path.abspath(fi)
    download_file_with_meta(bucket, key)
print "enc to download object" 

```

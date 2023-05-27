---
layout:     post
title:      "S3 boto set content from filename"
subtitle:   "S3 boto set content from filename"
date:       2019-02-22
author:     "Gavin"
catalog:    true
tags:
    - python
---



s3_boto_set_content_from_filename.py

```
root@node244:~# cat s3_boto_set_content_from_filename.py 
import os
import boto
import shutil
from boto.s3.key import Key
from boto.s3.connection import S3Connection, OrdinaryCallingFormat

import boto.s3.connection


from ezs3.command import do_cmd

filenames = ['sample.txt', 'notes/2019/January/sample.txt', 'notes/2019/February/sample2.txt',
             'notes/2019/February/sample3.txt', 'notes/2019/February/sample4.txt',
             'notes/2019/sample5.txt', 'nose/delete/delete_object.txt']

# create s3 connection
def s3_con(access_key, secret_access_key, host=None, port=80):
    """
    connect to S3
    :param access_key, string, access_key
    :param secret_access_key, string, secret_access_key
    :param host, string, S3 server IP address
    :param port, string, S3 port
    """

    host = '172.17.73.244'

    conn = S3Connection(access_key,
                        secret_access_key,
                        host=host,
                        port=port,
                        calling_format=OrdinaryCallingFormat(),
                        is_secure=False)

    return conn


def upload_dir(conn, bucket_name, upload_path=None):
    upload_path = "/tmp/nose_up" if upload_path is None else upload_path

    bucket = conn.get_bucket(bucket_name)

    for root, dirs, files in os.walk(upload_path):
        for name in files:
            path = root.split(os.path.sep)[1:]
            path.append(name)
            # key_id = os.path.join(*path)
            key_id = os.path.join(*path) + '/'
            k = Key(bucket)
            k.key = key_id
            k.set_contents_from_filename(os.path.join(root, name))

def upload_file_into_bucket(conn, bucket_name, upload_path=None):
    """
    Upload some objects into bucket
    :param conn, a instance, s3 connection
    :param bucket_name, string, a bucket name
    :param upload_path, string, upload file path
    """

    upload_path = "/tmp/nose_up" if upload_path is None else upload_path
    destDir = ''

    print('[Action]   Upload files to bucket , '
                 'set contents of object ) from filenames', bucket_name, filenames)

    if os.path.exists(upload_path):
        shutil.rmtree(upload_path)
        os.mkdir(upload_path, 0755)
 
    if not os.path.exists(upload_path):
        os.mkdir(upload_path, 0755)
 
    for each_file in filenames:
        # dir_path = upload_path + os.sep + os.path.dirname(each_file)
        dir_path = os.path.join(upload_path, os.path.dirname(each_file))
        file_name = os.path.basename(each_file)
        print("--  dir_path is : , file_name is : ", dir_path, file_name)
        if not os.path.exists(dir_path):
            if dir_path != '':
                os.makedirs(dir_path, 0755)
            # print("--  echo content to : ", dir_path + os.sep + file_name)
            do_cmd("echo {} > {}".format(file_name, dir_path + os.sep + file_name), 30)
        elif not os.path.exists(each_file):
            full_name = dir_path + os.sep + file_name
            print("--  full_name is : ", full_name)
            do_cmd("echo {} > {}".format(file_name, dir_path + os.sep + file_name), 30)

    try:
        bucket = conn.get_bucket(bucket_name)
        for each_file in filenames:
            key = Key(bucket, each_file)
            key.set_contents_from_filename(upload_path + os.sep + each_file)
#            full_key_name = os.path.join(upload_path, each_file)
#            print("----- full_key_name is : ", full_key_name)
#            k = bucket.new_key(full_key_name)
#            k.set_contents_from_filename(full_key_name)
#            # k.set_contents_from_filename(each_file)

#         for root, dirs, files in os.walk(upload_path):
#             for each_file in files:
#                 key = Key(bucket, each_file)
#                 key.set_contents_from_filename(upload_path + os.sep + each_file)
#        for each_file in filenames:
#            sourcepath = os.path.join(upload_path + '/' + each_file)
#            destpath = os.path.join(destDir + '/' + each_file)
#            k = boto.s3.key.Key(bucket)
#            k.key = destpath
#            k.set_contents_from_filename(sourcepath)
    except Exception as e:
        print("[ERROR]  Upload s3 object to bucket : ({}) failed, "
              "backend return : ({})".format(bucket_name, str(e)))
        return str(e)


def list_object_in_bucket(conn, bucket_name, prefix=None):
    """
    List all objects with a prefix under a bucket
    :param conn, instance, S3 connection
    :param bucket_name, string, a bucket name
    :param prefix, string, a object prefix name
    """

    print("[Action]   Start to list object in bucket : (%s)", bucket_name)
    prefix = '' if prefix is None else prefix

    match_objs = []

    try:
        bucket = conn.get_bucket(bucket_name)

        for obj in bucket.list(prefix=prefix):
            match_objs.append(obj.key)

        len_mat_objects = len(match_objs)
        if int(len_mat_objects) > 0:
            print("[Success]  List object : (%s) from bucket : (%s) success.", match_objs, bucket_name)
    except Exception as e:
        print("[ERROR]  Upload a single S3 object to bucket : ({}) failed, "
                      "backend return : ({})".format(bucket_name, str(e)))

    return match_objs



if __name__ == '__main__':
    access_key = '62HVFE4XEYSSA9C3C7U0'
    secret_access_key = 'gHlpbsR6E9nQ4EaLBcmrlNxwQ96NfeCpYq1kfMSq'
    bucket_name = 'bucket01'
    conn = s3_con(access_key, secret_access_key)
    # upload_dir(conn, bucket_name)
    upload_file_into_bucket(conn, bucket_name)
    list_object_in_bucket(conn, bucket_name)

```

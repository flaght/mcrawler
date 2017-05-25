# -*- coding: utf-8 -*-
#encoding=utf-8

"""
Created on 2016年8月7日

@author: kerry
"""

class FetchFileOpcode:
    """
    fetch file opcode 提取文件的方式,包括ftp获取文件,http方式获取文件,本地获取文件
    """
    ftp = 0

    http = 1

    local = 2


fetch_file_opcode = FetchFileOpcode()


class FilerOpcode:
    """
    filer opcode
    """
    ftp = 1

    http = 2

    local = 3

    kafka = 4

    hbase = 5

    redis = 6

filer_opcode = FilerOpcode()


class StorageOpcode(object):
    """
    storage opcode 存储方式
    """
    redis = 0

    hbase = 1

    mysql = 2

    text = 3

    memcache = 4

    sqlite = 5

    kafka_p = 6

    kafka_c = 7

storage_opcode = StorageOpcode()




#!/usr/bin/python2.6  
# -*- coding: utf-8 -*-  
# encoding=utf-8

import json
import zlib
import base64
from analysis.schduler.storage.kafka_manage_model import kafka_consumer_t
from analysis.common.ftp_manager import ftp_manager_t
from analysis.common.mstring import MString


"""
Created on 2015年9月29日

@author: kerry
"""

"""
def func(msg):
    print "msg:", msg
    time.sleep(3)
    print "end"
"""


class AnalysisManager:
    def __init__(self):
        ftp_manager_t.connent()
        kafka_consumer_t.set_callback(self.kafka_callback)

    def kafka_callback(self, data):
        name = data['key_name'] + data['pos_name']
        ftp_url = '~/text_storage/' + data['key_name'] + '/' + data['pos_name']
        # 采用多进程方式进行拉取
        ftp_string = MString(name)
        ftp_manager_t.get(ftp_url, ftp_string.write)
        self.text_parser(ftp_string.string, data['key_name'])

    def text_parser(self, ftp_string, name):
        charset_name = ''
        html_dict = json.loads(ftp_string)
        data = ''
        # 解base64
        try:
            data = base64.b32decode(html_dict['content'])
            charset_name = html_dict['charset']
        except Exception, e:
            print e
        # 解压缩
        try:
            data = zlib.decompress(data)
        except Exception, e:
            print e

        # 解字符串码
        try:
            data = data.decode(charset_name)
            print data
        except Exception, e:
            print e

        # html解析对象
        print name


    def ftp_downdata(self, name, ftp_url):
        ftp_manager_t.download(name, ftp_url)

    def run(self):
        kafka_consumer_t.run()


def main():
    # type: () -> object
    analysis = AnalysisManager()
    analysis.run()
    # pool = multiprocessing.Pool(processes = 1)
    # for i in xrange(4):
    #   msg = "hello %d " %(i)
    #  pool.apply_async(func, (msg, ))
    #  #time.sleep(3)
    #  print "1111"


if __name__ == '__main__':
    main()

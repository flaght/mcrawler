# -*- coding: utf-8 -*-

import json
import zlib
import base64
import sys
from schduler.storage.kafka_manage_model import kafka_consumer_t
from common.ftp_manager import ftp_manager_t
from common.mstring import MString
from parser.parser import Parser as MParser


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
        #ftp_manager_t.connect()
        self.mparser = MParser()
        kafka_consumer_t.set_callback(self.kafka_callback)


    def ftp_fle(self,path):
        ftp_manager_t.set_path(path)
        count = ftp_manager_t.file_count()
        i = 0
        while (i < count):
            tlist = ftp_manager_t.get_file(i,i+10)
            #print tlist
            i += 10
            for t in tlist:
                name = "60006" + t
                ftp_url = path + "/" + t
                print ftp_url
                ftp_string = MString(name)
                if ftp_manager_t.get(ftp_url, ftp_string.write):
                    self.text_parser(ftp_string.string, "60006")

        #print ftp_manager_t.get_file(0,10)

    def test_kafka(self):
        m = [
            "329872b3ee3a79701f8ab0d0a0d51fdd",
            "661b7c0f6f7ee2956d248161ba151af7",
            "99578860e856335429853afe4f4681a0",
            "cc7262698ad804f39bee1a89749dbb57",
            "32989cb653f01bcffabe15460fccab59",
            "661bc8de8f2acefb212ea690f8a4e53e",
            "99587d57cd1a5bb31138c859367028c4",
            "cc7322d2732dcc345262fbfd7b78b7ed",
            "3299407ed0386a5c73d2ab9aca015181",
            "661c92ef0e5d121b6731db38f0e19696",
            "9959bd6ae99423a96c50209cf18b5866",
            "cc732618825c5acb4d422fac26a5a43f",
            "3299b739eaf660c9383a1389af1ed404",
            "661d15fdfedc0f85548918ad0c235cdb",
            "995aba94f4816ce455985998a1ecfee5"
        ]

        for t in m:
            name = "60006" + t
            ftp_url = '~/text_storage/' + "60006/" + t
            ftp_string = MString(name)
            if ftp_manager_t.get(ftp_url, ftp_string.write):
                self.text_parser(ftp_string.string, "60006")

    def kafka_callback(self, data):
        name = data['key_name'] + data['pos_name']
        ftp_url = '~/text_storage/' + data['key_name'] + '/' + data['pos_name']
        print  ftp_url
        # 采用多进程方式进行拉取
        ftp_string = MString(name)
        if ftp_manager_t.get(ftp_url, ftp_string.write):
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
        except Exception, e:
            print e

        # 解析对象
        self.mparser.parse(int(name), data)


    def ftp_downdata(self, name, ftp_url):
        ftp_manager_t.download(name, ftp_url)

    def run(self):
        self.ftp_fle("~/text_storage/60006bak")
        #self.test_kafka()
        #kafka_consumer_t.run()


def main():
    # type: () -> object
    reload(sys)                         # 2
    sys.setdefaultencoding('utf-8')     # 3
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

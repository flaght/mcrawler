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
        ftp_manager_t.connect()
        self.mparser = MParser()
        kafka_consumer_t.set_callback(self.kafka_callback)


    def test_kafka(self):
        m = [
            "d9be6e67b6086781c3280473cddc998c",
            "d9be908302b049223e3571db1b8e14da",
            "d9bf99393ef11ad65d3eeac3140dad40",
            "d9c02435ddd5dc976bce9b084c1ad013",
            "d9c089e0a6f5fe519bb9d3f07daea7d6",
            "d9c1565d79963843edd998c6f79febe7",
            "d9c1d6db1a98e6ed71d7041e995bcf6a",
            "d9c1ee7509f1ec60265a5c2d5f2f53d6",
            "d9c1f733c64c9d688f2fe1fad535c374",
            "d9c283e4ef7c8241394a96fb299473a7",
            "d9c2ca4189df042903fd8d740b793772",
            "d9c33ad2ffdb8531db150b6f1befc031",
            "d9c3c4921f49e9464d9fb22958530b60",
            "d9c541cd02a2f44d2e8ae5a9eccac373",
            "d9c54daf7c3ebb11a89a5095044edd52",
            "d9c58f16618077a481c42347e626a2b6",
            "d9c657cbc47e4866b001354e67560424",
            "d9c6d6bc48aed589ea59384bae4cab97",
            "d9c71b71e654abe261abe18b97864086",
            "d9c7269f8a072d5f1f46c09d8deba8dc",
            "d9c8869e0e44e61e0ac38bb19977874f",
            "d9c887da3986e99cb177d024ef213041",
            "d9c8f40f60c228f7cdb8d6dd6a83b075",
            "d9c91495a0d137495a0f334b0194cd76",
            "d9c91751e15276a4bf9e7773aeb28c17",
            "d9c948d51c7590c001f4953df77c3de4",
            "d9c9ded35c21f59d485d28ed32ea38c2",
            "d9ca38d278b7378d66d65415fee7234f"
        ]

        for t in m:
            name = "60006" + t
            ftp_url = '~/text_storage/' + "60006/" + t
            ftp_string = MString(name)
            ftp_manager_t.get(ftp_url, ftp_string.write)
            self.text_parser(ftp_string.string, "60006")

    def kafka_callback(self, data):
        name = data['key_name'] + data['pos_name']
        ftp_url = '~/text_storage/' + data['key_name'] + '/' + data['pos_name']
        print  ftp_url
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
        except Exception, e:
            print e

        # 解析对象
        self.mparser.parse(int(name), data)


    def ftp_downdata(self, name, ftp_url):
        ftp_manager_t.download(name, ftp_url)

    def run(self):
        self.test_kafka()
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

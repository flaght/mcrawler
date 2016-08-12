# encoding=utf-8

import base64
import json
import zlib

from common.ftp_manager import ftp_manager_t
from common.mstring import MString
from schduler.storage.kafka_manage_model import kafka_consumer_t

"""
Created on 2015年9月29日

@author: kerry
"""


class AnalysisManager:
    def __init__(self):
        ftp_manager_t.connect()
        kafka_consumer_t.set_callback(self.kafka_callback)

        # self.detecotr = icu.CharsetDetector()

    def kafka_callback(self, data):
        name = data['key_name'] + data['pos_name']
        ftp_url = '~/text_storage/' + data['key_name'] + '/' + data['pos_name']
        print ftp_url
        ftp_string = MString(name)
        ftp_manager_t.get(ftp_url, ftp_string.write)
        self.parser(ftp_string.string)

    @staticmethod
    def parser(string):
        charset_name = ''
        html_dict = json.loads(string)
        data = None
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

    @staticmethod
    def ftp_download(name, ftp_url):
        ftp_manager_t.download(name, ftp_url)

    @staticmethod
    def run():
        kafka_consumer_t.run()


def main():
    analysis = AnalysisManager()
    analysis.run()


if __name__ == '__main__':
    main()

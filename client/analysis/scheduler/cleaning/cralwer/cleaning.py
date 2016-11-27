# -*- coding: utf-8 -*-
"""
Created on 20161118

@author kerry
"""

import json
import zlib
import base64
from analysis.base.mlog import mlog


class CleaningCrawler():
    @classmethod
    def clean_data(cls, content):
        charset_name = ''
        try:
            dict = json.loads(content)
        except Exception, e:
            mlog.log().error(e)
            print content
        data = ''
        # 解base64
        try:
            data = base64.b32decode(dict['content'])
            charset_name = dict['charset']
        except Exception, e:
            mlog.log().error(e)
            return None
        # 解压缩
        try:
            data = zlib.decompress(data)
        except Exception, e:
            mlog.log().error(e)
            return None

        # 解字符串码
        try:
            data = data.decode(charset_name)
        except Exception, e:
            mlog.log().error(e)
            return None

        return data

# -*- coding: utf-8 -*-
"""
Created On 20170523
@author kerry
"""
from analysis.base.urlparse_ext import  URLParseExt
import json

class WeiboIndex(object):

    def five_star_index(self, content):
        try:
            url = content.get('url')
            if url is None:
                return None, None
            turl = URLParseExt(url)
            index_id = turl.get_query_value('key')
            data = content['data']
            if data is None:
                return None, None
            return index_id, json.loads(data)
        except Exception, e:
            return None, None
        

sina_weibo_index = WeiboIndex()

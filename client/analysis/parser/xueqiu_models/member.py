# -*- coding: utf-8 -*-

"""
Created on 201601015

@author kerry
"""

from analysis.base.urlparse_ext import URLParseExt
import json

class Member():
    def member_max(self, content):
        try:
            url = content.get('url')
            if url is None:
                return None,None

            turl = URLParseExt(url)
            uid = turl.get_query_value('uid')
            data = content['data']
            if data is None:
                return None, None
            t = json.loads(data)
            max_page = t.get('maxPage', None)
            if max_page is None:
                return None, None
            return uid, max_page
        except Exception, e:
            return None, None
        except Exception, e:
            return None, None


xq_memeber = Member()
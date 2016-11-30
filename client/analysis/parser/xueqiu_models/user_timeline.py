# -.- coding:utf-8 -.-
"""
Created on 2016年11月30日

@author: kerry
"""
from analysis.base.urlparse_ext import URLParseExt
from analysis.base.mlog import mlog
class UserTimeline():


    def cralw_info(self, content):
        try:
            url = content.get('url')
            if url is None:
                return None,None

            turl = URLParseExt(url)
            uid = turl.get_query_value('user_id')
            data = content['data']
            if data is None:
                return None,None
            mlog.log().info(eval(data))
            max_page = eval(data).get('maxPage',None)
            if max_page is None:
                return None,None
            return uid, max_page
        except Exception, e:
            return None,None


xq_usertimeline = UserTimeline()
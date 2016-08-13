# -.- coding:utf-8 -.-
'''
Created on 2015年8月26日

@author: chenyitao
'''

import random
from scrapy.conf import settings

class ProxyMiddleware(object):
    """
    Proxy
    """
    def __init__(self):
        self.proxy_list = settings.attributes['HTTP_PROXY'].value

    def process_request(self, request, spider):
        """
        process request
        """
        self.proxy_list = settings.attributes['HTTP_PROXY'].value
        isforge = request.meta.get('isforge',None)
        if isforge == 1:
            request.meta['proxy'] = 'http://%s' % random.choice(self.proxy_list)

        del request.meta['isforge']

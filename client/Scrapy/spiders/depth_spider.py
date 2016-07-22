# -*- coding:utf-8 -*-

import md5
import time
import urllib

from scrapy import signals
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider
from scrapy.spider import Rule
from scrapy.xlib.pydispatch import dispatcher


# 爬虫心跳
custom_signal_heart = object()
# 存储信号
custom_signal_storage = object()

class DepthSpider(CrawlSpider):
    '''
    sipder
    '''
    name = 'DepthSpider'
    start_urls = []

    def __init__(self, params=None):
        '''
        params[0]:callback 爬虫状态回调
        params[1]:task_info 任务信息
        '''
        self.signals_callback = params[0]
        self.task_info = params[1]
        self.start_urls = [self.task_info.url]
        rest = urllib.splittype(self.task_info.url)
        res = urllib.splithost(rest[1])
        self.name = str(self.task_info.job_id)
        self.rules = (Rule(LinkExtractor(allow_domains=res),
                           callback='parse_item',
                           follow=True),)
        super(DepthSpider, self).__init__()
        dispatcher.connect(self.signal_dispatcher)

    def parse_item(self, response):
        item = {}
        item['key'] = md5.new(response.url+str(time.time())).hexdigest()
        item['value'] = response.body
        rest = urllib.splittype(response.url)
        res = urllib.splithost(rest[1])
        self.signals_callback(self, custom_signal_storage, [item,
                                                            res[0],
                                                            self.task_info,
                                                            item['key']])

    def signal_dispatcher(self, signal):
        '''
        callback signal
        '''
        if self.signals_callback:
            if signal == signals.engine_stopped:
                self.signals_callback(self, signal, [self.task_info])
                return
            self.signals_callback(self, signal)

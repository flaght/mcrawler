# -.- coding:utf-8 -.-
'''
Created on 2015年12月28日

@author: chenyitao
'''
'''
存储信号
'''

import md5
import time
import urlparse

from scrapy import signals
import scrapy
from scrapy.exceptions import DontCloseSpider
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher

from kid.common import kid_setting as kid_setting
#from kid.common.common_method import print_plus


signal_storage = object()

signal_response_url_not_request_url = object()

class SingleSpider(scrapy.Spider):
    '''
    single spider
    '''
    name = 'SingleSpider'
    start_urls = []
    handle_httpstatus_list = [403]

    def __init__(self, params):
        '''
        params[0]:callback 
        '''
        self.signals_callback = params[0]['callback']
        self.tasks = []
        self.task_cnt = 0
        dispatcher.connect(self.signal_dispatcher)

    def add_task(self, task_cookie):
        self.tasks.append(task_cookie)
        if not len(self.tasks):
            return
        task = self.tasks.pop(0)
        task_info = task['task_info']
        cookie = task['cookie']
        if task_info.attr_id == 20001:
            cookie = None
        url = task_info.url.rstrip(' ')
        url_info = urlparse.urlparse(url)
        if task_info.method == 1:
            method = 'POST'
        else:
            method = 'GET'

        req = Request(url,
                      method=method,
                      headers={'Cookie':cookie,
                               'Referer':url_info[0]+'://'+url_info[1]},
                      callback=self.parse,
                      meta={'item':task,
                            'isforge':task_info.is_forge},
                      dont_filter=True,
                      errback=self.req_err)
        self.crawler.engine.schedule(req, self)
        print('=>>>>>', cookie, '<=>',task_info.attr_id)

    def req_err(self, response):
        # self.add_task(response.request.meta['item'])
        pass

    def parse(self, response):
        if response.status == 404:
            return
        task = response.request.meta['item']['task_info']
        if task.url.split('://')[1] != response.url.split('://')[1]:
            self.signals_callback(self,
                                  signal_response_url_not_request_url,
                                  {'task':task})
            return
        item = {'basic':{}}
        item['basic']['url'] = response.url
        if kid_setting.CRAWLER_TYPE == 2:
            item['basic']['key'] = response.url
        else:
            time_str = '%f' % time.time()
            item['basic']['key'] = md5.new(task.url+time_str).hexdigest()
        item['basic']['content'] = response.body
        self.signals_callback(self,
                              signal_storage,
                              {'task':task,
                               'item':item})

    def signal_dispatcher(self, signal):
        '''
        callback signal
        '''
        if self.signals_callback:
            if signal == signals.spider_idle or signal == signals.spider_error:
                if kid_setting.CONNECT:
                    raise DontCloseSpider('..I prefer live spiders.')
                return
            elif signal == signals.spider_opened:
                self.signals_callback(self, signal, [self])

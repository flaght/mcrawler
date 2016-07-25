# -.- coding:utf-8 -.-
'''
Created on 2015年10月9日

@author: chenyitao
'''

import re
import time
import string
import ConfigParser
from lxml import html
from schduler.storage.redis_manage_model import RedisManageModel
from schduler.analysis_models.analysis_base import AnalysisBase

class ThsOptionalUnitAnalysis(AnalysisBase):
    '''
    classdocs
    '''
    __conf_path = '/etc/kid_conf/analysis/10jqka/ths_optional_unit.conf'
    tag = {'rule':'//*[@id="J_subnav"]/div/div[@class="u_nav_box"]/ul/li/a',
           'tag':'我的自选股'}

    def __init__(self, callback=None, **kwargs):
        '''
        Constructor
        '''
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self.follow_stock_list = []
        cf = ConfigParser.ConfigParser()
        cf.read(self.__conf_path)
        host = cf.get('redis_info', 'host')
        port = cf.get('redis_info', 'port')
        db = cf.get('redis_info', 'db')
        password = cf.get('redis_info', 'password')
        redis_model = RedisManageModel(host, port, db, password)
        self.stock_codes = redis_model.get_storage_info('LRANGE',
                                                        {'name':'stock:list',
                                                         'start':0,
                                                         'end':-1})
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        '''
        ananlysis
        '''
        doc = html.fromstring(self.html_data)
        ret = doc.xpath('/html/body/script[3]/text()')
        if not len(ret):
            return
        contents = ret[0]
        target = re.findall(r'"(.*?)"', contents)
        if not target:
            return
        if target[-1] == "":
            target.pop()
        self.follow_stock_list = target
        self.html_timestamp = str(self.kwargs['timestamp'])
        self.html_time_string = self.html_timestamp[:10]+'.0'
        self.html_time_float = string.atof(self.html_time_string)
        self.log_hour = time.strftime("%Y-%m-%d %H",
                                      time.localtime(self.html_time_float))
        self.__make_storage_info()

    def __make_storage_info(self):
        '''
        make storage info
        '''
        for stock_code in self.follow_stock_list:
            if stock_code in self.stock_codes:
                name = 'follow:%s:%s' % (stock_code, self.log_hour)
                self.storage_cmd_list.append({'cmd':'INCR',
                                              'params':{'name':name}})
                self.storage_cmd_list.append({'cmd':'EXPIRE',
                                              'params':{'name':name,
                                                        'time':50*60*60}})
                name = 'follow:%s' % self.log_hour
                self.storage_cmd_list.append({'cmd':'HINCRBY',
                                              'params':{'name':name,
                                                        'value':stock_code,
                                                        'amount':1}})
                self.storage_cmd_list.append({'cmd':'EXPIRE',
                                              'params':{'name':name,
                                                        'time':50*60*60}})

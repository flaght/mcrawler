# -*- coding: utf-8 -*-

"""
Created on 2016年11月19日

@author: kerry
"""

"""
用于作为解析后的数据处理
"""

from analysis.scheduler.storage.manage_model.xueqiu.storager_manage import Storager
from analysis.db.xueqiu import XueQiu as xqdb

class Scheduler:

    def __init__(self, config):
        #config = {}
        #config['name'] = xqdb.database
        self.storager = Storager(config.get('result'))
        self.__create_selector()

    def __del__(self):
        pass


    def process_data(self,pltid, data):
        content = data['content']
        pid = content.get('pid')
        if pid is None:
            pid = pltid
        else:
            pid = int(pid)
        logic_method = self.logic_selector[pid]
        if logic_method:
            logic_method(pid, data)


    def __search_event(self, pid, data):
        self.storager.process_data(pid, data)

    def __get_uid(self, pid, data):
        uid_set = data['content']['result']
        self.storager.process_data(pid, uid_set)

    def __fetch_crawl(self, pid, data):
        content = {'content':{'key':'crawl_info','result':data}}
        self.storager.process_data(pid, content)

    def __create_selector(self):
        self.logic_selector = {60006: self.__search_event,
                               -599: self.__get_uid,
                               599: self.__fetch_crawl}
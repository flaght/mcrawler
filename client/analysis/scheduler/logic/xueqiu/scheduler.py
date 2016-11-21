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

    def __init__(self):
        config = {}
        config['name'] = xqdb.database
        self.storager = Storager(config)
        self.__create_selector()

    def __del__(self):
        pass


    def process_data(self,pid, data):
        logic_method = self.logic_selector[pid]
        if logic_method:
            logic_method(pid, data)


    def __search_event(self, pid, data):
        self.storager.process_data(pid, data)

    def __create_selector(self):
        self.logic_selector = {60006: self.__search_event}
# -*- coding: utf-8 -*-

"""
Created on 2016年11月19日

@author: kerry
"""

from analysis.db.xueqiu import XueQiu as xqdb

"""
用于处理雪球相关的存储
"""
from scheduler.storage.manage_model.base_storager import BaseStorager,storage_opcode

class Storager:
    def __init__(self,config):
        self.sqlite_manager = BaseStorager.create_storager(storage_opcode.sqlite, config)
        self.__create_selector()


    def __create_selector(self):
        self.storage_selector = {60006: self.__storage_search}


    def __storage_search(self,content):
        name_table = xqdb.build_table_name(content)
        content_data = content['content']['result']
        self.sqlite_manager.create_table(xqdb.create_search_sql(name_table),1)
        self.sqlite_manager.save_data(xqdb.save_search_format(name_table), content_data)

    def process_data(self, pid, content):
        storage_method = self.storage_selector[pid]
        if storage_method:
            storage_method(content)


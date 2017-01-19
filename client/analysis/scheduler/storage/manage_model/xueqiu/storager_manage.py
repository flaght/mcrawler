# -*- coding: utf-8 -*-

"""
Created on 2016年11月19日

@author: kerry
"""

from analysis.db.xueqiu import XueQiu as xqdb

"""
用于处理雪球相关的存储
"""
from analysis.scheduler.storage.manage_model.base_storager import BaseStorager
from analysis.common.operationcode import storage_opcode
import json


class Storager:
    def __init__(self,config):
        if config.get('type') == 5:
            self.sqlite_manager = BaseStorager.create_storager(storage_opcode.sqlite, config)
        elif config.get('type') == 3:
            self.text_manager = BaseStorager.create_storager(storage_opcode.text, config)
        self.__create_selector()


    def __create_selector(self):
        self.storage_selector = {60006: self.__storage_search,
                                 -599: self.__storage_get_uid,
                                 599: self.__storage_crawl,
                                 598: self.__storage_clean_search,
                                 600: self.__storage_member_max,
                                 -600:self.__stroage_get_member}


    def __storage_search(self,content):
        name_table = xqdb.build_table_name(content)
        content_data = content['content']['result']
        if not self.sqlite_manager.check_table(name_table):
            self.sqlite_manager.create_table(xqdb.create_search_sql(name_table),1)
        self.sqlite_manager.save_data(xqdb.save_member_max(name_table), content_data)


    def __storage_member_max(self, content):
        name_table = "member_max"
        content_data = content['content']['result']
        if not self.sqlite_manager.check_table(name_table):
            self.sqlite_manager.create_table(xqdb.create_member_max(name_table),1)
        self.sqlite_manager.save_data(xqdb.save_member_max(name_table), content_data)

    def __storage_clean_search(self, content):
        content_data = content['content']['result']
        for key in content_data:
            clist = content_data.get(key)
            if clist is not None:
                if not self.sqlite_manager.check_table(key):
                    self.sqlite_manager.create_table(xqdb.create_clean_search_sql(key), 1)
                self.sqlite_manager.save_data(xqdb.save_search_clean_format(key), clist)


    def __storage_crawl(self, content):
        name_table = xqdb.build_table_name(content)
        content_data = [(content['content']['result']['content']['uid'],content['content']['result']['content']['max_page'])]
        if not self.sqlite_manager.check_table(name_table):
            self.sqlite_manager.create_table(xqdb.create_crawl_uid_sql(name_table),1)
        self.sqlite_manager.save_data(xqdb.save_crawl_format(name_table), content_data)


    def __storage_get_uid(self, content):
        t = json.dumps(content)
        self.text_manager.write(t)

    def __stroage_get_member(self, content):
        t = json.dumps(content)
        self.text_manager.write(t)

    def process_data(self, pid, content):
        storage_method = self.storage_selector[pid]
        if storage_method:
            storage_method(content)


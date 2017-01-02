# -*- coding: utf-8 -*-

"""
Created on 2016年11月19日

@author: kerry
"""

from analysis.db.hexun import HeXun as hxdb

"""
用于处理和讯相关的存储
"""
from analysis.scheduler.storage.manage_model.base_storager import BaseStorager
from analysis.common.operationcode import storage_opcode


class Storager:
    def __init__(self,config):
        if config.get('type') == 5:
            self.sqlite_manager = BaseStorager.create_storager(storage_opcode.sqlite, config)
        elif config.get('type') == 3:
            self.text_manager = BaseStorager.create_storager(storage_opcode.text, config)
        self.__create_selector()


    def __create_selector(self):
        self.storage_selector = {588: self.__stock_day_heat}


    def process_data(self, pid, content):
        storage_method = self.storage_selector[pid]
        if storage_method:
            storage_method(content)

    def __stock_day_heat(self, content):
        name_table = content['symbol']
        content_data = content['tlist']
        if not self.sqlite_manager.check_table(name_table):
            self.sqlite_manager.create_table(hxdb.create_stock_day_heat(name_table),1)
        self.sqlite_manager.save_data(hxdb.save_stock_day_heat(name_table), content_data)
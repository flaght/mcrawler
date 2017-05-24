# -*- coding: utf-8 -*-

'''
Created on 2017年5月23日

@author: kerry
'''

"""
用于处理新浪相关的存储
"""

from analysis.db.xueqiu import XueQiu as xqdb
from analysis.comm_opercode import net_task_opercode,local_task_opercode
from analysis.scheduler.storage.manage_model.base_storager import BaseStorager
from analysis.common.operationcode import storage_opcode
import json


class Storager(object):
    def __init__(self,config):
        if config.get('type') == storage_opcode.sqlite:
            self.sqlite_manager = BaseStorager.create_storager(storage_opcode.sqlite, config)
        elif config.get('type') == storage_opcode.text:
            self.text_manager = BaseStorager.create_storager(storage_opcode.text, config)
        elif config.get('type') == storage_opcode.redis:
            self.redis_manager = BaseStorager.create_storager(storage_opcode.redis, config)
        elif config.get('type') == storage_opcode.kafka_p:
            self.kafka_manager = BaseStorager.create_storager(storage_opcode.kafka_p, config)

        self.__create_selector()

    def __create_selector(self):
        self.storage_selector = {net_task_opercode.SINA_WEIBO_INDEX: self.__sina_weibo_index}

    def __sina_weibo_index(self, content):
        self.kafka_manager.push_data(json.dumps(content['content']))

    def process_data(self, pid, content):
        storage_method = self.storage_selector[pid]
        if storage_method:
            storage_method(content)
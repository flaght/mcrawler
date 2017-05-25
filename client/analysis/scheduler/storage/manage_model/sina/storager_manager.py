# -*- coding: utf-8 -*-

'''
Created on 2017年5月23日

@author: kerry
'''

"""
用于处理新浪相关的存储
"""

from analysis.scheduler.storage.manage_model.base_storager import BaseStorager
from analysis.common.operationcode import storage_opcode
from analysis.comm_opercode import net_task_opercode
import json


class Storager(object):
    def __init__(self,configs):
        "支持存储器中同时存在多个存储方式"
        self.storager_engines = {}
        storager_manager = None
        for k in configs:
            config = configs[k]
            if config.get('type') == storage_opcode.sqlite:
                storager_manager = BaseStorager.create_storager(storage_opcode.sqlite, config)
            elif config.get('type') == storage_opcode.text:
                storager_manager = BaseStorager.create_storager(storage_opcode.text, config)
            elif config.get('type') == storage_opcode.redis:
                storager_manager = BaseStorager.create_storager(storage_opcode.redis, config)
            elif config.get('type') == storage_opcode.kafka_p:
                storager_manager = BaseStorager.create_storager(storage_opcode.kafka_p, config)

            self.storager_engines[config.get('type')] = storager_manager

        self.__create_selector()

    def __create_selector(self):
        self.storage_selector = {net_task_opercode.SINA_WEIBO_INDEX: self.__sina_weibo_index}


    def __sina_weibo_index(self, content):
        redis_value = content[storage_opcode.redis]
        kafka_value = content[storage_opcode.kafka_p]
        value = redis_value['value']

        self.storager_engines[storage_opcode.redis].set_storage_info('hset',redis_value)
        self.storager_engines[storage_opcode.redis].commit()

        self.storager_engines[storage_opcode.kafka_p].push_data(json.dumps(kafka_value))


    def process_data(self, pid, content):
        storage_method = self.storage_selector[pid]
        if storage_method:
            storage_method(content)
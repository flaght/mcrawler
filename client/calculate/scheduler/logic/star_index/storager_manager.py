# -*- coding: utf-8 -*-

'''
Created on 2017年5月23日

@author: kerry
'''

"""
用于处理新浪相关的存储
"""

from calculate.scheduler.storage.base_storager import BaseStorager
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

    def star_index(self, content):
        kafka_value = content[storage_opcode.kafka_p]
        self.storager_engines[storage_opcode.kafka_p].push_data(json.dumps(kafka_value))


# -*- coding: utf-8 -*-

"""
Created on 2016年11月19日

@author: kerry
"""

from analysis.scheduler.storage.enclosure.sqlite_manage_model import SQLLiteStorage
from analysis.scheduler.storage.enclosure.redis_manage_model import RedisManageModel
from analysis.scheduler.storage.enclosure.kafka_manage_model import KafkaConsumerManager
from analysis.scheduler.storage.enclosure.kafka_manage_model import KafkaProducerManager
from analysis.base.text_ext import TextExt as TextStorage
from analysis.common.operationcode import storage_opcode


class BaseStorager:
    @classmethod
    def create_storager(cls, stype, config):
        if stype == storage_opcode.sqlite:
            return SQLLiteStorage(config['name'], 0)
        elif stype == storage_opcode.mysql:
            return None
        elif stype == storage_opcode.text:
            return TextStorage(config['name'])
        elif stype ==storage_opcode.redis:
            return RedisManageModel(config['host'],config['port'])
        elif stype == storage_opcode.kafka_p:
            return KafkaProducerManager(None, config['host'],config['name'])
        elif stype == storage_opcode.kafka_c:
            return KafkaConsumerManager(None, config['host'], config['name'])
        else:
            return None

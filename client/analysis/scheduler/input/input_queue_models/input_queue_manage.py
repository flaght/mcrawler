# -.- coding:utf-8 -.-
"""
Created on 2016年12月18日

@author: kerry
"""
from analysis.common.operationcode import filer_opcode
from analysis.scheduler.input.input_queue_models.queue_kafka_manage import QueueKafkaManage


class InputQueueManager:

    """
    队列读取
    """

    @classmethod
    def create_queue_manager(cls, config):
        stype = config['type']
        if stype == filer_opcode.kafka:
            return QueueKafkaManage(config)
# -.- coding:utf-8 -.-
"""
Created on 2017年5月23日

@author: kerry
"""
from tools.common.operationcode import filer_opcode
from calculate.scheduler.input.input_queue_models.queue_kafka_manage import QueueKafkaManage


class InputQueueManager(object):

    """
    队列读取
    """

    @classmethod
    def create_queue_manager(cls, config):
        stype = config['type']
        if stype == filer_opcode.kafka:
            return QueueKafkaManage(config)
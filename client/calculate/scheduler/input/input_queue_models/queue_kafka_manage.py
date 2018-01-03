# -.- coding:utf-8 -.-
"""
Created on 2016年12月18日

@author: kerry
"""
import json
from tools.base.mlog import mlog
from kafka import KafkaConsumer


class QueueKafkaManage(object):
    """
    kafka管理
    """
    def __init__(self, config):
        self.client = None
        self.host = config['host']
        self.coname = config['name']
        self.consumer = KafkaConsumer(self.coname, auto_offset_reset='latest',
                                 bootstrap_servers=self.host,
                                 group_id='my-group')

    def __del__(self):
        self.consumer.close()


    def set_callback(self, callback):
        self.callback = callback

    def start(self):
        """
        连接取数据
        """
        while True:
            i = 0
            for message in self.consumer:
                json_info=""
                try:
                    json_info = json.loads(message[6])
                except Exception, e:
                    mlog.log().error(message)
                if len(json_info) > 0:
                    mlog.log().debug(json_info)
                    self.callback(json_info)
# -.- coding:utf-8 -.-
"""
Created on 2016年12月18日

@author: kerry
"""
import json
from analysis.base.mlog import mlog
from kafka import KafkaConsumer


class QueueKafkaManage():
    """
    kafka管理
    """

    """

    def __init__(self, client, host, coname):
        # threading.Thread.__init__(self, name='kafka_manage')
        self.client = client
        self.host = host
        self.coname = coname
        # self.setDaemon(True)
        # self.start()
    """
    def __init__(self, config):
        self.client = None
        self.host = config['host']
        self.coname = config['name']

    def set_callback(self, callback):
        self.callback = callback

    def start(self):
        """
        连接取数据
        """
        while True:
            consumer = KafkaConsumer(self.coname,auto_offset_reset='latest',
                                     bootstrap_servers=self.host,
                                     group_id='my-group')
            i = 0
            for message in consumer:
                json_info=""
                try:
                    json_info = json.loads(message[6])
                except Exception, e:
                    mlog.log().error(message)
                if len(json_info) > 0:
                    mlog.log().debug(json_info)
                    self.callback(json_info)



def main():

    #t = QueueKafkaManage(None, "61.147.114.85:9092,61.147.114.80:9092,61.147.114.81:9092",
    #                        "kafka_newsparser_algo")

    config = {'host':'61.147.114.85:9092,61.147.114.80:9092,61.147.114.81:9092','name':'newsparser_task_algo'}
    t = QueueKafkaManage(config)

    t.start()



if __name__ == '__main__':
    main()
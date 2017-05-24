# -.- coding:utf-8 -.-
"""
Created on 2016年7月28日

@author: kerry
"""
import json
from analysis.base.mlog import mlog
from kafka import KafkaConsumer,KafkaProducer
from kafka import SimpleClient, SimpleProducer, SimpleConsumer
from analysis.base.analysis_conf_manager import analysis_conf


class KafkaProducerManager(object):



    def __init__(self, client, host, coname):
        self.client = client
        self.host = host
        self.coname = coname
        self.producer = KafkaProducer(bootstrap_servers=self.host)

    def push_data(self, parmas_message):
        producer = self.producer
        producer.send(self.coname, parmas_message.encode('utf-8'))
        producer.flush()



class KafkaConsumerManager(object):
    """
    kafka管理
    """

    def __init__(self, client, host, coname):
        # threading.Thread.__init__(self, name='kafka_manage')
        self.client = client
        self.host = host
        self.coname = coname
        # self.setDaemon(True)
        # self.start()

    def set_callback(self, callback):
        self.callback = callback

    def process_data(self, data):
        name = data['key_name'] + data['pos_name'] + '.txt'
        ftp_url = '~/text_storage/' + data['key_name'] + '/' + data['pos_name']
        # ftp_manager_t.download(str(name), (ftp_url))

    def run(self):
        """
        连接取数据
        """
        while True:
            consumer = KafkaConsumer(bootstrap_servers=self.host)
            consumer.subscribe([self.coname])
            for message in consumer:
                try:
                    json_info = json.loads(message[6])
                    print json_info
                    #self.callback(json_info)
                except Exception, e:
                    mlog.log().error(e)



def main():
    t = KafkaProducerManager(None,"kafka.t.smartdata-x.com:9092","kafka_newsparser_algo_1005")

    t.push_data("jiaoha")

    '''
    t = KafkaConsumerManager(None, "kafka.t.smartdata-x.com:9092",
                             "kafka_newsparser_algo_1005")
    t.run()
    '''


if __name__ == '__main__':
    main()

kafka_consumer_t = KafkaConsumerManager(None, analysis_conf.kafka_info['host'],
                                       analysis_conf.kafka_info['name'])

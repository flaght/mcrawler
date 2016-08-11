# -.- coding:utf-8 -.-
'''
Created on 2016年7月28日

@author: kerry
'''
import threading, logging, time,json
from kafka import KafkaConsumer
from kafka import TopicPartition
from pykafka import KafkaClient
#from analysis.common.ftp_manager import ftp_manager_t
from analysis.base.analysis_conf_manager import analysis_conf



class KafkaConsumerManager():
    '''
    kafka管理
    '''
    def __init__(self, client, host,coname):
        #ftp_manager_t.connent()
        #threading.Thread.__init__(self, name='kafka_manage')
        self.client = client
        self.host = host
        self.coname = coname
        #self.setDaemon(True)
        #self.start()
        
    def set_callback(self,callback):
        self.callback = callback
        
    def process_data(self,data):
        name = data['key_name'] + data['pos_name']+'.txt'
        print name
        ftp_url = '~/text_storage/'+data['key_name'] +'/'+data['pos_name']
        print ftp_url
        #ftp_manager_t.download(str(name), (ftp_url))

    def run(self):
        '''
        连接取数据
        '''
        while True:
            consumer = KafkaConsumer(bootstrap_servers=self.host)
            consumer.subscribe([self.coname])
            print 'start'
            for message in consumer:
                try:
                    json_info = json.loads(message[6])
                    self.callback(json_info)
                    #self.process_data(json_info)
                except Exception,e:
                    print e

def main():
    
    t = KafkaConsumerManager(None,analysis_conf.kafka_info['host'],
                               analysis_conf.kafka_info['name'])
    t.run()
   # threads = [
    #    KafkaConsumer(None,'61.147.80.85:9092','algo_cralwer_kafka')
     #          ]
    #for t in threads:
     #   t.start()
    '''
    client = KafkaClient(hosts="61.147.80.245:9092")
    topic = client.topics['kafka_algo']
    consumer = topic.get_simple_consumer()
    for message in consumer:
        if message is not None:
            print message.offset, message.value
    '''
    #KafkaManage(None, '61.147.80.245')
    #while True:
     #   time.sleep(1)

if __name__ == '__main__':
    main()

kafka_consumer_t = KafkaConsumerManager(None,analysis_conf.kafka_info['host'],
                               analysis_conf.kafka_info['name'])
# -.- coding:utf-8 -.-
'''
Created on 2015年9月15日

@author: chenyitao
'''

import threading
import time
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from kid.common.kid_signal import KidSignal
from kid.common.sub_model_opcode import SubModelOpcode
from kid.model_manage.crawler_manage.crawler_manager import CrawlerManager
from kid.model_manage.sock_manage.sock_recv_manager import SockRecvManager
from kid.model_manage.sock_manage.sock_send_manager import SockSendManager
from kid.common import kid_setting


crawler_process = CrawlerProcess(settings)
crawler_process.join()


class SubModelManager(object):
    '''
    子模块管理
    '''
    
    thread_not_alive_send = 1
    thread_not_alive_crawler = 2
    
    def __init__(self, caller=None):
        self.crawler_process = crawler_process
        self.caller = caller
        self.signals_list = []
        self.sub_model_signal_selector = {}
        self.__registre_signal()
        self.sub_model_dict = {}
        self.__start_sub_model()
        self.daemon_thread = threading.Thread(target=self.__daemon, name='daemon_thread')
        self.daemon_thread.setDaemon(True)
        self.daemon_thread.start()

    def __registre_signal(self):
        self.sub_model_signal_selector[SubModelManager.thread_not_alive_send] = \
        self.__send_thread_not_alive
        self.sub_model_signal_selector[SubModelManager.thread_not_alive_crawler] = \
        self.__crawler_thread_not_alive

    def dispatch_msg(self, signal):
        method = self.sub_model_signal_selector[signal.opcode]
        if method:
            method(signal)

    def __send_thread_not_alive(self, signal=None):
        self.sub_model_dict[SubModelOpcode.sock_send_model] = SockSendManager(self)

    def __crawler_thread_not_alive(self, signal=None):
        self.sub_model_dict[SubModelOpcode.crawler_model] = CrawlerManager(self)

    def __start_sub_model(self):
        '''
        __start_sub_model
        '''
        self.sub_model_dict[SubModelOpcode.sock_recv_model] = SockRecvManager(self)
        self.sub_model_dict[SubModelOpcode.sock_send_model] = SockSendManager(self)
        self.sub_model_dict[SubModelOpcode.crawler_model] = CrawlerManager(self)
        self.sub_model_dict[SubModelOpcode.sub_model_manager] = self

    def __run(self):
        '''
        run
        '''
        while kid_setting.CONNECT:
            if len(self.signals_list):
                signal = self.signals_list.pop()
                self.__sock_work(signal)
            else:
                break

    def add_signal(self, signal=None):
        '''
        signal = KidSignal
        '''
        if signal:
            self.signals_list.append(signal)
            self.__run()

    def __sock_work(self, signal):
        '''
        __sock_work
        '''
        self.sub_model_dict[signal.sub_model_opcode].dispatch_msg(signal)

    def __daemon(self):
        while kid_setting.CONNECT:
            if not self.sub_model_dict[SubModelOpcode.sock_send_model].is_alive():
                self.add_signal(KidSignal(sub_model_opcode=SubModelOpcode.sub_model_manager,
                                          opcode=SubModelManager.thread_not_alive_send))
            if not self.sub_model_dict[SubModelOpcode.crawler_model].is_alive():
                self.add_signal(KidSignal(sub_model_opcode=SubModelOpcode.sub_model_manager,
                                          opcode=SubModelManager.thread_not_alive_crawler))
            time.sleep(1)

def main():
    '''
    test
    '''
    model_manager = SubModelManager()
    model_manager.add_signal(KidSignal(sub_model_opcode=SubModelOpcode.sock_recv_model))
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()

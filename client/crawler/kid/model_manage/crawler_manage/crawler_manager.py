# -.- coding:utf-8 -.-
'''
Created on 2015年9月8日

@author: chenyitao
'''

import threading
import time

from scrapy import signals
from scrapy.conf import settings
from Scrapy.spiders.single_spider import SingleSpider
from Scrapy.spiders.single_spider import signal_storage, signal_response_url_not_request_url,signal_requst_error
from kid.common import kid_setting
from kid.common.common_method import print_plus
from kid.common.crawler_opcode import CrawlerOpcode
from kid.common.kid_signal import KidSignal
from kid.common.sock_opcode import KidSockOpcode
from kid.common.sub_model_opcode import SubModelOpcode
from kid.model_manage.crawler_manage.cookies_manage import CookiesManager
from kid.model_manage.sock_manage.package.s_distribute_task import TaskInfo
from kid.model_manage.storage_manage.storage_manager import storage_manager


class CrawlerManager(threading.Thread):
    '''
    爬虫管理器
    '''

    def __init__(self, caller=None):
        '''
        Constructor
        '''
        threading.Thread.__init__(self, name='crawler_manager')
        self.setDaemon(True)
        self.task_cnt = 0
        self.spider = None
        self.caller = caller
        self.msg_list = []
        self.task_pool = []
        self.task_id_list = set()
        self.storage_list = []
        self.cookies_request_list = []
        self.fake_pool = {'ip': [], 'ua': []}
        self.cookies_manager = CookiesManager()
        self.crawler_signal_selector = {CrawlerOpcode.task_distribute: self.__manage_task,
                                        CrawlerOpcode.fake_ip: self.__setting_fake_info_IP,
                                        CrawlerOpcode.fake_ua: self.__setting_fake_info_UA,
                                        CrawlerOpcode.cookies: self.__setting_cookies}
        self.signals_list = {signals.spider_opened: self.__spider_opened,
                             signal_storage: self.__storage,
                             signal_requst_error: self.__request_error,
                             signal_response_url_not_request_url: self.__task_is_over_but_error}
        self.start()
        self.process = self.caller.crawler_process
        self.process.crawl(SingleSpider, [{'callback': self.spider_signals}])
        self.__timer = threading.Thread(target=self.__timer_manager,
                                        name='__timer_manager')
        self.__timer.setDaemon(True)
        self.__timer.start()

    def run(self):
        '''
        run
        '''
        while kid_setting.CONNECT:
            if len(self.msg_list):
                signal = self.msg_list.pop(0)
                self.__crawler_work(signal)
            else:
                time.sleep(0.5)
                self.__exec_task()
        self.process.stop()

    def dispatch_msg(self, msg):
        '''
        add msg
        '''
        if msg:
            self.msg_list.append(msg)


    def __request_error(self,dic):
        task = dic['task']
        self.__task_state_feedback(task, 10)

    def __storage(self, dic):
        task = dic['task']
        item = dic['item']
        key = item['basic']['key']
        if item is None:
            self.__task_state_feedback(task, 10)
        self.__task_state_feedback(task, 5)
        table_name = str(task.attr_id)
        if kid_setting.CRAWLER_TYPE == 2:
            table_name += '_detail'
        ret = storage_manager.write_data(item, table_name, task.storage)
        if not ret:
            print_plus('Storage result failed', level=2)
            self.__task_state_feedback(task, 7)
            return
        self.__task_state_feedback(task, 6)
        self.storage_list.append({'job_id': task.job_id,
                                  'attr_id': task.attr_id,
                                  'table': table_name,
                                  'key': key,
                                  'depth': task.depth,
                                  'cur_depth': task.cur_depth,
                                  'storage': task.storage})
        if len(self.storage_list) >= 10:
            self.__send_msg()

    def __task_is_over_but_error(self, dic):
        task = dic.get('task')
        if task:
            self.__task_state_feedback(task, 7)

    def __timer_manager(self):
        cnt = 1
        while kid_setting.CONNECT and self.is_alive():
            if cnt % 59 == 0:
                print_plus('__timer_manager is alive')
            if cnt % 29 == 0:
                self.cookies_request_list = []
            if cnt % 4 == 0:
                if len(self.storage_list) > 0:
                    self.__send_msg()
            if cnt % 14 == 0:
                task_cnt = 0
                mqs = self.spider.crawler.engine.slot.scheduler.mqs.queues.get(0, None)

                """
                修改成返回当前任务数
                """
                if mqs:
                    task_cnt = len(mqs.q)
                else:
                    task_cnt = 0

                """
                if mqs:
                    if len(mqs.q) < kid_setting.DEVICE_MAX_TASK:
                        task_cnt = kid_setting.DEVICE_MAX_TASK - len(mqs.q)
                else:
                    task_cnt = kid_setting.DEVICE_MAX_TASK

                """

                signal = KidSignal(sub_model_opcode=SubModelOpcode.sock_send_model,
                                   opcode=KidSockOpcode.c_task_num,
                                   data=task_cnt)
                self.caller.add_signal(signal)
                signal = KidSignal(sub_model_opcode=SubModelOpcode.sock_send_model,
                                   opcode=KidSockOpcode.c_achieve_UA_IP)
                self.caller.add_signal(signal)
            time.sleep(1)
            cnt += 1

    def __send_msg(self):
        signal = KidSignal(sub_model_opcode=SubModelOpcode.sock_send_model,
                           opcode=KidSockOpcode.c_data_save_info,
                           data=self.storage_list)
        self.caller.add_signal(signal)
        for storage_info in self.storage_list:
            task = TaskInfo()
            task.attr_id = storage_info['attr_id']
            task.job_id = storage_info['job_id']
            self.__task_state_feedback(task, 7)
        self.storage_list = []

    def __crawler_work(self, signal):
        '''
        work
        '''
        method = self.crawler_signal_selector[signal.opcode]
        if method:
            method(signal)

    def __manage_task(self, signal):
        '''
        task manager
        '''
        package = signal.data
        for task in package.tasks:
            if task.job_id in self.task_id_list:
                continue
            else:
                self.task_pool.append(task)
                self.task_id_list.add(task.job_id)
        for task in package.tasks:
            self.__task_state_feedback(task, 2)
        self.task_cnt += len(self.task_pool)
        try:
            self.__exec_task()
        except Exception, e:
            print_plus('%s' % e, True, True, 2)

    def __exec_task(self):
        '''
        exec task
        '''
        while len(self.task_pool):
            if self.spider.crawler.engine.slot.scheduler.mqs.queues:
                mqs = self.spider.crawler.engine.slot.scheduler.mqs.queues.get(0, None)
                if mqs and len(mqs.q) > 299:
                    signal = KidSignal(sub_model_opcode=SubModelOpcode.sock_send_model,
                                       opcode=KidSockOpcode.c_task_num,
                                       data=0)
                    self.caller.add_signal(signal)
                    time.sleep(3)
                    return
            if self.fake_pool['ip'] and self.fake_pool['ua']:
                task = self.task_pool.pop(0)
                if task.job_id in self.task_id_list:
                    self.task_id_list.remove(task.job_id)
                if task.is_login:
                    # put1 get2 post3 delete4
                    if task.attr_id not in self.cookies_manager.cookies.keys():
                        self.cookies_manager.cookies[task.attr_id] = []
                    if not len(self.cookies_manager.cookies[task.attr_id]):
                        if task.attr_id in self.cookies_request_list:
                            self.task_pool.append(task)
                            self.task_id_list.add(task.job_id)
                            time.sleep(0.5)
                            break
                        print_plus('get cookie attrid=%d' % task.attr_id)
                        signal = KidSignal(sub_model_opcode=SubModelOpcode.sock_send_model,
                                           opcode=KidSockOpcode.c_cookies,
                                           data=task.attr_id)
                        self.caller.add_signal(signal)
                        self.cookies_request_list.append(task.attr_id)
                        self.task_pool.append(task)
                        self.task_id_list.add(task.job_id)
                    if not len(self.cookies_manager.cookies[task.attr_id]):
                        time.sleep(0.5)
                        continue
                self.__task_state_feedback(task, 3)
                if task.depth != 0:
                    if kid_setting.CRAWLER_TYPE == 3:
                        self.task_pool.append(task)
                        self.task_id_list.add(task.job_id)
                        get_cookie_pop = True
                    else:
                        get_cookie_pop = False
                    self.spider.add_task({'task_info': task,
                                          'cookie': self.cookies_manager.get_cookie(task.attr_id,
                                                                                    get_cookie_pop)})
                self.task_cnt -= 1
                print_plus('task_id=>%d    url=>%s' % (task.job_id, task.url))
                self.__task_state_feedback(task, 4)
            else:
                break

    def __task_state_feedback(self, task, state):
        '''
        task state feedback to server
        '''
        if state != 4 and state != 7 and state != 10 and state != 2:
            return
        if kid_setting.CRAWLER_TYPE == 3:
            return
        sock_opcode = KidSockOpcode.c_distribute_task
        if kid_setting.CRAWLER_TYPE == 2:
            sock_opcode = KidSockOpcode.c_news_detail_state
        signal = KidSignal(sub_model_opcode=SubModelOpcode.sock_send_model,
                           opcode=sock_opcode,
                           data={'task_id': task.job_id,
                                 'state': state})
        self.caller.add_signal(signal)

    def __setting_fake_info_IP(self, signal):
        '''
        set fake ip
        '''
        package = signal.data
        self.fake_pool['ip'] = package.forge_info
        ip = []
        for fake_info in self.fake_pool['ip']:
            ip.append(fake_info.forgr_info)
        if len(ip):
            settings.set('HTTP_PROXY', ip)

    def __setting_fake_info_UA(self, signal):
        '''
        set fake ua
        '''
        package = signal.data
        self.fake_pool['ua'] = package.forge_info
        ua = []
        for fake_info in self.fake_pool['ua']:
            ua.append(fake_info.forgr_info)
        if len(ua):
            settings.set('USER_AGENT', ua)

    def __setting_cookies(self, signal):
        '''
        setting cookies
        '''
        cookies = []
        for cookie in signal.data.cookies:
            cookies.append(cookie.cookie)
        self.cookies_manager.set_cookies(signal.data.attr_id, 0, cookies)
        if signal.data.attr_id in self.cookies_request_list:
            self.cookies_request_list.remove(signal.data.attr_id)

    def spider_signals(self, spider, signal, params=None):
        '''
        spiders signals
        '''
        if signal not in self.signals_list.keys():
            return
        func = self.signals_list[signal]
        if func:
            func(params)

    def __spider_opened(self, params):
        '''
        @param params:
        @type params:params[0]==spider
        '''
        self.spider = params[0]


def main():
    '''
    test
    '''
    crawler_manager = CrawlerManager()  # @UnusedVariable


if __name__ == '__main__':
    main()

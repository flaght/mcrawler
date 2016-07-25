# -.- coding:utf-8 -.-
'''
Created on 2015年9月8日

@author: chenyitao
'''

import threading
import time

from kid.common import kid_setting
from kid.common.common_method import print_plus
from kid.common.kid_signal import KidSignal
from kid.common.sock_opcode import KidSockOpcode
from kid.model_manage.sock_manage.package.c_achieve_UA_IP import SockCUA_IP
from kid.model_manage.sock_manage.package.c_cookies import SockCCookies
from kid.model_manage.sock_manage.package.c_crawling_amount import SockCCrawlingAmount
from kid.model_manage.sock_manage.package.c_data_save_info import SockCDataSaveInfo
from kid.model_manage.sock_manage.package.c_data_save_info import StorageInfo
from kid.model_manage.sock_manage.package.c_device_info import SockCDeviceInfo
from kid.model_manage.sock_manage.package.c_distribute_task import SockCDistributeTask
from kid.model_manage.sock_manage.package.c_manager_register import SockCManagerREG
from kid.model_manage.sock_manage.package.c_task_num import SockCTaskNum
from kid.model_manage.sock_manage.package.sock_head import SockHead


class SockSendManager(threading.Thread):
    '''
    sock消息发送管理模块
    '''
    def __init__(self, caller):
        '''
        Constructor
        caller 宿主对象
        '''
        threading.Thread.__init__(self, name='sock_send_manager')
        self.setDaemon(True)
        self.caller = caller
        self.msg_list = []
        self.task_timer = None
        self.send_selector = {KidSockOpcode.s_heart:self.__heart,
                              KidSockOpcode.c_manager_register:self.__manager_registting,
                              KidSockOpcode.c_device_info:self.__device_info,
                              KidSockOpcode.c_distribute_task:self.__distribute_task,
                              KidSockOpcode.c_crawling_amount:self.__task_amount,
                              KidSockOpcode.c_data_save_info:self.__data_saved_info,
                              KidSockOpcode.c_achieve_UA_IP:self.__UA_IP,
                              KidSockOpcode.c_cookies:self.__get_cookies,
                              KidSockOpcode.c_news_detail_state:self.__distribute_task,
                              KidSockOpcode.c_task_num:self.__task_num}
        self.start()
        self.heart_cnt = 0
        self.heart = threading.Timer(15, self.__heart_timer)
        self.heart.setDaemon(True)
        self.heart.setName('heart')
        self.heart.start()

    def run(self):
        '''
        run
        '''
        while kid_setting.CONNECT:
            if len(self.msg_list):
                msg = self.msg_list.pop(0)
                self.__sock_work(msg)
            else:
                time.sleep(0.5)

    def dispatch_msg(self, signal=None):
        '''
        add msg
        '''
        if signal:
            self.msg_list.append(signal)

    def __sock_work(self, signal):
        '''
        work
        '''
        if signal.opcode not in self.send_selector.keys():
            print_plus('sock_err', file_line=True, level=2)
            return
        send_method = self.send_selector[signal.opcode]
        if send_method:
            send_method(signal)

    def __send(self, package):
        '''
        send to server
        '''
        if self.caller.caller and package:
            try:
                self.caller.caller.transport.getHandle().sendall(package)
            except Exception,e:
                err = 'send except:%s' % e
                print_plus(err, file_line=True, level=2)

    def __heart(self, signal):
        '''
        heart
        '''
        if self.heart_cnt%3 == 2:
            print_plus('send heart')
        self.heart_cnt += 1
        self.__send(signal.data)

    def __heart_timer(self):
        '''
        heart timer
        '''
        cnt = 0
        heart = SockHead()
        heart.opcode = KidSockOpcode.s_heart
        data = heart.make_package()
        while kid_setting.CONNECT:
            if cnt >= 15:
                msg = KidSignal(opcode=KidSockOpcode.s_heart, data=data)
                self.dispatch_msg(msg)
                cnt = 0
            else:
                cnt += 1
                time.sleep(1)

    def __manager_registting(self, signal):
        '''
        register manager
        '''
        package = SockCManagerREG()
        package_info = package.make_package()
        self.__send(package_info)
        print_plus('send SockCManagerREG')

    def __device_info(self, signal):
        '''
        feedback device info
        '''
        package = SockCDeviceInfo()
        package_info = package.make_package()
        self.__send(package_info)
        print_plus('send SockCDeviceInfo')

    def __distribute_task(self, signal):
        '''
        feedback task state
        '''
        package = SockCDistributeTask()
        if kid_setting.CRAWLER_TYPE == 2:
            package.opcode = KidSockOpcode.c_news_detail_state
        package.state = signal.data['state']
        package.job_id = signal.data['task_id']
        package_info = package.make_package()
        self.__send(package_info)

    def __task_num(self, signal):
        '''
        feedback task num
        '''
        package = SockCTaskNum()
        package.task_num = signal.data
        self.__send(package.make_package())
        print_plus('send SockCTaskNum: %d' % package.task_num)

    def __task_amount(self, signal):
        '''
        task process
        '''
        package = SockCCrawlingAmount()
        package_info = package.make_package()
        self.__send(package_info)
        print_plus('send SockCCrawlingAmount')

    def __data_saved_info(self, signal):
        '''
        storage info
        '''
        tasks_info = signal.data
        package = SockCDataSaveInfo()
        for info in tasks_info:
            storage_info = StorageInfo()
            storage_info.key = info['key']
            storage_info.name = info['table']
            storage_info.job_id = info['job_id']
            storage_info.attr_id = info['attr_id']
            storage_info.depth = info['depth']
            storage_info.cur_depth = info['cur_depth']
            package.storages.append(storage_info)
        if info['storage'] == 3:
            package.opcode = KidSockOpcode.c_ftp_save_info
        package_info = package.make_package()
        self.__send(package_info)
        print_plus('send SockCDataSaveInfo [%d][%d]' % (len(package.storages),
                                                        len(package_info)))

    def __UA_IP(self, signal):
        '''
        get fake ua ip
        '''
        ua_ip = SockCUA_IP()
        ua_ip.state = 1
        ua_ip.num = 5
        package = ua_ip.make_package()
        self.__send(package)
        ua_ip.state = 2
        package = ua_ip.make_package()
        self.__send(package)
        if self.heart_cnt%3 == 2:
            print_plus('send UA IP')
        def task():
            package = SockHead()
            package.type = 1
            package.opcode = 20000
            self.__send(package.make_package())
            print_plus('send get task')
        if self.task_timer:
            return
        self.task_timer = threading.Timer(10, task)
        self.task_timer.setName(True)
        self.setName('get_task_timer')
        self.task_timer.start()

    def __get_cookies(self, signal):
        cookies = SockCCookies()
        cookies.amount = 5
        cookies.attr_id = signal.data
        package_info = cookies.make_package()
        print_plus('send SockCCookies:%d' % cookies.attr_id)
        self.__send(package_info)

if __name__ == '__main__':
    '''
with open('stream.log', 'a') as f:
        str_hex = '%s\n' % str(time.time())
        package_len = struct.unpack('=H', package[:2])[0]
        sock_opcode = struct.unpack('=H', package[6:8])[0]
        str_hex += ('len:%d  opcode:%d\n' % (package_len, sock_opcode))
        for index,c in enumerate(package):
            str_hex += ('%02x ' % ord(c))
            if (index+1) % 4 == 0:
                str_hex += '\n'
        str_hex += '\n\n'
        f.write(str_hex)
    '''
    pass

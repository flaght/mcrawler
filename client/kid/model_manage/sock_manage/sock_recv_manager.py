# -.- coding:utf-8 -.-
'''
Created on 2015年9月7日

@author: chenyitao
'''

import struct

from kid.common import common_method
from kid.common.common_method import print_plus
from kid.common.crawler_opcode import CrawlerOpcode
from kid.common.device_manager import current_device_manager
from kid.common.kid_signal import KidSignal
from kid.common.sock_opcode import KidSockOpcode
from kid.common.sub_model_opcode import SubModelOpcode
from kid.model_manage.sock_manage.package.c_achieve_UA_IP import SockCUA_IP
from kid.model_manage.sock_manage.package.s_IP_info import SockSCrawlerIP
from kid.model_manage.sock_manage.package.s_UA_info import SockSCrawlerUA
from kid.model_manage.sock_manage.package.s_cookies import SockSCookies
from kid.model_manage.sock_manage.package.s_crawling_amount import SockSCrawlingAmount
from kid.model_manage.sock_manage.package.s_device_info import SockSDeviceInfo
from kid.model_manage.sock_manage.package.s_distribute_task import SockSDistributeTask
from kid.model_manage.sock_manage.package.s_error import SockSError
from kid.model_manage.sock_manage.package.s_manager_register import SockSManagerREG
from kid.model_manage.sock_manage.package.sock_head import SockHead


class SockRecvManager(object):
    '''
    socket管理模块
    '''

    def __init__(self, caller):
        '''
        Constructor
        caller:宿主对象
        '''
        self.caller = caller
        self.buffer = ''
        self.num = 0
        self.recv_selector = {KidSockOpcode.s_heart:self.__heart,
                              KidSockOpcode.s_error_code:self.__error,
                              KidSockOpcode.s_manager_register:self.__manager_reg_success,
                              KidSockOpcode.s_device_info:self.__getting_device_info,
                              KidSockOpcode.s_distribute_task:self.__distribute_task,
                              KidSockOpcode.s_crawling_amount:self.__task_process,
                              KidSockOpcode.s_IP_info:self.__dispatch_IP,
                              KidSockOpcode.s_UA_info:self.__dispatch_UA,
                              KidSockOpcode.s_cookies:self.__cookies,
                              KidSockOpcode.s_news_deatil_task:self.__distribute_task}

    def __run(self):
        '''
        run
        '''
        while len(self.buffer) > 2:
            buffer_len = len(self.buffer)
            package_len = struct.unpack('=H', self.buffer[0:2])[0]
            if (package_len == 0 and buffer_len > 0) or package_len > 8192:
                self.caller.caller.transport.loseConnection()
                break
            if package_len < SockHead.sock_head_len:
                self.caller.caller.transport.loseConnection()
                break
            if package_len > buffer_len:
                break
            (data_len,
             is_compress,
             data) = struct.unpack('=HB%ds' % (package_len-3),
                                   self.buffer[0:package_len])
            if buffer_len >= data_len:
                buf = ''
                if is_compress == 0:
                    buf = self.buffer[0:package_len]
                elif is_compress == 1:
                    buf = common_method.decompress_package(data)
                package_head = SockHead(buf[0:SockHead.sock_head_len])
                package = buf[0:package_len]
                self.buffer = self.buffer[package_len:]
                self.__sock_work(package_head, package)

    def dispatch_msg(self, signal):
        '''
        add msg
        '''
        if signal and signal.data:
            self.buffer += signal.data
            self.__run()

    def __sock_work(self, package_head, package):
        '''
        work
        '''
        if package_head.opcode not in self.recv_selector.keys():
            self.caller.caller.transport.loseConnection()
            return
        recv_method = self.recv_selector[package_head.opcode]
        if recv_method:
            recv_method(package)

    def __add_signal(self, signal):
        '''
        add signal
        '''
        self.caller.add_signal(signal)

    def __heart(self, package):
        '''
        heart
        '''
        signal = KidSignal(sub_model_opcode=SubModelOpcode.sock_send_model,
                           opcode=KidSockOpcode.s_heart,
                           data=package)
        self.__add_signal(signal)

    def __error(self, package):
        error = SockSError(package)
        print_plus('sock error:%d' % error.error_code)

    def __manager_reg_success(self, package):
        '''
        reg success
        '''
        package_info = SockSManagerREG(package)
        current_device_manager.set_manager_id(package_info.manager_id)
        current_device_manager.set_token(package_info.token)
        print_plus('recv SockSManagerREG')
        self.__getting_UA_IP()

    def __getting_device_info(self, package):
        '''
        get device info
        '''
        package_info = SockSDeviceInfo(package)
        print package_info
        print_plus('recv SockSDeviceInfo')
        # TODO 发送设备当前使用情况
        signal = KidSignal(sub_model_opcode=SubModelOpcode.sock_send_model,
                           opcode=KidSockOpcode.c_device_info)
        self.__add_signal(signal)

    def __distribute_task(self, package):
        '''
        distribute task
        '''
        package_info = SockSDistributeTask(package)
        signal = KidSignal(sub_model_opcode=SubModelOpcode.crawler_model,
                           opcode=CrawlerOpcode.task_distribute,
                           data=package_info)
        self.__add_signal(signal)
        print_plus('recv SockSDistributeTask')

    def __task_process(self, package):
        '''
        get task process
        '''
        package_info = SockSCrawlingAmount(package)
        print package_info.opcode
        print package_info.manager_id
        print package_info.job_id
        print_plus('recv SockSCrawlingAmount')

    def __dispatch_IP(self, package):
        '''
        got fake ip
        '''
        package_info = SockSCrawlerIP(package)
        signal = KidSignal(sub_model_opcode=SubModelOpcode.crawler_model,
                           opcode=CrawlerOpcode.fake_ip,
                           data=package_info)
        self.__add_signal(signal)

    def __dispatch_UA(self, package):
        '''
        got fake ua
        '''
        package_info = SockSCrawlerUA(package)
        signal = KidSignal(sub_model_opcode=SubModelOpcode.crawler_model,
                           opcode=CrawlerOpcode.fake_ua,
                           data=package_info)
        self.__add_signal(signal)

    def __getting_UA_IP(self, params=None):
        '''
        get fake ua ip
        '''
        ua_ip = SockCUA_IP()
        ua_ip.state = 1
        ua_ip.num = 5
        signal = KidSignal(sub_model_opcode=SubModelOpcode.sock_send_model,
                           opcode=KidSockOpcode.c_achieve_UA_IP,
                           data=ua_ip.make_package())
        self.__add_signal(signal)
        ua_ip.state = 2
        signal.data = ua_ip.make_package()
        self.__add_signal(signal)

    def __get_fake_ip(self):
        '''
        定时获取伪造ip
        '''
        ua_ip = SockCUA_IP()
        ua_ip.state = 1
        ua_ip.num = 5
        signal = KidSignal(sub_model_opcode=SubModelOpcode.sock_send_model,
                           opcode=KidSockOpcode.c_achieve_UA_IP,
                           data=ua_ip.make_package())
        self.__add_signal(signal)

    def __cookies(self, package):
        cookies = SockSCookies(package)
        signal = KidSignal(sub_model_opcode=SubModelOpcode.crawler_model,
                           opcode=CrawlerOpcode.cookies,
                           data=cookies)
        self.__add_signal(signal)
        print_plus('recv SockSCookies')

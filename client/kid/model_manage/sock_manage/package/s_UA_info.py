# -.- coding:utf-8 -.-
'''
Created on 2015年9月7日

@author: chenyitao
'''

import struct

from kid.common.device_manager import current_device_manager
from kid.common.sock_opcode import KidSockOpcode
from kid.model_manage.sock_manage.package.sock_head import SockHead


class UAInfo(object):
    '''
    UA/IP属性
    '''
    __struct_analysis_rule = '=IB251s'
    ua_info_length = struct.calcsize(__struct_analysis_rule)

    def __init__(self, params=None):
        if not params:
            self.id = 0
            self.type = 0
            self.forgr_info = ''
            return
        (self.id,
        self.type,
        self.forgr_info) = struct.unpack(self.__struct_analysis_rule, params)
        self.forgr_info = self.forgr_info.rstrip('\x00')

    def make_package(self):
        '''
        make package
        '''
        package_body = struct.pack(self.__struct_analysis_rule,
                                   self.id,
                                   self.type,
                                   self.forgr_info)
        return package_body

class SockSCrawlerUA(SockHead):
    '''
    向客户端发送UA、IP
    '''
    __struct_analysis_rule = '=IQ%ds'
    __struct_analysis_rule_no_kv = '=IQ'

    def __init__(self, params=None):
        if not params:
            #head
            super(self.__class__, self).__init__()
            self.opcode = KidSockOpcode.s_UA_info
            self.type = 1
            # body
            self.manager_id = current_device_manager.get_manager_id()
            self.job_id = 0
            self.forge_info = []
            return
        params = super(self.__class__, self).compress_encrypt(params, False)
        str_head = params[0:SockHead.sock_head_len]
        str_body = params[SockHead.sock_head_len:]
        super(self.__class__, self).__init__(str_head)
        (self.manager_id,
        self.job_id,
        str_body) = struct.unpack(self.__struct_analysis_rule % (len(str_body)-4-8),
                                  str_body)
        self.forge_info = []
        while str_body:
            str_task = str_body[0:UAInfo.ua_info_length]
            forge_info = UAInfo(str_task)
            self.forge_info.append(forge_info)
            str_body = str_body[UAInfo.ua_info_length:]

    def make_package(self):
        package_forge_info = ''
        for forge_info in self.forge_info:
            package_forge_info += forge_info.make_package()
        package_body = struct.pack(self.__struct_analysis_rule % len(package_forge_info),
                                   self.manager_id,
                                   self.job_id,
                                   package_forge_info)
        self.make_checksum(len(package_body))
        package_head = super(self.__class__, self).make_package()
        return self.compress_encrypt(package_head+package_body)

def main():
    '''
    test
    '''
    # 封包
    package = SockSCrawlerUA()
    package.manager_id = 127
    package.job_id = 14
    info = UAInfo()
    info.id = 5
    info.type = 2
    info.forgr_info = '12345678901234567890a'
    package.forge_info = [UAInfo(info.make_package()),
                          UAInfo(info.make_package()),
                          UAInfo(info.make_package()),
                          UAInfo(info.make_package()),
                          UAInfo(info.make_package())]
    package_info = package.make_package()
    # 解包
    sock_crawler_manager_reg = SockSCrawlerUA(package_info)
    print sock_crawler_manager_reg

if __name__ == '__main__':
    main()

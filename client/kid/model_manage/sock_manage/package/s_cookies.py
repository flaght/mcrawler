# -.- coding:utf-8 -.-
'''
Created on 2015年11月16日

@author: chenyitao
'''

import struct

from kid.common.device_manager import current_device_manager
from kid.common.sock_opcode import KidSockOpcode
from kid.model_manage.sock_manage.package.sock_head import SockHead


class Coookie(object):
    '''
    Cookie属性
    '''
    # 由 H 来确定长度
    __struct_analysis_rule = '=H%ds'

    def __init__(self, params=None):
        if not params:
            self.len = 0
            self.cookie = ''
            return
        (self.len,
        self.cookie) = struct.unpack(self.__struct_analysis_rule % (len(params)-2),
                                     params)

    def make_package(self):
        '''
        make package
        '''
        package_body = struct.pack(self.__struct_analysis_rule,
                                   self.len,
                                   self.cookie)
        return package_body

class SockSCookies(SockHead):
    '''
    向客户端发送IP
    '''
    __struct_analysis_rule = '=IQ%ds'
    __struct_analysis_rule_no_kv = '=IQ'

    def __init__(self, params=None):
        if not params:
            #head
            super(self.__class__, self).__init__()
            self.opcode = KidSockOpcode.s_cookies
            self.type = 1
            # body
            self.manager_id = current_device_manager.get_manager_id()
            self.attr_id = 0
            self.cookies = []
            return
        params = super(self.__class__, self).compress_encrypt(params, False)
        str_head = params[0:SockHead.sock_head_len]
        str_body = params[SockHead.sock_head_len:]
        super(self.__class__, self).__init__(str_head)
        (self.manager_id,
         self.attr_id,
         str_body) = struct.unpack(self.__struct_analysis_rule % (len(str_body)-4-8),
                                     str_body)
        self.cookies = []
        while str_body:
            cookie_len = struct.unpack('=H', str_body[:2])[0]
            str_cookie = str_body[0:cookie_len+2]
            cookie_info = Coookie(str_cookie)
            self.cookies.append(cookie_info)
            str_body = str_body[cookie_len+2:]

    def make_package(self):
        package_cookies = ''
        for cookie in self.cookies:
            package_cookies += cookie.make_package()
        package_body = struct.pack(self.__struct_analysis_rule % len(package_cookies),
                                   self.manager_id,
                                   self.attr_id,
                                   package_cookies)
        self.make_checksum(len(package_body))
        package_head = super(self.__class__, self).make_package()
        return self.compress_encrypt(package_head+package_body)

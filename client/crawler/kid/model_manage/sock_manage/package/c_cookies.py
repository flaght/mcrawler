# -.- coding:utf-8 -.-
'''
Created on 2015年11月16日

@author: chenyitao
'''

import struct

from kid.common.device_manager import current_device_manager
from kid.common.sock_opcode import KidSockOpcode
from kid.model_manage.sock_manage.package.sock_head import SockHead


class SockCCookies(SockHead):
    '''
    获取cookies
    '''

    __struct_analysis_rule = '=I32sQB'

    def __init__(self, params=None):
        if params == None:
            # head
            super(self.__class__, self).__init__()
            self.opcode = KidSockOpcode.c_cookies
            self.type = 1
            # body
            self.manager_id = current_device_manager.get_manager_id()
            self.token = current_device_manager.get_token()
            self.attr_id = 0
            self.amount = 0
            return
        params = super(self.__class__, self).compress_encrypt(params, False)
        str_head = params[0:SockHead.sock_head_len]
        str_body = params[SockHead.sock_head_len:]
        super(self.__class__, self).__init__(str_head)
        (self.manager_id,
         self.token,
         self.attr_id,
         self.amount) = struct.unpack(self.__struct_analysis_rule, str_body)
        
    def make_package(self):
        package_body = struct.pack(self.__struct_analysis_rule,
                                   self.manager_id,
                                   self.token,
                                   self.attr_id,
                                   self.amount)
        self.make_checksum(len(package_body))
        package_head = super(self.__class__, self).make_package()
        return self.compress_encrypt(package_head+package_body)

if __name__ == '__main__':
    pass

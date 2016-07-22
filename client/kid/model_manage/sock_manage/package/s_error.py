# -.- coding:utf-8 -.-
'''
Created on 2015年9月17日

@author: chenyitao
'''

import struct

from kid.common.sock_opcode import KidSockOpcode
from kid.model_manage.sock_manage.package.sock_head import SockHead


class SockSError(SockHead):
    '''
    sock错误返回
    '''
    __struct_analysis_rule = '=i'

    def __init__(self, params=None):
        if params == None:
            #head
            super(self.__class__, self).__init__()
            self.opcode = KidSockOpcode.s_error_code
            self.type = 1
            # body
            self.error_code = -8888
            return
        params = super(self.__class__, self).compress_encrypt(params, False)
        str_head = params[0:SockHead.sock_head_len]
        str_body = params[SockHead.sock_head_len:]
        super(self.__class__, self).__init__(str_head)
        (self.error_code) = struct.unpack(self.__struct_analysis_rule, str_body)

    def make_package(self):
        package_body = struct.pack(self.__struct_analysis_rule,
                                   self.error_code)
        self.make_checksum(len(package_body))
        package_head = super(self.__class__, self).make_package()
        return self.compress_encrypt(package_head+package_body)

def main():
    '''
    test
    '''
    # 封包
    package = SockSError()
    package_info = package.make_package()
    # 解包
    sock_crawler_manager_reg = SockSError(package_info)
    print sock_crawler_manager_reg

if __name__ == '__main__':
    main()
    
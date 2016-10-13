# -.- coding:utf-8 -.-
'''
Created on 2015年9月7日

@author: chenyitao
'''

import struct

from kid.common import kid_setting
from kid.common.device_manager import current_device_manager
from kid.common.sock_opcode import KidSockOpcode
from kid.model_manage.sock_manage.package.sock_head import SockHead


class SockCManagerREG(SockHead):
    '''
    爬虫管理注册
    '''
    __struct_analysis_rule = '=h8s16s'

    def __init__(self, params=None):
        if params == None:
            #head
            super(self.__class__, self).__init__()
            self.opcode = KidSockOpcode.c_manager_register
            self.type = 1
            # body
            self.level = kid_setting.DEVICE_LEVEL
            self.password = kid_setting.DEVICE_PASSWD
            self.mac =  "A0999B04D047"#current_device_manager.get_mac_address()
            return
        params = super(self.__class__, self).compress_encrypt(params, False)
        str_head = params[0:SockHead.sock_head_len]
        str_body = params[SockHead.sock_head_len:]
        super(self.__class__, self).__init__(str_head)
        (self.level,
        self.password,
        self.mac) = struct.unpack(self.__struct_analysis_rule, str_body)

    def make_package(self):
        package_body = struct.pack(self.__struct_analysis_rule,
                                   self.level,
                                   self.password,
                                   self.mac)
        self.make_checksum(len(package_body))
        package_head = super(self.__class__, self).make_package()
        return self.compress_encrypt(package_head+package_body)

def main():
    '''
    test
    '''
    # 封包
    package = SockCManagerREG()
    package.is_compress_encrypt = 0
    package_info = package.make_package()
    # 解包
    sock_crawler_manager_reg = SockCManagerREG(package_info)
    print sock_crawler_manager_reg

if __name__ == '__main__':
    main()

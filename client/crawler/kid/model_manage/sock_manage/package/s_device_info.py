# -.- coding:utf-8 -.-
'''
Created on 2015年9月7日

@author: chenyitao
'''

from kid.common.sock_opcode import KidSockOpcode
from kid.model_manage.sock_manage.package.sock_head import SockHead


class SockSDeviceInfo(SockHead):
    '''
    获取客户端设备当前使用信息
    '''

    def __init__(self, params=None):
        if params == None:
            #head
            super(self.__class__, self).__init__()
            self.opcode = KidSockOpcode.s_device_info
            self.type = 1
            # body
            # 无包体
            return
        params = super(self.__class__, self).compress_encrypt(params, False)
        str_head = params[0:SockHead.sock_head_len]
        super(self.__class__, self).__init__(str_head)

    def make_package(self):
        package_body = ''
        self.make_checksum(len(package_body))
        package_head = super(self.__class__, self).make_package()
        return self.compress_encrypt(package_head+package_body)

def main():
    '''
    test
    '''
    # 封包
    package = SockSDeviceInfo()
    package_info = package.make_package()
    # 解包
    sock_crawler_manager_reg = SockSDeviceInfo(package_info)
    print sock_crawler_manager_reg

if __name__ == '__main__':
    main()

# -.- coding:utf-8 -.-
'''
Created on 2015年9月7日

@author: chenyitao
'''

import struct

from kid.common.device_manager import current_device_manager
from kid.common.sock_opcode import KidSockOpcode
from kid.model_manage.sock_manage.package.sock_head import SockHead


class SockCDistributeTask(SockHead):
    '''
    向服务端反馈任务分配结果
    '''
    __struct_analysis_rule = '=I32sQB'

    def __init__(self, params=None):
        if params == None:
            #head
            super(self.__class__, self).__init__()
            self.opcode = KidSockOpcode.c_distribute_task
            self.type = 1
            # body
            self.manager_id = current_device_manager.get_manager_id()
            self.token = current_device_manager.get_token()
            self.job_id = 0
            self.state = 0
            return
        params = super(self.__class__, self).compress_encrypt(params, False)
        str_head = params[0:SockHead.sock_head_len]
        str_body = params[SockHead.sock_head_len:]
        super(self.__class__, self).__init__(str_head)
        (self.manager_id,
        self.token,
        self.job_id,
        self.state) = struct.unpack(self.__struct_analysis_rule, str_body)

    def make_package(self):
        package_body = struct.pack(self.__struct_analysis_rule,
                                   self.manager_id,
                                   self.token,
                                   self.job_id,
                                   self.state)
#         self.make_checksum(len(package_body))
        self.body_len = len(package_body)
        package_head = super(self.__class__, self).make_package()
        self.checksum = self.u_short_checksum(package_head+package_body)
        return self.compress_encrypt(package_head+package_body)

def main():
    '''
    test
    '''
    # 封包
    package = SockCDistributeTask()
    package.manager_id = 127
    package.token = '0123456789abcdef0123456789ABCDEF'
    package.job_id = 13
    package.state = 1
    package_info = package.make_package()
    # 解包
    sock_crawler_manager_reg = SockCDistributeTask(package_info)
    print sock_crawler_manager_reg

if __name__ == '__main__':
    main()

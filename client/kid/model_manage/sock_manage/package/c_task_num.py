# -.- coding:utf-8 -.-
'''
Created on 2016年1月15日

@author: chenyitao
'''

import struct

from kid.common.device_manager import current_device_manager
from kid.common.sock_opcode import KidSockOpcode
from kid.model_manage.sock_manage.package.sock_head import SockHead


class SockCTaskNum(SockHead):
    '''
    向服务端反馈未完成任务个数
    '''

    __struct_analysis_rule = '=IH'

    def __init__(self, params=None):
        if params == None:
            #head
            super(self.__class__, self).__init__()
            self.opcode = KidSockOpcode.c_task_num
            self.type = 1
            # body
            self.manager_id = current_device_manager.get_manager_id()
            self.task_num = 0
            return
        params = super(self.__class__, self).compress_encrypt(params, False)
        str_head = params[0:SockHead.sock_head_len]
        str_body = params[SockHead.sock_head_len:]
        super(self.__class__, self).__init__(str_head)
        (self.manager_id,
        self.task_num) = struct.unpack(self.__struct_analysis_rule, str_body)

    def make_package(self):
        package_body = struct.pack(self.__struct_analysis_rule,
                                   self.manager_id,
                                   self.task_num)
        self.make_checksum(len(package_body))
        package_head = super(self.__class__, self).make_package()
        return self.compress_encrypt(package_head+package_body)

def main():
    '''
    test
    '''
    # 封包
    package = SockCTaskNum()
    package.manager_id = 127
    package.num = 13
    data = package.make_package()
    # 解包
    package_info = SockCTaskNum(data)
    print package_info

if __name__ == '__main__':
    main()

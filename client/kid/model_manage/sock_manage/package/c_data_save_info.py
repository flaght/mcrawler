# -.- coding:utf-8 -.-
'''
Created on 2015年9月7日

@author: chenyitao
'''

import struct

from kid.common.device_manager import current_device_manager
from kid.common.sock_opcode import KidSockOpcode
from kid.model_manage.sock_manage.package.sock_head import SockHead


class StorageInfo(object):
    '''
    存储属性
    '''
    __struct_analysis_rule = '=QQBB32s256s'
    storage_info_length = struct.calcsize(__struct_analysis_rule)

    def __init__(self, params=None):
        if not params:
            self.job_id = 0
            self.attr_id = 0
            self.depth = 0
            self.cur_depth = 0
            self.name = ''
            self.key = ''
            return
        (self.job_id,
        self.attr_id,
        self.depth,
        self.cur_depth,
        self.name,
        self.key) = struct.unpack(self.__struct_analysis_rule, params)

    def make_package(self):
        '''
        make package
        '''
        package_body = struct.pack(self.__struct_analysis_rule,
                                   self.job_id,
                                   self.attr_id,
                                   self.depth,
                                   self.cur_depth,
                                   self.name,
                                   self.key)
        return package_body

class SockCDataSaveInfo(SockHead):
    '''
    向服务端提交爬取内容信息（存储）
    '''
    __struct_analysis_rule = '=I32s%ds'
    __struct_analysis_rule_no_kv = '=I32s'

    def __init__(self, params=None):
        if params == None:
            #head
            super(self.__class__, self).__init__()
            self.opcode = KidSockOpcode.c_data_save_info
            self.type = 1
            # body
            self.manager_id = current_device_manager.get_manager_id()
            self.token = current_device_manager.get_token()
            self.storages = []
            return
        params = super(self.__class__, self).compress_encrypt(params, False)
        str_head = params[0:SockHead.sock_head_len]
        str_body = params[SockHead.sock_head_len:]
        str_no_storages = str_body[0:struct.calcsize(self.__struct_analysis_rule_no_kv)]
        super(self.__class__, self).__init__(str_head)
        (self.manager_id,
        self.token) = struct.unpack(self.__struct_analysis_rule_no_kv, str_no_storages)
        str_storages = str_body[struct.calcsize(self.__struct_analysis_rule_no_kv):]
        self.storages = []
        while str_storages:
            str_storage = str_storages[0:StorageInfo.storage_info_length]
            storage = StorageInfo(str_storage)
            self.storages.append(storage)
            str_storages = str_storages[StorageInfo.storage_info_length:]

    def make_package(self):
        package_storages = ''
        for storage in self.storages:
            package_storages += storage.make_package()
        package_body = struct.pack(self.__struct_analysis_rule % len(package_storages),
                                   self.manager_id,
                                   self.token,
                                   package_storages)
        self.make_checksum(len(package_body))
        package_head = super(self.__class__, self).make_package()
        return self.compress_encrypt(package_head+package_body)

def main():
    '''
    test
    '''
    # 封包
    package = SockCDataSaveInfo()
    package.manager_id = 127
    package.token = 'sasasaasasas'
    storage_info = StorageInfo()
    storage_info.job_id = 1
    storage_info.name = 'asasasas'
    storage_info.key = '123123132'
    package.storages = [StorageInfo(storage_info.make_package()),
                        StorageInfo(storage_info.make_package()),
                        StorageInfo(storage_info.make_package()),
                        StorageInfo(storage_info.make_package()),
                        StorageInfo(storage_info.make_package())]
    package_info = package.make_package()
    # 解包
    sock_crawler_manager_reg = SockCDataSaveInfo(package_info)
    print sock_crawler_manager_reg

if __name__ == '__main__':
    main()

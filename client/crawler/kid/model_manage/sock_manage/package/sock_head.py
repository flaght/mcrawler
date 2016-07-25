# -.- coding:utf-8 -.-
'''
Created on 2015年9月7日

@author: chenyitao
'''

import os
import struct
import time

from kid.common import common_method
from kid.common import kid_setting


class SockHead(object):
    '''
    socket包头
    '''
    __head_analysis_rule = '=HBBHHHIQI'
    sock_head_len = struct.calcsize(__head_analysis_rule)

    def __init__(self, params=None):
        if params == None:
            self.len = 0
            self.body_len = 0
            self.is_compress_encrypt = 0
            self.type = 0
            self.time = int(time.time())
            self.msg_id = int(os.urandom(8).encode('hex'), 16)
            self.reserve = 0
            self.checksum = 0
            return
        package_info = struct.unpack(self.__head_analysis_rule, params)
        self.len = package_info[0]
        self.is_compress_encrypt = package_info[1]
        self.type = package_info[2]
        self.checksum = package_info[3]
        self.opcode = package_info[4]
        self.body_len = package_info[5]
        self.time = package_info[6]
        self.msg_id = package_info[7]
        self.reserve = package_info[8]

    def make_package(self):
        '''
        make package
        '''
        self.len = self.sock_head_len + self.body_len
#         print self.len
        package_head = struct.pack(self.__head_analysis_rule,
                                   self.len,
                                   self.is_compress_encrypt,
                                   self.type,
                                   self.checksum,
                                   self.opcode,
                                   self.body_len,
                                   self.time,
                                   self.msg_id,
                                   self.reserve)
        return package_head

    def make_checksum(self, body_len):
        '''
        make checksum
        '''
        self.body_len = body_len
        self.checksum = 12345

    def u_short_checksum(self, data):
        '''
        char_checksum 按字节计算校验和。每个字节被翻译为无符号整数
        @param data: 字节串
        @param byteorder: 大/小端
        '''
        length = len(data)
        checksum = 0
        index = 0
        cnt = 0
        while length > 1:
            cnt += 1
            short_value = struct.unpack('=H', data[index:index+2])[0]
            checksum += short_value
            length -= 2
            index += 2
        if length == 1:
            checksum += struct.unpack('=B', data[-1])[0]
        while checksum>>16:
            checksum = (checksum>>16)+(checksum&0xffff)
        if checksum==0xffff:
            return checksum
        else:
            return ~checksum

    def compress_encrypt(self, package, is_compress_encrypt=True):
        '''
        compress
        '''
        package_info = struct.unpack('=HB%ds' % len(package[3:]), package)
        if 0 == package_info[1]: # 不压缩、不加密
            return package
        elif 1 == package_info[1]: # 压缩、不加密
            if is_compress_encrypt:
                package = common_method.compress_package(package_info)
            else:
                package = common_method.decompress_package(package_info)
        elif 2 == package_info[1]: # 不压缩、加密
            pass # TODO 加密
        elif 3 == package_info[1]: # 压缩、加密
            # TODO 加密
            if is_compress_encrypt:
                package = common_method.compress_package(package_info)
            else:
                package = common_method.decompress_package(package_info)
        return package

if __name__ == "__main__":
    head = SockHead()
    ret = head.u_short_checksum('1283784816481helo!')
    print hex(ret)
    print ret
    from kid.common.tea_model import encrypt, decrypt
    en = encrypt('1283784816481helo!', '1234567890abcdea')
    print en
    i = 0
    for c in en:
        print '%d: 0x%X' % (i, ord(c))
        i += 1
    de = decrypt(en, '1234567890abcdea')
    print de

# -.- coding:utf-8 -.-
'''
Created on 2015年9月15日

@author: chenyitao
'''

import struct
import sys
import time
import zlib


def enum(**enums):
    '''
    动态生成Enum
    '''
    return type('Enum', (), enums)

def compress_package(package_info):
    '''
    sock包压缩
    '''
    str_cmp = zlib.compress(package_info[2], 2)
    package = struct.pack('=HB%ds' % len(str_cmp),
                          len(str_cmp)+3,
                          package_info[1],
                          str_cmp)
    return package

def decompress_package(package_info):
    '''
    sock包解压
    '''
    str_cmp = zlib.decompress(package_info[2])
    package = struct.pack('=HB%ds' % len(str_cmp),
                          len(str_cmp)+3,
                          package_info[1],
                          str_cmp)
    return package

def print_plus(content=None, current_time=True, file_line=False, level=0):
    '''
    @param content:……
    @type content:str
    @param current_time:True=on False=off
    @type current_time:bool
    @param file_line:True=on False=off
    @type file_line:bool
    @param level:0=common 1=waring 2=error
    @type level:int
    '''
    _file_line = ''
    _time = ''
    _level = ''
    if level == 0:
        _level = '=>'
    elif level == 1:
        _level = 'WARNING:'
    elif level == 2:
        _level = 'ERROR:'
    if current_time:
        _time = '[%s]' % time.strftime('%Y-%m-%d %H:%M:%S')
    if file_line:
        path = sys.path[0]
        f = sys._getframe().f_back
        _file_line = '[%s | %s | %d]' % (f.f_code.co_filename.split(path)[1],
                                         f.f_code.co_name,
                                         f.f_lineno)
    msg = '%s %s %s ==> %s' % (_level, _time, _file_line, content)
    print msg
    with open('info.log', 'a') as f:
        f.write(msg+'\n')

def main():
    '''
    test
    '''
    print_plus('content', True, True)
    test = enum(a=0, b=1, c=2,)
    print test

if __name__ == '__main__':
    main()

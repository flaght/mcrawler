# -.- coding:utf-8 -.-
"""
Created on 2016年11月18日

@author: kerry
"""
from fetch_file_models.ftp_engine import FtpEngine
class FetchFileOpcode:
    """
    fetch file opcode
    """
    ftp = 0

    http = 1

    local = 2


fetch_file_opcode = FetchFileOpcode()


class FetchFileManager: # 返回为存储的数据
    """
    提供单线程获取和线程池获取两种方式
    """

    def __init__(self):
        self.ftp_engine = FtpEngine()


    def process_data(self, ftype, basic_path, file_name):
        if ftype == fetch_file_opcode.ftp:
            return self.ftp_engine.fetch_data(basic_path, file_name)

    def process_thread_pool(self, file):
        pass
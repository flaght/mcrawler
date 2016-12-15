# -.- coding:utf-8 -.-
"""
Created on 2016年11月18日

@author: kerry
"""
from fetch_file_models.ftp_engine import FtpEngine
from fetch_file_models.local_engine import LocalEngine
from analysis.common.operationcode import fetch_file_opcode


class FetchFileManager: # 返回为存储的数据
    """
    提供单线程获取和线程池获取两种方式
    """

    def __init__(self):
        self.ftp_engine = FtpEngine()
        self.local_engine = LocalEngine()



    def process_data(self, ftype, basic_path, file_name, fid = 0):
        if ftype == fetch_file_opcode.ftp:
            return self.ftp_engine.fetch_data(basic_path, file_name)
        elif ftype == fetch_file_opcode.local:
            return self.local_engine.fetch_data(basic_path, file_name, fid)

    def process_thread_pool(self, file):
        pass
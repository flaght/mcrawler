# -*- coding: utf-8 -*-

"""
Created on 2016年11月13日

@author: kerry
"""
from analysis.common.ftp_manager import FTPManager
from analysis.base.analysis_conf_manager import analysis_conf
from analysis.base.mlog import mlog


class FtpPoolManager:

    def __init__(self, num):
        self.ftp_pool = []
        self.__create_ftp_pool(num)
        self.num = num


    def __del__(self):
        self.__del_ftp_pool()



    def __del_ftp_pool(self):
        while len(self.ftp_pool) > 0 :
            ftp_t = self.ftp_pool.pop()
            ftp_t.close()


    def __create_ftp(self):
        ftp_t = FTPManager(analysis_conf.ftp_info['host'],
                           analysis_conf.ftp_info['port'],
                           analysis_conf.ftp_info['user'],
                           analysis_conf.ftp_info['passwd'],
                           analysis_conf.ftp_info['local'])
        ftp_t.connect()
        return ftp_t

    def __create_ftp_pool(self,num):
        i = 0
        while i < num :

            self.ftp_pool.append(self.__create_ftp())
            i += 1


    def push(self,ftp_t):
        self.ftp_pool.append(ftp_t)

    def pop(self):
        if len(self.ftp_pool) > 0:
            return self.ftp_pool.pop(0)
        else:
            mlog.log().info("create new ftp")
            ftp_t = self.__create_ftp()
            self.num += 1
            return ftp_t

def main():
    """
    test
    """
    t = FtpPoolManager(10)



if __name__ == '__main__':
    main()

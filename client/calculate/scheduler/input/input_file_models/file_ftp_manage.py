# -.- coding:utf-8 -.-
"""
Created on 2017年5月23日

@author: kerry
"""

from tools.common.ftp_manager import FTPManager

class FileFTPManage(object):

    def __init__(self,config):
        self.file_manage = FTPManager(config['host'],
                                      config['port'],
                                      config['user'],
                                      config['passwd'],
                                      config['local'])


    def __del__(self):
        self.file_manage.close()

    def start(self):
        self.file_manage.connect()

    def all_file(self, path):
        self.file_manage.set_path(path)
        return self.file_manage.get_file_list()

    def file(self,path, filename):
        """
        获取单个文件
        Args:
            path:
            filename:

        Returns:

        """
        pass


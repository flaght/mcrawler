# -.- coding:utf-8 -.-
"""
Created on 2017年5月23日

@author: kerry
"""

from tools.common.local_manager import LocalManager

class FileLocalManage(object):
    def __init__(self, config):
        self.file_manage = LocalManager()
        self.basic_path = config['path']

    def __del__(self):
        pass

    def start(self):
        pass

    def all_file(self, path):
        return self.file_manage.get_file_list(self.basic_path + '/' + path)

    def file(self, path, name):
        return self.file_manage.get_file(self.basic_path + '/' + path, name)
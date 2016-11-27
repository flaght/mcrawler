# -.- coding:utf-8 -.-
"""
Created on 2016年11月19日

@author: kerry
"""

from analysis.scheduler.input.input_file_models.input_file_manage import InputFileManager
"""
config 设置对应信息

file: 文件
type 0 : ftp
type 1 : http
type 2 :local
"""
class InputManager:

    def __init__(self,config):
        #config = config['ftp']
        config = config['local']
        self.file_manager = InputFileManager.create_file_manager(config)


    def start(self):
        self.file_manager.start()

    def get_alldata(self, info):
        return self.file_manager.all_file(info)

    def get_data(self, info, name):
        return self.file_manager.file(info, name)


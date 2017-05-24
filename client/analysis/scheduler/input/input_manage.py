# -.- coding:utf-8 -.-
"""
Created on 2016年11月19日

@author: kerry
"""

from analysis.scheduler.input.input_file_models.input_file_manage import InputFileManager
from analysis.scheduler.input.input_queue_models.input_queue_manage import InputQueueManager
"""
config 设置对应信息

file: 文件
type 0 : ftp
type 1 : http
type 2 :local
"""
class InputManager:

    def __init__(self,config):
        if config.get('ftp') is not None:
            self.file_manager = InputFileManager.create_file_manager(config.get('ftp'))
            self.queue_manager = None
        elif config.get('local') is not  None:
            self.file_manager = InputFileManager.create_file_manager(config.get('local'))
            self.queue_manager = None
        elif config.get('kafka') is not None:
            self.queue_manager = InputQueueManager.create_queue_manager(config.get('kafka'))
            self.file_manager = None

    def start(self,func_callback = None):
        if self.file_manager is not None:
            self.file_manager.start()
        elif self.queue_manager is not None and func_callback is not None:
            self.queue_manager.set_callback(func_callback)
            self.queue_manager.start()

    def get_alldata(self, info):
        return self.file_manager.all_file(info)

    def get_data(self, info, name):
        return self.file_manager.file(info, name)


# -.- coding:utf-8 -.-
"""
Created on 2016年11月19日

@author: kerry
"""

from calculate.scheduler.input.input_file_models.input_file_manage import InputFileManager
from calculate.scheduler.input.input_queue_models.input_queue_manage import InputQueueManager
class InputManager(object):

    def __init__(self,config):
        self.file_manager = None
        self.queue_manager = None
        if config.get('ftp') is not None:
            self.file_manager = InputFileManager.create_file_manager(config.get('ftp'))
        elif config.get('local') is not  None:
            self.file_manager = InputFileManager.create_file_manager(config.get('local'))
        elif config.get('kafka') is not None:
            self.queue_manager = InputQueueManager.create_queue_manager(config.get('kafka'))

    def start(self,func_callback = None):
        if self.file_manager is not None:
            self.file_manager.start()
        elif self.queue_manager is not None and func_callback is not None:
            self.queue_manager.set_callback(func_callback)
            self.queue_manager.start()

    def get_all_data(self, info):
        return self.file_manager.all_file(info)

    def get_data(self, info, name):
        return self.file_manager.file(info, name)


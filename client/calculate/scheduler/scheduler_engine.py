# -*- coding: utf-8 -*-

'''
Created on 2017-05-23
@author kerry
'''
from calculate.scheduler.input.input_manage import InputManager
class SchedulerEngine:
    
    def __init__(self,config):
        self.input_mgr = InputManager(config)


    def __del__(self):
        pass

    def start(self, func_callback=None):
        if func_callback is not None:
            self.input_mgr.start(func_callback)
        else:
            self.input_mgr.start()
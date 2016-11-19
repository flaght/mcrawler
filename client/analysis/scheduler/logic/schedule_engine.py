# -*- coding: utf-8 -*-

"""
Created on 2015年9月29日

@author: kerry
"""
from xueqiu.scheduler import Scheduler as XQScheduler

class ScheduleEngne:
    def __init__(self):
        self.xq_scheduler = XQScheduler()
        self.__create_selector()


    def __del__(self):
        pass

    def __create_selector(self):
        self.logic_selector = {6: self.xq_scheduler}


    def process_data(self, pid, result_dict):
        key = pid / 10000
        scheduler = self.logic_selector[key]
        if scheduler:
            scheduler.process_data(pid, result_dict)


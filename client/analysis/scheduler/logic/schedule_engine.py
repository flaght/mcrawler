# -*- coding: utf-8 -*-

"""
Created on 2015年9月29日

@author: kerry
"""
from analysis.scheduler.logic.xueqiu.scheduler import Scheduler as XQScheduler
from analysis.scheduler.logic.hexun.scheduler import Scheduler as HXScheduler

class ScheduleEngine:
    def __init__(self, config):
        self.xq_scheduler = XQScheduler(config)
        self.hx_scheduler = HXScheduler(config)

        self.__create_selector()


    def __del__(self):
        pass

    def __create_selector(self):
        self.logic_selector = {60006: self.xq_scheduler,
                               60008: self.hx_scheduler}


    def process_data(self, pid, result_dict):
        key = pid
        scheduler = self.logic_selector[key]
        if scheduler:
            scheduler.process_data(pid, result_dict)


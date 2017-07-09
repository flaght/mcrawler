# -*- coding: utf-8 -*-

"""
Created on 2017年5月23日

@author: kerry
"""

from calculate.scheduler.logic.star_index.scheduler import Scheduler as SIScheduler

class Scheduler(object):

    def __init__(self, config):
        self.si_scheduler = SIScheduler(config)
        self.__create_selector()

    def __del__(self):
        pass

    def process_data(self,data):
        print data
        type = data['type']
        scheduler = self.logic_selector[type]
        if scheduler:
            scheduler.process_data(data)

    def __create_selector(self):
        self.logic_selector = {1: self.si_scheduler,
                               2: self.si_scheduler,
                               3: self.si_scheduler,
                               4: self.si_scheduler}



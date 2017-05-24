# -*- coding: utf-8 -*-

"""
Created on 2017年5月23日

@author: kerry
"""
from analysis.scheduler.storage.manage_model.sina.storager_manager import Storager
from analysis.comm_opercode import net_task_opercode

class Scheduler(object):
    def __init__(self,config):
        tconfig = config.get('result')
        if tconfig is not None:
            mconfig = tconfig.get(60009)
            if mconfig is not None:
                self.storager = Storager(mconfig)
        self.__create_selector()

    def __five_weibo_index(self,pid, data):
        self.storager.process_data(pid, data)

    def __create_selector(self):
        self.logic_selector = {
            net_task_opercode.SINA_WEIBO_INDEX:self.__five_weibo_index
        }

    def process_data(self, pltid, data):
        content = data['content']
        pid = content.get('pid')
        pid = int(pid)
        logic_method = self.logic_selector[pid]
        if logic_method:
            logic_method(pid, data)
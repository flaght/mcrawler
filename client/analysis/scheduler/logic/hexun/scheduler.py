# -*- coding: utf-8 -*-

"""
Created on 2016年11月19日

@author: kerry
"""

from analysis.scheduler.storage.manage_model.hexun.storage_manage import Storager
from analysis.comm_opercode import net_task_opercode

class Scheduler:
    def __init__(self, config):
        tconfig = config.get('result')
        if tconfig is not None:
            mconfig = tconfig.get('60008')
            if mconfig is not None:
                self.storager = Storager(mconfig)
        self.__create_selector()


    def __del__(self):
        pass

    def __create_selector(self):
        self.logic_selector = {net_task_opercode.HEXUN_STOCK_DAY_HEAT: self.__stock_day_heat}

    def process_data(self, pltid, data):
        content = data['content']
        pid = content.get('pid')
        if pid is None:
            pid = pltid
        else:
            pid = int(pid)
        logic_method = self.logic_selector[pid]
        if logic_method:
            logic_method(pid, data)


    def __stock_day_heat(self, pid, data):
        content = data['content']['result']
        self.storager.process_data(pid, content)
# -*- coding: utf-8 -*-

"""
Created on 2017年5月23日

@author: kerry
"""
from analysis.scheduler.storage.manage_model.sina.storager_manager import Storager
from analysis.comm_opercode import net_task_opercode
from analysis.common.operationcode import storage_opcode
import json
import time

class Scheduler(object):
    def __init__(self,config):
        tconfig = config.get('result')
        if tconfig is not None:
            mconfig = tconfig.get(60009)
            if mconfig is not None:
                self.storager = Storager(mconfig)
        self.__create_selector()

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

    def __five_weibo_index(self, pid, data):
        result = data['content']
        weibo_index = result['index']
        hot_list = result['result']
        if len(hot_list) < 0 or len(hot_list)==0:
            return None
        end_hot = hot_list[-1]
        daykey = end_hot['daykey']
        total_num = 0
        for u in hot_list:
            total_num += int(u['value'])
        unix_time = self.__change_unixtime(daykey)
        value_dict = {'type':1,'index':weibo_index,'hot':total_num,'current':unix_time}
        weibo_index_dict = {'name':'weibo_index_' + weibo_index,
                            'key':unix_time,
                            'value':json.dumps(value_dict)}
        storage_dict = {storage_opcode.redis:weibo_index_dict,
                        storage_opcode.kafka_p:value_dict}
        self.storager.process_data(pid, storage_dict)

    def __change_unixtime(self,daykey):
        localtime = time.gmtime(time.time())
        a = str(localtime.tm_year) + "-" + str(localtime.tm_mon) + "-" + str(
            localtime.tm_mday) + " " + daykey
        t = time.strptime(a, "%Y-%m-%d %H:%M")
        u = time.mktime(t) - 8 * 60 * 60

        t_unix = int(u / 60 / 60) * 60 * 60
        return t_unix

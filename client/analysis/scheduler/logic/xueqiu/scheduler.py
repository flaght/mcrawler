# -*- coding: utf-8 -*-

"""
Created on 2016年11月19日

@author: kerry
"""

"""
用于作为解析后的数据处理
"""

from analysis.scheduler.storage.manage_model.xueqiu.storager_manage import Storager
from analysis.comm_opercode import net_task_opercode,local_task_opercode


class Scheduler:
    def __init__(self, config):
        tconfig = config.get('result')
        if tconfig is not None:
            mconfig = tconfig.get(60006)
            if mconfig is not None:
                self.storager = Storager(mconfig)
        self.__create_selector()

    def __del__(self):
        pass

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

    def __search_event(self, pid, data):
        self.storager.process_data(pid, data)

    def __clean_search_event(self, pid, data):
        self.storager.process_data(pid, data)

    def __get_uid(self, pid, data):
        uid_set = data['content']['result']
        self.storager.process_data(pid, uid_set)

    def __get_member_max(self, pid, data):
        uid_member = data['content']['result']
        self.storager.process_data(pid, uid_member)

    def __fetch_crawl(self, pid, data):
        content = {'content': {'key': 'crawl_info', 'result': data}}
        self.storager.process_data(pid, content)

    def __member_max(self,pid,data):
        self.storager.process_data(pid, data)

    def __member_userinfo(self, pid, data):
        self.storager.process_data(pid, data)


    def __create_selector(self):
        self.logic_selector = {60006: self.__search_event,
                               local_task_opercode.XUEQIU_GET_DISCUSSION_UID: self.__get_uid,
                               net_task_opercode.XUEQIU_GET_PERSONAL_TIMELINE_COUNT: self.__fetch_crawl,
                               net_task_opercode.XUEQIU_GET_FLLOWER_COUNT:self.__member_max,
                               598: self.__clean_search_event,
                               net_task_opercode.XUEQIU_GET_ALL_MEMBER: self.__member_userinfo,
                               local_task_opercode.XUEQIU_GET_MEMBER_MAX:self.__get_member_max}

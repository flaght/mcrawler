# -*- coding: utf-8 -*-

'''
Created on 2017/05/23

@author kerry
'''

from calculate.scheduler.scheduler_engine import SchedulerEngine
from calculate.scheduler.logic.scheduler import Scheduler as LGScheduler
import time


class CalculateConsole(object):
    def __init__(self, config):
        self.scheduler_engine = SchedulerEngine(config)
        self.conf = config
        self.logic_scheduler = LGScheduler(config)

    def start(self,callback=None):
        self.scheduler_engine.start(callback)

    def callback_parser(self,data):
        self.logic_scheduler.process_data(data)


class CalculateConfig(object):
    def __init__(self):
        self.conf_dict = {}
        self.reslut_dict = {}

    def set_source(self, type, host=None, port=None, user=None, passwd=None, name=None, timeout=5, local='./'):
        dict = {}
        if host is not None:
            dict['host'] = host
        if port is not None:
            dict['port'] = port
        if user is not None:
            dict['user'] = user
        if passwd is not None:
            dict['passwd'] = passwd
        if timeout is not  None:
            dict['timeout'] = timeout
        if local is not None:
            dict['local'] = local
        if name is not None:
            dict['name'] = name
        dict['type'] = type
        if type == 1:
            self.conf_dict['ftp'] = dict
        elif type == 4:
            self.conf_dict['kafka'] = dict

    def set_result(self, pid, type, host=None, port=None, user=None, passwd=None, name=None):
        dict = {}
        dict['type'] = type
        if host is not None:
            dict['host'] = host
        if port is not None:
            dict['port'] = port
        if user is not None:
            dict['user'] = user
        if passwd is not None:
            dict['passwd'] = passwd
        if name is not None:
            dict['name'] = name
        # 修改一个平台支持多个存储方式
        if self.reslut_dict.has_key(pid):  # 存在
            config_dict = self.reslut_dict[pid]
        else:
            config_dict = {}
        config_dict[type] = dict
        self.reslut_dict[pid] = config_dict

    def get_config(self):
        self.conf_dict['result'] = self.reslut_dict
        return self.conf_dict

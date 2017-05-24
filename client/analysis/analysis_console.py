# -*- coding: utf-8 -*-

'''
Created on 2017/05/23

@author kerry
'''
from analysis.scheduler.scheduler_engine import ScheduleEngine
from analysis.base.mlog import mlog
import time
import json


class AnalysisConsole(object):
    def __init__(self, config):
        self.scheduler_engine = ScheduleEngine(config)
        #self.scheduler_engine.start()
        self.conf = config


    def start(self,callback=None):
        self.scheduler_engine.start(callback)

    def callback_parser_file(self,data):
        path = '~/text_storage/' + data['key_name']
        self.__handle_single_file(data['attr_id'], path, data['pos_name'])

    def __handle_all_file(self, pid, path):
        file_list = self.scheduler_engine.input_data(path)
        i = 0
        count = len(file_list)
        while i < count:
            unit_list = file_list[i:i + 5]
            i += 5
            start_time = time.time()
            for t in unit_list:
                self.__handle_single_file(pid, path, t)
            end_time = time.time()
            mlog.log().info("analysis file count %d expend %d", i, end_time - start_time)

    def __handle_single_file(self, pid, path, tfile):
        self.scheduler_engine.process_file_data(pid, path, tfile, 0)

    def handle_all_file(self, pid, path):
        self.__handle_all_file(pid, path)

    def handle_single_file(self, pid, path, file):
        self.__handle_single_file(pid, path, file)


class AnalysisConfig(object):
    def __init__(self):
        self.conf_dict = {}
        self.reslut_dict = {}

    def set_source(self, type, host=None, port=None, user=None, passwd=None, name=None, timeout=5, local='./'):
        dict = {}
        if host is not None:
            dict['host'] = host
        if port is not  None:
            dict['port'] = port
        if user is not  None:
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
        self.reslut_dict[pid] = dict

    def get_config(self):
        self.conf_dict['result'] = self.reslut_dict
        return self.conf_dict

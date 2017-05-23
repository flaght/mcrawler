# -*- coding: utf-8 -*-

'''
Created on 2017/05/23

@author kerry
'''
from analysis.scheduler.scheduler_engine import ScheduleEngine
from analysis.base.mlog import mlog
import time

class AnalysisConsole(object):

    def __init__(self,config):
        self.scheduler_engine = ScheduleEngine(config) 
        self.scheduler_engine.start()


    def __handle_all_file(self, pid, path):
        file_list = self.scheduler_engine.input(path)
        i = 0
        count = len(file_list)
        while i < count:
            unit_list = file_list[i:i+5]
            i += 5
            start_time = time.time()
            for t in unit_list:
                self.__get_single_file(self, pid, path, t)
            end_time = time.time()
            mlog.log().info("analysis file count %d expend %d", i, end_time - start_time)
                    
    def __handle_single_file(self, pid, path, file):
        self.scheduler_engine.process_file_data(pid, path, file, 0)


    def handle_all_file(self):
        pid = 10006
        path = '~/text/tm'
        self.__handle_all_file(pid,path)

    def handle_single_file(self,file):
        pid = 10006
        path = '~/text/tm'
        self.__handle_single_file(pid, path, file)


class AnalysisConfig(object): 
    def __init__(self):
        self.conf_dict = {}
        self.reslut_dict = {}

    def set_ftp(self, host, port, user, passwd, timeout=5, local='./'):
        dict = {}
        dict['host'] = host
        dict['port'] = port
        dict['passwd'] = passwd
        dict['timeout'] = timeout
        dict['local'] = local
        dict['type'] = 1
        self.conf_dict['ftp'] = dict

    def set_result(self, pid, type, name):
        dict = {}
        dict['type'] = type
        dict['name'] = name
        self.reslut_dict[pid] = dict

    def get_config(self):
        self.conf_dict['result'] = self.reslut_dict
        return self.conf_dict

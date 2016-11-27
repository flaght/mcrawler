# -*- coding: utf-8 -*-

"""
Created on 2016年11月13日

@author: kerry
"""

from analysis.parser.parser import Parser as MParser
from analysis.scheduler.cleaning.cralwer.cleaning import CleaningCrawler
from analysis.scheduler.fetch.fetch_manage import FetchFileManager
from analysis.scheduler.input.input_manage import InputManager
from analysis.scheduler.logic.schedule_engine import ScheduleEngne

"""
采用多线程方式来获取数据,解析,存储数据。
ftp kafka hbase sqlite等采用预先建立连接数(和线程数相同),以参数方式传递进去。
"""
class AnalysisEngine:

    def __init__(self):
        """

        Returns:
            object:
        """

        self.parser = MParser()
        self.task_queue = []
        self.recovery_file = {}
        self.fetch_mgr = FetchFileManager()
        self.scheduler = ScheduleEngne()


        #config = {'ftp':{'type':1, 'host':'61.147.114.73', 'port':21, 'user':'crawler', 'passwd':'123456x', 'timeout':5, 'local':'./'}}
        config = {'local':{'type':3, 'path':'/Users/kerry/work/pj/gitfork/mcrawler/client'}}
        self.input_mgr = InputManager(config)
        self.input_mgr.start()

    def __del__(self):
        pass


    def input_data(self, path, filename=None):
        if filename is None:
            return self.input_mgr.get_alldata(path)
        else:
            return self.input_mgr.get_data(path, filename)




    """
    解析数据
    """
    def __data_parser(self, content, pid):
        #data = CleaningCrawler.clean_data(content)
        if content is not  None:
            return self.parser.parse(pid, content)
        else:
            return {'status': -1}




    """
    拉取文件转化为数据
    """
    def __process_fetch_file(self, pid, ftype, basic_path, file_name):
        return self.fetch_mgr.process_data(ftype, basic_path, file_name)




    def __process_file(self, pid, ftype, basic_path, file_name):
        data = self.__process_fetch_file(pid, ftype, basic_path,  file_name)
        parser_dict = self.__data_parser(data, pid)

        """
        根据平台id,传递给管理类
        """
        if parser_dict['status'] == 1:
            self.scheduler.process_data(pid, parser_dict)




    """
    单进程处理文件
    """
    def process_file_data(self, pid, basic_path, file_name, ftype):
        self.__process_file(pid, ftype, basic_path, file_name)

    """
    多线程处理文件
    """




def main():
    """
    test
    """
    pass



if __name__ == '__main__':
    main()


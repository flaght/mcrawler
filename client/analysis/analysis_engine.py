# -*- coding: utf-8 -*-

"""
Created on 2016年11月13日

@author: kerry
"""

import base64
import json
import zlib
from base.mlog import mlog
from parser.cleaning import CleaningCrawler
from parser.parser import Parser as MParser
from scheduler.fetch.fetch_manage import FetchFileManager
from scheduler.logic.schedule_engine import ScheduleEngne

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

    def __del__(self):
        pass


    """
    解析数据
    """
    def __data_parser(self, content, pid):
        data = CleaningCrawler.clean_data(content)
        return self.parser.parse(pid, data)

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
        print parser_dict
        self.scheduler.process_data(pid, parser_dict)




    """
    单进程处理文件
    """
    def process_file_data(self, pid, basic_path, file_name, ftype):
        self.__process_file(pid, ftype, basic_path, file_name)

    """
    多线程处理文件
    """










class AnalysisEngineV1:

    def __init__(self,num):
        self.ftp_pool = FtpPoolManager(num*4)
        self.mparser = MParser()
        if num == 0:
            self.thread_pool = ThreadPoolManager(num)
            self.ftp_mgr = None
        else:
            self.thread_pool = None
            self.ftp_mgr = FTPManager(analysis_conf.ftp_info['host'],
                                      analysis_conf.ftp_info['port'],
                                      analysis_conf.ftp_info['user'],
                                      analysis_conf.ftp_info['passwd'],
                                      analysis_conf.ftp_info['local'])
            self.ftp_mgr.connect()


        self.task_queue = []
        self.sqlite_manager = SQLLiteStorage("xueqiu.db", 0)
        self.failed_file_dict = {}

    def __del__(self):
        pass

    def text_parser(self, ftp_string, name):
        charset_name = ''
        html_dict = json.loads(ftp_string)

        data = ''
        # 解base64
        try:
            data = base64.b32decode(html_dict['content'])
            charset_name = html_dict['charset']
        except Exception, e:
            print e
        # 解压缩
        try:
            data = zlib.decompress(data)
        except Exception, e:
            print e

        # 解字符串码
        try:
            data = data.decode(charset_name)
        except Exception, e:
            print e

        # 解析对象
        t = self.mparser.parse(int(name), data)
        return t


    def parser(self, ftp_mgr, basic_path, plt_id, file_name):
        if ftp_mgr is None:
            ftp_mgr_unit = self.ftp_mgr
        else:
            ftp_mgr_unit = ftp_mgr


        ftp_string = MString(str(plt_id)+file_name)
        ftp_url = basic_path + "/" +file_name
        if ftp_mgr_unit.get(ftp_url, ftp_string.write):
            parser_result = self.text_parser(ftp_string.string, plt_id)
            if parser_result is not None:
                parser_result['file_name'] = file_name
            return parser_result
        else:
            return {"code": -1, "file_name": file_name, "basic_path": basic_path, "plt_id": plt_id}


    def set_task(self, basic_path,plt_id,file_name):
        if self.ftp_pool is  not None:
            ftp_mgr = self.ftp_pool.pop()
        else:
            ftp_mgr = None
        dict = {"ftp":ftp_mgr,"basic":basic_path,"plt_id":plt_id,"file_name":file_name}
        self.task_queue.append(dict)


    """
    单线程操作
    """
    def nexec(self):
        for unit in self.task_queue:
            ftp_basic_path = unit['basic']
            ftp_plt_id = unit['plt_id']
            ftp_file_name = unit['file_name']
            result = self.parser(None, ftp_basic_path, ftp_plt_id, ftp_file_name)
            if result is None:
                return
            code = result['code']
            if code == 1:
                name_table = result['name_table']
                result_list = result['result']
                sql_formate = result['sql_formate']
                try:
                    self.sqlite_manager.create_table(name_table, 1)
                    if result_list is not None:
                        self.sqlite_manager.save_data(sql_formate, result_list)
                except Exception, e:
                    mlog.log().info(e)
            elif code == -1:
                self.failed_file_dict[result['file_name']] = result

    """
    线程池操作
    """

    def run(self):
        self.thread_pool.create_task(self.task_queue, self.parser_run_callback, self.parser_stop_callback, None)
        self.thread_pool.run()

    def parser_stop_callback(self, content, result):
        c_agrs = content.args
        for unit in c_agrs:
            ftp_mgr = unit['ftp']
            self.ftp_pool.push(ftp_mgr)

        if result is None:
            return
        code = result['code']
        if code == 1:
            name_table = result['name_table']
            result_list = result['result']
            sql_formate = result['sql_formate']
            try:
                self.sqlite_manager.create_table(name_table,1)
                if result_list is not None:
                    self.sqlite_manager.save_data(sql_formate, result_list)
            except Exception, e:
                mlog.log().info(e)
        elif code == -1:
            self.failed_file_dict[result['file_name']] = result

    def parser_run_callback(self,content):
        ftp_mgr = content['ftp']
        ftp_basic_path = content['basic']
        ftp_plt_id = content['plt_id']
        ftp_file_name = content['file_name']
        return self.parser(ftp_mgr, ftp_basic_path, ftp_plt_id, ftp_file_name)



    def test(self):
        pass

    def get_failed_list(self):
        failed_list = []
        for (k, v) in self.failed_file_dict.items():
            failed_list.append(v['file_name'])
        return failed_list




from common.ftp_manager import FTPManager
from base.analysis_conf_manager import analysis_conf


def main():
    """
    test
    """
    engine = AnalysisEngine(3)


    ftp_manager_t = FTPManager(analysis_conf.ftp_info['host'],
                           analysis_conf.ftp_info['port'],
                           analysis_conf.ftp_info['user'],
                           analysis_conf.ftp_info['passwd'],
                           analysis_conf.ftp_info['local'])
    ftp_manager_t.connect()
    ftp_manager_t.set_path("~/text_storage/60006bak")
    count = ftp_manager_t.file_count()
    i = 0
    while i < count:
        tlist = ftp_manager_t.get_file(i, i + 10)
        # print tlist
        i += 10
        #print tlist

        mlog.log().info("[i %d,count %d]",i,count)
        for t in tlist:
            name = "60006" + t
            engine.set_task("~/text_storage/60006bak",60006,t)
        engine.run()




if __name__ == '__main__':
    main()


# -*- coding: utf-8 -*-

"""
Created on 2016年11月13日

@author: kerry
"""

import json
import zlib
import base64
from parser.parser import Parser as MParser
from common.mstring import MString
from pool.ftp_pool_manage import FtpPoolManager
from pool.thread_pool_manage import ThreadPoolManager
from schduler.storage.sqlite_manage_model import SQLLiteStorage
from base.mlog import mlog


"""
采用多线程方式来获取数据,解析,存储数据。
ftp kafka hbase sqlite等采用预先建立连接数(和线程数相同),以参数方式传递进去。
"""
class AnalysisEngine:

    def __init__(self,num):
        self.ftp_pool = FtpPoolManager(num*4)
        self.mparser = MParser()
        self.thread_pool = ThreadPoolManager(num)
        self.queue = []
        self.sqlite_manager = SQLLiteStorage("xueqiu.db", 0)
        self.error_file = []

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

    def set_task(self, basic_path,plt_id,file_name):
        ftp_mgr = self.ftp_pool.pop()

        dict = {"ftp":ftp_mgr,"basic":basic_path,"plt_id":plt_id,"file_name":file_name}
        self.queue.append(dict)

    def run(self):
        self.thread_pool.create_task(self.queue, self.parser_run, self.parser_stop, None)
        self.thread_pool.run()

    def parser(self, ftp_mgr, basic_path, plt_id, file_name):
        ftp_string = MString(str(plt_id)+file_name)
        ftp_url = basic_path + "/" +file_name
        try:
            if ftp_mgr.get(ftp_url, ftp_string.write):
                mlog.log().info(ftp_url)
                return self.text_parser(ftp_string.string, plt_id)
        except Exception, e:
            mlog.log().info(e)
        return None

    def parser_stop(self, content, result):
        c_agrs = content.args
        for unit in c_agrs:
            ftp_mgr = unit['ftp']
            self.ftp_pool.push(ftp_mgr)

        if result is not None:
            name_table = result['name_table']
            result_list = result['result']
            sql_formate = result['sql_formate']
            try:
                self.sqlite_manager.create_table(name_table,1)
                #mlog.log().info(name_table)
                if result_list is not None:
                    self.sqlite_manager.save_data(sql_formate, result_list)
            except Exception, e:
                mlog.log().info(e)
        else: #处理爬取失败




    def parser_run(self,content):
        ftp_mgr = content['ftp']
        ftp_basic_path = content['basic']
        ftp_plt_id = content['plt_id']
        ftp_file_name = content['file_name']
        return self.parser(ftp_mgr, ftp_basic_path, ftp_plt_id, ftp_file_name)


    def test(self):
        pass




from common.ftp_manager import FTPManager
from base.analysis_conf_manager import analysis_conf


def main():
    """
    test
    """
    engine  = AnalysisEngine(3)


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


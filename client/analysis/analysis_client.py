# -*- coding: utf-8 -*-

"""
Created on 2015年9月29日

@author: kerry
"""

import platform
import sys
import os
import time

sys.path.append('./../')

from analysis.analysis_engine import AnalysisEngine
from analysis.base.mlog import mlog
from multiprocessing import Pool
import json

"""
1.文件来源地址方式
2.文件地址
3.存储方式
4.平台id 0 忽略平台

"""

"""
config = {'ftp':{'type':1, 'host':'61.147.114.73', 'port':21, 'user':'crawler', 'passwd':'123456x', 'timeout':5, 'local':'./'},
          'local': {'type': 3, 'path': '/Users/kerry/work/pj/gitfork/mcrawler/client'}
         }
"""






class Console:

    def __init__(self):
        self.path = ""
        self.fetch_type = 0
        self.plt_id = 0
        self.input_data = 0
        self.__print_info()

    def __print_info(self):
        print "Generated by gfwlist2pac in precise mode:"
        #print "get data: 1.ftp 2.local 3.kakfa"
        #print "storage type : 1. sqlite"
        #print "other"

    def input_info(self):
        print "please input data type: 1. FILE  2.RawData"
        self.input_data = raw_input("type:")
        print "please input source path"
        self.path = raw_input("path:")
        print  "please analysis platform id"
        self.plt_id = int(raw_input("id:"))


def run(console):
    analysis_engine = AnalysisEngine()
    file_list = analysis_engine.input_data(console.path)
    i = 0
    count = len(file_list)
    while i < count:
        tlist = file_list[i:i + 4]
        i += 5
        start_time = time.time()
        for t in tlist:
            analysis_engine.process_file_data(console.plt_id, console.path, t, 0)
        end_time = time.time()
        mlog.log().info("analysis file count %d  expend %d", i, end_time - start_time)





def main():
    mlog.log().info('Python %s on %s' % (sys.version, sys.platform))
    sys_str = platform.system()
    mlog.log().info(sys_str)
    if platform.system() == "Darwin" or platform.system() == "Linux":
        reload(sys)
        sys.setdefaultencoding('utf-8')  # @UndefinedVariable
    os.chdir(os.getcwd())

    ### 控制台输出
    console = Console()
    console.input_info()



    pool = Pool(processes=3)

    result = pool.apply_async(run,(console,))

    pool.close()
    pool.join()
    if result.successful():
        mlog.log().info("successful")



def test():
    config = {'ftp': {'type': 1, 'host': '61.147.114.73', 'port': 21, 'user': 'crawler',
                      'passwd': '123456x', 'timeout': 5, 'local': './'}}

    analysis_engine = AnalysisEngine(config)
    file_list = analysis_engine.input_data('~/text_storage/60006bak')
    i = 0
    count = len(file_list)
    while i < count:
        tlist = file_list[i:i + 4]
        i += 5
        start_time = time.time()
        for t in tlist:
            analysis_engine.process_file_data(60006, '~/text_storage/60006bak', t, 0)
        end_time = time.time()
        mlog.log().info("analysis file count %d  expend %d", i, end_time - start_time)


def test_local():
    config = {'local': {'type': 3, 'path': '/Users/kerry/work/pj/gitfork/mcrawler/client'}}
    analysis_engine = AnalysisEngine(config)
    analysis_engine.process_file_data(60007,'./','xueqiu.db', 2)






"""
config = {
    'kafka': {'type': 4, 'host': '61.147.114.85:9092,61.147.114.80:9092,61.147.114.81:9092',
              'name': 'newsparser_task_algo'},
    'result': {
              '60006':{'type': 5, 'name': '../discuss1.db'},
              '60008':{'type': 5, 'name': '../hexunstock.db'}
            }
}

analysis_engine = AnalysisEngine(config)
"""
def tcallback(json):
    print json

def realtime_hexun():
    pass
    #analysis_engine.start(tcallback)


def tjson():
    tmjson = "{\"task_id\": \"2222970082354408886\", \"key_name\": \"60008/589\",     \"attr_id\": \"60008\",     \"analyze_id\": \"907736781\",     \"type\": \"1\",     \"cur_depth\": \"1\",     \"pos_name\": \"ffcd848f528ce73c15dca596057e3a1d\",     \"max_depth\": \"1\" }"
    t = json.loads(tmjson)
    analysis_engine.process_file_data(int(t.get('attr_id')), t.get('key_name'), t.get('pos_name'), 0)


def parser_xueqiu():

    mconfig = {
        'local': {'type': 3, 'path': '/Users/kerry/work/pj/gitfork/mcrawler'},
        'result':{
            '60006': {'type': 5, 'name': '../discuss.db'},
        }
    }
    ae = AnalysisEngine(mconfig)
    ae.process_file_data(60006, './file/', 'xueqiu.db', 2, -600)

    """

    input_path = '~/text_storagebak/60006bak'
    file_path = '~/text_storagebak/60006bak'
    plt_id = 60006


    config = {'ftp': {'type': 1, 'host': '61.147.114.73', 'port': 21, 'user': 'crawler',
                      'passwd': '123456x', 'timeout': 5, 'local': './'},
              'result': {'type': 5, 'name': '../discuss1.db'}}
    analysis_engine = AnalysisEngine(config)
    file_list = analysis_engine.input_data(input_path)
    i = 0
    count = len(file_list)
    while i < count:
        unit_list = file_list[i:i+5]
        i += 5
        start_time = time.time()
        for t in unit_list:
            analysis_engine.process_file_data(plt_id, file_path, t, 0)
        end_time = time.time()
        mlog.log().info("analysis file count %d  expend %d", i, end_time - start_time)
    """

"""
def parser_ftp():
    tconfig = {
        'ftp': {'type': 1, 'host': '61.147.114.73', 'port': 21, 'user': 'crawler',
                'passwd': '123456x', 'timeout': 5, 'local': './'},
        'result': {
            '60006': {'type': 5, 'name': '../discuss.db'},
            '60008': {'type': 5, 'name': '../hexunstock.db'}
        }
    }
    input_path = '~/text_storage/60006/599'
    tanalysis_engine = AnalysisEngine(tconfig)
    tanalysis_engine.start()
    file_list = tanalysis_engine.input_data(input_path)
    i = 0
    count = len(file_list)
    while i < count:
        unit_list = file_list[i:i + 5]
        i += 5
        start_time = time.time()
        for t in unit_list:
            tanalysis_engine.process_file_data(60006, input_path, t, 0)
        end_time = time.time()
        mlog.log().info("analysis file count %d  expend %d", i, end_time - start_time)
"""




def parser_local_method(config, path, name, pid, tid):
    ae = AnalysisEngine(config)
    ae.process_file_data(pid, path, name, 2, tid)

def parser_ftp_method(config, path, pid):
    ae = AnalysisEngine(config)
    ae.start()
    file_list = ae.input_data(path)
    i = 0
    count = len(file_list)
    while i < count:
        unit_list = file_list[i:i + 5]
        i += 5
        start_time = time.time()
        for t in unit_list:
            ae.process_file_data(pid, path, t, 0)
        end_time = time.time()
        mlog.log().info("analysis file count %d  expend %d", i, end_time - start_time)




if __name__ == '__main__':
    if platform.system() == "Darwin" or platform.system() == "Linux":
        reload(sys)
        sys.setdefaultencoding('utf-8')  # @UndefinedVariable

    #parser_xueqiu()


    config = {
        'ftp': {'type': 1, 'host': '61.147.114.73', 'port': 21, 'user': 'crawler',
                'passwd': '123456x', 'timeout': 5, 'local': './'},
        'result': {
            '60006': {'type': 5, 'name': '../follwer.db'}
        }
    }
    path = '~/text_storage/60006/601'
    pid = 60006
    parser_ftp_method(config, path, pid)

    """
    mconfig = {
        'local': {'type': 3, 'path': '/Users/kerry/work/pj/gitfork/mcrawler'},
        'result':{
            '60006': {'type': 3, 'name': '../member.txt'},
        }
    }

    parser_local_method(mconfig, 'file/', 'member.db', 60006, -600)
    """

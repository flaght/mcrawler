# -*- coding: utf-8 -*-

"""
Created on 2015年9月29日

@author: kerry
"""
import platform
import sys
import os
import time
from analysis_engine import AnalysisEngine
from scheduler.fetch.fetch_manage import FetchFileOpcode


"""
def analysis_file_threadpool(analysis_file, path, plt_id):
    i = 0
    count = len(analysis_file)
    while i < count:
        tlist = analysis_file[i:i + 4]
        i += 5
        for t in tlist:
            engine.set_task(path, plt_id, t)
        engine.run()
        mlog.log().info("==>file analysis count %d", i)
        mlog.log().info("==>failed_file_dict size %d", len(engine.failed_file_dict))
        time.sleep(0.5)

def analysis_file(analysis_file, path, plt_id):
    i = 0
    count = len(analysis_file)
    while i < count:
        tlist = analysis_file[i:i + 4]
        i += 5
        for t in tlist:
            engine.set_task(path, plt_id, t)
        engine.nexec()
"""

if __name__ == '__main__':
    sys_str = platform.system()
    print sys_str
    if platform.system() == "Darwin" or platform.system() == "Linux":
        reload(sys)
        sys.setdefaultencoding('utf-8')  # @UndefinedVariable
    analysis_engine = AnalysisEngine()
    data = analysis_engine.process_file_data(60006, '~/text_storage/60006bak', 'c35064c32ce3b2da746b8dc9c45c5d77', FetchFileOpcode.ftp)

    """
    engine = AnalysisEngine(0)

    ftp_manager_t = FTPManager(analysis_conf.ftp_info['host'],
                               analysis_conf.ftp_info['port'],
                               analysis_conf.ftp_info['user'],
                               analysis_conf.ftp_info['passwd'],
                               analysis_conf.ftp_info['local'])
    ftp_manager_t.connect()
    ftp_manager_t.set_path("~/text_storage/60006bak")
    file_list = ftp_manager_t.get_file_list()
    analysis_file(file_list,"~/text_storage/60006bak",60006)

    while len(engine.error_file) > 0:
        fail_file = engine.get_failed_list()
        engine.failed_file_dict = {}
        analysis_file(fail_file)

    ftp_manager_t.close()
    """
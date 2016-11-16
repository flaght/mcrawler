# -*- coding: utf-8 -*-

"""
Created on 2015年9月29日

@author: kerry
"""
import platform
import sys
import os
from analysis_engine import AnalysisEngine
from base.analysis_conf_manager import analysis_conf
from common.ftp_manager import FTPManager
from base.mlog import mlog

if __name__ == '__main__':
    sys_str = platform.system()
    print sys_str
    if platform.system() == "Darwin" or platform.system() == "Linux":
        reload(sys)
        sys.setdefaultencoding('utf-8')  # @UndefinedVariable

    print os.getcwd()



    engine = AnalysisEngine(5)

    ftp_manager_t = FTPManager(analysis_conf.ftp_info['host'],
                               analysis_conf.ftp_info['port'],
                               analysis_conf.ftp_info['user'],
                               analysis_conf.ftp_info['passwd'],
                               analysis_conf.ftp_info['local'])
    ftp_manager_t.connect()
    ftp_manager_t.set_path("~/text_storage/60006bak")
    file_list =ftp_manager_t.get_file_list()
    count = len(file_list)
    i = 0
    while i < count:
        tlist = file_list[i:i + 4]
        i += 5
        for t in tlist:
            engine.set_task("~/text_storage/60006bak", 60006, t)
        engine.run()
        mlog.log().info("[i %d,count %d]", i, count)

    ftp_manager_t.close()

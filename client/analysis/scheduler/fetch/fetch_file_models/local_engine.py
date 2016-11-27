# -.- coding:utf-8 -.-
"""
Created on 2016年11月18日

@author: kerry
"""

from analysis.common.local_manager import LocalManager
from analysis.base.analysis_conf_manager import analysis_conf
from analysis.scheduler.cleaning.sql.xueqiu import Xueqiu
from analysis.base.mlog import mlog

class LocalEngine:

    def __init__(self):
        self.file_manage = LocalManager()
        self.basic_path = analysis_conf.local_info['path']

    def __clean_data(self,file_path, type):
        clean = Xueqiu("./")
        clean.connect(file_path)
        return clean.fetchall_data()


    def fetch_data(self, basic_path, file_name):
        file_path = self.basic_path + '/' + basic_path + '/' + file_name
        mlog.log().info("%s",file_path)
        dict = self.__clean_data(file_path, 0)
        return dict



def main():
    t = LocalEngine()
    dict = t.fetch_data('analysis','xueqiu1.db')
    print len(dict)



if __name__ == '__main__':
    main()

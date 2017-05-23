# -*- coding: utf-8 -*-
'''
Created on 2017/05/23

@author kerry
'''

import platform
import sys
sys.path.append('./../')
from analysis.analysis_console import AnalysisConsole
from analysis.analysis_console import AnalysisConfig

if __name__ == '__main__':
    if platform.system() == "Darwin" or platform.system() == "Linux":
        reload(sys)
        sys.setdefaultencoding('utf-8')

    config = AnalysisConfig
    config.set_ftp(host='61.147.114.73',
                   port=21,
                   user='crawler',
                   passwd='123456x')

    config.set_reuslt(pid=600006,type=5,name='../follwer.db')
    config.set_reuslt(pid=600068,type=5,name='../f.db')

    console = AnalysisConsole(config)
    console.handle_all_file()

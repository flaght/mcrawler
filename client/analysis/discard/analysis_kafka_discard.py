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

config = {
    'kafka': {'type': 4, 'host': '61.147.114.85:9092,61.147.114.80:9092,61.147.114.81:9092',
              'name': 'newsparser_task_algo'},
    'result': {
              '60006':{'type': 5, 'name': '../discuss.db'},
              '60008':{'type': 5, 'name': '../hexunstock.db'}
            }
}

analysis_engine = AnalysisEngine(config)

def tcallback(data):
    analysis_engine.process_file_data(int(data.get('attr_id')), data.get('key_name'), data.get('pos_name'), 0)

def realtime():
    analysis_engine.start(tcallback)

if __name__ == '__main__':
    if platform.system() == "Darwin" or platform.system() == "Linux":
        reload(sys)
        sys.setdefaultencoding('utf-8')  # @UndefinedVariable
    realtime()
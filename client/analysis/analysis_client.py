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
from analysis.common.operationcode import storage_opcode
from analysis.base.analysis_conf_manager import analysis_conf

if __name__ == '__main__':
    if platform.system() == "Darwin" or platform.system() == "Linux":
        reload(sys)
        sys.setdefaultencoding('utf-8')

    config = AnalysisConfig()
    config.set_source(type=analysis_conf.kafka_info['type'],host=analysis_conf.kafka_info['host'],
                      name=analysis_conf.kafka_info['name'])

    #config.set_result(pid=60006, type=storage_opcode.sqlite, name='../follwer.db')
    #config.set_result(pid=60009, type=storage_opcode.sqlite, name='../f.db')
    config.set_result(pid=60009, type=storage_opcode.kafka_p, host='kafka.t.smartdata-x.com', name='kafka_weibo_index_1010')

    console = AnalysisConsole(config.get_config())
    console.start(console.callback_parser_file)
#    console.handle_all_file(60009,"~/text_storage/60009/602")

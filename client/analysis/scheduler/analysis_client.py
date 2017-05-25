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

    config.set_result(pid=60009, type=storage_opcode.kafka_p, host='kafka.t.smartdata-x.com', name='kafka_weibo_index_1010')
    config.set_result(pid=60009, type=storage_opcode.redis, host='122.144.169.216',port=6379)
    console = AnalysisConsole(config.get_config())
    console.start(console.callback_parser_file)
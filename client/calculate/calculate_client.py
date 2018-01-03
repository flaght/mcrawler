# -*- coding: utf-8 -*-
'''
Created on 2017/05/23

@author kerry
'''

import platform
import sys
import os
sys.path.append('./../')
from calculate.calculate_console import CalculateConsole
from calculate.calculate_console import CalculateConfig
from tools.base.conf_manager import ConfManager
from tools.common.operationcode import storage_opcode
from tools.common.operationcode import filer_opcode

if __name__ == '__main__':
    if platform.system() == "Darwin" or platform.system() == "Linux":
        reload(sys)
        sys.setdefaultencoding('utf-8')

    conf = ConfManager.get_instance()
    base_path = os.path.dirname(__file__)
    conf.init(base_path + "/calculate.conf",filer_opcode)
    config = CalculateConfig()
    config.set_source(type=conf.kafka_info['type'],host=conf.kafka_info['host'],
                      name=conf.kafka_info['name'])

    config.set_result(pid=60009, type=storage_opcode.kafka_p, host='139.224.18.190:9092', name='kafka_weibo_index_1011')

    console = CalculateConsole(config.get_config())
    console.start(console.callback_parser)

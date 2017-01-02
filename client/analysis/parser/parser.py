# -*- coding: utf-8 -*-
"""
Created on 20160812

@author rotciv
"""
import datetime

from analysis.base.analysis_conf_manager import analysis_conf
from analysis.base.mlog import mlog
from analysis.scheduler.storage.enclosure.text_storage_model import TextStorage

from hexun_models.parser_manager import HX_parser
from xueqiu_models.parser_manager import XQ_parser


"""
解析结果结构
['result'] = result
['status'] =  status  -1 解析失败 0 解析成功
"""
class Parser:
    def __init__(self):
        pass

    def parse(self, parse_id, content):
        status = -1
        rt = None
        if parse_id == 60006:
            rt = XQ_parser.parse(parse_id, content)
            status = -1 if rt is None else 1
        elif parse_id == 60008:
            rt = HX_parser.parse(parse_id, content)
            status = -1 if rt is None else 1
        else:
            rt = content
            status = 1
        return {"status":status,"content":rt}
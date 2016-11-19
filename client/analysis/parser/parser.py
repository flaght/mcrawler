# -*- coding: utf-8 -*-
"""
Created on 20160812

@author rotciv
"""
import datetime

from base.analysis_conf_manager import analysis_conf
from base.mlog import mlog
from scheduler.storage.enclosure.text_storage_model import TextStorage

from hexun_models.hexun_parser import HeXunParser
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
        if parse_id == 1:
            rt = HeXunParser.parse_xml(content)
        elif parse_id == 60006:
            rt = XQ_parser.parse(parse_id, content)
            status = -1 if rt is None else 1
        return {"status":status,"content":rt}
# -*- coding: utf-8 -*-
"""
Created on 20160812

@author rotciv
"""
import datetime

from hexun_parser import HeXunParser
from xueqiu_parser import xq_parser
from schduler.storage.text_storage_model import TextStorage
from base.analysis_conf_manager import analysis_conf
from base.mlog import mlog

class Parser:
    prefix = "result_storage/"

    def __init__(self):
        self.text_storage = TextStorage(analysis_conf.ftp_info['host'],
                           analysis_conf.ftp_info['port'],
                           analysis_conf.ftp_info['user'],
                           analysis_conf.ftp_info['passwd'])

    def parse(self, parse_id, content):
        path = Parser.prefix
        result = ""
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")

        if parse_id == 1:
            result = HeXunParser.parse_xml(content)
            path += "60005/market15/"
        elif parse_id == 2:
            result = HeXunParser.parse_xml(content)
            path += "60005/markettotal/"
        elif parse_id == 3:
            result = HeXunParser.parse_xml(content)
            path += "60005/stock15/"
        elif parse_id == 4:
            path += "60005/stocktotal/"
        elif parse_id == 60006:
            [subpath, name, result] = xq_parser.parser_search(content)
            if result is not None and len(result) > 0:
                mlog.log().info(subpath+name)
                self.text_storage.upload_data(result,
                                              subpath,name)
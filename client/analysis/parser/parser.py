# -*- coding: utf-8 -*-
"""
Created on 20160812

@author rotciv
"""
import datetime

from base.analysis_conf_manager import analysis_conf
from base.mlog import mlog
from schduler.storage.text_storage_model import TextStorage

from analysis.parser.hexun_models.hexun_parser import HeXunParser
from analysis.parser.xueqiu_models.parser_manager import XQ_parser

class Parser:
    prefix = "result_storage/"

    def __init__(self):
        """
        self.text_storage = TextStorage(analysis_conf.ftp_info['host'],
                           analysis_conf.ftp_info['port'],
                           analysis_conf.ftp_info['user'],
                           analysis_conf.ftp_info['passwd'])

        """

    def parse(self, parse_id, content):
        path = Parser.prefix

        result = ""
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")

        if parse_id == 1:
            result = HeXunParser.parse_xml(content)
            path += "60005/market15/"
        elif parse_id == 60006:
            return XQ_parser.parse(parse_id,content)
            """
            [subpath, name, result] = xq_parser.parser_search(content)
            if result is not None and len(result) > 0:
                mlog.log().info(subpath+name)
                self.text_storage.upload_data(result,
                                              subpath,name)
            """
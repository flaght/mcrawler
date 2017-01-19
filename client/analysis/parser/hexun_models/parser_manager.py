# -*- coding: utf-8 -*-
import json

from analysis.parser.hexun_models.stock_day_heat import hx_dayheat

"""
Created on 201601015

@author kerry
"""

class HexunParser:
    def __init__(self):
        self.logic_selector = {588:self.__stock_day_hot,
                               589:self.__stock_quarter_heat}

    def parse(self, parse_id, content):
        pid = content.get('pid')

        scheduler = self.logic_selector[int(pid)]
        if scheduler:
            return scheduler(content)
        return None

    """
    每支股票按天的热度统计
    """

    def __stock_day_hot(self, content):
        rt = hx_dayheat.day_heat(content['data'])
        return {'pid': 588, 'result': rt}

    """
    每支股票每一刻钟的热度
    """
    def __stock_quarter_heat(self, content):
        rt = hx_dayheat.quarter_heat(content['data'])
        return {'pid':589, 'result': rt}


HX_parser = HexunParser()
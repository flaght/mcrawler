# -*- coding: utf-8 -*-
import json

from analysis.parser.hexun_models.stock_day_heat import hx_dayheat
from analysis.comm_opercode import net_task_opercode

"""
Created on 201601015

@author kerry
"""

class HexunParser:
    def __init__(self):
        self.logic_selector = {net_task_opercode.HEXUN_STOCK_DAY_HEAT:self.__stock_day_hot,
                               net_task_opercode.HEXUN_STOCK_QUARTER_HEAT:self.__stock_quarter_heat}

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
        return {'pid': net_task_opercode.HEXUN_STOCK_DAY_HEAT, 'result': rt}

    """
    每支股票每一刻钟的热度
    """
    def __stock_quarter_heat(self, content):
        rt = hx_dayheat.quarter_heat(content['data'])
        return {'pid':net_task_opercode.HEXUN_STOCK_QUARTER_HEAT, 'result': rt}


HX_parser = HexunParser()
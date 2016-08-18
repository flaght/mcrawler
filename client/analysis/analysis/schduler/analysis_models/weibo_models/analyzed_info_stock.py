# -*- coding:utf-8 -*-
"""
Created on 2015年12月3日

@author: slm
"""


class AnalyzedInfoStock(object):
    """
    stock_name:股票名字
    stock_code:股票代码
    concern_num:关注数
    """
    __struct_fmt = '=H'
    stock_name = None
    stock_code = None
    concern_num = None

    def __init__(self, params=None):
        """
        Constructor
        """
        if not params:
            return
        self.stock_name = ''
        self.stock_code = ''
        self.stock_num = ''

# -*- coding:utf-8 -*-
"""
Created on 2015年11月25日

@author: slm
"""


class AnalyzedInfoExpert(object):
    """
    weibo_name:大V微博名
    url:链接
    """
    __struct_fmt = '=H'
    weibo_name = None
    url = None

    def __init__(self, params=None):
        """
        Constructor
        """
        if not params:
            return
        self.weibo_name = ''
        self.url = ''

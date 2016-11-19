# -*- coding:utf-8 -*-
"""
Created on 2015年12月09日

@author: slm
"""
from scheduler.analysis_models.model_namager_base import ModelManagerBase
from scheduler.analysis_models.weibo_models.weibo_analysis.stock_first_page import WBFirstPage
from scheduler.analysis_models.weibo_models.weibo_analysis.stock_expert import WBExpert
from scheduler.analysis_models.weibo_models.weibo_analysis.big_v import WBigV


class WBManager(ModelManagerBase):
    """
    微博管理
    """
    platform_id = 4
    rules_level = {}

    def reg_models(self):
        """
        doc
        """
        self.set_models_selector(WBFirstPage.tag['rule'], {WBFirstPage.tag['tag']: WBFirstPage})
        self.set_models_selector(WBExpert.tag['rule'], {WBExpert.tag['tag']: WBExpert})
        self.set_models_selector(WBigV.tag['rule'], {WBigV.tag['tag']: WBigV})

    def reg_rule_list(self):
        self.set_rule_sort_list(WBigV.tag['rule'])
        self.set_rule_sort_list(WBFirstPage.tag['rule'])
        self.set_rule_sort_list(WBExpert.tag['rule'])

    def match_type_tag(self, tag):
        if '_微博' in tag:
            return '_微博'
        else:
            return tag

    def analyzed(self, params):
        """
        解析完成
        """
        ModelManagerBase.analyzed(self, **params)

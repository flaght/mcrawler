# -.- coding:utf-8 -.-
"""
Created on 2015年12月09日

@author: slm
"""
from schduler.analysis_models.model_namager_base import ModelManagerBase
from schduler.analysis_models.cn_models.homepage import CNHomePage
from schduler.analysis_models.cn_models.cn_finance import CNFinance
from schduler.analysis_models.cn_models.cn_news import CNNews
from schduler.analysis_models.cn_models.finance_focus_more import CNMainNews
from schduler.analysis_models.cn_models.finance_industry_more import CNIndustry
from schduler.analysis_models.cn_models.finance_internet_more import CNinternet
from schduler.analysis_models.cn_models.finance_macro_more import CNMacro
from schduler.analysis_models.cn_models.finance_production_more import CNProduction
from schduler.analysis_models.cn_models.news_domestic_more import CNDomesticNews
from schduler.analysis_models.cn_models.news_focus_more import CNFocusMore


class CNManager(ModelManagerBase):
    """
    cn管理模块
    """
    platform_id = 5
    rules_level = {}

    def reg_models(self):
        """
        doc
        """
        self.set_models_selector(CNHomePage.tag['rule'], {CNHomePage.tag['tag']: CNHomePage})
        self.set_models_selector(CNFinance.tag['rule'], {CNFinance.tag['tag']: CNFinance})
        self.set_models_selector(CNNews.tag['rule'], {CNNews.tag['tag']: CNNews})
#         self.set_models_selector(CNNewsDetail.tag['rule'], {CNNewsDetail.tag['tag']: CNNewsDetail})
#         self.set_models_selector(CNDetail.tag['rule'], {CNDetail.tag['tag']: CNDetail})
        self.set_models_selector(CNMainNews.tag['rule'], {CNMainNews.tag['tag']: CNMainNews})
        self.set_models_selector(CNIndustry.tag['rule'], {CNIndustry.tag['tag']: CNIndustry})
        self.set_models_selector(CNinternet.tag['rule'], {CNinternet.tag['tag']: CNinternet})
        self.set_models_selector(CNMacro.tag['rule'], {CNMacro.tag['tag']: CNMacro})
        self.set_models_selector(CNProduction.tag['rule'], {CNProduction.tag['tag']: CNProduction})
        self.set_models_selector(CNDomesticNews.tag['rule'], {CNDomesticNews.tag['tag']: CNDomesticNews})
        self.set_models_selector(CNFocusMore.tag['rule'], {CNFocusMore.tag['tag']: CNFocusMore})

    def analyzed(self, params):
        """
        解析完成
        """
        ModelManagerBase.analyzed(self, **params)

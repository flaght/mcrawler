# -.- coding:utf-8 -.-
"""
Created on 2015年12月29日

@author: slm
"""

from schduler.analysis_models.model_namager_base import ModelManagerBase
from schduler.analysis_models.ths_more_models.ths_analysis.chance_info import THSChanceInfo
from schduler.analysis_models.ths_more_models.ths_analysis.finance_firstpage import THSFinanceFirstPage
from schduler.analysis_models.ths_more_models.ths_analysis.finance_main_new import THSMainNews
from schduler.analysis_models.ths_more_models.ths_analysis.homepage import THSHomePage
from schduler.analysis_models.ths_more_models.ths_analysis.more_famous import THSFamous
from schduler.analysis_models.ths_more_models.ths_analysis.more_finance_focus import THSFinanceFocus
from schduler.analysis_models.ths_more_models.ths_analysis.more_finance_macroscopic import THSFinanceMacroscopic
from schduler.analysis_models.ths_more_models.ths_analysis.more_original_sole import THSOriginalSole
from schduler.analysis_models.ths_more_models.ths_analysis.more_stock_company_news import THSStockNews
from schduler.analysis_models.ths_more_models.ths_analysis.more_stock_company_notice import THSStockNotice
from schduler.analysis_models.ths_more_models.ths_analysis.more_stock_company_research import THSStockResearch
from schduler.analysis_models.ths_more_models.ths_analysis.more_stock_grail import THSStockGrail
from schduler.analysis_models.ths_more_models.ths_analysis.more_stock_investment import THSStockInvestment
from schduler.analysis_models.ths_more_models.ths_analysis.more_stock_rolling import THSStockRolling
from schduler.analysis_models.ths_more_models.ths_analysis.stock_company import THSStockCompany
from schduler.analysis_models.ths_more_models.ths_analysis.stock_early import THSStockEarly
from schduler.analysis_models.ths_more_models.ths_analysis.stock_firstpage import THSStockFirstPage
from schduler.analysis_models.ths_more_models.ths_analysis.stock_industry import THSStockIndustry
from schduler.analysis_models.ths_more_models.ths_analysis.stock_market import THSStockMarket


class ThsNewsManager(ModelManagerBase):
    """
    管理模块
    """
    platform_id = 6

    def reg_models(self):
        """
        THS_ChanceInfo_TAG: 页面唯一标识
        THSChanceInfo: 页面解析类
        """
        self.set_models_selector(THSChanceInfo.tag['rule'],
                                 {THSChanceInfo.tag['tag']: THSChanceInfo})
        self.set_models_selector(THSFinanceFirstPage.tag['rule'],
                                 {THSFinanceFirstPage.tag['tag']: THSFinanceFirstPage})
        self.set_models_selector(THSMainNews.tag['rule'],
                                 {THSMainNews.tag['tag']: THSMainNews})
        self.set_models_selector(THSHomePage.tag['rule'],
                                 {THSHomePage.tag['tag']: THSHomePage})
        self.set_models_selector(THSFamous.tag['rule'],
                                 {THSFamous.tag['tag']: THSFamous})
        self.set_models_selector(THSFinanceFocus.tag['rule'],
                                 {THSFinanceFocus.tag['tag']: THSFinanceFocus})
        self.set_models_selector(THSFinanceMacroscopic.tag['rule'],
                                 {THSFinanceMacroscopic.tag['tag']: THSFinanceMacroscopic})
        self.set_models_selector(THSOriginalSole.tag['rule'],
                                 {THSOriginalSole.tag['tag']: THSOriginalSole})
        self.set_models_selector(THSStockNews.tag['rule'],
                                 {THSStockNews.tag['tag']: THSStockNews})
        self.set_models_selector(THSStockNotice.tag['rule'],
                                 {THSStockNotice.tag['tag']: THSStockNotice})
        self.set_models_selector(THSStockResearch.tag['rule'],
                                 {THSStockResearch.tag['tag']: THSStockResearch})
        self.set_models_selector(THSStockGrail.tag['rule'],
                                 {THSStockGrail.tag['tag']: THSStockGrail})
        self.set_models_selector(THSStockInvestment.tag['rule'],
                                 {THSStockInvestment.tag['tag']: THSStockInvestment})
        self.set_models_selector(THSStockRolling.tag['rule'],
                                 {THSStockRolling.tag['tag']: THSStockRolling})
        self.set_models_selector(THSStockCompany.tag['rule'],
                                 {THSStockCompany.tag['tag']: THSStockCompany})
        self.set_models_selector(THSStockEarly.tag['rule'],
                                 {THSStockEarly.tag['tag']: THSStockEarly})
        self.set_models_selector(THSStockFirstPage.tag['rule'],
                                 {THSStockFirstPage.tag['tag']: THSStockFirstPage})
        self.set_models_selector(THSStockIndustry.tag['rule'],
                                 {THSStockIndustry.tag['tag']: THSStockIndustry})
        self.set_models_selector(THSStockMarket.tag['rule'],
                                 {THSStockMarket.tag['tag']: THSStockMarket})

    def reg_rule_list(self):
        self.set_rule_sort_list(THSChanceInfo.tag['rule'])
        self.set_rule_sort_list(THSFinanceFirstPage.tag['rule'])
        self.set_rule_sort_list(THSMainNews.tag['rule'])
        self.set_rule_sort_list(THSHomePage.tag['rule'])
        self.set_rule_sort_list(THSFamous.tag['rule'])
        self.set_rule_sort_list(THSFinanceFocus.tag['rule'])
        self.set_rule_sort_list(THSFinanceMacroscopic.tag['rule'])
        self.set_rule_sort_list(THSOriginalSole.tag['rule'])
        self.set_rule_sort_list(THSStockNews.tag['rule'])
        self.set_rule_sort_list(THSStockNotice.tag['rule'])
        self.set_rule_sort_list(THSStockResearch.tag['rule'])
        self.set_rule_sort_list(THSStockGrail.tag['rule'])
        self.set_rule_sort_list(THSStockInvestment.tag['rule'])
        self.set_rule_sort_list(THSStockRolling.tag['rule'])
        self.set_rule_sort_list(THSStockCompany.tag['rule'])
        self.set_rule_sort_list(THSStockEarly.tag['rule'])
        self.set_rule_sort_list(THSStockFirstPage.tag['rule'])
        self.set_rule_sort_list(THSStockIndustry.tag['rule'])
        self.set_rule_sort_list(THSStockMarket.tag['rule'])

    def analyzed(self, params):
        """
        解析完成
        """
        ModelManagerBase.analyzed(self, **params)

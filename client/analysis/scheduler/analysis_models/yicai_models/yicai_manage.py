# -.- coding:utf-8 -.-
"""
Created on 2015年10月30日

@author: chenyitao
"""

from scheduler.analysis_models.model_namager_base import ModelManagerBase
from scheduler.analysis_models.yicai_models.homepage import YCHomePage
from scheduler.analysis_models.yicai_models.dotting import YCdotting
from scheduler.analysis_models.yicai_models.economy import YCeconomy
from scheduler.analysis_models.yicai_models.finance_yc import YCfinance
from scheduler.analysis_models.yicai_models.focus import YCFocus
from scheduler.analysis_models.yicai_models.markets import YCMarkets
from scheduler.analysis_models.yicai_models.opinion import YCOpinion
from scheduler.analysis_models.yicai_models.others_page import NextPage
from scheduler.analysis_models.yicai_models.politics import YCPolitics


class YiCaiManager(ModelManagerBase):
    """
    class docs
    """
    platform_id = 3
    rules_level = {}

    def reg_models(self):
        """
        YC_HOME_PAGE_TAG: 页面唯一标识
        YCHomePage: 页面解析类
        """
        self.set_models_selector(YCHomePage.tag['rule'], {YCHomePage.tag['tag']: YCHomePage})
        self.set_models_selector(YCdotting.tag['rule'], {YCdotting.tag['tag']: YCdotting})
        self.set_models_selector(YCeconomy.tag['rule'], {YCeconomy.tag['tag']: YCeconomy})
        self.set_models_selector(YCfinance.tag['rule'], {YCfinance.tag['tag']: YCfinance})
        self.set_models_selector(YCFocus.tag['rule'], {YCFocus.tag['tag']: YCFocus})
        self.set_models_selector(YCMarkets.tag['rule'], {YCMarkets.tag['tag']: YCMarkets})
        self.set_models_selector(YCOpinion.tag['rule'], {YCOpinion.tag['tag']: YCOpinion})
        self.set_models_selector(NextPage.tag['rule'], {NextPage.tag['tag']: NextPage})
        self.set_models_selector(YCPolitics.tag['rule'], {YCPolitics.tag['tag']: YCPolitics})

    def reg_rule_list(self):
        self.set_rule_sort_list(YCHomePage.tag['rule'])
        self.set_rule_sort_list(YCdotting.tag['rule'])
        self.set_rule_sort_list(YCeconomy.tag['rule'])
        self.set_rule_sort_list(YCfinance.tag['rule'])
        self.set_rule_sort_list(YCFocus.tag['rule'])
        self.set_rule_sort_list(YCMarkets.tag['rule'])
        self.set_rule_sort_list(YCOpinion.tag['rule'])
        self.set_rule_sort_list(YCPolitics.tag['rule'])
        self.set_rule_sort_list(NextPage.tag['rule'])

    def analyzed(self, params):
        """
        解析完成
        """
        ModelManagerBase.analyzed(self, **params)


def main():
    """
    test
    """
    manager = YiCaiManager()
    manager.setDaemon(True)
    manager.start()
    with open('./yicai_homepage.html', 'r') as f:
        html_data = f.read()
    manager.add_task(**{'content': html_data})
    import time
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()

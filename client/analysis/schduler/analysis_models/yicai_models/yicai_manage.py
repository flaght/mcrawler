# -.- coding:utf-8 -.-
'''
Created on 2015年10月30日

@author: chenyitao
'''

from schduler.analysis_models.model_namager_base import ModelManagerBase
from schduler.analysis_models.yicai_models.homepage import YCHomePage
from schduler.analysis_models.yicai_models.dotting import YCdotting
from schduler.analysis_models.yicai_models.economy import YCeconomy
from schduler.analysis_models.yicai_models.finance_yc import YCfinance
from schduler.analysis_models.yicai_models.focus import YCfocus
from schduler.analysis_models.yicai_models.markets import YCmarkets
from schduler.analysis_models.yicai_models.opinion import YCopinion
from schduler.analysis_models.yicai_models.others_page import NextPage
from schduler.analysis_models.yicai_models.politics import YCpolitics

class YicaiManager(ModelManagerBase):
    '''
    classdocs
    '''
    platform_id = 3
    rules_level = {}
    
    def reg_models(self):
        '''
        YC_HOME_PAGE_TAG: 页面唯一标识
        YCHomePage: 页面解析类
        '''
        self.set_models_selector(YCHomePage.tag['rule'], {YCHomePage.tag['tag']:YCHomePage})
        self.set_models_selector(YCdotting.tag['rule'], {YCdotting.tag['tag']:YCdotting})
        self.set_models_selector(YCeconomy.tag['rule'], {YCeconomy.tag['tag']:YCeconomy})
        self.set_models_selector(YCfinance.tag['rule'], {YCfinance.tag['tag']:YCfinance})
        self.set_models_selector(YCfocus.tag['rule'], {YCfocus.tag['tag']:YCfocus})
        self.set_models_selector(YCmarkets.tag['rule'], {YCmarkets.tag['tag']:YCmarkets})
        self.set_models_selector(YCopinion.tag['rule'], {YCopinion.tag['tag']:YCopinion})
        self.set_models_selector(NextPage.tag['rule'], {NextPage.tag['tag']:NextPage})
        self.set_models_selector(YCpolitics.tag['rule'], {YCpolitics.tag['tag']:YCpolitics})

    def reg_rule_list(self):
        self.set_rule_sort_list(YCHomePage.tag['rule'])
        self.set_rule_sort_list(YCdotting.tag['rule'])
        self.set_rule_sort_list(YCeconomy.tag['rule'])
        self.set_rule_sort_list(YCfinance.tag['rule'])
        self.set_rule_sort_list(YCfocus.tag['rule'])
        self.set_rule_sort_list(YCmarkets.tag['rule'])
        self.set_rule_sort_list(YCopinion.tag['rule'])
        self.set_rule_sort_list(YCpolitics.tag['rule'])
        self.set_rule_sort_list(NextPage.tag['rule'])

    def analyzed(self, params):
        '''
        解析完成
        '''
        ModelManagerBase.analyzed(self, **params)

def main():
    '''
    test
    '''
    manager = YicaiManager()
    manager.setDaemon(True)
    manager.start()
    with open('./yicai_homepage.html', 'r') as f:
        html_data = f.read()
    manager.add_task(**{'content':html_data})
    import time
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()

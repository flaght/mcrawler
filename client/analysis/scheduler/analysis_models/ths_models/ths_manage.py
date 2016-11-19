# -.- coding:utf-8 -.-
"""
Created on 2015年11月3日

@author: chenyitao
"""

from scheduler.analysis_models.model_namager_base import ModelManagerBase
from scheduler.analysis_models.ths_models.ths_optional_unit_analysis_model import ThsOptionalUnitAnalysis


class ThsManager(ModelManagerBase):
    """
    class docs
    """
    platform_id = 1

    def reg_models(self):
        """
        YC_HOME_PAGE_TAG: 页面唯一标识
        YCHomePage: 页面解析类
        """
        self.models_selector[ThsOptionalUnitAnalysis.tag['rule']] = {
                    ThsOptionalUnitAnalysis.tag['tag']: ThsOptionalUnitAnalysis}

    def analyzed(self, params):
        """
        解析完成
        """
        print params

# -.- coding:utf-8 -.-
"""
Created on 2015年11月16日

@author: chenyitao
"""
from schduler.analysis_models.analysis_base import AnalysisBase
from schduler.analysis_models.analyzed_info import AnalyzedInfo


class YCAnalysisBase(AnalysisBase):
    """
    class docs
    """

    def __make_storage_cmd(self):
        for analysis_info in self.analyzed_info_list:
            self.storage_cmd_list.append({'table': '3_analyzed',
                                          'key': analysis_info.url,
                                          'info': {'title': analysis_info.title,
                                                   'category': analysis_info.type,
                                                   'section': analysis_info.model,
                                                   'industry': analysis_info.vocation,
                                                   'url': analysis_info.url}})

    def analyzed(self):
        self.__make_storage_cmd()
        AnalysisBase.analyzed(self)

    def set_analyzed_info(self, title=None, _type=None, model=None, vocation=None, url=None):
        """
        设置analyzed info
        """
        if url in self.url_list:
            return
        analyzed_info = AnalyzedInfo()
        analyzed_info.title = title
        analyzed_info.type = _type
        analyzed_info.model = model
        analyzed_info.vocation = vocation
        analyzed_info.url = url
        #         self.url_list.append(url)
        self.analyzed_info_list.append(analyzed_info)

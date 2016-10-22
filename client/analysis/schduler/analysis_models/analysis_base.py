# -.- coding:utf-8 -.-
"""
Created on 2015年10月31日

@author: chenyitao
"""


class AnalysisBase(object):
    """
    解析基类
    tag：唯一标识（由字典组成：tag:唯一标识 rule:解析唯一标识的规则）
    storage_type：存储类型
    storage_cmd_list：存储指令
    """

    tag = None
    storage_type = 0
    default_analysis_model = 'default_analysis_model'

    def __init__(self, callback=None, **kwargs):
        """
        callback:解析结束回调函数
        kwargs:需要解析的数据（由字典组成：content:html内容……）
        """
        self.analyzed_info_list = []
        self.storage_cmd_list = []
        self.url_list = []
        self.kwargs = None
        self.html_data = None
        self.finished = None
        self.kwargs = kwargs
        if not self.kwargs:
            print 'kwargs is none'
            return
        self.html_data = self.kwargs['content']
        if not self.html_data:
            print 'html_data is none'
        self.finished = callback
        if not self.finished:
            print 'analysis callback is none'

    def get_storage_commands(self):
        """
        get storage sentence
        """
        return self.storage_cmd_list

    def analyzed(self):
        """
        必须在解析以及其他操作处理完后调用
        """
        if self.finished:
            self.url_list = list(set(self.url_list))
            self.finished({'storage_cmd_list': self.storage_cmd_list,
                           'url_list': self.url_list,
                           'storage_type': self.storage_type})

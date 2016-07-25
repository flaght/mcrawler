# -*- coding:utf-8 -*-
'''
Create on 2015年12月2日

@author: slm
'''
from schduler.analysis_models.analysis_base import AnalysisBase
from schduler.analysis_models.weibo_models.analyzed_info_expert import AnalyzedInfoExpert
from schduler.analysis_models.weibo_models.analyzed_info_stock import AnalyzedInfoStock
from schduler.analysis_models.weibo_models.analyzed_info_weibos import AnalyzedInfoWeibos

class WBAnalysisBase(AnalysisBase):
    '''
    解析基类
    '''
    def set_analyzed_info_expert(self, weibo_id=None, url=None):
        '''
        专家
        '''
        if url in self.url_list:
            return
        analyzed_info = AnalyzedInfoExpert()
        analyzed_info.weibo_id = weibo_id
        analyzed_info.url = url
        self.url_list.append(url)
        self.analyzed_info_list.append(analyzed_info)

    def make_storage_cmd_expert(self):
        '''
        存储专家命令
        '''
        for analysis_info in self.analyzed_info_list:
            self.storage_cmd_list.append({'table':'4_analyzed',
                                          'key':analysis_info.url,
                                          'info':{'weibo_name':analysis_info.weibo_name,
                                                   'url':analysis_info.url}})

    def set_analyzed_info_stock(self, stock_name=None, stock_code=None, concern_num=None):
        '''
        股票
        '''
        analyzed_info = AnalyzedInfoStock()
        analyzed_info.stock_name = stock_name
        analyzed_info.stock_code = stock_code
        analyzed_info.concern_num = concern_num
        self.analyzed_info_list.append(analyzed_info)

    def make_storage_cmd_stock(self):
        '''
        存储股票命令
        '''
        for analysis_info in self.analyzed_info_list:
            self.storage_cmd_list.append({'table':'4_analyzed',
                                          'key':analysis_info.stock_code,
                                          'info':{'stock_name':analysis_info.stock_name,
                                                   'stock_code':analysis_info.stock_code,
                                                   'concern_num':analysis_info.concern_num}})

    def set_analyzed_info_weibos(self, weibo_id=None, weibo=None, share_weibo_id=None,
                                 share_num=None, comment_num=None, likes_num=None):
        '''
        微博
        '''
        analyzed_info = AnalyzedInfoWeibos()
        analyzed_info.weibo_id = weibo_id
        analyzed_info.weibo = weibo
        analyzed_info.share_weibo_id = share_weibo_id
        analyzed_info.share_num = share_num
        analyzed_info.comment_num = comment_num
        analyzed_info.likes_num = likes_num
        self.analyzed_info_list.append(analyzed_info)

    def make_storage_cmd_weibos(self):
        '''
        存储微博命令
        '''
        for analysis_info in self.analyzed_info_list:
            self.storage_cmd_list.append({'table':'4_analyzed',
                                          'key':analysis_info.weibo_id,
                                          'info':{'weibo_id':analysis_info.weibo_id,
                                                   'weibo':analysis_info.weibo,
                                                   'share_num':analysis_info.share_num,
                                                   'comment_num':analysis_info.comment_num,
                                                   'likes_num':analysis_info.likes_num}})
    
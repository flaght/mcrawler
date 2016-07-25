# -.- coding:utf-8 -.-
'''
Created on 2015年11月30日

@author: chenyitao
'''
from schduler.analysis_models.analysis_base import AnalysisBase
from schduler.analysis_models.analyzed_info import AnalyzedInfo

class CNAnalysisBase(AnalysisBase):
    '''
    docs
    '''
    def set_analyzed_info(self, title=None, _type=None, model=None, vocation=None, url=None):
        '''
        标题、url
        '''
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

    def make_storage_cmd(self):
        '''
        标题、url
        '''
        for analysis_info in self.analyzed_info_list:
            self.storage_cmd_list.append({'table':'5_analyzed',
                                          'key':analysis_info.url,
                                          'info':{'title':analysis_info.title,
                                                   'category':analysis_info.type,
                                                   'section':analysis_info.model,
                                                   'industry':analysis_info.vocation,
                                                   'url':analysis_info.url}})

    def set_analyzed_info_word(self, current_id=None, date=None, content=None,
                               introduction=None, like_num=None, unlike_num=None,
                               comment_detail=None):
        '''
        普通新闻
        '''
        analyzed_info = AnalyzedInfo()
        analyzed_info.current_id = current_id
        analyzed_info.date = date
        analyzed_info.content = content
        analyzed_info.introduction = introduction
        analyzed_info.like_num = like_num
        analyzed_info.unlike_num = unlike_num
        analyzed_info.comment_detail = comment_detail
        self.analyzed_info_list.append(analyzed_info)

    def make_storage_cmd_words(self):
        '''
        存储普通新闻命令
        '''
        for analysis_info in self.analyzed_info_list:
            self.storage_cmd_list.append({'table':'5_analyzed',
                                          'key':analysis_info.current_id,
                                          'info':{'current_id':analysis_info.current_id,
                                                   'date':analysis_info.date,
                                                   'content':analysis_info.content,
                                                   'introduction':analysis_info.introduction,
                                                   'like_num':analysis_info.like_num,
                                                   'unlike_num':analysis_info.unlike_num,
                                                   'comment_detail':analysis_info.comment_detail}})

    def set_analyzed_info_picture(self, current_id=None, date=None, content=None, introduction=None,
                                  join_num=None, comment_num=None, comment_detail=None):
        '''
        图集新闻
        '''
        analyzed_info = AnalyzedInfo()
        analyzed_info.current_id = current_id
        analyzed_info.date = date
        analyzed_info.content = content
        analyzed_info.introduction = introduction
        analyzed_info.join_num = join_num
        analyzed_info.comment_num = comment_num
        analyzed_info.comment_detail = comment_detail
        self.analyzed_info_list.append(analyzed_info)

    def make_storage_cmd_picture(self):
        '''
        存储图集新闻命令
        '''
        for analysis_info in self.analyzed_info_list:
            self.storage_cmd_list.append({'table':'5_analyzed',
                                          'key':analysis_info.current_id,
                                          'info':{'current_id':analysis_info.current_id,
                                                   'date':analysis_info.date,
                                                   'content':analysis_info.content,
                                                   'introduction':analysis_info.introduction,
                                                   'join_num':analysis_info.join_num,
                                                   'comment_num':analysis_info.comment_num,
                                                   'comment_detail':analysis_info.comment_detail}})
    
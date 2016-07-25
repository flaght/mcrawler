# -.- coding:utf-8 -.-
'''
Created on 2015年12月4日

@author: slm
'''

class AnalyzedInfo(object):
    '''
    Args:
    content_id:内容id
    date:日期
    content:内容
    comment_num:评论数量
    like_num:点赞数
    unlike_num:踩数量
    comment_detail:评论详情
    '''
    __struct_fmt = '=H'
    content_id = None
    date = None
    content = None
    comment_num = None
    like_num = None
    unlike_num = None
    comment_detail = None

    def __init__(self, params=None):
        '''
        Constructor
        '''
        if not params:
            return
        self.content_id = ''
        self.date = ''
        self.content = ''
        self.comment_num = ''
        self.like_num = ''
        self.unlike_num = ''
        self.comment_detail = []

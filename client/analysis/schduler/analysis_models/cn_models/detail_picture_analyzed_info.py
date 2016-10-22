# -.- coding:utf-8 -.-
"""
Created on 2015年12月3日

@author: slm
"""


class AnalyzedInfo(object):
    """
    Args:
    current_id:当前新闻id
    date:日期
    content:内容
    introduction:导读
    comment_num:评论数量
    like_num:点赞数
    unlike_num:踩数量
    comment_detail:评论详情
    """
    __struct_fmt = '=H'
    current_id = None
    date = None
    content = None
    introduction = None
    join_num = None
    comment_num = None
    comment_detail = None

    def __init__(self, params=None):
        """
        Constructor
        """
        if not params:
            return
        self.current_id = ''
        self.date = ''
        self.content = ''
        self.introduction = ''
        self.join_num = ''
        self.comment_num = ''
        self.comment_detail = []

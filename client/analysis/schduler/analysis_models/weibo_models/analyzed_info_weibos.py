# -*- coding:utf-8 -*-
"""
Created on 2015年12月3日

@author: slm
"""


class AnalyzedInfoWeibos(object):
    """
    weibo:微博内容
    share_num:分享数
    share_weibo_id：转发微博的博主id
    comment_num:评论数
    likes_num:点赞数
    """
    __struct_fmt = '=H'
    weibo_id = None
    weibo = None
    share_weibo_id = None
    share_num = None
    comment_num = None
    likes_num = None

    def __init__(self, params=None):
        """
        Constructor
        """
        if not params:
            return
        self.weibo_id = ''
        self.weibo = ''
        self.share_weibo_id = ''
        self.share_num = ''
        self.comment_num = ''
        self.likes_num = ''

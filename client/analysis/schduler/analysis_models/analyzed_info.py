# -.- coding:utf-8 -.-
'''
Created on 2015年11月2日

@author: chenyitao
'''

class AnalyzedInfo(object):
    '''
    Args:
    title:标题
    type:类别
    model:模块
    vocation:行业
    url:链接
    '''
    
    __struct_fmt = '=H'
    title = None
    type = None
    model = None
    vocation = None
    url = None

    def __init__(self, params=None):
        '''
        Constructor
        '''
        if not params:
            return
        self.title = ''
        self.type = ''
        self.model = ''
        self.vocation = ''
        self.url = ''

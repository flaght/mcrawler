# -.- coding:utf-8 -.-
'''
Created on 2015年11月16日

@author: chenyitao
'''

import random

class CookiesManager(object):
    '''
    Cookies管理器
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.cookies = {}
        self.history = []

    def set_cookies(self, attr_id, action=0, cookies=None):
        '''
        设置平台cookies
        action:0 replace  1 extend
        '''
        if attr_id == 1:
            self.history.extend(cookies)
            self.history = list(set(self.history))
        if action:
            self.cookies[attr_id] = cookies
        else:
            if attr_id not in self.cookies.keys():
                self.cookies[attr_id] = []
            self.cookies[attr_id].extend(cookies)

    def get_cookie(self, attr_id, is_pop=True):
        '''
        get a cookie
        '''
        if attr_id not in self.cookies.keys():
            return None
        if not is_pop and len(self.cookies[attr_id]):
            return random.choice(self.cookies[attr_id])
        elif len(self.cookies[attr_id]):
            return self.cookies[attr_id].pop(0)

    def get_cookies(self, attr_id, is_pop=True):
        '''
        is_pop:False    get cookies
        is_pop:True     pop cookies
        '''
        if attr_id not in self.cookies.keys():
            return None
        if not is_pop:
            return self.cookies[attr_id]
        return self.cookies.pop(attr_id)

    def get_cookie_random(self, attr_id):
        '''
        获取随机cookie
        '''
        if attr_id not in self.cookies.keys():
            return None
        cookies = self.cookies[attr_id]
        if not len(cookies):
            return None
        return random.choice(cookies)

cookies_manager = CookiesManager()

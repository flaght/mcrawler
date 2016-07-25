# -*- coding:utf-8 -*-
'''
Created on 2015年11月09日

@author: slm
'''
import urllib

class GetUsefulUrl(object):
    '''
    筛选url
    '''
    def __init__(self, url_list):
        self.url_list = url_list
        self.removed_list = []
        self.useful_list = []
        self.remove_same_url()

    def remove_same_url(self):
        '''
        去除列表中重复的url
        '''
        url_set = set(self.url_list)
        self.removed_list = [i for i in url_set]
        self.get_url_domain()

    def get_url_domain(self):
        '''
        获得url域名，把站外的url排除
        '''
        for url in self.removed_list:
            proto, url_type = urllib.splittype(url)  # @UnusedVariable
            domain_name, others = urllib.splithost(url_type)  # @UnusedVariable
            if domain_name == 'www.yicai.com':
                self.useful_list.append(url)

def main():
    '''
    测试
    '''
    test_list = ['https://www.baidu.com/',
                 'http://www.douban.com/note/310564813/',
                 'http://www.douban.com/note/332584951/',
                 'http://www.v2ex.com/t/65589',
                 'http://www.yicai.com/economy/',
                 'http://www.yicai.com/economy/',
                 'http://www.yicai.com/ajax.php?op=getnewslist&type=1&typename=&page=2']
    test_object = GetUsefulUrl(test_list)
    print test_object.useful_list

if __name__ == '__main__':
    main()
    
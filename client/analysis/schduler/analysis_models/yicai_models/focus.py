# -*- coding:utf-8 -*-
'''
Created on 2015年11月2日

@author: slm
'''
import urllib2
import os
from lxml import html
from schduler.analysis_models.yicai_models.yicai_analysis_base import YCAnalysisBase

class YCfocus(YCAnalysisBase):
    '''
    第一财经主页更多聚焦分页解析
    '''
    tag = {'rule':'//*[@id="content"]/div[@class="eyeball"]/h3',
           'tag':'聚焦'}

    def __init__(self, callback=None, **kwargs):
        '''
        tag：唯一标识
        storage_type：存储类型
        storage_cmd_list：存储指令
        '''
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '聚焦'
        self.analyzed_info_list = []
        #解析
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        '''
        解析
        '''
#         with open('./yicai_focus.html', 'r') as f:
#             self.html_data = f.read()
        doc = html.fromstring(self.html_data)
        self.__focus(doc)
        self.__update(doc)
        self.__talk(doc)

    def __focus(self, doc):
        '''
        聚焦
        '''
        model = '资讯'
        news = doc.xpath(r'//div[@id="content"]//tr//td[@valign="top"]//dd//h1')
        for one_new in news:
            title = one_new.xpath(r'a/text()')[0].encode('utf-8')
            url = one_new.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)

    def __update(self, doc):
        '''
        最近更新
        '''
        model = '最近更新'
        news = doc.xpath(r'//div[@id="content"]//div[@class="update"]//h4')
        for one_new in news:
            title = one_new.xpath(r'a/text()')[0].encode('utf-8')
            url = one_new.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)

    def __talk(self, doc):
        '''
        对话互联网金融
        '''
        model = '对话互联网金融'
        news = doc.xpath(r'//div[@id="content"]//tr//td[2]//div[1]//ul//li//p')
        for one_new in news:
            title = one_new.xpath(r'a/text()')[0].encode('utf-8')
            url = one_new.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)

def main():
    '''
    测试
    '''
    analysis = YCfocus()
    print len(analysis.analyzed_info_list)
    for info in analysis.analyzed_info_list:
        print info.title
        print info.url
        print info.model
        print info.type
        print '============'
    print analysis

def load_data():
    '''
    加载要解析的html
    '''
    if not os.path.exists('./yicai_focus.html'):
        response = urllib2.urlopen('http://www.yicai.com/focus/index.html')
        with open('./yicai_focus.html', 'w') as f:
            f.write(response.read())

if __name__ == '__main__':
    load_data()
    main()
    
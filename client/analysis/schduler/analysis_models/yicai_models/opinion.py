# -*- coding:utf-8 -*-
'''
Created on 2015年11月2日

@author: slm
'''
import urllib2
import os
from lxml import html
from schduler.analysis_models.yicai_models.analysis import YCAnalysis
from schduler.analysis_models.yicai_models.yicai_analysis_base import YCAnalysisBase

class YCopinion(YCAnalysisBase):
    '''
    第一财经主页思想分页解析(cid=201&subcid=225)
    '''
    tag = {'rule':'//*[@id="menulist"]/li[contains(@class, "hover")]/a',
           'tag':'思想'}

    def __init__(self, callback=None, **kwargs):
        '''
        tag：唯一标识
        storage_type：存储类型
        storage_cmd_list：存储指令
        '''
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '思想'
        self.analyzed_info_list = []
        #解析
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        '''
        解析
        '''
#         with open('./yicai_opinion.html', 'r') as f:
#             self.html_data = f.read()
        doc = html.fromstring(self.html_data)
        #类别列表
        self.category = doc.xpath(r'//div[@id="Tab1"]//li/text()')
        self.module = doc.xpath(r'//ul[@id="menulist"]//a/text()')[9]
        self.__header_news(doc)
        self.__middle_all_news(doc)
        self.__get_url_list(doc)

    def __get_url_list(self, doc):
        '''
        获得要返回给服务器的url
        '''
        #把后面url返回给服务器
        analysis = YCAnalysis('1', '9', doc, 201, 225)
        analysis.middle_first_next_url()
        for url_info in analysis.next_url_list:
            self.url_list.append(url_info)

    def __header_news(self, doc):
        '''
        头部咨询栏
        '''
        model = '资讯'
        header_news = doc.xpath(r'//div[@id="content"]//div[@class="banana"]//h1')
        for header_new in header_news:
            title = header_new.xpath(r'a/text()')[0].encode('utf-8')
            url = header_new.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)

    def __middle_all_news(self, doc):
        '''
        全部
        '''
        header_news = doc.xpath(r'//div[@id="con_one_1"]/dl//h1')
        for header_new in header_news:
            title = header_new.xpath(r'a/text()')[0].encode('utf-8')
            url = header_new.xpath(r'a/@href')[0].encode('utf-8')
            model = doc.xpath\
            (r'//div[@id="Tab1"]//li/text()')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)

def main():
    '''
    测试
    '''
    analysis = YCopinion()
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
    if not os.path.exists('./yicai_opinion.html'):
        response = urllib2.urlopen('http://www.yicai.com/opinion/')
        with open('./yicai_opinion.html', 'w') as f:
            f.write(response.read())

if __name__ == '__main__':
    load_data()
    main()
    
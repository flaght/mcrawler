# -*- coding:utf-8 -*-
'''
Create on 2015年12月02日

@author: slm
'''
import urllib2
import os
from lxml import html
from schduler.analysis_models.cn_models.cn_analysis_base import CNAnalysisBase
from schduler.analysis_models.analysis_base import AnalysisBase

class CNFinance(CNAnalysisBase):
    '''
    财经频道
    '''
    tag = {'rule':'/html/head/title/text()',
           'tag':'财经频道-21CN'}

    def __init__(self, callback=None, **kwargs):
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '财经'
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def analyzed(self):
        '''
        解析完成
        '''
        self.make_storage_cmd()
        AnalysisBase.analyzed(self)

    def __analysis(self):
        '''
        解析
        '''
#         with open('./21cn_finance.html', 'r') as f:
#             self.html_data = f.read()
        doc = html.fromstring(self.html_data)
        self.__scroll_news(doc)
        self.__main_news(doc)
        self.__express_news(doc)
        self.__get_url_list(doc)

    def __get_url_list(self, doc):
        '''
        将宏观1、产经2、金融3的url返给服务器
        '''
        model_list = doc.xpath(r'//div[@class="nav"]//a/@href')        
        self.url_list.append(model_list[1])
        self.url_list.append(model_list[2])
        self.url_list.append(model_list[3])

    def __express_news(self, doc):
        '''
        财经速递
        '''
        news_list = doc.xpath(r'//div[@class="col-r"]//div[@class="mod"]')
        model = '财经'
        for news in news_list:
            name_list = news.xpath(r'div[@class="hd"]/h3/a/text()')
            if len(name_list) == 0:
                continue
            name = name_list[0].encode('utf-8')
            if name == '财经速递':
                express_news_list = news.xpath(r'div[@class="picTxtList splitLine"]//ul//li')
                for express in express_news_list:
                    title = express.xpath(r'p/a/text()')[0].encode('utf-8')
                    url = express.xpath(r'p/a/@href')[0].encode('utf-8')
                    self.set_analyzed_info(title, self._type, model, None, url)

    def __main_news(self, doc):
        '''
        财经要闻、宏观经济、产经动态、热点观察
        '''
        model_list = doc.xpath(r'//div[@class="main"]//div[@class="mod"]')
        for model_info in model_list:
            name = model_info.xpath(r'div[@class="hd"]/h3/a/text()')[0].encode('utf-8')
            if name == '证券行情' or name == '宏观经济':
                continue
            elif name == '热点观察':
                self.__hot_news(model_info)
            else:#财经要闻 产经动态
                print name
                self.__left_news(model_info)
                self.__right_news_with_picture(model_info)
                #把这三模块的url返给服务器
                name_url = model_info.xpath(r'div[@class="hd"]/h3/a/@href')[0].encode('utf-8')
                self.url_list.append(name_url)

    def __hot_news(self, doc):
        '''
        热点观察
        '''
        model = '热点观察'
        picture_list = doc.xpath(r'//ul[@id="new-pic-list"]//li')
        for picture in picture_list:
            title = picture.xpath(r'a/em/text()')[0].encode('utf-8')
            url = picture.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)

    def __right_news_with_picture(self, doc):
        '''
        右边图片新闻
        '''
        model = '财经要闻'
        picture_list = doc.xpath(r'div[@class="bd clearfix"]//div[@class="fr"]//div')
        for picture in picture_list:
            title = picture.xpath(r'a/em/text()')[0].encode('utf-8')
            url = picture.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)

    def __left_news(self, doc):
        '''
        左边无图片新闻
        '''
        model = '财经要闻'
        top_news_list = doc.xpath(r"div[@class='bd clearfix']//li[(contains(@class,'top1'))]")
        for top_new in top_news_list:
            title = top_new.xpath(r'a/b/text()')[0].encode('utf-8')
            url = top_new.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)
        bottom_news_url = doc.xpath(r"div[@class='bd clearfix']//li[not(contains(@class,'top1'))]")
        for bottom_new in bottom_news_url:
            title = bottom_new.xpath(r'a/text()')[0].encode('utf-8')
            url = bottom_new.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)

    def __scroll_news(self, doc):
        '''
        滚动试图
        '''
        scroll_news_list = doc.xpath(r'//div[@id="focus-image"]//li')
        model = '滚动新闻'
        for news in scroll_news_list:
            title = news.xpath(r'a/span/text()')[0].encode('utf-8')
            url = news.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)

def main():
    '''
    执行
    '''
    analysis = CNFinance()
    print analysis
    for analyzed_info in analysis.analyzed_info_list:
        print analyzed_info.title
        print analyzed_info.type
        print analyzed_info.model
        print analyzed_info.vocation
        print analyzed_info.url
        print '================='

def load_data():
    '''
    加载html
    '''
    if not os.path.exists('./21cn_finance.html'):
        response = urllib2.urlopen('http://finance.21cn.com/')
        with open('./21cn_finance.html', 'w') as f:
            f.write(response.read())

if __name__ == '__main__':
    load_data()
    main()

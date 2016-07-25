# -.- coding:utf-8 -.-
'''
Created on 2015年12月23日

@author: slm
'''
import os
import sys
import urllib2

import chardet
from lxml import html

from schduler.analysis_models.ths_more_models.ths_analysis.more_news_base import MoreNewsBase


class THSMainNews(MoreNewsBase):
    '''
    要闻（2.财经要闻）
    '''
    tag = {'rule': '/html/head/title',
           'tag': '要闻-财经新闻频道-同花顺财经'}

    def __init__(self, callback=None, **kwargs):
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '财经要闻'
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        '''
        解析
        '''
#         with open('./ths_finance_news.html', 'r') as f:
#             self.html_data = f.read()
        try:
            self.html_data = self.gzdecode(self.html_data)
        except:
            pass
        typeEncode = sys.getfilesystemencoding()#系统默认编码
        infoencode = chardet.detect(self.html_data).get('encoding')#通过第3方模块来自动提取网页的编码
#         #先转换成unicode编码，然后转换系统编码输出
        self.html_data = self.html_data.decode(infoencode, 'ignore').encode(typeEncode)
        doc = html.fromstring(self.html_data)
        self.__get_model_url(doc)
        self.__tody_focus_news(doc)
        self.__finance_focus_news(doc)
        self.__domestic_economy(doc)

    def __get_model_url(self, doc):
        '''
        获得本页爬取的2级页面
        '''
        model_urls = doc.xpath(r'//ul[@id="zixuyekaqu"]//li')
        for model_url in model_urls:
            title = model_url.xpath(r'a/text()')[0].encode('ISO-8859-1')
            if title == '财经要闻' or title == '国内经济':
                #将此url传给服务器
                title_url = model_url.xpath(r'a/@href')[0]
                self.url_list.append(title_url)

    def __domestic_economy(self, doc):
        '''
        国内经济
        '''
        model = '国内经济'
        economy_news = doc.xpath(r'//li[@class=" clearfix zixuqu"]//a')
        for new in economy_news:
            title = new.xpath(r'div/span[@class="title"]/text()')[0].encode('ISO-8859-1')
            url = new.xpath(r'@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)

    def __finance_focus_news(self, doc):
        '''
        财经要闻
        '''
        model = '财经要闻'
        focus_news = doc.xpath(r'//ul[@id="caijin_list"]//a')
        for new in focus_news:
            title = new.xpath(r'div/span[@class="title"]/text()')[0].encode('ISO-8859-1')
            url = new.xpath(r'@href')[0].encode('ISO-8859-1')
            self.set_analyzed_info(title, self._type, model, None, url)

    def __tody_focus_news(self, doc):
        '''
        今日要闻
        '''
        model = '今日要闻'
        picture_new_title = doc.xpath\
        (r'//span[@data-tce-tag="intr"]/text()')[0].encode('ISO-8859-1')
        picture_new_url = doc.xpath(r'//div[@id="toutiaoqu"]//a/@href')[0].encode('ISO-8859-1')
        self.set_analyzed_info(picture_new_title, self._type, model, None, picture_new_url)
        focus_news = doc.xpath(r'//div[@class="box today-focus-text fl"]/ul//a')
        for new in focus_news:
            title = new.xpath(r'text()')[0].encode('ISO-8859-1').strip()
            url = new.xpath(r'@href')[0].encode('ISO-8859-1')
            self.set_analyzed_info(title, self._type, model, None, url)

def main():
    '''
    执行
    '''
    analysis = THSMainNews()
    for info in analysis.analyzed_info_list:
        print info.title
        print info.url
        print info.model
        print info.type
        print '============'
    print analysis

def load_data():
        '''
        加载网页html
        '''
        if not os.path.exists('./ths_finance_news.html'):
            response = urllib2.urlopen('http://news.10jqka.com.cn/yaowen/')
            with open('./ths_finance_news.html', 'w') as f:
                f.write(response.read())

if __name__ == '__main__':
    load_data()
    main()
    
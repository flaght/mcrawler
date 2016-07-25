# -.- coding:utf-8 -.-
'''
Created on 2015年12月28日

@author: slm
'''
import urllib2
import os
from lxml import html
from schduler.analysis_models.ths_more_models.ths_analysis.more_news_base import MoreNewsBase

class THSStockFristpage(MoreNewsBase):
    '''
    股票首页（15.股票频道）
    '''
    tag = {'rule': '/html/head/title',
           'tag':'股票频道-提供今日最新股票行情信息,股票新闻资讯,股票投资_同花顺财经'}

    def __init__(self, callback=None, **kwargs):
        '''
        Constructor
        '''
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '股票'
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        '''
        解析
        '''
#         with open('./ths_stock.html', 'r') as f:
#             self.html_data = f.read()
        try:
            self.html_data = self.gzdecode(self.html_data)
        except:
            pass
        doc = html.fromstring(self.html_data)
        self.__get_model_url(doc)
        self.__securities_news(doc)
        self.__listed_company(doc)
        self.__industry_research(doc)
        self.__stocks_research(doc)

    def __get_model_url(self, doc):
        '''
        获得下一级模块url
        '''
        early_url = doc.xpath(r'//div[@id="block_2850"]//a/@href')[1].encode('utf-8')
        self.url_list.append(early_url)
        model_url_list = doc.xpath(r'//div[@id="block_2849"]//a')
        for model in model_url_list:
            model_title = model.xpath(r'text()')[0].encode('utf-8')
            if model_title == '市场' or model_title == '行业' or model_title == '公司':
                model_url = model.xpath(r'@href')[0].encode('utf-8')
                self.url_list.append(model_url)

    def __stocks_research(self, doc):
        '''
        个股研究
        '''
        model = '个股研究'
        more_news = doc.xpath\
        (r'//div[@class="ui-section clearfix"]//div[@class="ui-box"]//ul//li//a')
        for new in more_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __industry_research(self, doc):
        '''
        行业研究
        '''
        model = '行业研究'
        more_news = doc.xpath(r'//div[@class="ui-box pb-m"]//ul[@class="ui-list"]//li//a')
        for new in more_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __listed_company(self, doc):
        '''
        上市公司
        '''
        model = '上市公司'
        more_news = doc.xpath(r'//div[@class="ui-box companynews"]//ul//li//a')
        for new in more_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __securities_news(self, doc):
        '''
        证劵要闻
        '''
        model = '证劵要闻'
        more_news = doc.xpath\
        (r'//div[@class="ui-box noborder bondnews"]//div[@class="secnews-title"]//h3//a')
        for new in more_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

def load_data():
    '''
    加载网页html
    '''
    if not os.path.exists('./ths_stock.html'):
        response = urllib2.urlopen('http://stock.10jqka.com.cn/')
        with open('./ths_stock.html', 'w') as f:
            f.write(response.read())

def main():
    '''
    执行
    '''
    analysis = THSStockFristpage()
    for info in analysis.analyzed_info_list:
        print info.title
        print info.url
        print info.model
        print info.type
        print '============'
    print analysis

if __name__ == '__main__':
    load_data()
    main()
    
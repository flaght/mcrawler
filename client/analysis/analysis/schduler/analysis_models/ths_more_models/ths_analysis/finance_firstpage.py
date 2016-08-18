# -.- coding:utf-8 -.-
"""
Created on 2015年12月28日

@author: slm
"""
import urllib2
import os
import traceback
from lxml import html
from schduler.analysis_models.ths_more_models.ths_analysis.more_news_base import MoreNewsBase


class THSFinanceFirstPage(MoreNewsBase):
    """
    财经首页（14.财经新闻频道）
    """
    tag = {'rule': '/html/head/title',
           'tag': '财经新闻频道-搜罗最新鲜的国内外财经新闻资讯,股市证券新闻,经济新闻_同花顺财经'}

    def __init__(self, callback=None, **kwargs):
        """
        Constructor
        """
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '财经'
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        """
        解析
        """
#         with open('./ths_finance.html', 'r') as f:
#             self.html_data = f.read()
        try:
            self.html_data = self.gz_decode(self.html_data)
        except:
            traceback.print_exc()
        doc = html.fromstring(self.html_data)
        self.__top_news(doc)
        self.__finance_main_news(doc)
        self.__domestic_economy(doc)

    def __domestic_economy(self, doc):
        """
        国内经济
        """
        model = '国内经济'
        more_news = doc.xpath(r'//ul[@class="m_list p0_10"]')[0]
        news_list = more_news.xpath(r'li//a')
        for new in news_list:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __finance_main_news(self, doc):
        """
        财经要闻
        """
        model = '财经要闻'
        more_news = doc.xpath(r'//div[@class="head_list"]//a')
        for new in more_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __top_news(self, doc):
        """
        滚动新闻下方新闻
        """
        model = '新闻'
        more_news = doc.xpath(r'//div[@class="head_news"]//a')
        for new in more_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)


def load_data():
    """
    加载网页html
    """
    if not os.path.exists('./ths_finance.html'):
        response = urllib2.urlopen('http://news.10jqka.com.cn/')
        with open('./ths_finance.html', 'w') as f:
            f.write(response.read())


def main():
    """
    执行
    """
    analysis = THSFinanceFirstPage()
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

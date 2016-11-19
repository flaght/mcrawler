# -.- coding:utf-8 -.-
"""
Created on 2015年12月28日

@author: slm
"""
import urllib2
import os
import traceback
from lxml import html
from scheduler.analysis_models.ths_more_models.ths_analysis.more_news_base import MoreNewsBase


class THSStockEarly(MoreNewsBase):
    """
    股票-早盘必读（20.早盘视点）
    """
    tag = {'rule': '/html/head/title',
           'tag': '早盘视点_早盘必读_同花顺财经'}

    def __init__(self, callback=None, **kwargs):
        """
        Constructor
        """
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '股票'
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        """
        解析
        """
#         with open('./ths_zaopan.html', 'r') as f:
#             self.html_data = f.read()
        try:
            self.html_data = self.gz_decode(self.html_data)
        except:
            traceback.print_exc()
        doc = html.fromstring(self.html_data)
        self.__get_model_url(doc)
        self.__early_reading(doc)

    def __get_model_url(self, doc):
        """
        获得下一级页面的url
        """
        model_url = doc.xpath\
        (r'//div[@id="hot"]//div[@class="content-title-fl"]//a/@href')[0].encode('utf-8')
        self.url_list.append(model_url)

    def __early_reading(self, doc):
        """
        早盘必读
        """
        model = '早盘必读'
        more_news = doc.xpath(r'//div[@id="block_2125"]//div[@class="clearfix"]')
        for new in more_news:
            title = new.xpath(r'a/img/@title')[0]
            url = new.xpath(r'a/@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)


def load_data():
    """
    加载网页html
    """
    if not os.path.exists('./ths_zaopan.html'):
        response = urllib2.urlopen('http://stock.10jqka.com.cn/zaopan/')
        with open('./ths_zaopan.html', 'w') as f:
            f.write(response.read())


def main():
    """
    执行
    """
    analysis = THSStockEarly()
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

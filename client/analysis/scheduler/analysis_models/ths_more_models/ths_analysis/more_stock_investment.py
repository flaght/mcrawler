# -.- coding:utf-8 -.-
"""
Created on 2015年12月25日

@author: slm
"""
import urllib2
import os
import traceback
from lxml import html
from scheduler.analysis_models.ths_more_models.ths_analysis.more_news_base import MoreNewsBase


class THSStockInvestment(MoreNewsBase):
    """
    股票投资机会（5.投资参考）
    """
    tag = {'rule': '/html/head/title',
           'tag': '投资机会_股票_同花顺财经'}

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
#         with open('./ths_tzjh_list.html', 'r') as f:
#             self.html_data = f.read()
        model = '投资参考'
        try:
            self.html_data = self.gz_decode(self.html_data)
        except:
            traceback.print_exc()
        doc = html.fromstring(self.html_data)
        self.__get_model_url(doc)
        self.more_news(doc, self._type, model)

    def __get_model_url(self, doc):
        """
        名家url（名家论市）
        """
        model_list = doc.xpath(r'//div[@id="hd"]//ul[@class="inner_nav_list"]//li//a')
        for model in model_list:
            model_title = model.xpath(r'text()')[0].encode('utf-8')
            if model_title == '名家':
                model_url = model.xpath(r'@href')[0].encode('utf-8')
                self.url_list.append(model_url)
                return


def load_data():
    """
    加载网页html
    """
    if not os.path.exists('./ths_tzjh_list.html'):
        response = urllib2.urlopen('http://stock.10jqka.com.cn/tzjh_list/')
        with open('./ths_tzjh_list.html', 'w') as f:
            f.write(response.read())


def main():
    """
    执行
    """
    analysis = THSStockInvestment()
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

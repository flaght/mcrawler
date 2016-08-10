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


class THSStockCompany(MoreNewsBase):
    """
    公司-公司新闻（10.上市公司）(利用源代码解析)
    """
    tag = {'rule': '/html/head/title',
           'tag': '上市公司_上市公司公告_上市公司信息披露-股票频道-同花顺财经'}

    def __init__(self, callback=None, **kwargs):
        """
        Constructor
        """
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '公司'
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        """
        解析
        """
#         with open('./ths_company.html', 'r') as f:
#             self.html_data = f.read()
        try:
            self.html_data = self.gz_decode(self.html_data)
        except:
            traceback.print_exc()
        doc = html.fromstring(self.html_data)
        self.__get_model_url(doc)
        self.__company_news(doc)

    def __get_model_url(self, doc):
        """
        获得下一级页面的url
        """
        model_url_list = doc.xpath(r'//div[@class="channel-nav channel-nav-gegu"]//a[@target]')
        for model in model_url_list:
            model_title = model.xpath(r'text()')[0].encode('utf-8')
            if model_title == '公司新闻' or model_title == '公司研究' or model_title == '公司解读':
                model_url = model.xpath(r'@href')[0].encode('utf-8')
                self.url_list.append(model_url)

    def __company_news(self, doc):
        """
        公司新闻
        """
        model = '上市公司'
        more_news = \
        doc.xpath(r'//div[@class="left part-l"]//div[@data-taid="ggpd_ggjj"]//ul//li//a')
        print len(more_news)
        for new in more_news:
            title = new.xpath(r'@title')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)


def load_data():
    """
    加载网页html
    """
    if not os.path.exists('./ths_company.html'):
        response = urllib2.urlopen('http://stock.10jqka.com.cn/company.shtml')
        with open('./ths_company.html', 'w') as f:
            f.write(response.read())


def main():
    """
    执行
    """
    analysis = THSStockCompany()
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

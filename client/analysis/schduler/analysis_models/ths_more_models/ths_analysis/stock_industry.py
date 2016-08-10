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


class THSStockIndustry(MoreNewsBase):
    """
    股票-行业（9.行业研究）
    """
    tag = {'rule': '/html/head/title',
           'tag': '行业研究_股票_同花顺财经'}

    def __init__(self, callback=None, **kwargs):
        """
        Constructor
        """
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '股票行业'
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        """
        解析
        """
#         with open('./ths_bkfy_list.html', 'r') as f:
#             self.html_data = f.read()
        model = '行业研究'
        try:
            self.html_data = self.gz_decode(self.html_data)
        except:
            traceback.print_exc()
        doc = html.fromstring(self.html_data)
        self.get_page_url(doc)
        self.more_news(doc, self._type, model)


def load_data():
    """
    加载网页html
    """
    if not os.path.exists('./ths_bkfy_list.html'):
        response = urllib2.urlopen('http://stock.10jqka.com.cn/bkfy_list/')
        with open('./ths_bkfy_list.html', 'w') as f:
            f.write(response.read())


def main():
    """
    执行
    """
    analysis = THSStockIndustry()
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

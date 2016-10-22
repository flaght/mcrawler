# -.- coding:utf-8 -.-
"""
Created on 2015年12月25日

@author: slm
"""
import urllib2
import os
import traceback
from lxml import html
from schduler.analysis_models.ths_more_models.ths_analysis.more_news_base import MoreNewsBase


class THSStockRolling(MoreNewsBase):
    """
    股票-股票滚动（21.股票滚动）
    """
    tag = {'rule': '/html/head/title',
           'tag': '股票滚动_股票_同花顺财经'}

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
#         with open('./ths_gpgd_list.html', 'r') as f:
#             self.html_data = f.read()
        model = '股票滚动'
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
    if not os.path.exists('./ths_gpgd_list.html'):
        response = urllib2.urlopen('http://stock.10jqka.com.cn/gpgd_list/')
        with open('./ths_gpgd_list.html', 'w') as f:
            f.write(response.read())


def main():
    """
    执行
    """
    analysis = THSStockRolling()
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

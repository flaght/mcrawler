# -*- coding:utf-8 -*-
"""
Create on 2015年12月02日

@author: slm
"""
import urllib2
import os
from lxml import html
from scheduler.analysis_models.cn_models.more_news import CNMoreNews


class CNinternet(CNMoreNews):
    """
    财经金融模块
    """
    tag = {'rule': '/html/head/title/text()',
           'tag': '财经-互联网金融-21CN财经频道-21CN.COM'}

    def __init__(self, callback=None, **kwargs):
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '财经金融'
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        """
        解析
        """
#         with open('./21cn_internet.html', 'r') as f:
#             self.html_data = f.read()
        doc = html.fromstring(self.html_data)
        self.main_news_have_picture(doc)
        self.main_news_no_picture(doc)
        self.get_url_list(doc)


def main():
    """
    执行
    """
    analysis = CNinternet()
    print analysis
    for analyzed_info in analysis.analyzed_info_list:
        print analyzed_info.title
        print analyzed_info.type
        print analyzed_info.model
        print analyzed_info.vocation
        print analyzed_info.url
        print '================='


def load_data():
    """
    加载html
    """
    if not os.path.exists('./21cn_internet.html'):
        response = urllib2.urlopen('http://finance.21cn.com/webfocus/internet/')
        with open('./21cn_internet.html', 'w') as f:
            f.write(response.read())

if __name__ == '__main__':
    load_data()
    main()

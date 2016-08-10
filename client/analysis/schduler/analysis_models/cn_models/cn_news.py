# -*- coding:utf-8 -*-
"""
Create on 2015年12月01日

@author: slm
"""
import urllib2
import os
from lxml import html
from schduler.analysis_models.cn_models.cn_analysis_base import CNAnalysisBase
from schduler.analysis_models.analysis_base import AnalysisBase


class CNNews(CNAnalysisBase):
    """
    新闻频道
    """
    tag = {'rule': '/html/head/title/text()',
           'tag': '新闻频道-21CN'}

    def __init__(self, callback=None, **kwargs):
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '新闻'
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def analyzed(self):
        """
        解析完成
        """
        self.make_storage_cmd()
        AnalysisBase.analyzed(self)

    def __analysis(self):
        """
        解析
        """
        #         with open('./21cn_news.html', 'r') as f:
        #             self.html_data = f.read()
        doc = html.fromstring(self.html_data)
        self.__scroll_view(doc)
        self.__domestic_news(doc)

    def __domestic_news(self, doc):
        """
        国内版块
        """
        info_list = doc.xpath(r'//div[@class="mod"]')
        for info in info_list:
            name_list = info.xpath(r'div[@class="hd"]/h3/a/text()')
            if len(name_list) == 0:
                continue
            name = name_list[0].encode('utf-8')
            if name == '国内':
                # 将国内0和要闻3新闻模块url返给服务器
                name_url = info.xpath(r'div[@class="hd"]//a/@href')
                self.url_list.append(name_url[0])
                self.url_list.append(name_url[3])
                self.__left_news(info)
                self.__right_news(info)

    def __right_news(self, doc):
        """
        右面图片新闻
        """
        model = '国内'
        picture_list = doc.xpath(r'div[@class="bd clearfix"]//div[@class="fr"]')
        for picture in picture_list:
            title = picture.xpath(r'div[@class="bigpic"]/a/em/text()')[0].encode('utf-8')
            url = picture.xpath(r'div[@class="bigpic"]/a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)

    def __left_news(self, doc):
        """
        左面新闻
        """
        model = '国内'
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

    def __scroll_view(self, doc):
        """
        头部滚动新闻
        """
        scroll_news_list = doc.xpath(r'//div[@id="focus-image"]//li')
        model = '滚动新闻'
        for news in scroll_news_list:
            title = news.xpath(r'a/span/text()')[0].encode('utf-8')
            url = news.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)


def main():
    """
    执行
    """
    analysis = CNNews()
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
    if not os.path.exists('./21cn_news.html'):
        response = urllib2.urlopen('http://news.21cn.com/')
        with open('./21cn_news.html', 'w') as f:
            f.write(response.read())


if __name__ == '__main__':
    load_data()
    main()

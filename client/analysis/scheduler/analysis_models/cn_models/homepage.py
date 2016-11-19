# -*- coding:utf-8 -*-
"""
Create on 2015年11月30日

@author: SLM
"""
import urllib2
import os
from lxml import html
from scheduler.analysis_models.cn_models.cn_analysis_base import CNAnalysisBase
from scheduler.analysis_models.analysis_base import AnalysisBase


class CNHomePage(CNAnalysisBase):
    """
    21cn首页
    """
    tag = {'rule': '/html/head/title/text()',
           'tag': '21CN'}

    def __init__(self, callback=None, **kwargs):
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '资讯'
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
        #         with open('./21cn_firstpage.html', 'r') as f:
        #             self.html_data = f.read()
        doc = html.fromstring(self.html_data)
        self.__news(doc)
        self.__finance(doc)

    def __news(self, data):
        """
        新闻
        """
        info_list = data.xpath(r'//div[@class="channel_cnt"]//div[@class="mod"]')
        # 第一个元素为新闻模块
        doc = info_list[0]
        # 把新闻模块url上传到服务器
        name_url = doc.xpath(r'div[@class="hd clearfix"]/h3/a/@href')[0].encode('utf-8')
        self.url_list.append(name_url)
        self.__picture_news_left(doc)
        self.__new_left(doc)
        self.__picture_news_right(doc)
        self.__news_right(doc)

    def __finance(self, data):
        """
        财经
        """
        info_list = data.xpath(r'//div[@class="channel_cnt"]//div[@class="mod"]')
        for i in xrange(len(info_list)):
            # 第一个为新闻模块
            if i == 0:
                continue
            name = info_list[i].xpath(r'div[@class="hd"]/h3/a/text()')[0].encode('utf-8')
            if name == '财经':
                # 把财经模块url上传到服务器
                name_url = info_list[i].xpath(r'div[@class="hd"]/h3/a/@href')[0].encode('utf-8')
                self.url_list.append(name_url)
                self.__picture_news_left(info_list[i])
                self.__new_left(info_list[i])
                self.__picture_news_right(info_list[i])
                self.__news_right(info_list[i])

    def __picture_news_left(self, doc):
        """
        图片新闻（左边新闻）
        """
        title = doc.xpath(r'div[@class="bd clearfix"]//div[@class="fl"]//h3//a/text()')[0].encode('utf-8')
        url = doc.xpath(r'div[@class="bd clearfix"]//div[@class="fl"]//h3//a/@href')[0].encode('utf-8')
        model = '新闻'
        self.set_analyzed_info(title, self._type, model, None, url)

    def __new_left(self, doc):
        """
        左边除图片新闻的新闻列表
        """
        new_list = doc.xpath(r'div[@class="bd clearfix"]//div[@class="fl"]//li')
        model = '新闻'
        for news in new_list:
            title = news.xpath(r'a/text()')[0].encode('utf-8')
            url = news.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)

    def __picture_news_right(self, doc):
        """
        图片新闻（右边两个）
        """
        title_list = doc.xpath(r'div[@class="bd clearfix"]//div[@class="fr"]//em/text()')
        url_list = doc.xpath(r'div[@class="bd clearfix"]//div[@class="fr"]//li//a/@href')
        model = '新闻'
        for i in xrange(len(title_list)):
            title = title_list[i].encode('utf-8')
            url = url_list[i].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)

    def __news_right(self, doc):
        """
        右边除图片新闻的新闻列表
        """
        new_list = doc.xpath(r'div[@class="bd clearfix"]//div[@class="fr"]//ul[@class="art ico-dot"]//li')
        model = '新闻'
        for news in new_list:
            title = news.xpath(r'a/text()')[0].encode('utf-8')
            url = news.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, url)


def main():
    analysis = CNHomePage()
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
    if not os.path.exists('./21cn_firstpage.html'):
        response = urllib2.urlopen('http://www.21cn.com/')
        with open('./21cn_firstpage.html', 'w') as f:
            f.write(response.read())


if __name__ == '__main__':
    load_data()
    main()

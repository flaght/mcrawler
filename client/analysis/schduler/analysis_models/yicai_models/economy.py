# -*- coding:utf-8 -*-
"""
Created on 2015年11月2日

@author: slm
"""
import urllib2
import os
from lxml import html
from schduler.analysis_models.yicai_models.analysis import YCAnalysis
from schduler.analysis_models.yicai_models.yicai_analysis_base import YCAnalysisBase


class YCeconomy(YCAnalysisBase):
    """
    第一财经主页宏观分页解析(cid=182&subcid=194)
    """
    tag = {'rule': '//*[@id="menulist"]/li[contains(@class, "hover")]/a',
           'tag': '宏观'}

    def __init__(self, callback=None, **kwargs):
        """
        tag：唯一标识
        storage_type：存储类型
        storage_cmd_list：存储指令
        """
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        # 解析数据列表
        self.analyzed_info_list = []
        # 解析
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        """
        解析(标题，url，类别，行业，模块)
        """
        #         with open('./yicai_economy.html', 'r') as f:
        #             self.html_data = f.read()
        doc = html.fromstring(self.html_data)
        self.__header_news(doc)
        self.__middle_news_all(doc)
        self.__yc_tv(doc)
        self.__get_url_list(doc)

    def __get_url_list(self, doc):
        """
        获得要返回给服务器的url(下一页url和模块url)
        """
        # 把后面url返回给服务器
        analysis = YCAnalysis('1', '1', doc, 182, 194)
        analysis.middle_first_next_url()
        for url_info in analysis.next_url_list:
            self.url_list.append(url_info)

    def __yc_tv(self, doc):
        """
        第一财经电视
        """
        model = '第一财经电视'
        new_type = '宏观'
        news = doc.xpath(r'//div[@class="box company"]//ul//li')
        for header_new in news:
            title = header_new.xpath(r'a/text()')[0].encode('utf-8')
            url = header_new.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, new_type, model, None, url)

    def __header_news(self, doc):
        """
        头部咨询栏
        """
        model = '资讯'
        new_type = '宏观'
        header_news = doc.xpath(r'//div[@id="content"]//div[@class="banana"]//h1')
        for header_new in header_news:
            title = header_new.xpath(r'a/text()')[0].encode('utf-8')
            url = header_new.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, new_type, model, None, url)

    def __middle_news_all(self, doc):
        """
        全部（中间分栏第一个）
        """
        new_type = '宏观'
        header_news = doc.xpath(r'//div[@id="con_one_1"]/dl//h1')
        for header_new in header_news:
            title = header_new.xpath(r'a/text()')[0].encode('utf-8')
            url = header_new.xpath(r'a/@href')[0].encode('utf-8')

            #             该语句可提到for循环外
            model = doc.xpath(r'//div[@id="Tab1"]//li/text()')[0].encode('utf-8')
            self.set_analyzed_info(title, new_type, model, None, url)


def main():
    """
    测试
    """
    analysis = YCeconomy()
    print len(analysis.analyzed_info_list)
    for info in analysis.analyzed_info_list:
        print info.title
        print info.url
        print info.model
        print info.type
        print '============'
    print analysis


def load_data():
    """
    加载网页html
    """
    if not os.path.exists('./yicai_economy.html'):
        response = urllib2.urlopen('http://www.yicai.com/economy/')
        with open('./yicai_economy.html', 'w') as f:
            f.write(response.read())


if __name__ == '__main__':
    load_data()
    main()

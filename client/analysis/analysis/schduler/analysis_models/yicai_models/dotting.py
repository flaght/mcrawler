# -*- coding:utf-8 -*-
"""
Created on 2015年11月2日

@author: slm
"""
import urllib2
import os
from lxml import html
from schduler.analysis_models.yicai_models.yicai_analysis_base import YCAnalysisBase


class YCdotting(YCAnalysisBase):
    """
    第一财经主页更多点睛分页解析
    """
    tag = {'rule': '//*[@id="content"]/div[@class="eyeball"]/h3',
           'tag': '一财点睛'}

    def __init__(self, callback=None, **kwargs):
        """
        tag：唯一标识
        storage_type：存储类型
        storage_cmd_list：存储指令
        """
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self.analyzed_info_list = []
        # 解析
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        """
        解析
        """
        #         with open('./yicai_cbndianjing.html', 'r') as f:
        #             self.html_data = f.read()
        doc = html.fromstring(self.html_data)
        self.__update(doc)

    def __update(self, doc):
        """
        最近更新
        """
        new_type = '一财点睛'
        model = '最近更新'
        news = doc.xpath(r'//div[@id="content"]//div[@class="update"]//ul//li//h4')
        for one_new in news:
            title = one_new.xpath(r'a/text()')[0].encode('utf-8')
            url = one_new.xpath(r'a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, new_type, model, None, url)


def main():
    """
    测试
    """
    analysis = YCdotting()
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
    加载要解析的html
    """
    if not os.path.exists('./yicai_cbndianjing.html'):
        response = urllib2.urlopen('http://www.yicai.com/cbndianjing/index.html')
        with open('./yicai_cbndianjing.html', 'w') as f:
            f.write(response.read())


if __name__ == '__main__':
    load_data()
    main()

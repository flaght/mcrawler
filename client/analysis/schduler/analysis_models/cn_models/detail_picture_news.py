# -*- coding:utf-8 -*-
"""
Create on 2015年12月03日

@author: slm
"""
import urllib2
import os
import re
from lxml import html
from schduler.analysis_models.cn_models.cn_analysis_base import CNAnalysisBase
from schduler.analysis_models.analysis_base import AnalysisBase


class CNNewsDetail(CNAnalysisBase):
    """
    首页详情页(新闻、财经模块)
    """
    tag = {'rule': '//a[@id="J_set_album_mode"]',
           'tag': '图集'}

    def __init__(self, callback=None, **kwargs):
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '新闻'
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def analyzed(self):
        self.make_storage_cmd_picture()
        AnalysisBase.analyzed(self)

    def __analysis(self):
        """
        解析
        """
#         with open('./21cn_cn_detail.html', 'r') as f:
#             self.html_data = f.read()
        doc = html.fromstring(self.html_data)        
        self.__get_current_url()
        self.__detail(doc)

    def __get_current_url(self):
        """
        获得当前url
        """
        self.current_id = re.findall("contentId: (.*?),", self.html_data)[0].encode('utf-8')

    def __detail(self, doc):
        """
        详情
        date:日期
        content:内容
        introduction:导读
        comment_num:评论数量
        like_num:点赞数
        unlike_num:踩数量
        comment_detail:评论详情
        """
        content = None
        first_news = doc.xpath(r"//div[@id='img_sum1']//p/text()")
        for info in first_news:
            if len(info) == 0:
                continue
            content = info.encode('utf-8')
        date = doc.xpath(r'//div[@class="top"]//div[@class="headline"]//span/text()')[0].encode('utf-8')
        introduction = doc.xpath(r'/html/head/meta[@name="description"]/@content')[0].encode('utf-8')
        self.set_analyzed_info_picture(self.current_id, date, content, introduction, None, None, None)


def main():
    """
    执行
    """
    analysis = CNNewsDetail()
    print analysis
    for analyzed_info in analysis.analyzed_info_list:
        print analyzed_info.current_id
        print analyzed_info.date
        print analyzed_info.content
        print analyzed_info.introduction
        print '================='


def load_data():
    """
    加载html
    """
    if not os.path.exists('./21cn_cn_detail.html'):
        response = urllib2.urlopen(r'http://news.21cn.com/photo/a/2015/1203/11/30339421.shtml')
        with open('./21cn_cn_detail.html', 'w') as f:
            f.write(response.read())

if __name__ == '__main__':
    load_data()
    main()

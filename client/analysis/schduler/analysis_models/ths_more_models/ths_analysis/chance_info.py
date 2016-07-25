# -.- coding:utf-8 -.-
'''
Created on 2015年12月25日

@author: slm
'''
import urllib2
import os
from lxml import html
from schduler.analysis_models.ths_more_models.ths_analysis.more_news_base import MoreNewsBase

class THSChanceInfo(MoreNewsBase):
    '''
    机会情报（6.机会情报）
    '''
    tag = {'rule': '/html/head/title',
           'tag': '第一情报,股市机会情报_同花顺财经'}

    def __init__(self, callback=None, **kwargs):
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '机会情报'
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        '''
        解析
        '''
#         with open('./ths_qingbao.html', 'r') as f:
#             self.html_data = f.read()
        try:
            self.html_data = self.gzdecode(self.html_data)
        except:
            pass
        doc = html.fromstring(self.html_data)
        self.__more_news(doc)

    def __more_news(self, doc):
        '''
        更多新闻
        '''
        model = '新闻'
        more_news = doc.xpath(r'//div[@id="Newslist"]//h2//a')
        print len(more_news)
        for new in more_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

def load_data():
    '''
    加载网页html
    '''
    if not os.path.exists('./ths_qingbao.html'):
        response = urllib2.urlopen('http://yuanchuang.10jqka.com.cn/qingbao/')
        with open('./ths_qingbao.html', 'w') as f:
            f.write(response.read())

def main():
    '''
    执行
    '''
    analysis = THSChanceInfo()
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
    
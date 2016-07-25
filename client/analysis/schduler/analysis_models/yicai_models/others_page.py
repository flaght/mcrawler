# -*- coding:utf-8 -*-
'''
Created on 2015年11月4日

@author: slm
'''
import urllib2
import os
from lxml import html
from schduler.analysis_models.yicai_models.yicai_analysis_base import YCAnalysisBase

class NextPage(YCAnalysisBase):
    '''
    解析其他模块url第一页
    '''
    tag = {'rule':'//dl/dd/h1/a',
           'tag':YCAnalysisBase.default_analysis_model}

    def __init__(self, callback=None, **kwargs):
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        '''
        解析
        '''
#         with open('./others_first_page.html', 'r') as f:
#             self.html_data = f.read()
        doc = html.fromstring(self.html_data)
        header_news = doc.xpath(r'//dl//dd//h1')
        for header_new in header_news:
            title = header_new.xpath(r'a/text()')[0].encode()
            url = header_new.xpath(r'a/@href')[0].encode()
            self.set_analyzed_info(title, None, None, None, url)

def load_data():
    '''
    加载网页html
    '''
    if not os.path.exists('./others_first_pages2.html'):
        #其他模块可翻页
        model_type = '5'
        type_name = '%E4%B8%80%E8%B4%A2%E7%9C%8B%E4%B8%A4%E4%BC%9A'
        page_num = '1'
        #其他模块不可翻页
#         model_type = '2'
#         type_name = '%E7%AE%80%E7%AC%94%E8%AF%9D%E6%94%BF'
#         page_num = '1'
#         #第一个模块其他页
#         model_type = '1'
#         type_name = ''
#         page_num = '2'
        url_part1 = 'http://www.yicai.com/ajax.php?op=getnewslist'
        url_part2 = '&type=%s&typename=%s&page=%s' %(model_type, type_name, page_num)
        url = '%s%s' %(url_part1, url_part2)
        response = urllib2.urlopen(url)
        with open('./others_first_page.html', 'w') as f:
            f.write(response.read())

def main():
    '''
    测试
    '''
    analysis = NextPage()
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
    
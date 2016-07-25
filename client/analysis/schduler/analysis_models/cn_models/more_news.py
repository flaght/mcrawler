# -*- coding:utf-8 -*-
'''
Create on 2015年12月01日

@author: slm
'''
from schduler.analysis_models.cn_models.cn_analysis_base import CNAnalysisBase
from schduler.analysis_models.analysis_base import AnalysisBase

class CNMoreNews(CNAnalysisBase):
    '''
    更多新闻
    '''
    def analyzed(self):
        '''
        解析完成
        '''
        self.make_storage_cmd()
        AnalysisBase.analyzed(self)

    def get_url_list(self, doc):
        '''
        获得要返回给服务的url（页数url）
        '''
        pass

    def main_news_no_picture(self, doc):
        '''
        要闻(无图)
        '''
        model = '新闻'
        _type = '新闻'
        news_list = doc.xpath(r'//div[@class="bd"]//div[@class="pic-tit bigPic"]')
        print len(news_list)
        for info in news_list:
            title = info.xpath(r'h3/a/text()')[0].encode('utf-8')
            url = info.xpath(r'h3/a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, _type, model, None, url)

    def main_news_have_picture(self, doc):
        '''
        要闻（有图）
        '''
        model = '新闻'
        _type = '新闻'
        news_list = doc.xpath(r'//div[@class="bd"]//div[@class="pic-tit bigPic "]')
        print len(news_list)
        for info in news_list:
            title = info.xpath(r'h3/a/text()')[0].encode('utf-8')
            url = info.xpath(r'h3/a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, _type, model, None, url)

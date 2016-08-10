# -.- coding:utf-8 -.-
"""
Created on 2015年12月25日

@author: slm
"""
import StringIO
import gzip
from schduler.analysis_models.ths_more_models.ths_analysis_base import THSAnalysisBase


class MoreNewsBase(THSAnalysisBase):
    """
    更多新闻基类
    """

    @staticmethod
    def get_page_url(doc):
        """
        得到新闻总页数，拼接url
        """
        pass

    def more_news(self, doc, _type, model):
        """
        财经要闻新闻
        """
        more_news = doc.xpath(r'//div[@class="list_item"]//h2/a')
        for new in more_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, _type, model, None, url)

    @staticmethod
    def gz_decode(data):
        """
        解压缩
        """
        compressed_stream = StringIO.StringIO(data)
        gziper = gzip.GzipFile(fileobj=compressed_stream)
        gziper_html_data = gziper.read()  # 读取解压缩后数据
        return gziper_html_data

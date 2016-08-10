# -.- coding:utf-8 -.-
"""
Created on 2015年12月22日

@author: slm
"""
import urllib2
import os
import traceback
from lxml import html
from schduler.analysis_models.ths_more_models.ths_analysis.more_news_base import MoreNewsBase


class THSHomePage(MoreNewsBase):
    """
    首页（1.首页）
    """
    tag = {'rule': '/html/head/title',
           'tag': '同花顺财经__让投资变得更简单'}

    def __init__(self, callback=None, **kwargs):
        """
        Constructor
        """
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '财经'
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        """
        解析
        """
        #         with open('./ths_homepage.html', 'r') as f:
        #             self.html_data = f.read()
        try:
            self.html_data = self.gz_decode(self.html_data)
        except:
            traceback.print_exc()
        doc = html.fromstring(self.html_data)
        self.__get_model_url(doc)
        self.__today_top(doc)
        self.__financial_focus_news_top(doc)
        self.__nvestment_news(doc)
        self.__chance_news(doc)
        self.__real_time(doc)
        self.__market_analysis(doc)
        self.__listed_company(doc)
        self.__financial_focus_news_bellow(doc)
        self.__hot_top(doc)

    def __get_model_url(self, doc):
        """
        获得模块下级页面url（要闻 股票  独家报道 机会情报 投资参考 大盘分析 下方财经要闻）
        """
        model_url_list = doc.xpath(r'//div[@id="block_3362"]//em//a')
        for i in xrange(len(model_url_list)):
            model_title = model_url_list[i].xpath(r'text()')[0].encode('utf-8')
            if model_title == '要闻' or model_title == '股票':
                model_url = model_url_list[i].xpath(r'@href')[0]
                self.url_list.append(model_url)
        # 大盘分析
        model_url_grail = doc.xpath(r'//div[@id="block_3350"]/h2/a/@href')[0]
        self.url_list.append(model_url_grail)
        # 机会情报
        model_url_chance = doc.xpath(r'//div[@id="block_3349"]/h2/a/@href')[0]
        self.url_list.append(model_url_chance)
        # 投资参考
        model_url_investment = doc.xpath(r'//div[@id="block_3347"]/h2/a/@href')[0]
        self.url_list.append(model_url_investment)
        # 下方财经要闻
        model_url_finance = doc.xpath(r'//div[@id="block_3354"]/h2/a/@href')[0]
        self.url_list.append(model_url_finance)
        model_url_original = doc.xpath(r'//div[@id="block_3351"]//span[@class="links"]//a')
        for i in xrange(len(model_url_original)):
            model_title = model_url_original[i].xpath(r'text()')[0].encode('utf-8')
            if model_title == '独家报道' or model_title == '机会情报':
                model_url = model_url_original[i].xpath(r'@href')[0]
                self.url_list.append(model_url)

    def __hot_top(self, doc):
        """
        24小时热榜
        """
        model = '24小时热榜'
        market_analysis_news = doc.xpath(r'//div[@class="box-r hot-comment ta-parent-box"]//ul//li//a')
        for new in market_analysis_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __financial_focus_news_bellow(self, doc):
        """
        财经要闻（下方）
        """
        model = '财经要闻'
        market_analysis_news = doc.xpath(r'//div[@class="box ta-parent-box"]//ul//li//a[@id]')
        for new in market_analysis_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __listed_company(self, doc):
        """
        上市公司
        """
        model = '上市公司'
        market_analysis_news = doc.xpath(r'//div[@class="sub-box control module fl"]//ul//li//a[@id]')
        for new in market_analysis_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __market_analysis(self, doc):
        """
        大盘分析
        """
        model = '大盘分析'
        market_analysis_news = doc.xpath(r'//div[@class="sub-box module fl ta-parent-box"]//ul//li//a[@id]')
        for new in market_analysis_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __real_time(self, doc):
        """
        实时解盘
        """
        model = '实时解盘'
        real_time_news = doc.xpath(r'//div[@class="now-read box-r ta-parent-box"]//ul//a')
        for new in real_time_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __chance_news(self, doc):
        """
        机会情报
        """
        model = '机会情报'
        nvestment_news = doc.xpath(r'//div[@class="sub-box fl"]//ul[@class="content jhqb"]//li/a')
        for new in nvestment_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __nvestment_news(self, doc):
        """
        投资参考
        """
        model = '投资参考'
        nvestment_news = doc.xpath(r'//div[@class="sub-box fl"]//ul[@class="content"]//li//a')
        for new in nvestment_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __financial_focus_news_top(self, doc):
        """
        财经要闻
        """
        model = '财经要闻'
        focus_news = doc.xpath(r'//div[@class="item cjyw ta-parent-box"]//ul//li//a')
        for new in focus_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __today_top(self, doc):
        """
        今日头条
        """
        model = '今日头条'
        top_news = doc.xpath(r'//div[@class="jrtt ta-parent-box"]//a')
        for new in top_news:
            title = new.xpath(r'text()')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)


def load_data():
    """
    加载网页html
    """
    if not os.path.exists('./ths_homepage.html'):
        response = urllib2.urlopen('http://www.10jqka.com.cn/')
        with open('./ths_homepage.html', 'w') as f:
            f.write(response.read())


def main():
    """
    执行
    """
    analysis = THSHomePage()
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

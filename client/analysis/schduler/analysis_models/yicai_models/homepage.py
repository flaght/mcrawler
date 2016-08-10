# -.- coding:utf-8 -.-
"""
Created on 2015年10月31日

@author: chenyitao
"""
import os
import urllib2
from lxml import html
from schduler.analysis_models.yicai_models.yicai_analysis_base import YCAnalysisBase

class YCHomePage(YCAnalysisBase):
    """
    class docs
    """
    tag = {'rule':'//*[@id="menulist"]/li[contains(@class, "hover")]/a',
           'tag':'首页'}
    host = 'yicai.com'

    def __init__(self, callback=None, **kwargs):
        """
        Constructor
        """
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self.analyzed_info_list = []
        self.__analysis()
        # 解析结束回传数据
        self.analyzed()

    def __analysis(self):
        """
        解析
        """
#         with open('./yicai_homepage.html', 'r') as f:
#             self.html_data = f.read()
        doc = html.fromstring(self.html_data)
        self._type = doc.xpath('//*[@id="menulist"] \
        /li[contains(@class, "hover")]/a')[0].text.encode('utf-8')
        self.tag = self._type
        self.__scroll_news(doc)
        self.__headline(doc)
        self.__combine(doc)
        self.__audiovisual(doc)
        self.__important_news(doc)
        self.__catch_url(doc)
        
    def __scroll_news(self, doc):
        """
        滚动新闻
        """
        model = '滚动新闻'
        scroll_news = doc.xpath('//*[@id="focusslider"]/div[@class="lislide"]')
        for scroll_new in scroll_news:
            title = scroll_new.xpath('h2/span/a[@title]')[0].text.encode('utf-8')
            href = scroll_new.xpath('h2/span/a[@href]/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, href)

    def __headline(self, doc):
        """
        今日头条
        """
        headline = doc.xpath('//*[@id="content"]/div[@class="lefbar fl"] \
        /div[@class="headline"]')[0]
        model = headline.xpath('h2')[0].text
        h3 = headline.xpath('h3')
        for h in h3:
            a = h.xpath('a')
            for _a in a:
                self.set_analyzed_info(_a.text,
                                       self._type,
                                       model,
                                       None,
                                       str(_a.xpath('@href')[0].encode('utf-8')))
        li = headline.xpath('ul/li')
        for _li in li:
            a = _li.xpath('a')
            for _a in a:
                self.set_analyzed_info(_a.text,
                                       self._type,
                                       model,
                                       None,
                                       str(_a.xpath('@href')[0].encode('utf-8')))

    def __combine(self, doc):
        """
        combine
        """
        model = 'combine'
        combine_news = doc.xpath('//*[@id="content"]/div[@class="rigbar fr"] \
        /div[@class="combine"]/ul/li')
        for combine_new in combine_news:
            title = combine_new.xpath('a/text()')[0].encode('utf-8')
            href = combine_new.xpath('a/@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, href)
        
    def __audiovisual(self, doc):
        """
        今日视听
        """
        audiovisual = doc.xpath('//*[@id="content"]/div[@class="rigbar fr"] \
        /div[@class="seeing"]')[0]
        model = audiovisual.xpath('h2/text()')[0].encode('utf-8')
        videos = audiovisual.xpath('ul[@class="tt"]/li/a')
        for video in videos:
            title = video.xpath('@title')[0].encode('utf-8')
            href = video.xpath('@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, href)

    def __important_news(self, doc):
        """
        要闻
        """
        important_new = doc.xpath('//*[@id="con_two_1"]')[0]
        model = important_new.xpath('@param3')[0].encode('utf-8')
        important_news = important_new.xpath('dl/dd/h1/a')
        for news in important_news:
            title = news.xpath('@title')[0].encode('utf-8')
            href = news.xpath('@href')[0].encode('utf-8')
            self.set_analyzed_info(title, self._type, model, None, href)

    def __catch_url(self, doc):
        """
        解析所有url并去重、过滤外站url
        """
        target_list = ['宏观', '时政', '金融', '股市', '思想', '一财点睛', '\xe8\x81\x9a\xc2\xa0\xc2\xa0\xe7\x84\xa6']
        a_tag_list = doc.xpath('//*[@id="menulist"]/li/a')
        for a in a_tag_list:
            text = a.xpath('text()')[0].encode('utf-8')
            if text in target_list:
                url = a.xpath('@href')[0].encode('utf-8')
                self.url_list.append(url)
        a2_tag_list = doc.xpath('//*[@id="cbnmore"]/p/a')
        for a in a2_tag_list:
            text = a.xpath('text()')[0].encode('utf-8')
            if text in target_list:
                url = a.xpath('@href')[0].encode('utf-8')
                self.url_list.append(url)
        li_tag_list = doc.xpath('//*[@id="newslist"]/div/div[@class="Menubox"]/ul/li')
        for li in li_tag_list:
            typename = li.xpath('text()')[0].encode('utf-8')
            if typename == '要闻':
                continue
            api = 'http://www.yicai.com/ajax.php?op=getnewslist'
            url = '%s&typename=%s&page=1' % (api, typename)
#             self.url_list.append(url)

def main():
    """
    test
    """
    analyzer = YCHomePage()
    print analyzer
    for analyzed_info in analyzer.analyzed_info_list:
        print analyzed_info.title
        print analyzed_info.type
        print analyzed_info.model
        print analyzed_info.vocation
        print analyzed_info.url

def load_data():
    """
    加载要解析的html
    """
    if not os.path.exists('./yicai_homepage.html'):
        response = urllib2.urlopen('http://www.yicai.com/')
        with open('./yicai_homepage.html', 'w') as f:
            f.write(response.read())

if __name__ == '__main__':
    load_data()
    main()

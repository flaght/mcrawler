# -*- coding:utf-8 -*-
"""
Create on 2015年11月20日

@author: SLM
"""
import urllib2
import os
import re
from lxml import html
from scheduler.analysis_models.weibo_models.weibo_analysis.weibo_analysis_base import WBAnalysisBase
from scheduler.analysis_models.analysis_base import AnalysisBase
from scheduler.analysis_models.weibo_models.login.login import LoginWeibo


class WBFirstPage(WBAnalysisBase):
    """
    微博股票首页 (从源码中利用正则获得html，去反斜杠，保存到本地，再用xpath去解析)
    知解析热门微博
    """
    # 发现股票
    tag = {'rule': '/html/head/title',
           'tag': '发现－股票'}

    def __init__(self, callback=None, **kwargs):
        """
        tag：唯一标识
        storage_type：存储类型
        storage_cmd_list：存储指令
        """
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()
        print self.url_list

    def analyzed(self):
        self.make_storage_cmd_expert()
        AnalysisBase.analyzed(self)

    def __analysis(self):
        """
        解析
        """
        #         with open('./stock_first_page.html', 'r') as f:
        #             self.html_data = f.read()
        #         with open('./stock_first_page.json', 'w') as f:
        #             f.write(self.html_data)
        self.__get_model_url()
        self.__get_part_html()

    def __get_model_url(self):
        """
        获得模块url返回给服务器(热门股票、专家)
        """
        expert_url = 'http://d.weibo.com/230771_-_EXPERTUSER'
        self.url_list.append(expert_url)

    def __get_part_html(self):
        """
        从源码中解析获得每块的html
        """
        view_list = re.findall('FM\.view\((.*?)\)</script>', self.html_data)
        for i in xrange(len(view_list)):
            if i == 0:
                continue
            list_info = view_list[i]
            html_dic = eval(list_info)
            info = html_dic.get('html', 'NotFound')
            if len(info) == 0:
                continue
            # 去掉反斜杠
            html_info = info.replace('\\', '')
            # 以ns的值作为html的名字
            title_domid = html_dic.get('domid', 'NotFound')
            if title_domid == 'Pl_Core_MixedFeed__5':
                self.__hot_weibo(html_info)

    def __hot_weibo(self, stock_html_data):
        """
        热门微博
        """
        #         with open('./stock_html_data.html', 'w') as f:
        #             f.write(stock_html_data)
        doc = html.fromstring(stock_html_data)
        weibo_list = doc.xpath(r'//div[@action-type="feed_list_item"]')
        user_card_xpath = \
            'div[@class="WB_feed_detail clearfix"]//a[@class="W_f14 W_fb S_txt1"]/@usercard'
        url_xpath = 'div[@class="WB_feed_detail clearfix"]//a[@class="W_f14 W_fb S_txt1"]/@href'
        for one_weibo in weibo_list:
            weibo_user_card = one_weibo.xpath(r'%s' % user_card_xpath)[0].encode().strip()
            weibo_id = weibo_user_card.split('=').pop()
            url = one_weibo.xpath(r'%s' % url_xpath)[0].encode()
            self.set_analyzed_info_expert(weibo_id, url)


def main():
    """
    执行
    """
    analysis = WBFirstPage()
    print analysis
    for analyzed_info in analysis.analyzed_info_list:
        print analyzed_info.weibo_id
        print analyzed_info.url


def load_data():
    """
    加载网页html
    """
    if not os.path.exists('./stock_first_page.html'):
        # 有效url,测试用
        # http://passport.weibo.com/wbsso/login?ssosavestate=1481272211&
        # url=http%3A%2F%2Fd.weibo.com%2F230771&ticket=ST-NTc2NzAxODk1Mw
        # ==-1449736211-gz-BCA2ACA48F5EDA80444CA51437447BBE&retcode=0
        response = urllib2.urlopen('http://d.weibo.com/230771')
        with open('./stock_first_page.html', 'w') as f:
            f.write(response.read())


if __name__ == '__main__':
    # 登陆
    LoginWeibo()
    load_data()
    main()

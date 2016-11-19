# -*- coding:utf-8 -*-
"""
Create on 2015年11月30日

@author: SLM
"""
import urllib2
import os
import re
from lxml import html
from scheduler.analysis_models.weibo_models.weibo_analysis.weibo_analysis_base import WBAnalysisBase
from scheduler.analysis_models.weibo_models.login.login import LoginWeibo


class WBigV(WBAnalysisBase):
    """
    解析大V微博
    """
    tag = {'rule': '/html/head/title',
           'tag': '_微博'}

    def __init__(self, callback=None, **kwargs):
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self.weibo_id = ''
        self.analyzed_info_list = []
        self.__analysis()
        self.make_storage_cmd_weibos()
        self.analyzed()

    def __analysis(self):
        """
        解析
        """
        #         with open('./stock_big_v.html', 'r') as f:
        #             self.html_data = f.read()
        #         with open('./stock_big_v.json', 'w') as f:
        #             f.write(self.html_data)
        self.__get_weibo_id()
        self.__get_part_html()

    def __get_weibo_id(self):
        """
        获得微博id
        """
        self.weibo_id = re.findall("\$CONFIG\[\'oid\'\]=\'(.*?)\';", self.html_data)[0]

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
            title_ns = html_dic.get('ns', 'NotFound')
            #             with open('./json/%s.html' %title_ns, 'w') as f:
            #                 f.write(html_info)
            if title_ns == 'pl.content.homeFeed.index':
                #                 with open('./%s.html' %title_ns, 'w') as f:
                #                     f.write(html_info)
                self.__first_page_weibo(html_info)
                # 博主简介
            #             title_domid = html_dic.get('domid', 'NotFound')
            #             if title_domid == 'Pl_Core_UserInfo__5':
            #                 self.__weibo_microblogger_info(html_info)

    @staticmethod
    def __weibo_microblogger_info(stock_html_data):
        """
        微博博主信息（个人简介）
        """
        doc = html.fromstring(stock_html_data)
        job_list = doc.xpath(r'//div[@class="PCD_person_info"]//p[@class="info"]//span/text()')
        if len(job_list) > 0:
            job = job_list[0].encode('ISO-8859-1')
            print job
        info_list = doc.xpath(r'//ul[@class="ul_detail"]//span[@class="item_text W_fl"]/text()')
        for i in xrange(len(info_list)):
            detail = info_list[i].encode('ISO-8859-1').strip()
            print detail
            print '======='

    def __first_page_weibo(self, stock_html_data):
        """
        只需解析首页微博
        """
        doc = html.fromstring(stock_html_data)
        weibo_list_xpath = \
            '//div[@class="WB_feed WB_feed_profile"]//div[(contains(@action-type,"feed_list_item"))]'
        weibo_list = doc.xpath(r'%s' % weibo_list_xpath)
        self.__get__info(weibo_list)

    def __get__info(self, weibo_list):
        """
        获得微博信息
        """
        if len(weibo_list) == 0:
            return
        for info in weibo_list:
            weibo = self.__get_weibo_detail(info)
            # 是否有转发
            share_weibo_id = self.__share_weibo_id(info)
            # 评论、转发、点赞
            bottom_list = info.xpath(r'div[@class="WB_feed_handle"]//span[@class="pos"]')
            share_num = self.__bottom_list(bottom_list[1], 1)
            comment_num = self.__bottom_list(bottom_list[2], 2)
            likes_num = self.__bottom_list(bottom_list[3], 3)
            self.set_analyzed_info_weibos(self.weibo_id, weibo, share_weibo_id,
                                          share_num, comment_num, likes_num)

    @staticmethod
    def __share_weibo_id(info):
        """
        博主转发微博的id
        """
        share_weibos_xpath = \
            'div[@class="WB_feed_detail clearfix"]//a[@class="W_fb S_txt1"]/@usercard'
        share_weibos = info.xpath(r'%s' % share_weibos_xpath)
        if len(share_weibos) == 0:
            pass
        else:
            share_weibo_id_list = share_weibos[0].encode('ISO-8859-1')
            share_weibo_id = share_weibo_id_list.split('=').pop()
            return share_weibo_id

    @staticmethod
    def __get_weibo_detail(info):
        """
        波账户所发微博内容
        """
        detail_list_xpath = \
            'div[@class="WB_feed_detail clearfix"]//div[@class="WB_text W_f14"]/text()'
        detail_list = info.xpath(r'%s' % detail_list_xpath)
        for detail in detail_list:
            info_strip = detail.strip()
            if len(info_strip) > 0:
                weibo = info_strip.encode('ISO-8859-1').strip()
                return weibo

    @staticmethod
    def __bottom_list(bottomn_doc, index):
        """
        关注、评论、点赞
        """
        if index == 3:
            num_list = bottomn_doc.xpath(r'span[@class="line S_line1"]//em/text()')
            if len(num_list) > 0:
                num = num_list[0]
            else:
                num = 0
        else:
            num_list = bottomn_doc.xpath(r'span/text()')
            pure_num = num_list[0].split(' ')
            if len(pure_num) > 1:
                num = pure_num.pop().encode('ISO-8859-1')
            else:
                num = 0
        return num


def main():
    """
    执行
    """
    analysis = WBigV()
    print analysis
    for analyzed_info in analysis.analyzed_info_list:
        print analyzed_info.weibo_id
        print analyzed_info.weibo
        print analyzed_info.share_weibo_id
        print analyzed_info.share_num
        print analyzed_info.comment_num
        print analyzed_info.likes_num
        print '=============='


def load_data():
    """
    加载网页
    """
    if not os.path.exists('./stock_big_v1.html'):
        #         response = urllib2.urlopen('http://weibo.com/u/1279693157')#念父
        #         response = urllib2.urlopen('http://weibo.com/taishanggong')#太商公
        #         response = urllib2.urlopen('http://weibo.com/u/2234433682')#薄求
        #         response = urllib2.urlopen('http://weibo.com/kingsuanpan')#泽丰瑞熙熊总
        #         response = urllib2.urlopen('http://weibo.com/u/2075811071')#洪灝
        #         response = urllib2.urlopen('http://weibo.com/u/2436093373')#金融侠女盈盈
        #         response = urllib2.urlopen('http://weibo.com/peterlinqi')#林奇看盘
        #         response = urllib2.urlopen('http://weibo.com/315826888')#后知后觉股市直播
        response = urllib2.urlopen('http://weibo.com/u/1445403190')  # 财富密钥
        #         response = urllib2.urlopen('http://weibo.com/caolei214')#熊市猎人
        #         response = urllib2.urlopen('http://weibo.com/fanweifeng')
        with open('./stock_big_v.html', 'w') as f:
            f.write(response.read())


if __name__ == '__main__':
    # 登陆
    LoginWeibo()
    load_data()
    main()

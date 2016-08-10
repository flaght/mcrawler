# -*- coding:utf-8 -*-
"""
Create on 2015年11月27日

@author: SLM
"""
import urllib2
import os
import re
from lxml import html
from schduler.analysis_models.weibo_models.weibo_analysis.weibo_analysis_base import WBAnalysisBase
from schduler.analysis_models.analysis_base import AnalysisBase
from schduler.analysis_models.weibo_models.login.login import LoginWeibo


class WBExpert(WBAnalysisBase):
    """
    专家
    """
    tag = {'rule': '/html/head/title',
           'tag': '发现－股票专家'}

    def __init__(self, callback=None, **kwargs):
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self.analyzed_info_list = []
        self.__analysis()
        self.make_storage_cmd_expert()
        self.analyzed()

    def analyzed(self):
        self.make_storage_cmd_expert()
        AnalysisBase.analyzed(self)

    def __analysis(self):
        """
        解析
        """
        #         with open('./stock_expert.html', 'r') as f:
        #             self.html_data = f.read()
        #         with open('./stock_expert.json', 'w') as f:
        #             f.write(self.html_data)
        self.__get_part_html()

    def __get_part_html(self):
        """
        从源码中解析获得每块的html
        """
        view_list = re.findall("FM\.view\((.*?)\)</script>", self.html_data)
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
            # 以domid的值作为html的名字，domid为Pl_Core_F4RightUserList__4
            # ns为：pl.content.signInPeople.index
            title_domid = html_dic.get('domid', 'NotFound')
            if title_domid == 'Pl_Core_F4RightUserList__4':
                self.__expert(html_info)

    def __expert(self, stock_html_data):
        """
        股评专家
        """
        doc = html.fromstring(stock_html_data)
        expert_list = doc.xpath(r'//dd[@class="mod_info S_line1"]')
        for expert in expert_list:
            weibo_usercard = expert.xpath(r'div[@class="info_name W_fb W_f14"]//a[@class="S_txt1"]/@usercard')[
                0].encode()
            weibo_id = weibo_usercard.split('=').pop()
            # 这个url要上传到服务器
            url = expert.xpath(r'div[@class="info_name W_fb W_f14"]//a[@class="S_txt1"]/@href')[0].encode()
            self.set_analyzed_info_expert(weibo_id, url)
        current_num = doc.xpath(r'//a[@class="page S_txt1 S_bg1"]/text()')[0]
        # 获得翻页url
        if str(current_num) == '1':
            href_list = doc.xpath(r'//a[@class="page S_txt1"]/text()')
            part_url = 'http://d.weibo.com/230771_-_EXPERTUSER?page=%s#Pl_Core_F4RightUserList__4'
            page_num = href_list.pop()
            for i in xrange(int(page_num) + 1):
                if i == 0 or i == 1:
                    continue
                whole_url = part_url % i
                self.url_list.append(whole_url)


def main():
    """
    执行
    """
    analysis = WBExpert()
    print analysis
    for analyzed_info in analysis.analyzed_info_list:
        print analyzed_info.weibo_id
        print analyzed_info.url


def load_data():
    """
    加载网页html
    """
    if not os.path.exists('./stock_expert.html'):
        # 有效url,测试用
        # http://passport.weibo.com/wbsso/login?ssosavestate=1481201558&url=
        # http%3A%2F%2Fd.weibo.com%2F230771_-_EXPERTUSER%3Fpage%3D2&ticket=ST-NTc2NzAxODk1Mw
        # ==-1449665558-gz-CCAD32E5FAFCE71EC974EB3649A8B162&retcode=0
        url = 'http://d.weibo.com/230771_-_EXPERTUSER?page=2#Pl_Core_F4RightUserList__4'
        response = urllib2.urlopen(url)
        with open('./stock_expert.html', 'w') as f:
            f.write(response.read())


if __name__ == '__main__':
    LoginWeibo()
    load_data()
    main()

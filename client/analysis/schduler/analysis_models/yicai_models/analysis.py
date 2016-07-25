# -*- coding:utf-8 -*-
'''
Created on 2015年11月2日

@author: slm
'''
import urllib

class YCAnalysis(object):
    '''
    头部咨讯和中间分栏咨询解析
    '''
    def __init__(self, category_id, moudle_id, doc, cid, subcid):
        self.category_id = category_id
        self.moudle_id = moudle_id
        self.doc = doc
        self.cid = cid
        self.subcid = subcid
        self.url_part = 'http://www.yicai.com/ajax.php?op=getnewslist&'
        self.next_url_list = []
        #中间模块分栏列表(模块)
        self.middle_title_list = doc.xpath(r'//div[@id="Tab1"]//div[@class="Menubox"]//li/text()')

    def middle_first_next_url(self):
        '''
        (全部)其他模块第一页url，返给服务器
        '''
        if len(self.middle_title_list) > 1:
            #分栏数至少为两个时,获得其他模块url第一页url
            for i in xrange(len(self.middle_title_list)):
                if i == 0:
                    continue
                if self.moudle_id == '2' and i >= 4:
                    #时政
                    continue
                if self.moudle_id == '4' and i == 5:
                    #金融
                    continue
                if self.moudle_id == '9' and i == 4:
                    #思想
                    continue
                model_type = i+1
                name_str = '%s' % self.middle_title_list[i]
                type_name = urllib.quote(name_str.encode('utf-8', 'replace'))
                url = '%stype=%s&typename=%s&cid=%s&subcid=%s&page=%s'\
                 %(self.url_part, model_type, type_name, self.cid, self.subcid, 1)
                self.next_url_list.append(url)

def main():
    '''
    测试
    '''
    from lxml import html
    with open('./yicai_economy.html', 'r') as f:
        html_data = f.read()
    doc = html.fromstring(html_data)
    analysis = YCAnalysis('1', '1', doc, 182, 194)
    analysis.middle_first_next_url()
    print analysis.next_url_list
    for url in analysis.next_url_list:
        print url

def load_data():
    '''
    加载网页html
    '''
    import os
    import urllib2
    if not os.path.exists('./yicai_economy.html'):
        response = urllib2.urlopen('http://www.yicai.com/economy/')
        with open('./yicai_economy.html', 'w') as f:
            f.write(response.read())

if __name__ == '__main__':
    load_data()
    main()

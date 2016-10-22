# -*- coding:utf-8 -*-
'''
doc
'''
import urllib2
import socket
import random
from models.test_data import Data 

socket.setdefaulttimeout(5)#10s后超时

class CheckProxy(object):
    '''
    检测IP有效性，利用10个url进行检测，若失败次数超过5次则遗弃
    '''
    user_agents = []
    test_urls = []
    test_ip_list = []
    test_cnt = 0
    callback = None

    def __init__(self, ip_list, callback):
        appended_ip = []
        self.test_ip_list = []
        self.callback = callback
        for ip_info in ip_list:
            if ip_info['ip'] in appended_ip:
                continue
            self.test_ip_list.append(ip_info)
            appended_ip.append(ip_info['ip'])
        self.user_agents = Data.user_agents
        self.test_urls = Data.test_urls

    def start(self):
        '''
        开始执行
        '''
        self.spider_with_proxy()

    def spider_with_proxy(self):
        '''
        检测 利用多线程(每个线程爬全部测试网站)
        '''
        for i in xrange(len(self.test_ip_list)):
            proxy_dic = self.test_ip_list[i]
            self.use_thread(proxy_dic)

    def test_finished(self):
        self.test_cnt += 1
        test_url_cnt = float(len(self.test_urls))
        if self.test_cnt == len(self.test_ip_list):
            for k in xrange(len(self.test_ip_list)):
                ip_info = self.test_ip_list[k]
                time_out = ip_info['time_out']
                time_out_p = time_out/test_url_cnt
                refuse = ip_info['refuse']
                refuse_p = refuse/test_url_cnt
                if (time_out_p > 0.3 and refuse_p > 0.3) or time_out_p > 0.4 or refuse_p > 0.4:
                    #舍弃 used标记为0
                    self.test_ip_list[k].update({'used':0})
            if self.callback:
                self.callback(self.test_ip_list)

    def use_thread(self, proxy_dic):
        '''
        单个线程 分别对测试网站进行爬取
        '''
        ip = proxy_dic['ip']
        proxy = {'http':'http://%s' % (ip)}
        for i in xrange(len(self.test_urls)):
            self.work(i, proxy, proxy_dic)
        self.test_finished()
        print proxy_dic

    def work(self, index, proxy, proxy_dic):
        '''
        利用urlib连接服务器
        proxy:当前ip和端口
        proxy_dic：存放当前IP的所有信息
        '''
        spider_url = self.test_urls[index]
        user_agent = random.choice(self.user_agents)
        #设置使用代理
        proxy_support = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        #添加头信息，模仿浏览器抓去网页，对付返回403禁止访问的问题
        i_headers = {'User_Agent': user_agent}
        req = urllib2.Request(spider_url, headers=i_headers)
        try:
            response = urllib2.urlopen(req, timeout=3)
        except urllib2.HTTPError, e:
            print e.reason
            num = proxy_dic['refuse']
            proxy_dic.update({'refuse':num+1})
            return
        except Exception:
            num = proxy_dic['time_out']
            proxy_dic.update({'time_out':num+1})
            return

if __name__ == '__main__':

    all_ip_list = [{'type':'HTTPS', 'ip':'219.133.31.120:8888', \
                    'refuse':0, 'time_out':0, 'used':1},
                   {'type':'HTTP', 'ip':'119.253.252.27:3128', \
                    'refuse':0, 'time_out':0, 'used':1},
                   {'type':'HTTPS', 'ip':'218.200.66.199:80', \
                    'refuse':0, 'time_out':0, 'used':1},
                   {'type':'HTTP', 'ip':'182.88.231.4:8127', \
                    'refuse':0, 'time_out':0, 'used':1},
                   {'type':'HTTP', 'ip':'122.96.59.102:83', \
                    'refuse':0, 'time_out':0, 'used':1},
                   {'type':'HTTP', 'ip':'222.88.236.234:80', \
                    'refuse':0, 'time_out':0, 'used':1}]

    CheckProxy(all_ip_list).start()
    

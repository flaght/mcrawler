#! /usr/bin/env python
# coding=utf8
"""
测试用
"""
import urllib
import urllib2
import cookielib
import base64
import re
import json
import rsa
import binascii
import os

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)
part_url = 'framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack'
post_url = 'http://weibo.com/ajaxlogin.php?%s' % part_url
post_data = {
    'entry': 'weibo',
    'gateway': '1',
    'from': '',
    'savestate': '7',
    'userticket': '1',
    'pagerefer': '',
    'vsnf': '1',
    'su': '',
    'service': 'miniblog',
    'servertime': '',
    'nonce': '',
    'pwencode': 'rsa2',
    'rsakv': '',
    'sp': '',
    'sr': '1920*1080',
    'encoding': 'UTF-8',
    'prelt': '402',
    'url': post_url,
    'returntype': 'META'
}


class LoginWeibo(object):
    """
    登陆
    """

    def __init__(self):
        username = '2386183708@qq.com'
        pwd = '1293227197'
        cookie_file = 'cookie.txt'
        if self.login(username, pwd, cookie_file):
            print 'Login WEIBO succeeded'
        else:
            print 'Login WEIBO failed'

    @staticmethod
    def get_server_time(username):
        """
        获得服务器时间
        """
        url_first = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback='
        url = '%ssinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.18)' \
              % (url_first, username)
        data = urllib2.urlopen(url).read()
        p = re.compile('\((.*)\)')
        try:
            json_data = p.search(data).group(1)
            data = json.loads(json_data)
            server_time = str(data['servertime'])
            nonce = data['nonce']
            rsakv = data['rsakv']
            return server_time, nonce, rsakv
        except:
            print 'Get severtime error!'
            return None

    @staticmethod
    def get_pwd(pwd, servertime, nonce):
        """
        对密码加密
        """
        weibo_rsa_n = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D2' \
                      '45A87AC253062882729293E5506350508E7F9AA3BB77F4333' \
                      '231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB' \
                      '784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928' \
                      'EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3' \
                      '181D6442443'
        weibo_rsa_e = 65537
        # servertime:1447983475 nonce:BA2QI8 password:UUSU97A4VV
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)
        key = rsa.PublicKey(int(weibo_rsa_n, 16), weibo_rsa_e)
        encropy_pwd = rsa.encrypt(message, key)
        return binascii.b2a_hex(encropy_pwd)

    @staticmethod
    def get_user(username):
        """
        用户名加密
        """
        username_ = urllib.quote(username)
        username = base64.encodestring(username_)[:-1]
        return username

    def login(self, username, pwd, cookie_file):
        """
        登陆获得cookie
        """
        cookie_jar = None
        if os.path.exists(cookie_file):
            try:
                cookie_jar = cookielib.LWPCookieJar(cookie_file)
                cookie_jar.load(ignore_discard=True, ignore_expires=True)
                loaded = 1
            except cookielib.LoadError:
                loaded = 0
                print 'Loading cookies error'
            # install loaded cookies for urllib2
            if loaded:
                cookie_support_again = urllib2.HTTPCookieProcessor(cookie_jar)
                opener_again = urllib2.build_opener(cookie_support_again, urllib2.HTTPHandler)
                urllib2.install_opener(opener_again)
                print 'Loading cookies success'
                return 1
            else:
                return self.do_login(username, pwd, cookie_file)
        else:
            return self.do_login(username, pwd, cookie_file)

    def do_login(self, username, pwd, cookie_file):
        """
        登陆
        """
        cookie_jar2 = cookielib.LWPCookieJar()
        cookie_support2 = urllib2.HTTPCookieProcessor(cookie_jar2)
        opener2 = urllib2.build_opener(cookie_support2, urllib2.HTTPHandler)
        urllib2.install_opener(opener2)
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        try:
            servertime, nonce, rsakv = self.get_server_time(username)
        except:
            return
        global post_data
        post_data['servertime'] = servertime
        post_data['nonce'] = nonce
        post_data['su'] = self.get_user(username)
        post_data['sp'] = self.get_pwd(pwd, servertime, nonce)
        post_data['rsakv'] = rsakv
        post_data = urllib.urlencode(post_data)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
        req = urllib2.Request(
            url=url,
            data=post_data,
            headers=headers
        )
        result = urllib2.urlopen(req)
        text = result.read()
        p = re.compile('location\.replace\(\'(.*?)\'\)')
        print p
        try:
            login_url = p.search(text).group(1)
            print login_url
            data = urllib2.urlopen(login_url).read()
            patt_feedback = 'feedBackUrlCallBack\((.*)\)'
            p = re.compile(patt_feedback, re.MULTILINE)
            feedback = p.search(data).group(1)
            feedback_json = json.loads(feedback)
            if feedback_json['result']:
                cookie_jar2.save(cookie_file, ignore_discard=True, ignore_expires=True)
                return 1
            else:
                return 0
        except:
            print 'Login error!'


if __name__ == '__main__':
    LoginWeibo()

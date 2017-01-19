# -*- coding: utf-8 -*-

"""
Created on 201601207

@author kerry
"""

from bs4 import BeautifulSoup
from analysis.base.mlog import mlog
import xml.etree.ElementTree as ET
import platform
import sys
import re
import urllib2
import cookielib
import json


class Discussion:
    def __init__(self):
        self.__result = {}
        self.__stack_depth = 0
        self.__str_pos = 0
        self.__stringlist = []

    def __check_nickname(self, content):
        if content[0:1] == '@':
            return True

    def __face_format(self, content):
        re_style = re.compile('(<img src=.//assets\\.imedao\\.com).*?(images).*?(face).*?(title).*?(alt).*?(>)', re.I)
        for m in re_style.finditer(content):
            tree = ET.fromstring(m.group())
            if tree.attrib.has_key('title'):
                value = tree.attrib['title']
                content = content.replace(m.group(), value)
        return content

    def __check_quote(self, content):
        if content[len(content) - 2:len(content)] == '//':
            return True

    def __build_dictionary(self, valuet=None):
        """

        Returns:
            object:
        """
        current_pos = 0
        node = {}
        rlyf = 0
        while not self.__str_pos >= len(self.__stringlist):
            value = self.__stringlist[self.__str_pos]
            if value == ':回复' or value == '回复':
                rlyf = 1
                if current_pos > 0:
                    node["reply"] = self.__stringlist[self.__str_pos - 1]
                node["reverted"] = self.__stringlist[self.__str_pos + 1]
                node["content"] = self.__stringlist[self.__str_pos + 2]
                self.__str_pos += 1
            elif self.__check_quote(value):
                self.__str_pos += 1
                current_pos += 1
                node["quote"] = self.__build_dictionary(self.__stringlist[self.__str_pos + 1])
                node["content"] = value
            elif self.__check_nickname(value):
                if rlyf == 0 and (self.__str_pos + 1) < len(self.__stringlist):
                    c = self.__stringlist[self.__str_pos + 1]
                    t = c[0:1]
                    if ':' == t:
                        node["author"] = self.__stringlist[self.__str_pos]
            else:  # 字符串没有特殊性,视为普通内容
                if value[0:1] <> ":":
                    tcontent = node.get("content")
                    if tcontent is None:
                        node["content"] = value
                    else:
                        tcontent += value
                        node["content"] = tcontent
            self.__str_pos += 1
            current_pos += 1
        self.__stack_depth -= 1
        if node.has_key('author') and node.has_key('reply') and node.get('author') == node.get('reply'):
            del node['author']
        return node

    def __parser_t(self):
        # for string in stringlist:
        string = self.__stringlist[self.__str_pos]
        node = self.__build_dictionary()
        return node

    def parser_int(self, text):

        soup = BeautifulSoup(self.__face_format(text), "lxml")

        for string in soup.stripped_strings:
            self.__stringlist.append(string)
        return self.__parser_t()
        #print json.dumps(self.__parser_t())


if __name__ == '__main__':
    if platform.system() == "Darwin" or platform.system() == "Linux":
        reload(sys)
        sys.setdefaultencoding('utf-8')  # @UndefinedVariable
    #text = '当年那两套公寓不卖，现在市值不止1000万<img src="//assets.imedao.com/images/face/21lol.png" title="[大笑]" alt="[大笑]" height="24" />//<a href="http://xueqiu.com/n/股民张生" target="_blank">@股民张生</a>:回复<a href="http://xueqiu.com/n/QIINN" target="_blank">@QIINN</a>:06年3月入市资金20多万，当年追加十几万，第二年深圳卖两套公寓又追加30多万，06年买入万科，一年半后涨8倍赚200万后卖出，赚取人生的第一桶金。我一般重仓持有，赚100万以上的股票有6、7个，有万科、茅台、张裕B股、招行、浦发、格力、建行。当然，在深圳如果有钱就缴首付买房也能赚不少。'
    #text = '张大哥发家致富早，2006年就曾经在深圳有两套公寓了高手<a href="http://xueqiu.com/n/b_ing" target="_blank">@b_ing</a>。这两套公寓如果一直持有，估计收益率也是相当的高。<img src="//assets.imedao.com/images/face/20smile-smile.png" title="[笑]" alt="[笑]" height="24" />//<a href="http://xueqiu.com/n/股民张生" target="_blank">@股民张生</a>:回复<a href="http://xueqiu.com/n/QIINN" target="_blank">@QIINN</a>:06年3月入市资金20多万，当年追加十几万，第二年深圳卖两套公寓又追加30多万，06年买入万科，一年半后涨8倍赚200万后卖出，赚取人生的第一桶金。我一般重仓持有，赚100万以上的股票有6、7个，有万科、茅台、张裕B股、招行、浦发、格力、建行。当然，在深圳如果有钱就缴首付买房也能赚不少。'
    #text = '<p>&nbsp; &nbsp; &nbsp; &nbsp;今年港股投入十万，截止2016年12月31日，收益两万，港股方面全是银行股，买了几个不同的银行，估计和买指数基金差不多了，不过我对指数基金不熟，费用也不了解。A股投入43万，从三月份开始买茅台开始一路加仓，目前A股持仓方面：10万兴业银行+4万招商，5万国投+4.5川投，6万长安汽车，4万中国平安，还有双汇，福耀，茅台都是只有一点点。</p><p>&nbsp; &nbsp; &nbsp; &nbsp;今年是第一年买股票，所以开始时不知所措，买入第一支股票贵州茅台，买入价格243，之后一路涨，之后就没有买也没有卖过，随着时间的推移，买入股票的增多，越加发现茅台的好，真是不比较不知道什么叫好！！！全年最重仓的是银行股，但是A股银行股收益很有限，其次是水电，国投买入时机不好，到目前为止还是亏损一点。长安汽车是十二月份买进的，买的是B股，PE跌破5，目前为止亏损4%。平安好像是9月份买的，目前为止盈利3%左右。其实这一年最赚钱的是双汇，福耀，和茅台，都是些PE比较高的，相对而言，因为我喜欢买PE低的，哈哈。双汇，福耀，我是不太了解，不知道未来是什么样，所以当初是为了分散而买的，只知道是好公司，结果收益率是最好的。当然，在一年的时间里，这和买入时间点有很强的关系，两三年后再来比较一番。。。。。。。对了，全年中了一只新股贵广网络，目前还没有开板，目前为止新股盈利9870。</p><p>&nbsp; &nbsp; &nbsp; &nbsp;今年自己投入股票的资产还是太少了，占流动资产比率太低，明年应该加大配置，还有多弄几个账户打新，打新这事，老有人说这说那的，我觉得还是要弄弄，真到时候没有打新收益再说，现在明明有的收益自己不要偷懒。。。。。银行股的持仓太杂了，应该把它放集中到一两个，我想想是不是这样的。。。</p><p>&nbsp; &nbsp; &nbsp; &nbsp;上个星期和女朋友分手了，大家有很多不合的地方，是我不够好，辜负了她的期望。我给不了的幸福希望别人能给，一定要找个比我好的。感谢她带给我的所有快乐时光，我们经历的一切我都埋藏在内心中，或者让它随风而逝，微笑的面对没有你的生活。</p><p>&nbsp; &nbsp; &nbsp; &nbsp;2017年，既然做好了准备，既然什么都可以失去，那么不要辜负了自己，扬帆起航，全速前进。</p>'
    #dis = Discussion()
    #dis.parser_int(text)





    spider_url = "https://xueqiu.com/v4/statuses/user_timeline.json?user_id=4105865702&page=1&type=&_=1480139101751"
    #spider_url = "https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=SZ300072&hl=0&source=all&sort=alpha&page=1&_=1483343250780"
    user_agent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a1) Gecko/20070308 Minefield/3.0a1"
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
    urllib2.install_opener(opener)
    cookie = "s=5v11kwhniz; u=661483274707164; xq_a_token=f5871dbcf21ad05a1869c9ac5d8003738780e00a; xq_r_token=02e70b76a4eb12083a6af1e068f11ec0490f17bf;"
    # cookie = "xq_a_token=ba3a563ac0e6e80f3ec726611f51b6c4ee183d0b;xq_r_token=e386c22c5442603d86294a718b13da436909b3f07;s=4wqrx2gsap;u=027398863330126;"
    i_headers = {'User-Agent': user_agent, "Cookie": cookie}
    try:
        req = urllib2.Request(url=spider_url, headers=i_headers)
        # req.set_proxy('113.18.193.6:8080', 'http')
        response = opener.open(req, timeout=5)
    except Exception, e:
        print e

    if response.getcode() == 200:
        str = response.read()
        tstr = json.loads(str)

    tobj = []
    for i in tstr.get('statuses'):
        text = i.get('text')
        dis = Discussion()
        text = text.replace('<p>', '')
        text = text.replace('</p>', '')
        #dis.parser_int(text)
        tobj.append(dis.parser_int(text))

    tm = json.dumps(tobj)
    print tm

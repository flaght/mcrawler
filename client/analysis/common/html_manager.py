#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
#encoding=utf-8

"""
Created on 2016年12月7日

@author: kerry
"""

import re

class HtmlManager:
    def filter_tags(self, htmlstr):
        # 先过滤CDATA
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', htmlstr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n', s)
        s = self.__replaceCharEntity(s)  # 替换实体
        return s

    ##替换常用HTML字符实体.
    # 使用正常的字符替换HTML中特殊的字符实体.
    # 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
    # @param htmlstr HTML字符串.
    def __replaceCharEntity(self, htmlstr):
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"',}

        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()  # entity全称，如&gt;
            key = sz.group('name')  # 去除&;后entity,如&gt;为gt
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                # 以空串代替
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

    def __repalce(self, s, re_exp, repl_string):
        return re_exp.sub(repl_string, s)



html_manager = HtmlManager()

if __name__=='__main__':
    #s='<p>招浦民兴2016年10月20日融资余额：<br>浦发银行23.80 亿,日+759.23 万;<br>民生银行57.44 亿,日-452.85 万;<br>招商银行20.88 亿,日+1518.97 万;<br>兴业银行59.74 亿,日-5630.34 万.<br>沪港通2016年10月20日前十<br>无<br>港股通2016年10月19日前十<br>民生买1.8万,卖8316万.<br><a href="http://xueqiu.com/S/SH600000" target="_blank">$浦发银行(SH600000)$</a>&nbsp;&nbsp; &nbsp; &nbsp;<a href="http://xueqiu.com/S/SH600036" target="_blank">$招商银行(SH600036)$</a>&nbsp;&nbsp; &nbsp; &nbsp;<a href="http://xueqiu.com/S/SH601166" target="_blank">$兴业银行(SH601166)$</a>&nbsp;</p>'
    s='<img src="//assets.imedao.com/images/face/03zan.png" title="[很赞]" alt="[很赞]" height="24" />//<a href="http://xueqiu.com/n/W安全边际" target="_blank">@W安全边际</a>:回复<a href="http://xueqiu.com/n/top_gun888" target="_blank">@top_gun888</a>:“银粉队伍分崩离析”这个标题好！<br />几年前我也曾是银粉的一员，重仓持有兴业银行多年，也确确实实为我创造了些许利润。随着对银行之外的行业逐渐的学习与了解，我也逐渐跳出了固守银行股的圈子，目前银行股的仓位已降到10%左右。但价值投资的理念与原则并没有改变！我还自认为是价值投资者的一员！<br />曾经有过迷茫，也有过反思。价值投资并不一定非得投资银行股，投银行股的也并不全是价值投资者。只要是自己所了解的领域，只要是有低估的价格，那么完全可以运用价值投资理念探索与发展。<br />最后向曾经帮着我学习并实践价值投资理念的银行股致敬！<a href="http://xueqiu.com/S/SH601166" target="_blank">$兴业银行(SH601166)$</a> <a href="http://xueqiu.com/S/SH600036" target="_blank">$招商银行(SH600036)$</a> <a href="http://xueqiu.com/S/SH600000" target="_blank">$浦发银行(SH600000)$</a>'
    news=html_manager.filter_tags(s)
    print "before====>"
    print s
    print "after====>"
    print news
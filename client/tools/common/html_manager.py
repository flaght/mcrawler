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
        s = re_br.sub('\n', s)  # 将br转换为换行,再直接替换掉
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        s = s.replace(' ', '')
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
    #s='<p>招浦民兴2016年10月20日融资余额：<br>   浦发银行23.80 亿,日+759.23 万;<br>民生银行57.44 亿,日-452.85 万;<br>招商银行20.88 亿,日+1518.97 万;<br>兴业银行59.74 亿,日-5630.34 万.<br>沪港通2016年10月20日前十<br>无<br>港股通2016年10月19日前十<br>民生买1.8万,卖8316万.<br><a href="http://xueqiu.com/S/SH600000" target="_blank">$浦发银行(SH600000)$</a>&nbsp;&nbsp; &nbsp; &nbsp;<a href="http://xueqiu.com/S/SH600036" target="_blank">$招商银行(SH600036)$</a>&nbsp;&nbsp; &nbsp; &nbsp;<a href="http://xueqiu.com/S/SH601166" target="_blank">$兴业银行(SH601166)$</a>&nbsp;</p>'
    #s='<img src="//assets.imedao.com/images/face/03zan.png" title="[很赞]" alt="[很赞]" height="24" />//<a href="http://xueqiu.com/n/W安全边际" target="_blank">@W安全边际</a>:回复<a href="http://xueqiu.com/n/top_gun888" target="_blank">@top_gun888</a>:“银粉队伍分崩离析”这个标题好！<br />几年前我也曾是银粉的一员，重仓持有兴业银行多年，也确确实实为我创造了些许利润。随着对银行之外的行业逐渐的学习与了解，我也逐渐跳出了固守银行股的圈子，目前银行股的仓位已降到10%左右。但价值投资的理念与原则并没有改变！我还自认为是价值投资者的一员！<br />曾经有过迷茫，也有过反思。价值投资并不一定非得投资银行股，投银行股的也并不全是价值投资者。只要是自己所了解的领域，只要是有低估的价格，那么完全可以运用价值投资理念探索与发展。<br />最后向曾经帮着我学习并实践价值投资理念的银行股致敬！<a href="http://xueqiu.com/S/SH601166" target="_blank">$兴业银行(SH601166)$</a> <a href="http://xueqiu.com/S/SH600036" target="_blank">$招商银行(SH600036)$</a> <a href="http://xueqiu.com/S/SH600000" target="_blank">$浦发银行(SH600000)$</a>'
    s = ' &nbsp     ;无论从营收还是销量计算，华润都是国内三巨头中的NO.1（华润营收已由港币换算成人民币，计算时汇率0.8502）。2015年华润的销量达到1168.3万千升（千升约等于吨），青岛紧随其后848万千升>     ，华润在巨头中销量垫底，483万千升。    销量好不代>     表利润高。毛利润率一端三巨头的情况确相反，顺序完全对调。燕京可以达到40%+，青岛约38%，华润仅有31%。观察三巨头毛利润率，同比全部倒退，老大华润甚至同比倒退3.5%+之多。如果一个行业老大得毛利润率都不能保持平稳，甚至出现大幅倒退，那这个行业的境况也多半不佳。除非该行业中的公司估值有着极佳的吸引力，不然还是谨慎为妙。    啤酒业的净利>     润率如此之低，让我有些不敢相信。作为龙头的华润其净利润率居然仅仅2.4%，最好的青岛也不过6.2%（如以扣非利润计算，不过3.81%）。在毛利率不差的前提下，为何净利润率不佳？查看了销售费用、管理费用和财务费用后，答案不言自明。三巨头的各自情况相差不多，三费率均在25%+。青岛25.39%、燕京25.27%、华润27.84%。这一项数据与同是酿酒业的白酒们相比就显得拿不出手了。从侧>     面隐含证明了啤酒业无论从产品的差异化，对渠道的控制力，还是产品的定价能力都与白酒业不可同日而语。    作为盈利能力的重要考核指标--ROE，因净利润率的表现不佳，就只能寄希望于资产周转率了，杠杆虽然可以提升盈利能力，但经营环境不佳时，对公司的伤害也一点都不含糊。很遗憾，资产周转率相对于啤酒业庞大的销量而言，并不是想象中的美。最好的青岛仅勉强可以达到1次，其他两家均不足0.7次。      &n     bsp;经营上，各家的情况不同。在低利润率的基础上，成本决定竞争能力。成本费用率方面，青岛94.95%、燕京、95.53%、华润98.18%。三家均较高的数据透露出这个行业在成本控制方面的难度不低。     作为消费品中的快消品，并且有保质期限制的产品。存货周转率是每家公司的生命线。三家的情况表现出了很大的差别。青岛的存货周转率两倍于华润，三倍于燕京，这一耀眼的数据下掩盖着怎样的市场表象，需要通过销售市场来观察。>     （这不是本文的重点，在此略过）@疯狂_de_石头 能否谈谈？     最后一项数据，相对于三家的产品定位也许能够说明一些问题。每千升的收入和每千升的利润大概能够反映出 现阶段各家的经营策略。青岛的吨收入和吨利润明显高出其他两家，吨收入超过另两家近30%。青啤产品在高端化的进程上还是值得持续观察的，毕竟外资两巨头百威、嘉士伯及进口啤酒掌控的高端领域和高利润率是一块不小的蛋糕，如何挣得一部分高端领域的蛋糕，是眼下的难题和机遇。    华润和燕京吨收入几近相同的情况下，吨利润确不尽相同。华润的产品销量如>     此庞大，达到千万吨级，除了低端化的产品定位，不知对于低端市场是否也占据着绝对优势？ 华润啤酒当下的产能达到2200万吨！！！是其销量的两倍。 只是利润率如此之低，规模有如此之大，让>     人不禁联想到大部分央企们的唯一经营之道--- 一切经营围绕规模开展，规模是检验经营的唯一标准！'
    news=html_manager.filter_tags(s)
    print "before====>"
    print s
    print "after====>"
    print news
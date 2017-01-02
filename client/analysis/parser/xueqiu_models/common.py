# -*- coding: utf-8 -*-

"""
Created on 201601207

@author kerry
"""

import re
import platform
import sys
import xml.etree.ElementTree as ET
from analysis.common.html_manager import html_manager

from analysis.base.mlog import mlog
class Common:

    """
    表情替换成文字
    """
    @classmethod
    def face_format(cls, content):
        re_t = re.compile('(<img src=.//assets\\.imedao\\.com).*?(images).*?(face).*?(title).*?(alt).*?(>)', re.DOTALL)
        list = []
        for m in re_t.finditer(content):
            try:
                tree = ET.fromstring(m.group())
                if tree.attrib.has_key('title'):
                    value = tree.attrib['title']
                    r = {'start': m.start(), 'end': m.end(), 'str': m.group(), 'value': value}
                    list.append(r)
            except Exception, e:
                mlog.log().error(m.group())

        for i in list:
            str = i['str']
            content = content.replace(str, i['value'])
        return content


    """
    昵称解析
    """
    @classmethod
    def nickname_format(cls, str,content):
        reply_nickname = None
        try:
            tree = ET.fromstring(str[2:len(str) - 1])
            lst_node = tree.getiterator('a')
            for node in lst_node:
                reply_nickname = node.text[1:len(node.text)]
                break
        except Exception, e:
            mlog.log().error(str + "===>" + content)

        return reply_nickname

    """
    转发回复人分离
    """
    @classmethod
    def reply_format(cls, content):
        #re_m = re.compile('(<)(a)( )(href)(=).*?(xueqiu\\.com/n).*?(target).*?(@).*?(<\\/a>(:))', re.DOTALL)
        re_m = re.compile('(<a href="http://xueqiu.com/n/).*?(target="_blank">@).*?(<\\/a>:)', re.DOTALL)
        for m in re_m.finditer(content):
            reply_name = cls.nickname_format("//" + m.group(), content)
            return {"reply_name":reply_name, "comment":cls.face_format(content[m.end():len(content)])}
        return {"reply_name":None,"comment":cls.face_format(content)}



    """
    过滤图片
    """
    @classmethod
    def filter_pic(cls, content):
        re_t = re.compile('(<img src=.*?xqimg\\.imedao\\.com).*?(class=).*?(>)', re.DOTALL)
        for m in re_t.finditer(content):
            content = content.replace(m.group(), '')
        return content

    """
    其他符号处理
    """
    @classmethod
    def filter_symbol(cls, content):
        content = content.replace('>', '')
        content = content.replace('\n','')
        return content

    @classmethod
    def replaceCharEntity(cls, htmlstr):
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

    """
    将转发切割
    """
    @classmethod
    def quote_format(cls, content):
        last_end = 0
        last_nick_name = None
        queue = []
        re_t = re.compile('(\\/)(\\/)(<)(a)( )(href)(=).*?(xueqiu\\.com).*?(target).*?(@).*?(<\\/a>(:))', re.DOTALL)
        for m in re_t.finditer(content):
            last_unit = {}
            if last_nick_name is not None:
                last_unit['nickname'] = last_nick_name
            last_nick_name = Common.nickname_format(m.group(),content)
            text = content[last_end:m.start()]
            last_end = m.end()
            reply = Common.reply_format(text)
            if reply.get('reply_name') is not None:
                last_unit['reply_name'] = reply.get('reply_name')
            last_unit['comment'] = Common.filter_symbol(html_manager.filter_tags(reply.get('comment')))
            queue.append(last_unit)
            # 最后一段特殊处理
        text = content[last_end:len(content)]
        reply = Common.reply_format(text)
        last_unit = {}
        if reply.get('reply_name') is not None:
            last_unit['reply_name'] = reply.get('reply_name')
        last_unit['comment'] = Common.filter_symbol(html_manager.filter_tags(reply.get('comment')))
        queue.append(last_unit)
        return queue


xq_common = Common()

import json

if __name__=='__main__':
    if platform.system() == "Darwin" or platform.system() == "Linux":
        reload(sys)
        sys.setdefaultencoding('utf-8')  # @UndefinedVariable
    #text = '<img src="//assets.imedao.com/images/face/03zan.png" title="[很赞]" alt="[很赞]" height="24" />//<a href="http://xueqiu.com/n/W安全边际" target="_blank">@W安全边际</a>:回复<a href="http://xueqiu.com/n/top_gun888" target="_blank">@top_gun888</a>:“银粉队伍分崩离析”这个标题好！<br />几年前我也曾是银粉的一员，重仓持有兴业银行多年，也确确实实为我创造了些许利润。<img src="//assets.imedao.com/images/face/04zan.png" title="[很叼]" alt="[很叼]" height="24" />随着对银行之外的行业逐渐的学习与了解，我也逐渐跳出了固守银行股的圈子，目前银行股的仓位已降到10%左右。但价值投资的理念与原则并没有改变！我还自认为是价值投资者的一员！<br />曾经有过迷茫，也有过反思。<img src="//assets.imedao.com/images/face/05zan.png" title="[很棒]" alt="[很棒]" height="24" />价值投资并不一定非得投资银行股，投银行股的也并不全是价值投资者。<img class="ke_img" src="//xqimg.imedao.com/158d866c1a92f7f3fd47df38.jpeg!custom.jpg" />只要是自己所了解的领域，只要是有低估的价格，那么完全可以运用价值投资理念探索与发展。<br />最后向曾经帮着我学习并实践价值投资理念的银行股致敬！<a href="http://xueqiu.com/S/SH601166" target="_blank">$兴业银行(SH601166)$</a> <a href="http://xueqiu.com/S/SH600036" target="_blank">$招商银行(SH600036)$</a> <a href="http://xueqiu.com/S/SH600000" target="_blank">$浦发银行(SH600000)$</a>'
    #text = '<img src="//assets.imedao.com/images/face/14guzhang.png" title="[鼓鼓掌]" alt="[鼓鼓掌]" height="24" /><img src="//assets.imedao.com/images/face/21lol.png" title="[大笑]" alt="[大笑]" height="24" /><img src="//assets.imedao.com/images/face/19qiaopi.png" title="[俏皮]" alt="[俏皮]" height="24" /> //<a href="http://xueqiu.com/n/呼噜老K" target="_blank">@呼噜老K</a>: &nbsp;说的好//<a href="http://xueqiu.com/n/ozrunner" target="_blank">@ozrunner</a>:回复<a href="http://xueqiu.com/n/股市狂韭菜" target="_blank">@股市狂韭菜</a>: 这些商业常识性的细节被很多人选择性忽视了。简单说，乐视群企业已经失去了商誉，很多人竟然还当他是个宝，害怕人低价强购，我乐个去啊'
    #text = '<img src="//assets.imedao.com/images/face/14guzhang.png" title="[鼓鼓掌]" alt="[鼓鼓掌]" height="24" /><img src="//assets.imedao.com/images/face/21lol.png" title="[大笑]" alt="[大笑]" height="24" /><img src="//assets.imedao.com/images/face/19qiaopi.png" title="[俏皮]" alt="[俏皮]" height="24" /> //<a href="http://xueqiu.com/n/ozrunner" target="_blank">@ozrunner</a>:回复<a href="http://xueqiu.com/n/股市狂韭菜" target="_blank">@股市狂韭菜</a>: 这些商业常识性的细节被很多人选择性忽视了。简单说，乐视群企业已经失去了商誉，很多人竟然还当他是个宝，害怕人低价强购，我乐个去啊 //<a href="http://xueqiu.com/n/呼噜老K" target="_blank">@呼噜老K</a>: &nbsp;<img src="//assets.imedao.com/images/face/14guzhang.png" title="[鼓鼓掌]" alt="[鼓鼓掌]" height="24" /> <img src="//assets.imedao.com/images/face/19qiaopi.png" title="[俏皮]" alt="[俏皮]" height="24" />说的好'
    #text = '<img src="//assets.imedao.com/images/face/14guzhang.png" title="[鼓鼓掌]" alt="[鼓鼓掌]" height="24" /><img src="//assets.imedao.com/images/face/21lol.png" title="[大笑]" alt="[大笑]" height="24" /><img src="//assets.imedao.com/images/face/19qiaopi.png" title="[俏皮]" alt="[俏皮]" height="24" />这些商业常识性的细节被很多人选择性忽视了。简单说，乐视群企业已经失去了商誉，很多人竟然还当他是个宝，害怕人低价强购，我乐个去啊 '
    #text = '<a href="http://xueqiu.com/S/SZ300400" target="_blank">$劲拓股份(SZ300400)$</a> <a href="http://xueqiu.com/n/随风启动" target="_blank">@随风启动</a>: 大盘在悄悄的起变化，盘中跳水虽有，但外强中干，资金逢低坚决吸入。券商股今天走强预示有资金开始看好未来大势，提前在高弹性的券商板块里布局。个股上看：<br/><a href="http://xueqiu.com/S/SH600367" target="_blank">$红星发展(SH600367)$</a>&nbsp;600367今天不错，安心持有。<br/><a href="http://xueqiu.com/S/SH601789" target="_blank">$宁波建工(SH601789)$</a>&nbsp;601789有成为大牛潜力，坚决杀入<br/><a href="http://xueqiu.com/S/SH600128" target="_blank">$弘业股份(SH600128)$</a>&nbsp;600128前景光明<br/><a href="http://xueqiu.com/S/SH600773" target="_blank">$西藏城投(SH600773)$</a>&nbsp;600773形态乐观<br/><a href="http://xueqiu.com/S/SZ000065" target="_blank">$北方国际(SZ000065)$</a>&nbsp;000065,<a href="http://xueqiu.com/S/SH600262" target="_blank">$北方股份(SH600262)$</a>&nbsp;600262等待亲兄弟王者归来后拉它们一把！！<br/>全都棒棒哒<img src="//assets.imedao.com/images/face/03zan.png" title="[很赞]" alt="[很赞]" height="24" />'
    #text = '<a href="http://xueqiu.com/S/SZ300400" target="_blank">$劲拓股份(SZ300400)$</a> <a href="http://xueqiu.com/n/随风启动" target="_blank">@随风启动</a>:这股的好处也有:深圳的公司；行业前景好；盘小。跌稳以后还是可以投机参与。30左右~60左右波动。后面就看公司发展了！300033,300333,002618,002739,603866,000514,300059,002067,002777,002322,002088'

    #text = '<img src="//xqimg.imedao.com/155dfb64aba15b3fe33bf304.jpg!custom.jpg" class="ke_img" ><br>&nbsp;&nbsp;&nbsp;&nbsp     ;无论从营收还是销量计算，华润都是国内三巨头中的NO.1<img src="//assets.imedao.com/images/face/14guzhang.png" title="[鼓鼓掌]" alt="[鼓鼓掌]" height="24" />（华润营收已由港币换算成人民币，计算时汇率0.8502）。2015年华润的销量达到1168.3万千升（千升约等于吨），青岛紧随其后848万千升>     ，华润在巨头中销量垫底，483万千升。<br/><br/><img src="//xqimg.imedao.com/155dfb64a841303fe447f733.jpg!custom.jpg" class="ke_img" >&nbsp;&nbsp;&nbsp;&nbsp;<br><br/>销量好不代>     表利润高。毛利润率一端三巨头的情况确相反，顺序完全对调。燕京可以达到40%+，青岛约38%，华润仅有31%。观察三巨头毛利润率，同比全部倒退，老大华润甚至同比倒退3.5%+之多。如果一个行业老大得毛利润率都不能保持平稳，甚至出现大幅倒退，那这个行业的境况也多半不佳。除非该行业中的公司估值有着极佳的吸引力，不然还是谨慎为妙。&nbsp;&nbsp;&nbsp;&nbsp;<br>啤酒业的净利>     润率如此之低，让我有些不敢相信。作为龙头的华润其净利润率居然仅仅2.4%，最好的青岛也不过6.2%（如以扣非利润计算，不过3.81%）。在毛利率不差的前提下，为何净利润率不佳？查看了销售费用、管理费用和财务费用后，答案不言自明。三巨头的各自情况相差不多，三费率均在25%+。青岛25.39%、燕京25.27%、华润27.84%。这一项数据与同是酿酒业的白酒们相比就显得拿不出手了。从侧>     面隐含证明了啤酒业无论从产品的差异化，对渠道的控制力，还是产品的定价能力都与白酒业不可同日而语。<br/><br/><img src="//xqimg.imedao.com/155dfb64c791623fe6a53649.jpg!custom.jpg"      class="ke_img" >&nbsp;&nbsp;&nbsp;&nbsp;<br><br/>作为盈利能力的重要考核指标--ROE，因净利润率的表现不佳，就只能寄希望于资产周转率了，杠杆虽然可以提升盈利能力，但经营环境不佳时，对公司的伤害也一点都不含糊。很遗憾，资产周转率相对于啤酒业庞大的销量而言，并不是想象中的美。最好的青岛仅勉强可以达到1次，其他两家均不足0.7次。<br/><br/><img src="//xqimg.ime     dao.com/155dfb645631603fd5a4525d.jpg!custom.jpg" class="ke_img" >&nbsp;&nbsp;&nbsp;&nbsp;<br/><br>如此庞大的销量支撑下，为何资产的周转率这样不堪？我们审视一下资产负债表中的固>     定资产一项，答案就明了了，主要有以下两方面原因：&nbsp;<br>啤酒业的固定资产占比基本在35%及以上，华润则达到42%+。而图中白酒的两大巨头茅台和五粮液这一数据只有10%、13%。啤酒业对酿制工艺的要求不必白酒差，只是对于酿制工艺的把控，需要高端制作设备的支持。作为山东人的我们，经常听到的啤酒专业词语之一就是德国酿造工艺。为了这几个字，厂家可是没少采购最新的制作>     设备，无形中的经营再投入就会增加，转化为固定资产。第二点是行业目前的局面形成的。啤酒业正在经历着兼并、收购阶段，由于有着重资产的属性，再加上收购的步伐较快，固定资产比例的增加>     则会越来越多。<br/><br>&nbsp;&nbsp;&nbsp;&nbsp;<img src="//xqimg.imedao.com/155dfb64b9c1313fea262c9c.jpg!custom.jpg" class="ke_img" >&nbsp;&nbsp;&nbsp;<br>&nbsp;&nbsp;&nbsp;&n     bsp;<br/>经营上，各家的情况不同。在低利润率的基础上，成本决定竞争能力。成本费用率方面，青岛94.95%、燕京、95.53%、华润98.18%。三家均较高的数据透露出这个行业在成本控制方面的难度不低。<br/><br/>&nbsp;<img src="//xqimg.imedao.com/155dfb64a5712f3fc31e7a38.jpg!custom.jpg" class="ke_img" >&nbsp;&nbsp;&nbsp;&nbsp;<br><br/>作为消费品中的快消品，并且有保质期限制的产品。存货周转率是每家公司的生命线。三家的情况表现出了很大的差别。青岛的存货周转率两倍于华润，三倍于燕京，这一耀眼的数据下掩盖着怎样的市场表象，需要通过销售市场来观察。>     （这不是本文的重点，在此略过）<br><a href="http://xueqiu.com/n/疯狂_de_石头" target="_blank">@疯狂_de_石头</a>&nbsp;能否谈谈？&nbsp;<img src="//xqimg.imedao.com/155dfb64b98161     3fea444bd9.jpg!custom.jpg" class="ke_img" >&nbsp;&nbsp;&nbsp;&nbsp;<br><br/>最后一项数据，相对于三家的产品定位也许能够说明一些问题。每千升的收入和每千升的利润大概能够反映出 现阶段各家的经营策略。青岛的吨收入和吨利润明显高出其他两家，吨收入超过另两家近30%。青啤产品在高端化的进程上还是值得持续观察的，毕竟外资两巨头百威、嘉士伯及进口啤酒掌控的高端领域和高利润率是一块不小的蛋糕，如何挣得一部分高端领域的蛋糕，是眼下的难题和机遇。&nbsp;&nbsp;&nbsp;&nbsp;<br>华润和燕京吨收入几近相同的情况下，吨利润确不尽相同。华润的产品销量如>     此庞大，达到千万吨级，除了低端化的产品定位，不知对于低端市场是否也占据着绝对优势？ 华润啤酒当下的产能达到2200万吨！！！是其销量的两倍。 只是利润率如此之低，规模有如此之大，让>     人不禁联想到大部分央企们的唯一经营之道--- 一切经营围绕规模开展，规模是检验经营的唯一标准！<img src="//assets.imedao.com/images/face/04bian.png" title="[不赞]" alt="[不赞]" hei     ght="24" />'
    #text = '//<a href="http://xueqiu.com/n/躇杉" target="_blank">@躇杉</a> 回复<a href="http://xueqiu.com/n/赵叔" target="_blank">@赵叔</a>:===><a href="http://xueqiu.com/n/躇杉" target="_blank">@躇杉</a> 回复<a href="http://xueqiu.com/n/赵叔" target="_blank">@赵叔</a>:按照叔的提示，小盘缩量业绩佳的有： <a href="http://xueqiu.com/S/SH603566" target="_blank">$普莱柯(SH603566)$</a> <a href="http://xueqiu.com/S/SH603601" target="_blank">$再升科技(SH603601)$</a> <a href="http://xueqiu.com/S/SH603818" target="_blank">$曲美股份(SH603818)$</a> <a href="http://xueqiu.com/S/SH603022" target="_blank">$新通联(SH603022)$</a> <a href="http://xueqiu.com/S/SH600605" target="_blank">$汇通能源(SH600605)$</a>'
    text = '<a href="http://xueqiu.com/n/躇杉" target="_blank">@躇杉</a> 回复<a href="http://xueqiu.com/n/赵叔" target="_blank">@赵叔</a>:按照叔的提示，小盘缩量业绩佳的有： <a href="http://xueqiu.com/S/SH603566" target="_blank">$普莱柯(SH603566)$</a> <a href="http://xueqiu.com/S/SH603601" target="_blank">$再升科技(SH603601)$</a> <a href="http://xueqiu.com/S/SH603818" target="_blank">$曲美股份(SH603818)$</a> <a href="http://xueqiu.com/S/SH603022" target="_blank">$新通联(SH603022)$</a> <a href="http://xueqiu.com/S/SH600605" target="_blank">$汇通能源(SH600605)$</a>'
    #text = Common.filter_pic(text)
    """
    quote_result = Common.quote_format(text)

    t = json.dumps(quote_result)
    #print t.decode('unicode-escape')
    for i in quote_result:
        if i.has_key('nickname') :
            print "nickname:" + i.get('nickname')
        if i.has_key('reply_name'):
            print "reply_name:" + i.get('reply_name')
        if i.has_key('comment'):
            print "comment:" + i.get('comment')
        print "================"
    """
    re_t = re.compile('(<a href="http://xueqiu.com/n/)*?(" target="_blank">@)*?(</a> )*?(<a href="http://xueqiu.com/n/)*?(" target="_blank">@)*?(</a>:)', re.DOTALL)
    i = 0
    last_end = 0
    last_nick_name = ""
    dict = {}
    for m in re_t.finditer(text):
        content = text[last_end:m.start()]
        last_end = m.end()
        print last_nick_name, Common.reply_format(content)
        last_nick_name = Common.nickname_format(m.group())
        i += 1

    #最后一段特殊处理
    content = text[last_end:len(text)]

    #回复人处理
    t =  Common.reply_format(content)
    if t is not  None:
        print last_nick_name,t.get('reply_name'),t.get('coment')

    #print m.group()
        #print m.start(),m.end(),m.group()[2:len(m.group())]
        #tree = ET.fromstring(m.group()[2:len(m.group())])
        #content = text[0:m.start()]
        #lst_node = tree.getiterator('a')
        #for node in lst_node:
        #    nickname =  node.text[1:len(node.text)]
        #    break
    #    print Common.face(text[0:m.start()])
    #    print Common.face(text[m.start() + 2:len(text)])
    #    print m.group()
    #print Common.face(text)

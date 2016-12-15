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
        re_t = re.compile('(<img src=.*?assets\\.imedao\\.com).*?(images).*?(face).*?(title).*?(alt).*?(>)', re.DOTALL)
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
    def nickname_format(cls, str):
        reply_nickname = None
        try:
            tree = ET.fromstring(str[2:len(str) - 1])
            lst_node = tree.getiterator('a')
            for node in lst_node:
                reply_nickname = node.text[1:len(node.text)]
                break
        except Exception, e:
            mlog.log().error(reply_nickname)

        return reply_nickname

    """
    转发回复人分离
    """
    @classmethod
    def reply_format(cls, content):
        #re_m = re.compile('(<)(a)( )(href)(=).*?(xueqiu\\.com/n).*?(target).*?(@).*?(<\\/a>(:))', re.DOTALL)
        re_m = re.compile('(<a href="http://xueqiu.com/n/).*?(target).*?(@).*?(<\\/a>(:))', re.DOTALL)
        for m in re_m.finditer(content):
            reply_name = cls.nickname_format("//" + m.group())
            return {"reply_name":reply_name, "comment":cls.face_format(content[m.end():len(content)])}
        return {"reply_name":None,"comment":cls.face_format(content)}


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
            last_nick_name = Common.nickname_format(m.group())
            text = content[last_end:m.start()]
            last_end = m.end()
            reply = Common.reply_format(text)
            if reply.get('reply_name') is not None:
                last_unit['reply_name'] = reply.get('reply_name')
            last_unit['comment'] = html_manager.filter_tags(reply.get('comment'))
            queue.append(last_unit)
            # 最后一段特殊处理
        text = content[last_end:len(content)]
        reply = Common.reply_format(text)
        last_unit = {}
        if reply.get('reply_name') is not None:
            last_unit['reply_name'] = reply.get('reply_name')
        last_unit['comment'] = html_manager.filter_tags(reply.get('comment'))
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
    text = '<a href="http://xueqiu.com/S/SZ300400" target="_blank">$劲拓股份(SZ300400)$</a> <a href="http://xueqiu.com/n/随风启动" target="_blank">@随风启动</a>:这股的好处也有:深圳的公司；行业前景好；盘小。跌稳以后还是可以投机参与。30左右~60左右波动。后面就看公司发展了！300033,300333,002618,002739,603866,000514,300059,002067,002777,002322,002088'
    quote_result = Common.quote_format(text)

    t = json.dumps(quote_result)
    print t.decode('unicode-escape')
    for i in quote_result:
        if i.has_key('nickname') :
            print "nickname:" + i.get('nickname')
        if i.has_key('reply_name'):
            print "reply_name:" + i.get('reply_name')
        if i.has_key('comment'):
            print "comment:" + i.get('comment')
        print "================"
    """
    re_t = re.compile('(\\/)(\\/)(<)(a)( )(href)(=).*?(xueqiu\\.com).*?(target).*?(@).*?(<\\/a>(:))', re.DOTALL)
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
    """
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

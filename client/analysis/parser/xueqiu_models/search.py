# -*- coding: utf-8 -*-

import json

"""
Created on 201601015

@author kerry
"""


class Search():
    """
    雪球
    """
    prefix = "xueqiu"
    plt_id = "60006"
    def __init__(self):
        pass

    def parser(self,data):
        tlist = []
        jobj = json.loads(data)

        if (jobj.has_key("error_code")):
            return None, None
        symbol = jobj.get("symbol", "")
        dlist = jobj.get("list", "")
        for d in dlist:
            x = self.__parser_search_text_unit(d)
            tlist.append(x)
        if (len(tlist) > 0):
            return tlist,str(symbol)
        else:
            return None,str(symbol)

    def clean(self,data):
        pass


    def __parser_search_text_unit(self, unit):
        id = unit.get("id", "")
        uid = unit.get("user_id","")
        title = unit.get("title", "")
        text = unit.get("text", "")
        create_time = unit.get("created_at", "")
        retweet_count = unit.get("retweet_count","")
        reply_count = unit.get("reply_count","")
        fav_count = unit.get("fav_count","")
        retweet_id = unit.get("retweet_id","")
        type = unit.get("type","")
        source_link = unit.get("source_link","")
        edited_at = unit.get("edited_at","")
        pic = unit.get("pic","")
        target = unit.get("target","")
        source = unit.get("source","")
        x = (id,uid,title,text,create_time,retweet_count,reply_count,fav_count,retweet_id,type,source_link,edited_at,pic,target,source)
        return x



xq_search = Search()

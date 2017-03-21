# -*- coding: utf-8 -*-

"""
Created on 201601015

@author kerry
"""

from analysis.base.urlparse_ext import URLParseExt
import json

class Member():

    def member_max(self, content):
        try:
            url = content.get('url')
            if url is None:
                return None,None

            turl = URLParseExt(url)
            uid = turl.get_query_value('uid')
            data = content['data']
            if data is None:
                return None, None
            t = json.loads(data)
            max_page = t.get('maxPage', None)
            if max_page is None:
                return None, None
            return uid, max_page
        except Exception, e:
            return None, None
        except Exception, e:
            return None, None

    def member_userinfo(self, data):
        tlist = []
        jobj = json.loads(data)
        try:
            if (jobj.has_key("error_code")):
                return None
            dlist = jobj.get("users", "")
            for d in dlist:
                x = self.__member_userinfo_unit(d)
                tlist.append(x)
            if (len(tlist) > 0):
                return tlist
            else:
                return None
        except Exception,e:
            return None

    def __member_userinfo_unit(self, unit):
        st_color = unit.get("st_color")
        domain = unit.get("domain")
        type = unit.get("type")
        stock_status_count = unit.get("stock_status_count")
        recommend = unit.get("recommend")
        location = unit.get("location")
        description = unit.get("description")
        verified = unit.get("verified")
        id = unit.get("id")
        status = unit.get("status")
        profile = unit.get("profile")
        screen_name = unit.get("screen_name")
        step = unit.get("step")
        allow_all_stock = unit.get("allow_all_stock")
        blog_description = unit.get("blog_description")
        city = unit.get("city")
        gender = unit.get("gender")
        followers_count = unit.get("followers_count")
        friends_count = unit.get("friends_count")
        status_count = unit.get("status_count")
        province = unit.get("province")
        url = unit.get("url")
        verified_description = unit.get("verified_description")
        verified_type = unit.get("verified_type")
        stocks_count = unit.get("stocks_count")
        intro = unit.get("intro")
        name = unit.get("name")
        profile_image_url = unit.get("profile_image_url")
        name_pinyin = unit.get("name_pinyin")
        screenname_pinyin = unit.get("screenname_pinyin")
        photo_domain = unit.get("photo_domain")
        verified_realname = unit.get("verified_realname")
        cube_count = unit.get("cube_count")
        x = (id, screen_name, gender,province, description, location, city, intro, name, st_color,domain, type, stock_status_count,recommend,
             status,profile,step,allow_all_stock,cube_count,blog_description,followers_count,friends_count,status_count,url,verified,verified_description,
             verified_type,verified_realname,stocks_count,profile_image_url,name_pinyin,screenname_pinyin,photo_domain)
        return x


xq_memeber = Member()
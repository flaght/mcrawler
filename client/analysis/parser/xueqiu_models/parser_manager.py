# -*- coding: utf-8 -*-

"""
Created on 201601015

@author kerry
"""

import json
import icu

from analysis.parser.xueqiu_models.search import xq_search
from analysis.parser.xueqiu_models.user_timeline import xq_usertimeline
from analysis.base.mlog import mlog


class XueQiuParser:
    def __init__(self):
        self.dbname = "xueqiu.db"
        self.logic_selector = {60006: self.__search_event,
                               599: self.__get_uid_crawler}

    def parse(self, parse_id, content):
        pid = content.get('pid')
        if pid is None:
            pid = 60006

        scheduler = self.logic_selector[int(pid)]
        if scheduler:
            return scheduler(content)
        return None


    def __get_uid(self,content):
        dict = {}
        for key in content:
            mlog.log().info("tabel name %s content %d",key, len(content[key]))
            for t in content[key]:
                uid = t[1]
                dict[uid] = uid
        return dict



    def __get_uid_crawler(self, content):
        uid, max_page = xq_usertimeline.cralw_info(content)
        if uid is None or max_page is None:
            return None
        try:
            pid = content['pid']
        except Exception, e:
            pid = 0
        return {'uid':uid,'max_page':max_page,'pid':pid}

    def __search_event(self,content):
        result_list,symbol = xq_search.parser(content['data'])
        if symbol is None or result_list is None:
            return None

        return {'key':symbol, 'result':result_list}



    """
    def parser_search(self, content):
        prefix = "discuss"
        data = ""
        jobj = json.loads(content)
        if (jobj.has_key("error_code")):
            return None, None
        symbol = jobj.get("symbol", "")
        count = jobj.get("page", "")
        dlist = jobj.get("list", "")

        #print xqdb.crate_searcg_sql(symbol)

        for d in dlist:
            data += self.__parser_search_list_unit(d)
        return prefix + '/' + str(symbol) + '/', str(count), data



    def __parser_search_text_unit(self, unit):
        id = unit.get("id", "")
        user_id = unit.get("user_id","")
        create_time = unit.get("created_at", "")
        title = unit.get("title", "")
        text = unit.get("text", "")
        return "{0},{1},{2},{3},{4}".format(str(id),
                                                str(user_id), str(create_time), str(title), str(text))

    def __parser_search_list_unit(self, unit):
        data = ""
        data += self.__parser_search_text_unit(unit)
        if unit.get("retweeted_status", "") <> None:
            data += ","
            data += self.__parser_search_text_unit(unit.get("retweeted_status", ""))
        data += "\r\n"
        return data

    """

def main():
    """

    Returns:

    """
    file_object = open('/Users/kerry/work/test.txt')
    try:
        all_the_text = file_object.read()
    finally:
        file_object.close()

    xueqiu = XueQiuParser()
    xueqiu.parser_search(all_the_text)


if __name__ == '__main__':
    main()

XQ_parser = XueQiuParser()

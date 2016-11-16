# -*- coding: utf-8 -*-

import json
import icu

from parser.xueqiu_models.search import xq_search
from db.xueqiu import XueQiu as  xqdb
"""
Created on 201601015

@author kerry
"""


class XueQiuParser:
    def __init__(self):
        #self.sqlite_manager = SQLLiteStorage("xueqiu.db",0)
        self.dbname = "xueqiu.db"

    def parse(self, parse_id, content):
        return self.__search_event(content)

    def __search_event(self,content):
        result_list,symbol = xq_search.parser(content)
        if symbol is None or result_list is None:
            return None

        return {"code":1,"dbname":self.dbname ,"name_table":xqdb.crate_search_sql(symbol),"sql_formate":xqdb.save_search_format(symbol),"result":result_list}

        #name_table = xqdb.crate_search_sql(symbol)
        #self.sqlite_manager.create_table(name_table,1)
        #if result_list is not None:
          #  self.sqlite_manager.save_data(xqdb.save_search_format(symbol),result_list)
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

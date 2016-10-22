# -*- coding: utf-8 -*-

import json
import icu
from bs4 import BeautifulSoup

"""
Created on 201601015

@author kerry
"""


class XueQiuParser:
    def __init__(self):
        pass

    def parser_search(self, content):
        """

        Returns:
            object:
        """
        prefix = "discuss"
        data = ""
        jobj = json.loads(content)
        if (jobj.has_key("error_code")):
            return None, None
        symbol = jobj.get("symbol", "")
        count = jobj.get("page", "")
        dlist = jobj.get("list", "")
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

xq_parser = XueQiuParser()

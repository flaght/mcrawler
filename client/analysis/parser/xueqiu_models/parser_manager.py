# -*- coding: utf-8 -*-

"""
Created on 201601015

@author kerry
"""

import json
import icu

from analysis.parser.xueqiu_models.common import xq_common
from analysis.parser.xueqiu_models.search import xq_search
from analysis.parser.xueqiu_models.user_timeline import xq_usertimeline
from analysis.base.mlog import mlog


class XueQiuParser:
    def __init__(self):
        self.dbname = "xueqiu.db"
        self.logic_selector = {60006: self.__search_event,
                               599: self.__get_uid_crawler,
                               -599: self.__get_uid,
                               -600: self.__clean_search_event}

    def parse(self, parse_id, content):
        pid = content.get('pid')
        if pid is None:
            pid = 60006

        scheduler = self.logic_selector[int(pid)]
        if scheduler:
            return scheduler(content)
        return None

    """
    提取讨论区里用户的id
    """

    def __get_uid(self,content):
        dict = {}
        data = content.get('dict')
        for key in data:
            mlog.log().info("tabel name %s content %d",key, len(data[key]))
            for t in data[key]:
                uid = t[1]
                dict[uid] = uid
        return {'pid':-599, 'result':dict}


    """
    每个用户对应的讨论数
    """

    def __get_uid_crawler(self, content):
        uid, max_page = xq_usertimeline.cralw_info(content)
        if uid is None or max_page is None:
            return None
        try:
            pid = content['pid']
        except Exception, e:
            pid = 0
        return {'uid':uid,'max_page':max_page,'pid':pid}

    """
    每支股票对应的讨论信息
    """

    def __search_event(self,content):
        result_list,symbol = xq_search.parser(content['data'])
        if symbol is None or result_list is None:
            return None

        return {'key':symbol, 'result':result_list}


    """
    清洗数据
    """

    def __clean_search_event(self,content):
        dt = {}
        d = content['dict']
        for key, value in d.items():
            lt = []
            for t in value:
                replpy = xq_common.quote_format(t[3])
                l = list(t)
                s = json.dumps(replpy)
                l.append(s.decode('unicode-escape'))
                lt.append(l)
            dt[key] = lt
        return {'pid':600,'result':dt}

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

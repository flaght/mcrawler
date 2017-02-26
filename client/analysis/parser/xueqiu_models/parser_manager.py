# -*- coding: utf-8 -*-

"""
Created on 201601015

@author kerry
"""

import json

from analysis.parser.xueqiu_models.search import xq_search
from analysis.parser.xueqiu_models.member import xq_memeber
from analysis.parser.xueqiu_models.discussion import Discussion
from analysis.parser.xueqiu_models.user_timeline import xq_usertimeline
from analysis.comm_opercode import net_task_opercode,local_task_opercode
from analysis.base.mlog import mlog


class XueQiuParser:
    def __init__(self):
        self.dbname = "xueqiu.db"
        self.logic_selector = {60006: self.__search_event,
                               net_task_opercode.XUEQIU_GET_STOCK_DISCUSSION : self.__search_event,
                               net_task_opercode.XUEQIU_GET_PERSONAL_TIMELINE_COUNT: self.__get_uid_crawler,
                               net_task_opercode.XUEQIU_GET_ALL_MEMBER: self.__get_member_userinfo,
                               net_task_opercode.XUEQIU_GET_FLLOWER_COUNT:self.__get_member_max,
                               local_task_opercode.XUEQIU_GET_DISCUSSION_UID: self.__get_uid,
                               local_task_opercode.XUEQIU_DISCUSSION: self.__clean_search_event,
                               local_task_opercode.XUEQIU_GET_MEMBER_MAX: self.__get_uid_member_max}

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
        return {'pid':local_task_opercode.XUEQIU_GET_DISCUSSION_UID, 'result':dict}


    """
    提取用户的最大关注人数
    """
    def __get_uid_member_max(self, content):
        dict = {}
        data = content.get('dict')
        for key in data:
            for t in data[key]:
                uid = t[0]
                max_page = t[1]
                dict[uid] = {'uid':uid,'max_page':max_page}
        return {'pid':local_task_opercode.XUEQIU_GET_MEMBER_MAX, 'result':dict}

    """
    解析用户关注的每个用户信息
    """
    def __get_member_userinfo(self, content):
        result_list = xq_memeber.member_userinfo(content['data'])
        if result_list is None:
            return None
        try:
            pid = content['pid']
        except Exception, e:
            pid = 0
        return {'result':result_list,'pid':pid}

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
    每个用户对应关注用户数量
    """
    def __get_member_max(self,content):
        lt = []
        uid, max_page = xq_memeber.member_max(content)
        if uid is None or max_page is None:
            return None
        try:
            pid = content['pid']
            l = (uid,pid,max_page)
            lt.append(l)
        except Exception, e:
            pid = 0
        return {'result':lt,'pid':pid}

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
                #replpy = xq_common.quote_format(t[3])
                try:
                    dic = Discussion()
                    reply = dic.parser_int(t[3])
                    l = list(t)
                    s = json.dumps(reply)
                    l.append(s.decode('unicode-escape'))
                    lt.append(l)
                except Exception, e:
                    mlog.log().error("https://xueqiu.com/" + str(t[1]) + "/" + str(t[0]))
            dt[key] = lt
        return {'pid':net_task_opercode.XUEQIU_GET_MEMBER_COUT,'result':dt}




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

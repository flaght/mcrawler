# -*- coding: utf-8 -*-

"""
Created on 201705023

@author kerry
"""
from analysis.comm_opercode import net_task_opercode,local_task_opercode
from analysis.parser.sina_modules.weibo_index import sina_weibo_index

class SinaParser(object):

    def __init__(self):
        self.logic_selector = {
            net_task_opercode.SINA_WEIBO_INDEX:self.__five_weibo_index
        }


    def parse(self, parse_id, content):
        pid = content.get('pid')
        scheduler = self.logic_selector[int(pid)]
        if scheduler:
            return scheduler(content)
        return None

    def __five_weibo_index(self,content):
        pid = content['pid']
        index,data = sina_weibo_index.five_star_index(content)
        return {'result':data,'index':index,'pid':pid,'type':1} # 传输到计算平台上,进行区分。1,明星微博热度指数


Sina_parser = SinaParser()
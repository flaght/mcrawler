# -.- coding:utf-8 -.-
"""
Created on 2015年10月30日

@author: chenyitao
"""

import threading
import time

from lxml import html
from lxml.html import HtmlElement

from scheduler.analysis_models.analysis_base import AnalysisBase


class ModelManagerBase(threading.Thread):
    """
    平台模块管理基类
    start()启动
    """
    platform_id = 0

    def __init__(self, finished_callback=None):
        """
        Constructor
        """
        threading.Thread.__init__(self)
        self.finished_callback = finished_callback
        self.wait_queue = []
        self.is_stop = False
        self.rule_sort_list = []
        self.models_selector = {}
        self.reg_models()
        self.reg_rule_list()

    def set_models_selector(self, key, value):
        if key in self.models_selector.keys():
            self.models_selector[key].append(value)
        else:
            self.models_selector[key] = [value]

    def reg_rule_list(self):
        pass

    def set_rule_sort_list(self, rule):
        if rule not in self.rule_sort_list:
            self.rule_sort_list.append(rule)

    def add_task(self, **task):
        if task:
            self.wait_queue.append(task)

    def run(self):
        while not self.is_stop:
            if len(self.wait_queue):
                task = self.wait_queue.pop(0)
                try:
                    self.__dispatch(**task)
                except Exception, e:
                    print 'analyzing error:%s' % e
            else:
                time.sleep(0.5)

    def match_type_tag(self, tag):
        return tag

    def __dispatch(self, **task):
        tag, rule = self.get_tag(task['content'])
        print tag, rule
        if tag:
            tag = self.match_type_tag(tag)
            tag_list = self.models_selector[rule]
            model_cls = None
            for tag_dic in tag_list:
                if tag in tag_dic.keys():
                    model_cls = tag_dic[tag]
                if model_cls:
                    print model_cls.__name__
                    try:
                        model_cls(self.analyzed, **task)
                        self.is_stop = True
                    except Exception, e:
                        print e
                        self.analyzed()
                    return
            for tag_dic in tag_list:
                if AnalysisBase.default_analysis_model in tag_dic.keys():
                    model_cls = tag_dic[AnalysisBase.default_analysis_model]
                    print model_cls.__name__
                    try:
                        model_cls(self.analyzed, **task)
                        self.is_stop = True
                    except Exception, e:
                        print e
                        self.analyzed()
                else:
                    print '无对应解析规则=>'
                    #                 self.is_stop = True
                    self.analyzed()
                    break
        else:
            #             print task['content']
            print '无对应解析规则'
            #             self.is_stop = True
            self.analyzed()

    def reg_models(self):
        """
        子模块注册（子类需重写）
        """
        pass

    def analyzed(self, **params):
        """
        解析完成（子类需重写并在最后调用）
        """
        self.is_stop = True
        if self.finished_callback:
            self.finished_callback(**params)

    def get_tag(self, data):
        """
        解析当前页面，获取唯一标识
        """
        rule = None
        try:
            doc = html.fromstring(data)
        except:
            print 'fromstring error'
            return None, None
        if len(self.rule_sort_list):
            rule_list = self.rule_sort_list
        else:
            rule_list = self.models_selector.keys()
        for rule in rule_list:
            try:
                value = doc.xpath(rule)
            except Exception, e:
                print 'html error:'
                print e
                return None, rule
            if len(value):
                if value[0].__class__ == HtmlElement:
                    tag = value[0].text.encode('utf-8')
                else:
                    tag = str(value[0])
                return tag, rule
        return None, rule

    @staticmethod
    def rules_clash():
        """
        出现多条解析规则都能提取tag时调用，子类需重写
        """
        rule = None
        return rule

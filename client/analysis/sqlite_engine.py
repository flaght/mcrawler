# -.- coding:utf-8 -.-
"""
Created on 2016年11月18日

@author: kerry
"""
from analysis.base.sqlite_ext import SQLiteExt


class SQLiteEngine:

    def __init__(self):
        self.sqlite_mgr = None

    def connect(self,name):
        self.sqlite_mgr = SQLiteExt(name, 0)

    def __del__(self):
        pass

    def __get_data(self,sql,list):
        self.sqlite_mgr.fetch(sql,list)

    def __get_tables(self, sql, list):
        self.sqlite_mgr.fetch(sql, list)

    def fetch_data(self, table=None,other=None): # 若未指定table 则是获取所有数据
        if table is not None:
            sql = "SELECT name FROM sqlite_master WHERE type='table' order by name"
            result_queue = self.__get_tables(sql)



# -.- coding:utf-8 -.-
"""
Created on 2016年11月18日

@author: kerry
"""
from analysis.base.sqlite_ext import SQLiteExt
import icu

class SQLiteStorage:

    def __init__(self, name, type, timeout = 5):
        self.engine =SQLiteExt(name, type, timeout)
        self.name = name
        self.wait_queue = []


    def get_data(self, table):
        return self.engine.fetch(table)

    def get_table(self):
        sql = "select name from sqlite_master where type='table' order by name"
        return self.engine.fetch(sql)
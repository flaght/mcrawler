# -*- coding: utf-8 -*-

"""
Created on 2016年12月19日

@author: kerry
"""


class HeXun:

    @classmethod
    def create_stock_day_heat(cls, table):
        sql = '''CREATE TABLE `''' + table + '''`(
                    `date` VARCHAR(128) NULL,
                    `count` INT NULL,
                     PRIMARY KEY (`date`));'''
        return sql

    @classmethod
    def save_stock_day_heat(cls,table):
        sql = '''INSERT INTO `''' + table + '''` values (?, ?)'''
        return sql

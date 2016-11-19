# -*- coding: utf-8 -*-
"""
Created on 20161106

@author kerry
"""

class XueQiu:

    database = "xueqiu.db"

    @classmethod
    def build_table_name(cls, dict):
        return dict['content']['key']

    @classmethod
    def create_search_sql(cls,table):
        sql = '''CREATE TABLE `''' + table + '''`(
                    `id` BIGINT NOT NULL,
                    `uid` BIGINT NULL,
                    `title` VARCHAR(128) NULL,
                    `text` VARCHAR(40960) NULL,
                    `created_at` INT NULL,
                    `retweet_count` INT NULL,
                    `reply_count` INT NULL,
                    `fav_count` INT NULL,
                    `retweet_id` INT NULL,
                    `type` INT NULL,
                    `source_link` VARCHAR(256),
                    `edited_at` INT NULL,
                    `pic` VARCHAR(256) NULL,
                    `target` VARCHAR(256) NULL,
                    `source` VARCHAR(256) NULL,
                    PRIMARY KEY (`id`));'''
        return sql


    @classmethod
    def save_search_format(cls,table):
        sql = '''INSERT INTO `''' + table + '''` values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        return sql






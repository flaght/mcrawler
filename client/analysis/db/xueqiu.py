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
    def create_member_max(cls,table):
        sql = '''CREATE TABLE `''' + table + '''`(
                    `uid` BIGINT NOT NULL,
                    `pid` INT NOT NULL,
                    `max_page` BIGINT NOT NULL,
                     PRIMARY KEY (`uid`));'''
        return sql


    @classmethod
    def create_member_sql(cls,table):
        sql = '''CREATE TABLE `''' + table + '''`(
                    `id` BIGINT NOT NULL,
                    `screen_name` VARCHAR(256) NULL,
                    `gender` VARCHAR(256) NULL,
                    `province` VARCHAR(256) NULL,
                    `description` VARCHAR(256) NULL,
                    `location` VARCHAR(256) NULL,
                    `city` VARCHAR(256) NULL,
                    `intro` VARCHAR(256) NULL,
                    `name` VARCHAR(256) NULL,
                    `st_color` VARCHAR(256) NULL,
                    `domain` VARCHAR(256) NULL,
                    `type` VARCHAR(256) NULL,
                    `stock_status_count` VARCHAR(256) NULL,
                    `recommend` VARCHAR(256) NULL,
                    `status` INT NULL,
                    `profile` VARCHAR(256) NULL,
                    `step` VARCHAR(256) NULL,
                    `allow_all_stock` VARCHAR(256) NULL,
                    `cube_count` INT NULL,
                    `blog_description` VARCHAR(1024) NULL,
                    `followers_count` INT NULL,
                    `friends_count` INT NULL,
                    `status_count` INT NULL,
                    `url` VARCHAR(256) NULL,
                    `verified` VARCHAR(256) NULL,
                    `verified_description` VARCHAR(256) NULL,
                    `verified_type` VARCHAR(256) NULL,
                    `verified_realname` VARCHAR(256) NULL,
                    `stocks_count` INT NULL,
                    `profile_image_url` VARCHAR(256) NULL,
                    `name_pinyin` VARCHAR(256) NULL,
                    `screenname_pinyin` VARCHAR(256) NULL,
                    `photo_domain` VARCHAR(256) NULL,
                    PRIMARY KEY (`id`));'''
        return sql

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
    def create_clean_search_sql(cls,table):
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
                    `clean_data` VARCHAR(40960) NULL,
                     PRIMARY KEY (`id`));'''
        return sql

    @classmethod
    def create_crawl_uid_sql(cls, table):
        sql = '''CREATE TABLE `''' + table + '''`(
                    `uid` BIGINT NOT NULL,
                    `max_page` BIGINT NOT NULL,
                     PRIMARY KEY (`uid`));'''
        return sql



    @classmethod
    def save_member_format(cls,table):
        sql = '''INSERT INTO `''' + table + ('` values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?\n'
                                             '        , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
        return sql

    @classmethod
    def save_search_format(cls,table):
        sql = '''INSERT INTO `''' + table + '''` values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        return sql

    @classmethod
    def save_search_clean_format(cls,table):
        sql = '''INSERT INTO `''' + table + '''` values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        return sql

    @classmethod
    def save_member_max(cls, table):
        sql = '''INSERT INTO `''' + table + '''` values (?, ?, ?)'''
        return sql


    @classmethod
    def save_crawl_format(cls, table):
        sql = '''INSERT INTO `''' + table + '''` values (?, ?)'''
        return sql

    @classmethod
    def get_id(cls, table):
        sql = '''SELECT id, uid, title, text, created_at,
                    retweet_count, reply_count, fav_count,
                    retweet_id, type, source_link, edited_at,
                    pic, target, source FROM `''' + table + '''`'''
        return sql

    @classmethod
    def get_member_max(cls, table):
        sql = '''select uid,max_page from   `''' + table + '''`'''
        return sql







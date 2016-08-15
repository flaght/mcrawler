# -*- coding: utf-8 -*-

import json
import time
import datetime

from bs4 import BeautifulSoup

"""
Created on 20160812

@author rotciv
"""


class HeXunParser:
    def __init__(self):
        pass

    @staticmethod
    def market_15(content):
        soup = BeautifulSoup(content, 'xml')
        result = {}
        stock_list = []
        for item in soup.find_all("Item"):
            values = {}
            time_str = item['d']
            time_minute = time_str.split()[1]
            number = int(item['v'])
            timestamp = int(time.mktime(datetime.datetime.strptime(time_str.encode("utf8"), "%Y年%m月%d日 %H:%M")
                                        .timetuple()))
            values['time'] = time_minute
            values['vcount'] = number
            values['unixtime'] = timestamp
            stock_list.append(values)
        result['list'] = stock_list
        return json.dumps(result)

    @staticmethod
    def market_total(content):
        soup = BeautifulSoup(content, 'xml')
        result = {}
        stock_list = []
        for item in soup.find_all("Item"):
            values = {}
            time_str = item['d']
            number = int(item['v'])
            values['time'] = time_str
            values['vcount'] = number
            stock_list.append(values)
        result['list'] = stock_list
        return json.dumps(result)

    @staticmethod
    def stock_15(content):
        soup = BeautifulSoup(content, 'xml')
        result = {}
        stock_list = []
        stock_code = soup.find("Title")['id']
        for item in soup.find_all("Item"):
            values = {}
            time_str = item['d']
            time_minute = time_str.split()[1]
            number = int(item['v'])
            timestamp = int(time.mktime(datetime.datetime.strptime(time_str.encode("utf8"), "%Y年%m月%d日 %H:%M")
                                        .timetuple()))
            values['time'] = time_minute
            values['vcount'] = number
            values['unixtime'] = timestamp
            stock_list.append(values)
        result['list'] = stock_list
        return json.dumps(result), stock_code

    @staticmethod
    def stock_total(content):
        soup = BeautifulSoup(content, 'xml')
        result = {}
        stock_list = []
        stock_code = soup.find("Title")['id']
        for item in soup.find_all("Item"):
            values = {}
            time_str = item['d']
            number = int(item['v'])
            values['time'] = time_str
            values['vcount'] = number
            stock_list.append(values)
        result['list'] = stock_list
        return json.dumps(result), stock_code



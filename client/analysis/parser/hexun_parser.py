import json

from bs4 import BeautifulSoup

"""
Created on 20160812

@author rotciv
"""


class HeXunParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_xml(content):
        soup = BeautifulSoup(content, 'xml')
        values = {}
        for item in soup.find_all("Item"):
            time_stamp = item['d']
            number = item['v']
            values[time_stamp] = number
        return json.dumps(values)

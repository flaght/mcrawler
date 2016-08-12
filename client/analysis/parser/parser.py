"""
Created on 20160812

@author rotciv
"""
import datetime

from common import ftp_manager
from hexun_parser import HeXunParser


class Parser:
    prefix = "~/text_storage/"

    def __init__(self):
        pass

    @staticmethod
    def parse(parse_id, content):
        path = Parser.prefix
        result = ""
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        ftp_manager_t = ftp_manager.ftp_manager_t
        ftp_manager_t.connect()

        if parse_id == 1:
            result = HeXunParser.parse_xml(content)
            path += "60005/market15/"
        elif parse_id == 2:
            result = HeXunParser.parse_xml(content)
            path += "60005/markettotal/"
        elif parse_id == 3:
            result = HeXunParser.parse_xml(content)
            path += "60005/stock15/"
        elif parse_id == 4:
            path += "60005/stocktotal/"

        ftp_manager_t.write(path + today_str, result)
        ftp_manager_t.close()

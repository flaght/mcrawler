"""
Created on 20160812

@author rotciv
"""
import datetime

from analysis.common import ftp_manager
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
            result = HeXunParser.market_15(content)
            path += "heat/hexun/All/market_min/"
        elif parse_id == 2:
            result = HeXunParser.market_total(content)
            path += "heat/hexun/All/market_day/"
        elif parse_id == 3:
            result, stock_code = HeXunParser.stock_15(content)
            Parser.create_stock_code_dir(stock_code, "text_storage/heat/hexun/everyone/market_min")
            path += "heat/hexun/everyone/market_min/" + stock_code + "/"
        elif parse_id == 4:
            result, stock_code = HeXunParser.stock_total(content)
            Parser.create_stock_code_dir(stock_code, "text_storage/heat/hexun/everyone/market_day")
            path += "heat/hexun/everyone/market_day/" + stock_code + "/"

        ftp_manager_t.write(path + today_str, result)

    @staticmethod
    def create_stock_code_dir(stock_code, path):
        ftp_manager_t = ftp_manager.ftp_manager_t
        ftp_manager_t.connect()
        exist = ftp_manager_t.exist_dir(path, stock_code)
        if not exist:
            ftp_manager_t.mkd(path + "/" + stock_code)

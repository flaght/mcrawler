"""
Created on 20160812

@author rotciv
"""
import datetime
import time

from analysis.common import ftp_manager
from hexun_parser import HeXunParser
from base.analysis_conf_manager import analysis_conf
import MySQLdb

conn = MySQLdb.connect(host=analysis_conf.mysql_info['host'], user=analysis_conf.mysql_info['username'],
                       passwd=analysis_conf.mysql_info['password'])
conn.select_db('crawler')


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
            result = HeXunParser.market_quater(content)
            path += "heat/hexun/All/market_min/"
        elif parse_id == 2:
            result = HeXunParser.market_total(content)
            try:
                cursor = conn.cursor()
                count = cursor.execute("select * from hexun_daily_heat where date=%s" % result[0])
                if count == 0:
                    cursor.execute("insert into hexun_daily_heat (date,heat,time_stamp) values(%s,%d,%ld);" %
                                   (result[0], int(result[1]), long(time.time() * 1000)))
            except Exception as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
            finally:
                cursor.close()
        elif parse_id == 3:
            result, stock_code = HeXunParser.stock_15(content)
            Parser.create_stock_code_dir(stock_code, "text_storage/heat/hexun/everyone/market_min")
            path += "heat/hexun/everyone/market_min/" + stock_code + "/"
        elif parse_id == 4:
            result = HeXunParser.stock_total(content)
            try:
                cursor = conn.cursor()
                count = cursor.execute("select * from hexun_stock_daily_heat where date=%s and code=%s;" % (result[0], result[2]))
                if count == 0:
                    cursor.execute("insert into hexun_stock_daily_heat (date,heat,time_stamp,code) values(%s,%d,%ld,%s);" %
                                  (result[0], int(result[1]), long(time.time() * 1000), result[2]))
            except Exception as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
            finally:
                cursor.close()
        if parse_id == 1 or parse_id == 3:
            ftp_manager_t.write(path + today_str, result)

    @staticmethod
    def create_stock_code_dir(stock_code, path):
        ftp_manager_t = ftp_manager.ftp_manager_t
        ftp_manager_t.connect()
        exist = ftp_manager_t.exist_dir(path, stock_code)
        if not exist:
            ftp_manager_t.mkd(path + "/" + stock_code)

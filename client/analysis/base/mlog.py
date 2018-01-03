# -*- coding: utf-8 -*-

import logging
import datetime
'''
Created on 2014年6月6日

@author: Administrator
'''

class MLog(object):
    """
    classdocs
    """


    def __init__(self,name = "logging"):
        """
        Constructor
        """
        filename = name + datetime.datetime.now().strftime('%b_%d')+'.log'
        #[Tue Nov 15 11:35:53 2016] [notice] Apache/2.2.15 (Unix) DAV/2 PHP/5.3.3 mod_ssl/2.2.15 OpenSSL/1.0.1e-fips configured -- resuming normal operations
        format_str = "[%(process)d %(thread)d][%(asctime)s][%(filename)s line:%(lineno)d][%(levelname)s] %(message)s"
        # define a Handler which writes INFO messages or higher to the sys.stderr
        logging.basicConfig(level=logging.DEBUG,
                            format=format_str,
                            datefmt='%m-%d %H:%M',
                            filename=filename,
                            filemode='a')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(format_str)
        console.setFormatter(formatter)
        # 将定义好的console日志handler添加到root logger
        logging.getLogger('').addHandler(console)


    def log(self):
        #logging.error()
        return logging

mlog = MLog()


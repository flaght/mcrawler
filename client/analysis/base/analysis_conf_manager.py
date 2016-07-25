# -.- coding:utf-8 -.-
'''
Created on 2015年10月9日

@author: chenyitao
'''

import ConfigParser

class AnalysisConfManager(object):
    '''
    classdocs
    '''

    __conf_path = '/etc/kid_conf/analysis/analysis.conf'

    def __init__(self):
        '''
        Constructor
        '''
        self.hbase_info = {}
        self.redis_info = {}
        self.ftp_info = {}
        self.conf_file = ConfigParser.ConfigParser()
        self.conf_file.read(self.__conf_path)
        self.__read_hbase_info()
        self.__read_redis_info()
        self.__read_ftp_info()

    def __read_hbase_info(self):
        '''
        read hbase info
        '''
        host = self.conf_file.get('hbase_info', 'host')
        self.hbase_info['host'] = host
        port = self.conf_file.get('hbase_info', 'port')
        self.hbase_info['port'] = int(port)

    def __read_redis_info(self):
        '''
        read redis info
        '''
        host = self.conf_file.get('redis_info', 'host')
        self.redis_info['host'] = host
        port = self.conf_file.get('redis_info', 'port')
        self.redis_info['port'] = int(port)
        db = self.conf_file.get('redis_info', 'db')
        self.redis_info['db'] = int(db)
        password = self.conf_file.get('redis_info', 'password')
        self.redis_info['password'] = password

    def __read_ftp_info(self):
        '''
        read ftp info
        '''
        host = self.conf_file.get('ftp_info', 'host')
        self.ftp_info['host'] = host
        port = self.conf_file.get('ftp_info', 'port')
        self.ftp_info['port'] = int(port)
        user = self.conf_file.get('ftp_info', 'user')
        self.ftp_info['user'] = user
        passwd = self.conf_file.get('ftp_info', 'passwd')
        self.ftp_info['passwd'] = passwd
        timeout = self.conf_file.get('ftp_info', 'timeout')
        self.ftp_info['timeout'] = int(timeout)

analysis_conf = AnalysisConfManager()

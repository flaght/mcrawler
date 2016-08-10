# -.- coding:utf-8 -.-
"""
Created on 2015年10月27日

@author: chenyitao
"""

from base.analysis_conf_manager import analysis_conf
from schduler.storage.hbase_manage_model import hbase_manager
from schduler.storage.redis_manage_model import redis_manager
from schduler.storage.text_storage import TextStorage


class StorageOpcode(object):
    """
    storage opcode
    """
    redis = 0

    hbase = 1

    mysql = 2

    text = 3

    memcache = 4


storage_opcode = StorageOpcode()


class StorageManager(object):
    """
    class docs
    """

    def __init__(self, params=None):
        """
        Constructor
        """
        ftp_info = analysis_conf.ftp_info
        self.ftp_text_manager = TextStorage(ftp_info['host'],
                                            ftp_info['port'],
                                            ftp_info['user'],
                                            ftp_info['passwd'],
                                            ftp_info['timeout'])
        self.ftp_text_manager.setDaemon(True)
        self.ftp_text_manager.start()
        self.storage_selector = {storage_opcode.redis: self.__storage_to_redis,
                                 storage_opcode.hbase: self.__storage_to_hbase,
                                 storage_opcode.mysql: self.__storage_to_mysql,
                                 storage_opcode.text: self.__storage_to_text,
                                 storage_opcode.memcache: self.__storage_to_text}

    def storage(self, storage_type, cmd_list):
        storage_method = self.storage_selector[storage_type]
        if storage_method:
            storage_method(cmd_list)

    @staticmethod
    def __storage_to_redis(cmd_list):
        """

        """
        for cmd_sentence in cmd_list:
            redis_manager.set_storage_info(cmd_sentence['cmd'],
                                           cmd_sentence['params'])
            redis_manager.commit()

    @staticmethod
    def __storage_to_hbase(self, cmd_list):
        """
        
        """
        for cmd_sentence in cmd_list:
            hbase_manager.write_data(cmd_sentence.pop('table'),
                                     cmd_sentence.pop('key'),
                                     cmd_sentence)

    @staticmethod
    def __storage_to_mysql(self, cmd_list):
        """
        
        """
        pass

    def __storage_to_text(self, cmd_list):
        """

        """
        for cmd_sentence in cmd_list:
            self.ftp_text_manager.upload_data(cmd_sentence['value'],
                                              cmd_sentence['table'],
                                              cmd_sentence['key'])

    @staticmethod
    def __storage_to_memcache(self, cmd_list):
        """
        
        """
        pass


storage_manager = StorageManager()

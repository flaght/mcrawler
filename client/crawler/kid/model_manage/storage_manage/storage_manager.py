# -.- coding:utf-8 -.-
'''
Created on 2015年9月14日

@author: chenyitao
'''

from kid.common import kid_setting
from kid.model_manage.storage_manage.hbase_manager import HbaseManager
from kid.model_manage.storage_manage.text_storage import TextStorage


class StorageManager(object):
    '''
    存储管理
    '''

    def __init__(self):
        '''
        [0] host    [1] port
        '''
        self.hbase_manager = HbaseManager(kid_setting.HBASE_HOST,
                                          kid_setting.HBASE_PORT) 
        self.hbase_state = self.hbase_manager.state
        self.ftp_manager = TextStorage(kid_setting.FTP_HOST,
                                       kid_setting.FTP_PORT,
                                       kid_setting.FTP_UNAME,
                                       kid_setting.FTP_PWD)

    def write_data(self, data, table_path, pid, storage_type=1):
        '''
        write data to hbase
        data: {'basic':{'content':'xx', 'key':'xxx', 'url':'xxxx'}}
        '''
        storage_type = 2
        if storage_type == 1:
            if self.hbase_state:
                ret = self.hbase_manager.put(table_path,
                                             data['basic'].pop('key'),
                                             data)
                if ret != HbaseManager.NoError:
                    return False
                return True
        else:
            self.ftp_manager.upload_data(data['basic']['content'],
                                         table_path, pid,
                                         data['basic']['key'])
            return True


storage_manager = StorageManager()

def main():
    '''
    test
    '''
    storage_manager = StorageManager()
    print storage_manager.read_data('1')

if __name__ == '__main__':
    main()

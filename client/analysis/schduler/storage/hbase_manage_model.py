# -.- coding:utf-8 -.-
'''
Created on 2015年10月9日

@author: chenyitao
'''
import threading
import time

from _cffi_backend import callback
import happybase
from hbase import Hbase
from hbase.ttypes import ColumnDescriptor
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport

from base.analysis_conf_manager import analysis_conf


class HbaseManageModel(threading.Thread):
    '''
    Hbase读写类
    '''

    def __init__(self, host=None, port=None):
        '''
        Constructor
        '''
        threading.Thread.__init__(self, name='hbase')
        self.state = 0
        self.sock = TSocket.TSocket(host, port)
        self.sock.setTimeout(5000)
        self.transport = TTransport.TBufferedTransport(self.sock)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Hbase.Client(self.protocol)
        self.task = []
        try:
#             self.transport.open()
            self.pool = happybase.ConnectionPool(size=1, host=host)
            with self.pool.connection() as connection:
                self.hb = connection
            self.state = 1
        except Exception, e:
            self.transport.close()
            print 'hbase init failed:%s' % e
            return
        print 'hbase init successed'

    def run(self):
        while True:
            if len(self.task):
                task = self.task.pop(0)
                try:
                    data = task['data']
                    callback = task['callback']
                    if task['action'] == 1:
                        self.__write_data(data['table'], data['rowkey'], data['value'], callback)
                    elif task['action'] == 2:
                        self.__get_row(data['table'], data['rowkey'], callback)
                    continue
                except Exception, e:
                    print e
            time.sleep(1)

    def write_data(self, table, key, value, callback=None):
        '''
        write data
        '''
        self.task.append({'action':1,
                          'data':{'table': table, 'rowkey': key, 'value': value},
                          'callback':callback})
        return
        if not self.state:
            return
        self.__create_table(table, value.keys())
        self.__write(table, key, value)

    def __write_data(self, table, key, value, callback=None):
        '''
        write data
        '''
        if not self.state:
            return
        self.__create_table(table, value.keys())
        self.__write(table, key, value)
        if callback:
            callback('finished')

    def read_data(self, table_path, items=None):
        '''
        read data
        '''
        scanner = self.client.scannerOpen(table_path, '', items, None)
        results = self.client.scannerGet(scanner)
        self.client.scannerClose(scanner)
        return results

    def get_row(self, table=None, rowkey=None, callback=None):
        '''
        get row
        '''
        self.task.append({'action':2,
                          'data':{'table': table, 'rowkey': rowkey},
                          'callback':callback})
        return
        if table and rowkey:
            try:
                ret = self.hb.table(table).row(rowkey)
                return ret
            except Exception, e:
                print 'err:',e
            return None
            try:
                ret = self.client.getRow(table, rowkey, None)
                return ret
            except Exception, e:
                print 'error : table:%s rowkey:%s err:%s' % (table, rowkey, e)
                return None
        else:
            print 'get row error'
            return None

    def __get_row(self, table=None, rowkey=None, callback=None):
        '''
        get row
        '''
        if table and rowkey:
            try:
                ret = self.hb.table(table).row(rowkey)
                if callback:
                    callback(ret)
#                 return ret
            except Exception, e:
                print 'err:',e
            return None
            try:
                ret = self.client.getRow(table, rowkey, None)
                return ret
            except Exception, e:
                print 'error : table:%s rowkey:%s err:%s' % (table, rowkey, e)
                return None
        else:
            print 'get row error'
            return None

    def __create_table(self, table, columns_name):
        '''
        create table
        '''
#         tables = self.client.getTableNames()
        tables = self.hb.tables()
        if table not in tables:
            cols = []
            for column_name in columns_name:
                col = ColumnDescriptor(name='%s:'%column_name, maxVersions=1)
                cols.append(col)
                f = column_name
#             self.client.createTable(table, cols)
            self.hb.create_table(table, f)

    def __write(self, table, key, value):
        '''
        write
        '''
#         mutations = []
        data = {}
        key = str(key)
        for f in value.keys():
            values = value[f]
            for c in values.keys():
#                 mutation = Mutation(column='%s:%s' % (f, c), value=values[c])
                fkey = '%s:%s' % (f, c)
                data[fkey] = values[c]
#                 mutations.append(mutation)
#         self.client.mutateRow(table, key, mutations, None)
        self.hb.table(table).put(key, data)
        
    def __del__(self):
        '''
        del
        '''
        self.transport.close()

hbase_manager = HbaseManageModel(analysis_conf.hbase_info['host'],
                                 analysis_conf.hbase_info['port'])
hbase_manager.setDaemon(True)
hbase_manager.start()

def main():
    '''
    test
    '''
    hm = HbaseManageModel('192.168.0.2', 9090)
    print hm.read_data('t.10jqka.com.cn', ['content:'])
    row_data = hm.get_row('t.10jqka.com.cn', 'ebc3415a0d7700964dd9e3eaa9b93549')
    print row_data
    for row in row_data:
        print row.columns.get('content:').value

if __name__ == '__main__':
    main()

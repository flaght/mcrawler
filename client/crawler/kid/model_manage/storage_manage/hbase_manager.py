# -.- coding:utf-8 -.-
'''
Created on 2015年10月9日

@author: chenyitao
'''
import threading
import time
from hbase import Hbase
from hbase.ttypes import ColumnDescriptor
from hbase.ttypes import Mutation
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport
from kid.common.common_method import print_plus

class HbaseManager(object):
    '''
    Hbase Manager
    '''
    NoError = -1
    ConnectError = 0
    CreateError = 1
    PutError = 2
    GetError = 3
    ParamsError = 4

    def __init__(self, host=None, port=None, timeout=15000):
        '''
        Constructor
        '''
        self.sock = TSocket.TSocket(host, port)
        self.sock.setTimeout(timeout)
        self.transport = TTransport.TBufferedTransport(self.sock)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Hbase.Client(self.protocol)
        try:
            self.transport.open()
            self.state = 1
            self.tables = self.client.getTableNames()
            print_plus(content='HBase Init Succssed')
        except:
            self.state = 0
            print_plus(content='HBase Init Failed', level=1)
        finally:
            self.connection_check_thread = threading.Thread(target=self.__hbase_daemon,
                                                            name='hbase_daemon')
            self.connection_check_thread.setDaemon(True)
            self.connection_check_thread.start()

    def put(self, table, key, value):
        '''
        put data to hbase
        '''
        if not self.state:
            return HbaseManager.ConnectError
        ret = self.__create_table(table, value.keys())
        if ret != HbaseManager.NoError:
            return ret
        ret = self.__put(table, key, value)
        if ret != HbaseManager.NoError:
            return ret
        return HbaseManager.NoError

    def get(self, table=None, rowkey=None):
        '''
        get row
        '''
        if not self.state:
            return HbaseManager.ConnectError
        if table and rowkey:
            try:
                return self.client.getRow(table, rowkey, None)
            except Exception,e:
                print_plus(content='GetRowExcept: table:%s  %s' % (table, e), level=1)
                return HbaseManager.GetError
        else:
            print_plus(content='get row error', level=1)
            return HbaseManager.ParamsError

    def __create_table(self, table, columns_name):
        '''
        create table
        '''
        try:
            if table not in self.tables:
                self.tables = self.client.getTableNames()
            if table not in self.tables:
                cols = []
                for column_name in columns_name:
                    col = ColumnDescriptor(name='%s:'%column_name, maxVersions=1)
                    cols.append(col)
                try:
                    self.client.createTable(table, cols)
                except Exception,e:
                    print_plus(content=e, level=1)
                    return HbaseManager.CreateError
        except Exception, e:
            print_plus(content=e, level=1)
            return HbaseManager.ConnectError
        return HbaseManager.NoError

    def __put(self, table, key, value):
        '''
        write
        '''
        mutations = []
        for f in value.keys():
            values = value[f]
            for c in values.keys():
                mutation = Mutation(column='%s:%s' % (f, c), value=values[c])
                mutations.append(mutation)
        try:
            self.client.mutateRow(table, key, mutations, None)
            print_plus(content='write to hbase success: %s<=>%s' % (table, key))
        except Exception,e:
            print_plus(content=e, level=1)
            return HbaseManager.PutError
        return HbaseManager.NoError

    def __hbase_daemon(self):
        cnt = 0
        while True:
            if cnt >= 5:
                try:
                    self.client.getTableNames()
                except Exception, e:
                    print_plus(content='Hbase Check Alive Failed', level=1)
                    print_plus(content=e, level=1)
                    self.__reconnect_hbase()
                finally:
                    cnt = 0
            else:
                cnt += 1
                time.sleep(1)

    def __reconnect_hbase(self):
        self.transport.close()
        try:
            self.transport.open()
            self.state = 1
            print_plus(content='HBase Init Succssed')
        except Exception, e:
            print_plus(content='HBase Init Failed', level=1)
            print_plus(content=e, level=1)
            self.state = 0

    def __del__(self):
        '''
        del
        '''
        self.transport.close()

def main():
    '''
    test
    '''
    hm = HbaseManager('222.73.57.3', 9090)
#     task_info = (59, 553, 6, 140162634135544, 3, 1, 0, 1, 0, 0, 1, 2, 'http://www.10jqka.com.cn/')
    item = {'basic':{}}
    item['basic']['url'] = 'this a url'
    item['basic']['key'] = '19921028'
    item['basic']['content'] = 'this a content'
    hm.put('slmtablename', '19921029', item)
    data = hm.get('slmtablename', '19921029')
#     hm.start()
    print data
    while True:
        time.sleep(1)
    '''
    row_data = hm.get_row('htmlcontent', 'http://futures.eastmoney.com/news/1765,20160207593542255.html')
    if row_data:
        for row in row_data:
            data = row.columns.get('basic:content').value
            from lxml import html
            doc = html.fromstring(data)
            print doc
            
    else:
        print row_data
    '''
    
if __name__ == '__main__':
    main()

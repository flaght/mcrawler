# -.- coding:utf-8 -.-
'''
Created on 2015年10月9日

@author: chenyitao
'''
from hbase import Hbase
from hbase.ttypes import ColumnDescriptor
from hbase.ttypes import Mutation
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport
from kid.common.common_method import print_plus


class HbaseManageModel(object):
    '''
    Hbase读写类
    '''

    def __init__(self, host=None, port=None, timeout=15000):
        '''
        Constructor
        '''
        self.state = 0
        self.transport = TSocket.TSocket(host, port)
        self.transport.setTimeout(timeout)
        self.transport = TTransport.TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Hbase.Client(self.protocol)
        try:
            self.transport.open()
            self.state = 1
            print_plus('HBase Init Succssed')
        except:
            print_plus('HBase Init Failed', level=1)

    def write_data(self, table, key, value):
        '''
        write data
        '''
        if not self.state:
            return
        if not self.transport.isOpen():
            self.transport.open()
        self.__create_table(table, value.keys())
        self.__write(table, key, value)

    def read_data(self, table_path, items=None):
        '''
        read data
        '''
        if not self.state:
            return None
        scanner = self.client.scannerOpen(table_path, '', items, None)
        results = self.client.scannerGet(scanner)
        self.client.scannerClose(scanner)
        return results

    def get_row(self, table=None, rowkey=None):
        '''
        get row
        '''
        if not self.state:
            return
        if table and rowkey:
            try:
                return self.client.getRow(table, rowkey, None)
            except Exception,e:
                print_plus('GetRowExcept: table:%s  %s' % (table, e), level=2)
        else:
            print_plus('get row error', level=2)

    def __create_table(self, table, columns_name):
        '''
        create table
        '''
        tables = self.client.getTableNames()
        if table not in tables:
            cols = []
            for column_name in columns_name:
                col = ColumnDescriptor(name='%s:'%column_name, maxVersions=1)
                cols.append(col)
            try:
                self.client.createTable(table, cols)
            except Exception,e:
                print e

    def __write(self, table, key, value):
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
            print_plus('write to hbase success: %s<=>%s' % (table, key))
        except Exception,e:
            print_plus(e, level=2)

    def __del__(self):
        '''
        del
        '''
        self.transport.close()

def main():
    '''
    test
    '''
    hm = HbaseManageModel('222.73.34.91', 9090)
#     hm.write_data('pytest', 'k223', {'k1':{'hello':'123', 'world':'456'}})
#     print hm.read_data('pytest', ['v1:', 'v2:'])
    row_data = hm.get_row('htmlcontent', 'http://futures.eastmoney.com/news/1765,20160207593542255.html')
    if row_data:
        for row in row_data:
            data = row.columns.get('basic:content').value
            from lxml import html
            doc = html.fromstring(data)
            print doc
            
    else:
        print row_data

if __name__ == '__main__':
    main()

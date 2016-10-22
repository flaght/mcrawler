# -*- coding:utf-8 -*-
'''
doc
'''
import MySQLdb
from common import setting

class SaveInDatabase(object):
    '''
     把有效的IP存到数据库
    '''
    all_ip_list = []
    def __init__(self, all_ip_list):
        self.all_ip_list = all_ip_list

    def connect_sql(self):
        '''
         连接数据库 插入有效ip信息
        '''
        # 打开数据库连接
        # 192.168.0.2 root crawler hadoop
        # 112.124.49.59 migfm crawler miglab2012
        db_connect = MySQLdb.connect(host=setting.MYSQL_HOST,
                                     user=setting.MYSQL_USER,
                                     db=setting.MYSQL_DB,
                                     passwd=setting.MYSQL_PASSWD)
        #使用cursor()方法获取操作游标
        cursor = db_connect.cursor()
        creat_sql = '''CREATE TABLE crawler_forge_ip (
                       ip  VARCHAR(20) NOT NULL PRIMARY KEY,
                       used INT NOT NULL,
                       type  INT NOT NULL,
                       create_time VARCHAR(20) NOT NULL)'''
        try:
            cursor.execute(creat_sql)
        except:
        # 发生错误时回滚(已存在表)
            db_connect.rollback()
        #清空表数据，重新填写ip
            cursor.execute('delete from crawler_forge_ip where id!=0')
            db_connect.commit()
        cursor.execute('delete from crawler_forge_ip where id!=0')
        inserted_ip = []
        for i in xrange(len(self.all_ip_list)):
            used = self.all_ip_list[i]['used']
            if used == 1:
                ip = self.all_ip_list[i]['ip']
                if ip in inserted_ip:
                    continue
                ip_type = self.all_ip_list[i]['type']
                used = self.all_ip_list[i]['used']
                insert_sql = 'INSERT INTO crawler_forge_ip(ip, used, type, create_time)\
                 VALUES ("%s", %d, %d, now())' % (str(ip), used, ip_type)
                try:
                    cursor.execute(insert_sql)
                    inserted_ip.append(ip)
                except db_connect.IntegrityError:
                    update_sql = 'UPDATE crawler_forge_ip SET used = %d, type = %d, \
                    create_time = now()' % (used, ip_type)
                    cursor.execute(update_sql)
        db_connect.commit()
        cursor.close()
        db_connect.close()
        print '===========finish========'

if __name__ == '__main__':
    ip_list = [{'type':'HTTPS', 'ip':'219.133.31.120:8888',\
                'refuse':0, 'time_out':0, 'used':1},
               {'type':'HTTP', 'ip':'119.253.252.27:3128', \
                'refuse':0, 'time_out':0, 'used':1},
               {'type':'HTTPS', 'ip':'218.200.66.199:80', \
                'refuse':0, 'time_out':0, 'used':1},
               {'type':'HTTP', 'ip':'182.88.231.4:8127', \
                'refuse':0, 'time_out':0, 'used':1},
               {'type':'HTTP', 'ip':'122.96.59.102:83', \
                'refuse':0, 'time_out':0, 'used':1},
               {'type':'HTTP', 'ip':'222.88.236.234:80', \
                'refuse':0, 'time_out':0, 'used':1}]
    SaveInDatabase(ip_list).connect_sql()
    print '==is ok=='


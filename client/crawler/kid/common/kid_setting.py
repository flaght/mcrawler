# -.- coding:utf-8 -.-
'''
Created on 2015-12-25

@author: chenyitao
'''

'''
SOCKET INFO
'''

# socket state
CONNECT=0
# socket host
TEST=0
if TEST == 0:
    SERVER_IP='61.147.114.87'
    SERVER_PORT=15000
    __VER=1
elif TEST == 1:
    SERVER_IP='222.73.34.92'
    SERVER_PORT=16003
    __VER=1
elif TEST == 2:
    SERVER_IP='222.73.34.92'
    SERVER_PORT=17777
    __VER=1
elif TEST == 3:
    SERVER_IP='222.73.34.101'
    SERVER_PORT=15555
    __VER=0
elif TEST == 4:
    SERVER_IP='222.73.34.101'
    SERVER_PORT=16003
    __VER=0
elif TEST == 5:
    SERVER_IP='222.73.34.101'
    SERVER_PORT=17777
    __VER=0


'''
CRAWLER INFO
'''
# crawler type  1:common    2:detail    3:selfstock
CRAWLER_TYPE=1

'''
PROC INFO
'''
__CRAWL_TYPE_NAME = {1:'common', 2:'detail', 3:'selfstock'}
__CRAWL_VER_NAME = {1:'debug', 0:'release'}
__PROC_NAME = __CRAWL_TYPE_NAME[CRAWLER_TYPE] + '_' + __CRAWL_VER_NAME[__VER]
DAEMON_PROC_NAME = __PROC_NAME + '_daemon'
CLIENT_PROC_NAME = __PROC_NAME + '_client'



'''
HBASE INFO
'''
# hbase info
HBASE_NODE=3
__HBASE_DEBUG_NODE = {0:'222.73.57.12',
                      1:'192.168.57.3',
                      2:'222.73.57.7',
                      3:'222.73.57.8',
                      4:'222.73.57.11'}

__HBASE_RELEASE_NODE = {0:'222.73.34.99',
                        1:'222.73.34.95',
                        2:'222.73.34.96',
                        3:'222.73.34.98',
                        4:'222.73.34.103'}

if __VER == 1: # debug
    HBASE_HOST = __HBASE_DEBUG_NODE[HBASE_NODE] 
    HBASE_PORT = 9090
elif __VER == 0: # release
    HBASE_HOST = __HBASE_RELEASE_NODE[HBASE_NODE]
    HBASE_PORT = 9090


'''
FTP INFO
'''
FTP_HOST = '61.147.114.73'
FTP_PORT = 21
FTP_UNAME = 'crawler'
FTP_PWD = '123456x'

'''
DEVICE INFO
'''
DEVICE_LEVEL=5
DEVICE_PASSWD='12345678'
DEVICE_MANAGER_ID=1
DEVICE_MAX_TASK = 300

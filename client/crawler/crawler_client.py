#!/usr/bin/python2
# -.- coding:utf-8 -.-
'''
Created on 2015年9月1日

@author: chenyitao
'''

import socket

from twisted.internet import reactor

from kid.client import KidClientFactory
from kid.common import kid_setting
from kid.common.common_method import print_plus
import setproctitle


def main():
    '''
    启动爬虫客户端
    '''
    setproctitle.setproctitle(kid_setting.CLIENT_PROC_NAME)
    client_factory = KidClientFactory()
    reactor.__init__()  # @UndefinedVariable
    reactor.suggestThreadPoolSize(25) # @UndefinedVariable
    connector = reactor.connectTCP(kid_setting.SERVER_IP, # @UndefinedVariable
                                    kid_setting.SERVER_PORT,
                                   client_factory)
    connector.transport.getHandle().setsockopt(socket.SOL_SOCKET,
                                               socket.SO_SNDBUF,
                                               4096*100)
    print_plus('IP:%s\tPort:%s\tHBase IP:%s\tCrawler Type:%d' % (kid_setting.SERVER_IP,
                                                                 kid_setting.SERVER_PORT,
                                                                 kid_setting.HBASE_HOST,
                                                                 kid_setting.CRAWLER_TYPE))
    reactor.run()  # @UndefinedVariable

if __name__ == '__main__':
    main()

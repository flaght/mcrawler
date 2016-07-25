#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2015年9月29日

@author: kerry
'''

from ctypes.test.test_errno import threading
import os
import struct
import time

from twisted.internet import defer
from twisted.internet import reactor, protocol
from twisted.internet import threads

from base.log import kidlog
from netsvc.packet_processing import PacketHead
from netsvc.resolve import NetData
from schduler.analysis_manage_model.analytical_manager import AnalyticalManager


class KIDBaseSchedulerClient(protocol.Protocol):
    '''
    protocol
    '''
    user = ''
    password = ''

    def __init__(self):
        self.is_alive = False
        self.netdata = NetData()
        self.is_finished = True
        self.send_data_queue = []
        self.analy_mgr = AnalyticalManager()
        self.analy_mgr.network = self
        self.send_thread = threading.Thread(target=self.__send_msg,
                                            name='send')
        self.send_thread.setDaemon(True)
        self.send_thread.start()

    def connectionMade(self):
        kidlog.log().debug("connection success")
        self.is_alive = True
        self.transport.write(self.analy_mgr.Login(6, self.password, self.user))
        self.analy_mgr.feedback = self.feedback_state
        self.analy_mgr.transport = self.transport
        self.heart = threading.Timer(15, self.__heart)
        self.heart.setDaemon(True)
        self.heart.setName('heart')
        self.heart.start()

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        pack_stream, result = self.netdata.net_wok(data)
        kidlog.log().debug("result %d", result)
        if result == 0:
            return
        packet_head = self.analy_mgr.UnpackHead(pack_stream)
        if(int(packet_head.packet_length) - int(packet_head.packet_head_length())
           <> int(packet_head.data_length)):
            kidlog.log().error("packet_length error %d",
                               int(packet_head.packet_length))
            return
        if packet_head.packet_length <= packet_head.packet_head_length():
#             kidlog.log().error("packet_length less packet head %d",
#                                int(packet_head.packet_length))
            return
        if packet_head.operate_code == 100:#心跳包回复
            self.transport.write(pack_stream)
        elif packet_head.operate_code == 1002:
            kidlog.log().debug("operate_code %d", packet_head.operate_code)
            manager_id, token = struct.unpack('=I32s', pack_stream[26:])
            self.analy_mgr.manager_id = manager_id
            self.analy_mgr.token = token
            kidlog.log().debug('id:%d  token:%s', manager_id, token)
        elif packet_head.operate_code == 1030:
            self.analy_mgr.AnalyticalHBaseInfo(pack_stream)

    def connectionLost(self, reason):
        self.is_alive = False
        print "connection lost"

    def feedback_state(self, data):
        '''
        feedback state
        '''
        self.transport.write(data)

    def send_msg(self, data):
        '''
        发送数据
        '''
        self.send_data_queue.append(data)

    def __send_msg(self):
        def finished(param=None):
            self.is_finished = True
        while True:
            if not self.is_finished:
                time.sleep(0.02)
                continue
            if len(self.send_data_queue):
                deferlist = []
                self.is_finished = False
                d = threads.deferToThread(self.transport.write, self.send_data_queue.pop(0))
                deferlist.append(d)
                dl = defer.DeferredList(deferlist)
                dl.addBoth(finished)
            else:
                time.sleep(0.02)

    def __heart(self):
        heart = PacketHead()
        heart.make_head(0, 0, 0, 100, 0, 0)
        heart.packet_length = heart.packet_head_length()
        heart.headstream()
        data = heart.head
        cnt = 0
        while self.is_alive:
            if cnt >= 15:
                self.send_msg(data)
                print '[%s] send heart' % time.strftime('%Y-%m-%d %H:%M:%S')
                cnt = 0
            else:
                cnt += 1
                time.sleep(1)

class KIDBaseSchedulerFactory(protocol.ReconnectingClientFactory):
    '''
    factory
    '''
    def __init__(self, user=None, password=None):
        print "KIDBaseSchedulerFactory:__init__"
        self.protocol = KIDBaseSchedulerClient
        self.protocol.user = user
        self.protocol.password = password

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed"
        time.sleep(15)
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        print "Connection lost"
        time.sleep(15)
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def buildProtocol(self, addr):
        build_protocol = protocol.ClientFactory.buildProtocol(self, addr)
        return build_protocol

class KIDInitialScheduler(object):
    '''
    scheduler
    '''
    def connection(self, host, port, user, password):
        '''
        connection
        因使用进程池
        故工作进程会把主进程的reactor拷贝过来
        reactor在主进程已经运行
        故需要重新初始化 @UndefinedVariable
        '''
        factory = KIDBaseSchedulerFactory(user, password)
        reactor.__init__()  # @UndefinedVariable
        reactor.connectTCP(host, int(port), factory)  # @UndefinedVariable

    def start_run(self):
        '''
        run
        '''
        reactor.run()  # @UndefinedVariable

#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2015年10月6日

@author: kerry
'''

import time
from netsvc.package_manage.login_manager import login_manager
from netsvc.package_manage.state_manager import state_manager
from netsvc.packet_processing import AnalyzedURLInfo, AnalyzedURLs
import netsvc.packet_processing as packet
from schduler.analysis_manage_model.analyzer import Analysiser
from schduler.storage.storage_manage import StorageManager


class AnalyticalManager(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.network = None
        self.feedback = None
        self.transport = None
        self.task_num = 0
        self.manager_id = 0
        self.token = ''
        self.storage_manager = StorageManager()

    def UnpackHead(self, data):
        '''
        unpack head
        '''
        packet_head = packet.PacketHead()
        packet_head.unpackhead(data)
        return packet_head

    def Login(self, level, password, mac):
        '''
        login
        '''
        return login_manager.manager_register(level, mac, password)

    def AnalyticalHBaseInfo(self, data):
        '''
        analytical hbase info
        '''
        analytical_info = packet.AnalyticalInfo()
        analytical_info.unpackstream(data)
        analytical_list = analytical_info.getanalylist()
        if len(analytical_list) > 0:
            for analytical in analytical_list:
                while self.task_num > 8:
                    time.sleep(0.2)
                print "task_id %d attr_id %d key %s name %s" %(analytical.get_task_id(),
                                                               analytical.get_attr_id(),
                                                               analytical.get_key(),
                                                               analytical.get_name())
                if analytical.get_name() == '3':
                    analytical.set_attr_id(3)
                analysis = Analysiser(analytical, self.finished, self.storage_manager)
                self.task_num += 1
                ret = None
                try:
                    ret = analysis.analyze()
                    if ret != Analysiser.err_ok:
                        self.__feedback_analysis_state(analysis.analytical.analysis_id,
                                                       ret)
                        print 'ERR: %d' % ret
                        self.task_num -= 1
                except Exception,e:
                    self.__feedback_analysis_state(analysis.analytical.analysis_id,
                                                   Analysiser.err_exception)
                    print 'ERR: %s' % e
                    self.task_num -= 1

    def finished(self, **kwargs):
        self.task_num -= 1
        analytical = kwargs['analytical']
        self.__feedback_analysis_state(analytical.analysis_id, kwargs['success'])
        url_list = kwargs['url_list']
        if len(url_list):
            self.__feedback_url_list(analytical, url_list)

    def __feedback_analysis_state(self, analysis_id, state):
        '''
        feedback analysis state
        '''
        data = state_manager.set_package_info(analysis_id, state)
        self.network.send_msg(data)

    def __feedback_url_list(self, analytical, url_list):
        '''
        '''
        cnt = 0
        analyzed_urls = None
        print 'urls:%d' % len(url_list)
        for url in url_list:
            if cnt == 0:
                analyzed_urls = AnalyzedURLs()
                analyzed_urls.manage_id = self.manager_id
                analyzed_urls.token = self.token
            analyzed_url_info = AnalyzedURLInfo()
            analyzed_url_info.task_id = analytical.task_id
            analyzed_url_info.attr_id = analytical.attr_id
            analyzed_url_info.depth = analytical.depth
            analyzed_url_info.cur_depth = analytical.cur_depth + 1
            analyzed_url_info.method = 2 # 1:PUT 2:GET 3:POST
            analyzed_url_info.url = url
            analyzed_urls.url_infos.append(analyzed_url_info)
            cnt += 1
            if cnt == 10 or url == url_list[-1]:
                data = analyzed_urls.packestream()
#                 self.transport.write(data)
                self.network.send_msg(data)
                cnt = 0

analy_mgr = AnalyticalManager()
        
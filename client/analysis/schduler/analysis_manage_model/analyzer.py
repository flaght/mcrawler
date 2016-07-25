# -.- coding:utf-8 -.-
'''
Created on 2015年10月9日

@author: chenyitao
'''

import json
import time

from schduler.analysis_models.cn_models.cn_manage import CNManager
# from schduler.analysis_models.ths_models.ths_manage import ThsManager
from schduler.analysis_models.ths_more_models.ths_manage import ThsNewsManager
from schduler.analysis_models.weibo_models.weibo_analysis.weibo_manage import WBManager
from schduler.analysis_models.yicai_models.yicai_manage import YicaiManager
from schduler.storage.hbase_manage_model import hbase_manager


class Analysiser(object):
    '''
    '''
    err_ok = 2
    err_exception = 128
    err_get_source_data_failed = 129
    err_source_data_unusual = 130
    err_can_not_find_attr_id = 131

    def __init__(self, analytical, finished_callback=None, storage_manager=None):
        '''
        '''
        self.data = None
        self.storage_manager = storage_manager
        self.analytical = analytical
        self.finished_callback = finished_callback
        self.analysis_managers = {}
        self.__reg_managers()

    def __reg_managers(self):
#         self.analysis_managers[ThsManager.platform_id] = ThsManager
        self.analysis_managers[YicaiManager.platform_id] = YicaiManager
        self.analysis_managers[WBManager.platform_id] = WBManager
        self.analysis_managers[CNManager.platform_id] = CNManager
        self.analysis_managers[ThsNewsManager.platform_id] = ThsNewsManager

    def __analyzing(self):
        '''
        return: False:解析失败（row_data、row错误） 
                True:解析中
        '''
        if self.analytical.get_type() == 1:
            self.row_data = None
            def callback(ret):
                self.row_data = ret
            hbase_manager.get_row(self.analytical.key,
                                  self.analytical.name,
                                  callback)
            cnt = 0
            while not self.row_data:
                if cnt > 50:
                    break
                time.sleep(0.1)
                cnt += 1
            if self.row_data:
#                 for row in row_data:
#                 content = row_data.columns.get('basic:content')
                content = self.row_data['basic:content']
#                 value = content.value
                value = content
#                 timestamp = content.timestamp
            else:
                return self.err_get_source_data_failed
        elif self.analytical.get_type() == 3:
            def get_data(content):
                self.data = content
            self.storage_manager.ftp_text_manager.download_data(self.analytical.name,
                                                                self.analytical.key,
                                                                get_data)
            while not self.data:
                if self.data == 'err':
                    return self.err_get_source_data_failed
                time.sleep(0.2)
            content = json.loads(self.data)
            value = content['content']
#             timestamp = content['timestamp']
#         if value and timestamp:
        if value:
            analysis_manager_cls = self.analysis_managers[self.analytical.attr_id]
            if analysis_manager_cls:
                analysis_manager = analysis_manager_cls(finished_callback=self.finished)
                analysis_manager.setDaemon(True)
                analysis_manager.start()
                analysis_manager.add_task(**{'content':value})
#                                              'timestamp':timestamp})
                cnt = 0
                while not analysis_manager.is_stop:
                    if cnt > 50:
                        analysis_manager.is_stop = True
                        break
                    time.sleep(0.1)
                    cnt += 1
                return self.err_ok
            else:
                return self.err_can_not_find_attr_id
        return self.err_source_data_unusual

    def finished(self, **kwargs):
        if not len(kwargs) and self.finished_callback:
            self.finished_callback(**{'analytical':self.analytical,
                                      'url_list':[],
                                      'success':Analysiser.err_exception})
            return
        storage_cmd_list = kwargs['storage_cmd_list']
        url_list = kwargs['url_list']
        if kwargs['storage_type'] != -1:
            self.storage_manager.storage(kwargs['storage_type'],
                                    storage_cmd_list)
        if self.finished_callback:
            self.finished_callback(**{'analytical':self.analytical,
                                      'url_list':url_list,
                                      'success':Analysiser.err_ok})

    def analyze(self):
        '''
        '''
        return self.__analyzing()

if __name__ == '__main__':
    data_to_redis = Analysiser(1, 't.10jqka.com.cn', 'd7fc75dd5675eb0c70534488710a8c21')
    data_to_redis.analyze()

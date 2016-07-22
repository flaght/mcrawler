# -.- coding:utf-8 -.-
'''
Created on 2015年9月7日

@author: chenyitao
'''

import struct

from kid.common.device_manager import current_device_manager
from kid.common.sock_opcode import KidSockOpcode
from kid.model_manage.sock_manage.package.sock_head import SockHead


class TaskInfo(object):
    '''
    任务属性
    '''
    __struct_analysis_rule = '=QQQBBBBBBBB256s'
    task_info_length = struct.calcsize(__struct_analysis_rule)

    def __init__(self, params=None):
        if not params:
            self.job_id = 0
            self.attr_id = 0
            self.job_time = 0
            self.depth = 0
            self.cur_depth = 0
            self.machine = 0
            self.storage = 0
            self.is_login = 0
            self.is_over = 0
            self.is_forge = 0
            self.method = 0
            self.url = ''
            return
        (self.job_id,
        self.attr_id,
        self.job_time,
        self.depth,
        self.cur_depth,
        self.machine,
        self.storage,
        self.is_login,
        self.is_over,
        self.is_forge,
        self.method,
        self.url) = struct.unpack(self.__struct_analysis_rule, params)
        self.url = self.url.rstrip('\x00')

    def make_package(self):
        '''
        make package
        '''
        package_body = struct.pack(self.__struct_analysis_rule,
                                   self.job_id,
                                   self.attr_id,
                                   self.job_time,
                                   self.depth,
                                   self.cur_depth,
                                   self.machine,
                                   self.storage,
                                   self.is_login,
                                   self.is_over,
                                   self.is_forge,
                                   self.method,
                                   self.url)
        return package_body

class SockSDistributeTask(SockHead):
    '''
    向客户端分配任务(多)
    '''
    __struct_analysis_rule = '=I%ds'

    def __init__(self, params=None):
        if params == None:
            #head
            super(self.__class__, self).__init__()
            self.opcode = KidSockOpcode.s_distribute_task
            self.type = 1
            # body
            self.manager_id = current_device_manager.get_manager_id()
            self.tasks = []
            return
        params = super(self.__class__, self).compress_encrypt(params, False)
        str_head = params[0:SockHead.sock_head_len]
        str_body = params[SockHead.sock_head_len:]
        super(self.__class__, self).__init__(str_head)
        (self.manager_id,
        str_body) = struct.unpack(self.__struct_analysis_rule % (len(str_body)-4),
                                  str_body)
        self.tasks = []
        while str_body:
            str_task = str_body[0:TaskInfo.task_info_length]
            task = TaskInfo(str_task)
            self.tasks.append(task)
            str_body = str_body[TaskInfo.task_info_length:]

    def make_package(self):
        package_tasks = ''
        for task in self.tasks:
            package_tasks += task.make_package()
        package_body = struct.pack(self.__struct_analysis_rule % len(package_tasks),
                                   self.manager_id,
                                   package_tasks)
        self.make_checksum(len(package_body))
        package_head = super(self.__class__, self).make_package()
        return self.compress_encrypt(package_head+package_body)

def main():
    '''
    test
    '''
        # 封包
#     package = SOCK_S_CrawlerDistributeTask_Single()
#     package.manager_id = 127
#     package.task = TaskInfo()
#     package.task.job_id = 1
#     package.task.depth = 2
#     package.task.machine = 3
#     package.task.storage = 4
#     package.task.url = 'http://www.cnblogs.com/gala/archive/2011/09/22/2184801.html'
#     package_info = package.make_package()
#     # 解包
#     sock_crawler_manager_reg = SOCK_S_CrawlerDistributeTask_Single(package_info)
#     print sock_crawler_manager_reg
#
#     package2 = SOCK_S_CrawlerDistributeTask_Multi()
#     package2.manager_id = 123
#     package2.tasks = [TaskInfo(package.task.make_package()),
#                       TaskInfo(package.task.make_package()),
#                       TaskInfo(package.task.make_package()),
#                       TaskInfo(package.task.make_package()),
#                       TaskInfo(package.task.make_package())]
#     package2_info = package2.make_package()
#     sock_crawler_manager_reg = SOCK_S_CrawlerDistributeTask_Multi(package2_info)
#     print sock_crawler_manager_reg
    pass

if __name__ == '__main__':
    main()

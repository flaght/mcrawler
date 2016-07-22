# -.- coding:utf-8 -.-
'''
Created on 2015年9月7日

@author: chenyitao
'''

import threading
import time
import psutil


class DeviceManager(object):
    '''
    爬虫客户端配置及设备信息管理
    '''

    def __init__(self):
        self.manager_id = 0
        self.token = ''
        self.cpu_usage = 0
        cpu_timer = threading.Thread(target=self.__cal_cpu_usage, name='check_cpu_usage')
        cpu_timer.setDaemon(True)
        cpu_timer.start()

    def get_mac_address(self):
        '''
        mac address
        '''
        import uuid
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
        return '%s%s%s%s%s%s' % (mac[0:2],
                                 mac[2:4],
                                 mac[4:6],
                                 mac[6:8],
                                 mac[8:10],
                                 mac[10:])

    def get_cpu_usage(self):
        '''
        cpu usage
        '''
        if self.cpu_usage == 0:
            time.sleep(0.5)
        return self.cpu_usage

    def __cal_cpu_usage(self):
        '''
        check cpu usage
        '''
        while True:
            self.cpu_usage = psutil.cpu_percent(0.2)
            time.sleep(1.5)

    def get_mem_usage(self):
        '''
        mem usage
        '''
        return psutil.virtual_memory()[2]

    def get_manager_id(self):
        '''
        get manager id
        '''
        return self.manager_id

    def set_manager_id(self, manager_id):
        '''
        set manager id
        '''
        self.manager_id = manager_id

    def set_token(self, manager_token):
        '''
        set token
        '''
        self.token = manager_token

    def get_token(self):
        '''
        get token
        '''
        return self.token

current_device_manager = DeviceManager()

def main():
    '''
    test
    '''
    while True:
        print current_device_manager.get_cpu_usage()
        time.sleep(1)

if __name__ == '__main__':
    main()

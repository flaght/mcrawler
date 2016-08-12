#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  
# encoding=utf-8

"""
Created on 2015年9月29日

@author: kerry
"""

from multiprocessing import Pool
import platform
import sys

from netsvc.network import KIDInitialScheduler

account_list = []


def init_account():
    for i in range(100):
        account_list.append('9%dABCD123' % (i + 1))


def start_process(user, password):
    initial_scheduler = KIDInitialScheduler()
    initial_scheduler.connection("222.73.34.101", 16000, user, password)
    #    print user
    initial_scheduler.start_run()


def main():
    pool = Pool(processes=1)
    for i in range(1):
        ret = pool.apply_async(start_process, (account_list[i], '1234567'))
    pool.close()
    pool.join()
    if ret.successful():
        print 'create processes successful'


def kafka_main():
    pass


if __name__ == '__main__':
    sys_str = platform.system()
    print sys_str
    if platform.system() == "Darwin" or platform.system() == "Linux":
        reload(sys)
        sys.setdefaultencoding('utf-8')  # @UndefinedVariable

    init_account()
    main()
# start_process(account_list[10], '1234567')

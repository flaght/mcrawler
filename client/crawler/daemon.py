#!/usr/bin/python
#coding: utf-8
'''
Created on 2015年10月16日

@author: chenyitao
'''

import os
import socket
import time
import setproctitle
from kid.common import kid_setting

# from kid.common.send_sms import SendSms


def check_aliveness(ip, port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((ip,port))
        return True
    except Exception:
        return False
    finally:
        sk.close()
    return False

def main():
    '''
    daemon proc start
    '''
    setproctitle.setproctitle(kid_setting.DAEMON_PROC_NAME)
    while True:
        proc_info = os.popen('ps ax | grep '+kid_setting.CLIENT_PROC_NAME+' |grep -v grep',
                             'r').read()
        if len(proc_info) > 0:
            print proc_info
        else:
            if not check_aliveness(kid_setting.SERVER_IP, kid_setting.SERVER_PORT):
                time.sleep(30)
                continue
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if os.path.isfile('info.log'):
                os.rename('info.log', time_str+'_info.log')
            if os.path.isfile('warning.log'):
                os.rename('warning.log', time_str+'_warning.log')
            if os.path.isfile('error.log'):
                os.rename('error.log', time_str+'_error.log')
            os.system('python ./crawler_client.py')
#             sms = SendSms('15157109258,15158114927,18668169052',
#                           '【KID客户端】程序已停止，正在重启。')
#             sms.main()
        time.sleep(30)

if __name__ == '__main__':
    main()

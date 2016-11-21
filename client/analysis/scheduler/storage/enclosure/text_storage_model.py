# -.- coding:utf-8 -.-
"""
Created on 2015年11月16日

@author: chenyitao
"""

import threading
import base64
import time
import json
import icu
from analysis.base.ftp_ext import FTPExt
from analysis.base.analysis_conf_manager import analysis_conf

class TextStorage(threading.Thread):
    '''
    文本存储
    '''

    def __init__(self, host, port, user, passwd, timeout=5):
        '''
        Constructor
        '''
        self.detecotr = icu.CharsetDetector()
        super(TextStorage, self).__init__(name='ftp_manager')
        self.charset_list = ['utf-8', 'UTF-8', 'utf8', 'UTF8', 'gbk', 'GBK',
                             'gb2312', 'GB2312', 'gb18030', 'GB18030']

        self.ftp_host = host
        self.ft_port = port
        self.ftp_user = user
        self.ftp_passwd = passwd

        self.wait_queue = []
        self.state = 0
        self.__upload_cnt = 0
        self.is_stop = True
        self.ftp = FTPExt()
        self.ftp.set_pasv(True, host)
        try:
            if not self.ftp.connect(host, port):
                print 'connect ftp srever failed'
                return
            if not self.ftp.login(user, passwd):
                print 'login ftp server failed'
                return
        except Exception, e:
            print 'ftp error:%s' % e
            return

        self.ftp.cwd('~')
        file_list = self.ftp.nlst()
        if 'result_storage' not in file_list:
            self.ftp.mkd('result_storage')
        self.ftp.cwd('result_storage')
        self.path = self.ftp.pwd()
        self.state = 1
        self.is_stop = False
        self.setDaemon(True)
        self.start()

    def upload_data(self, data, path, filename):
        self.wait_queue.append({'data': data,
                                'path': path,
                                'filename': filename})
        self.is_stop = False
        self.run()

    def run(self):
        if len(self.wait_queue):
            item = self.wait_queue.pop(0)
            self.__upload_data(item['data'],
                           item['path'],
                           item['filename'])

        """
        while not self.is_stop:
            if len(self.wait_queue):
                if self.__upload_cnt > 10:
                    time.sleep(0.5)
                    continue
                item = self.wait_queue.pop(0)
                self.__upload_data(item['data'],
                                   item['path'],
                                   item['filename'])
            else:
                time.sleep(0.5)
         """

    def __reconection(self):
        self.ftp = FTPExt()
        self.ftp.set_pasv(True, self.ftp_host)
        try:
            if not self.ftp.connect(self.ftp_host, self.ft_port):
                print 'connect ftp srever failed'
                return None
            if not self.ftp.login(self.ftp_user, self.ftp_passwd):
                print 'login ftp server failed'
                return None
            return True
        except Exception, e:
            print 'ftp error:%s' % e
            return None

    def __upload_data(self, data, path, filename):
        path_list = path.split('/')
        if not self.ftp.is_connected():
            print 'ftp error'
            self.ftp.close()
            if self.__reconection() is None:
                return

        self.ftp.cwd('~/result_storage')
        for _path in path_list:
            if _path == '':
                continue
            if _path not in self.ftp.nlst():
                self.ftp.mkd(_path)
            self.ftp.cwd(_path)
        if filename in self.ftp.nlst():
            self.ftp.delete(filename)
        with open('tmp', 'wb') as f:
            f.write(data)

        """
        with open('tmp', 'wb') as f:
            '''
            if '<!DOCTYPE html' in data:
                charset = re.search(r'charset=(.*?)>', data).group(0)
                for code in self.charset_list:
                    if code in charset:
                        charset = code
                        break
                data = data.decode(charset)
            '''
            self.detecotr.setText(data)
            match = self.detecotr.detect()
            charset_name = match.getName()

            # data = data.decode(charset_name)
            # zlib

            compressed = zlib.compress(data)
            obj = {'charset': charset_name,
                   'content': base64.b32encode(compressed),
                   'timestamp': time.time()}
            jsons = json.dumps(obj)
            f.write(jsons)
        """
        with open('tmp', 'rb') as f:
            self.__upload_cnt += 1
            self.ftp.storbinary(cmd='STOR %s' % filename,
                            fp=f,
                            blocksize=len(data),
                            callback=self.__uploaded)
        self.is_stop = True

    def __uploaded(self, param):
        self.__upload_cnt -= 1

    def close(self):
        self.ftp.quit()
        self.is_stop = True


def main():
    '''test'''
    text_storage = TextStorage('61.147.80.233', 21, 'crawler', '123456x', 5)
    text_storage.upload_data('dsadasdasd', '3/20151116/', 'hello2.html')
    #     text_storage.close()
    while True:
        time.sleep(0.5)


if __name__ == '__main__':
    main()

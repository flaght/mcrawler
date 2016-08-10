# -.- coding:utf-8 -.-
"""
Created on 2015年11月16日

@author: chenyitao
"""

import threading
import base64
import time
import json
from base.ftp_ext import FTPExt
from base.analysis_conf_manager import analysis_conf


class TextStorage(threading.Thread):
    """
    文本存储
    """

    def __init__(self, host, port, user, passwd, timeout):
        """
        Constructor
        """
        threading.Thread.__init__(self)
        self.wait_queue = []
        self.state = 0
        self.__upload_cnt = 0
        self.is_stop = True
        self.ftp = FTPExt()
        self.ftp.set_pasv(True, host)
        if not self.ftp.connect(host, port):
            print 'connect ftp srever failed'
            return
        if not self.ftp.login(user, passwd):
            print 'login ftp server failed'
            return
        self.ftp.cwd('~')
        file_list = self.ftp.nlst()
        if 'text_storage' not in file_list:
            self.ftp.mkd('text_storage')
        self.ftp.cwd('text_storage')
        self.path = self.ftp.pwd()
        self.state = 1
        self.is_stop = False

    def upload_data(self, data, path, filename):
        self.wait_queue.append({'data': data,
                                'path': path,
                                'filename': filename})

    def download_data(self, filename, path, callback):
        self.wait_queue.append({'data': None,
                                'path': path,
                                'filename': filename,
                                'callback': callback})

    def __download_data(self, filename, path, callback):
        self.ftp.cwd('~/text_storage')
        with open('tmp', 'wb') as f:
            file_path = '%s/%s/%s' % (self.ftp.pwd(), path.split(':')[1], filename)
            try:
                self.__upload_cnt += 1
                self.ftp.retrbinary('RETR ' + file_path,
                                    f.write)
            except Exception, e:
                print 'download %s:%s failed' % (path, filename)
                self.uploaded()
                callback('err')
                return
        with open('tmp', 'rb') as f:
            data = f.read()
            self.uploaded()
            callback(data)

    def run(self):
        while not self.is_stop:
            if len(self.wait_queue):
                if self.__upload_cnt > 20:
                    time.sleep(0.2)
                    continue
                item = self.wait_queue.pop(0)
                if item['data']:
                    self.__upload_data(item['data'],
                                       item['path'],
                                       item['filename'])
                else:
                    self.__download_data(item['filename'],
                                         item['path'],
                                         item['callback'])
            else:
                time.sleep(0.2)

    def __upload_data(self, data, path, filename):
        path_list = path.split('/')
        self.ftp.cwd('~/text_storage')
        for _path in path_list:
            if _path == '':
                continue
            if _path not in self.ftp.nlst():
                self.ftp.mkd(_path)
            self.ftp.cwd(_path)
        with open('tmp', 'wb') as f:
            obj = {'content': data, 'timestamp': time.time()}
            try:
                f.write(json.dumps(obj))
            except Exception, e:
                print 'upload error'
                return None
        with open('tmp', 'rb') as f:
            try:
                filename_base64 = base64.b64encode(filename)
                self.__upload_cnt += 1
                self.ftp.storbinary(cmd='STOR %s' % filename_base64,
                                    fp=f,
                                    blocksize=8192,
                                    callback=self.uploaded)
            except:
                print 'upload %s failed' % filename
                return None

    def uploaded(self, param=None):
        self.__upload_cnt -= 1

    def close(self):
        self.ftp.quit()
        self.is_stop = True


ftp_info = analysis_conf.ftp_info
ftp_text_manager = TextStorage(ftp_info['host'],
                               ftp_info['port'],
                               ftp_info['user'],
                               ftp_info['passwd'],
                               ftp_info['timeout'])
ftp_text_manager.setDaemon(True)


# ftp_text_manager.start()


def main():
    """test"""
    text_storage = TextStorage('112.124.49.59', 21, 'root', 's6g2BNYrKRa[', 5)
    text_storage.setDaemon(True)
    text_storage.start()
    text_storage.upload_data('dsadasdasd', '3/20151116/', 'hello.html')
    #     text_storage.close()
    while text_storage.is_alive():
        time.sleep(0.5)


if __name__ == '__main__':
    main()

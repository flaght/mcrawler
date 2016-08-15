# -.- coding:utf-8 -.-
"""
Created on 2016年8月6日

@author: kerry
"""
from base.ftp_ext import FTPExt
from base.analysis_conf_manager import analysis_conf
import io


class FTPManager:
    def __init__(self, host, port, name, pwd, local='./'):
        self.host = host
        self.port = port
        self.name = name
        self.pwd = pwd
        self.local = local
        self.ftp = FTPExt()
        self.is_connected = False

    def connect(self):
        if self.is_connected:
            return

        self.ftp.set_pasv(True, self.host)
        try:
            if not self.ftp.connect(self.host, self.port):
                print 'connect ftp server failed'
                return
            if not self.ftp.login(self.name, self.pwd):
                print 'login ftp server failed'
                return
        except Exception, e:
            print 'ftp error:%s' % e
            return

        self.is_connected = True
        # print "connect succeeded"
        '''
        self.ftp.connect(self.host, self.port)
        self.ftp.login(self.name, self.pwd)
        '''

    def log(self):
        print self.host
        print self.port
        print self.name
        print self.pwd

    def run(self):
        self.ftp.cwd('~/text_storage/60005')
        date_files = self.ftp.nlst()
        print date_files

    @staticmethod
    def callback(msg):
        print '===============>'
        print msg
        print '===============>'

    def get(self, ftp_path, callback=None):
        file_size = self.ftp.size(ftp_path)
        if callback is None:
            self.ftp.retrbinary('RETR ' + ftp_path, self.callback, file_size)
        else:
            self.ftp.retrbinary('RETR ' + ftp_path, callback, file_size)

    def download(self, local_path, ftp_path):
        with open(self.local + '/' + local_path, 'wb') as f:
            self.ftp.retrbinary('RETR ' + ftp_path, f.write)
            f.close()

    def write(self, path, content):
        self.ftp.storbinary("STOR " + path, io.BytesIO(content))

    def exist_dir(self, path, folder_name):
        filelist = []
        self.ftp.retrlines('LIST ' + path, filelist.append)
        for f in filelist:
            if f.split()[-1] == folder_name:
                return True
        return False

    def mkd(self, path):
        return self.ftp.mkd(path)

    def close(self):
        self.ftp.close()


def main():
    """test"""
    ftp_manager = FTPManager(analysis_conf.ftp_info['host'],
                             analysis_conf.ftp_info['port'],
                             analysis_conf.ftp_info['user'],
                             analysis_conf.ftp_info['passwd'],
                             analysis_conf.ftp_info['local'])
    ftp_manager.connect()
    ftp_manager.run()
    # ftp_manager.get('~/text_storage/60005/ffc926edd312d4e1dd1c2d4fc22314f4', None)
    # ftp_manager.download('./3.txt', '~/text_storage/60005/fd0c096acbf091ff81f1f7f925044187')
    ftp_manager.close()


if __name__ == '__main__':
    main()

ftp_manager_t = FTPManager(analysis_conf.ftp_info['host'],
                           analysis_conf.ftp_info['port'],
                           analysis_conf.ftp_info['user'],
                           analysis_conf.ftp_info['passwd'],
                           analysis_conf.ftp_info['local'])

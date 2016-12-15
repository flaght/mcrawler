# -.- coding:utf-8 -.-
"""
Created on 2016年8月6日

@author: kerry
"""
from analysis.base.ftp_ext import FTPExt
from analysis.base.analysis_conf_manager import analysis_conf
from analysis.base.mlog import mlog
import io


class FTPManager:
    def __init__(self, host, port, name, pwd, timeout=7, local='./'):
        self.host = host
        self.port = port
        self.name = name
        self.pwd = pwd
        self.local = local
        self.ftp = FTPExt()
        self.is_connected = False
        self.timeout = 5



    def file_count(self):
        return len(self.ftp.nlst())

    def set_path(self,path):
        self.ftp.cwd(path)

    def get_file(self,start,end):
        file_list = self.ftp.nlst()
        return file_list[start:end]

    def get_file_list(self):
        return self.ftp.nlst()

    def __u_connect(self):
        self.ftp.set_pasv(True, self.host)
        try:
            if not self.ftp.connect(self.host, self.port, self.timeout):
                mlog.log().error("connect ftp server failed")
                return False
            if not self.ftp.login(self.name, self.pwd):
                mlog.log().error("login ftp server failed")
                return False
            self.is_connected = True
            mlog.log().info("ftp login success")
            return True
        except Exception, e:
            mlog.log().error("ftp error[%s]", e)
            return False


    def connect(self):
        if self.is_connected:
            return

        self.__u_connect()

    def log(self):
        mlog.log().info(self.host)
        mlog.log().info(self.port)
        mlog.log().info(self.name)
        mlog.log().info(self.pwd)

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
        if not self.ping():
            return False
        try:
            file_size = self.ftp.size(ftp_path)
            if callback is None:
                self.ftp.retrbinary('RETR ' + ftp_path, self.callback, file_size)
            else:
                self.ftp.retrbinary('RETR ' + ftp_path, callback, file_size)
            return True
        except Exception,e:
            mlog.log().error("ftp error:%s url:%s", e, ftp_path)
            return False

    def ping(self):
        if not self.ftp.is_connected():
            self.ftp.close()
            self.is_connected = False
            if self.__u_connect() is True:
                return True
            else:
                return False
        return True


    def download(self, local_path, ftp_path):
        if not self.ping():
            return
        with open(self.local + '/' + local_path, 'wb') as f:
            self.ftp.retrbinary('RETR ' + ftp_path, f.write)
            f.close()

    def write(self, path, content):
        if not self.ping():
            return
        self.ftp.storbinary("STOR " + path, io.BytesIO(content))

    def close(self):
        self.ftp.close()
        mlog.log().info("close ftp ip %s",self.host)


def main():
    """test"""
    ftp_manager = FTPManager(analysis_conf.ftp_info['host'],
                             analysis_conf.ftp_info['port'],
                             analysis_conf.ftp_info['user'],
                             analysis_conf.ftp_info['passwd'],
                             analysis_conf.ftp_info['local'])
    ftp_manager.connect()
    ftp_manager.run()
    ftp_manager.get('~/text_storage/60005/ffc926edd312d4e1dd1c2d4fc22314f4', None)
    # ftp_manager.download('./3.txt', '~/text_storage/60005/fd0c096acbf091ff81f1f7f925044187')
    ftp_manager.close()


if __name__ == '__main__':
    main()

ftp_manager_t = FTPManager(analysis_conf.ftp_info['host'],
                           analysis_conf.ftp_info['port'],
                           analysis_conf.ftp_info['user'],
                           analysis_conf.ftp_info['passwd'],
                           analysis_conf.ftp_info['local'])

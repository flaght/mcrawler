# -.- coding:utf-8 -.-
"""
Created on 2016年8月6日

@author: kerry
"""
from tools.base.ftp_ext import FTPExt
from tools.base.mlog import mlog
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
        self.ftp.cwd('~/text_storage')
        path_list = path.split('/')
        for _path in path_list:
            self.ftp.cwd(_path)

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
            mlog.log().info("host : "+self.host+"  ftp login success")
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



    def get(self, basic_path, filename, callback=None):
        if not self.ping():
            return False
        try:
            #self.ftp.cwd('~/text_storage')
            path_list = basic_path.split('/')
            for _path in path_list:
                self.ftp.cwd(_path)
            #self.ftp.cwd(basic_path)
            file_size = self.ftp.size(filename)
            if callback is None:
                self.ftp.retrbinary('RETR ' + filename, self.callback, file_size)
            else:
                self.ftp.retrbinary('RETR ' + filename, callback, file_size)
            return True
        except Exception,e:
            mlog.log().error("ftp error:%s url:%s", e, filename)
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
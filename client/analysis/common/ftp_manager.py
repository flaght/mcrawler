# -.- coding:utf-8 -.-
'''
Created on 2016年8月6日

@author: kerry
'''
from analysis.base.ftp_ext import FTPExt
from analysis.base.analysis_conf_manager import analysis_conf

class FTPManager():
   
    def __init__(self,host,port,name,pwd,local='./'):
        self.host = host
        self.port = port
        self.name = name
        self.pwd = pwd
        self.local = local
        self.ftp = FTPExt()
        self.is_connted = False
    
    def connent(self):
        if(self.is_connted):
            return
        
        self.ftp.set_pasv(True, self.host)
        try:
            if not self.ftp.connect(self.host, self.port):
                print 'connect ftp srever failed'
                return
            if not self.ftp.login(self.name, self.pwd):
                print 'login ftp server failed'
                return
        except Exception, e:
            print 'ftp error:%s' % e
            return
        
        self.is_connted = True
        #print "connect successed"
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
        
    def callback(self,str):
        print '===============>'
        print str
        print '===============>'
        
    def get(self,ftppath,callback=None):
        file_size = self.ftp.size(ftppath)
        if(callback==None):
            self.ftp.retrbinary('RETR ' + ftppath, self.callback,file_size)
        else:
            self.ftp.retrbinary('RETR ' + ftppath, callback,file_size)
        
    def download(self, localpath, ftppath):
        with open(self.local+'/'+localpath, 'wb') as f:
            self.ftp.retrbinary('RETR ' + ftppath, f.write)
            f.close()
    
    def close(self):
        self.ftp.close()
        
        
def main():
    '''test'''
    ftp_manager = FTPManager(analysis_conf.ftp_info['host'], 
                           analysis_conf.ftp_info['port'], 
                           analysis_conf.ftp_info['user'], 
                           analysis_conf.ftp_info['passwd'],
                           analysis_conf.ftp_info['local'])
    ftp_manager.connent()
    ftp_manager.run()
    ftp_manager.get('~/text_storage/60005/fd0c096acbf091ff81f1f7f925044187', None)
    #ftp_manager.download('./3.txt', '~/text_storage/60005/fd0c096acbf091ff81f1f7f925044187')
    ftp_manager.close()

if __name__ == '__main__':
    main()
    
ftp_manager_t = FTPManager(analysis_conf.ftp_info['host'], 
                           analysis_conf.ftp_info['port'], 
                           analysis_conf.ftp_info['user'], 
                           analysis_conf.ftp_info['passwd'],
                           analysis_conf.ftp_info['local'])

        
        
    
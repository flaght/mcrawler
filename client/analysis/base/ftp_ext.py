# -.- coding:utf-8 -.-
"""
Created on 2015年12月15日

@author: chenyitao
"""

from ftplib import FTP, parse227, parse229
import socket


class FTPExt(FTP):
    """
    class docs
    """

    def __init__(self):
        """
        Constructor
        """
        self.passive_server = None
        self.fix_host = None
        FTP.__init__(self)

    def set_pasv(self, val, addr=None):
        self.passive_server = val
        self.fix_host = addr

    def makepasv(self):
        if self.af == socket.AF_INET:
            host, port = parse227(self.sendcmd('PASV'))
        else:
            host, port = parse229(self.sendcmd('EPSV'), self.sock.getpeername())
        if self.fix_host is not None:
            host = self.fix_host
        return host, port

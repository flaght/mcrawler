# -.- coding:utf-8 -.-

'''
Created on 2015年8月25日

@author: chenyitao
'''

import time

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet.protocol import connectionDone

from kid.common import kid_setting
from kid.common.common_method import print_plus
from kid.common.kid_signal import KidSignal
from kid.common.sock_opcode import KidSockOpcode
from kid.common.sub_model_opcode import SubModelOpcode
from kid.model_manage.sub_model_manager import SubModelManager


class KidClientProtocol(Protocol):
    '''
    Protocal
    '''
    
    def __init__(self):
        kid_setting.CONNECT = 1
        self.sub_model_manager = SubModelManager(self)

    def connectionMade(self):
        '''
        sock链接成功，向服务器注册管理器
        '''
        self.sub_model_manager.add_signal(KidSignal(sub_model_opcode=\
                                                    SubModelOpcode.sock_send_model,
                                                    opcode=\
                                                    KidSockOpcode.c_manager_register))

    def connectionLost(self, reason=connectionDone):
        kid_setting.CONNECT = 0
        print_plus('connectionLost', level=1)

    def dataReceived(self, data):
        self.last_packet_time = time.time()
        self.sub_model_manager.add_signal(KidSignal(sub_model_opcode=\
                                                    SubModelOpcode.sock_recv_model,
                                                    data=data))


class KidClientFactory(ReconnectingClientFactory):
    '''
    Factory
    '''
    protocol = KidClientProtocol

    def startedConnecting(self, connector):
        print_plus('Start to connect')

    def clientConnectionLost(self, connector, reason):
        print_plus('clientConnectionLost', level=1)
        time.sleep(15)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print_plus('clientConnectionFailed', level=1)
        time.sleep(15)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

def main():
    '''
    test
    '''
    client = KidClientProtocol()
    client.connectionMade()
    from kid.model_manage.sock_manage.package.s_manager_register import SockSManagerREG
    package = SockSManagerREG()
    package.manager_id = 127
    package.token = '0123456789abcdef0123456789ABCDEF'
    package_info = package.make_package()
    print package_info
#     client.dataReceived(package_info)
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()

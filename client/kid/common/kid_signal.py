# -.- coding:utf-8 -.-
'''
Created on 2016年2月25日

@author: chenyitao
'''

class KidSignal(object):
    '''
    KidSignal
    '''


    def __init__(self, sub_model_opcode=None, opcode=None, data=None):
        '''
        Constructor
        '''
        self.sub_model_opcode = sub_model_opcode
        self.opcode = opcode
        self.data = data

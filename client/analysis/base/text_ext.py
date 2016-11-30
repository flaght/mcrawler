# -.- coding:utf-8 -.-

"""
Created on 2016年11月26日

@author: kerry
"""


class TextExt():
    def __init__(self, name):
        self.obj = open(name, 'w+')

    def __del__(self):
        self.obj.close()

    def write(self, data):
        self.obj.write(str(data))

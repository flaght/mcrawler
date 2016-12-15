#!/usr/bin/python2.6  
# -*- coding: utf-8 -*-  
#encoding=utf-8

"""
Created on 2016年8月7日

@author: kerry
"""

class MString():
    
    def __init__(self,name=None):
        self.string = ''
        self.name = name
    
    def write(self,string):
        self.string += string
        
    def string(self):
        return self.string
# -*- coding: utf-8 -*-

"""
Created on 2016年11月19日

@author: kerry
"""

from analysis.scheduler.storage.enclosure.sqlite_manage_model import SQLLiteStorage
from analysis.base.text_ext import TextExt as TextStorage
from analysis.common.operationcode import storage_opcode


class BaseStorager:
    @classmethod
    def create_storager(cls, stype, config):
        if stype == storage_opcode.sqlite:
            return SQLLiteStorage(config['name'], 0)
        elif stype == storage_opcode.mysql:
            return None
        elif stype == storage_opcode.text:
            return TextStorage(config['name'])
        else:
            return None

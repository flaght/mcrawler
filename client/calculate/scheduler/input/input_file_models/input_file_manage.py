# -.- coding:utf-8 -.-
"""
Created on 2017年5月23日

@author: kerry
"""

from calculate.scheduler.input.input_file_models.file_ftp_manage import FileFTPManage
from calculate.scheduler.input.input_file_models.file_local_manage import FileLocalManage
from tools.common.operationcode import filer_opcode

class InputFileManager(object):
    """
    文件读取管理器
    """

    @classmethod
    def create_file_manager(cls,config):
        stype = config['type']
        if stype == filer_opcode.ftp:
            return FileFTPManage(config)
        elif stype == filer_opcode.local:
            return FileLocalManage(config)
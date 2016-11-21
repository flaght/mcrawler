# -.- coding:utf-8 -.-
"""
Created on 2016年11月18日

@author: kerry
"""

from analysis.scheduler.input.input_file_models.file_ftp_manage import FileFTPManage
class FilerOpcode:
    """
    storage opcode
    """
    ftp = 1
    http = 2
    local = 3

filer_opcode = FilerOpcode()

class InputFileManager:
    """
    文件读取管理器
    """

    @classmethod
    def create_file_manager(cls,config):
        stype = config['type']
        if stype == filer_opcode.ftp:
            return FileFTPManage(config)
        else:
            return None
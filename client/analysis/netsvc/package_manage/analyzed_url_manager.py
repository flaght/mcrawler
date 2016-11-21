# -.- coding:utf-8 -.-
"""
Created on 2015年11月5日

@author: chenyitao
"""

from analysis.netsvc.packet_processing import AnalyzedURLInfo


class AnalyzedURLManager(object):
    """
    class docs
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    @staticmethod
    def set_package_info(task_id, depth, cur_depth, method, url):
        """
        set package info
        """
        state_info = AnalyzedURLInfo()
        state_info.make_head(0, 0, 0, 1033, 0, 0)  # todo 该方法是否已被启用
        state_info.task_id = task_id
        state_info.depth = depth
        state_info.cur_depth = cur_depth
        state_info.method = method
        state_info.url = url
        return state_info.packet_stream()


analyzed_url_manager = AnalyzedURLManager()

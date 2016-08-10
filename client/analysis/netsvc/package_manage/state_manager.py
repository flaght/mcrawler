# -.- coding:utf-8 -.-
"""
Created on 2015年10月9日

@author: chenyitao
"""
from netsvc.packet_processing import AnalyticalState


class StateManager(object):
    """
    class docs
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    @staticmethod
    def set_package_info(analysis_id, state):
        """
        set package info
        """
        state_info = AnalyticalState()
        state_info.make_head(0, 0, 0, 1032, 0, 0)
        state_info.set_analytical_id(analysis_id)
        state_info.set_state(state)
        return state_info.packet_stream()

state_manager = StateManager()

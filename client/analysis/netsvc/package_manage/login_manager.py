# -*- coding: utf-8 -*-
# encoding=utf-8

"""
Created on 2015年10月6日

@author: kerry
"""
from netsvc.packet_processing import AnalyticalReg


class LoginManager(object):
    """
    class docs
    """

    def __init__(self):
        """
        Constructor
        """

    @staticmethod
    def manager_register(level, mac, password):
        """
        manager reg
        """
        login = AnalyticalReg()
        login.make_head(0, 0, 0, 1031, 0, 0)
        login.set_level(level)
        login.set_password(password)
        login.set_mac(mac)
        return login.packet_stream()


login_manager = LoginManager()

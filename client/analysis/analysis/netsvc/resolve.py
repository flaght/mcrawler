# -.- coding:utf-8 -.-
"""
Created on 2015年9月29日

@author: kerry
"""
import struct


class NetData(object):
    """
    class docs
    """

    def __init__(self):
        """
        Constructor
        """
        self.struct_format = "=h"
        self.prefix_length = struct.calcsize(self.struct_format)
        self._unprocessed = ""
        self.PACKET_MAX_LENGTH = 99999

    def net_wok(self, data):
        """
        work
        长度取前2个字节
        """
        all_data = self._unprocessed + data
        current_offset = 0
        fmt = self.struct_format
        self._unprocessed = all_data
        packet, result = None, None

        while len(all_data) >= (current_offset + self.prefix_length):
            message_start = current_offset + self.prefix_length
            length, = struct.unpack(fmt, all_data[current_offset:message_start])
            if length > self.PACKET_MAX_LENGTH:
                self._unprocessed = all_data
                self.lenthLimitExceeded(length)  # todo unknown method
                return
            message_end = current_offset + length
            if len(all_data) < message_end:
                packet = ""
                result = 0
                break
            packet = all_data[current_offset:message_end]
            current_offset = message_end
            result = 1
        self._unprocessed = all_data[current_offset:]
        return packet, result

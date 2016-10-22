# encoding=utf-8

"""
Created on 2015年9月29日

@author: kerry
"""
import struct


class PacketHead(object):
    """
    package head
    """

    def __init__(self):
        self.packet_length = 0
        self.is_zip_encrypt = 0
        self.head_type = 0
        self.signature = 0
        self.operate_code = 0
        self.data_length = 0
        self.timestamp = 0
        self.session_id = 0
        self.reserved = 0
        self.head = None
        self.body = None

    def set_packet_length(self, packet_length):
        """
        set packet length
        """
        self.packet_length = packet_length

    def set_is_zip_encrypt(self, is_zip_encrypt):
        """
        set is zip
        """
        self.is_zip_encrypt = is_zip_encrypt

    def set_type(self, head_type):
        """
        set type
        """
        self.head_type = head_type

    def set_signature(self, set_signature):
        """
        set signature
        """
        self.signature = set_signature

    def set_operate_code(self, operate_code):
        """
        set operate code
        """
        self.operate_code = operate_code

    def set_data_length(self, data_length):
        """
        set data length
        """
        self.data_length = data_length

    def set_timestamp(self, timestamp):
        """
        set timestamp
        """
        self.timestamp = timestamp

    def set_session_id(self, session_id):
        """
        set session id
        """
        self.session_id = session_id

    def set_reserved(self, reserved):
        """
        set reserved
        """
        self.reserved = reserved

    def make_head(self,
                  is_zip_encrypt,
                  head_type,
                  signature,
                  operate_code,
                  session_id,
                  reserved):
        """
        make head
        """
        self.is_zip_encrypt = is_zip_encrypt
        self.head_type = head_type
        self.signature = signature
        self.operate_code = operate_code
        self.timestamp = 0
        self.session_id = session_id
        self.reserved = 0

    def head_stream(self):
        """
        head stream
        """
        self.head = struct.pack('=HBBHHHIQI',
                                self.packet_length,
                                self.is_zip_encrypt,
                                self.head_type,
                                self.signature,
                                self.operate_code,
                                self.data_length,
                                self.timestamp,
                                self.session_id,
                                int(self.reserved))

    @staticmethod
    def packet_head_length():
        """
        return packet head length
        """
        return 26

    def unpack_head(self, packet_stream):
        """
        unpack head
        """
        self.packet_length, \
            self.is_zip_encrypt, \
            self.head_type, \
            self.signature, \
            self.operate_code, \
            self.data_length, \
            self.timestamp, \
            self.session_id, \
            self.reserved = struct.unpack_from('=hbbhhhiqi', packet_stream)


class AnalyticalReg(PacketHead):
    """
    analytical reg
    """

    def __init__(self):
        PacketHead.__init__(self)
        self.level = 0
        self.password = ""
        self.mac = ""

    def set_level(self, level):
        """
        set level
        """
        self.level = level

    def set_password(self, password):
        """
        set password
        """
        self.password = password

    def set_mac(self, mac):
        """
        set mac
        """
        self.mac = mac

    def body_stream(self):
        """
        body stream
        """
        self.body = struct.pack('=h8s16s',
                                self.level,
                                self.password,
                                self.mac)

    @staticmethod
    def packet_body_length():
        """
        packet body length
        """
        return 2 + 8 + 16

    def packet_stream(self):
        """
        packet stream
        """
        self.body_stream()
        self.set_packet_length(self.packet_head_length() + self.packet_body_length())
        self.set_data_length(self.packet_body_length())
        self.head_stream()
        return self.head + self.body


class ElementAnalysis(object):
    """
    element analysis
    """

    def __init__(self):
        self.analysis_id = 0
        self.task_id = 0
        self.attr_id = 0
        self.type = 0  # 1:hbase 3:ftp
        self.depth = 0
        self.cur_depth = 0
        self.name = ""
        self.key = ""

    def set_depth(self, depth):
        self.depth = depth

    def set_cur_depth(self, cur_depth):
        self.cur_depth = cur_depth

    def set_name(self, name):
        """
        set name
        """
        self.name = name

    def set_key(self, key):
        """
        set key
        """
        self.key = key

    def set_analysis_id(self, analysis_id):
        """
        set analysis id
        """
        self.analysis_id = analysis_id

    def set_task_id(self, task_id):
        """
        set task id
        """
        self.task_id = task_id

    def set_attr_id(self, attr_id):
        """
        set attr id
        """
        self.attr_id = attr_id

    def set_type(self, _type):
        self.type = _type

    def get_depth(self):
        return self.depth

    def get_cur_depth(self):
        return self.cur_depth

    def get_name(self):
        """
        get name
        """
        return self.name

    def get_key(self):
        """
        get key
        """
        return self.key

    def get_analysis_id(self):
        """
        get analysis id
        """
        return self.analysis_id

    def get_task_id(self):
        """
        get task id
        """
        return self.task_id

    def get_attr_id(self):
        """
        get attr id
        """
        return self.attr_id

    def get_type(self):
        return self.type

    @classmethod
    def packet_len(cls):
        """
        return packet len
        """
        return struct.calcsize('=qqiBBB32s32s')


class AnalyticalInfo(PacketHead):
    """
    analytical info
    """

    def __init__(self):
        PacketHead.__init__(self)
        self.id = 0
        self.analytical = []

    def get_analysis_list(self):
        """
        get analysis list
        """
        return self.analytical

    def unpack_stream(self, data):
        """
        unpack stream
        """
        self.unpack_head(data)
        i = 0
        n = self.data_length / ElementAnalysis.packet_len()
        while n > 0:
            element = ElementAnalysis()
            analysis_id, \
                task_id, \
                attr_id, \
                storage_type, \
                depth, \
                cur_depth, \
                name, \
                key = struct.unpack_from('=qqiBBB32s32s',
                                         data,
                                         26 + i * ElementAnalysis.packet_len())
            n -= 1
            i += 1
            element.set_analysis_id(analysis_id)
            element.set_task_id(task_id)
            element.set_attr_id(attr_id)
            element.set_type(storage_type)
            element.set_name(name.rstrip('\x00'))
            element.set_key(key.rstrip('\x00'))
            element.set_depth(depth)
            element.set_cur_depth(cur_depth)
            self.analytical.append(element)


class AnalyticalState(PacketHead):
    """
    analytical state
    """

    def __init__(self):
        PacketHead.__init__(self)
        self.analytical_id = 0
        self.state = 0

    def set_analytical_id(self, analytical_id):
        """
        set analytical id
        """
        self.analytical_id = analytical_id

    def set_state(self, state):
        """
        set state
        """
        self.state = state

    def get_analytical_id(self):
        """
        get analytical id
        """
        return self.analytical_id

    def get_state(self):
        """
        get state
        """
        return self.state

    def body_stream(self):
        """
        body stream
        """
        self.body = struct.pack('=qB', self.analytical_id, self.state)

    @staticmethod
    def packet_body_length():
        """
        packet body length
        """
        return 8 + 1

    def packet_stream(self):
        """
        pack stream
        """
        self.body_stream()
        self.set_packet_length(self.packet_head_length() + self.packet_body_length())
        self.set_data_length(self.packet_body_length())
        self.head_stream()
        return self.head + self.body


class AnalyzedURLInfo(object):
    """
    analytical state
    """
    length = struct.calcsize('QQBBB256s')

    def __init__(self):
        self.task_id = 0
        self.attr_id = 0
        self.depth = 0
        self.cur_depth = 0
        self.method = 0
        self.url = ''
        self.body = None

    def body_stream(self):
        """
        body stream
        """
        self.body = struct.pack('=QQBBB256s',
                                self.task_id,
                                self.attr_id,
                                self.depth,
                                self.cur_depth,
                                self.method,
                                str(self.url))

    @staticmethod
    def packet_body_length():
        """
        packet body length
        """
        return struct.calcsize('QQBBB256s')

    def packet_stream(self):
        """
        pack stream
        """
        self.body_stream()
        return self.body


class AnalyzedURLs(PacketHead):
    def __init__(self):
        PacketHead.__init__(self)
        self.make_head(0, 0, 0, 1033, 0, 0)
        self.manage_id = 0
        self.token = ''
        self.url_info_list = []

    def packet_stream(self):
        """
        unpack stream
        """
        info_data = ''
        for info in self.url_info_list:
            info_data += info.packestream()
        self.body = struct.pack('=I32s%ds' % len(info_data),
                                self.manage_id,
                                self.token,
                                info_data)
        body_len = len(self.body)
        self.set_packet_length(self.packet_head_length() + body_len)
        self.set_data_length(body_len)
        self.head_stream()
        return self.head + self.body

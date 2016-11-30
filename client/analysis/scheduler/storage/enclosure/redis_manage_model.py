# -.- coding:utf-8 -.-
"""
Created on 2015年10月9日

@author: chenyitao
"""

import redis
from analysis.base.analysis_conf_manager import analysis_conf


class RedisManageModel(object):
    """
    class docs
    """

    def __init__(self, host=None, port=None, db=None, password=None):
        """
        Constructor
        """
        self.state = 0
        try:
            self.redis = redis.StrictRedis(host, port, db, password, socket_timeout=5)
            self.pipe = self.redis.pipeline()
            self.state = 1
        except:
            print 'redis init failed'
            return
        print 'redis init successed'

    def get_storage_info(self, cmd=None, params=None):
        """
        get storage info
        """
        if cmd == 'LRANGE' or cmd == 'lrange':
            return self.redis.lrange(params['name'], params['start'], params['end'])

    def set_storage_info(self, cmd=None, params=None):
        """
        set storage info
        """
        if cmd == 'INCR' or cmd == 'incr':
            self.pipe.incr(params['name'])
        elif cmd == 'EXPIRE' or cmd == 'expire':
            self.pipe.expire(params['name'], params['time'])
        elif cmd == 'ZINCRBY' or cmd == 'zincrby':
            self.pipe.zincrby(params['name'], params['value'], params['amount'])
        elif cmd == 'HINCRBY' or cmd == 'hincrby':
            self.pipe.hincrby(params['name'], params['value'], params['amount'])

    def commit(self):
        """
        commit
        """
        self.pipe.execute()

redis_manager = RedisManageModel(analysis_conf.redis_info['host'],
                                 analysis_conf.redis_info['port'],
                                 analysis_conf.redis_info['db'],
                                 analysis_conf.redis_info['password'])

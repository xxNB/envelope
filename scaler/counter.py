# -*- coding: utf-8 -*-

import redis
import random


class RedisPipe:
    def __init__(self):
        self.pool = redis.ConnectionPool(host='localhost', port=6379,
                                         decode_responses=True)
        self._r = redis.Redis(connection_pool=self.pool)
        # self.package = "red"

    def setcrement(self, key, n):
        """ 总红包数 key"""
        self._r.set(key, n)

    def decrement(self, key):
        """红包总数标识key, 防止抢为0"""
        re = self._r.decr(key)
        return re

    def increment(self, key):
        """抢红包时的用户标识key, 针对同一用户的多次抢"""
        re = self._r.incr(key)
        return re


if __name__ == '__main__':
    c = RedisPipe()
    # c._r.set("red", 100)
    # c.setcrement(100)
    for i in range(100):
        key = "{}".format(i)
        print(key)
        c.setcrement(key, 0)
        for n in range(random.randint(0, 3)):
            re = c.increment(key)
            if re > 1:
                "{}号 您已经抢过了".format(key)
                c.decrement(key)
                break

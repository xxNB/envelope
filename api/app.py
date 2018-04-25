# -*- coding: utf-8 -*-

from pymongo import MongoClient
from scaler.counter import RedisPipe
from tornado.web import RequestHandler

pipe_user = RedisPipe()
pipe_red = RedisPipe()
pipe_red.setcrement("red", 100)
db = MongoClient('127.0.0.1', 27017)['red']['user']


class RobHandler(RequestHandler):
    """抢红包接口"""

    def get(self):
        name = self.get_argument("name", "")
        if not pipe_user._r.exists(name):
            pipe_user.setcrement(name, 0)
        re = pipe_user.increment(name)
        if re > 1:
            pipe_user.decrement(name)
            return self.write({"res": "该红包你已经抢过"})
        red_last = pipe_red.decrement("red")
        if red_last > 0:
            db.insert({"user": name})
            return self.write({"res": "{}，恭喜你，抢到红包啦".format(name)})
        if red_last < 0:
            return self.write({"res": "该红包已经抢完了，下次再来"})

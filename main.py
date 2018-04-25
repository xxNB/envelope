# -*- coding: utf-8 -*-

from tornado import ioloop
from api import app
from tornado.web import Application


def make_app():
    return Application([(r'/api/redpost', app.RobHandler),])


if __name__ == '__main__':
    app = make_app()
    app.listen('8010')
    ioloop.IOLoop.instance().start()

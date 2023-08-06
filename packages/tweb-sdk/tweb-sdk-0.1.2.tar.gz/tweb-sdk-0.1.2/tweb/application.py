# coding=utf-8

import config
import importlib
import os
import logging

import tornado.web
from .base_handler import BaseHandler
from tornado.web import StaticFileHandler


class Application(tornado.web.Application):
    def __init__(self):

        base_handlers = [
            (r'.*', BaseHandler),
            (r"/static/(.*)", StaticFileHandler, {"path": '/static'})
        ]

        settings = config.TornadoSettings

        tornado.web.Application.__init__(self, base_handlers, **settings)

    def scan_routes(self):
        path = 'routes'
        list_dirs = os.walk(path)
        for dirName, subdirList, fileList in list_dirs:
            for file_name in fileList:
                if file_name[-3:] != ".py":
                    continue
                if file_name == "__init__.py":
                    continue
                if file_name[-11:] == "_exclude.py":
                    continue

                module_name = file_name.replace('.py', '')
                route_module = importlib.import_module('{}.{}'.format(path, module_name))
                rs = route_module.routes
                if rs is None:
                    continue

                logging.info('route [/%s/%s] added' % (route_module.base, module_name))
                self.add_handlers(r'.*', rs)
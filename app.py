#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from config import Config
from trainier import AppConfig

AppConfig.init_path()

from trainier.util.logger import Log
from trainier.util.staticify import static_templates
from trainier.web import urls

if sys.version_info < (3, 6):
    print("please use python 3.6 or above.")
    sys.exit(-1)
sys.path.append('trainier')


def main() -> None:

    # static_templates(AppConfig.TEMPLATE, AppConfig.STATIC)

    app: Application = Application(urls)
    server: HTTPServer = HTTPServer(app)
    server.listen(Config.PORT, Config.HOST)
    Log.trainier.info('tornado start 1 process. listen on %s:%s', Config.HOST, Config.PORT)

    IOLoop.instance().start()


if __name__ == '__main__':
    main()

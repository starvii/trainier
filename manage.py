#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python 3.7 (>=3.5)
depends on: flask / sqlalchemy / flask_sqlalchemy
front-end:  bulma / vue.js
"""

from __future__ import print_function
import sys

if sys.version_info.major < 3 or (sys.version_info.major == 3 and sys.version_info.minor < 5):
    print('must use python version >= 3.5')
    sys.exit(-1)

from flask import Flask
from werkzeug.routing import BaseConverter
from trainier import Config, set_flask_app, get_flask_app
from trainier.logger import  logger


class RegexConverter(BaseConverter):
    """ flask regex url pattern """

    def __init__(self, map, *args) -> None:
        super().__init__(map)
        self.map = map
        self.regex = args[0]


def bind_views() -> None:
    app = get_flask_app()
    import trainier.page
    logger.info('%s loaded.', trainier.page)
    import trainier.api.imp.controller
    app.register_blueprint(trainier.api.imp.controller.blueprint)
    logger.info('%s loaded.', trainier.api.imp.controller)
    import trainier.api.question.controller
    app.register_blueprint(trainier.api.question.controller.blueprint)
    logger.info('%s loaded.', trainier.api.question.controller)


def main() -> None:
    c = Config.default
    app = Flask(c.APP_NAME, static_url_path='', template_folder=c.VIEW_PATH, static_folder=c.STATIC_PATH,
                root_path=c.APP_PATH)
    set_flask_app(app)
    app.url_map.converters['regex'] = RegexConverter
    bind_views()
    app.run(host=c.HOST, port=c.PORT, debug=c.DEBUG)


if __name__ == '__main__':
    main()

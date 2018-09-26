#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

from flask import Flask


class _ConfigBase:
    APP_NAME: str = 'trainier'
    HOST: str = '127.0.0.1'
    PORT: str = 80
    SECRET_KEY = b'train1erSecret!'
    APP_PATH: str = str(Path(__file__).parent.parent)
    STATIC_PATH: str = str(Path(APP_PATH) / Path('static'))
    VIEW_PATH: str = str(Path(APP_PATH) / Path('template'))
    LOG_PATH: str = str(Path(APP_PATH) / Path('log'))
    SQLALCHEMY_COMMIT_ON_TEARDOWN: bool = True
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = str(Path(APP_PATH) / Path('database/dev-db.sqlite'))


class DevelopmentConfig(_ConfigBase):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = str(Path(_ConfigBase().APP_PATH) / Path('database/dev-db.sqlite'))


class TestingConfig(_ConfigBase):
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = str(Path(_ConfigBase().APP_PATH) / Path('database/test-db.sqlite'))


class ProductionConfig(_ConfigBase):
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str = str(Path(_ConfigBase().APP_PATH) / Path('database/db.sqlite'))


class Config:
    development = DevelopmentConfig
    testing = TestingConfig
    production = ProductionConfig
    default = DevelopmentConfig


_this = sys.modules[__name__]


def get_flask_app() -> Flask:
    app: Flask = _this._flaskApp
    if app is not None and type(app) == Flask:
        return app
    else:
        raise RuntimeError('cannot get flask current app.')


def set_flask_app(app: Flask):
    _this._flaskApp = app

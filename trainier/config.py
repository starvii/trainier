#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path


class AppConfig:
    BASE: Path = Path(__file__).absolute().parent.parent
    STATIC: Path = BASE / Path('static')
    HTML: Path = BASE / Path('html')
    TEMPLATE: Path = BASE / Path('template')
    DATABASE: Path = BASE / Path('database')
    DB_FILE: Path = DATABASE / Path('db.sqlite')
    LOG: Path = BASE / Path('log')
    SECRET: bytes = b'HelloW0r1d!'

    @staticmethod
    def init_path() -> None:
        if not AppConfig.HTML.exists():
            AppConfig.HTML.mkdir()
        if not AppConfig.DATABASE.exists():
            AppConfig.DATABASE.mkdir()
        if not AppConfig.LOG.exists():
            AppConfig.LOG.mkdir()
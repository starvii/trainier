#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from logging import Logger, StreamHandler, Handler, Formatter, getLogger, DEBUG
from logging.handlers import RotatingFileHandler
from pathlib import Path

from trainier import AppConfig


def make_log(name: str) -> Logger:
    log_file: str = str(Path(AppConfig.LOG) / Path(name + '.log'))
    fmt: str = '%(asctime)s [%(filename)s:%(lineno)s][%(name)s][%(levelname)s] - %(message)s'
    file_handler: Handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
    std_handler: Handler = StreamHandler()
    formatter = Formatter(fmt)
    file_handler.setFormatter(formatter)
    std_handler.setFormatter(formatter)
    logger: Logger = getLogger(name)
    logger.addHandler(std_handler)
    logger.addHandler(file_handler)
    logger.setLevel(DEBUG)
    return logger


class Log:
    trainier: Logger = make_log('trainier')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from typing import Dict, Tuple

from trainier.util import const
from trainier.util.logger import Log

const.PAGE_NUMBER_DEFAULT: int = 1
const.PAGE_SIZE_DEFAULT: int = 10
const.PAGE_SIZES: Tuple = (10, 15, 30, 50, 100)


def process_page_parameters(arguments: Dict) -> (int, int, str):
    page = arguments.get('page')
    size = arguments.get('size')
    keyword = arguments.get('keyword')
    try:
        page = int(page[0])
    except Exception as e:
        page = const.PAGE_NUMBER_DEFAULT
        Log.trainier.debug(e)
    try:
        size = int(size[0])
        if size not in const.PAGE_SIZES:
            raise ValueError('size not in PAGE_SIZES')
    except Exception as e:
        size = const.PAGE_SIZE_DEFAULT
        Log.trainier.debug(e)
    try:
        keyword = '%' + keyword.decode() + '%'
    except Exception as e:
        keyword = ''
        Log.trainier.debug(e)
    Log.trainier.debug('get: page = %s, size = %s, keyword = %s', page, size, keyword)
    return page, size, keyword


def jsonify(val: object) -> str:
    return json.dumps(val, ensure_ascii=False, separators=(',', ':'))
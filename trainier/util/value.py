#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from typing import Dict, Tuple, Any

from bs4 import BeautifulSoup

from trainier.util import const
from trainier.util.base32 import encode_for_id
from trainier.util.logger import Log
from trainier.util.object_id import ObjectId

const.PAGE_NUMBER_DEFAULT: int = 1
const.PAGE_SIZES: Tuple = (10, 15, 30, 50, 100)
const.PAGE_SIZE_DEFAULT: int = const.PAGE_SIZES[0]


def _parameter_from_request(parameter: str, arguments: Dict, body: bytes, body_json: Dict) -> (Any, Dict):
    if parameter in arguments:
        return arguments.get(parameter)[0], body_json
    if body_json is not None and parameter in body_json:
        return body_json.get(parameter)[0], body_json
    if body_json is None:
        try:
            j: Dict = json.loads(body)
            return j.get(parameter)[0], j
        except Exception as e:
            Log.trainier.debug(e)
    return None, None


def process_page_parameters(arguments: Dict, body: bytes) -> (int, int, str):
    body_json: Dict = None

    page, body_json = _parameter_from_request('page', arguments, body, body_json)
    try:
        page: int = int(page)
    except Exception as e:
        Log.trainier.debug(e)
        page = const.PAGE_NUMBER_DEFAULT

    size, body_json = _parameter_from_request('size', arguments, body, body_json)
    try:
        size: int = int(size)
        if size not in const.PAGE_SIZES:
            raise ValueError('size not in PAGE_SIZES')
    except Exception as e:
        Log.trainier.debug(e)
        size = const.PAGE_SIZE_DEFAULT

    kw, body_json = _parameter_from_request('keyword', arguments, body, body_json)
    try:
        keyword: str = kw.decode().strip()
        if len(keyword) > 0:
            keyword = f'%{keyword}%'
    except Exception as e:
        Log.trainier.debug(e)
        keyword = ''

    Log.trainier.debug('get: page = %s, size = %s, keyword = %s', page, size, keyword)
    return page, size, keyword


def jsonify(val: object) -> str:
    return json.dumps(val, ensure_ascii=False, separators=(',', ':'))


def b32_obj_id() -> str:
    return encode_for_id(ObjectId.gen_id()).lower().decode()


def html_strip(val: str) -> str:
    if val is None:
        return ''
    soup: BeautifulSoup = BeautifulSoup(val, features='html.parser')
    return soup.get_text(strip=True)
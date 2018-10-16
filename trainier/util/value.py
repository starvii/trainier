#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
from typing import Pattern, Dict, List

from bs4 import BeautifulSoup
from requests import Request

HEX_PATTERN: Pattern = re.compile(r'[0-9a-f]{24}')
BASE64_PATTERN: Pattern = re.compile(r'^[\-_0-9A-Za-z]{32}$')


def not_none(val) -> str:
    if val is None:
        return ''
    elif type(val) == str:
        return val.strip()
    else:
        return str(val).strip()


def html_strip(val: str) -> str:
    if val is None:
        return ''
    soup: BeautifulSoup = BeautifulSoup(val, features="lxml")
    return soup.get_text(strip=True)


def jsonify(val: object) -> str:
    return json.dumps(val, ensure_ascii=False, separators=(',', ':'))


def read_str_json_or_cookie(key: str, _json: Dict, req: Request, def_val: str or None = '') -> str or None:
    if key in _json:
        return str(_json[key])
    if key in req.cookies and len(req.cookies[key]) > 0:
        return req.cookies[key]
    return def_val


def read_int_json_or_cookie(key: str, _json: Dict, req: Request, def_val: int = 0) -> int:
    if key in _json and type(_json[key]) == int:
        return _json[key]
    try:
        if key in req.cookies and len(req.cookies[key]) > 0:
            return int(req.cookies[key])
    except ValueError:
        pass
    return def_val


def read_list_json(key: str, _json: Dict, def_val: List = None) -> List or None:
    if key in _json and type(_json[key]) == list:
        return _json[key]
    return def_val

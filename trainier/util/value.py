#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Pattern, Dict
import re
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


def read_str_json_or_cookie(key: str, _json: Dict, req: Request, def_val: str = '') -> str:
    if key in _json and len(_json[key]) > 0:
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

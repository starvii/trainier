#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Pattern
import re
import base64

HEX_PATTERN: Pattern = re.compile(r'[0-9a-f]{24}')
BASE64_PATTERN: Pattern = re.compile(r'^[\-_0-9A-Za-z]{32}$')


def not_none(val) -> str:
    if val is None:
        return ''
    elif type(val) == str:
        return val.strip()
    else:
        return str(val).strip()


def extract_id(web_id: str) -> str:
    if BASE64_PATTERN.match(web_id):
        _ = base64.urlsafe_b64decode(web_id).decode()
        if HEX_PATTERN.match(_):
            return _
    return web_id

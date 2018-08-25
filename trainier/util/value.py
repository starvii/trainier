#!/usr/bin/env python
# -*- coding: utf-8 -*-

def NoNone(val) -> str:
    if val is None:
        return ''
    elif type(val) == str:
        return val.strip()
    else:
        return str(val).strip()
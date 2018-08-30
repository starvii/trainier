#!/usr/bin/env python
# -*- coding: utf-8 -*-


def not_none(val) -> str:
    if val is None:
        return ''
    elif type(val) == str:
        return val.strip()
    else:
        return str(val).strip()


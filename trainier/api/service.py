#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, Set, List
from sqlalchemy.orm.attributes import InstrumentedAttribute


def __deal_fields(fields: Set[str or InstrumentedAttribute]) -> Set[str]:
    _set: Set[str] = set()
    for f in fields:
        if type(f) == str:
            _set.add(f)
        elif type(f) == InstrumentedAttribute:
            s: str = str(f)
            p: int = s.rfind('.')
            if p >= 0:
                _set.add(s[p + 1:])
            else:
                _set.add(s)
    return _set


def labelify(obj: object, fields: Set[str or InstrumentedAttribute] = None) -> Dict or List[Dict] or None:
    if type(obj) == list:
        l: List = obj
        return __list_to_dict(l, fields)
    else:
        return __entity_to_dict(obj, fields)


def __entity_to_dict(obj: object, fields: Set[str or InstrumentedAttribute] = None) -> Dict or None:
    r: Dict = dict()
    if obj is None:
        return None
    if fields is not None and len(fields) > 0:
        fs: Set[str] = __deal_fields(fields)
    else:
        fs: Set[str] = set([_ for _ in obj.__dict__.keys() if not _.startswith('_')])
    for k, v in obj.__dict__.items():
        if k in fs:
            r[k] = v
    return r


def __list_to_dict(lst: List[object], fields: Set[str or InstrumentedAttribute] = None) -> List[Dict] or None:
    r: List[Dict] = list()
    if lst is None or len(lst) == 0:
        return None
    if fields is not None and len(fields) > 0:
        fs: Set[str] = __deal_fields(fields)
    else:
        obj: object = lst[0]
        fs: Set[str] = set([_ for _ in obj.__dict__.keys() if not _.startswith('_')])
    for obj in lst:
        dct = dict()
        for k, v in obj.__dict__.items():
            if k in fs:
                dct[k] = v
        r.append(dct)
    return r


def dict_to_entity(_dict, entity=None) -> object:
    return entity

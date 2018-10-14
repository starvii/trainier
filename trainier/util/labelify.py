#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
从Sqlalchemy实体中筛选出必要的数据（供前台展示使用）
"""

from typing import Dict, Set, List

from sqlalchemy.orm.attributes import InstrumentedAttribute

from dao.model import Trunk, Option


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


def sub(obj: object, fields: Set[str or InstrumentedAttribute]) -> Set[str] or None:
    if obj is None:
        return None
    if obj._sa_class_manager is None:
        return None
    if obj._sa_class_manager._all_key_set is None:
        return None
    fs: Set[str] = obj._sa_class_manager._all_key_set
    sub_fs = __deal_fields(fields)
    return fs - sub_fs


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


def dict_to_entity(_dict: Dict, target: object, fields: Set[str or InstrumentedAttribute] = None) -> object or None:
    if target is None:
        return None
    if target._sa_class_manager is None:
        return None
    if target._sa_class_manager._all_key_set is None:
        return None

    if fields is not None and len(fields) > 0:
        fs: Set[str] = __deal_fields(fields)
    else:
        fs: Set[str] = target._sa_class_manager._all_key_set
    for k, v in _dict.items():
        if k in fs and k in target._sa_class_manager._all_key_set:
            target.__dict__[k] = v
    return target


def list_to_entities(_list: List[Dict],
                     sample: object,
                     fields: Set[str or InstrumentedAttribute] = None) -> List[object] or None:
    if _list is None or len(_list) == 0:
        return None
    if sample is None:
        return None
    if sample._sa_class_manager is None:
        return None
    if sample._sa_class_manager._all_key_set is None:
        return None

    if fields is not None and len(fields) > 0:
        fs: Set[str] = __deal_fields(fields)
    else:
        fs: Set[str] = sample._sa_class_manager._all_key_set
    l: List = list()
    for d in _list:
        o = sample.__class__()
        for k, v in d.items():
            if k in fs and k in sample._sa_class_manager._all_key_set:
                o.__dict__[k] = v
        l.append(o)
    return l

def trans_trunk_to_dict(trunk: Trunk, trunk_fields: Set[InstrumentedAttribute] = None,
                        option_fields: Set[InstrumentedAttribute] = None) -> Dict:
    trunk_dict: Dict = labelify(trunk, trunk_fields)

    trunk_dict['en_trunk_len'] = len(trunk.en_trunk_text)
    trunk_dict['cn_trunk_len'] = len(trunk.cn_trunk_text)

    trunks: List[Trunk] = trunk.__dict__.get('_trunks')
    if trunks is not None and len(trunks) > 0:
        trunk_list: List[Dict] = list()
        for trunk_child in trunks:
            trunk_child_dict: Dict = trans_trunk_to_dict(trunk_child)
            trunk_list.append(trunk_child_dict)
        trunk_dict['trunks'] = trunk_list
    else:
        options: List[Option] = trunk.__dict__.get('_options')
        options_dict: Dict = labelify(options, option_fields)
        trunk_dict['options'] = options_dict
    return trunk_dict


def trans_dict_to_trunk(trunk_dict: Dict, trunk_fields: Set[InstrumentedAttribute] = None,
                        option_fields: Set[InstrumentedAttribute] = None) -> Trunk:
    trunk: Trunk = dict_to_entity(trunk_dict, Trunk(), trunk_fields)
    if 'trunks' in trunk_dict and len(trunk_dict['trunks']) > 0:
        # 存在子问题
        trunk_children_dict: Dict = trunk_dict['trunks']
        trunk_children: List[Trunk] = list()
        trunk.__setattr__('_trunks', trunk_children)
        for trunk_child_dict in trunk_children_dict:
            trunk_child: Trunk = trans_dict_to_trunk(trunk_child_dict)
            trunk_children.append(trunk_child)
    elif 'options' in trunk_dict and len(trunk_dict['options']) > 0:
        options_dict: List[Dict] = trunk_dict['options']
        options: List[Option] = list_to_entities(options_dict, Option(), option_fields)
        trunk.__setattr__('_options', options)
    return trunk

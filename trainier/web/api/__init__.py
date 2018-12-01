#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Dict, Set

from playhouse.shortcuts import model_to_dict, dict_to_model

from dao.model import Trunk, Option


class CannotFindError(LookupError):
    def __init__(self, exception_wrapper: Exception or None, *args: object) -> None:
        super().__init__(*args)
        self.exception_wrapper = exception_wrapper


class ErrorInQueryError(LookupError):
    def __init__(self, exception_wrapper: Exception or None, *args: object) -> None:
        super().__init__(*args)
        self.exception_wrapper = exception_wrapper


class TrunkIntegrityError(ValueError):
    def __init__(self, exception_wrapper: Exception or None, *args: object) -> None:
        super().__init__(*args)
        self.exception_wrapper = exception_wrapper


def trunk_to_dict(trunk: Trunk, trunk_exclude: Set = None, option_exclude: Set = None, functions: List = None) -> Dict:
    trunk_dict: Dict = model_to_dict(trunk, exclude=trunk_exclude)
    if functions is not None and len(functions) > 0:
        for func in functions:
            func(trunk, trunk_dict)
    if len(trunk.__dict__.get('trunks', [])) > 0:
        trunks: List[Trunk] = trunk.__dict__['trunks']
        trunk_list: List[Dict] = list()
        for trunk_child in trunks:
            trunk_child_dict: Dict = trunk_to_dict(trunk_child, trunk_exclude, option_exclude, functions)
            trunk_list.append(trunk_child_dict)
        trunk_dict['trunks'] = trunk_list
    elif len(trunk.__dict__.get('options', [])) > 0:
        options: List[Option] = trunk.__dict__['options']
        options_list: List[Dict] = [model_to_dict(o, exclude=option_exclude) for o in options]
        trunk_dict['options'] = options_list
    else:
        raise TrunkIntegrityError(None, f'Trunk: {trunk} have something wrong of integrity')
    return trunk_dict


def dict_to_trunk(trunk_dict: Dict) -> Trunk:
    if 'options' in trunk_dict and 'trunks' in trunk_dict:
        raise TrunkIntegrityError(None, f'options and trunks all in trunk dict {trunk_dict}')
    if 'options' not in trunk_dict and 'trunks' not in trunk_dict:
        raise TrunkIntegrityError(None, f'options or trunks not in trunk dict {trunk_dict}')
    trunk: Trunk = dict_to_model(Trunk, trunk_dict, True)
    if 'trunks' in trunk_dict:
        if isinstance(trunk_dict['trunks'], List) and len(trunk_dict['trunks']) > 0:
            trunks: List[Dict] = trunk_dict['trunks']
            trunk.__dict__['trunks'] = [dict_to_trunk(t) for t in trunks]
        else:
            raise TrunkIntegrityError(None, f'trunks not correct in trunk dict {trunk_dict}')
    else:
        if isinstance(trunk_dict.get('options'), list) and len(trunk_dict.get('options')) > 0:
            options: List[Dict] = trunk_dict['options']
            trunk.__dict__['options'] = [dict_to_model(Option, o, True) for o in options]
        else:
            raise TrunkIntegrityError(None, f'options not correct in trunk dict {trunk_dict}')
    return trunk

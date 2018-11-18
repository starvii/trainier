#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from trainier.dao.model import Trunk, Option
from trainier.util import const

const.ROOT_NODE = 'root'

class QuestionService:
    @staticmethod
    def select_trunk_by_id(entity_id: str) -> Trunk or None:
        pass

    @staticmethod
    def select_next_prev_by_id(entity_id: str) -> (str, str):
        pass

    @staticmethod
    def select_options_by_trunk_id(trunk_id: str) -> List[Option]:
        pass

    @staticmethod
    def select_trunks(page: int, size: int, keyword: str, ids: List[str] = None) -> (List[Trunk], int):
        pass

    @staticmethod
    def save(trunk: Trunk) -> None:
        pass
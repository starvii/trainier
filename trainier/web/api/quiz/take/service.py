#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from trainier.dao.model import Trunk, Option, Result
from trainier.dao.orm import db
from trainier.web.api.question.service import QuestionService


class TakeService:

    @staticmethod
    def trunk_to_dict(trunk: Trunk):
        trunk_exclude = {
            Trunk.db_id,
            Trunk.en_trunk_text,
            Trunk.cn_trunk_text,
            Trunk.explanation,
            Trunk.source,
            Trunk.level,
            Trunk.comment,
            Trunk.order_num,
            Trunk.parent_id,

        }
        option_exclude = {
            Option.db_id,
            Option.trunk_id,
            Option.code,
            Option.order_num,
        }
        return QuestionService.trunk_to_dict(trunk, trunk_exclude, option_exclude, [QuestionService.view_trunk_length])

    @staticmethod
    def save(results: List[Result]):
        with db.connection_context():
            with db.transaction() as tx:
                pass
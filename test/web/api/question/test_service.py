# -*- coding: utf-8 -*-

import unittest
from trainier.web.api.question.service import *

class TestService(unittest.TestCase):

    def test_service_save(self):
        trunk: Trunk = Trunk()
        # trunk.entity_id = '123456'
        trunk.code = 'A2/3/6'
        trunk._options = [
            Option(

            )
        ]
        QuestionService.save(trunk)

    def test_service_select_trunk_by_id(self):
        entity_id = '0p2sp2g40z3sj0y20s7b'
        trunk = QuestionService.select_trunk_by_id(entity_id)
        print(trunk)

    def test_service_select_trunks(self):
        query = Trunk.select().where((Trunk.parent_id.is_null()) | (Trunk.parent_id == '') | (Trunk.parent_id == const.ROOT_NODE))
        print(query.sql())
        print([x for x in query])
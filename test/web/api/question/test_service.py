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
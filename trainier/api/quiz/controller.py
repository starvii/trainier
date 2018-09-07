#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测验题目制定（管理）
题目列表（测验）
题目页面（测验）
结果页面/保存（测验）
"""

import json
from logging import Logger
import base64
import binascii
from typing import Dict, List, Set
from flask import Blueprint, Response, Request, request, make_response, abort
from sqlalchemy.orm.attributes import InstrumentedAttribute
from trainier.model import Trunk, Option, Pic
from trainier.logger import logger
from trainier.api.service import dict_to_entity, list_to_entities
from trainier.api.question.service import QuestionService
from trainier.api.service import labelify

blueprint: Blueprint = Blueprint('api-quiz', __name__, url_prefix='/api/quiz')


class Quiz:

    @staticmethod
    def index() -> Response:
        pass

    @staticmethod
    def add() -> Response:
        pass

    @staticmethod
    def edit() -> Response:
        pass

    @staticmethod
    def remove() -> Response:
        pass

    @staticmethod
    def stat() -> Response:
        pass

    @staticmethod
    @blueprint.route('/<quiz_id>/<question_id>', methods=('GET',))
    def question(quiz_id: str, question_id: str) -> Response:
        """
        将结果保存在cookie中？
        :param quiz_id:
        :param question_id:
        :return:
        """
        pass

    @staticmethod
    @blueprint.route('/<quiz_id>/<question_id>', methods=('POST',))
    def answer(quiz_id: str, question_id: str) -> Response:
        pass

    @staticmethod
    def review(quiz_id: str, question_id: str) -> Response:
        pass

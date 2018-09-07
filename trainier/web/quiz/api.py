#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测验题目制定（管理）
题目列表（测验）
题目页面（测验）
结果页面/保存（测验）
"""

from flask import Blueprint, Response

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
    @blueprint.route('/<quiz_id>', methods=('POST',))
    def quiz(quiz_id: str) -> Response:
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

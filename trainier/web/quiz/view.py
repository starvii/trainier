#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测验题目制定（管理） quiz-list(search), quiz-create, quiz-modify, quiz-delete(X)
题目列表（测验） question-list, question-marked-list
题目页面（测验） question-view
结果页面/保存（测验） result, statistics
"""

import json
from typing import Dict, List, Set
from flask import Blueprint, Response, request, make_response, abort, render_template
from sqlalchemy.orm.attributes import InstrumentedAttribute
from util.logger import logger
from util.labelify import dict_to_entity, list_to_entities
from web.question.service import QuestionService
from util.labelify import labelify

blueprint: Blueprint = Blueprint('quiz', __name__, url_prefix='/quiz')


class API:
    @staticmethod
    @blueprint.route('/api', methods=('POST',))
    @blueprint.route('/api/', methods=('POST',))
    def api_quiz_index() -> Response:
        pass

    @staticmethod
    def api_quiz_get() -> Response:
        pass

    @staticmethod
    def api_quiz_create() -> Response:
        pass

    @staticmethod
    def api_quiz_modify() -> Response:
        pass

    @staticmethod
    def api_quiz_remove() -> Response:
        pass


class View:
    @staticmethod
    @blueprint.route('/', methods=('GET',))
    def quiz_index() -> str:
        """
        参数：page, size, keyword
        调用api:
            获取quiz列表
        :return:
        """
        return render_template('quiz/index.html')

    @staticmethod
    def quiz_edit():
        """
        参数: quiz_id
        调用api:
            获取quiz
            保存quiz（新建、修改）
        :return:
        """
        pass

    @staticmethod
    def question_index():
        """
        获取一项测验中的所有题目
        参数：quiz_id
        调用api：
            获取quiz
            获取question-list
        :return:
        """
        pass

    @staticmethod
    def question_answer():
        """
        获取一项题目，并可进行答题
        参数：quiz_id, trunk_id
        调用api：
            获取question
            提交答案
        :return:
        """
        pass

    @staticmethod
    def quiz_result():
        """
        计分和查看结果（全部、错误）
        参数：quiz_id, take_id?
        调用api：
            计分
        :return:
        """
        pass

    @staticmethod
    def statistics():
        """
        数据统计，全局来看，某道题做过几次、错误几次
        参数：

        :return:
        """
        pass

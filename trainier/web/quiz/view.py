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
from trainier.util.logger import logger
from trainier.dao.model import Quiz
from trainier.util.labelify import dict_to_entity, list_to_entities
from trainier.web.quiz.service import QuizService
from trainier.util.labelify import labelify
from trainier.util.value import read_int_json_or_cookie, read_str_json_or_cookie

blueprint: Blueprint = Blueprint('quiz', __name__, url_prefix='/quiz')


class API:
    @staticmethod
    # @blueprint.route('/api', methods=('POST',))
    @blueprint.route('/api/', methods=('POST',))
    def api_quiz_index() -> Response:
        try:
            data: bytes = request.data
            try:
                j: Dict = json.loads(data)
            except json.JSONDecodeError:
                j = dict()
            page = read_int_json_or_cookie('page', j, request, 1)
            size = read_int_json_or_cookie('size', j, request, 10)
            keyword = read_str_json_or_cookie('keyword', j, request, '')
            quiz, c = QuizService.select_quiz(page, size, keyword)
            if quiz is None or len(quiz) == 0:
                lst: List[Dict] = list()
            else:
                fields: Set[InstrumentedAttribute] = {
                    Quiz.entity_id,
                    Quiz.code,
                    Quiz.name,
                    Quiz.random_trunk,
                    Quiz.random_choice,
                }
                lst: List[Dict] = labelify(quiz, fields)
            r: Dict = dict(
                page=page,
                size=size,
                total=c,
                keyword=keyword,
                data=lst,
            )
            res: Response = make_response()
            res.content_type = 'application/json; charset=utf-8'
            res.data = json.dumps(r).encode()
            return res
        except Exception as e:
            logger.error(str(e))
            abort(500)

    @staticmethod
    # @blueprint.route('/api/<entity_id>', methods=('GET',))
    @blueprint.route('/api/<entity_id>/', methods=('GET',))
    def api_quiz_get(entity_id: str) -> Response:
        pass

    @staticmethod
    # @blueprint.route('/api/<entity_id>', methods=('POST',))
    @blueprint.route('/api/<entity_id>/', methods=('POST',))
    def api_quiz_trunks(entity_id: str) -> Response:
        pass

    @staticmethod
    # @blueprint.route('/api', methods=('PUT',))
    @blueprint.route('/api/', methods=('PUT',))
    def api_quiz_create() -> Response:
        pass

    @staticmethod
    # @blueprint.route('/api/<entity_id>', methods=('PUT',))
    @blueprint.route('/api/<entity_id>/', methods=('PUT',))
    def api_quiz_modify(entity_id: str) -> Response:
        pass

    @staticmethod
    # @blueprint.route('/api/<entity_id>', methods=('DELETE',))
    @blueprint.route('/api/<entity_id>/', methods=('DELETE',))
    def api_quiz_remove(entity_id: str) -> Response:
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
    @blueprint.route('/edit', methods=('GET',))
    def quiz_edit() -> str:
        """
        参数: quiz_id
        调用api:
            获取quiz
            保存quiz（新建、修改）
        :return:
        """
        return render_template('quiz/edit.html')

    @staticmethod
    def question_index() -> str:
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
    def question_answer() -> str:
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
    def quiz_result() -> str:
        """
        计分和查看结果（全部、错误）
        参数：quiz_id, take_id?
        调用api：
            计分
        :return:
        """
        pass

    @staticmethod
    def statistics() -> str:
        """
        数据统计，全局来看，某道题做过几次、错误几次
        参数：

        :return:
        """
        pass

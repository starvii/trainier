#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测验题目制定（管理） quiz-list(search), quiz-create, quiz-modify, quiz-delete(X)
"""

import json
from typing import Dict, List, Set
from flask import Blueprint, Response, request, make_response, abort, render_template
from sqlalchemy.orm.attributes import InstrumentedAttribute
from trainier.util.logger import logger
from trainier.dao.model import Quiz
from trainier.util.labelify import dict_to_entity, list_to_entities, labelify, sub
from trainier.web.quiz.service import QuizService
from trainier.util.value import read_int_json_or_cookie, read_str_json_or_cookie

blueprint: Blueprint = Blueprint('quiz', __name__, url_prefix='/quiz')

quiz_fields: Set[str] = sub(Quiz(), {Quiz.db_id})


class API:
    @staticmethod
    @blueprint.route('/api/', methods=('POST',))
    def api_quiz_index() -> Response:
        try:
            data: bytes = request.data
            try:
                j: Dict = json.loads(data)
            except json.JSONDecodeError:
                j: Dict = dict()
            page: int = read_int_json_or_cookie('page', j, request, 1)
            size: int = read_int_json_or_cookie('size', j, request, 10)
            keyword: str = read_str_json_or_cookie('keyword', j, request, '')

            quiz, c = QuizService.select_quiz(page, size, keyword)
            if quiz is None or len(quiz) == 0:
                lst: List[Dict] = list()
            else:
                fields: Set[InstrumentedAttribute] = {
                    Quiz.entity_id,
                    Quiz.code,
                    Quiz.name,
                    Quiz.comment,
                }
                lst: List[Dict] = labelify(quiz, fields)
            # 统计数量
            for q, d in zip(quiz, lst):
                count = len([_.strip() for _ in q.questions.split(',') if len(_.strip()) > 0])
                d['count'] = count
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
    @blueprint.route('/api/<entity_id>', methods=('GET',))
    def api_quiz_get(entity_id: str) -> Response:
        q: Quiz = QuizService.select_quiz_by_id(entity_id)
        if q is not None:
            r: Dict = labelify(q, quiz_fields)
            r['questions'] = q.questions.split(',')
            res: Response = make_response()
            res.content_type = 'application/json; charset=utf-8'
            res.data = json.dumps(r).encode()
            return res
        else:
            abort(404)

    @staticmethod
    @blueprint.route('/api/', methods=('PUT',))
    def api_quiz_create() -> Response:
        try:
            data: bytes = request.data
            try:
                j: Dict = json.loads(data)
            except json.JSONDecodeError:
                j: Dict = dict()
            if 'quiz' in j and 'questions' in j['quiz'] and type(j['quiz']['questions']) == list:
                j['quiz']['questions'] = ','.join(j['quiz']['questions'])
            q: Quiz = Quiz()
            q = dict_to_entity(j['quiz'], q)
            QuizService.save(q)
            res: Response = make_response()
            res.content_type = 'application/json; charset=utf-8'
            res.data = json.dumps(dict(result=True)).encode()
            return res
        except Exception as e:
            logger.error(e)
            abort(500)

    @staticmethod
    @blueprint.route('/api/<entity_id>', methods=('PUT',))
    def api_quiz_modify(entity_id: str) -> Response:
        try:
            data: bytes = request.data
            try:
                j: Dict = json.loads(data)
            except json.JSONDecodeError:
                j: Dict = dict()
            if 'quiz' in j and 'questions' in j['quiz'] and type(j['quiz']['questions']) == list:
                j['quiz']['questions'] = ','.join(j['quiz']['questions'])
            q: Quiz = Quiz()
            q = dict_to_entity(j['quiz'], q)
            if q.entity_id != entity_id:
                abort(404)
            QuizService.save(q)
            res: Response = make_response()
            res.content_type = 'application/json; charset=utf-8'
            res.data = json.dumps(dict(result=True)).encode()
            return res
        except Exception as e:
            logger.error(e)
            abort(500)

    @staticmethod
    @blueprint.route('/api/<entity_id>', methods=('DELETE',))
    def api_quiz_remove(entity_id: str) -> Response:
        """
        DELETE /api/<entity_id>
        暂不提供删除功能
        :param entity_id:
        :return:
        """
        pass


class View:
    @staticmethod
    @blueprint.route('/', methods=('GET',))
    def view_index() -> str:
        """
        参数：page, size, keyword
        调用api:
            获取quiz列表
        :return:
        """
        return render_template('quiz/index.html')

    @staticmethod
    @blueprint.route('/edit', methods=('GET',))
    def view_edit() -> str:
        """
        参数: quiz_id
        调用api:
            获取quiz
            保存quiz（新建、修改）
        :return:
        """
        return render_template('quiz/edit.html')

    @staticmethod
    @blueprint.route('/view', methods=('GET',))
    def view_view() -> str:
        """
        参数: quiz_id
        调用api:
            获取quiz
            保存quiz（新建、修改）
        :return:
        """
        return render_template('quiz/view.html')

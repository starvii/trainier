#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测验题目制定（管理） quiz-list(search), quiz-create, quiz-modify, quiz-delete(X)
题目列表（测验） question-list, question-marked-list
题目页面（测验） question-view
结果页面/保存（测验） result, statistics
"""

import json
from typing import Dict, List

from flask import Blueprint, Response, make_response, abort, render_template

from trainier import Config
from trainier.dao.model import Quiz
from trainier.util.labelify import labelify
from trainier.util.logger import logger
from trainier.util.sec_cookie import Codec
from trainier.web.quiz.service import QuizService

blueprint: Blueprint = Blueprint('quiz_take', __name__, url_prefix='/quiz/take')


class API:
    @staticmethod
    @blueprint.route('/api/<entity_id>', methods=('GET',))
    def api_take_start(entity_id: str) -> Response:
        try:
            quiz: Quiz = QuizService.select_quiz_by_id(entity_id)
            if quiz is None:
                abort(404)
            # 哪些数据明文？
            # code name random_trunk random_choice comment
            # 哪些数据要加密？
            # entity_id questions
            r: Dict = labelify(quiz, {Quiz.code, Quiz.name, Quiz.random_trunk, Quiz.random_choice})
            q: List[str] = [_.strip() for _ in quiz.questions.split(',') if len(_.strip()) > 0]
            d: Dict[str, List] = dict()
            for _ in q:
                d[_] = list()
            c: Dict = dict(
                entity_id=entity_id,
                question=q,
                answer=d,
            )
            cs: str = Codec(Config.default.SECRET_KEY).enc_dict(c)
            # r['cookie'] = cs
            res: Response = make_response(json.dumps(r).encode())
            res.content_type = 'application/json; charset=utf-8'
            # res.content_type = 'text/html; charset=utf-8'
            # res.data = json.dumps(r).encode()
            res.set_cookie('quiz', value=cs)
            return res
        except Exception as e:
            logger.error(str(e))
            abort(500)


class View:
    @staticmethod
    @blueprint.route('/', methods=('GET',))
    def view_index() -> str:
        return render_template('quiz/take/index.html')

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

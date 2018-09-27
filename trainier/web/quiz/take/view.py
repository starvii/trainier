#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
题目列表（测验） question-list, question-marked-list
题目页面（测验） question-view
结果页面/保存（测验） result, statistics
"""

import json
from typing import Dict, List, Set
from urllib.parse import quote, unquote
import random
import string

from flask import Blueprint, Response, Request, make_response, abort, render_template, request

from trainier import Config
from trainier.dao.model import Quiz, Trunk, Option, Pic
from trainier.util.labelify import labelify
from trainier.util.logger import logger
from trainier.util.sec_cookie import Codec
from trainier.web.quiz.service import QuizService
from trainier.web.question.service import QuestionService

blueprint: Blueprint = Blueprint('quiz_take', __name__, url_prefix='/quiz/take')

codec: Codec = Codec(Config.default.SECRET_KEY)

trunk_fields = {
    Trunk.entity_id,
    Trunk.code,
    Trunk.en_trunk,
    Trunk.en_trunk,
    Trunk.source,
    Trunk.level,
}

option_fields = {
    Option.entity_id,
    Option.en_option,
    Option.cn_option,
}

pic_fields = {
    Pic.entity_id,
    Pic.code,
    Pic.name,
    Pic.data,
    Pic.source,
    Pic.order_num,
    Pic.comment,
}


class API:
    @staticmethod
    @blueprint.route('/api/<entity_id>', methods=('GET',))
    def api_take_start(entity_id: str) -> Response:
        try:
            quiz: Quiz = QuizService.select_quiz_by_id(entity_id)
            if quiz is None:
                abort(404)
            quiz_dict: Dict = labelify(quiz)
            question_id_list: List[str] = [_.strip() for _ in quiz.questions.split(',') if len(_.strip()) > 0]
            if quiz.random_trunk:
                random.shuffle(question_id_list)
            quiz_dict['questions'] = list()
            for e in question_id_list:
                question: Dict = dict(
                    id=e,
                    marked=False,
                    answer='',
                    seed=-1,
                )
                if quiz.random_choice:
                    question['seed'] = random.randint(0, 65535)
                quiz_dict['questions'].append(question)

            c: str = quote(codec.enc_dict(quiz_dict))
            res: Response = make_response(json.dumps(dict(result=True)).encode())
            res.content_type = 'application/json; charset=utf-8'
            res.set_cookie('quiz', value=c)
            return res
        except Exception as e:
            logger.error(str(e))
            abort(500)

    @staticmethod
    def __deal_submit(quiz_dict: Dict, post_dict: Dict) -> Dict:
        """
        将提交的结果保存进cookie
        :param quiz_dict:
        :param post_dict:
        :return:
        """
        idx: int = post_dict['idx'] - 1
        answer: str = post_dict['answer']
        marked: bool = post_dict['marked']
        question: Dict = quiz_dict['questions'][idx]
        question['answer'] = answer
        question['marked'] = marked
        return quiz_dict

    @staticmethod
    def __deal_switch(quiz_dict: Dict, question_idx: int) -> Dict:
        """
        根据 question_idx 从数据库内读取题目数据
        :param quiz_dict:
        :param question_idx:
        :return:
        """
        # 读取新的数据
        question: Dict = quiz_dict['questions'][question_idx - 1]
        qid = question['entity_id']
        trunk: Trunk = None
        options: List[Option] = None
        pics: List[Pic] = None
        trunk, options, pics = QuestionService.select_trunk_options_pics_by_id(qid)
        # 判断是单选还是多选
        if trunk is None:
            raise ValueError('cannot select trunk by id:' + qid)
        trunk_dict: Dict = labelify(trunk, trunk_fields)
        counter: int = len([_ for _ in options if _.is_true])
        if counter == 1:
            trunk_dict['multi_choice'] = False
        elif counter > 1:
            trunk_dict['multi_choice'] = True
        options_dict: Dict = labelify(options, option_fields)
        # 对选项进行排序
        if quiz_dict.get('random_choice'):
            random.seed(question.get('seed'))
            random.shuffle(options_dict)
        # 加上之前保存的答题结果
        for option_dict in options_dict:
            option_dict['is_true'] = False
        answer: str = question['answer'].strip().upper()
        for ch in answer:
            idx: int = string.ascii_uppercase.find(ch)
            if idx < 0 or idx >= len(answer):
                raise ValueError('something wrong in answer {} of {}'.format(answer, str(question)))
            options_dict[idx]['is_true'] = True
        pics_dict: Dict = labelify(pics, pic_fields)
        ret: Dict = dict(
            trunk=trunk_dict,
            options=options_dict,
            pics=pics_dict,
        )
        return ret

    @staticmethod
    def __list_status(quiz_dict: Dict) -> List[Dict]:
        # 题目列表
        question_list: List[Dict] = [dict(marked=question['marked'], answer=question['answer']) for question in
                                     quiz_dict['questions']]
        return question_list

    @staticmethod
    @blueprint.route('/api/<int:question_idx>', methods=('POST',))
    def api_take_submit_switch(question_idx: int) -> Response:
        try:
            cookie: str = request.cookies.get('quiz')
            cookie = unquote(cookie)
            quiz_dict: Dict = codec.dec_dict(cookie)
            # 保存提交的结果
            data: bytes = request.data
            try:
                post_dict: Dict = json.loads(data)
                quiz_dict = API.__deal_submit(quiz_dict, post_dict)
            except json.JSONDecodeError:
                # 如果没有提交数据或提交有误，就不进行更新
                pass
            ret: Dict = API.__deal_switch(quiz_dict, question_idx)
            ret['question_list'] = API.__list_status(quiz_dict)
            enc_quiz: str = codec.enc_dict(quiz_dict)

            res: Response = make_response(json.dumps(ret).encode())
            res.content_type = 'application/json; charset=utf-8'
            res.set_cookie('quiz', value=enc_quiz)
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

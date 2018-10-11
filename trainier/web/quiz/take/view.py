#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
题目列表（测验） question-list, question-marked-list
题目页面（测验） question-view
结果页面/保存（测验） result, statistics
"""

import json
import random
import string
from typing import Dict, List
from urllib.parse import quote, unquote

from flask import Blueprint, Response, make_response, abort, render_template, request

from trainier import Config
from trainier.dao.model import Quiz, Trunk, Option, Result
from trainier.util.labelify import labelify
from trainier.util.logger import logger
from trainier.util.object_id import object_id
from trainier.util.sec_cookie import Codec
from trainier.web.question.service import QuestionService
from trainier.web.quiz.service import QuizService
from trainier.web.quiz.take.service import TakeService

blueprint: Blueprint = Blueprint('quiz_take', __name__, url_prefix='/quiz/take')

codec: Codec = Codec(Config.default.SECRET_KEY)

trunk_fields = {
    Trunk.entity_id,
    Trunk.code,
    Trunk.en_trunk,
    Trunk.cn_trunk,
    Trunk.source,
    Trunk.level,
}

option_fields = {
    Option.entity_id,
    Option.en_option,
    Option.cn_option,
}

# pic_fields = {
#     Pic.entity_id,
#     Pic.code,
#     Pic.name,
#     Pic.data,
#     Pic.source,
#     Pic.order_num,
#     Pic.comment,
# }


class QuestionVO:
    # TODO:
    pass


class API:
    @staticmethod
    @blueprint.route('/api/<quiz_id>', methods={'GET'})
    def api_take_start(quiz_id: str) -> Response:
        """
        初始化，读取数据生成cookie
        :param quiz_id:
        :return:
        """
        try:
            quiz: Quiz = QuizService.select_quiz_by_id(quiz_id)
            if quiz is None:
                abort(404)
            quiz_dict: Dict = labelify(quiz)
            quiz_dict['quiz_inst_id'] = object_id()
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
        index: int = post_dict['index'] - 1
        answer: List[str] or str = post_dict['answer']
        marked: bool = post_dict['marked']
        question: Dict = quiz_dict['questions'][index]
        question['answer'] = answer
        question['marked'] = marked
        return quiz_dict

    @staticmethod
    def __deal_switch(quiz_dict: Dict, switch_to_index: int) -> Dict:
        """
        根据 question_idx 从数据库内读取题目数据
        :param quiz_dict:
        :param switch_to_index:
        :return:
        """
        # 读取新的数据
        question: Dict = quiz_dict['questions'][switch_to_index - 1]
        qid: str = question['id']
        trunk: Trunk = None
        options: List[Option] = None
        # pics: List[Pic] = None
        trunk, options, pics = QuestionService.select_trunks_options_pics_by_id(qid)
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
        # for option_dict in options_dict:
        #     option_dict['is_true'] = False
        # answer: List[str] or str = question['answer']
        # for ch in answer:
        #     idx: int = string.ascii_uppercase.find(ch.strip().upper())
        #     if idx < 0 or idx >= len(answer):
        #         raise ValueError('something wrong in answer {} of {}'.format(answer, str(question)))
        #     options_dict[idx]['is_true'] = True

        # pics_dict: Dict = labelify(pics, pic_fields)
        ret: Dict = dict(
            trunk=trunk_dict,
            options=options_dict,
            # pics=pics_dict,
        )
        return ret

    @staticmethod
    def __list_status(quiz_dict: Dict) -> List[Dict]:
        # 题目列表
        questions: List[Dict] = [dict(marked=question['marked'], answer=question['answer']) for question in
                                 quiz_dict['questions']]
        return questions

    @staticmethod
    @blueprint.route('/api/<int:switch_to_index>', methods={'POST'})
    def api_take_submit_switch(switch_to_index: int) -> Response:
        try:
            cookie: str = request.cookies.get('quiz')
            cookie = unquote(cookie)
            quiz_dict: Dict = codec.dec_dict(cookie)
            if switch_to_index > 0:
                # 保存提交的结果
                data: bytes = request.data
                try:
                    post_dict: Dict = json.loads(data)
                    quiz_dict = API.__deal_submit(quiz_dict, post_dict)
                except json.JSONDecodeError:
                    # 如果没有提交数据或提交有误，就不进行更新
                    pass
                ret: Dict = API.__deal_switch(quiz_dict, switch_to_index)
                ret['questions'] = API.__list_status(quiz_dict)
            else:
                # 第一次请求
                ret: Dict = API.__deal_switch(quiz_dict, 1)
                ret['questions'] = API.__list_status(quiz_dict)
            enc_quiz: str = codec.enc_dict(quiz_dict)

            res: Response = make_response(json.dumps(ret).encode())
            res.content_type = 'application/json; charset=utf-8'
            res.set_cookie('quiz', value=enc_quiz)
            return res
        except Exception as e:
            logger.error(str(e))
            abort(500)

    @staticmethod
    @blueprint.route('/api/', methods={'DELETE'})
    def api_exit() -> Response:
        try:
            res: Response = make_response(json.dumps(dict(result=True)).encode())
            res.delete_cookie('quiz')
            res.content_type = 'application/json; charset=utf-8'
            return res
        except Exception as e:
            logger.error(str(e))
            abort(500)

    @staticmethod
    @blueprint.route('/api/', methods={'PUT'})
    def api_submit() -> Response:
        try:
            cookie: str = request.cookies.get('quiz')
            cookie = unquote(cookie)
            quiz_dict: Dict = codec.dec_dict(cookie)
            data: bytes = request.data
            try:
                post_dict: Dict = json.loads(data)
                quiz_dict = API.__deal_submit(quiz_dict, post_dict)
            except json.JSONDecodeError:
                # 如果没有提交数据或提交有误，就不进行更新
                pass
            quiz_id: str = quiz_dict.get('entity_id')
            random_choice: bool = quiz_dict.get('random_choice')
            quiz_inst_id: str = quiz_dict.get('quiz_inst_id')
            questions: List[Dict] = quiz_dict['questions']
            results: List[Result] = list()
            for question_dict in questions:
                trunk_id: str = question_dict.get('id')
                result: Result = Result(
                    entity_id=object_id(),
                    quiz_id=quiz_id,
                    quiz_inst_id=quiz_inst_id,
                    trunk_id=trunk_id,
                    answer=''
                )
                answer: List[str] or str = question_dict.get('answer')
                options: List[Option] = QuestionService.select_options_by_trunk_id(trunk_id)
                if random_choice:
                    seed: int = question_dict.get('seed')
                    random.seed(seed)
                    random.shuffle(options)
                answers: List[str] = list()
                for ch in answer:
                    ch: str = ch.strip().upper()
                    idx: int = string.ascii_uppercase.find(ch)
                    if idx >= 0 and idx < len(options):
                        option: Option = options[idx]
                        answers.append(option.entity_id)
                result.answer = ','.join(answers)
                results.append(result)
            TakeService.save(results)
            res: Response = make_response(json.dumps(dict(result=True)).encode())
            res.delete_cookie('quiz')
            res.content_type = 'application/json; charset=utf-8'
            return res
        except Exception as e:
            logger.error(str(e))
            abort(500)


class View:
    @staticmethod
    @blueprint.route('/', methods={'GET'})
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

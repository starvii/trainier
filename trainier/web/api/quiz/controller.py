#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from concurrent.futures import Executor, ThreadPoolExecutor
from typing import Dict, List

from playhouse.shortcuts import model_to_dict, dict_to_model
from tornado.concurrent import run_on_executor

from trainier.dao.model import Trunk, Quiz
from trainier.util.logger import Log
from trainier.util.value import process_page_parameters, jsonify
from trainier.web.api import ErrorInQueryError
from trainier.web.api.quiz.service import QuizService


class QuizController:
    executor: Executor = ThreadPoolExecutor(4)

    @run_on_executor
    def query_quizzes(self, arguments: Dict, body: bytes) -> str:
        """
        优先使用arguments中的参数（get / post urlencoded），如果没有再采用body中的参数（json），如果再没有则使用默认值
        :param arguments:
        :param body:
        :return:
        """
        try:
            page, size, keyword = process_page_parameters(arguments, body)
            quiz, count = QuizService.select_quizzes(page, size, keyword)


            quiz_list: List[Dict] = [model_to_dict(t, only={
                Quiz.entity_id,
                Quiz.code,
                Quiz.name,
                Quiz.comment,
            }) for t in quiz]
            for q in quiz_list:
                questions: str = quiz.questions
                c: int = len([q.strip() for q in questions.split(',') if len(q.strip()) > 0])
                q['count'] = c
            result: Dict = dict(
                result=1,
                quizzes=quiz_list,
                count=count,
            )
        except ErrorInQueryError as e:
            Log.trainier.error(e)
            result: Dict = dict(
                result=0,
                error='query error',
            )
        except Exception as e:
            Log.trainier.error(e)
            result: Dict = dict(
                result=0,
                error='query error',
            )
        return jsonify(result)

    @run_on_executor
    def query_quiz(self, entity_id: str, referer: str) -> str:
        quiz: Quiz = QuizService.select_quiz_by_id(entity_id)

        questions: str = quiz.questions
        question_list: List = [q.strip() for q in questions.split(',') if len(q.strip()) > 0]
        quiz_dict: Dict = model_to_dict(quiz, exclude={Quiz.db_id, Quiz.questions})
        quiz_dict['questions'] = question_list
        result: Dict = dict(
            result=1,
            quiz=quiz_dict,
        )
        return jsonify(result)


    @run_on_executor
    def create_quiz(self, http_body: bytes) -> str:
        try:
            request_dict: Dict = json.loads(http_body)
            if 'quiz' not in request_dict:
                raise ValueError(f'there is no quiz in http body {http_body}')
            quiz_dict: Dict = request_dict['quiz']
            quiz: Quiz = dict_to_model(Quiz, quiz_dict, True)
            QuizService.save(quiz)
            return jsonify(dict(result=1))
        except Exception as e:
            Log.trainier.error(e)
            return jsonify(dict(result=0, error='save error'))

    @run_on_executor
    def modify_quiz(self, entity_id: str, http_body: bytes) -> str:
        try:
            request_dict: Dict = json.loads(http_body)
            if 'quiz' not in request_dict:
                raise ValueError(f'there is no quiz in http body {http_body}')
            quiz_dict: Dict = request_dict['quiz']
            quiz: Quiz = dict_to_model(Quiz, quiz_dict, True)
            if quiz.entity_id != entity_id:
                raise ValueError(f'entity_id from url {entity_id} is not equal to json {quiz.entity_id}')
            QuizService.save(quiz)
            return jsonify(dict(result=1))
        except Exception as e:
            Log.trainier.error(e)
            return jsonify(dict(result=0, error='save error'))

    @run_on_executor
    def delete_quiz(self, entity_id: str) -> str:
        Log.trainier.debug('delete: entity_id = %s', entity_id)
        return jsonify(dict(
            result=0,
            error='NotImplementedError',
        ))

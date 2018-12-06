#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
from concurrent.futures import Executor
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict, List

from tornado.concurrent import run_on_executor

from trainier.config import AppConfig
from trainier.dao.model import Quiz, Trunk
from trainier.util.sec_cookie import Codec
from trainier.util.value import b32_obj_id, jsonify
from trainier.web.api.question.service import QuestionService
from trainier.web.api.quiz.service import QuizService
from trainier.web.api.quiz.take.service import TakeService


class QuizInstance:
    class Question:
        def __init__(self) -> None:
            self.trunk_id = ''
            self.marked = 0
            self.answer = ''
            self.option_seed = -1

        # def to_dict(self) -> Dict:
        #     d = {}
        #     for k, v in self.__dict__.items():
        #         if not k.startswith('_'):
        #             d[k] = v
        #     return d

        # def from_dict(self, question: Dict):
        #     for k, v in question.items():
        #         if k in self.__dict__:
        #             self.__dict__[k] = v

    def __init__(self) -> None:
        self.instance_id: str = ''
        self.quiz_id: str = ''
        self.trunks: List[QuizInstance.Question] = []


    # def to_dict(self) -> Dict:
    #     d = {}
    #     for k, v in self.__dict__.items():
    #         if not k.startswith('_'):
    #             if isinstance(v, QuizInstance.Question):
    #                 d[k] = v.to_dict()
    #             else:
    #                 d[k] = v
    #     return d

    # def from_dict(self, inst: Dict):
    #     pass

    def from_model(self, model: Quiz):
        self.quiz_id = model.entity_id
        questions: str = model.questions
        ql: List = [_q.strip() for _q in questions.split(',') if len(_q.strip()) > 0]
        if len(ql) == 0:
            raise ValueError('no question in the quiz')
        for qid in ql:
            q: QuizInstance.Question = QuizInstance.Question()
            q.trunk_id = qid
            if model.random_choice:
                q.option_seed = random.randint(0, 65535)
            self.trunks.append(q)
        if model.random_trunk:
            random.shuffle(model.trunks)

    def get_index_status(self) -> List[Dict]:
        return [dict(a=len(t.answer)>0, m=t.marked) for t in self.trunks]



class QuizActionController:
    """
    题目答案提交时使用以下格式：
    {"trunk_id": "option_id"}
    {"trunk_id": ["option_id1", "option_id2"]}
    {"trunk_id": {"sub_trunk_id1": "option_id1", "sub_trunk_id2": ["option_id2", "option_id3"]}}
    """
    executor: Executor = ThreadPoolExecutor(4)
    codec: Codec = Codec(AppConfig.SECRET)

    @run_on_executor
    def quiz_start(self, quiz_id: str) -> (str, str):
        """
        开始测验
        :param quiz_id:
        :return: json, encrypted cookie
        """
        quiz: Quiz = QuizService.select_quiz_by_id(quiz_id)
        inst: QuizInstance = QuizInstance()
        inst.instance_id = time.strftime('%Y%m%d%H%M') + b32_obj_id()[12:]
        inst.from_model(quiz)
        # 取第一题的数据
        trunk: Trunk = QuestionService.select_trunk_by_id(inst.trunks[0].trunk_id)
        trunk_view: Dict = TakeService.trunk_to_dict(trunk)
        index: List[Dict] = inst.get_index_status()
        cookie: str = self.codec.enc_obj(inst)
        result = dict(result=1, index=index, trunk=trunk_view, answer='', current=0)
        return jsonify(result), cookie

    @run_on_executor
    def quiz_switch(self, quiz_id: str, cookie: str, switch: int, submit: Dict) -> (str, str):
        inst: QuizInstance = self.codec.dec_obj(cookie)
        if inst.quiz_id != quiz_id:
            raise ValueError('quiz_id not equal')
        self._merge_submit(inst, submit)
        trunk_index: QuizInstance.Question = inst.trunks[switch]
        answer: str = trunk_index.answer
        trunk: Trunk = QuestionService.select_trunk_by_id(trunk_index.trunk_id)
        trunk_view: Dict = TakeService.trunk_to_dict(trunk)
        index: List[Dict] = inst.get_index_status()
        c: str = self.codec.enc_obj(inst)
        result = dict(result=1, index=index, trunk=trunk_view, answer=answer, current=0)
        return jsonify(result), c

    @run_on_executor
    def quiz_submit(self, quiz_id: str, cookie: str, submit: Dict) -> str:
        inst: QuizInstance = self.codec.dec_obj(cookie)
        if inst.quiz_id != quiz_id:
            raise ValueError('quiz_id not equal')
        self._merge_submit(inst, submit)

    @staticmethod
    def _merge_submit(inst: QuizInstance, submit: Dict):
        idx: int = submit.get('current')
        marked: int = submit.get('marked')
        answer: str = submit.get('answer')
        current: QuizInstance.Question = inst.trunks[idx]
        current.marked = marked
        current.answer = answer
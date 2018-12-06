#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
from concurrent.futures import Executor
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict, List

from tornado.concurrent import run_on_executor

from trainier.config import AppConfig
from trainier.dao.model import Quiz, Trunk, Result
from trainier.util.sec_cookie import Codec
from trainier.util.value import b32_obj_id, jsonify
from trainier.web.api.quiz.service import QuizService
from trainier.web.api.quiz.take.service import TakeService, QuizInstance, TrunkIndex


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
        trunk: Trunk = inst.trunks[0].get_trunk()
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
        trunk_index: TrunkIndex = inst.trunks[switch]
        answer: str = trunk_index.answer
        trunk: Trunk = trunk_index.get_trunk()
        trunk_view: Dict = TakeService.trunk_to_dict(trunk)
        index: List[Dict] = inst.get_index_status()
        c: str = self.codec.enc_obj(inst)
        result = dict(result=1, index=index, trunk=trunk_view, answer=answer, current=switch)
        return jsonify(result), c

    @run_on_executor
    def quiz_submit(self, quiz_id: str, cookie: str, submit: Dict) -> str:
        inst: QuizInstance = self.codec.dec_obj(cookie)
        if inst.quiz_id != quiz_id:
            raise ValueError('quiz_id not equal')
        self._merge_submit(inst, submit)
        results: List[Result] = [t.get_result() for t in inst.trunks]
        for r in results:
            r.quiz_id = quiz_id
            r.instance_id = inst.instance_id
            r.user_id = 'test_user'
        TakeService.save(results)
        return jsonify(dict(result=1))

    @staticmethod
    def _merge_submit(inst: QuizInstance, submit: Dict):
        idx: int = submit.get('current')
        marked: int = submit.get('marked')
        answer: str = submit.get('answer')
        current: TrunkIndex = inst.trunks[idx]
        current.marked = marked
        current.answer = answer
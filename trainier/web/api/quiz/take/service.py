#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random
from collections import deque
from typing import List, Dict, Deque, Set

from trainier.dao.model import Trunk, Option, Result, Quiz
from trainier.dao.orm import db
from trainier.util.logger import Log
from trainier.util.value import b32_obj_id, jsonify
from trainier.web.api.question.service import QuestionService


class TrunkIndex:
    def __init__(self, index: int) -> None:
        self.index: int = index
        self.trunk_id: str = ''
        self.marked: int or bool = 0
        self.answer: Dict = dict()
        self.option_seed: int = -1

    def get_current(self) -> Dict:
        r: Dict = dict(
            index=self.index,
            marked=1 if self.marked else 0,
            answer=self.answer,
        )
        return r

    def get_status(self) -> Dict:
        answer: int = 1
        if self.answer is None or len(self.answer) == 0:
            answer = 0
        else:
            for _, v in self.answer.items():
                if len(v) == 0:
                    answer = 0
                    break
        r: Dict = dict(
            m=1 if self.marked else 0,
            a=answer,
        )
        return r

    def set_current(self, current: Dict) -> None:
        marked = current.get('marked')
        if marked is not None:
            self.marked = marked
        answer = current.get('answer')
        if answer is not None:
            self.answer = answer

    def get_trunk(self) -> Trunk:
        trunk: Trunk = QuestionService.select_trunk_by_id(self.trunk_id)
        if self.option_seed >= 0:
            random.seed(self.option_seed)
        queue: Deque[Trunk] = deque([trunk])
        while len(queue) > 0:
            trunk_cur: Trunk = queue.popleft()
            if hasattr(trunk_cur, 'trunks'):
                queue.extend(trunk_cur.trunks)
            else:
                if self.option_seed >= 0:
                    random.shuffle(trunk_cur.options)
        return trunk

    def get_result(self) -> Result:
        result: Result = Result()
        result.trunk_id = self.trunk_id
        result.answer = jsonify(self.answer)
        result.is_true = True

        trunk: Trunk = QuestionService.select_trunk_by_id(self.trunk_id)
        queue: Deque[Trunk] = deque([trunk])
        correct_dict: Dict = {}
        while len(queue) > 0:
            trunk_cur: Trunk = queue.popleft()
            if hasattr(trunk_cur, 'trunks'):
                queue.extend(trunk_cur.trunks)
            else:
                correct_options: Set[str] = set([o.entity_id for o in trunk_cur.options if o.is_true])
                n: int = len(correct_options)
                if n < 1:
                    raise ValueError(f'no correct option of trunk({trunk_cur.entity_id})')
                elif n == 1:
                    correct_dict[trunk_cur.entity_id] = correct_options.pop()
                elif n < len(trunk_cur.options):
                    correct_dict[trunk_cur.entity_id] = correct_options
                else:
                    raise ValueError(f'too many correct option of trunk({trunk_cur.entity_id})')
        if len(correct_dict) != len(self.answer):
            result.is_true = False
            return result
        for k, v in self.answer.items():
            if k not in correct_dict:
                result.is_true = False
                return result
            a: str or Set = correct_dict[k]
            if isinstance(v, str):
                if v != a:
                    result.is_true = False
                    return result
            elif isinstance(v, List):
                if len(v) != len(a):
                    result.is_true = False
                    return result
                for e in v:
                    if e not in a:
                        result.is_true = False
                        return result
            else:
                result.is_true = False
                return result
        # answer_dict: Dict = json.loads(self.answer)
        # queue: Deque[Dict] = deque([answer_dict])
        # while len(queue) > 0:
        #     dct: Dict = queue.popleft()
        #     for k, v in dct.items():
        #         if isinstance(v, Dict):
        #             queue.append(v)
        #         elif isinstance(v, List):
        #             if k not in correct_dict:
        #                 result.is_true = False
        #                 return result
        #             s: Set[str] = correct_dict[k]
        #             if not isinstance(s, Set):
        #                 result.is_true = False
        #                 return result
        #             if set(v) != s:
        #                 result.is_true = False
        #                 return result
        #         elif isinstance(v, str):
        #             if k not in correct_dict:
        #                 result.is_true = False
        #                 return result
        #             if v != correct_dict[k]:
        #                 result.is_true = False
        #                 return result
        #         else:
        #             result.is_true = False
        #             return result
        return result


class QuizInstance:
    def __init__(self) -> None:
        self.instance_id: str = ''
        self.quiz_id: str = ''
        self.trunks: List[TrunkIndex] = []

    def from_model(self, model: Quiz) -> None:
        self.quiz_id = model.entity_id
        questions: str = model.questions
        ql: List = [_q.strip() for _q in questions.split(',') if len(_q.strip()) > 0]
        if len(ql) == 0:
            raise ValueError('no question in the quiz')
        for idx, qid in enumerate(ql):
            q: TrunkIndex = TrunkIndex(idx)
            q.trunk_id = qid
            if model.random_choice:
                q.option_seed = random.randint(0, 65535)
            self.trunks.append(q)
        if model.random_trunk:
            random.shuffle(model.trunks)

    def get_index_status(self) -> List[Dict]:
        return [t.get_status() for t in self.trunks]


class TakeService:

    @staticmethod
    def multi_choice(src: Trunk, dst: Dict):
        if hasattr(src, 'options'):
            l: List[Option] = [o for o in src.options if o.is_true]
            n: int = len(l)
            if n < 1:
                raise ValueError(f'no correct option of trunk({src.entity_id})')
            elif n == 1:
                dst['multi_choice'] = 0
            elif n < len(src.options):
                dst['multi_choice'] = 1
            else:
                raise ValueError(f'too many correct option of trunk({src.entity_id})')

    @staticmethod
    def trunk_to_dict(trunk: Trunk):
        trunk_exclude = {
            Trunk.db_id,
            Trunk.en_trunk_text,
            Trunk.cn_trunk_text,
            Trunk.explanation,
            Trunk.source,
            Trunk.comment,
            Trunk.order_num,
            Trunk.parent_id,

        }
        option_exclude = {
            Option.db_id,
            Option.trunk_id,
            Option.code,
            Option.order_num,
            Option.is_true,
            Option.comment,
        }
        return QuestionService.trunk_to_dict(trunk, trunk_exclude, option_exclude, [QuestionService.view_trunk_length, TakeService.multi_choice])

    @staticmethod
    def save(results: List[Result]):
        with db.connection_context():
            with db.transaction() as tx:
                try:
                    for result in results:
                        result.entity_id = b32_obj_id()
                        result.save()
                    tx.commit()
                except Exception as e:
                    tx.rollback()
                    Log.trainier.error(e)
                    raise e

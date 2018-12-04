#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from trainier.dao.model import Quiz
from trainier.dao.orm import db
from trainier.util.logger import Log
from trainier.util.value import b32_obj_id


class QuizService:
    @staticmethod
    def select_quizzes(page: int, size: int, keyword: str) -> (List[Quiz], int):
        query = Quiz.select(Quiz.entity_id, Quiz.code, Quiz.name, Quiz.questions, Quiz.comment)
        if keyword is not None and len(keyword) > 0:
            k: str = '%' + keyword + '%'
            query = query.where(
                (Quiz.code ** k) |
                (Quiz.name ** k)
            )
        c: int = query.count()
        l: List[Quiz] = [q for q in query.paginate(page, size)]
        return l, c

    @staticmethod
    def select_quiz_by_id(quiz_id: str) -> Quiz or None:
        return Quiz.get(Quiz.entity_id == quiz_id)

    @staticmethod
    def save(quiz: Quiz) -> None:
        with db.transaction() as tx:
            try:
                _id: str = quiz.entity_id
                if quiz.entity_id is None or len(_id.strip()) == 0:
                    quiz.entity_id = b32_obj_id()
                    quiz.save()
                else:
                    Quiz.update(
                        code = quiz.code,
                        name = quiz.name,
                        questions = quiz.questions,
                        random_trunk = quiz.random_trunk,
                        random_choice = quiz.random_choice,
                        comment = quiz.comment
                    ).execute()
                tx.commit()
            except Exception as e:
                tx.rollback()
                Log.trainier.error(e)
                raise e

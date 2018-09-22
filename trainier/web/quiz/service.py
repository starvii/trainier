#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List
from sqlalchemy.sql import or_
from sqlalchemy.orm.query import Query
from trainier.dao.model import Quiz, Trunk
from trainier.dao.orm import Session
from trainier.util.logger import logger
from trainier.util.object_id import object_id
from trainier.web.question.service import QuestionService


class QuizService:
    @staticmethod
    def select_quiz(page: int = 1, size: int = 10, keyword: str = '') -> (List[Quiz], int):
        session: Session = Session()
        try:
            if len(keyword) > 0:
                k: str = '%' + keyword + '%'
                q: Query = session.query(Quiz).filter(or_(
                    Quiz.code.like(k),
                    Quiz.name.like(k)
                ))
            else:
                q: Query = session.query(Quiz)
            c: int = q.count()
            l: List[Quiz] = q.offset((page - 1) * size).limit(size).all()
            return l, c
        except Exception as e:
            logger.error(e)
            return None, 0
        finally:
            session.close()

    @staticmethod
    def select_quiz_by_id(quiz_id: str) -> Quiz or None:
        session: Session = Session()
        try:
            if quiz_id is not None and len(quiz_id) > 0:
                quiz: Quiz = session.query(Quiz).filter(Quiz.entity_id == quiz_id).one_or_none()
                return quiz
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close()

    @staticmethod
    def save(quiz: Quiz) -> None:
        session: Session = Session()
        try:
            if quiz.entity_id is None or len(quiz.entity_id.strip()) == 0:
                quiz.entity_id = object_id()
                session.add(quiz)
            else:
                session.merge(quiz)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(e)
            raise e
        finally:
            session.close()

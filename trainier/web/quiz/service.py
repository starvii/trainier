#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List
from sqlalchemy.sql import or_
from sqlalchemy.orm.query import Query
from trainier.dao.model import Quiz
from dao.orm import Session
from util.logger import logger


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
            return None, -1
        finally:
            session.close()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Dict, Set
from sqlalchemy.sql import or_
from trainier.orm import Session
from util.object_id import object_id
from trainier.model import Trunk, Option, Pic
from trainier.logger import logger


class QuestionService:
    @staticmethod
    def select_trunk_by_id(entity_id: str) -> Trunk or None:
        pass

    @staticmethod
    def select_options_by_trunk_id(trunk_id: str) -> List[Option]:
        pass

    @staticmethod
    def select_pics_by_trunk_id(trunk_id: str) -> List[Pic]:
        pass

    @staticmethod
    def select_trunks(keyword: str = '', page: int = 1, pagesize: int = 20) -> List[Trunk] or None:
        session: Session = Session()
        try:
            if len(keyword) > 0:
                k: str = '%' + keyword + '%'
                l: List[Trunk] = session.query(Trunk).filter(or_(
                    Trunk.enTrunk.like(k),
                    Trunk.cnTrunk.like(k),
                    Trunk.analysis.like(k),
                    Trunk.source.like(k),
                    Trunk.comment.like(k)
                )).offset((page - 1) * pagesize).limit(pagesize).all()
            else:
                l: List[Trunk] = session.query(Trunk).offset((page - 1) * pagesize).limit(pagesize).all()
            return l
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close()

    @staticmethod
    def save(trunk: Trunk, options: List[Option], pics: List[Pic]) -> bool:
        pass


class QuizService:
    @staticmethod
    def quiz():
        pass

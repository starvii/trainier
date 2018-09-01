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
    def select_trunk_options_pics_by_id(entity_id: str) -> (Trunk, List[Option], List[Pic]) or None:
        session: Session = Session()
        try:
            trunk: Trunk = session.query(Trunk).filter(Trunk.entityId == entity_id).one_or_none()
            if trunk is None:
                return None
            options: List[Option] = session.query(Option).filter(Option.trunkId == entity_id).all()
            pics: List[Pic] = session.query(Pic).filter(Pic.trunkId == entity_id).all()
            return trunk, options, pics
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close()

    @staticmethod
    def select_trunks(keyword: str = '', page: int = 1, pagesize: int = 20) -> (List[Trunk], int) or None:
        """

        :param keyword:
        :param page:
        :param pagesize:
        :return: (data: List[Trunk], record size: int)
        """
        session: Session = Session()
        try:
            if len(keyword) > 0:
                k: str = '%' + keyword + '%'
                q = session.query(Trunk).filter(or_(
                    Trunk.enTrunk.like(k),
                    Trunk.cnTrunk.like(k),
                    Trunk.analysis.like(k),
                    Trunk.source.like(k),
                    Trunk.comment.like(k)
                ))
            else:
                q = session.query(Trunk)
            c: int = q.count()

            l: List[Trunk] = q.offset((page - 1) * pagesize).limit(pagesize).all()
            return l, c
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close()

    @staticmethod
    def save(trunk: Trunk, options: List[Option], pics: List[Pic]) -> bool:
        pass

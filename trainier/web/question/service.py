#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from typing import List
from sqlalchemy.sql import or_
from dao.orm import Session
from trainier.util.object_id import object_id
from dao.model import Trunk, Option, Pic
from util.logger import logger


class QuestionService:
    @staticmethod
    def select_trunk_options_pics_by_id(entity_id: str) -> (Trunk, List[Option], List[Pic]) or None:
        session: Session = Session()
        try:
            trunk: Trunk = session.query(Trunk).filter(Trunk.entity_id == entity_id).one_or_none()
            if trunk is None:
                return None
            options: List[Option] = session.query(Option).filter(Option.trunk_id == entity_id).all()
            pics: List[Pic] = session.query(Pic).filter(Pic.trunk_id == entity_id).all()
            return trunk, options, pics
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close()

    @staticmethod
    def select_trunks(page: int = 1, size: int = 10, keyword: str = '') -> (List[Trunk], int):
        """

        :param keyword:
        :param page:
        :param size:
        :return: (data: List[Trunk], record size: int)
        """
        session: Session = Session()
        try:
            if len(keyword) > 0:
                k: str = '%' + keyword + '%'
                # 查询符合条件的option
                lst: List[Option] = session.query(Option).filter(or_(
                    Option.en_option.like(k),
                    Option.cn_option.like(k)
                )).all()
                entity_ids = set([o.trunk_id for o in lst])
                # 查询符合条件的pic
                lst: List[Pic] = session.query(Pic).filter(or_(
                    Pic.name.like(k),
                    Pic.source.like(k)
                )).all()
                entity_ids = entity_ids.union(set([o.trunk_id for o in lst]))

                q = session.query(Trunk).filter(or_(
                    Trunk.code.like(k),
                    Trunk.en_trunk.like(k),
                    Trunk.cn_trunk.like(k),
                    Trunk.analysis.like(k),
                    Trunk.source.like(k),
                    Trunk.comment.like(k),
                    Trunk.entity_id.in_(entity_ids)
                ))
            else:
                q = session.query(Trunk)
            c: int = q.count()

            l: List[Trunk] = q.offset((page - 1) * size).limit(size).all()
            return l, c
        except Exception as e:
            logger.error(e)
            return None, -1
        finally:
            session.close()

    @staticmethod
    def save(trunk: Trunk, options: List[Option], pics: List[Pic] = None) -> None:
        session: Session = Session()
        try:
            if trunk.entity_id is None or len(trunk.entity_id.strip()) == 0:
                trunk_id = object_id()
                trunk.entity_id = trunk_id
                session.add(trunk)
                if options is not None and len(options) > 0:
                    for i, option in enumerate(options):
                        option.entity_id = object_id()
                        option.trunk_id = trunk_id
                        option.order_num = i
                        if trunk.code is not None and len(trunk.code.strip()) > 0:
                            option.code = trunk.code.strip() + '-' + string.ascii_uppercase[i]
                    session.add_all(options)
                if pics is not None and len(pics) > 0:
                    for i, pic in enumerate(pics):
                        pic.entity_id = object_id()
                        pic.trunk_id = trunk_id
                        pic.order_num = i
                        if trunk.code is not None and len(trunk.code.strip()) > 0:
                            pic.code = trunk.code.strip() + '-' + str(i)
                    session.add_all(options)
            else:
                trunk_id = trunk.entity_id
                session.merge(trunk)
                # assert len(options) >= 4
                if options is not None and len(options) > 0:
                    for i, option in enumerate(options):
                        option.trunk_id = trunk_id
                        option.order_num = i
                        if trunk.code is not None and len(trunk.code.strip()) > 0:
                            option.code = trunk.code.strip() + '-' + string.ascii_uppercase[i]
                        if option.entity_id is None or len(option.entity_id.strip()) == 0:
                            option.entity_id = object_id()
                            session.add(option)
                        else:
                            session.merge(option)
                if pics is not None and len(pics) > 0:
                    for i, pic in enumerate(pics):
                        pic.trunk_id = trunk_id
                        pic.order_num = i
                        if trunk.code is not None and len(trunk.code.strip()) > 0:
                            pic.code = trunk.code.strip() + '-' + str(i)
                        if pic.entity_id is None or len(pic.entity_id.strip()) == 0:
                            pic.entity_id = object_id()
                            session.add(pic)
                        else:
                            session.merge(pic)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(e)
            raise e
        finally:
            session.close()

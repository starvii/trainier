#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
from typing import List, Set

from sqlalchemy.sql import or_

from trainier.dao.model import Trunk, Option
from trainier.dao.orm import Session
from trainier.util.logger import logger
from trainier.util.object_id import object_id
from util.value import html_strip

ROOT_NODE = 'root'


class QuestionService:
    @staticmethod
    def select_trunk_by_id(entity_id: str) -> Trunk or None:
        """
        options, pic 在 trunk._options trunk._pics 中
        :param entity_id:
        :return:
        """
        session: Session = Session()
        try:
            trunk: Trunk = session.query(Trunk).filter(Trunk.entity_id == entity_id).one_or_none()
            if trunk is None:
                return None
            trunks: List[Trunk] = [trunk]
            if trunk.parent == ROOT_NODE:
                queue: List[Trunk] = [trunk]
                while len(queue) > 0:
                    trunk_parent: Trunk = queue.pop(0)
                    trunk_children: List[Trunk] = session.query(Trunk).filter(
                        Trunk.parent == trunk_parent.entity_id).order_by(
                        Trunk.order_num.asc()).all()
                    if len(trunk_children) > 0:
                        trunks.extend(trunk_children)
                        trunk_parent.__setattr__('_trunks', trunk_children)
                        for trunk in trunk_children:
                            if trunk.parent == ROOT_NODE:
                                queue.append(trunk)
            for trunk in trunks:
                if trunk.parent != ROOT_NODE:
                    options: List[Option] = session.query(Option).filter(
                        Option.trunk_id == trunk.entity_id).order_by(
                        Option.order_num.asc()).all()
                    trunk.__setattr__('_options', options)
                # trunk.__dict__['_pics']: List[Pic] = session.query(Pic).filter(
                #     Pic.trunk_id == trunk.entity_id).order_by(
                #     Pic.order_num.asc()).all()
            return trunks[0]
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close()

    @staticmethod
    def select_options_by_trunk_id(trunk_id: str) -> List[Option]:
        """
        供保存测验结果时使用
        :param trunk_id:
        :return:
        """
        session: Session = Session()
        try:
            options: List[Option] = session.query(Option).filter(Option.trunk_id == trunk_id).order_by(
                Option.order_num.asc()).all()
            return options
        except Exception as e:
            logger.error(e)
        finally:
            session.close()

    @staticmethod
    def select_trunks(page: int = 1, size: int = 10, keyword: str = '', ids: List[str] = None) -> (List[Trunk], int):
        """
        :param keyword:
        :param page:
        :param size:
        :param ids:
        :return: (data: List[Trunk], record size: int)
        """
        session: Session = Session()
        try:
            q = session.query(Trunk).filter(or_(Trunk.parent.is_(None), Trunk.parent == '', Trunk.parent == ROOT_NODE))
            if keyword is not None and len(keyword) > 0:
                k: str = '%' + keyword + '%'
                # 由于新加了组合题目，此处处理有点麻烦，暂时禁用从选项、图片查询功能
                # 查询符合条件的option
                # lst: List[Option] = session.query(Option).filter(or_(
                #     Option.en_option.like(k),
                #     Option.cn_option.like(k)
                # )).all()
                # entity_ids = set([o.trunk_id for o in lst])
                # # 查询符合条件的pic
                # lst: List[Pic] = session.query(Pic).filter(or_(
                #     Pic.name.like(k),
                #     Pic.source.like(k)
                # )).all()
                # entity_ids = entity_ids.union(set([o.trunk_id for o in lst]))
                q = q.filter(or_(
                    Trunk.code.like(k),
                    Trunk.en_trunk.like(k),
                    Trunk.cn_trunk.like(k),
                    Trunk.analysis.like(k),
                    Trunk.source.like(k),
                    Trunk.comment.like(k),
                    # Trunk.entity_id.in_(entity_ids)
                ))
            if ids is not None:
                q = q.filter(Trunk.entity_id.in_(ids))
            c: int = q.count()

            l: List[Trunk] = q.order_by(Trunk.order_num.asc()).offset((page - 1) * size).limit(size).all()
            return l, c
        except Exception as e:
            logger.error(e)
            return None, 0
        finally:
            session.close()

    @staticmethod
    def __save_trunk(session: Session, trunk: Trunk):
        if trunk.entity_id is None or len(trunk.entity_id.strip()) == 0:
            trunk_id = object_id()
            trunk.entity_id = trunk_id
            session.add(trunk)
        else:
            session.query(Trunk).filter(Trunk.entity_id == trunk.entity_id).update({
                Trunk.code:trunk.code,
                Trunk.en_trunk: trunk.en_trunk,
                Trunk.en_trunk_text: trunk.en_trunk_text,
                Trunk.cn_trunk: trunk.cn_trunk,
                Trunk.cn_trunk_text: trunk.cn_trunk_text,
                Trunk.analysis: trunk.analysis,
                Trunk.source: trunk.source,
                Trunk.level: trunk.level,
                Trunk.comment: trunk.comment,
                Trunk.order_num: trunk.order_num,
                Trunk.parent: trunk.parent,
            })
            # session.merge(trunk)

    @staticmethod
    def __save_options(session: Session, options: List[Option], trunk: Trunk):
        """
        trunk新增时，删除所有option后再插入
        trunk修改时，修改已有的option，如果某option在数据库中存在，而在提交中不存在，则删除
        :param session:
        :param options:
        :return:
        """
        options_db: List[Option] = session.query(Option).filter(Option.trunk_id == trunk.entity_id).all()
        exist_db_ids: Set[str] = set([i.entity_id for i in options_db])
        write_db_ids: Set[str] = set()
        for option in options:
            if option.entity_id is None or len(option.entity_id.strip()) == 0:
                option.entity_id = object_id()
                session.add(option)
            else:
                session.query(Option).filter(Option.entity_id == option.entity_id).update({
                    Option.trunk_id: option.trunk_id,
                    Option.code: option.code,
                    Option.en_option: option.en_option,
                    Option.cn_option: option.cn_option,
                    Option.is_true: option.is_true,
                    Option.order_num: option.order_num,
                    Option.comment: option.comment,
                })
                # session.merge(option)
            write_db_ids.add(option.entity_id)
        delete_db_ids: Set[str] = exist_db_ids - write_db_ids
        if len(delete_db_ids) > 0:
            session.query(Option).filter(Option.entity_id.in_(delete_db_ids)).delete()

    # @staticmethod
    # def __save_pics(session: Session, pics: List[Pic], trunk_id: str):
    #     pics_db: List[Option] = session.query(Pic).filter(Pic.trunk_id == trunk_id).all()
    #     exist_db_ids: Set[str] = set([i.entity_id for i in pics_db])
    #     write_db_ids: Set[str] = set()
    #     for pic in pics:
    #         if pic.entity_id is None or len(pic.entity_id.strip()) == 0:
    #             pic.entity_id = object_id()
    #             session.add(pic)
    #         else:
    #             session.merge(pic)
    #         write_db_ids.add(pic.entity_id)
    #     delete_db_ids: Set[str] = exist_db_ids - write_db_ids
    #     session.query(Pic).filter(Pic.entity_id.in_(delete_db_ids)).delete()

    @staticmethod
    def save(trunk: Trunk) -> None:
        session: Session = Session()
        queue: List[Trunk] = [trunk]
        try:
            while len(queue) > 0:
                trunk_cur: Trunk = queue.pop(0)
                trunk_children: List[Trunk] = trunk_cur.__dict__.get('_trunks')
                trunk_cur.en_trunk_text = html_strip(trunk_cur.en_trunk)
                trunk_cur.cn_trunk_text = html_strip(trunk_cur.cn_trunk)
                trunk_cur.order_num = 0
                trunk_cur.parent = ''
                if trunk_children is not None:
                    trunk_cur.parent = ROOT_NODE
                    trunk_cur.analysis = ''
                QuestionService.__save_trunk(session, trunk_cur)  # 保存后可获取 trunk_id
                if trunk_children is not None:
                    for idx, trunk_child in enumerate(trunk_children):
                        trunk_child.parent = trunk_cur.entity_id
                        trunk_child.code = '{}({})'.format(trunk_cur.code, idx + 1)
                        trunk_child.order_num = idx
                        queue.append(trunk_child)
                else:  # leaf node
                    trunk_cur.parent = ''
                    options: List[Option] = trunk_cur.__dict__.get('_options')
                    for idx, option in enumerate(options):
                        option.code = '{}-{}'.format(trunk_cur.code, string.ascii_uppercase[idx])
                        option.trunk_id = trunk_cur.entity_id
                        option.order_num = idx
                    QuestionService.__save_options(session, options, trunk_cur)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(e)
            raise e
        finally:
            session.close()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import string
from typing import List, Set, Dict

from peewee import Query

from trainier.dao.model import Trunk, Option
from trainier.dao.orm import db
from trainier.util import const
from trainier.util.logger import Log
from trainier.util.value import b32_obj_id, html_strip
from web.api import CannotFindError, ErrorInQueryError

const.ROOT_NODE = 'root'


class QuestionService:
    @staticmethod
    def _split_code(code: str) -> (int, str):
        """
        将编码分解为书名缩写、版本、章节、题目编号
        :param code:
        :return:
        """
        code = code.upper()
        m = re.match(r'^[A-Z]{1,3}\d{1,2}/\d{1,3}/\S+', code)
        if not m:
            raise ValueError(f'code {code} not match.')
        book: str = re.search(r'^[A-Z]+', code).group()
        version: int = int(re.search(r'\d+', code).group())
        cs = code.split('/')
        chapter: int = int(cs[1])
        question_num: str = cs[2]
        return QuestionService._order_num(book, version, chapter, question_num)

    @staticmethod
    def _order_num(book: str, version: int, chapter: int, question_num: str) -> (int, str):
        """
        根据 code 生成排序编码，一共是 18 位（十进制）
        sqlite int 8 字节 (long long) 整型，
            用来存储有符号的整数，从 -9223372036854775808 到 9223372036854775807(19)
            或者无符号的整数，从 0 到 18446744073709551615(20)
        :param book: space 100
        :param version: space 10
        :param chapter: space 100
        :param question_num: space 1000 + sub-question 100
        :return:
        """
        book_idx: int = string.ascii_uppercase.find(book[0].upper())
        sub_question: int = 0
        if re.match(r'\d+-\d+\(\d+\)', question_num):
            qn = int(question_num.split('-')[0])
            m = re.search(r'(?<=\()\d+(?=\))', question_num)
            sub_question = int(m.group())
        elif re.match(r'\d+-\d+', question_num):
            qn = int(question_num.split('-')[0])
        elif re.match(r'\d+', question_num):
            qn = int(question_num)
        else:
            raise ValueError(f'question_num {question_num} not match.')
        order_num: int = int(
            str(book_idx).rjust(3, '0') + str(version).rjust(2, '0') + str(chapter).rjust(3, '0') + str(qn).rjust(
                4, '0') + str(sub_question).rjust(3, '0'))
        code: str = f'{book}{version}/{chapter}/{question_num}'
        return order_num, code

    @staticmethod
    def select_trunk_by_id(entity_id: str) -> Trunk:
        try:
            trunk: Trunk = Trunk.get(Trunk.entity_id == entity_id)
            if trunk is None:
                raise CannotFindError(None, f'cannot find {entity_id}')
            trunks: List[Trunk] = [trunk]
            if trunk.parent_id == const.ROOT_NODE:
                queue: List[Trunk] = [trunk]
                while len(queue) > 0:
                    trunk_parent: Trunk = queue.pop(0)
                    query: Query = Trunk.select().where(
                        Trunk.parent_id == trunk_parent.entity_id
                    ).order_by(Trunk.order_num.asc())
                    trunk_children: List[Trunk] = [t for t in query]
                    if len(trunk_children) > 0:
                        trunks.extend(trunk_children)
                        trunk_parent.__setattr__('trunks', trunk_children)
                        for trunk in trunk_children:
                            if trunk.parent_id == const.ROOT_NODE:
                                queue.append(trunk)
            for trunk in trunks:
                if trunk.parent_id != const.ROOT_NODE:
                    options: List[Option] = QuestionService.select_options_by_trunk_id(trunk.entity_id)
                    trunk.__setattr__('options', options)
            return trunks[0]
        except Exception as e:
            Log.trainier.error(e)
            raise ErrorInQueryError(e, f'some exception in query id={entity_id}. {e}')

    @staticmethod
    def select_next_prev_by_id(entity_id: str) -> (str, str):
        try:
            trunk: Trunk = Trunk.get(Trunk.entity_id == entity_id)
            if trunk is None:
                return '', ''
            order_num: int = trunk.order_num
            query = Trunk.select(Trunk.entity_id).where((
                (Trunk.parent_id.is_null()) | (Trunk.parent_id == '') | (Trunk.parent_id == const.ROOT_NODE)
            ))
            next_trunk: Trunk = query.where(Trunk.order_num > order_num).order_by(Trunk.order_num.asc()).first()
            prev_trunk: Trunk = query.where(Trunk.order_num < order_num).order_by(Trunk.order_num.desc()).first()
            next_id: str = next_trunk.entity_id if next_trunk is not None else ''
            prev_id: str = prev_trunk.entity_id if prev_trunk is not None else ''
            return prev_id, next_id
        except Exception as e:
            Log.trainier.error(e)
            return '', ''

    @staticmethod
    def select_options_by_trunk_id(trunk_id: str) -> List[Option] or None:
        """
        供保存测验结果时使用
        :param trunk_id:
        :return:
        """
        try:
            options: List[Option] = Option.select().where(Option.trunk_id == trunk_id).order_by(Option.order_num.asc())
            return options
        except Exception as e:
            Log.trainier.error(e)
            return None

    @staticmethod
    def select_trunks(page: int, size: int, keyword: str, ids: List[str] = None) -> (List[Trunk], int):
        try:
            query = Trunk.select().where(
                (Trunk.parent_id.is_null()) | (Trunk.parent_id == '') | (Trunk.parent_id == const.ROOT_NODE)
            )
            if keyword is not None and len(keyword) > 0:
                k: str = '%' + keyword + '%'
                query = query.where(
                    (Trunk.code ** k) |
                    (Trunk.en_trunk_text ** k) |
                    (Trunk.cn_trunk_text ** k) |
                    (Trunk.explanation ** k) |
                    (Trunk.source ** k) |
                    (Trunk.comment ** k)
                )
            if ids is not None:
                query = query.where(Trunk.entity_id.in_(ids))
            c: int = query.count()
            query = query.order_by(Trunk.order_num.asc()).paginate(page, size)
            Log.trainier.debug(query.sql())
            l: List[Trunk] = [t for t in query]
            # 由于增添了新字段，在此处查询时，覆盖原有字段
            for e in l:
                e.en_trunk = e.en_trunk_text
                e.cn_trunk = e.cn_trunk_text
            return l, c
        except Exception as e:
            Log.trainier.error(e)
            raise ErrorInQueryError(e, f'some exception in query page={page}, size={size}, keyword={keyword}, ids={ids}. {e}')

    @staticmethod
    @db.atomic()
    def save(trunk: Trunk) -> None:
        queue: List[Trunk] = [trunk]
        relation: Dict[Trunk, str] = dict()
        with db.transaction() as tx:
            try:
                while len(queue) > 0:
                    trunk_cur: Trunk = queue.pop(0)
                    trunk_children: List[Trunk] = trunk_cur.__dict__.get('trunks')
                    trunk_cur.en_trunk_text = html_strip(trunk_cur.en_trunk)
                    trunk_cur.cn_trunk_text = html_strip(trunk_cur.cn_trunk)
                    trunk_cur.order_num = 0
                    trunk_cur.parent_id = ''
                    if trunk_children is not None:
                        trunk_cur.parent_id = const.ROOT_NODE
                        trunk_cur.analysis = ''
                    if trunk_cur in relation:
                        trunk_cur.parent_id = relation[trunk_cur]  # 保存主题干的ID
                    trunk_cur.order_num, trunk_cur.code = QuestionService._split_code(trunk_cur.code)  # 计算 order_num
                    QuestionService._save_trunk(trunk_cur)  # 保存后可获取 trunk_id
                    if trunk_children is not None:
                        for idx, trunk_child in enumerate(trunk_children):
                            relation[trunk_child] = trunk_cur.entity_id
                            trunk_child.code = f'{trunk_cur.code}({idx + 1})'
                            trunk_child.order_num = idx
                            trunk_child.source = ''
                            trunk_child.level = trunk_cur.level
                            queue.append(trunk_child)
                    else:  # leaf node
                        options: List[Option] = trunk_cur.__dict__.get('options')
                        if options is None:
                            raise ValueError('this is no options of trunk.')
                        for idx, option in enumerate(options):
                            option.code = f'{trunk_cur.code}-{string.ascii_uppercase[idx]}'
                            option.trunk_id = trunk_cur.entity_id
                            option.order_num = idx
                            option.comment = ''
                        QuestionService._save_options(options, trunk_cur)
                tx.commit()
            except Exception as e:
                tx.rollback()
                Log.trainier.error(e)
                raise e

    @staticmethod
    def _save_trunk(trunk: Trunk) -> None:
        if trunk.entity_id is None or trunk.entity_id == '':
            trunk.entity_id = b32_obj_id()
            trunk.save()
        else:
            query = Trunk.update(
                code = trunk.code,
                en_trunk = trunk.en_trunk,
                en_trunk_text = trunk.en_trunk_text,
                cn_trunk = trunk.cn_trunk,
                cn_trunk_text = trunk.cn_trunk_text,
                explanation = trunk.explanation,
                source = trunk.source,
                level = trunk.level,
                comment = trunk.comment,
                order_num=trunk.order_num,
                parent_id=trunk.parent_id,
            ).where(Trunk.entity_id == trunk.entity_id)
            query.execute()

    @staticmethod
    def _save_options(options: List[Option], trunk: Trunk) -> None:
        options_db: List[Option] = [x for x in Option.select().where(Option.trunk_id == trunk.entity_id)]
        exist_db_ids: Set[str] = set([i.entity_id for i in options_db])
        write_db_ids: Set[str] = set()
        for option in options:
            if option.entity_id is None or len(option.entity_id.strip()) == 0:
                option.entity_id = b32_obj_id()
                option.save()
            else:
                query = Option.update(
                    trunk_id = trunk.entity_id,
                    code = option.code,
                    en_option = option.en_option,
                    cn_option = option.cn_option,
                    is_true = option.is_true,
                    order_num = option.order_num,
                    comment = option.comment,
                ).where(Option.entity_id == option.entity_id)
                query.execute()
            write_db_ids.add(option.entity_id)
        delete_db_ids: Set[str] = exist_db_ids - write_db_ids
        if len(delete_db_ids) > 0:
            Option.delete().where(Option.entity_id.in_(delete_db_ids)).execute()


def test():
    print(QuestionService)


if __name__ == '__main__':
    test()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import List, Dict, Set
from sqlalchemy.sql import or_
from trainier.orm import Session
from util.object_id import object_id
from trainier.model import Trunk, Option, Pic
from trainier.logger import logger

OPTION_TITLE_PATTERN = re.compile(r'^[A-J]\.|(?<=\n)[A-J]\.')
TITLE_PREFIX = 'Comptia Security Plus Mock Test'.replace(' ', '').lower()


class ImportService:
    @staticmethod
    def save(trunk: Trunk, options: List[Option]) -> bool:
        session = Session()
        try:
            if trunk.entity_id is None or len(trunk.entity_id.strip()) == 0:
                trunk.entity_id = object_id()
            # session.execute('BEGIN;')
            session.add(trunk)
            for option in options:
                option.trunk_id = trunk.entity_id
                if option.entity_id is None or len(option.entity_id.strip()) == 0:
                    option.entity_id = object_id()
                session.add(option)
            session.commit()
            # session.execute('COMMIT;')
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            session.close()

    @staticmethod
    def save_dict(result: Dict) -> bool:
        trunk: Trunk = Trunk(
            entityId=result['entityId'],
            enTrunk=result['enTrunk'],
            cnTrunk=result['cnTrunk'],
            level=result['level'],
            comment=result['comment'],
            source=result['source'],
            analysis=result['analysis']
        )
        l: List[Option] = list()
        for j, o in enumerate(result['options']):
            opt = Option(
                entityId=o['entityId'],
                trunkId=o['trunkId'],
                enOption=o['enOption'],
                cnOption=o['cnOption'],
                isTrue=o['isTrue'],
                comment=o['comment'],
                orderNum=o['orderNum']
            )
            l.append(opt)
        return ImportService.save(trunk, l)

    @staticmethod
    def split(text: str) -> Dict[str, str]:
        _t: str = text.strip()
        # Chrome复制时会出现的无关文字，先删除
        _t = _t.replace('Show Answer', '')
        _t = _t.replace('Hide Answer', '')
        _t = _t.replace('.hidden-div{ display:none }', '')
        # 如果第一行为标题，则作为source
        p: int = _t.find('\n')
        assert p > 0
        line1: str = _t[:p]
        source: str = ''
        _: str = line1.replace(' ', '').lower()
        if _.startswith(TITLE_PREFIX):
            source = line1.strip()
            _t = _t[p:].strip()
        # 获取题干
        _ = next(re.finditer(r'A\.\s*', _t)).span()
        assert len(_) == 2
        p = _[0]
        enTrunk: str = _t[:p].strip()
        # 获取题目解析
        _t = _t[p:].strip()
        _ = next(re.finditer(r'Correct Answer:\s*', _t)).span()
        assert len(_) == 2
        p0, p1 = _
        _ = _t[p1:]
        p = _.find('\n')
        if p > 0:
            analysis = _[p:].strip()
            answers: str = _[:p]
        else:
            analysis = ''
            answers: str = _
        # 获取正确答案
        answers: List = answers.split(',')
        answers: Set = set([x.strip() for x in answers if len(x.strip()) > 0])
        # 获取选项
        _t = _t[:p0].strip()
        opt_titles: List = [x.strip()[0] for x in OPTION_TITLE_PATTERN.findall(_t)]
        opt_texts: List = [x.strip() for x in OPTION_TITLE_PATTERN.split(_t) if len(x.strip()) > 0]
        assert len(opt_titles) == len(opt_texts)
        options = list()
        for optTitle, optText in zip(opt_titles, opt_texts):
            opt: Dict = dict(
                enOption=optText,
                cnOption='',
                isTrue=optTitle in answers
            )
            options.append(opt)

        return dict(
            enTrunk=enTrunk,
            cnTrunk='',
            comment='',
            source=source,
            analysis=analysis,
            level=0,
            options=options,
        )
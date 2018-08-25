#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import List, Dict, Set
from uuid import uuid4 as guid
from trainier.orm import Session
from trainier.model import Trunk, Option

OPTION_TITLE_PATTERN = re.compile(r'[A-Z]{1}\.\s*')
TITLE_PREFIX = 'Comptia Security Plus Mock Test'.replace(' ', '').lower()

class ImportService:
    @staticmethod
    def save(trunk: Trunk, options: List[Option]) -> bool:
        session = Session()
        try:
            if trunk.entityId is None or len(trunk.entityId.strip()) == 0:
                trunk.entityId = str(guid()).replace('-', '')
            # session.execute('BEGIN;')
            session.add(trunk)
            for option in options:
                option.trunkId = trunk.entityId
                option.entityId = str(guid()).replace('-', '')
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
    def split(text: str) -> Dict[str, str]:
        _t: str = text.strip()
        # 如果第一行为标题，则作为source
        p: int = _t.find('\n')
        line1: str = _t[:p]
        source: str = ''
        _:str = line1.replace(' ', '').lower()
        if _.startswith(TITLE_PREFIX):
            source = line1.strip()
            _t = _t[p:].strip()
        # 获取题干
        p = next(re.finditer(r'A\.\s*', _t)).span()[0]
        enTrunk: str = _t[:p].strip()
        # 获取题目解析
        _t = _t[p:].strip()
        p0, p1 = next(re.finditer(r'Correct Answer:\s*.+(?=\n)', _t)).span()
        analysis = _t[p1:].strip()
        # 获取正确答案
        answers: str = _t[p0:p1]
        answers = answers.split(':')[1].strip()
        answers:List = answers.split(',')
        answers:Set = set([x.strip() for x in answers if len(x.strip()) > 0])
        # 获取选项
        _t = _t[:p0].strip()
        optTitles: List = [x.strip()[0] for x in OPTION_TITLE_PATTERN.findall(_t)]
        optTexts: List = [x.strip() for x in re.split(r'[A-Z]{1}\.\s*', _t) if len(x.strip()) > 0]
        assert len(optTitles) == len(optTexts)
        options = list()
        for optTitle, optText in zip(optTitles, optTexts):
            opt:Dict = dict(
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


def test():
    text: str = '''

    
    CompTIA Security Plus Mock Test Q1717
    
    After a merger between two companies a security analyst has been asked to ensure that the organization’s systems are secured against infiltration by any former employees that were terminated during the transition. Which of the following actions are MOST appropriate to harden applications against infiltration by former employees? (Select TWO)
    
    A. Monitor VPN client access
    B. Reduce failed login out settings
    C. Develop and implement updated access control policies
    D. Review and address invalid login attempts
    E. Increase password complexity requirements
    F. Assess and eliminate inactive accounts
    
    
    Correct Answer: E,F
    Section: Mixed Questions
    '''
    d = ImportService.split(text)
    print(repr(d))


if __name__ == '__main__':
    test()

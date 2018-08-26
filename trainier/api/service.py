#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import List, Dict, Set
from uuid import uuid4 as guid
from trainier.orm import Session
from trainier.model import Trunk, Option

OPTION_TITLE_PATTERN = re.compile(r'^[A-J]{1}\.|(?<=\n)[A-J]{1}\.')
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
                if option.entityId is None or len(option.entityId.strip()) == 0:
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
    def saveDict(result:Dict) -> bool:
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
        _:str = line1.replace(' ', '').lower()
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
        answers:List = answers.split(',')
        answers:Set = set([x.strip() for x in answers if len(x.strip()) > 0])
        # 获取选项
        _t = _t[:p0].strip()
        optTitles: List = [x.strip()[0] for x in OPTION_TITLE_PATTERN.findall(_t)]
        optTexts: List = [x.strip() for x in OPTION_TITLE_PATTERN.split(_t) if len(x.strip()) > 0]
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

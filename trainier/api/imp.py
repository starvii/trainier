#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from logging import Logger
from uuid import uuid4 as guid
from typing import Dict, List
from pathlib import Path
from flask import Flask, Blueprint, Response, request, make_response, abort
from trainier import getFlaskApp
from trainier.orm import Session
from trainier.model import Trunk, Option

blueprint: Blueprint = Blueprint('api-imp', str(Path(__file__).parent.name), url_prefix='/api/import')
instance: Flask = getFlaskApp()
log: Logger = instance.logger


@blueprint.route('/split', methods=('POST',))
def split() -> Response:
    try:
        data: bytes = request.data
        text: str = data.decode()
        r: Dict[str, str] = ImportService.split(text)
        res: Response = make_response()
        res.content_type = 'application/json'
        res.data = json.dumps(r).encode()
        return res
    except:
        abort(500)


@blueprint.route('/save', methods=('POST',))
def save() -> Response:
    try:
        data: bytes = request.data
        j = json.loads(data)
        trunk = Trunk(entityId=j['entityId'].strip(), enTrunk=j['enTrunk'].strip(), cnTrunk=j['cnTrunk'].strip(),
                      comment=j['comment'].strip())
        list: List[Option] = []
        for o in j['options']:
            list.append(Option(enOption=o['enOption'].strip(), cnOption=o['cnOption'].strip(), isTrue=o['answer']))
        r: bool = ImportService.save(trunk, list)
        res: Response = make_response()
        res.content_type = 'application/json'
        res.data = json.dumps(dict(success=True)).encode()
        return res
    except:
        abort(500)


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
        r = dict(
            enTrunk='''Sara, a company's security officer, often receives reports of unauthorized personnel having access codes to the cipher locks of secure areas in the building. Sara should immediately implement which of the following?''',
            cnTrunk='''公司安全主管Sara经常收到未授权人员访问安全区的报告，该安全区已使用密码锁进行防护，Sara应该第一时间采取如下哪种措施？''',
            options=[
                dict(
                    enOption='''Acceptable Use Policy''',
                    cnOption='''可接受使用策略''',
                    answer=False,
                ),
                dict(
                    enOption='''Physical security controls''',
                    cnOption='''物理安全管控''',
                    answer=False,
                ),
                dict(
                    enOption='''Technical controls''',
                    cnOption='''技术管控''',
                    answer=False,
                ),
                dict(
                    enOption='''Security awareness training''',
                    cnOption='''安全意识培训''',
                    answer=True
                ),
            ],
        )
        return r

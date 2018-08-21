#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from logging import Logger
from typing import List
from pathlib import Path
from flask import Flask, Blueprint, request, make_response, Response
from trainier import getFlaskApp
from trainier.orm import Session
from trainier.model import Trunk, Option

blueprint: Blueprint = Blueprint('api-imp', str(Path(__file__).parent.name), url_prefix='/api/import')
instance: Flask = getFlaskApp()
log: Logger = instance.logger


@blueprint.route('/split', methods=('POST',))
def split() -> Response:
    """
    enTrunk
    cnTrunk
    [
        [enOpt][cnOpt][answer]
        ...
    ]
    :return:
    """
    question:bytes = request.data
    question:str = question.decode()
    print(question)
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
                answer=True,
            ),
        ],
    )

    res:Response = make_response()
    res.content_type = 'application/json'
    res.data = json.dumps(r).encode()
    return res


@blueprint.route('/save', methods=('POST',))
def save() -> str:
    pass


class ImportService:
    @staticmethod
    def split(text: str) -> List[str]:
        pass

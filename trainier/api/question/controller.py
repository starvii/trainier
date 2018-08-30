#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from logging import Logger

from typing import Dict, List, Set
from flask import Blueprint, Response, request, make_response, abort
from sqlalchemy.orm.attributes import InstrumentedAttribute
from trainier.model import Trunk, Option
from trainier.util.value import not_none
from trainier.logger import logger
from trainier.api.question.service import QuestionService
from trainier.api.service import entity_to_dict

blueprint: Blueprint = Blueprint('api-q', __name__, url_prefix='/api/q')
log: Logger = logger


@blueprint.route('/', methods=('POST',))
def index() -> Response:
    page: int = 1
    pagesize: int = 20
    keyword: str = ''
    try:
        data: bytes = request.data
        try:
            j: Dict = json.loads(data)
        except json.JSONDecodeError as _:
            j = dict()
        if 'page' in j and type(j['page']) == int:
            page = j['page']
        if 'pagesize' in j and type(j['pagesize']) == int:
            pagesize = j['pagesize']
        if 'keyword' in j and type(j['keyword']) == str:
            keyword = j['keyword']
        trunks: List[Trunk] = QuestionService.select_trunks(keyword, page, pagesize)
        l = list()
        filters: Set[InstrumentedAttribute] = {
            Trunk.entityId,
            Trunk.enTrunk,
            Trunk.cnTrunk,
            Trunk.level
        }
        for t in trunks:
            l.append(entity_to_dict(t, filters))
        res: Response = make_response()
        res.content_type = 'application/json'
        res.data = json.dumps(l).encode()
        return res
    except Exception as e:
        log.error(e)
        abort(500)


@blueprint.route('/save', methods=('POST',))
def save() -> Response:
    try:
        data: bytes = request.data
        j = json.loads(data)
        trunk = Trunk(
            entityId=not_none(j['entityId']),
            enTrunk=not_none(j['enTrunk']),
            cnTrunk=not_none(j['cnTrunk']),
            comment=not_none(j['comment']),
            analysis=not_none(j['analysis']),
            source=not_none(j['source']),
            level=j['level']
        )
        list: List[Option] = []
        for o in j['options']:
            list.append(Option(
                enOption=not_none(o['enOption']),
                cnOption=not_none(o['cnOption']),
                isTrue=o['isTrue']
            ))
        r: bool = ImportService.save(trunk, list)
        res: Response = make_response()
        res.content_type = 'application/json'
        res.data = json.dumps(dict(success=True)).encode()
        return res
    except Exception as e:
        print(e)
        abort(500)

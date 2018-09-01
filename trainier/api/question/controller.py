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
from trainier.api.service import labelify

blueprint: Blueprint = Blueprint('api-q', __name__, url_prefix='/api/q')
log: Logger = logger


@blueprint.route('/', methods=('POST',))
def index() -> Response:
    page: int = 1
    size: int = 10
    keyword: str = ''
    try:
        data: bytes = request.data
        try:
            j: Dict = json.loads(data)
        except json.JSONDecodeError as _:
            j = dict()
        if 'page' in j and type(j['page']) == int:
            page = j['page']
        if 'size' in j and type(j['size']) == int:
            size = j['size']
        if size not in {10, 15, 20, 30, 50, 100}:
            size = 10
        if 'keyword' in j and type(j['keyword']) == str:
            keyword = j['keyword'].strip()
        trunks, c = QuestionService.select_trunks(keyword, page, size)
        fields: Set[InstrumentedAttribute] = {
            Trunk.entityId,
            Trunk.enTrunk,
            Trunk.cnTrunk,
            Trunk.level
        }
        l: List[Dict] = labelify(trunks, fields)
        # 数据简化
        for item in l:
            if len(item['enTrunk']) > 50:
                item['enTrunk'] = item['enTrunk'][:47] + '...'
            if len(item['cnTrunk']) > 50:
                item['cnTrunk'] = item['cnTrunk'][:47] + '...'
        r: Dict = dict(
            page=page,
            size=size,
            total=c,
            keyword=keyword,
            data=l,
        )
        res: Response = make_response()
        res.content_type = 'application/json; charset=utf-8'
        res.data = json.dumps(r).encode()
        return res
    except Exception as e:
        log.error(e)
        abort(500)


@blueprint.route('/<entity_id>', methods=('POST',))
def operation(entity_id: str) -> Response:
    res: Response = make_response()
    res.content_type = 'application/json; charset=utf-8'
    return res
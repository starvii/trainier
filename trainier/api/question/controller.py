#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from logging import Logger
import base64
import binascii
from typing import Dict, List, Set
from flask import Blueprint, Response, Request, request, make_response, abort
from sqlalchemy.orm.attributes import InstrumentedAttribute
from trainier.model import Trunk, Option, Pic
from trainier.logger import logger
from trainier.api.service import dict_to_entity, list_to_entities
from trainier.api.question.service import QuestionService
from trainier.api.service import labelify

blueprint: Blueprint = Blueprint('api-question', __name__, url_prefix='/api/question')
log: Logger = logger


@blueprint.route('/', methods=('POST',))
def dispatch() -> Response or None:
    if 'X-HTTP-Method-Override' in request.headers:
        method = request.headers['X-HTTP-Method-Override']
        if method == 'GET':
            return index(request)
        elif method == 'POST':
            return post()
        else:
            abort(404)
            return
    else:
        return post()


def index(req: Request) -> Response:
    page: int = 1
    size: int = 10
    keyword: str = ''
    try:
        data: bytes = req.data
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


@blueprint.route('/<entity_id>', methods=('GET',))
def get(entity_id: str) -> Response or None:
    if len(entity_id) == 16:
        eid: str = binascii.hexlify(base64.urlsafe_b64decode(entity_id)).decode()
    elif len(entity_id) == 24:
        eid: str = entity_id
    else:
        abort(404)
        return None
    _ = QuestionService.select_trunk_options_pics_by_id(eid)
    if _ is not None and _[0] is not None:
        trunk, options, pics = _
        r: Dict = dict(
            trunk=labelify(trunk),
            options=labelify(options),
            pics=labelify(pics)
        )
        res: Response = make_response()
        res.content_type = 'application/json; charset=utf-8'
        res.data = json.dumps(r).encode()
        return res
    else:
        abort(404)


def post() -> Response or None:
    data: bytes = request.data
    j = json.loads(data)
    log.debug(j)
    trunk: Trunk = Trunk()
    trunk = dict_to_entity(j['trunk'], trunk)
    options = list_to_entities(j['options'], Option())
    pics = list_to_entities(j['pics'], Pic())

    b: bool = QuestionService.save(trunk, options, pics)

    res: Response = make_response()
    res.content_type = 'application/json; charset=utf-8'
    res.data = json.dumps(dict(result=b)).encode()
    return res


@blueprint.route('/<entity_id>', methods=('POST',))
def put(entity_id: str) -> Response or None:
    if len(entity_id) == 16:
        eid: str = binascii.hexlify(base64.urlsafe_b64decode(entity_id)).decode()
    elif len(entity_id) == 24:
        eid: str = entity_id
    else:
        abort(404)
        return None
    data: bytes = request.data
    j = json.loads(data)
    log.debug(j)
    trunk: Trunk = Trunk()
    trunk = dict_to_entity(j['trunk'], trunk)
    if trunk.entityId != eid:
        abort(404)
        return None
    options = list_to_entities(j['options'], Option())
    pics = list_to_entities(j['pics'], Pic())

    b: bool = QuestionService.save(trunk, options, pics)

    res: Response = make_response()
    res.content_type = 'application/json; charset=utf-8'
    res.data = json.dumps(dict(result=b)).encode()
    return res

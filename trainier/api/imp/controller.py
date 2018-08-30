#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from logging import Logger

from typing import Dict, List
from flask import Flask, Blueprint, Response, request, make_response, abort
from trainier import get_flask_app
from trainier.api.imp.service import ImportService
from trainier.model import Trunk, Option
from trainier.util.value import not_none

blueprint: Blueprint = Blueprint('api-imp', __name__, url_prefix='/api/import')
instance: Flask = get_flask_app()
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
    except Exception as e:
        print(e)
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

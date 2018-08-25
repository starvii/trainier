#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from logging import Logger

from typing import Dict, List
from pathlib import Path
from flask import Flask, Blueprint, Response, request, make_response, abort
from trainier import getFlaskApp
from trainier.api.service import ImportService
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
    except Exception as e:
        print(e)
        abort(500)


@blueprint.route('/save', methods=('POST',))
def save() -> Response:
    try:
        data: bytes = request.data
        j = json.loads(data)
        trunk = Trunk(entityId=j['entityId'].strip(), enTrunk=j['enTrunk'].strip(), cnTrunk=j['cnTrunk'].strip(),
                      comment=j['comment'].strip(), analysis=j['analysis'], source=j['source'])
        list: List[Option] = []
        for o in j['options']:
            list.append(Option(enOption=o['enOption'].strip(), cnOption=o['cnOption'].strip(), isTrue=o['isTrue']))
        r: bool = ImportService.save(trunk, list)
        res: Response = make_response()
        res.content_type = 'application/json'
        res.data = json.dumps(dict(success=True)).encode()
        return res
    except:
        abort(500)
